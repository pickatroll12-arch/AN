# Propuesta de piloto: Asistente Inteligente para GruaHelper

**Proyecto:** GruaHelper  
**Propósito:** Validar el uso de inteligencia artificial como apoyo técnico para capacitación, consulta documental y diagnóstico asistido de puentes grúa.

---

## 1. Resumen ejecutivo

GruaHelper ya es una aplicación de simulación y consulta para sistemas de puente grúa. El siguiente paso propuesto es incorporar un **Asistente Técnico Inteligente** que ayude al personal de operación, mantenimiento y formación a comprender estados de la grúa, consultar documentación y orientar un diagnóstico de forma ordenada.

El piloto no busca automatizar ni controlar equipos. Busca demostrar que una IA, conectada a una base documental aprobada y a casos históricos de falla, puede:

- reducir el tiempo de búsqueda de información técnica;
- mejorar la consistencia del análisis inicial de fallas;
- apoyar la capacitación del personal;
- preservar y reutilizar conocimiento técnico hoy distribuido entre manuales, planos y experiencia de especialistas;
- entregar respuestas trazables, con fuentes y advertencias de seguridad.

> **Principio rector:** la IA será un copiloto de consulta y formación. La autoridad operativa seguirá siendo el procedimiento vigente, las protecciones industriales y el personal autorizado.

---

## 2. Oportunidad de negocio

En mantenimiento industrial, el conocimiento para resolver fallas suele estar distribuido entre:

- manuales técnicos y procedimientos;
- planos eléctricos y diagramas;
- reportes de mantenimiento;
- registros de fallas anteriores;
- experiencia de técnicos y supervisores.

Encontrar la información correcta puede tomar tiempo, y la transferencia de conocimiento depende con frecuencia de personas específicas. GruaHelper puede convertirse en un punto único de consulta que combine simulación, documentación y experiencia histórica.

### Beneficios esperados

| Beneficio | Resultado esperado durante el piloto |
|---|---|
| Acceso más rápido al conocimiento | Menos tiempo buscando manuales, planos y casos anteriores. |
| Capacitación más consistente | Personal nuevo practica escenarios guiados en un entorno de simulación. |
| Conservación de experiencia | Casos resueltos y lecciones aprendidas quedan registrados y reutilizables. |
| Diagnóstico inicial más ordenado | La aplicación ayuda a distinguir hechos, hipótesis, pruebas pendientes y escalamiento. |
| Trazabilidad | Cada respuesta puede mostrar la fuente documental y el caso histórico relacionado. |
| Base para mejora continua | Las consultas sin respuesta y las correcciones de técnicos alimentan futuras mejoras. |

---

## 3. Qué se propone construir

Se propone incorporar en GruaHelper un módulo denominado **Asistente Técnico**.

El usuario podrá seleccionar una grúa, un componente o una pantalla del simulador y realizar preguntas en lenguaje natural. Por ejemplo:

> “El gancho principal no eleva. Hay tensión de control, pero el contactor no cierra. ¿Qué debo revisar primero?”

El asistente entregará una respuesta clara y estructurada:

1. **Información confirmada:** lo que se conoce del simulador y de la consulta.
2. **Posibles causas:** hipótesis ordenadas, sin presentarlas como hechos.
3. **Información o verificaciones pendientes:** qué dato hace falta para avanzar.
4. **Referencia técnica:** manual, plano o caso histórico aplicable.
5. **Seguridad y escalamiento:** cuándo detenerse y solicitar apoyo de personal autorizado.

También podrá utilizarse para capacitación:

- explicar por qué un contacto cambia de estado en el simulador;
- crear casos de práctica;
- evaluar el razonamiento de un aprendiz contra procedimientos aprobados;
- mostrar las diferencias entre una condición normal y una condición de falla.

---

## 4. Alcance del piloto

Para que la validación sea rápida, medible y controlada, se recomienda un alcance limitado.

### Incluido

- Una grúa o familia de grúas seleccionada.
- Gancho principal y gancho auxiliar como primeros subsistemas.
- Documentación técnica vigente y aprobada.
- Entre 30 y 50 casos históricos de falla revisados por especialistas.
- Consulta mediante la aplicación GruaHelper.
- Respuestas con fuentes documentales y advertencias de seguridad.
- Pruebas con un grupo reducido de técnicos y/o formadores.

