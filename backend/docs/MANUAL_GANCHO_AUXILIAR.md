# Manual Empírico - Gancho Auxiliar (GRÚA 1)

> **Origen:** Corriente continua 40/60s - contactores y resistencias. Sin manual, solo planos. Transcripción empírica del comportamiento real.
> **Fuente código:** `C:\Users\PC2B\Documents\Pruebas\AN\index.html:216-245` (A_BOX, A_TERM, A_RACKS, aClosedMap)

## 1. Principio de funcionamiento

Similar a gancho principal pero con menos etapas. Motor DC auxiliar con resistencias en serie. Contactores `M, H, 1L-3L, 1A-4A, DB` controlan escalones.

*Empírico a completar:*
- Diferencia de capacidad/torque vs principal.
- Frenado dinámico en bajada.

## 2. Arquitectura física

- **20 BOX** en 3 racks:
  - `26`  BOX 1-8   - AUX. HOIST RESISTOR RACK #1
  - `26A` BOX 9-16  - AUX. HOIST RESISTOR RACK #2
  - `26B` BOX 17-20 - AUX. HOIST RESISTOR RACK #3
- Visual: `gancho auxiliar.png`, `Disposicion resistencias.png`, `PLANO_MAP gancho-auxiliar`

### 2.1 Terminales y pines por BOX

| BOX | pinL | pinR | termL | termR | midPin | midTerm |
|-----|------|------|-------|-------|--------|---------|
| 1 |1|10|A|R1|-|-|
| 2 |1|10|A|B|-|-|
| 3 |1|10|C|B|-|-|
| 4 |1|10|C|D|-|-|
| 5 |1|10|E|D|4|R11|
| 6 |1|10|E|F|-|-|
| 7 |1|10|G|F|3|R2|
| 8 |1|10|G|H|-|-|
| 9 |1|10|J|H|-|-|
|10 |1|7|J|R3|-|-|
|11 |1|7|K|R3|-|-|
|12 |1|7|K|L|-|-|
|13 |1|7|R4|L|-|-|
|14 |1|7|R4|M|-|-|
|15 |1|7|N|M|-|-|
|16 |1|10|N|R5|5|R5|
|17 |1|10|P|R7|-|-|
|18 |1|10|P|R|2|R8|
|19 |1|10|S|R|7|R9|
|20 |1|10|S|R|5|R10|

## 3. Lógica de contactores por posición

`posA` = -5 (bajar máx) a +5 (subir máx), 0 = neutro. `aClosedMap(pos)` `index.html:271-278`:

| Símbolo | Cerrado cuando |
|---------|----------------|
| M | p != 0 |
| H | p > 0 |
| DB | p == 0 \|\| p == -1 |
| 1L | p < 0 |
| 2L | p -2 a -4 |
| 3L | p == -5 |
| 1A | p 2-5 |
| 2A | (p 3-5) \|\| (p -2 a -3) |
| 3A | (p 4-5) \|\| (p -1 a -2) |
| 4A | (p ==5) \|\| (p -1 a -2) |

## 4. Secuencia paso a paso

### Neutro (pos 0)
- DB cerrado. Fila `A_BOX[5]`.

### Subir 1-5
- Cierre progresivo 1A-4A. Sin degradados especiales en subida (a diferencia del principal).
- *Completar empírico:* velocidad, corriente.

### Bajar 1-5
- Bajar1: degradados en BOX7 (blanco→rojo a R2) y BOX20 (blanco→azul a R10) si hasMid.
- Bajar2: BOX7 rojo→blanco? BOX19 azul a R9, BOX7 variación.
- Bajar2-4: BOX19 se mantiene azul a R9.
- Bajar3: BOX7 rojo izquierda→derecha a R2.
- Bajar5: BOX18 azul a R8.
- Ver `computeSimA()` `index.html:376-456` para degradados exactos.
- *Completar empírico:* cómo se comporta DB, resistencias calientes.

## 5. Cómo debe funcionar (a completar)

> Describe en tus palabras:
- Qué contactos cierran en cada paso.
- Qué cajas se ponen rojas/azules.
- Señales de que está sano (sonido contactor, amperaje).

## 6. Hipótesis de falla (plantilla)

| Síntoma | Posición | Contactos | Hipótesis | Verificación |
|---------|----------|-----------|-----------|--------------|
| No baja, DB no entra | -1 | DB abierto | 1. Contacto DB quemado 2. 1L no cierra | Medir continuidad DB |
| *Agregar* | | | | |

## 7. Fallas y soluciones recordadas

| Fecha | Síntoma | Causa confirmada | Solución | Resultado |
|-------|---------|------------------|----------|-----------|
|  |  |  |  |  |
|  |  |  |  |  |

## 8. Planos y fuentes

- `gancho auxiliar.png`
- `PLANO_MAP gancho-auxiliar` en `index.html:610`
- Este manual v0.1

---
**Instrucción RAG:** Cada párrafo que escribas aquí será recuperado por `server.py:retrieve_docs()` y citado por `qwen3.5-4b` como `sources: ["MANUAL_GANCHO_AUXILIAR.md"]`.
