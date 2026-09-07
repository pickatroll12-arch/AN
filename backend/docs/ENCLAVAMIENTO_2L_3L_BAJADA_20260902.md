# Enclavamiento 2L/3L Bajada - VR y Línea 7
**Fuente:** Audio `WhatsApp Ptt 2026-09-02 at 02.10.38.ogg` (234s) `TRANSC_WhatsApp Ptt 2026-09-02 at 02.10.38.txt`
**Complejidad:** Alta, juego lógico con VR, pendiente modelo visión.

## Lógica
- En bajada a través de **línea 7** mientras está **1L** se energiza **2L**.
- **3L se energiza directo cuando se cierra VR** (VR via línea2 + R7). Al energizarse 3L queda **enclavado por sí mismo a través de VR** (contacto NA de 3L).
- Al entrar 3L, **2L sale** (condición: 3L y VR no deben estar antes que 2L). No sale antes para evitar cambio brusco en gancho.
- **Secuencia:** energiza 3L → <1s deja 2L fuera; si 3L sale entra 2L inmediatamente.
- **Falla línea7 o VR:** comportamiento errático entre 2L y 3L (3L solo se activa cuando VR). 3L solo si VR.
- **Prueba control último punto bajada:** VR no se energiza sin paño resistencia con energía (negativo a R7 físico). Hay que activarlo manualmente para ver 2L/3L. Paño sin energía → circuito RC (resistencia+condensador) amortigua entrada/salida.
- **Nota:** Dejar como aparte; ideal modelo con entrada video/imagen para explicar contactos y enclavamiento.

Citar: `ENCLAVAMIENTO_2L_3L_BAJADA_20260902.md`
