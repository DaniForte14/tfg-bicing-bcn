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
Respuesta: <cuando se encuentre, con fecha>
Estado: abierta | resuelta | descartada
```

---

## Abiertas

## Q-001 — ¿Es `api.bsmsa.eu` solo un proxy por delante del feed de PBSC?
Fecha: 2026-09-10
Contexto: bsmsa devuelve 503 de pasarela WSO2 (I-001) y se ha adoptado
PBSC como fuente en vivo unica (D-001). Hipotesis sin verificar: BSM es
el operador y PBSC el proveedor de la plataforma, asi que bsmsa podria
ser una capa intermedia por delante del mismo backend. Si se confirma,
PBSC no es una fuente alternativa sino la de arriba, y la objecion de
"fuente no oficial" desaparece.
Como resolverla: chequeo periodico barato a bsmsa. Si vuelve a responder,
descargar ambas respuestas en el mismo instante y compararlas campo a
campo. Identicas -> hipotesis confirmada, va al capitulo de calidad de
datos. Distintas -> se revisa D-001 con una entrada nueva.
Respuesta: —
Estado: abierta

## Resueltas

- —
