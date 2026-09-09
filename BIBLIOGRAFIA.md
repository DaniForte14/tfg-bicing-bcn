# BIBLIOGRAFIA

> **Lo gestiona Dani, no A0.**
>
> **La salida de un agente no es una fuente citable.** Si un agente hace
> búsquedas web, las URLs consultadas son un log de trabajo, no referencias.
>
> **Regla dura, sin excepciones:** ninguna entrada se añade sin haber
> abierto el DOI o la URL y comprobado que existe y que dice lo que crees
> que dice. Ni una.
>
> Aprobar un resumen ("me parece bien") **no cuenta como verificación**.

## Los dos fallos

1. *Referencia inventada* — autor, título y DOI inexistentes. Fácil de detectar.
2. *Referencia real atribuida a algo que no dice* — paper real, DOI correcto,
   colgado de una afirmación que nunca hizo. **Este es el peligroso.**
   Por eso "Qué dice realmente" se escribe con tus palabras después de leerlo.

Verificar "¿existe el paper?" no basta. Hay que verificar
**"¿respalda lo que estoy diciendo, en las condiciones en que lo digo?"**.

## Flujo

| # | Paso | Quién |
|---|---|---|
| 1 | Buscar candidatos y proponerlos con un resumen breve | Agente |
| 2 | Abrir el paper: abstract + conclusiones (~5 min) | **Dani** |
| 3 | Comprobar que dice lo que decía el resumen **y** que respalda tu afirmación concreta | **Dani** |
| 4 | Escribir "Qué dice realmente" con tus propias palabras | **Dani** |
| 5 | Dar de alta la entrada `B-XXX` y exportar al `.bib` | Agente (formato) |

Los pasos 2, 3 y 4 no se delegan nunca.

---

## Plantilla

```
## B-XXX
Cita: Autor et al. (año). Título. Revista / Congreso / Editorial.
DOI/URL: 10.xxxx/xxxxx
VERIFICADO: sí — AAAA-MM-DD, abierto y leído (mín. abstract + conclusiones)
Tipo: paper | libro | documentación oficial | fuente de datos | norma
Respalda: <qué afirmación concreta de la memoria>
Capítulo: <dónde va>
Qué dice realmente: <1-2 líneas propias>
```

---

## Qué buscar para cada capítulo

| Capítulo | Qué necesitas |
|---|---|
| Introducción / contexto | Movilidad urbana compartida, impacto de los sistemas de bike-sharing |
| Estado del arte | Predicción de demanda y disponibilidad en bike-sharing; métodos usados y horizontes evaluados |
| Datos | Spec GBFS, portal Open Data BCN, licencia CC-BY 4.0, AEMET OpenData — como **fuentes de datos**, no como literatura |
| Metodología | Fuga de datos y validación en series temporales; walk-forward CV; justificación del embargo. **El bloque que más blinda.** |
| Modelos | Papers originales de los algoritmos usados (gradient boosting, etc.) |
| Evaluación | Reglas de puntuación propias (Brier, 1950; Gneiting & Raftery); calibración; métricas bajo desbalanceo |
| Implementación | Documentación técnica oficial (Compose, FastAPI) — como documentación, no como paper |
| Discusión | Estado del arte otra vez: ¿tus resultados concuerdan con lo publicado? |

Registra la referencia **cuando la usas**, no al final.
Exporta a `.bib` (Zotero o similar) desde el principio → `memoria/bibliografia.bib`.

---

## Referencias

<!-- B-001 ... -->
