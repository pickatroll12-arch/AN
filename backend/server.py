"""
Backend wrapper GruaHelper <-> Ollama
Cubre la brecha stateless: el modelo Ollama no recuerda nada entre requests.
Este servicio mantiene:
  1. Memoria conversacional (historial por sessionId)
  2. RAG documental (inyecta manuales/casos en cada prompt)
  3. Formato de respuesta esperado por GruaHelper

Uso:
  python server.py  -> http://localhost:8000/api/diagnostico
  OLLAMA_MODEL=qwen2.5:3b python server.py  # cambiar modelo
  Ver /api/health y /api/models para estado

Cuando quieras cambiar de modelo, avisa y cambio OLLAMA_MODEL aquí y en .env
"""
import os
import re
import json
import glob
import time
from pathlib import Path
from typing import Dict, List

# carga .env si existe (para cambio fácil de modelo)
try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).parent / ".env")
except Exception:
    pass

import httpx
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
import asyncio
try:
    from vector_store import vector_search
    HAS_VECTOR = True
except Exception as e:
    vector_search = None
    HAS_VECTOR = False
    print(f"[vector] no disponible: {e}")

# ================= CONFIGURACIÓN CAMBIABLE =================
# Modelo por defecto para pruebas. Cuando llegue el momento de usar otro,
# cambia esta variable o crea un .env con OLLAMA_MODEL=nuevo_modelo
# Modelos disponibles en este PC (ollama list):
# - qwen2.5:3b            -> rápido, ideal para pruebas iniciales
# - qwen2.5:3b-32k         -> mismo pero ventana larga
# - ds-r1-1.5b-32k / fix2  -> DeepSeek R1 1.5B
# - deepseek-r1:7b / 7b-tight -> más calidad, más RAM
# - minicpm-v4.6:q6_K      -> multimodal (si necesitas visión)
OLLAMA_MODEL_DEFAULT = os.getenv("OLLAMA_MODEL", "qwen2.5:3b")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://127.0.0.1:11434")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
GROQ_MODEL_DEFAULT = os.getenv("GROQ_MODEL", OLLAMA_MODEL_DEFAULT)
DEEPSEEK_MODEL_DEFAULT = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
BACKEND_PORT = int(os.getenv("PORT", "8000"))
IS_GROQ = ("groq" in OLLAMA_URL.lower() and GROQ_API_KEY != "")
IS_DEEPSEEK = "deepseek" in OLLAMA_URL.lower() and DEEPSEEK_API_KEY != ""
# prioridad: Groq si OLLAMA_URL es groq, sino DeepSeek si OLLAMA_URL es deepseek, sino Ollama local
API_KEY = GROQ_API_KEY if IS_GROQ else (DEEPSEEK_API_KEY if IS_DEEPSEEK else "")
# fallback automático: si Groq configurado pero falla, permite reintentar con DeepSeek si existe
HAS_GROQ_FALLBACK = bool(GROQ_API_KEY and DEEPSEEK_API_KEY)

# Aviso explícito para cambio de modelo futuro
PROVIDER_NAME = "DeepSeek" if IS_DEEPSEEK else ("Groq" if IS_GROQ else "Ollama")
MODEL_SWITCH_NOTE = f"Modelo actual: {OLLAMA_MODEL_DEFAULT} ({PROVIDER_NAME}) | Para cambiar: set OLLAMA_MODEL/GROQ_MODEL/DEEPSEEK_MODEL=nuevo_modelo && reiniciar server.py"

ASSISTANT_SAFETY_NOTICE = "Este asistente es una herramienta de consulta y capacitación. No controla equipos ni sustituye procedimientos vigentes."

