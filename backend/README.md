# Backend GruaHelper - Ollama Wrapper

Cubre la brecha stateless de Ollama para GruaHelper.

## Inicio rápido
```cmd
ollama serve
ollama run qwen2.5:3b   # o el modelo que quieras probar
set OLLAMA_MODEL=qwen2.5:3b && python server.py
# abre http://localhost:8000/api/health
```

Cambiar modelo sin tocar código:
```cmd
set OLLAMA_MODEL=deepseek-r1:7b && python server.py
```
O editar `.env`.

## Endpoint que espera GruaHelper
`POST http://localhost:8000/api/diagnostico`
Body: `{question, context:{crane, module, simulatorView, position, activeContacts}}`
Response: `{mode, summary, facts, hypotheses, questions, safety, sources}`

Ver `index.html` -> `ASSISTANT_CONFIG.endpoint`
