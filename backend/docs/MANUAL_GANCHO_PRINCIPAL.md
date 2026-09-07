# Manual Empírico - Gancho Principal (GRÚA 1)

> **Origen:** Tecnología corriente continua años 40/60 - control por contactores y resistencias. Sin manual de fábrica, solo planos de control/fuerza. Este documento transcribe el funcionamiento real observado.
> **Fuente código:** `C:\Users\PC2B\Documents\Pruebas\AN\index.html:182-213` (P_BOX, P_TERM, P_RACKS, pClosedMap)

## 1. Principio de funcionamiento

Motor DC con regulación por resistencias en serie. Cada `BOX` es una etapa de resistencia. Contactores `M, H, 1L-3L, 1A-5A, DB` cortocircuitan tramos de resistencia para variar corriente/torque. `DB` = frenado dinámico.

*Empírico a completar por técnico:*
- Describir sentido de giro, campo, armadura.
- Cómo entra DB en bajada.

## 2. Arquitectura física

- **28 BOX** distribuidos en 4 racks:
  - `19`  BOX 1-8   - MAIN HOIST RESISTOR RACK #1
  - `19A` BOX 9-16  - MAIN HOIST RESISTOR RACK #2
  - `19B` BOX 17-23 - MAIN HOIST RESISTOR RACK #3
  - `19C` BOX 24-28 - MAIN HOIST RESISTOR RACK #4
- Referencia visual: `gancho principal.png`, `Disposicion resistencias.png`, `C:\Users\PC2B\Documents\Pruebas\AN\index.html:608` PLANO_MAP gancho-principal

### 2.1 Terminales y pines por BOX

| BOX | pinL | pinR | termL | termR | midPin | midTerm |
|-----|------|------|-------|-------|--------|---------|
| 1 |1|7|A|R1|-|-|
| 2 |1|7|A|B|-|-|
| 3 |1|7|C|B|-|-|
| 4 |1|7|C|D|-|-|
| 5 |1|7|E|D|-|-|
| 6 |1|7|E|F|-|-|
| 7 |1|7|G|F|-|-|
| 8 |1|7|G|R11|-|-|
| 9 |1|7|H|R11|-|-|
| 10|1|7|H|J|-|-|
| 11|1|7|K|J|-|-|
| 12|1|7|K|L|5|R2|
| 13|1|7|M|L|-|-|
| 14|1|7|M|R3|-|-|
| 15|1|7|N|R3|-|-|
| 16|1|7|N|P|-|-|
| 17|1|7|R4|P|-|-|
| 18|1|6|R4|R|-|-|
| 19|1|6|S|R|-|-|
| 20|1|6|S|R5|-|-|
| 21|1|6|T|R5|-|-|
| 22|1|6|T|U|-|-|
| 23|1|6|R6|U|-|-|
| 24|1|10|R7|R8|-|-|
| 25|1|10|R7|R8|-|-|
| 26|1|7|V|R8|-|-|
| 27|1|7|V|W|3|R9|
| 28|1|7|V|W|3|R10|

*Nota: BOX 12,27,28 tienen toma intermedia (midPin) que genera degradado en simulador `computeSimP()`.*

## 3. Lógica de contactores por posición

`posP` = -6 (bajar máximo) a +6 (subir máximo), 0 = neutro. `pClosedMap(pos)` `index.html:263-269`:

| Símbolo | Cerrado cuando |
|---------|----------------|
| M | p != 0 |
| H | p > 0 |
| DB | p == 0 \|\| p == -1 |
| 1L | p < 0 |
| 2L | p <= -2 && p >= -5 |
| 3L | p == -6 |
| 1A | p 2-6 |
| 2A | (p 3-6) \|\| (p -2 a -4) |
| 3A | (p 4-6) \|\| (p -1 a -4) |
| 4A | (p 5-6) \|\| (p -1 a -3) |
| 5A | p==6 \|\| (p -1 a -2) |

Panel de estado en simulador: `status-panel` muestra ✅ Cerrado / — Abierto.

## 4. Secuencia paso a paso

### Neutro (pos 0)
- DB cerrado, resto abierto. Resistencias en reposo. Color `P_BOX[6]` = fila 6.

### Subir 1 a 6 (pos +1 .. +6)
- BOX 12 especial: Subir1 todo rojo, Subir2 degradado a R2, Subir3-6 blanco.
- A medida que sube, se cierran 1A-5A progresivamente cortocircuitando resistencias.
- *Completar empírico:* qué se siente (corriente, velocidad, chispa).

### Bajar 1 a 6 (pos -1 .. -6)
- Bajar1: BOX 24-27 azul, BOX28 degradado R10.
- Bajar2-4: BOX12 blanco, BOX27 degradado azul a R9.
- Bajar5-6: BOX1-23 rojo.
- DB solo en -1 y 0.
- *Completar empírico:* frenado dinámico activo, cómo disipa energía.

## 5. Cómo debe funcionar (a completar)

> Escribe aquí en lenguaje natural cómo sabes que está sano:
- Qué contactos deben cerrar en cada paso (tabla arriba).
- Qué cajas deben estar rojas/azules/blancas en cada paso (ver `computeSimP()`).
- Ruido, vibración, amperaje esperado.

## 6. Hipótesis de falla (plantilla - agregar las que recuerdas)

| Síntoma | Posición | Contactos observados | Hipótesis ordenada | Verificación |
|---------|----------|----------------------|--------------------|--------------|
| No eleva, contactor no cierra, hay tensión control | 0 | DB cerrado | 1. Bobina contactor abierta 2. Enclavamiento 1L 3. Cableado A-R1 | Medir tensión en bornes bobina |
| *Agregar fila* | | | | |

## 7. Fallas y soluciones recordadas (a completar)

| Fecha aprox | Síntoma | Causa confirmada | Solución | Resultado |
|-------------|---------|------------------|----------|-----------|
|  |  |  |  |  |
|  |  |  |  |  |

## 8. Planos y fuentes

- `gancho principal.png`
- `Disposicion resistencias.png`
- `PLANO_MAP gancho-principal` base64 en `index.html:608`
- Este manual (versión empírica v0.1)

---
**Próximo paso:** Rellenar secciones 5-7 con tu experiencia. Cada fila que agregues será indexada por el RAG de `server.py:retrieve_docs()` y citada como fuente por `qwen3.5-4b`.
