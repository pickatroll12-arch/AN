# Circuito Bajada - DB, 2A, 2L y 3L (Gancho Principal) - Para mente humana
**Fuente:** `DB_CORRECCION_20260902.md` + `ENCLAVAMIENTO_2L_3L_BAJADA_20260902.md` + `SECUENCIA_CANONICA_20260902.md` + audios `04.00.59/04.06.01` + `02.10.38` + `01.17.01`
**Idea:** Aunque circuito sencillo, en bajada se confunde. Siempre bajada es compleja; subida es serie simple.

## DB - Frenado dinámico
- **Qué es:** DB conecta freno dinámico a armadura en bajada (R7-R10 → DB en 1º pto).
- **Subida (toda):** bobina DB via **H** → NA H **línea6 MH6** → **línea31** → nodo **R // NC DB + NC H** → bobina DB. Negativo **línea26** via **línea51 NC DB + línea31 NA H**. Siempre energizado en subida.
- **Bajada:** desde **2L** via **línea7** que viene **NA 1L** → nodo **NA 2L + NA 3L + NC H + R** → DB. Desde 2º pto queda **sellado** (via 2L o 3L) para juego 2L↔3L. Solo NC en 1º pto (abre al energizar y su NA cierra para 2A).

## 2A - Depende de DB
- **Línea 8A** entra directo pero **condicionado a NA de DB**. DB solo presente 1º pto → 2A solo si DB cerró su NA. Si DB no energiza (falla H línea6 o 2L línea7), 2A no entra.

## 2L y 3L - Enclavamiento VR (lo más confuso)
- **2L:** via **línea7 NA 1L** → alimenta **DB**. Entra primero en bajada.
- **3L:** **última velocidad bajada**, via **línea2 + NA DV** con **VR** (VR negativo a **R7**). Al cerrar, **se enclava a sí mismo via NA 3L+VR**.
- **Juego:** al entrar 3L, **sale 2L** (<1s). No sale antes (evita cambio brusco). Si 3L sale, **entra 2L inmediato**. Circuito **RC** amortigua. Falla **línea7 o VR** → comportamiento errático 2L/3L (3L solo si VR).
- **Prueba control último pto:** VR no energiza sin paño con energía (R7). Hay que activarlo manual.

## Resumen tabla bajada
| Contactor | Línea | Condición | Pto |
|-----------|-------|-----------|-----|
| DB | 6 MH6→31 (H) / 7 via 1L→2L (bajada) | NA H o NA 2L/3L+NC H+R | subida toda / bajada≥2L |
| 2A | 8A | NA DB | -1 |
| 2L | 7 via 1L | NA 1L, sale al entrar 3L | bajada |
| 3L | 2 via VR | NA DV, enclavado NA 3L+VR | último |

## Cómo no equivocarse
1. ¿Preguntan DB? → mira H (subida) o 2L línea7 (bajada), NO 4A línea13 (eso es 5A).
2. ¿Preguntan 2A bajada? → verifica DB NA primero.
3. ¿Preguntan 2L/3L? → verifica línea7 y VR R7, no 4A.

Citar: `CIRCUITO_BAJADA_DB_2A_2L_3L_20260902.md`
