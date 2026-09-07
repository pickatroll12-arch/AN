# Carbones y Escobillas - Fallas Típicas (DC Industrial)
**Fuente:** `C:\Users\PC2B\Downloads\info\Conmutador y escobillas.pdf` (Helwig Carbon, 24 págs) - Guía de especificaciones y diagnóstico. Convertido a markdown para RAG de `qwen3.5-4b`.

## 1. Función
Escobilla = contacto eléctrico entre circuito inmóvil y móvil (colector/anillo). Bloque carbón/grafito + terminal/casquete. Conduce corriente y lubrica.

## 2. Fallas de película del conmutador (indicador principal)
- **Película ligera (marrón claro):** Buen funcionamiento, carga liviana/baja humedad. OK.
- **Película mediana (marrón medio):** Ideal - máxima duración escobilla+conmutador.
- **Película gruesa (marrón oscuro/no marrón):** Carga alta, alta humedad o grado con película alta → contaminación, alta fricción/resistencia.
- **Inconsistencia de color / deformación:** Señal de problema, desgaste rápido.

## 3. Modos de falla específicos (extraídos p.18-19)

| Falla | Causa | Solución empírica Helwig |
|-------|-------|--------------------------|
| **Desgaste rápido** | Superficie no circunferencial, barras altas, muescas, rebabas → chispoteo + ruido fricción; polvo excesivo | Verificar redondez <0.002", presión resorte 4-6 PSI, densidad corriente correcta |
| **Carga liviana** | Densidad corriente baja para el grado → película inadecuada, alta fricción, polvo, hilachado | Subir densidad removiendo escobillas o cambiar a grado de película ligera |
| **Hilachado** | Transferencia cobre a cara escobilla → abrasión metal-metal. Baja densidad + baja presión + contaminación | Verificar carga y presión, eliminar contaminación |
| **Ranurado** | Poco contacto eléctrico → chispoteo y maquinado eléctrico; o grado abrasivo; baja/alta corriente; presión inadecuada | Verificar redondez, vibración <6 mils, densidad y presión |
| **Rayado / Arrastre cobre** | Transferencia metal, carga liviana + baja presión; conmutador recalentado y ablandado → cobre arrastrado a ranuras | Incrementar presión, reducir temperatura conmutador |
| **Quemadura borde barra** | Poca conmutación, grado con caída voltaje inadecuada, escobillas no en neutro, interpolos mal | Verificar grado, neutral, fuerza interpolos |
| **Muescas de barras** | Error bobinas armadura, patrón relacionado a conductores por barra | Revisar bobinado |

## 4. Presión de resorte (causa más común de falla)

| Aplicación | PSI recomendado | g/cm² |
|------------|-----------------|-------|
| Industrial DC | 4.0-6.0 | 280-420 |
| WRIM & Anillos sinc. | 3.5-4.5 | 240-310 |
| Grafito blando alta vel. | 2.5-3.5 | 170-240 |
| Metal-grafito | 4.5-5.5 | 310-390 |
| Tracción | 5.0-8.0 | 350-560 |

Cálculo: `PSI = Fuerza medida (lbs) / (Espesor x Ancho pulgadas)`. Usar dinamómetro Helwig. Para biseles >25° añadir 0.5-1 PSI.

Curva desgaste: baja presión → desgaste eléctrico alto; alta presión → desgaste mecánico alto; mínimo total en rango ideal 4-6 PSI.

## 5. Grados y materiales (p.22-24)
- **Grafito carbón:** limpieza a baja velocidad/corriente, equipos viejos con mica.
- **Grafito:** baja fricción, muy baja densidad o alta velocidad periférica.
- **Electrografito:** más común moderno, alto voltaje/densidad/velocidad, soporta sobrecarga.
- **Cobre-grafito (15-95% Cu):** alta densidad, bajo voltaje.
- **Plata-grafito (15-95% Ag):** muy alta densidad, bajo voltaje.

Selección requiere: carga real, ciclo, voltaje, velocidad periférica, ambiente. Helwig recomienda consulta técnica - no cambiar grado como primer intento.

## 6. Conexión para grúa DC 40/60s
Tus motores DC de grúa (ver `Mill motor frames (2).pdf` + `GRUA NUEVA/Planos/R81187...`) usan escobillas bañadas plata/cobre. Si ves en `TRANSCRIPCION` "carbones violáceos/rotos, pitting colector" → correlaciona con tabla arriba: presión inadecuada o grado incorrecto + contaminación nave.

**Uso RAG:** Cuando preguntes a `qwen3.5-4b` "carbón violáceo gancho no eleva", el retriever traerá esta tabla y citará `CARBONES_FALLAS_TIPICAS.md:3-4`.

---
*Extracto textual para indexación - no reemplazar PDF original, mantener `Conmutador y escobillas.pdf` como fuente primaria.*
