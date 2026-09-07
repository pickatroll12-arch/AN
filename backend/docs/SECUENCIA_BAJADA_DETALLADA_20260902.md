# Secuencia Bajada Detallada - Líneas, Interlocks y Retardos
**Fuente:** Audio `WhatsApp Ptt 2026-09-02 at 01.17.01.ogg` (262s) `TRANSC_20260902_0117.txt`
**Claridad:** Alta, pero denso en líneas 8A/10/12/13/14 y enclavamiento 1L/2L. Organizado abajo para RAG.

## Cadena de dependencias (bajada)
- **5A depende de 4A** por **línea 13** (solo contacto auxiliar de 4A la interrumpe).
- **4A depende de 3A** por **línea 12**.
- **3A entra directo** por **línea 10**, sin auxiliar previo en bajada.
- **2A entra directo** pero con condición de **DB** (frenado dinámico) - entra por **línea 8A**. DB solo presente en **1º punto bajada**, normalmente cerrado; al energizarse abre físicamente y su auxiliar NA cierra.
- **1L energiza directo** por **línea 14**. En **1º punto** la línea 14 también energiza **bobina 5A** a través del **contacto NC del DB**; en **2º punto** ya es vía **auxiliar de 4A**.

## Seguridad por enclavamiento (bajada)
- **3A** cierra su circuito al negativo a través de **contacto NC de 1A**.
- **4A** también cierra vía **NC de 1A**.
- **5A** cierra vía **NO de 1L**.
- **Sentido:** Evitar que por falla eléctrica entre un contacto en punto incorrecto. Se usa NC de un contacto exclusivo de subida (1A) y NO de 1L (exclusivo de bajada) como interlock.

## Retardos
- **Contactores con time-delay en bajada:** 2L, 3A, 4A, 5A operan con **TR (time delay)** para que la secuencia no entre de golpe.
- **Ajuste:** 0.6s o 1.2s según puenteo de sus terminales.

## Subida (repaso)
- 5A depende de 4A, 4A de 3A, etc., y **H** siempre. Subida es simple (serie), bajada es compleja por interlocks y retardos.

## Para el modelo
- Si preguntan por 5A en bajada y no hay voltaje en bobina 5A, verificar primero auxiliar de 4A (línea 13) y luego cadena 4A→3A.
- Si preguntan por 3A en bajada y no cierra, verificar NC de 1A.
- No preguntar por "códigos de panel", es DC +/-.
- Citar: `SECUENCIA_BAJADA_DETALLADA_20260902.md` + `SECUENCIA_CONTACTORES_20260902.md`

## Feedback sobre el audio
- **Claro:** Cadena 5A→4A→3A y líneas 13/12/10/8A, y el rol de DB en 1º punto.
- **A mejorar (opcional):** Una tabla línea→contactor para 1L/2L (p. ej. Línea 14→1L directo, Línea 14 via DB-NC→5A en punto 1). Si la entregas en próximo audio como "Línea 14 alimenta 1L y en punto1 a 5A via DB-NC", queda redondo.
