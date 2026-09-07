# Fuerza Subida / Bajada - Configuración Serie y Frenado Dinámico
**Fuente:** Audios `02.32.02.ogg` (196s) + `02.37.46.ogg` (341s) `TRANSC_02.32.02.txt` + `TRANSC_02.37.46.txt`
**Claridad:** Alta en subida, media en bajada (límites LS y conexiones MHY1/MHR7). Ver correcciones solicitadas abajo.

## Subida - Ruta H (serie)
De positivo a negativo (izquierda→derecha):
1. Switch cuchilla `LSW600A 250V` → fusible `900A 250V` → **1L** → **H o 1L** (exclusivos, no ambos)
2. Ruta H: **H** → contacto cerrado **LS límite** → **armadura** → contacto cerrado límite → **campo S1-S2** → **2 frenos serie** (gancho principal en grúa 1,2,3: V1 freno1→V2 freno1 → V1 freno2→V2 freno2) → **paño aceleración R6 R5 R4 R3 R2 R1** → contactores cortocircuito: **5A→R6, 4A→R5, 3A→R4, 2A→R3, 1A→R2+R1** (gancho auxiliar solo 4A para abajo, 5 ptos) → **M** → **2L (time delay)** → fusible2 `950V` → cuchilla `LSW650V` → negativo.
- Nota: Repetiste "1L" dos veces (min 0:33 y 0:38) - confirmar si primer 1L es seccionador y segundo es H/1L selector.

## Bajada - Ruta 1L
Entrada positivo, cuchilla, 1L igual pero bifurca a **límite LS y 3** (resistencia límite) → conecta a la derecha a **S2 bobina campo** y abajo del **DB**. Punto entre **1L y LS y 3** va a **A2 armadura y S2 campo**; hacia izquierda **A1 armadura** y **límite NC** llega a **MHY1 → MHR7** (inicio paño dinámico).
- Paño dinámico: **R7 (inicio) → R8 → R9 → R10 (final) → DB** (solo 1º pto bajada). Salida DB = **S2 campo + B1 freno1 → B2 freno1 → B1 freno2 → B2 freno2** → paño aceleración (igual que subida: 5A R6 etc bajo MHR7).
- Intermedias: **R9 asociado a 2L (salta gran parte dinámico, entra por R11)**, **R8 asociado a 3L (conecta en R1)**. Marcas cables `MH + nº resistencia`.

## Límite (LS y 3 / LS y 1 / LS y 4 / LS y 2)
- Al activarse límite: corta circuito por arriba, energiza **resistencia límite**, opera **SR** para que gancho no se embale (dijiste "ancho no se envale" → ¿SR = relé límite?).
- Abre circuito armadura↔frenado dinámico y pasa a circuito serie momentáneo: energía **A2→A1 → límite → MHS1 → vacía bobina campo → A2 → B1 B2 freno1 → B1 B2 freno2 ...** Solo mientras límite activo, no perpetuar, verificar tras mantención.

## Correcciones solicitadas (responde si puedes)
1. Subida: confirma si son **dos frenos serie en gancho principal de las 3 grúas** (dijiste "grúa1 y3, tanto 1,2,3" - ¿todas?).
2. Bajada: **MHY1 vs MHR7 vs MHS1** - ¿son 3 cables distintos o typo? ¿MHY1→MHR7 es correcta?
3. Bajada DB: ¿salida DB es común a **S2 + B1 freno1** tal cual?
4. Límite: ¿**LS y 3, y1, y4, y2** son 4 contactos o borneras del limit switch? ¿SR es relé de seguridad?
5. Auxiliar: ¿confirma 5 ptos subida solo hasta 4A (sin 5A) en auxiliar?

Si confirmas 1-5, actualizo `SECUENCIA_CANONICA.md` sin enredo.
