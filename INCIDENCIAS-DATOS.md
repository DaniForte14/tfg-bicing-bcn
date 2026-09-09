# INCIDENCIAS DE DATOS

> Cada rareza encontrada en los datos, con fecha, alcance y qué se hizo.
> Se convierte casi literalmente en la sección de **calidad de datos** de
> la memoria.

Qué registrar: huecos en el histórico, estaciones que aparecen o
desaparecen, `num_docks_available` incoherente, timestamps raros o
afectados por el cambio de hora, duplicados, filas fuera de servicio,
respuestas anómalas de GBFS o AEMET.

---

## Plantilla

```
## I-XXX — <título corto>
Fecha detección: AAAA-MM-DD
Fuente: histórico .7z | GBFS station_status | GBFS station_information | AEMET obs | AEMET pred
Alcance: <periodo afectado, estaciones afectadas, nº de filas>
Descripción: <qué se observó exactamente>
Impacto: <sobre qué features / target / particiones afecta>

Solución aplicada: <excluido | marcado | corregido | pendiente>
  Qué se hizo, en concreto: <fichero y commit, no solo la intención>
  Qué NO se hizo, y por qué: <las alternativas que se descartaron>
  Verificación: <qué comprobación demuestra que la solución funciona>
  Recordatorio: las filas fuera de servicio se excluyen y se marcan,
  NO se imputan.

Qué queda vivo: <nada | Q-XXX | pendiente de tal cosa>
Estado: abierta | cerrada
```

**Regla de este registro:** una entrada no es solo el parte del daño.
Se escribe qué se rompió **y qué se hizo con ello**. Un hueco sin acción
registrada es una laguna en el capítulo de calidad de datos, y ese
capítulo es justo el que distingue un TFG serio de uno flojo.

---

<!-- Ya documentado en CLAUDE.md §8 como conocido: hueco en agosto 2020,
     días 7-10. Registrar aquí cuando se confirme sobre los datos reales. -->

---

## I-001 — `api.bsmsa.eu` devuelve 503 «API blocked»
Fecha detección: 2026-09-09 (confirmada de nuevo el 2026-09-10)
Fuente: GBFS `station_status` / `station_information` vía `api.bsmsa.eu`
Alcance: el endpoint entero, todos los feeds, todas las estaciones.
No afecta al histórico `.7z` ya publicado.

Descripción: la petición a
`https://api.bsmsa.eu/ext/api/bsm/gbfs/v2/en/station_status` responde
HTTP 503 con un cuerpo XML de pasarela WSO2, no con JSON GBFS:

    <am:fault xmlns:am="http://wso2.org/apimanager">
      <am:code>700700</am:code>
      <am:message>API blocked</am:message>
      <am:description>This API has been blocked temporarily. Please try
      again later or contact the system administrators.</am:description>
    </am:fault>

El error lo emite la pasarela de gestión de API, no el backend de datos.
Comprobado el 2026-09-10 a las ~01:40 UTC: sigue igual. En paralelo,
`barcelona.publicbikesystem.net/customer/gbfs/v2/en/station_status`
responde 200 con 544 estaciones y esquema GBFS v2 válido.

Impacto: bloquea la ingesta en vivo por el endpoint documentado en la §2
original del CLAUDE.md. Sin impacto sobre el target ni sobre las
particiones: no hay todavía datos en vivo incorporados al dataset.

Solución aplicada: **sustituido el endpoint de la ingesta en vivo por el
feed de PBSC**, como fuente única y sin fallback automático (D-001).

Qué se hizo, en concreto:
  1. `BASE_URL` de `src/ingest_gbfs.py` apunta a
     `https://barcelona.publicbikesystem.net/customer/gbfs/v2/en`.
     Commit `dcad0d8`.
  2. Actualizada la §2 del `CLAUDE.md`, con una nota que deja constancia
     de que añadir conmutación entre endpoints contradice D-001.
  3. Documentada la diferencia de esquema que introduce el cambio: PBSC
     expone el desglose por tipo como `vehicle_types_available`
     (modelos comerciales) y no como `num_bikes_available_types`.

Qué **no** se hizo, y por qué:
  - No se implementó fallback a bsmsa: conmutaría de fuente a mitad de la
    serie sin aviso y obligaría a marcar la procedencia fila a fila.
  - No se imputó ni se rellenó nada. No existen snapshots por el endpoint
    caído, y una ausencia de dato no es un dato.

Verificación: `python src/ingest_gbfs.py --self-check` pasa. El feed de
PBSC devuelve 200 con 544 estaciones y trae `num_docks_available` como
campo reportado, que es el requisito duro de la §3.

Qué queda vivo de esta incidencia: Q-001 — si bsmsa vuelve, comparar
ambas respuestas en el mismo instante antes de plantearse volver.

Estado: abierta (el endpoint sigue caído; la ingesta **no** está
bloqueada gracias a la solución de arriba. Se cierra cuando bsmsa
responda y se resuelva Q-001, o cuando se dé por muerto el endpoint)