# ================= FASTAPI =================
app = FastAPI(title="GruaHelper Backend - Ollama Wrapper", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # en producción restringir a tu dominio
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Memoria simple: sessionId -> lista de messages (últimos 12 turnos)
HISTORIAL: Dict[str, List[dict]] = {}
MAX_HISTORIAL_TURNS = 12

# Cache de documentos
DOCS_CACHE = []
DOCS_LOADED_AT = 0

# Validaciones pendientes de solución reportada por usuario (requiere tu visto bueno)
PENDING_FILE = Path(__file__).parent / "data" / "validaciones_pendientes.json"
VALIDATED_FILE = Path(__file__).parent / "data" / "validaciones_validadas.json"
PENDING_FILE.parent.mkdir(parents=True, exist_ok=True)
import uuid
from datetime import datetime, timezone

def _load_json(p: Path):
    if not p.exists():
        return []
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except:
        return []
def _save_json(p: Path, data):
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

SOLUCION_PATTERNS = [r"solucion fue", r"se soluciono", r"solucionado", r"la solucion", r"cambiamos", r"reemplazamos", r"repare", r"quedo operativo", r"quedo funcionando", r"era el contactor", r"era la bobina", r"era el cable", r"problema era", r"time delay", r"timedelay", r"delay.*4a", r"4a.*delay"]

def detect_solucion_reportada(text: str) -> bool:
    t=text.lower()
    return any(re.search(pat, t) for pat in SOLUCION_PATTERNS)

def add_pending(question: str, context: dict, session_id: str):
    data=_load_json(PENDING_FILE)
    entry={"id": str(uuid.uuid4())[:8], "timestamp": datetime.now(timezone.utc).isoformat(), "sessionId": session_id, "question": question, "context": context, "estado": "pendiente_validacion"}
    data.append(entry)
    _save_json(PENDING_FILE, data)
    return entry

def load_docs():
    global DOCS_CACHE, DOCS_LOADED_AT
    # Lee todos los .md de la raíz del repo + backend/docs si existe
    base = Path(__file__).parent.parent  # AN/
    patterns = [
        str(base / "*.md"),
        str(base / "backend" / "docs" / "*.md"),
        str(base / "backend" / "docs" / "*.txt"),
        str(base / "backend" / "docs" / "pdfs_txt" / "*.txt"),
    ]
    files = []
    for pat in patterns:
        files.extend(glob.glob(pat))
    docs = []
    for fp in files:
        try:
            text = Path(fp).read_text(encoding="utf-8", errors="ignore")
            # chunk simple por párrafos, limita 3000 chars por doc para no saturar prompt
            docs.append({"file": Path(fp).name, "text": text[:4000]})
        except Exception as e:
            print(f"[docs] error leyendo {fp}: {e}")
    # Fallback si no hay docs
    if not docs:
        docs = [{"file": "fallback", "text": "Sin documentación cargada. Responde de forma general y trazable."}]
    DOCS_CACHE = docs
    DOCS_LOADED_AT = time.time()
    print(f"[docs] cargados {len(docs)} archivos: {[d['file'] for d in docs]}")
    return docs

def retrieve_docs(question: str, context: dict = None, top_k=3):
    """RAG híbrido: TF-IDF vectorial offline + keyword + boost por filtro. Sin API, sin bloqueo."""
    if not DOCS_CACHE or time.time() - DOCS_LOADED_AT > 300:
        load_docs()
    # 1) intento vectorial (offline, numpy)
    vector_docs = []
    if HAS_VECTOR and vector_search:
        try:
            vec_hits = vector_search(question, context, DOCS_CACHE, top_k=top_k)
            # vec_hits: list of (score, {file,text})  score 0..1
            for score, doc in vec_hits:
                # convierte a escala keyword para combinar: 0..1 -> 0..10
                vector_docs.append((score*10, doc))
        except Exception as e:
            print(f"[vector] search fail: {e}")
    # 2) keyword scoring clásico
    q_lower = question.lower()
    q_words = set(re.findall(r"\w+", q_lower))
    scope = ""
    if context:
        scope = (context.get("assistantScope") or context.get("module") or "").lower()
    scored = []
    for doc in DOCS_CACHE:
        d_lower = doc["text"].lower()
        d_words = set(re.findall(r"\w+", d_lower))
        score = len(q_words & d_words)
        if scope:
            if scope in d_lower or scope in doc["file"].lower():
                score += 5
            if "5a" in q_lower and "principal" in scope and "5a" in d_lower:
                score += 10
            if "principal" in scope and ("19" in doc["file"] or "principal" in d_lower):
                score += 2
            if "auxiliar" in scope and ("26" in doc["file"] or "auxiliar" in d_lower):
                score += 2
        if "db" in q_lower and "db" in d_lower:
            score += 8
            if "db_correccion" in doc["file"].lower() or "secuencia_canonica" in doc["file"].lower():
                score += 12
        if "db" in q_lower and "canonica" in doc["file"].lower():
            score += 10
        if any(k in q_lower for k in ["2l","3l","2a"]) and "circuito_bajada" in doc["file"].lower():
            score += 15
        if "auxiliar" in q_lower and "auxiliar_bajada" in doc["file"].lower():
            score += 15
        if any(k in q_lower for k in ["hp", "potencia", "frame", "caballo", "cuantos hp", "cuántos hp"]):
            if "motores_frames" in doc["file"].lower():
                score += 20
            if "transc_20260907_1245" in doc["file"].lower():
                score += 10
            if "motores_y_resistencias" in doc["file"].lower():
                score -= 5
        if "auxiliar" in scope and "auxiliar" in q_lower and "bajada" in q_lower and "auxiliar" in d_lower:
            score += 8
        if "secuencia_canonica" in doc["file"].lower():
            score += 3
        scored.append((score, doc))
    scored.sort(key=lambda x: x[0], reverse=True)
    # 3) fusión híbrida: promedia vectorial + keyword, deduplica por file
    # si hay vector, combina; si no, solo keyword
    if vector_docs:
        # diccionario file -> mejor score combinado
        combined = {}
        for s, d in scored:
            combined[d["file"]] = combined.get(d["file"], 0) + s*0.6
        for s, d in vector_docs:
            # chunks vectoriales pueden tener file con #chunk, normaliza
            base = d["file"].split("#")[0]
            combined[base] = combined.get(base, 0) + s*0.4
            # también guarda texto del chunk para citar
            # si el chunk no está en scored, añádelo como doc candidato
        # re-rank: reconstruye lista a partir de combined y recupera docs originales + chunks vectoriales
        # prioriza chunks vectoriales si tienen texto más específico
        vec_map = {d["file"].split("#")[0] if "#" in d["file"] else d["file"]: d for _, d in vector_docs}
        ranked = sorted(combined.items(), key=lambda x: x[1], reverse=True)
        top = []
        for fname, _ in ranked[:top_k]:
            if fname in vec_map:
                top.append(vec_map[fname])
            else:
                # busca en DOCS_CACHE
                for _, d in scored:
                    if d["file"] == fname:
                        top.append(d)
                        break
        if not top:
            top = [d for _, d in scored[:top_k] if _ > 0] or DOCS_CACHE[:top_k]
        return top
    else:
        top = [d for s, d in scored[:top_k] if s > 0]
        if not top:
            top = DOCS_CACHE[:top_k]
        return top

def build_system_prompt(context: dict, retrieved: List[dict]):
    ctx_labels = {
        "crane": context.get("crane", "No especificada"),
        "module": context.get("module", "Consulta general"),
        "simulatorView": context.get("simulatorView", ""),
        "assistantScope": context.get("assistantScope", context.get("module", "consulta general")),
        "position": context.get("position", 0),
        "activeContacts": ", ".join(context.get("activeContacts", [])) or "Ninguno",
    }
    position_text = "Neutro" if ctx_labels["position"] == 0 else (
        f"Subir paso {ctx_labels['position']}" if ctx_labels["position"] > 0 else f"Bajar paso {abs(ctx_labels['position'])}"
    )
    # Nota de alcance para filtro
    scope_note = ""
    m = ctx_labels["module"].lower()
    if "principal" in m:
        scope_note = "Alcance filtrado: Gancho principal (28 BOX, 19/19A/19B/19C). Contactor 5A SOLO existe aquí. pClosedMap Principal: 5A cierra solo en +6 (subida) y en -1 a -2 (bajada): 5A = (p===6) || (p<=-1 && p>=-2). Si preguntan por 5A en otro paso (ej. +2) es normal que esté abierto."
    elif "auxiliar" in m:
        scope_note = "Alcance filtrado: Gancho auxiliar (20 BOX, 26/26A/26B). NO tiene 5A (A_SYMBOLS solo 1A-4A). aClosedMap Aux: H = p>0 (subida, junto con M en +1), M = p!=0, 1L = p<0 (SOLO bajada). H NUNCA depende de 1L ni está después de 1L; 1L es exclusivo bajada."
    elif "carro" in m:
        scope_note = "Alcance filtrado: Carro (traslación). Resistencias y contactores distintos a gancho."
    elif "avance" in m or "puente" in m:
        scope_note = "Alcance filtrado: Avance/Puente (traslación). Resistencias y contactores distintos a gancho."
    else:
        scope_note = "Alcance: Consulta general (sin filtro de movimiento)."
    docs_text = "\n\n".join([f"--- {d['file']} ---\n{d['text'][:1500]}" for d in retrieved])
    return f"""Eres Asistente Técnico de GruaHelper, modo piloto para grúa analógica DC 40/60s (contactores y resistencias, Grúa 2 aún no operativa). Tu tarea es orientar, NO diagnosticar de forma definitiva.

Contexto del simulador:
- Grúa: {ctx_labels['crane']} [filtro activo]
- Módulo: {ctx_labels['module']} (scope: {ctx_labels['assistantScope']}, vista: {ctx_labels['simulatorView']})
- Posición: {position_text} (valor {ctx_labels['position']})
- Contactos activos: {ctx_labels['activeContacts']}
- {scope_note}
 - Nota operativa: En subida (+1 a +6 principal / +1 a +5 auxiliar) es serie: M+H en +1 (ambos cierran al salir de neutro, H = p>0, M = p!=0), luego +1A en +2, +2A en +3, +3A en +4, +4A en +5, +5A en +6 (solo principal). Regla: 2A requiere 1A, 3A requiere 2A, 4A requiere 3A, 5A requiere 4A y H. H NO depende de 1L (1L = p<0 SOLO bajada). En bajada 5A y 4A solo en -1/-2, 4A persiste hasta -3; H no participa en bajada. Bobina 5A se alimenta por línea 13 del máster, interrumpida solo por contacto auxiliar de 4A (ver SECUENCIA_CONTACTORES_20260902.md). El fallo es físico o de secuencia, sin límites.
 - Regla de trampa 5A: Si preguntan por 5A y el filtro es gancho auxiliar/carro/avance o consulta general sin gancho principal, responder que 5A no existe en ese movimiento; solo gancho principal tiene 5A (pClosedMap). IMPORTANTE: cita el filtro activo tal cual aparece arriba (ej. "Gancho Auxiliar") y no lo cambies a "Gancho Principal" al describir el contexto actual; "Gancho Principal" solo aparece como sugerencia de cambio en questions.

Documentación / casos relevantes (usar solo si aplica, citar fuente):
{docs_text}

Reglas obligatorias:
1. No controles equipos. No anules protecciones, finales de carrera, frenos, paros de emergencia o enclavamientos.
2. Separa hechos / hipótesis / verificaciones. No preguntes por RACK/paño asociado a un contactor (no correlaciona). No inventes códigos/paneles, NUNCA preguntes por "códigos de error", "indicadores de falla en panel", "panel de control con códigos", "display de fallas" - es grúa analógica 40/60s sin códigos ni interfaz, solo contactores y resistencias. Circuito de corriente continua DC: alimentación es + y -, NO hay conexión a tierra, nunca preguntes por "continuidad a tierra" o "conexión a tierra de bobina". Si falta info, pide medición entre + y - o verificación física concreta.
3. Orden de hipótesis para contactor que no cierra: 1) falta de energía en bobina (+/-), 2) contacto previo no cierra — M+H en +1 no tienen previo; para 1A es H+M, para 2A es 1A, para 3A es 2A, para 4A es 3A, para 5A es 4A y H. H NUNCA tiene como previo a 1L (1L es solo bajada p<0); si falla H sospechar M o alimentación +/-, NO 1L. En bajada el asociado es 1L: primero verificar si 1L entra y si el resto de la secuencia tiene el mismo síntoma, 3) daño en conductor master→panel gancho (línea 13 para 5A solo, línea 11 para 4A subida; en bajada NO es 13), 4) AR time-delay que cierra a negativo / bobina abierta / contacto plata (solo después de mediciones). Respeta este orden y NO inventes para abultar: si el usuario solo dice "gancho no se mueve en primer punto bajar" sin mediciones, deja hypotheses vacío o con "No puedo dar hipótesis sin medir 1L y bobina vs +/-" y pregunta.
4. Si no hay evidencia, pide medición concreta antes de hipotetizar master. Está permitido y es preferible responder "No puedo dar una hipótesis concreta sin más datos" cuando falte información clave; en ese caso deja hypotheses vacío o con ese mensaje y usa questions para pedir síntoma exacto, posición/paso, qué se midió (tensión bobina +/-, continuidad 1L, si resto de secuencia falla igual). NUNCA rellenes hypotheses para completar campos.
5. CASO FUERA DE ALCANCE POR FILTRO (trampa 5A): Si preguntan por 5A y el filtro es Gancho auxiliar / Carro / Avance / Consulta general sin principal, NO rellenes hipótesis. Responde solo con summary + facts confirmando que 5A no existe en ese módulo (solo Gancho principal tiene 5A) y en "questions" pregunta únicamente si la selección de filtros es la adecuada. Deja hypotheses vacío. Ejemplo válido: summary="Se confirma que el contacto 5A no está presente en la secuencia de bajada para el módulo Gancho Auxiliar." facts=["El módulo actual es Gancho Auxiliar (GRÚA 1) [filtro activo].","Según la documentación y el filtro activo, el Gancho Auxiliar no posee el contacto 5A.","El contacto 5A es exclusivo del Gancho Principal."] questions=["¿Es correcta la selección actual (Gancho Auxiliar - GRÚA 1) o deseas cambiar el filtro a Gancho Principal para consultar 5A?"] IMPORTANTE: en facts usa exactamente el Módulo y Grúa del contexto; en questions menciona primero el filtro activo actual y luego sugiere Gancho Principal solo como alternativa.
6. CAPACIDAD LIMITADA Y ANTI-RELLENO: Si la consulta es ambigua o sin datos suficientes (ej. solo "gancho no se mueve en primer punto bajar" sin decir si 1L entra, sin tensión bobina), responde con honestidad capa por capa: summary breve, facts con lo poco confirmado, hypotheses = [] (vacío) y questions pidiendo: ¿entra 1L en bajada? ¿pasa en todos los puntos de bajada o solo en -1? ¿qué tensión +/ - hay en bobina 4A/3A y si AR cierra a negativo? NO inventes 3-4 hipótesis para llenar espacio.
7. BAJADA SIEMPRE 1L: En bajada el contactor que habilita es 1L (p<0). Si 1L no entra, nada de bajada funciona; pregunta primero por 1L y si el resto de la secuencia muestra el mismo síntoma antes de culpar 4A/3A.
8. HP/FRAME OBLIGATORIO CON DUTY CYCLE Y CORRIENTE 230V: Si preguntan HP, potencia, frame, corriente o "de cuántos HP es el motor de X", responde SOLO desde MOTORES_FRAMES_20260907.md + Captura.JPG/dimensiones + tabla corrientes 230V. REGLA DE OUTPUT: SIEMPRE incluir FRAME + AMBOS HP con ciclo + RPM según conexión + CORRIENTE ESTIMADA @230V CC. Formato: "Frame 616: 150 HP @60 MIN 75°C (SERIES 450 RPM / COMP 460 RPM / ADJ 460/1150) ≈541 A @230V η0.90 — 200 HP @30 MIN (400/430 RPM) ≈721 A; arranque 811–1081A". Aclarar SERIES=conexión serie (no serie 600), COMP=compound/shunt. Si preguntan sin ciclo, da ambos + corrientes y advierte "estimado a confirmar con placa (V,A,RPM)". Grúa 1 princ 616 150/200 HP 541/721A, aux 614 100/135 HP 360/487A, puente 2x612 75/100 HP 270/360A por motor, carro 606 25/33 HP 90/119A; G2/3 princ 614, aux 612, puente 608 35/45 HP 126/162A. Prohibido inventar (40 HP falso).
9. VOLTAJE BOBINAS CONTROL: Circuito de control fuerza es 230/240VDC nominal para contactores principales M,H,1A-5A,1L-3L,DB. Si reportan 110VDC en bobina principal, NO concluir "alimentación presente OK" — es subtensión (faltan ~120V) y explica que no cierre. Preguntar por medición +/- completa y fuente. Existen contactores puntuales con voltajes diferentes (se detallará) — no generalizar 230V a todos sin confirmar.
10. SEGUNDA RONDA — VERIFICACIÓN CONTROL: Tras la 1ª ronda donde pediste más info (ej. posición, tensión, si entra 1L), en la 2ª ronda con datos del usuario DEBES sugerir/verificar si en control está entrando correctamente: tensión +/- estable 230/240VDC en barras, sin caídas, contactos del máster y de secuencia previa cerrando (H/M para subida, 1L para bajada, AR time-delay cerrando a negativo antes de 1A). No vuelvas a pedir lo mismo: avanza a verificar entrada de control antes de saltar a bobina o cable.
11. PROPUESTA EXCLUSIONES (no verdad absoluta, pendiente validar): Owner propuso 7 reglas (H vs 1L excluyentes, DB solo neutro/-1, 1L→2L→3L secuencial, 1A→5A acumulativo, M requerido para H/1L, etc.) — aún no canónico. Verificar contra pClosedMap/aClosedMap y SECUENCIA_CANONICA antes de asumir.
7. Responde SIEMPRE en JSON válido con esta estructura exacta, sin texto fuera del JSON:
{{
  "mode": "API local Ollama ({OLLAMA_MODEL_DEFAULT})",
  "summary": "Resumen breve",
  "facts": ["hecho 1"],
  "hypotheses": ["hipótesis 1"],
  "questions": ["verificación pendiente 1"],
  "safety": "{ASSISTANT_SAFETY_NOTICE}",
  "sources": ["archivo.md sección X o 'Modo local sin fuente específica'"]
}}
No añadas markdown, ni ```json, solo el objeto JSON puro. No uses <think> ni bloques de razonamiento, responde directamente con el JSON.
"""

def extract_json(text: str):
    """Extrae JSON aunque venga envuelto en ```json, <think> o texto extra."""
    # elimina bloques <think>...</think> de Qwen/Groq
    try:
        text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)
    except:
        pass
    # intento directo
    try:
        return json.loads(text.strip())
    except:
        pass
    # busca bloque ```json ... ```
    m = re.search(r"```(?:json)?\s*(\{{.*\}})\s*```", text, re.DOTALL)
    if m:
        try:
            return json.loads(m.group(1))
        except:
            pass
    # busca primer { ... } balanceado
    m = re.search(r"\{.*\}", text, re.DOTALL)
    if m:
        try:
            return json.loads(m.group(0))
        except:
            pass
    return None

