# Protecciones UV, OL y VR - Bajada Frenado Dinámico
**Fuente:** Audio `WhatsApp Ptt 2026-09-02 at 01.28.24.ogg` (194s) `TRANSC_WhatsApp Ptt 2026-09-02 at 01.28.24.txt`
**Fecha:** 2026-09-02

## UV - Undervoltage
- **Función:** Evita que bajo bajas de voltaje el sistema funcione y vuelva riesgosa la carga.
- **Bobina:** 230V continuo.
- **Antecedido por 2 protecciones:** 1 OL y 2 OL (contactos NA de ambos anteceden a UV).
- **1 OL:** Instantáneo, para falla cortocircuito.
- **2 OL:** Time delay, para sobrecarga progresiva, mediante aceite hace retardo de activación.
- **Regla:** Si UV no acciona, nada de lo que sigue en secuencia funciona.

## VR - Asociado a frenado dinámico bajada
- **Asociado a:** Contactor 3L (última velocidad de bajada).
- **Alimentación:** Línea 2, condición contacto **NA de DV**.
- **Negativo:** Cierra con conexión física a resistencia **R7**.
- **Función:** Permite que al activarse el paño dinámico esté habilitado. Si no, falla de circuito abierto en frenado dinámico (ver audio siguiente).

## Para el modelo
- Si nada funciona (ni subida ni bajada), verificar UV y OLs antes que secuencia.
- Si falla solo última velocidad bajada (3L), verificar VR y DV y R7/R8.
- Citar: `PROTECCIONES_UV_OL_VR_20260902.md`
