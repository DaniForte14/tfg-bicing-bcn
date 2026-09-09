# DUDAS

> Cola de cosas a resolver más adelante que **no bloquean ahora**.
> Registro operativo: no va a la memoria.
>
> Lo que bloquea no va aquí: va a `ESTADO.md` como bloqueo.

---

## Plantilla

```
## Q-XXX — <pregunta>
Fecha: AAAA-MM-DD
Contexto: <por qué surge>
Solución mientras siga abierta: <con qué se trabaja entretanto y por qué
  eso no bloquea. Si resulta que sí bloquea, esto no es una duda: va a
  ESTADO.md>
Cómo resolverla: <el paso concreto que la cierra, y qué se hace con cada
  resultado posible>
Respuesta: <cuando se encuentre, con fecha>
Estado: abierta | resuelta | descartada
```

**Regla de este registro:** toda duda abierta lleva escrito con qué se
está trabajando mientras tanto. "Pendiente" a secas no dice si el
proyecto está avanzando o parado.

---

## Abiertas

## Q-001 — ¿Es `api.bsmsa.eu` solo un proxy por delante del feed de PBSC?
Fecha: 2026-09-10
Contexto: bsmsa devuelve 503 de pasarela WSO2 (I-001) y se ha adoptado
PBSC como fuente en vivo única (D-001). Hipótesis sin verificar: BSM es
el operador y PBSC el proveedor de la plataforma, así que bsmsa podría
ser una capa intermedia por delante del mismo backend. Si se confirma,
PBSC no es una fuente alternativa sino la de arriba, y la objeción de
"fuente no oficial" desaparece.

Solución mientras siga abierta: **no bloquea nada**. La ingesta corre
contra PBSC según D-001, y el proyecto avanza sin depender de esta
respuesta. Es una duda de justificación para la memoria, no un bloqueo
técnico — por eso está aquí y no en `ESTADO.md`.

Cómo resolverla: chequeo periódico barato a bsmsa. Si vuelve a responder,
descargar ambas respuestas en el mismo instante y compararlas campo a
campo.
  - Idénticas → hipótesis confirmada. Va al capítulo de calidad de datos
    como argumento de que la fuente adoptada es la de aguas arriba.
  - Distintas → se revisa D-001 con una entrada nueva, con el diff
    concreto delante.

Respuesta: — (pendiente de que bsmsa vuelva a responder)
Estado: abierta

## Resueltas

- —
