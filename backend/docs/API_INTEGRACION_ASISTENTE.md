# Conexión de la API corporativa — Asistente Técnico

La primera versión del asistente funciona en **modo demostración local**. No requiere API, credenciales ni conexión a Internet.

## Cuándo entregar la API

La API debe entregarse **cuando exista un endpoint corporativo seguro** que reciba consultas desde GruaHelper. No envíes una clave secreta en el chat ni la coloques en `index.html`.

Para avanzar con la integración real, se necesita que el equipo responsable de la API proporcione:

1. **URL HTTPS del endpoint interno**, por ejemplo:
   ```text
   https://asistente.interno.empresa/api/diagnostico
   ```
2. **Método de autenticación permitido**. Lo recomendado es que GruaHelper se autentique ante un backend propio mediante sesión corporativa o token de corta duración. La clave del proveedor de IA debe permanecer exclusivamente en el servidor.
3. **Contrato de solicitud/respuesta** o una persona técnica de contacto. La aplicación ya está preparada para enviar:
   ```json
   {
     "question": "Consulta escrita por el usuario",
     "context": {
       "crane": "GRÚA 1",
       "module": "Gancho principal",
       "simulatorView": "gancho-principal",
       "position": 0,
       "activeContacts": ["DB"]
     }
   }
   ```
4. **Respuesta JSON esperada**, con esta estructura orientativa:
   ```json
   {
     "mode": "API corporativa",
     "summary": "Resumen de la orientación técnica.",
     "facts": ["Hecho confirmado 1"],
     "hypotheses": ["Hipótesis 1"],
     "questions": ["Verificación o dato pendiente"],
     "safety": "Advertencia y condiciones de seguridad.",
     "sources": ["Manual X, revisión Y, sección Z"]
   }
   ```
5. **Restricciones de red y seguridad**, tales como CORS, VPN, autenticación corporativa, certificados y roles de usuario.

## Cambio que se hará en la aplicación

Cuando el endpoint esté validado, se modifica únicamente esta sección de `index.html`:

```js
const ASSISTANT_CONFIG = {
  enabled: false,
  endpoint: '',
  timeoutMs: 30000
};
```

A:

```js
const ASSISTANT_CONFIG = {
  enabled: true,
  endpoint: 'https://asistente.interno.empresa/api/diagnostico',
  timeoutMs: 30000
};
```

La aplicación **no debe contener** una clave de OpenAI ni de ningún proveedor. El backend corporativo es quien guarda la clave, consulta la documentación autorizada y llama a la API del modelo.

## Recomendación de prueba inicial

Antes de conectar documentos reales, validar el endpoint con tres casos controlados:

1. Explicar un estado conocido del simulador.
2. Solicitar orientación ante un contactor que no cambia de estado.
3. Solicitar una acción insegura y comprobar que el sistema responde con límites de seguridad y escalamiento.

Una vez superadas estas pruebas, se conectan manuales, planos y casos históricos aprobados.
