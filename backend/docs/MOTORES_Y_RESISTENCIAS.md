# Motores y Paños Resistivos - Identificación
**Fuentes:** `C:\Users\PC2B\Downloads\info\Mil motor frames (2).pdf` (HP ratings 400/600/800 frames), `Tabweld ressitors.pdf` (Class 6715), `GRUA NUEVA/Planos/R81187_*.pdf` + `R81225_*.pdf`, `info/GRUA NUEVA/Catalogo/`

## Motores DC - Grúa 40/60s
- **Frames:** 800 (5-250 HP), 600 (7.5-500 HP), 400 (5-200 HP) según tablas Mill motor. Tus grúas 1,2,3 usan frames 800 para ganchos principales (ver planos R81187_REV3, R81225_REV05 en `GRUA NUEVA/Planos`).
- **Placa:** Cada motor tiene placa con HP, RPM, voltaje, corriente, frame. Extraer de `Mill motor frames (2).pdf` p.1-3 y de fotos de placas en `info/` si las tienes.
- **Falla empírica ya transcripta:** pitting colector, carbones violáceos/rotos, shunts quemados → ver `CARBONES_FALLAS_TIPICAS.md`.

## Paños Resistivos (Bancos)
- **Tipo:** Tab-Weld® Class 6715, grids acero inoxidable, para vibración/polvo severo (nave). Secciones 18" y 26.5" con 2 terminales.
- **Modelos en tu grúa:** TW500D (0.0214Ω) a TW13D (22.10Ω) - ver tabla `Tabweld ressitors.pdf`. Los racks de simulador `19/19A/19B/19C` (gancho principal, 28 BOX) y `26/26A/26B` (auxiliar, 20 BOX) son físicamente estos paños.
- **Identificación placa paño:** Cada paño tiene etiqueta `Type TWxxx` + resistencia entre taps a 25°C. Si ves "paño 19-BOX12" en simulador, es físicamente `TWxx` en `Disposicion resistencias.png`.
- **Falla típica transcripta:** abierto/aislado/a masa, conexiones escoridas, necesita linterna para revisar.

## Planos a indexar
- `GRUA NUEVA/Planos/PG-8101-01-03-*.pdf` (4 hojas), `R81187_REV02 Sheet01-05`, `R81225_REV03_1-4` - contienen líneas 1-20 (control) y conexiones contactor→motor/resistencia/límites.
- **Acción:** Convertir cada PDF a `.txt` via `faster-whisper` no, sino via `pdftotext` y guardar en `backend/docs/PLANOS_TXT/` para que `retrieve_docs()` los encuentre. Por ahora, este `.md` ya da el mapeo.

## Catálogos contactores/frenos
- `Catalogo contactores.pdf`, `Contactor.pdf`, `SPNO type M`, `Master Sw`, `SBE brake spanish.pdf`, `Type F brakes` - en `info/` raíz. Cada uno será un `.md` futuro si lo necesitas citar.

**Próximo paso RAG:** Ya tienes `CASOS_EMPERICOS_ORGANIZADOS` + `CARBONES` + este archivo. Cuando cites "motor 150HP frame 814 se calienta" o "paño 19B mide 2.16Ω", el modelo citará `MOTORES_Y_RESISTENCIAS.md:2-3`.
