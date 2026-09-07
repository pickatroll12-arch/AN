# Corrección Voltaje Bobinas Control 2026-09-07
**Fuente:** Owner corrección `C:\Users\PC2B\Documents\imagenes\correcion 1.JPG` (captura consulta "si tengo, 110vdc en la bobina" con respuesta aberrante asumiendo 110VDC como normal) + indicación owner 2026-09-07.
**Corrección:** Bobinas de contactores principales del circuito de control = **230/240 VDC** (no 110 VDC). La respuesta que valida "110VDC indica alimentación presente" es incorrecta para estos equipos: a 110V el contactor no tiene tensión nominal y su comportamiento no es fiable.
**Matiz:** Existen contactores puntuales con voltajes diferentes (ej. auxiliares, relés específicos, protecciones) — se detallará en corrección futura. Para diagnóstico general de M,H,1A-5A,1L-3L,DB el nominal es 230/240VDC.
**Implicancia para modelo:** Si miden tensión en bobina, esperar ~230-240VDC (no 110V). Si reportan 110VDC, no concluir "alimentación presente OK" sino pedir repetir medición y verificar fuente + caída. Si preguntan por 110VDC, explicar que no corresponde al estándar de estos contactores principales.
**Para citar:** `CORRECCION_VOLTAJE_BOBINAS_20260907.md`
