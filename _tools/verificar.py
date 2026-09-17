# -*- coding: utf-8 -*-
"""Verifica enlaces, recursos y consistencia de datos del sitio generado"""
import io, json, os, re, sys

RAIZ = r"C:\Users\leonn\Documents\web\senorlimon"
errores, avisos = [], []

html_files = [f for f in os.listdir(RAIZ) if f.endswith(".html")]
html_files.sort()

# ---------- 1. recursos y enlaces locales ----------
for nombre in html_files:
    ruta = os.path.join(RAIZ, nombre)
    txt = io.open(ruta, encoding="utf-8").read()
    refs = re.findall(r'(?:src|href)="([^"]+)"', txt)
    for r in refs:
        if r.startswith(("http", "#", "tel:", "mailto:", "data:")):
            continue
        destino = r.split("#")[0]
        if not destino:
            continue
        if not os.path.exists(os.path.join(RAIZ, destino.replace("/", os.sep))):
            errores.append("%s -> recurso inexistente: %s" % (nombre, destino))
    # anclas internas
    ids = set(re.findall(r'id="([^"]+)"', txt))
    for r in refs:
        if "#" in r and not r.startswith("http"):
            ancla = r.split("#", 1)[1]
            if ancla and ancla not in ids:
                avisos.append("%s -> ancla #%s no está en esta página (puede ser de otra página): %s" % (nombre, ancla, r))

# ---------- 2. datos ----------
txt = io.open(os.path.join(RAIZ, "assets", "js", "data.js"), encoding="utf-8").read()
datos = json.loads(txt.split("=", 1)[1].rsplit(";", 1)[0])
imgs_datos = []
platos = 0
for cat in datos["categorias"]:
    for sub in cat["subs"]:
        for it in sub["items"]:
            platos += 1
            if it.get("img"):
                imgs_datos.append(it["img"])
for p in datos.get("destacados", []):
    if p.get("img"):
        imgs_datos.append(p["img"])
for l in datos.get("locales", []):
    if l.get("mapa"):
        imgs_datos.append(l["mapa"])

for img in set(imgs_datos):
    if not os.path.exists(os.path.join(RAIZ, "assets", "img", img)):
        errores.append("data.js -> imagen inexistente: %s" % img)

en_disco = set(os.listdir(os.path.join(RAIZ, "assets", "img")))
usadas = set(imgs_datos) | {"hero-cebiche.webp", "logo.webp", "marca.webp", "tarjetas.webp", "favicon.png"}
huerfanas = sorted(f for f in en_disco if f not in usadas and not f.startswith("plato-mesa-de-trabajo"))
if huerfanas:
    avisos.append("imágenes sin usar en assets/img: %d (%s...)" % (len(huerfanas), ", ".join(huerfanas[:6])))

# ---------- 3. SEO por página ----------
for nombre in html_files:
    txt = io.open(os.path.join(RAIZ, nombre), encoding="utf-8").read()
    if 'name="description"' not in txt:
        errores.append("%s -> sin meta description" % nombre)
    if 'property="og:image"' not in txt:
        errores.append("%s -> sin og:image" % nombre)
    if 'rel="canonical"' not in txt:
        errores.append("%s -> sin canonical" % nombre)
    if "<h1" not in txt:
        errores.append("%s -> sin h1" % nombre)
    if txt.count("<h1") > 1:
        avisos.append("%s -> más de un h1" % nombre)
    for img_tag in re.findall(r"<img\b[^>]*>", txt):
        if "alt=" not in img_tag:
            errores.append("%s -> img sin alt: %s" % (nombre, img_tag[:70]))

# ---------- 4. peso total ----------
peso_img = sum(os.path.getsize(os.path.join(RAIZ, "assets", "img", f))
               for f in os.listdir(os.path.join(RAIZ, "assets", "img")))
peso_css = os.path.getsize(os.path.join(RAIZ, "assets", "css", "styles.css"))
peso_js = sum(os.path.getsize(os.path.join(RAIZ, "assets", "js", f))
              for f in os.listdir(os.path.join(RAIZ, "assets", "js")))

print("páginas: %d | platos: %d | categorías: %d | locales: %d"
      % (len(html_files), platos, len(datos["categorias"]), len(datos["locales"])))
print("assets: img=%.2f MB  css=%.1f KB  js=%.1f KB"
      % (peso_img / 1048576, peso_css / 1024, peso_js / 1024))
hero = os.path.join(RAIZ, "assets", "img", "hero-cebiche.webp")
print("hero: %.0f KB" % (os.path.getsize(hero) / 1024))
print()
if errores:
    print("ERRORES (%d):" % len(errores))
    for e in errores:
        print("  -", e)
else:
    print("Sin errores de recursos, enlaces ni SEO básico.")
if avisos:
    print("\nAVISOS (%d):" % len(avisos))
    for a in avisos[:12]:
        print("  -", a)
sys.exit(1 if errores else 0)
