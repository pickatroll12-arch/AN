# AR Time-Delay Subida y Línea 11 para 4A
**Fuente:** Corrección usuario 2026-09-02 09:40 - 4A no energizaba en subida, luego sí llegaba energía bobina vs negativo pero no cerraba. Modelo sugirió línea12 (bajada) cuando es línea11 subida.
**Fecha:** 2026-09-02

## Líneas
- **4A subida:** se alimenta via **línea 11** (no 12). Línea 12 es bajada (4A depende de 3A en bajada).
- Si bobina 4A tiene voltaje vs negativo pero no cierra → no es falta de alimentación, es **bobina abierta / mecánico / contacto potencia**.

## AR (Time-Delay) en subida y bajada
- **Gancho principal:** **2A, 3A, 4A, 5A** tienen **time-delay (AR)** asociados. **Gancho auxiliar:** también, pero solo hasta **4A** (no tiene 5A).
- En **subida** los contactos **AR** **cierran el circuito con el negativo** para los contactores de aceleración.
- Están presentes en subida y son condición para que bobina cierre a negativo (aunque llegue positivo via línea 11).
- Si AR no cierra a negativo, aunque haya positivo en bobina 4A, no hay corriente y no cierra. Muy confundible con falta de línea.

## Para el modelo
- Si preguntan por **4A en subida (+5)** y hay voltaje bobina vs negativo pero no cierra:
  1. No sugerir línea12 (es bajada)
  2. Sugerir línea11 ok, pero si ya hay voltaje, hipótesis: **AR no cierra a negativo / bobina abierta / mecánico**
  3. Pedir medir **continuidad negativo a través de AR**
- Citar: `AR_SUBIDA_LINEA11_20260902.md` + `SECUENCIA_CANONICA_20260902.md`

## Verificación
- ¿Confirmas que AR de 4A subida va a negativo via TR? ¿Qué AR específico (AR1-4)?
