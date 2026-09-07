# Corrección DB - No es 1L/4A, es H (subida) y 2L (bajada)
**Fuente:** Audios `04.00.59.ogg` (122s) + `04.06.01.ogg` (136s) `TRANSC_04.00.59.txt` + `TRANSC_04.06.01.txt`
**Error previo:** Modelo 4B interpretó "DB se alimenta via línea 1L y depende de 4A (-1/-2 hasta -3)" - eso corresponde a **5A (línea13 via 4A)**, no a DB. Fue error de interpretación del modelo, no de tu transcripción.

## Correcto DB bobina
- **Subida (toda la secuencia):** DB se energiza via **H** → contacto NA de H alimentado por **línea 6 (MH6)** → **línea 31** → nodo con **resistencia en paralelo a NC de DB** + **NC de H** → bobina DB. Circuito negativo: **línea26→negativo**, vía **línea51 NC de DB** + **línea31 NA de H**.
- **Bajada (a partir de 2L):** DB se energiza via **2L** → contacto NA de 2L → **línea7** que viene via **NA de 1L** → nodo con **NA de 2L + NA de 3L + NC de H** + resistencia → DB. Por eso a partir del 2º pto bajada DB siempre queda sellado (ya sea via 2L o 3L), haciendo el juego 2L↔3L.

## Qué mantener de lo previo
- 5A sí depende de 4A via línea13 y 4A en -1/-2 persiste hasta -3 (eso es correcto para 5A, no para DB).

## Para el modelo
- Si preguntan por DB en bajada y no energiza, verificar **2L y línea7 via 1L**, no 4A.
- Si preguntan por 5A en bajada y no hay voltaje en bobina 5A ni en aux de 4A, verificar **línea13**.

Citar: `DB_CORRECCION_20260902.md` + `SECUENCIA_CANONICA_20260902.md`
