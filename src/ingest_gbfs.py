"""Ingesta GBFS en vivo — snapshots crudos e inmutables.

CLAUDE.md §9: data/raw/ es inmutable y nunca se edita. Este modulo solo
crea ficheros nuevos; jamas modifica uno existente.

Idempotencia: el nombre del fichero es el `last_updated` que reporta el
feed. Si ya existe, no se reescribe. Reejecutar el poller dentro de la
misma ventana de refresco no duplica nada.

Timestamps: siempre UTC (§9). Las features de calendario se derivan en
Europe/Madrid mas adelante, no aqui.
"""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

# Endpoint del operador (PBSC). El de CLAUDE.md §2 (api.bsmsa.eu) devolvia
# 503 "API blocked" el 2026-09-10 — ver INCIDENCIAS-DATOS.md I-001.
BASE_URL = "https://barcelona.publicbikesystem.net/customer/gbfs/v2/en"

FEEDS = ("station_status", "station_information")

RAW_DIR = Path(__file__).resolve().parent.parent / "data" / "raw" / "gbfs"

TIMEOUT_S = 30
USER_AGENT = "tfg-bicing-bcn/0.1 (proyecto academico UOC)"


def fetch(feed: str, base_url: str = BASE_URL) -> dict:
    """Descarga un feed GBFS y devuelve el JSON parseado."""
    req = urllib.request.Request(
        f"{base_url}/{feed}", headers={"User-Agent": USER_AGENT}
    )
    with urllib.request.urlopen(req, timeout=TIMEOUT_S) as resp:
        payload = json.loads(resp.read().decode("utf-8"))

    # El feed puede responder 200 con un cuerpo que no es GBFS valido.
    if "data" not in payload or "last_updated" not in payload:
        raise ValueError(f"{feed}: respuesta sin 'data' o 'last_updated'")
    return payload


def snapshot_path(feed: str, last_updated: int, raw_dir: Path = RAW_DIR) -> Path:
    """Ruta destino, particionada por dia UTC."""
    day = datetime.fromtimestamp(last_updated, tz=timezone.utc).strftime("%Y-%m-%d")
    return raw_dir / feed / day / f"{last_updated}.json"


def _comparable(data: dict) -> str:
    """Version canonica de `data` para comparar dos snapshots.

    Ignora las extensiones de proveedor (claves con guion bajo delante,
    convencion GBFS). Motivo concreto: `_bluetooth_id` es un
    identificador BLE rotativo — cambia entre peticiones consecutivas sin
    que cambie nada real de la estacion, y sin esto ninguna comparacion
    de contenido llegaria a coincidir nunca.

    Los campos ignorados SI se guardan en el fichero crudo; solo no
    cuentan para decidir si hay cambio.
    """
    def strip(obj):
        if isinstance(obj, dict):
            return {k: strip(v) for k, v in obj.items() if not k.startswith("_")}
        if isinstance(obj, list):
            return [strip(v) for v in obj]
        return obj

    return json.dumps(strip(data), sort_keys=True, ensure_ascii=False)


def _latest_snapshot(feed: str, raw_dir: Path) -> Path | None:
    """Snapshot mas reciente ya guardado de este feed, si hay alguno."""
    snaps = raw_dir.joinpath(feed).rglob("*.json")
    return max(snaps, key=lambda p: int(p.stem), default=None)


def save(feed: str, payload: dict, raw_dir: Path = RAW_DIR) -> tuple[Path, bool]:
    """Guarda el snapshot. Devuelve (ruta, escrito).

    `escrito` es False si el snapshot ya existia: eso es lo que hace la
    ingesta idempotente.

    Dos niveles de deduplicacion:
      1. Mismo `last_updated` -> mismo fichero, no se reescribe.
      2. Contenido identico al ultimo snapshot -> no se guarda.

    El (2) hace falta porque `last_updated` es un reloj global del feed:
    avanza en cada peticion aunque el contenido no cambie. Sin el,
    station_information (metadatos casi estaticos) generaria un fichero
    duplicado en cada pasada del poller.
    """
    path = snapshot_path(feed, payload["last_updated"], raw_dir)
    if path.exists():
        return path, False

    previous = _latest_snapshot(feed, raw_dir)
    if previous is not None:
        old = json.loads(previous.read_text(encoding="utf-8"))
        if _comparable(old.get("data", {})) == _comparable(payload.get("data", {})):
            return previous, False

    path.parent.mkdir(parents=True, exist_ok=True)
    # Fichero temporal + rename atomico: un poller interrumpido no deja
    # JSON truncado en data/raw/.
    tmp = path.with_suffix(".json.part")
    tmp.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    tmp.replace(path)
    return path, True


