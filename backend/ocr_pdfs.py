import pathlib, re, sys
import fitz  # pymupdf
import pytesseract
from PIL import Image
import io

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

src_root = pathlib.Path(r"C:\Users\PC2B\Downloads\info")
out_root = pathlib.Path(r"C:\Users\PC2B\Documents\Pruebas\AN\backend\docs\pdfs_txt")
out_root.mkdir(parents=True, exist_ok=True)

# Solo re-procesa los que hoy están vacíos (<700 chars = escaneado)
pdfs = list(src_root.rglob("*.pdf"))
print(f"Total PDFs: {len(pdfs)}")
todo = []
for pdf in pdfs:
    rel = str(pdf.relative_to(src_root)).replace("\\", "__").replace("/", "__").replace(".pdf", ".txt")
    out_path = out_root / rel
    needs_ocr = True
    if out_path.exists():
        try:
            txt = out_path.read_text(encoding="utf-8")
            # si tiene >800 chars útiles, ya está bien
            if len(txt) > 800 and "AutoCAD Drawing" not in txt[:500]:
                needs_ocr = False
            else:
                # marca como escaneado
                needs_ocr = "escaneado sin texto" in txt or "AutoCAD 2007 Drawing" in txt
        except:
            needs_ocr = True
    if needs_ocr:
        todo.append(pdf)

print(f"A OCR: {len(todo)}")
for idx, pdf in enumerate(todo, 1):
    print(f"[{idx}/{len(todo)}] OCR {pdf.relative_to(src_root)}")
    try:
        doc = fitz.open(pdf)
        full_text = ""
        for page_num, page in enumerate(doc):
            # primero intento texto nativo
            t = page.get_text("text")
            if t and len(t.strip()) > 100 and "AutoCAD" not in t:
                full_text += t + "\n"
                continue
            # OCR via raster + tesseract
            pix = page.get_pixmap(dpi=300)
            img_data = pix.tobytes("png")
            img = Image.open(io.BytesIO(img_data))
            # tesseract con config para planos (eng+spa)
            ocr_text = pytesseract.image_to_string(img, lang="eng+spa", config="--psm 6")
            if ocr_text.strip():
                full_text += ocr_text + "\n"
            else:
                full_text += f"[Página {page_num+1} sin texto]\n"
        full_text = re.sub(r'\s+', ' ', full_text).strip()
        if len(full_text) < 50:
            full_text = f"[PDF escaneado sin texto extraíble tras OCR: {pdf.name}]"
        rel = str(pdf.relative_to(src_root)).replace("\\", "__").replace("/", "__").replace(".pdf", ".txt")
        out_path = out_root / rel
        out_path.write_text(f"# {pdf.name}\nFuente: {pdf}\n\n{full_text[:15000]}", encoding="utf-8")
        print(f"  -> {rel} ({len(full_text)} chars)")
    except Exception as e:
        print(f"  ERR {pdf.name}: {e}")

print("OCR listo")
