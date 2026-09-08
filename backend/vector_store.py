"""
GruaHelper - Vector store híbrido offline sin API
Sin dependencias externas: usa TF-IDF + cosine con numpy (stdlib + numpy ya instalado).
Cuando esté sentence-transformers/Ollama instalado, cambia EMBEDDING_MODE a 'transformer' o 'ollama'.
"""
import re, math, json, time, hashlib
from pathlib import Path
import numpy as np

# Config
EMBEDDING_MODE = "tfidf"  # tfidf | transformer | ollama
CACHE_FILE = Path(__file__).parent / "data" / "vector_cache.json"
MAX_CHUNK_CHARS = 1200
CHUNK_OVERLAP = 200

_stop_es = set("el la de que y a en un ser se no haber por con su para como estar tener le lo todo pero más hacer o poder decir este ir otro ese la si me ya ver porque dar cuando él muy sin vez mucho saber qué sobre mi mismo hasta trabajo tan entre".split())

def _tokenize(text):
    toks = re.findall(r"[a-záéíóúñ0-9]+", text.lower())
    return [t for t in toks if t not in _stop_es and len(t) > 2]

def chunk_text(text, max_chars=MAX_CHUNK_CHARS, overlap=CHUNK_OVERLAP):
    if len(text) <= max_chars:
        return [text]
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + max_chars, len(text))
        # corta en párrafo
        if end < len(text):
            cut = text.rfind("\n", start, end)
            if cut > start + max_chars//2:
                end = cut
        chunks.append(text[start:end])
        if end >= len(text):
            break
        start = end - overlap
    return chunks

class TfidfVectorStore:
    def __init__(self):
        self.vocab = {}  # token -> idx
        self.idf = np.array([])
        self.doc_vectors = []  # list of np arrays normalized
        self.chunks = []  # list of {file, text, chunk_id}
        self.built_at = 0

    def build(self, docs):
        """docs: list of {file, text}"""
        self.chunks = []
        for d in docs:
            for i, ch in enumerate(chunk_text(d["text"])):
                self.chunks.append({"file": d["file"], "text": ch, "chunk_id": f"{d['file']}#{i}", "doc_file": d["file"]})
        # vocab
        df = {}
        tokenized = []
        for ch in self.chunks:
            toks = _tokenize(ch["text"])
            uniq = set(toks)
            for t in uniq:
                df[t] = df.get(t, 0) + 1
            tokenized.append(toks)
        vocab_list = sorted(df.keys())
        self.vocab = {t:i for i,t in enumerate(vocab_list)}
        N = len(self.chunks)
        self.idf = np.array([math.log((N+1)/(df[t]+1))+1 for t in vocab_list], dtype=np.float32)
        # vectors
        self.doc_vectors = []
        for toks in tokenized:
            vec = np.zeros(len(vocab_list), dtype=np.float32)
            if not toks:
                self.doc_vectors.append(vec)
                continue
            counts = {}
            for t in toks:
                counts[t] = counts.get(t, 0) + 1
            for t, c in counts.items():
                if t in self.vocab:
                    idx = self.vocab[t]
                    tf = c / len(toks)
                    vec[idx] = tf * self.idf[idx]
            norm = np.linalg.norm(vec)
            if norm > 0:
                vec /= norm
            self.doc_vectors.append(vec)
        self.built_at = time.time()
        # cache simple
        try:
            CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
            # no guardamos vectores grandes, solo marca
            CACHE_FILE.write_text(json.dumps({"built_at": self.built_at, "n_chunks": len(self.chunks), "vocab": len(vocab_list)}, ensure_ascii=False), encoding="utf-8")
        except:
            pass
        print(f"[vector] TF-IDF built: {len(self.chunks)} chunks, vocab {len(vocab_list)}")
        return self

    def query(self, text, top_k=3):
        if not self.doc_vectors:
            return []
        toks = _tokenize(text)
        if not toks:
            return []
        qvec = np.zeros(len(self.vocab), dtype=np.float32)
        counts = {}
        for t in toks:
            counts[t] = counts.get(t, 0) + 1
        for t, c in counts.items():
            if t in self.vocab:
                idx = self.vocab[t]
                tf = c / len(toks)
                qvec[idx] = tf * self.idf[idx]
        norm = np.linalg.norm(qvec)
        if norm > 0:
            qvec /= norm
        else:
            return []
        scores = []
        for i, dvec in enumerate(self.doc_vectors):
            s = float(np.dot(qvec, dvec))
            # boost por coincidencia literal de palabras clave críticas aún en vectorial
            scores.append((s, self.chunks[i]))
        scores.sort(key=lambda x: x[0], reverse=True)
        return scores[:top_k]

# Singleton
_store = None

def get_store(docs):
    global _store
    # rebuild si no existe o si docs cambió (hash simple por count)
    need_build = _store is None or len(_store.chunks) == 0
    # también si pasó >300s como DOCS_CACHE
    if _store and time.time() - _store.built_at > 300:
        need_build = True
    if need_build:
        _store = TfidfVectorStore().build(docs)
    return _store

def vector_search(question, context, docs, top_k=3):
    """Retorna list de (score, chunk) por similitud vectorial. Chunk tiene {file,text}."""
    store = get_store(docs)
    # expande query con contexto para mejor recall
    q_expanded = question
    if context:
        scope = (context.get("assistantScope") or context.get("module") or "")
        crane = context.get("crane") or ""
        if scope:
            q_expanded += " " + scope
        if crane:
            q_expanded += " " + crane
    results = store.query(q_expanded, top_k=top_k)
    # mapea a formato doc {file, text}
    docs_out = []
    for score, ch in results:
        docs_out.append((score, {"file": ch["file"], "text": ch["text"]}))
    return docs_out
