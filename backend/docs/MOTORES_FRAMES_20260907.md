# Frames de Motores por Grúa y Movimiento - Dato Owner 2026-09-07
**Fuente:** Audio `WhatsApp Ptt 2026-09-07 at 12.45.25` → `TRANSC_20260907_1245.txt` + imágenes `Captura.JPG` (600 FRAME MOTORS HORSEPOWER RATINGS: 60 MIN 75°C vs 30 MIN 75°C + tabla DIMENSIONS A-U) y `dimensiones motor.JPG` (vista Armored Mill Auxiliary Motors con cotas A,B,C,D,E,F,N,O,U). Ambas del mismo catálogo 600 FRAME.
**Corrección 2026-09-07:** La primera versión de la imagen recortaba el `duty cycle`; esta versión incluye ambos ciclos. El HP depende del ciclo que mencione la placa/catálogo. **Prevalencia:** Este mapeo corrige a `MOTORES_Y_RESISTENCIAS.md:5` (serie 800) — frames reales serie 600.

## Mapeo frame por grúa (owner)
| Grúa | Gancho principal | Gancho auxiliar | Puente (avance) | Carro |
|------|------------------|-----------------|-----------------|-------|
| GRÚA 1 | 616 | 614 | 2 motores 612 | 606 |
| GRÚA 2 | 614 | 612 (norte/sur) | 608 | 606 |
| GRÚA 3 | 614 | 612 (norte/sur) | 608 | 606 |

## Tabla referencia (Captura.JPG, serie 600 - con duty cycle)
**Claves:** Toda potencia es a `75°C RISE`. Dos ciclos: `60 MIN.` vs `30 MIN.`. En 30 MIN el HP es mayor porque es servicio intermitente.

| Frame | 60 MIN 75°C HP | SERIES RPM 60M | COMP/SHUNT RPM 60M | ADJ. SPEED RPM 60M | 30 MIN 75°C HP | SERIES RPM 30M | COMP RPM 30M |
|-------|---------------|----------------|--------------------|--------------------|----------------|----------------|----------------|
| 602 | 7.5 | 800 | 900 | 900/1800 | 10 | 675 | 775 |
| 603 | 10 | 725 | 800 | 800/2000 | 13.5 | 620 | 700 |
| 604 | 15 | 650 | 725 | 725/1800 | 19 | 560 | 650 |
| 606 | 25 | 575 | 650 | 650/1950 | 33 | 515 | 600 |
| 608 | 35 | 525 | 575 | 575/1725 | 45 | 470 | 525 |
| 610 | 50 | 500 | 550 | 550/1650 | 65 | 445 | 500 |
| 612 | 75 | 475 | 515 | 515/1300 | 100 | 430 | 475 |
| 614 | 100 | 460 | 485 | 485/1200 | 135 | 400 | 450 |
| 616 | 150 | 450 | 460 | 460/1150 | 200 | 400 | 430 |
| 618 | 200 | 410 | 420 | 420/1050 | 265 | 385 | 390 |
| 620 | 275 | 370 | 390 | 390/975 | 360 | 340 | 360 |
| 622 | 375 | 340 | 360 | 360/1080 | 500 | 310 | 325 |
| 624 | 500 | 320 | 340 | 340/1020 | 650 | 290 | 300 |

- **Clave columnas:** `SERIES` no es "serie del motor" ni "frame series 600": es **tipo de conexión serie** (RPM con devanado serie). `COMP. OR SHUNT` es **compound o shunt** (RPM con devanado compound/shunt). `ADJ. SPEED` es rango de velocidad ajustable (ej. para 616: 460/1150 RPM). Ej. 616: 450 RPM si está en serie, 460 RPM si en compound/shunt, 460/1150 ajustable.
- **Regla de lectura:** Si solo dicen "150 HP 616" es el de 60 MIN (450 RPM serie / 460 RPM comp); el mismo frame rinde 200 HP en 30 MIN (400/430 RPM). Idem 100 HP (60M) = 135 HP (30M) para 614, etc. La conexión (series vs compound) define la RPM base, no el frame.

## Tabla DIMENSIONS 600 FRAME (Captura.JPG lado derecho + dimensiones motor.JPG)
Cotas según ilustración Armored Mill Auxiliary Motors (vista lateral/frontal): A,B,C,D,E,F,N,O,U en pulgadas.