@app.get("/api/health")
async def health():
    # verifica Ollama o Groq/DeepSeek
    if IS_GROQ:
        try:
            async with httpx.AsyncClient(timeout=5) as client:
                r = await client.get(f"{OLLAMA_URL}/models", headers={"Authorization": f"Bearer {API_KEY}"})
                groq_ok = r.status_code == 200
                models = r.json().get("data", []) if groq_ok else []
                model_names = [m.get("id") for m in models] if groq_ok else []
        except Exception as e:
            groq_ok = False
            model_names = []
            e_msg = str(e)
        else:
            e_msg = ""
        return {
            "status": "ok",
            "backend": "GruaHelper Groq Wrapper",
            "ollama_url": OLLAMA_URL,
            "ollama_ok": groq_ok,
            "model_actual": OLLAMA_MODEL_DEFAULT,
            "model_switch_note": MODEL_SWITCH_NOTE,
            "ollama_models": model_names,
            "docs_loaded": len(DOCS_CACHE),
            "error": e_msg,
            "provider": "groq",
        }
    else:
        try:
            async with httpx.AsyncClient(timeout=5) as client:
                r = await client.get(f"{OLLAMA_URL}/api/tags")
                ollama_ok = r.status_code == 200
                models = r.json().get("models", []) if ollama_ok else []
        except Exception as e:
            ollama_ok = False
            models = []
            e_msg = str(e)
        else:
            e_msg = ""
        return {
            "status": "ok",
            "backend": "GruaHelper Ollama Wrapper",
            "ollama_url": OLLAMA_URL,
            "ollama_ok": ollama_ok,
            "model_actual": OLLAMA_MODEL_DEFAULT,
            "model_switch_note": MODEL_SWITCH_NOTE,
            "ollama_models": [m.get("name") for m in models] if ollama_ok else [],
            "docs_loaded": len(DOCS_CACHE),
            "error": e_msg,
            "provider": "ollama",
        }

