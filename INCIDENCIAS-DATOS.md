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
Acción tomada: <excluido | marcado | corregido | pendiente>  — recordatorio:
  las filas fuera de servicio se excluyen y se marcan, NO se imputan
Estado: abierta | cerrada
```

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

Acción tomada: **cambiada la fuente en vivo a PBSC** — ver D-001. Sin
fallback automático. No se imputa ni se rellena nada: simplemente no
existen snapshots por ese endpoint. Queda Q-001 para revisar si vuelve.

Estado: abierta (el endpoint sigue caído; se cierra cuando se resuelva
en un sentido o en otro)
