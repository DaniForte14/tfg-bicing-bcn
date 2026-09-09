# ESTADO

> Se **reescribe entero** cada vez. No se acumula histórico aquí.
> Última actualización: 2026-09-10

## Hitos propios

No hay entrega externa. Hitos orientativos:

- [ ] Histórico `.7z` descargado y normalizado a esquema único
- [ ] Capítulo de datos (`03-datos.tex`) escrito **antes** de tocar modelado
- [ ] Los tres baselines de la §6 corriendo y comparados
- [ ] Curva de skill frente a horizonte — el resultado central del TFG

## Hecho

- Estructura de directorios, siete registros vivos, `.gitignore`,
  esqueleto de `memoria/`. Commit `56dcde7`.
- **A1 — ingestor GBFS en vivo** (`src/ingest_gbfs.py`, commit `dcad0d8`).
  Idempotente por `last_updated` + deduplicación por contenido.
  Escritura atómica vía fichero temporal. `--self-check` pasa sin red.
  4 snapshots crudos del 2026-09-09 en `data/raw/gbfs/`.
- **D-001** — fuente GBFS en vivo: PBSC, fuente única, sin fallback.
- **I-001** — `api.bsmsa.eu` en `503 API blocked` desde el 2026-09-09.
- **Q-001** — abierta: ¿es bsmsa un proxy por delante de PBSC?
- §2 del `CLAUDE.md` actualizada conforme a D-001.

## En curso

| Agente | Tarea | Rama / carpeta | Desde |
|---|---|---|---|
| — | — | — | — |

Ningún ejecutor activo. Límite §10: máximo 2 a la vez.

## Bloqueado

| Qué | Bloqueado por |
|---|---|
| Features y modelado (A2) | No hay histórico `.7z` descargado. Con 4 snapshots no hay dataset. |
| Backend (A3) y app (A4) | No hay modelo entrenado que servir. |
| Cierre de Q-001 / I-001 | Que `api.bsmsa.eu` vuelva a responder. Sin plazo. |

## Notas de traspaso

**Para A1 — lo que hay que saber antes de tocar nada:**

1. **Fuente en vivo cerrada por D-001**: PBSC, sin fallback. Si añades
   conmutación entre endpoints, contradices una decisión registrada.
2. **`num_docks_available` se lee, nunca se calcula** (§3). El feed de
   PBSC lo trae como campo propio. Verificado el 2026-09-10.
3. **Mapeo de tipos de bici sin resolver.** PBSC da
   `vehicle_types_available` con modelos comerciales
   (`ICONIC`, `BOOST`, `FIT`, `EFIT`); la §3 pide
   `num_bikes_available_types` (mecánica / eléctrica). Verificar contra
   el feed `vehicle_types` del propio GBFS. **No deducir por el nombre.**
4. **Cadencia real del feed sin medir.** Tres snapshots consecutivos del
   2026-09-09 separados 2 y 6 segundos tienen MD5 distintos: pasaron el
   filtro de deduplicación por contenido. O el feed cambia de verdad a
   esa cadencia, o algún campo volátil sin guion bajo se está colando.
   Hay que medirlo **antes** de dejar el poller desatendido: si es lo
   segundo, son miles de ficheros al día.
5. **Riesgo crítico para el join histórico ↔ vivo.** Los `station_id` de
   PBSC son numéricos (`1`…`614`, 544 estaciones hoy). Si no coinciden
   con los del histórico `.7z`, no se pueden unir las dos fuentes, y el
   dataset de entrenamiento depende de ese join. **Comprobar en cuanto
   haya un `.7z` descargado**, antes de construir nada encima.
6. Cada hueco, estación que aparece o desaparece, y rareza de esquema
   va a `INCIDENCIAS-DATOS.md` **según sale**, no al final.
