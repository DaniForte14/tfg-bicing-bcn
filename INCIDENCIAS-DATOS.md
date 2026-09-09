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