| Frame | A | B | C | D | E | F | N | O | U |
|-------|---|---|---|---|---|---|---|---|---|
| 602 | 15 | 19 | 32 7/8 | 7 5/8 | 6 1/4 | 8 1/4 | 4 7/16 | 15 13/16 | 1 3/4 |
| 603 | 17 | 21 | 37 | 8 1/2 | 7 | 9 | 5 | 17 3/8 | 2 |
| 604 | 18 | 22 | 39 | 9 | 7 1/2 | 9 1/2 | 5 | 18 15/16 | 2 |
| 606 | 20 | 24 1/2 | 42 1/2 | 10 | 8 1/4 | 10 1/2 | 5 5/8 | 20 3/8 | 2 1/2 |
| 608 | 22 3/4 | 28 1/2 | 47 1/2 | 11 1/4 | 9 3/8 | 12 3/8 | 6 1/4 | 22 13/16 | 3 |
| 610 | 24 1/2 | 30 1/2 | 50 1/4 | 12 1/4 | 10 1/4 | 13 | 6 3/8 | 24 13/16 | 3 1/4 |
| 612 | 27 | 33 | 55 | 13 3/8 | 11 1/4 | 14 1/4 | 7 | 27 1/4 | 3 5/8 |
| 614 | 30 | 37 1/2 | 60 3/4 | 14 3/4 | 12 1/2 | 16 | 7 1/8 | 30 1/16 | 4 1/4 |
| 616 | 32 1/2 | 41 | 67 1/8 | 16 | 13 1/2 | 17 1/2 | 7 3/4 | 32 1/2 | 4 5/8 |
| 618 | 36 | 45 1/2 | 70 5/8 | 17 3/4 | 15 | 19 1/2 | 7 13/16 | 36 1/16 | 5 |
| 620 | 41 1/2 | 52 | 78 | 20 7/8 | 18 | 22 | 9 | 42 | 5 7/8 |
| 622 | 45 1/2 | 62 | 86 1/4 | 23 | 20 | 25 3/4 | 10 1/8 | 46 1/2 | 6 1/4 |
| 624 | 47 1/2 | 68 | 96 1/4 | 24 | 21 | 28 | 12 1/8 | 48 1/2 | 7 |

- **Esquema:** `dimensiones motor.JPG` muestra C= largo total, A= distancia entre centros de patas, B= largo base, D= altura eje, E= separación patas, F= largo patas, N= saliente eje, O= alto total, U= diámetro eje.
- Si piden verificar si un motor entra en bancada o repuestos, cruzar frame con esta tabla.

## Corrientes estimadas a 230V CC (cálculo directo, sin placa)
**Voltaje confirmado owner:** 230V CC. **Fórmula:** `I[A] = HP×746 / (V×η)`. **η** estimado 0.90 para motores DC grandes 600 frame (placa mandará; si es menor, corriente sube). Se deja tabla para cálculo directo:

| Frame | HP 60MIN | I nom 60MIN @230V η0.90 | HP 30MIN | I nom 30MIN @230V η0.90 | I arranque típico 150% |
|-------|----------|--------------------------|----------|--------------------------|------------------------|
| 602 | 7.5 | 27.0 A | 10 | 36.0 A | 40–54 A |
| 603 | 10 | 36.0 A | 13.5 | 48.7 A | 54–73 A |
| 604 | 15 | 54.0 A | 19 | 68.5 A | 81–103 A |
| 606 | 25 | 90.1 A | 33 | 119.0 A | 135–179 A |
| 608 | 35 | 126.1 A | 45 | 162.2 A | 189–243 A |
| 610 | 50 | 180.2 A | 65 | 234.3 A | 270–351 A |
| 612 | 75 | 270.3 A | 100 | 360.4 A | 405–541 A |
| 614 | 100 | 360.4 A | 135 | 486.5 A | 541–730 A |
| 616 | 150 | 540.6 A | 200 | 720.8 A | 811–1081 A |
| 618 | 200 | 720.8 A | 265 | 955.1 A | 1081–1433 A |
| 620 | 275 | 991.0 A | 360 | 1297.4 A | 1487–1946 A |
| 622 | 375 | 1351.4 A | 500 | 1801.9 A | 2027–2703 A |
| 624 | 500 | 1801.9 A | 650 | 2342.5 A | 2703–3514 A |

- **Mapeo grúas a 230V:**
  - Grúa 1 principal 616: **541 A @60MIN / 721 A @30MIN** (arranque 811–1081 A con reóstato en serie).
  - Grúa 1 auxiliar 614: **360 A / 487 A**.
  - Puente Grúa 1 (2×612): **270 A por motor / 360 A** (total puente 540 A si ambos traccionan).
  - Carro todas 606: **90 A / 119 A**.
  - Grúas 2/3 principal 614: 360/487 A; auxiliar 612: 270/360 A; puente 608: 126/162 A.
- **Nota:** Con η 0.85 corriente sube ~6% (616: 573 A vs 541 A). Cuando tengas placa (V, A nominales, RPM base y tipo conexión series vs compound 450/460) reemplazar estimación. Útil para calibrar OLs: 1 OL instantáneo cortocircuito, 2 OL time-delay aceite sobrecarga progresiva.

## Implicancias RAG / MoE
- Grúa 1 mayor: principal 616 = 150 HP @60MIN / 200 HP @30MIN = 541/721 A @230V; Grúas 2/3 principal 614 = 100/135 HP = 360/487 A — citar SIEMPRE frame+HP+ciclo+corriente si preguntan HP/corriente.
- Si consulta cita HP sin ciclo, citar ambos y corriente estimada con advertencia "a confirmar con placa".
- Si consulta cita frame (ej. "motor 616 se calienta", "falla en 612 de puente"), filtrar por esta tabla antes de hipotetizar contactores/secuencia.
- Puente Grúa 1 = 2 motores 612 = 75 HP @60MIN / 100 HP @30MIN = 270/360 A por motor (coherente con `GRUAS_DIFERENCIAS_20260901.md:6`); Grúas 2/3 puente = 608 = 35/45 HP = 126/162 A.
- Carro = 606 = 25/33 HP = 90/119 A en las 3 grúas.
- Gancho auxiliar Grúa 1 = 614 (100/135 HP = 360/487 A); Grúas 2/3 = 612 (75/100 HP = 270/360 A) con norte/sur (coherente con `GRUAS_DIFERENCIAS_20260901.md:13-14`).