---

## 5. Cómo funcionará, en términos simples

La aplicación no enviará una pregunta aislada a la IA. Antes de responder, reunirá el contexto disponible: el equipo elegido, el subsistema, la situación en el simulador y los documentos o casos relacionados.

```text
Usuario consulta en GruaHelper
          ↓
La aplicación identifica el contexto técnico
          ↓
El sistema busca manuales, planos y casos similares aprobados
          ↓
La API de IA analiza la información disponible
          ↓
GruaHelper presenta una respuesta con fuentes, límites y seguridad
```

Así, la IA no depende solamente de conocimiento general. Se apoya en información de la propia operación y deja claro cuándo no cuenta con evidencia suficiente.

---

## 6. Hoja de ruta propuesta

### Fase 1 — Preparación y selección de conocimiento

**Objetivo:** definir el caso de uso y reunir la información necesaria para una primera prueba confiable.

**Actividades principales:**

- Seleccionar una grúa y los subsistemas iniciales.
- Identificar manuales, planos y procedimientos vigentes.
- Reunir entre 30 y 50 fallas representativas ya resueltas.
- Clasificar cada caso: síntoma, condiciones, causa confirmada, solución y resultado.
- Definir responsables técnicos que revisarán las respuestas.
- Establecer reglas de seguridad y límites del asistente.

**Entregable:** biblioteca técnica inicial aprobada y conjunto de casos de prueba.

**Duración orientativa:** 2 a 4 semanas.

---

### Fase 2 — Prototipo de asistente en GruaHelper

**Objetivo:** mostrar una experiencia real de consulta dentro de la aplicación.

**Actividades principales:**

- Añadir una pantalla o panel de “Asistente Técnico”.
- Enviar automáticamente el contexto relevante del simulador.
- Conectar la aplicación a una API segura provista por la empresa.
- Configurar la búsqueda de documentos y casos relacionados.
- Diseñar una respuesta uniforme: hechos, hipótesis, verificaciones, fuentes y seguridad.
- Implementar un registro básico de consultas y retroalimentación del técnico.

**Entregable:** demostración funcional para un grupo controlado.

**Duración orientativa:** 3 a 5 semanas.

---

### Fase 3 — Validación con casos reales y formación

**Objetivo:** medir utilidad, precisión y seguridad antes de ampliar el proyecto.

**Actividades principales:**

- Probar el asistente con casos cuya solución ya se conoce.
- Comparar las respuestas contra el criterio de técnicos expertos.
- Ejecutar sesiones de capacitación usando fallas simuladas.
- Registrar errores, dudas frecuentes y documentos faltantes.
- Ajustar la biblioteca de información y el formato de respuesta.

**Entregable:** informe de resultados, hallazgos y recomendación de continuidad.

**Duración orientativa:** 3 a 4 semanas.

---

### Fase 4 — Decisión de continuidad

**Objetivo:** evaluar los resultados del piloto y definir los siguientes pasos del proyecto.

La decisión se basará en la utilidad observada, la calidad de las respuestas, la trazabilidad de las fuentes, el cumplimiento de las reglas de seguridad y la adopción por parte de los usuarios de prueba.

**Entregable:** recomendación ejecutiva de continuidad, ampliación o ajuste del alcance.

---

## 7. Por qué comenzar con una API potente

El piloto debe demostrar utilidad antes de comprometer recursos adicionales. Utilizar una API corporativa permite:

- obtener rápidamente una referencia de calidad;
- validar si los documentos y casos disponibles son suficientes;
- descubrir las preguntas reales de los técnicos;
- medir el valor del asistente sin implementar infraestructura adicional desde el inicio;
- generar un conjunto de datos y evaluaciones para respaldar decisiones posteriores.

El objetivo del piloto es producir evidencia: demostrar en qué situaciones el asistente agrega valor, cuáles son sus límites y qué información se necesita para mejorar sus respuestas.

---

## 8. Criterios de éxito del piloto

Se recomienda definir metas concretas antes de iniciar. Ejemplos:

