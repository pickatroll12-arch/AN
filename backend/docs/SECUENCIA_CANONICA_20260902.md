# SECUENCIA CANÓNICA - Gancho Principal (Usar siempre para 1A-5A, subida/bajada)
**Fuente única** fusiona `SECUENCIA_CONTACTORES`+`BAJADA_DETALLADA`+`PROTECCIONES_UV`+`FALLA_DINAMICO`+`JUMPER_TORQUE`+`ENCLAVAMIENTO_2L_3L` + audios 01.03/05/06/17/28/31/02.06/02.10. **Leer este primero.**

## 1) Subida (+1 a +6) - Serie. Sin límites, solo cuadro de secuencia.
| Paso | Contactor que cierra | Quita resistencia | Línea master | Requiere previo |
|------|----------------------|-------------------|--------------|-----------------|
| +1 | M+H | R inicia | - | H |
| +2 | 1A | +R | - | 1A |
| +3 | 2A | +R | - | 1A → 2A |
| +4 | 3A | +R | - | 2A → 3A |
| +5 | 4A | +R | **11** (subida) | 3A → 4A; negativo via **AR time-delay** |
| +6 | 5A (solo GANCHO PRINCIPAL, 28 BOX) | +R | 13 (subida/bajada) | 4A+H → 5A |
- **Regla 5A subida:** `5A = (p===6)` y `pClosedMap: 5A=(p===6)||(p<=-1&&p>=-2)`. Auxiliar/Carro/Avance NO tiene 5A (A_SYMBOLS solo 1A-4A, 20 BOX).
- **Cadena dependencias subida:** 2A requiere 1A, 3A requiere 2A, 4A requiere 3A, 5A requiere 4A.
- **AR (time-delay):** **principal 2A/3A/4A/5A**, **auxiliar 2A/3A/4A** (hasta 4A). Cierran negativo en subida/bajada; si bobina 4A tiene voltaje vs negativo pero no cierra, sospechar AR abierto / bobina abierta, no línea12 (12 es bajada) ver `AR_SUBIDA_LINEA11_20260902.md`.

## 2) Bajada - Compleja. 5A y 4A solo en -1/-2, 4A persiste hasta -3. Paño frenado dinámico R7-R10.
| Contactor | Línea | Condición / auxiliar | Punto bajada |
|-----------|-------|----------------------|--------------|
| 5A | 13 | depende de 4A (solo NC de 4A la interrumpe), negativo via NO de 1L | -1,-2 |
| 4A | 12 | depende de 3A, negativo via NC de 1A | -1,-2,-3 |
| 3A | 10 | entra directo, negativo via NC de 1A | -1,-2 |
| 2A | 8A | entra directo pero con NA de DB | -1 |
| 1L | 14 | directo | -1 |
| DB | - | NC presente solo en 1º pto bajada; al energizar abre y su NA cierra para 2A | 1º pto |
| 1L/5A pto1 | 14 via DB-NC | línea14 alimenta 5A via DB-NC en pto1, luego via 4A en pto2 | pto1 |
| DB | 6 MH6/31 via H (subida) o 7 via 1L→2L (bajada) | subida: NA H línea6→31→R//NC DB→bobina DB (neg línea26/51). bajada: línea7 via NA 1L → NA 2L/3L+NC H → DB sellado desde 2º pto | subida toda / bajada desde 2L |
| 2L | 7 | via 1L, sale al entrar 3L | bajada |
| 3L | 2 via VR | enclavado por sí mismo via NA 3L+VR, hace salir 2L (<1s). Falla línea7/VR → errático 2L/3L | última vel bajada |
- **Interlock seguridad bajada:** 3A y 4A cierran al negativo via NC de 1A (exclusivo subida), 5A via NO de 1L (exclusivo bajada). Evita entrada en pto incorrecto por falla.
- **Time-delay bajada:** 2L, 3A, 4A, 5A tienen retardo 0.6s o 1.2s según puenteo terminales. Circuito RC amortigua entrada/salida 2L/3L. En principal AR para 2A/3A/4A/5A, en auxiliar hasta 4A.
- **DB corrección:** DB NO depende de 4A/línea1L; 5A sí depende de 4A línea13 (-1/-2 hasta -3). DB depende de H (subida línea6) o 2L (bajada línea7 via 1L) ver `DB_CORRECCION_20260902.md`.
- **Jumper torque:** bornera 5-6 puenteado → en punto1 subida entra M+H+1A (más torque), nota plano detalle.

## 3) Protecciones que anteceden a todo
- **UV (230V):** si UV no acciona, nada de secuencia funciona. Antecedido por **1 OL instantáneo (cortocircuito)** y **2 OL time-delay aceite (sobrecarga progresiva)**.
- **VR:** asociado a **3L** última velocidad bajada, alimentado **línea2 + NA DV**, negativo a **R7**. Habilita paño dinámico.

## 4) Falla frenado dinámico (síntoma sobrerrevolución en bajada, armadura circuito abierto)
- **Causa:** paño R7-R10 abierto, o 2L/3L dañado (gore plata/shunt/conductor).
- **Por punto:** pto2 → 2L/R9/R11, pto1 → R7/R10/DB, último pto → 3L/R8/R1. VR asegura último pto pero puede fallar antes.

## 5) Fuerza (subida H serie, bajada 1L dinámico)
- Subida H: LSW600A→900A→1L→H→LS NC→Armadura→LS NC→S1-S2→2 frenos serie V1-V2→R6-1→5A R6/4A R5/3A R4/2A R3/1A R2+R1→M→2L TD→950V→LSW650V→neg. Auxiliar solo hasta 4A.
- Bajada 1L: positivo→1L→LS y3 (R límite) → MHY1→MHR7→R7-R10→DB(pto1)→S2+B1→frenos→aceleración. R9→2L→R11, R8→3L→R1. Límite corta arriba, SR energizado, paso a serie A2-A1-MHS1-campo solo momentáneo.

## Regla para hipótesis (NO preguntar RACK→contactor, sin códigos panel, DC +/-)
1. Falta energía bobina +/- 2. Previo no cierra (para 5A es 4A) 3. Conductor master→panel (línea 13 solo 4A) 4. Contactos plata master aislados (solo tras mediciones).

Citar: `SECUENCIA_CANONICA_20260902.md` + `FUERZA_SUBIDA_BAJADA_20260902.md`.
