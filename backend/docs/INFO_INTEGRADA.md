# Info Integrada - Grúa DC (Motores, Resistencias, Planos, Carbones)
**Fuente:** `C:\Users\PC2B\Downloads\info` (60 PDFs convertidos a `backend/docs/pdfs_txt/` via `pymupdf` 2026-09-01) + transcripción empírica.
**Uso RAG:** `qwen3.5-4b` cita este índice y los `.txt` de `pdfs_txt/` como `sources`.

## Motores
- **Frames 800/600/400** (`Mill motor frames (2).txt`): HP 5-500, RPM 410-1425, datos placa. Grúas 1-3 usan 800 (ganchos 150-250HP).
- **Placas:** Ver `info/GRUA NUEVA/Planos/R81187*` y `R81225*` para identificación exacta por grúa.

## Paños Resistivos
- **Tab-Weld Class 6715** (`Tabweld ressitors.txt` + `Class 6715 TAB-WELD*.txt`): TW500D 0.0214Ω a TW13D 22.10Ω, secciones 18"/26.5", inoxidable. Mapeo a racks `19/19A/19B/19C` y `26/26A/26B` del simulador (`MANUAL_GANCHO_*.md`).
- **Placa paño:** `Type TWxxx` + resistencia entre taps @25°C. Ver `Disposicion resistencias.png`.

## Contactores y Frenos
- **Contactores:** `Catalogo contactores.txt`, `SPNO type M.txt`, `Class 7004 Type M LINE-ARC DC Contactors.txt` (DC), `Class 8503 AC` (comparativa). `6121 Frontline DC Hoist Controller.txt` para lógica gancho.
- **Frenos:** `SBE brake spanish.txt`, `Type F brakes series A.txt`, `Class 5010 DC Magnetic Brakes.txt` - electroimán, gap, 2 frenos/gancho, termografía.

## Carbones
- **Fallas típicas:** `CARBONES_FALLAS_TIPICAS.md` (Helwig) + `Conmutador y escobillas.txt` (15k chars). Presión 4-6 PSI, pitting colector → ver `CASOS_EMPERICOS_ORGANIZADOS.md:6`.

## Planos
- **Control/fuerza:** `PG-8101-01-03-*.txt`, `R81187_REV02 Sheet01-05.txt`, `R81225_REV02/03*.txt` - líneas 1-20 control ganchos, conexiones a motores/resistencias/límites. Algunos son escaneados (28 chars) → requieren OCR manual si se necesita detalle.

**Cómo preguntar ahora a GruaHelper:**
- "paño 19B cuánto debe medir" → cita `Tabweld` + `MANUAL_GANCHO_PRINCIPAL.md`
- "carbón violáceo motor 150HP frame 814" → cita `CARBONES_FALLAS_TIPICAS.md` + `Mill motor frames`
- "freno no libera en bajar 1" → cita `SBE brake` + `CASOS_EMPERICOS`

*Todos los 60 PDFs ya están en `backend/docs/pdfs_txt/` y son buscables por `retrieve_docs()`.*