| Área | Indicador de éxito |
|---|---|
| Utilidad | La mayoría de los participantes califica las respuestas como útiles para orientar la consulta o capacitación. |
| Precisión | Las respuestas relevantes usan el equipo y subsistema correctos y se apoyan en fuentes válidas. |
| Seguridad | No se generan recomendaciones de anular protecciones o realizar maniobras no autorizadas. |
| Trazabilidad | Las respuestas técnicas muestran manual, plano, procedimiento o caso asociado cuando corresponde. |
| Tiempo | Se reduce el tiempo requerido para localizar información técnica frente a la búsqueda manual. |
| Adopción | Técnicos y formadores utilizan el asistente de forma recurrente durante el período de prueba. |
| Mejora continua | Se identifican y registran preguntas sin respuesta, documentos faltantes y correcciones técnicas. |

Una métrica sencilla para la presentación final podría ser:

> “En los casos evaluados, el asistente entregó una respuesta útil, segura y con fuente verificable en X % de las consultas.”

---

## 9. Gobierno, seguridad y responsabilidades

El piloto debe incorporar desde el inicio una política clara:

- El asistente es una herramienta de apoyo, capacitación y consulta.
- No controla equipos ni emite órdenes de operación.
- Las intervenciones físicas requieren los procedimientos vigentes y personal autorizado.
- Las protecciones, finales de carrera, frenos, paros de emergencia y enclavamientos no deben anularse.
- Cuando no exista evidencia suficiente, el sistema debe pedir más información o recomendar escalamiento.
- La documentación utilizada debe estar identificada por versión y vigencia.
- El acceso a la información y a la API debe respetar las políticas internas de seguridad y confidencialidad.
- Las respuestas y fuentes relevantes deben conservar trazabilidad para revisión.

---

## 10. Recursos requeridos para el piloto

### Recursos de negocio y mantenimiento

- Patrocinador del piloto.
- Uno o dos técnicos expertos para validar contenido.
- Responsable de seguridad o mantenimiento para aprobar límites de uso.
- Acceso controlado a manuales, planos, procedimientos y registros de falla.
- Grupo pequeño de usuarios de prueba.

### Recursos tecnológicos

- Acceso a la API corporativa de IA.
- Un servicio interno seguro que conecte GruaHelper con la API.
- Espacio controlado para almacenar documentación y casos de falla.
- Apoyo puntual de desarrollo para integrar el asistente.

---

## 11. Riesgos y cómo se controlan

| Riesgo | Control propuesto |
|---|---|
| Respuesta incorrecta o incompleta | Presentar hipótesis, no diagnósticos definitivos; exigir fuentes y revisión técnica. |
| Recomendación insegura | Reglas explícitas de seguridad, advertencias obligatorias y límites de uso. |
| Documentación obsoleta | Control de versión, vigencia y responsable de cada fuente. |
| Información confidencial | Uso de infraestructura y API aprobadas por la empresa; acceso por roles. |
| Expectativas excesivas | Alcance limitado: apoyo a capacitación y consulta, no automatización operacional. |
| Falta de adopción | Involucrar a técnicos desde el diseño y medir utilidad con casos reales. |

---

## 12. Solicitud de aprobación

Se solicita aprobar un piloto controlado de GruaHelper con Asistente Técnico Inteligente, utilizando la API corporativa disponible, para validar durante aproximadamente **8 a 13 semanas**:

- la utilidad para capacitación y consulta técnica;
- la calidad de la base documental y de los casos históricos;
- la seguridad y trazabilidad de las respuestas;
- el nivel de adopción por parte de técnicos y formadores;
- los siguientes pasos necesarios para ampliar o ajustar el proyecto.

La continuidad del proyecto se decidirá al finalizar el piloto, con datos de uso, evaluación técnica y criterios de negocio claros.

---

## 13. Mensaje final para dirección

GruaHelper puede evolucionar de un simulador útil a una plataforma de conocimiento técnico industrial. El piloto propuesto permite probar esta visión de forma prudente, medible y segura: aprovechar una API corporativa potente para validar valor, capturar conocimiento técnico y establecer una base de mejora continua.

El objetivo no es reemplazar al técnico. Es darle una herramienta que encuentre información relevante, estructure el análisis y conserve la experiencia colectiva de la organización.
