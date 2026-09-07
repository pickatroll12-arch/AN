# Diferencias Grúas 1, 2 y 3 - Para filtro MoE del asistente
**Fuente:** Instrucción directa `instruccion.ogg` + `WhatsApp 20:33/20:39` + explicación 21:00 - Usuario AN (2026-09-01)
**Objetivo:** Permitir que el asistente centre su razonamiento solo en el alcance filtrado (Grúa + movimiento), aliviando carga al modelo.

## Grúa 1 (piloto actual)
- **Sistema de avance (traslación puente):** 2 motores.
- **Gancho auxiliar:** 1 solo freno.
- **Ganchos totales:** 2 (principal + auxiliar). Es la configuración base del simulador actual (`gancho-principal` 28 BOX 19/19A/19B/19C, `gancho-auxiliar` 20 BOX 26/26A/26B).
- **Motores gancho principal:** ver `MOTORES_Y_RESISTENCIAS.md` (Mill motor, TAB-Weld TW series).
- **Límites/LSR:** ver `LIMITES_Y_LSR.md`.

## Grúas 2 y 3 (no operativas en piloto, pero distinto hardware)
- **Ganchos totales:** 3 (1 principal + 2 auxiliares: gancho auxiliar norte + gancho auxiliar sur).
- **No confundir con Grúa 1:** Grúa 1 tiene solo 1 auxiliar; Grúas 2/3 tienen 2 auxiliares (norte/sur). Si el filtro es Grúa 1 + gancho auxiliar, es un único auxiliar; si filtro es Grúa 2/3 + gancho auxiliar, hay que distinguir norte vs sur (aún no modelado en `A_BOX/A_TERM`).
- **Estado en código:** `CRANES[1].ready=[]`, `CRANES[2].ready=[]` en `index.html:177-179` - aún no disponible.
- **Implicancia para RAG:** Si pregunta menciona "norte/sur" o "segundo auxiliar", solo aplica a Grúas 2/3.

## Regla para el modelo (filtro = MoE)
- Cuando `context.crane` = GRÚA 1 y `context.module` = Avance → responder con base de 2 motores avance.
- Cuando `context.crane` = GRÚA 1 y `context.module` = Gancho auxiliar → 1 freno.
- Cuando `context.crane` = GRÚA 2/3 y `context.module` = Gancho auxiliar → aclarar que existen norte y sur, no es único.
- Si pregunta es general sin filtro, listar las 3 configuraciones y pedir que filtre.

## Ejemplo trampa para validar filtro
- Pregunta: "contactor 5A" con filtro "GRÚA 1 + gancho auxiliar" → debe responder: 5A no existe en auxiliar (solo principal tiene 5A, ver `MANUAL_GANCHO_PRINCIPAL.md:P_SYMBOLS` incluye 5A, `MANUAL_GANCHO_AUXILIAR.md:A_SYMBOLS` solo 1A-4A).
- Pregunta: "falla en avance" con filtro "GRÚA 1 + avance" → usar dato 2 motores, no mezclar con gancho.

## Para citar en respuestas
- Fuente: `GRUAS_DIFERENCIAS_20260901.md` + `MANUAL_GANCHO_PRINCIPAL.md` / `MANUAL_GANCHO_AUXILIAR.md`
