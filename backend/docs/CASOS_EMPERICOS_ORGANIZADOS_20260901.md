# Casos Empíricos Organizados - Puente Grúa DC (Años 40/60)
**Fuente:** Transcripción `TRANSCRIPCION_AUDIO_20260901.txt` (large-v3, 13m14s, 2026-09-01) - relato empírico sin manual, solo planos control/fuerza. Grúas 1,2,3 - movimientos: ganchos, carros, avances.
**RAG:** Este archivo es indexado por `C:\Users\PC2B\Documents\Pruebas\AN\backend\server.py:retrieve_docs()` y citado como `sources:["CASOS_EMPERICOS_ORGANIZADOS_20260901.md"]`

---

## Caso 0 - Metodología de diagnóstico (válido para cualquier falla)

| Paso | Acción | Detalle empírico |
|------|--------|------------------|
| 1 | Probar secuencia sin fuerza | Dejar tablero sin fuerza, solo control. Pedir al operador que ejecute subir/bajar/avance y ver que contactores hagan cierre mecánico como indican planos. Líneas 1-20 en ganchos indican cada movimiento. |
| 2 | Verificar energización | Si no cierra mecánico, medir en bornera (líneas 1-20) y luego en bobina del contactor. Si llega voltaje y no acciona → bobina dañada (medir: ~2,5 kΩ para 250V). |
| 3 | Si secuencia OK | Quitar energía total, levantar protecciones apagachispa y revisar contactos fuerza (cobre bañado en plata) - mover, forzar recorrido, ver desgaste/quemado. No mezclar componentes de tableros distintos. |
| 4 | Cableado y resistencia | Seguir en planos cada punto contactor → exterior (motores, bancos resistencia, límites). Ir primero al rack resistencia (lo más cercano), ver buen contacto, no escoriado, buscar abierto/aislado/a masa con buena linterna. |
| 5 | Mecánica | Ver frenos y motor (ver casos 5 y 6). |

---

## Caso 1 - Pantógrafo principal: grúa sin ningún movimiento (sin energía)

**Síntoma:** Ningún movimiento en grúa 1,2 o 3, independientemente de gancho/carro/avance.
**Sistema:** Dos barras de cobre paralelas a la nave entregan DC → pantógrafos con carbones y tensores/resortes que se adaptan a la distancia grúa-barra.
**Causa 1:** Tensores/resortes del pantógrafo rotos → carbón pierde contacto con barra → grúa queda sin energía.
**Verificación:** Inspección visual pantógrafo, tensión de resortes, continuidad carbón-barra.
**Solución:** Reemplazar tensor/resorte, verificar presión carbón.

## Caso 2 - Parada de emergencia / enclavamiento switch principal

**Síntoma:** Grúa sin energía, control principal muerto.
**Causa:** Parada de emergencia o enclavamiento del switch principal no cierra. Elementos de alterna usados en DC no cortan bien la llama de DC → se dañan/escorian.
**Verificación:** Medir continuidad del circuito de enclavamiento, revisar estado contactos parada.
**Solución:** Reemplazar por elemento apto para DC, limpiar contactos.

## Caso 3 - Caída de voltaje por rectificadora sala N°2

**Síntoma:** Grúa no trabaja, UV (undervoltage) no cierra.
**Origen:** Rectificadora sala N°2 debe dar 230-240V DC constante. Si hay falla en alguna grúa (corte, diodo rectificador dañado, fusible) voltaje cae.
**Verificación:** Medir entre positivo y negativo llegando al gabinete/switch principal de la grúa. Si <230V → revisar rectificadora y diodos.
**Protección:** Contactos UV no cierran si voltaje bajo → grúa bloqueada.

## Caso 4 - Secuencia incompleta: contactor no cierra

**Síntoma:** Se ve que contactor no cierra pero no se sabe si es falta de energía o bobina dañada.
**Verificación:** Medir voltaje en bornera (líneas 1-20) y luego directo en bobina. Si llega voltaje y no acciona → bobina abierta (medir resistencia).
**Nota:** Bobinas similares, referencia ~2,5 kΩ para 250V (dar dato exacto después).

## Caso 5 - Frenos electroimán (ganchos y avances)

**Síntoma:** Falla de movimiento atribuida a eléctrico pero es freno. 2 frenos por gancho, tambor gira con motor.
**Principio:** Electroimán depende de corriente/voltaje. A mayor corriente mayor fuerza. Si gap núcleo-bobina-elemento es muy grande, a bajas corrientes (puntos 1 y 2 bajar) no cierra y no libera tambor.
**Verificación:** Medir gap, ver accionamiento simultáneo de ambos frenos. Usar cámara termográfica: tambor sobrecalentado indica freno frenando.
**Solución:** Ajustar gap, sincronizar ambos frenos.

## Caso 6 - Motor DC

**Síntoma:** Después de descartar control, fuerza, resistencia y frenos, motor no gira.
**Verificación visual (motores DC robustos, falla ya es visible):** alta temperatura, pitting en colector, carbones quebrados, shunts hacia portaescobilla violáceos o rotos.
**Instrumentos:** Medición existe pero visual es determinante.
**Solución:** Reemplazo/reparación motor, cambio carbones.

---

## Pendiente para próximos audios (plantilla)

| Fecha | Grúa | Movimiento | Síntoma puntual | Posición | Contactos observados | Causa confirmada | Solución |
|-------|------|------------|-----------------|----------|----------------------|------------------|----------|
|  |  |  |  |  |  |  |  |

*Cuando cites fallas puntuales en el próximo audio, las agrego aquí con la misma estructura y recargo el RAG. Cada fila será citada por `qwen3.5-4b`.*
