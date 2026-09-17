# -*- coding: utf-8 -*-
"""Lista los platos sin foto y propone candidatos de la biblioteca de medios del sitio"""
import io, json, os, re, unicodedata

RAIZ = r"C:\Users\leonn\Documents\web\senorlimon"
REVIEW = os.path.join(RAIZ, "_review")

datos = json.loads(io.open(os.path.join(RAIZ, "assets", "js", "data.js"), encoding="utf-8")
                   .read().split("=", 1)[1].rsplit(";", 1)[0])

sin_foto = []
for cat in datos["categorias"]:
    for sub in cat["subs"]:
        for it in sub["items"]:
            if not it.get("img"):
                sin_foto.append((cat["id"], sub["nombre"], it["nombre"], it.get("precio")))

print("=== PLATOS SIN FOTO: %d de %d ===" % (
    len(sin_foto), sum(len(s["items"]) for c in datos["categorias"] for s in c["subs"])))
for cid, sub, nombre, precio in sin_foto:
    print("  [%-20s] %-52s %s" % (cid, nombre, precio))


def normal(t):
    t = unicodedata.normalize("NFKD", t or "")
    t = "".join(c for c in t if not unicodedata.combining(c)).lower()
    return re.sub(r"[^a-z0-9 ]+", " ", t)


PALABRAS_VACIAS = {"de", "del", "la", "el", "los", "las", "con", "a", "al", "y", "o", "en",
                   "senor", "limon", "restaurante", "scaled", "copia", "mesa", "trabajo", "jpg", "png"}

medios = []
for n in (1, 2, 3):
    ruta = os.path.join(REVIEW, "media-all-%d.json" % n)
    if os.path.exists(ruta):
        medios.extend(json.load(io.open(ruta, encoding="utf-8")))

archivos = []
for m in medios:
    url = m.get("source_url") or ""
    nombre = url.split("/")[-1]
    base = re.sub(r"-\d+x\d+(?=\.)", "", nombre)
    base = re.sub(r"\.(jpe?g|png|webp)$", "", base, flags=re.I)
    palabras = {p for p in normal(base).split() if p and p not in PALABRAS_VACIAS and len(p) > 2}
    archivos.append((url, nombre, palabras))

print("\n=== CANDIDATOS POR PLATO ===")
for cid, sub, nombre, precio in sin_foto:
    clave = {p for p in normal(nombre).split() if p and p not in PALABRAS_VACIAS and len(p) > 2}
    puntuados = []
    for url, archivo, palabras in archivos:
        if not palabras or not clave:
            continue
        comunes = clave & palabras
        if comunes:
            puntuados.append((len(comunes) / len(clave), len(comunes), archivo, url))
    puntuados.sort(reverse=True)
    print("\n  %s" % nombre)
    if not puntuados:
        print("      (sin candidatos)")
    for score, comunes, archivo, url in puntuados[:4]:
        print("      %.2f  %-46s %s" % (score, archivo[:46], url))
