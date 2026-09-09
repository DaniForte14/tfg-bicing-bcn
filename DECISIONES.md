# DECISIONES

> El registro más importante del proyecto.
>
> Tres reglas:
> 1. **Se escribe en el momento en que se toma la decisión**, con la
>    información que había entonces. Nunca reconstruido a posteriori.
> 2. **Las alternativas descartadas son la parte que más rinde**: son el
>    material del capítulo de discusión.
> 3. A0 registra lo que decidió **Dani, con el razonamiento de Dani**.
>
> Las decisiones **no se borran ni se editan**: se marcan como revisadas y
> se añade una entrada nueva.

---

## Plantilla

```
## D-XXX — <título corto>
Fecha: AAAA-MM-DD
Decisión: <qué se decidió, en una o dos líneas>
Contexto: <qué se sabía en ese momento>
Alternativas descartadas:
  - <alternativa> → descartada porque <motivo>
  - <alternativa> → descartada porque <motivo>
Consecuencias: <qué obliga a hacer o impide después>
Estado: vigente | revisada en D-0XX | revertida
```

---

<!-- Las decisiones ya cerradas en CLAUDE.md (target, horizontes,
     validación, baselines, métricas) pueden registrarse aquí como
     D-001... si se quiere dejar constancia de su razonamiento. -->

---

## D-001 — Fuente GBFS en vivo: PBSC, sin fallback
Fecha: 2026-09-10
Decisión: la ingesta en vivo usa
`barcelona.publicbikesystem.net/customer/gbfs/v2/en` como **fuente única**.
No se implementa conmutación automática a `api.bsmsa.eu`. Se actualiza la
§2 del CLAUDE.md en consecuencia.

Contexto: `api.bsmsa.eu` (el endpoint documentado en la §2 original y en
Open Data BCN) devuelve `503 API blocked` desde el 2026-09-09 — ver I-001.
A1 ya había cambiado el endpoint por su cuenta al topárselo caído, sin
registrar la decisión. Comprobado en vivo el 2026-09-10: bsmsa sigue en
503; PBSC responde 200 con 544 estaciones y trae todos los campos que
exige la §3, incluido `num_docks_available` como campo reportado. No se
puede comparar cuál es "más completo" mientras bsmsa esté caído.

Alternativas descartadas:
  - **Parche con fallback** (intentar bsmsa, caer a PBSC si falla) → era mi
    primera opción, y la descarté por dos motivos. El que me hizo dudar
    primero: más código y más que explicar en la memoria. El que
    realmente decidió: A0 señaló que un fallback automático puede
    conmutar de fuente a mitad de la serie en vivo sin que yo me entere,
    con dos vocabularios distintos de tipo de bici, y eso obliga a marcar
    el origen fila a fila y a duplicar ramas en las features. Es un caso
    borde permanente a cambio de conservar una etiqueta de "oficial".
  - **Esperar a que bsmsa vuelva** → descartada porque lleva caído desde
    ayer, no hay plazo anunciado, y mientras tanto no se ingesta nada.
    Los datos en vivo no se recuperan a posteriori.

Consecuencias:
  - La memoria debe declarar en el capítulo de datos que la fuente en vivo
    no es la que documenta Open Data BCN, y por qué.
  - El desglose por tipo de bici llega como `vehicle_types_available`
    (`ICONIC`/`BOOST`/`FIT`/`EFIT`), no como `num_bikes_available_types`
    (§3). Hace falta un mapeo verificado contra el feed `vehicle_types`.
  - Queda abierta Q-001: chequeo periódico a bsmsa. Si vuelve, comparar
    ambas respuestas en el mismo instante. Si son idénticas, confirma la
    hipótesis de que bsmsa es solo un proxy WSO2 por delante de PBSC, y
    eso se documenta. Si difieren, se revisa esta decisión con una D-0XX
    nueva.

Nota de trazabilidad: el razonamiento de descarte del fallback lo aportó
A0 en la conversación del 2026-09-10; Dani lo evaluó y lo hizo suyo. Se
registra así para no atribuir a Dani un argumento que no originó.
Estado: vigente
