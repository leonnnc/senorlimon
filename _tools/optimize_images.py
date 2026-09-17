# -*- coding: utf-8 -*-
"""Convierte las imagenes descargadas a WebP optimizado para web"""
import os, json, io
from PIL import Image, ImageOps

RAW = r"C:\Users\leonn\Documents\web\senorlimon\_raw\img"
OUT = r"C:\Users\leonn\Documents\web\senorlimon\assets\img"
os.makedirs(OUT, exist_ok=True)

# key destino -> (ancho maximo, calidad, recorte cuadrado?)
SPECS = {
    "hero-cebiche": (1600, 82, False),
    "logo": (560, 88, False),
    "logo-marca": (512, 88, False),
    "tarjetas": (320, 85, False),
    "favicon": (256, 90, True),
}

# la imagen principal del hero
HERO_SRC = "plato-ceviche-mixto.png"


def save_webp(im, dest, quality):
    if im.mode in ("RGBA", "LA", "P"):
        im = im.convert("RGBA")
    else:
        im = im.convert("RGB")
    im.save(dest, "WEBP", quality=quality, method=6)


def resize(im, width, square=False):
    if square:
        im = ImageOps.fit(im, (width, width), method=Image.LANCZOS)
        return im
    if im.width > width:
        h = round(im.height * width / im.width)
        im = im.resize((width, h), Image.LANCZOS)
    return im


report = []

# hero
src = os.path.join(RAW, HERO_SRC)
im = Image.open(src)
w, q, sq = SPECS["hero-cebiche"]
dest = os.path.join(OUT, "hero-cebiche.webp")
save_webp(resize(im, w, sq), dest, q)
report.append(("hero-cebiche", os.path.getsize(src), os.path.getsize(dest)))

# logo principal
src = os.path.join(RAW, "logo.png")
im = Image.open(src)
w, q, sq = SPECS["logo"]
dest = os.path.join(OUT, "logo.webp")
save_webp(resize(im, w, sq), dest, q)
report.append(("logo", os.path.getsize(src), os.path.getsize(dest)))

# marca (personaje limon) + favicon
src = os.path.join(RAW, "logo-footer.png")
im = Image.open(src)
w, q, sq = SPECS["logo-marca"]
dest = os.path.join(OUT, "marca.webp")
save_webp(resize(im, w, sq), dest, q)
report.append(("marca", os.path.getsize(src), os.path.getsize(dest)))
w, q, sq = SPECS["favicon"]
resize(im, w, sq).convert("RGBA").save(os.path.join(OUT, "favicon.png"), "PNG", optimize=True)

# tarjetas de pago
src = os.path.join(RAW, "tarjetas.png")
if os.path.exists(src):
    im = Image.open(src)
    w, q, sq = SPECS["tarjetas"]
    dest = os.path.join(OUT, "tarjetas.webp")
    save_webp(resize(im, w, sq), dest, q)
    report.append(("tarjetas", os.path.getsize(src), os.path.getsize(dest)))

# fotos de platos: sin recorte, ancho maximo 900, calidad 78
platos = [f for f in os.listdir(RAW) if f.startswith("plato-")]
total_before = total_after = 0
for f in sorted(platos):
    if f == HERO_SRC:
        pass
    src = os.path.join(RAW, f)
    name = os.path.splitext(f)[0] + ".webp"
    dest = os.path.join(OUT, name)
    try:
        im = Image.open(src)
        before = os.path.getsize(src)
        save_webp(resize(im, 900), dest, 78)
        after = os.path.getsize(dest)
        total_before += before
        total_after += after
        report.append((name, before, after))
    except Exception as e:
        print("ERROR %s: %s" % (f, e))

print("%-46s %10s %10s" % ("archivo", "antes", "despues"))
for name, b, a in report:
    pct = (100.0 * a / b) if b else 0
    print("%-46s %9.0fK %9.0fK  %5.1f%%" % (name, b / 1024, a / 1024, pct))
print("-" * 70)
print("platos: %.2f MB -> %.2f MB" % (total_before / 1048576, total_after / 1048576))
