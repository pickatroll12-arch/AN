# Falla Frenado Dinámico - Armadura Circuito Abierto en Bajada
**Fuente:** Audio `WhatsApp Ptt 2026-09-02 at 01.31.20.ogg` (172s) `TRANSC_WhatsApp Ptt 2026-09-02 at 01.31.20.txt`
**Fecha:** 2026-09-02

## Síntoma
- Al dar **bajar**, la grúa se **acelera demasiado, se sobrerrevoluciona** porque la **armadura queda circuito abierto**, no hay limitante que evite velocidad. Ocurre en bajada, no en subida.

## Causas (falla rebuscada, no común pero crítica)
- **Paño de resistencia frenado dinámico abierto:** interconexión rota en R7, R8, R9, R10.
- **Contactor 2L o 3L dañado:** contacto gore bañado en plata, shunt de conducción, o conductor hacia resistencia.
- **VR:** Se asegura que no suceda en último punto (más crítico), pero puede pasar en puntos anteriores.

## Diagnóstico por punto de bajada
- **Desde punto 2 bajada:** conexión asociada a **2L** rota, hacia R9 y del otro lado R11.
- **1º punto bajada:** línea en **R7 o R10** rota, o conexión del **DB**.
- **Último punto bajada (gancho principal o auxiliar):** directamente **3L** y su conexión al paño vía **R8** o del otro lado vía **R1**.

## Para el modelo
- Preguntar **¿en qué punto de bajada ocurre?** (-1, -2, final). Según punto, hipótesis cambia:
  - Punto 2 → 2L / R9/R11
  - Punto 1 → R7/R10 / DB
  - Último → 3L / R8/R1
- Paño dinámico = R7, R8, R9, R10 (ver `DISPOSICION_RESISTENCIAS_SRC` en `index.html:689`).
- Citar: `FALLA_FRENADO_DINAMICO_20260902.md`