@app.get("/api/models")
async def list_models():
    if IS_GROQ:
        try:
            async with httpx.AsyncClient(timeout=5) as client:
                r = await client.get(f"{OLLAMA_URL}/models", headers={"Authorization": f"Bearer {API_KEY}"})
                r.raise_for_status()
                return r.json()
        except Exception as e:
            return JSONResponse(status_code=502, content={"error": str(e), "ollama_url": OLLAMA_URL, "provider": "groq"})
    else:
        try:
            async with httpx.AsyncClient(timeout=5) as client:
                r = await client.get(f"{OLLAMA_URL}/api/tags")
                r.raise_for_status()
                return r.json()
        except Exception as e:
            return JSONResponse(status_code=502, content={"error": str(e), "ollama_url": OLLAMA_URL})

@app.get("/api/validaciones/pendientes")
async def validaciones_pendientes():
    return {"pendientes": _load_json(PENDING_FILE), "validadas": _load_json(VALIDATED_FILE)}

@app.post("/api/validaciones/aprobar")
async def validaciones_aprobar(request: Request):
    body = await request.json()
    vid = body.get("id")
    if not vid:
        return JSONResponse(status_code=400, content={"error": "id requerido"})
    pendientes=_load_json(PENDING_FILE)
    validadas=_load_json(VALIDATED_FILE)
    found=None
    remain=[]
    for p in pendientes:
        if p.get("id")==vid:
            found=p
        else:
            remain.append(p)
    if not found:
        return JSONResponse(status_code=404, content={"error": "no encontrado"})
    found["estado"]="validada"
    found["validada_at"]=datetime.now(timezone.utc).isoformat()
    found["validador"]=body.get("validador","owner")
    validadas.append(found)
    _save_json(PENDING_FILE, remain)
    _save_json(VALIDATED_FILE, validadas)
    # también persiste como caso validado en docs para RAG futuro
    casos_path = Path(__file__).parent / "docs" / "CASOS_VALIDADOS_POR_USUARIO.md"
    entry_md = f"\n## {found['timestamp'][:10]} {found['id']} - {found['context'].get('module','?')} {found['context'].get('crane','?')} pos {found['context'].get('position','?')}\n**Reportado:** {found['question']}\n**Validado por:** {found['validador']} el {found['validada_at']}\n**Estado:** validada - usar como caso empírico\n"
    try:
        with open(casos_path, "a", encoding="utf-8") as f:
            f.write(entry_md)
    except: pass
    return {"ok": True, "validada": found, "pendientes_restantes": len(remain)}