def poll(feeds: tuple[str, ...] = FEEDS, raw_dir: Path = RAW_DIR) -> dict[str, str]:
    """Una pasada sobre todos los feeds. No lanza: registra el fallo.

    Un fallo de red no debe tumbar el proceso periodico. Los huecos
    resultantes se detectan despues sobre los ficheros, que son la unica
    fuente de verdad.
    """
    result = {}
    for feed in feeds:
        try:
            payload = fetch(feed)
            path, written = save(feed, payload, raw_dir)
            n = len(payload["data"].get("stations", []))
            result[feed] = f"{'guardado' if written else 'ya existia'} {path.name} ({n} estaciones)"
        except (urllib.error.URLError, ValueError, OSError, json.JSONDecodeError) as e:
            result[feed] = f"ERROR {type(e).__name__}: {e}"
    return result


def _self_check() -> None:
    """Comprueba idempotencia y particionado sin tocar la red."""
    import tempfile

    with tempfile.TemporaryDirectory() as tmpdir:
        raw = Path(tmpdir)
        payload = {"last_updated": 1788996324, "ttl": 0, "data": {"stations": []}}

        p1, w1 = save("station_status", payload, raw)
        assert w1 is True, "primera escritura debe escribir"

        p2, w2 = save("station_status", payload, raw)
        assert w2 is False, "segunda escritura debe ser no-op (idempotencia)"
        assert p1 == p2

        # 1788996324 UTC == 2026-09-09 (no 2026-09-10 hora de Madrid):
        # el particionado es por dia UTC, no local.
        assert p1.parent.name == "2026-09-09", p1.parent.name
        assert p1.name == "1788996324.json"

        assert list(raw.rglob("*.json")) == [p1], "no debe duplicar ficheros"
        assert not list(raw.rglob("*.part")), "no debe dejar temporales"

        # Mismo contenido, last_updated distinto -> no se guarda de nuevo.
        movido = dict(payload, last_updated=payload["last_updated"] + 120)
        p3, w3 = save("station_status", movido, raw)
        assert w3 is False, "contenido identico no debe generar snapshot nuevo"
        assert p3 == p1
        assert list(raw.rglob("*.json")) == [p1]

        # Solo cambia una extension de proveedor (_bluetooth_id rotativo)
        # -> no cuenta como cambio real.
        vol = dict(payload, last_updated=payload["last_updated"] + 130,
                   data={"stations": [{"station_id": "1", "_bluetooth_id": "abcd"}]})
        p_v, w_v = save("station_status", vol, raw)
        assert w_v is True, "primer snapshot con estaciones debe guardarse"
        vol2 = dict(vol, last_updated=vol["last_updated"] + 5,
                    data={"stations": [{"station_id": "1", "_bluetooth_id": "9999"}]})
        p_v2, w_v2 = save("station_status", vol2, raw)
        assert w_v2 is False, "_bluetooth_id rotativo no es un cambio real"
        assert p_v2 == p_v

        # Contenido distinto -> si se guarda.
        cambiado = dict(movido, last_updated=payload["last_updated"] + 300,
                        data={"stations": [{"station_id": "2"}]})
        p4, w4 = save("station_status", cambiado, raw)
        assert w4 is True, "contenido distinto debe guardarse"
        assert p4 not in (p1, p_v)
        assert len(list(raw.rglob("*.json"))) == 3

    print("self-check OK")


if __name__ == "__main__":
    import sys

    if "--self-check" in sys.argv:
        _self_check()
    else:
        for feed, status in poll().items():
            print(f"{feed:22s} {status}")
