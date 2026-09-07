# Límites y Contactor LSR - Gancho Principal/Auxiliar
**Fuente empírica:** Relato técnico 2026-09-01 (segundo bloque) - "secuencia en subida y bajada no se ve afectada por los límites salvo en una condición. Cuando el gancho alcanza el punto más alto, activa el límite de subida."

## 1. Comportamiento normal
- Secuencia subir (pos +1 a +6) y bajar (pos -1 a -6) **no** es afectada por límites en condiciones normales.
- Contactores `M,H,1L-3L,1A-5A,DB` cierran según `pClosedMap`/`aClosedMap` sin intervención de límite.

## 2. Condición límite de subida activado
**Evento:** Gancho alcanza punto más alto → activa límite de subida.
**Efecto:**
- Secuencia de subida **no responde**: ningún punto en subida (+1 a +6) cierra.
- El límite **cambia la conexión física del motor**: mientras esté activado, solo permite bajada y lo hace en **conexión serie** (a través del mismo límite) para que el motor no se embale y sufra daños.
- Existe contactor **LSR** que solo permite **movimientos cortos en bajada** (jogging) hasta que se desactive el límite y vuelva a configuración normal.

## 3. Verificación y diagnóstico
- Si gancho no sube pero sí hace movimientos cortos en bajada → sospechar límite de subida activado/pegado.
- Verificar estado físico del límite (fin de carrera superior), continuidad del circuito serie, y estado de LSR.
- No confundir con falla de contactores de subida: el límite anula toda la lógica de subida por cambio de conexión, no por contactor dañado.

## 4. Pendiente de completar
- Ubicación exacta del límite en cada grúa (1,2,3)
- Esquema de conexión serie vs normal (plano control hoja)
- Características de LSR (bobina, contactos)

*Este archivo es citable por `qwen3.5-4b` como `sources:["LIMITES_Y_LSR.md"]`.*
