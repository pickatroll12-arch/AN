"""One-off generator for GruaHelper PWA icons. Not part of the app runtime."""
from PIL import Image, ImageDraw

BG = (26, 31, 46, 255)      # #1a1f2e
ACCENT = (232, 137, 74, 255)  # #e8894a
CABLE = (59, 91, 219, 255)   # #3b5bdb


def draw_hook(size, maskable=False):
    img = Image.new("RGBA", (size, size), BG)
    d = ImageDraw.Draw(img)

    pad = size * (0.18 if maskable else 0.10)
    radius = size * 0.22
    d.rounded_rectangle([0, 0, size - 1, size - 1], radius=radius, fill=BG)

    cx = size / 2
    top = pad
    bottom = size - pad

    beam_h = size * 0.07
    d.rounded_rectangle([pad, top, size - pad, top + beam_h], radius=beam_h * 0.3, fill=ACCENT)

    cable_w = max(2, size * 0.018)
    cable_top = top + beam_h
    cable_bottom = bottom - size * 0.16
    d.line([(cx, cable_top), (cx, cable_bottom)], fill=CABLE, width=int(cable_w * 2))

    hook_r = size * 0.14
    d.ellipse([cx - hook_r * 0.55, cable_bottom - hook_r * 0.1,
               cx + hook_r * 1.45, cable_bottom + hook_r * 1.9],
              outline=ACCENT, width=int(size * 0.035))

    return img


for name, size, maskable in [
    ("icon-192.png", 192, False),
    ("icon-512.png", 512, False),
    ("icon-maskable-192.png", 192, True),
    ("icon-maskable-512.png", 512, True),
    ("apple-touch-icon.png", 180, False),
    ("favicon-32.png", 32, False),
    ("favicon-16.png", 16, False),
]:
    im = draw_hook(size, maskable)
    if name == "apple-touch-icon.png":
        im = im.convert("RGB")
    im.save(f"/home/user/AN/icons/{name}")

print("done")
