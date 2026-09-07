import fitz  # pymupdf
import pathlib, os, re
src_root = pathlib.Path(r"C:\Users\PC2B\Downloads\info")
out_root = pathlib.Path(r"C:\Users\PC2B\Documents\Pruebas\AN\backend\docs\pdfs_txt")
out_root.mkdir(parents=True, exist_ok=True)
pdfs = list(src_root.rglob("*.pdf"))
print(f"Encontrados {len(pdfs)} PDFs")
for pdf in pdfs:
    try:
        doc = fitz.open(pdf)
        text = ""
        for page in doc:
            t = page.get_text("text")
            if t:
                text += t + "\n"
        # fallback: si no hay texto (escaneado), deja marca
        if not text.strip():
            text = f"[PDF escaneado sin texto extraíble: {pdf.name} - requiere OCR manual]"
        # limpia
        text = re.sub(r'\s+', ' ', text)[:15000]  # limita 15k por archivo para RAG
        # nombre salida relativo
        rel = pdf.relative_to(src_root)
        out_name = str(rel).replace("\\", "__").replace("/", "__").replace(".pdf", ".txt")
        out_path = out_root / out_name
        out_path.write_text(f"# {pdf.name}\nFuente: {pdf}\n\n{text}", encoding="utf-8")
        print(f"OK {pdf.name} -> {out_name} ({len(text)} chars)")
    except Exception as e:
        print(f"ERR {pdf}: {e}")
print("Listo")
