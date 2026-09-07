# Caso Corregido - Contactor 2A no entra en 2º punto de Subida
**Fuente:** Feedback `TRANSCRIPCION_AUDIO_20260901_2033.txt` (186.9s, 2026-09-01 20:33) + `LIMITES_Y_LSR.md`
**Simulador:** Gancho principal, pos +2, `2A` no cierra (según `pClosedMap: 2A = (p 3-6)||(p -2 a -4)` debería cerrar en +2).

## Evaluación de hipótesis previas de qwen3.5-4b
- **Hipótesis 1 (Válida):** Falla de alimentación en bobina del contactor 2A → mantener.
- **Hipótesis 2 (Válida):** Contacto 2A mecánicamente dañado / no hace contacto físico → mantener, pero especificar que es contacto de potencia/plata.
- **Hipótesis 3 (Parcialmente incorrecta):** Límite de subida activado → **descartar para este caso**. El límite bloquea TODA la subida (ningún punto +1 a +6), no solo un contactor. Si fuera límite, no habría ningún movimiento en subida, no solo falla de 2A. Se mencionó como dato pero no aplica a falla puntual de un solo contactor.

## Orden correcto de escalamiento (no intentar resolver todo a la primera)

**Regla:** Pedir más información capa por capa, no dar diagnóstico definitivo inicial.

1. **Verificar secuencia anterior:** ¿Está cerrado correctamente `1A` y su contacto auxiliar? (2A depende de 1A en subir). Si 1A no cierra, 2A tampoco lo hará.
2. **Inspección visual:** ¿Se inspeccionó visualmente el contacto 2A para descartar suciedad, escoriado o desgaste? (ver `CARBONES_FALLAS_TIPICAS.md:4` presión 4-6 PSI)
3. **Prueba de bajada:** ¿El motor responde a mandos de bajada (jogging) o está completamente inactivo? ¿La falla es solo en secuencia de subida o también en bajada? Esto abre abanico: si bajada funciona, es falla específica de lógica de subida; si tampoco bajada, es alimentación general o freno.

## Qué debe preguntar el modelo (questions)
- ¿Se ha verificado que el contacto anterior de la secuencia de subida (1A + auxiliar) está cerrado correctamente?
- ¿Se inspeccionó visualmente el contacto 2A para descartar suciedad/desgaste?
- ¿El equipo responde a bajada (jogging) o está inactivo en ambas direcciones? ¿Falla solo en subida?

## Para RAG
Este caso corrige al modelo: no alucinar límite cuando es falla de un solo contactor, y priorizar preguntas de escalamiento sobre hipótesis definitivas.
