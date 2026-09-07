# Corrección Auxiliar Bajada - 1A NO va en bajada
**Fuente:** Captura `Screenshot_20260902_070227_com.android.chrome.jpg` 07:02 `GRÚA 3 Gancho Auxiliar` primer punto bajada. Modelo dijo "1A es único contacto en primer punto bajada" - falso.
**Corrección:** Según `MANUAL_GANCHO_AUXILIAR.md:55-62` `aClosedMap`:
- **DB:** p==0 || p==-1 (neutro y -1)
- **1L:** p<0 (toda bajada)
- **3A:** p -1 a -2
- **4A:** p -1 a -2
- **2A:** p -2 a -3
- **1A:** p 2-5 **solo subida** (NO bajada)
- **Primer punto bajada (-1) auxiliar:** **DB + 3A + 4A** (y 1L), **NO 1A**. 1A nunca en bajada.
**Para el modelo:** Si preguntan auxiliar bajada, NO mencionar 1A como contacto de bajada. Citar este archivo.