@app.post("/api/diagnostico")
async def diagnostico(request: Request):
    body = await request.json()
    question = (body.get("question") or "").strip()
    context = body.get("context") or {}
    session_id = body.get("sessionId") or request.client.host or "default"
    requested_model = body.get("model") or OLLAMA_MODEL_DEFAULT

    if not question:
        return JSONResponse(status_code=400, content={"error": "question vacía"})

    # Si usuario reporta solución, guarda como pendiente (no auto-valida)
    pending_entry=None
    if detect_solucion_reportada(question):
        pending_entry=add_pending(question, context, session_id)

    # Recupera docs relevantes (con boost por filtro)
    retrieved = retrieve_docs(question, context, top_k=2)
    system_prompt = build_system_prompt(context, retrieved)

    # Historial simple por sessionId
    hist = HISTORIAL.get(session_id, [])
    messages = hist[-MAX_HISTORIAL_TURNS*2:]  # últimos turnos
    # Añade system + pregunta actual
    ollama_messages = [{"role": "system", "content": system_prompt}] + messages + [{"role": "user", "content": question}]

    # Llama a Ollama o Groq
    if IS_GROQ:
        payload = {
            "model": requested_model,
            "messages": ollama_messages,
            "stream": False,
            "temperature": 0.2,
            "max_tokens": 1500,
        }
        headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
        endpoint = f"{OLLAMA_URL}/chat/completions"
        try:
            async with httpx.AsyncClient(timeout=180) as client:
                r = await client.post(endpoint, json=payload, headers=headers)
                r.raise_for_status()
                data = r.json()
                content = data.get("choices", [{}])[0].get("message", {}).get("content", "") or ""
        except Exception as e:
            return JSONResponse(status_code=502, content={
                "mode": "Error Groq",
                "summary": f"No se pudo consultar Groq: {e}",
                "facts": [f"Modelo: {requested_model}", f"Groq URL: {OLLAMA_URL}"],
                "hypotheses": [],
                "questions": [],
                "safety": ASSISTANT_SAFETY_NOTICE,
                "sources": []
            })
    else:
        payload = {
            "model": requested_model,
            "messages": ollama_messages,
            "stream": False,
            "think": False,
            "format": "json",
            "options": {"temperature": 0.2, "num_predict": 600}
        }
        try:
            async with httpx.AsyncClient(timeout=180) as client:
                r = await client.post(f"{OLLAMA_URL}/api/chat", json=payload)
                if r.status_code == 404:
                    gen_payload = {"model": requested_model, "prompt": system_prompt + "\n\nPregunta: " + question, "stream": False, "format": "json"}
                    r = await client.post(f"{OLLAMA_URL}/api/generate", json=gen_payload, timeout=180)
                    content = r.json().get("response", "")
                else:
                    r.raise_for_status()
                    data = r.json()
                    content = data.get("message", {}).get("content", "") or data.get("response", "")
        except httpx.ConnectError:
            return JSONResponse(status_code=502, content={
                "mode": "Error",
                "summary": "Ollama no está corriendo. Ejecuta 'ollama serve' primero.",
                "facts": [f"Ollama URL: {OLLAMA_URL}", f"Modelo solicitado: {requested_model}"],
                "hypotheses": [],
                "questions": ["¿Ejecutaste 'ollama serve' en otra terminal?"],
                "safety": ASSISTANT_SAFETY_NOTICE,
                "sources": []
            })
        except Exception as e:
            return JSONResponse(status_code=502, content={
                "mode": "Error backend",
                "summary": f"No se pudo consultar Ollama: {e}",
                "facts": [f"Modelo: {requested_model}", f"Ollama URL: {OLLAMA_URL}"],
                "hypotheses": [],
                "questions": [],
                "safety": ASSISTANT_SAFETY_NOTICE,
                "sources": []
            })

    # Parsea JSON de respuesta
    parsed = extract_json(content)
    if not parsed:
        # fallback: envuelve texto bruto en formato esperado
        parsed = {
            "mode": f"API local Ollama ({requested_model}) - texto libre",
            "summary": content[:400] if content else "Sin respuesta del modelo",
            "facts": [f"Contexto: {context.get('module','')} pos {context.get('position',0)}", f"Pregunta: {question}"],
            "hypotheses": ["Respuesta no vino en JSON, se muestra texto bruto"],
            "questions": ["Reintenta con pregunta más específica"],
            "safety": ASSISTANT_SAFETY_NOTICE,
            "sources": [d["file"] for d in retrieved]
        }
    else:
        # asegura campos obligatorios y normaliza tipos
        parsed.setdefault("mode", f"API local Ollama ({requested_model})")
        parsed.setdefault("safety", ASSISTANT_SAFETY_NOTICE)
        parsed.setdefault("sources", [d["file"] for d in retrieved])
        # normaliza sources a lista si el modelo devolvió string
        if isinstance(parsed.get("sources"), str):
            parsed["sources"] = [parsed["sources"]]
        for k in ["facts","hypotheses","questions"]:
            if isinstance(parsed.get(k), str):
                parsed[k] = [parsed[k]]

    # Guarda en historial
    HISTORIAL[session_id] = (hist + [{"role": "user", "content": question}, {"role": "assistant", "content": json.dumps(parsed, ensure_ascii=False)}])[-MAX_HISTORIAL_TURNS*2:]

    # Añade nota de cambio de modelo y de validación pendiente
    parsed["_meta"] = {"model_usado": requested_model, "model_default": OLLAMA_MODEL_DEFAULT, "switch_note": "Para cambiar de modelo avisa y se actualiza OLLAMA_MODEL"}
    if pending_entry:
        parsed["_pending_validacion"] = {"id": pending_entry["id"], "estado": "pendiente_validacion", "nota": "Solución reportada quedó pendiente de tu visto bueno. Usa GET /api/validaciones/pendientes y POST /api/validaciones/aprobar {id}"}

    return JSONResponse(content=parsed)

