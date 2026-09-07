# Secuencia de Contactores y Dependencias - Gancho Principal
**Fuente:** 3 audios 2026-09-02 01:03-01:06 `TRANSC_WhatsApp Ptt 2026-09-02 at 01.03.28/01.05.01/01.06.02.txt` + `R81187_REV3 pClosedMap`
**Fecha:** 2026-09-02

## Subida (más simple, serie + quita resistencias progresivo)
- **Puntos:** +1: M+H, +2: M+H+1A, +3: +2A, +4: +3A, +5: +4A, +6 (solo principal): +5A
- **Regla de oro:** Para que entre un contactor, debe estar antes el que lo antecede. 2A requiere 1A, 3A requiere 2A, 4A requiere 3A, **5A requiere 4A** antes cerrado. Además **H** debe estar sí o sí para subida.
- **pClosedMap principal subida:** MIH en +1..6, 1A +2..6, 2A +3..6, 3A +4..6, 4A +5..6, 5A solo +6.

## Bajada (más complicada)
- **5A en bajada:** Según cuadro secuencia, **5A y 4A solo están presentes en los primeros 2 puntos de bajada** (-1, -2). **4A persiste un punto más hasta el 3º** (-3). Es decir: -1: 4A+5A, -2: 4A+5A, -3: 4A, luego se van.
- **Alimentación bobina 5A:** Viene por **línea 13 del máster de control**, y esa línea 13 **se ve interrumpida solamente por el contacto auxiliar del 4A**. Por lo tanto, si no hay voltaje en el contacto auxiliar del 4A, no está llegando desde el máster principal hacia bobina 5A.
- **Caso observado:** 5A no cerraba en bajada, 4B dijo bien "contacto anterior debe estar presente para 5A en bajada (1 y 2)". Al decirle "no tengo energía en bobina 5A" no supo responder. Al añadir "tampoco tengo voltaje en contactos auxiliares del 4A", entendió que para 5A debe estar antes 4A y dedujo falta de llegada desde máster por línea 13.

## Para el modelo
- En **subida**, si preguntan por 5A en +6 y 1A-4A cierran bien pero bobina 5A tiene 48V, no preguntar por 1A sino verificar continuidad física de 5A o línea 13.
- En **bajada**, si 5A no cierra en -1/-2 y no hay voltaje en bobina 5A ni en auxiliar de 4A, hipótesis #1 es falta de energía desde máster por línea 13 interrumpida por 4A.
- Siempre respetar orden: falta energía bobina -> previo no cierra -> conductor master línea 13 -> plata master.

## Cita
- Fuente: `SECUENCIA_CONTACTORES_20260902.md` + `MANUAL_GANCHO_PRINCIPAL.md pClosedMap`