@app.post("/api/diagnostico/stream")
async def diagnostico_stream(request: Request):
    body = await request.json()
    question = (body.get("question") or "").strip()
    context = body.get("context") or {}
    session_id = body.get("sessionId") or request.client.host or "default"
    requested_model = body.get("model") or OLLAMA_MODEL_DEFAULT
    if not question:
        return JSONResponse(status_code=400, content={"error": "question vacía"})
    if detect_solucion_reportada(question):
        add_pending(question, context, session_id)
    retrieved = retrieve_docs(question, context, top_k=2)
    system_prompt = build_system_prompt(context, retrieved)
    hist = HISTORIAL.get(session_id, [])
    messages = hist[-MAX_HISTORIAL_TURNS*2:]
    ollama_messages = [{"role": "system", "content": system_prompt}] + messages + [{"role": "user", "content": question}]
    if IS_GROQ:
        payload = {
            "model": requested_model,
            "messages": ollama_messages,
            "stream": True,
            "temperature": 0.2,
            "max_tokens": 1500,
        }
        headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
        endpoint = f"{OLLAMA_URL}/chat/completions"
        async def event_generator():
            full_content = ""
            try:
                async with httpx.AsyncClient(timeout=300) as client:
                    async with client.stream("POST", endpoint, json=payload, headers=headers) as r:
                        async for line in r.aiter_lines():
                            if not line:
                                continue
                            if line.startswith("data: "):
                                data_str = line[6:].strip()
                                if data_str == "[DONE]":
                                    break
                                try:
                                    data = json.loads(data_str)
                                except:
                                    continue
                                delta = data.get("choices", [{}])[0].get("delta", {}).get("content", "")
                                if delta:
                                    full_content += delta
                                    yield f"data: {json.dumps({'token': delta}, ensure_ascii=False)}\n\n"
                            else:
                                continue
                try:
                    parsed = extract_json(full_content)
                    if not parsed:
                        parsed = {"mode": f"API Groq ({requested_model}) - texto libre", "summary": full_content[:400], "facts": [], "hypotheses": [], "questions": [], "safety": ASSISTANT_SAFETY_NOTICE, "sources": [d["file"] for d in retrieved]}
                    else:
                        if isinstance(parsed.get("sources"), str):
                            parsed["sources"] = [parsed["sources"]]
                    HISTORIAL[session_id] = (hist + [{"role": "user", "content": question}, {"role": "assistant", "content": json.dumps(parsed, ensure_ascii=False)}])[-MAX_HISTORIAL_TURNS*2:]
                    yield f"data: {json.dumps({'done': True, 'final': parsed}, ensure_ascii=False)}\n\n"
                except Exception as e:
                    yield f"data: {json.dumps({'done': True, 'error': str(e)}, ensure_ascii=False)}\n\n"
            except Exception as e:
                yield f"data: {json.dumps({'error': str(e)}, ensure_ascii=False)}\n\n"
        return StreamingResponse(event_generator(), media_type="text/event-stream", headers={"Cache-Control": "no-cache", "Connection": "keep-alive", "X-Accel-Buffering": "no"})
    else:
        payload = {
            "model": requested_model,
            "messages": ollama_messages,
            "stream": True,
            "think": False,
            "format": "json",
            "options": {"temperature": 0.2, "num_predict": 600}
        }
        async def event_generator():
            full_content = ""
            try:
                async with httpx.AsyncClient(timeout=300) as client:
                    async with client.stream("POST", f"{OLLAMA_URL}/api/chat", json=payload) as r:
                        async for line in r.aiter_lines():
                            if not line:
                                continue
                            try:
                                data = json.loads(line)
                            except:
                                continue
                            token = data.get("message", {}).get("content", "")
                            if token:
                                full_content += token
                                yield f"data: {json.dumps({'token': token}, ensure_ascii=False)}\n\n"
                            if data.get("done"):
                                break
                try:
                    parsed = extract_json(full_content)
                    if not parsed:
                        parsed = {"mode": f"API local Ollama ({requested_model}) - texto libre", "summary": full_content[:400], "facts": [], "hypotheses": [], "questions": [], "safety": ASSISTANT_SAFETY_NOTICE, "sources": [d["file"] for d in retrieved]}
                    else:
                        if isinstance(parsed.get("sources"), str):
                            parsed["sources"] = [parsed["sources"]]
                    HISTORIAL[session_id] = (hist + [{"role": "user", "content": question}, {"role": "assistant", "content": json.dumps(parsed, ensure_ascii=False)}])[-MAX_HISTORIAL_TURNS*2:]
                    yield f"data: {json.dumps({'done': True, 'final': parsed}, ensure_ascii=False)}\n\n"
                except Exception as e:
                    yield f"data: {json.dumps({'done': True, 'error': str(e)}, ensure_ascii=False)}\n\n"
            except Exception as e:
                yield f"data: {json.dumps({'error': str(e)}, ensure_ascii=False)}\n\n"
        return StreamingResponse(event_generator(), media_type="text/event-stream", headers={"Cache-Control": "no-cache", "Connection": "keep-alive", "X-Accel-Buffering": "no"})

@app.get("/")
async def root():
    return {"message": "GruaHelper backend activo", "endpoint": "/api/diagnostico", "health": "/api/health", "model_actual": OLLAMA_MODEL_DEFAULT, "nota": MODEL_SWITCH_NOTE}

if __name__ == "__main__":
    import uvicorn
    load_docs()
    print(f"[backend] Iniciando en http://localhost:{BACKEND_PORT}")
    print(f"[backend] {MODEL_SWITCH_NOTE}")
    print(f"[backend] Ollama URL: {OLLAMA_URL}")
    uvicorn.run(app, host="0.0.0.0", port=BACKEND_PORT)
