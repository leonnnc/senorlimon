# -*- coding: utf-8 -*-
"""Busca huecos de contenido: duplicados, descripciones vacías o repetidas, precios nulos
   y comprueba que los textos institucionales no perdieron contenido respecto al original"""
import io, json, os, re, unicodedata

RAIZ = r"C:\Users\leonn\Documents\web\senorlimon"
datos = json.loads(io.open(os.path.join(RAIZ, "assets", "js", "data.js"), encoding="utf-8")
                   .read().split("=", 1)[1].rsplit(";", 1)[0])


def sin_tildes(t):
    t = unicodedata.normalize("NFKD", t)
    return "".join(c for c in t if not unicodedata.combining(c)).lower()


print("=== 1. Duplicados dentro de la misma subsección ===")
dup = 0
for cat in datos["categorias"]:
    for sub in cat["subs"]:
        vistos = {}
        for it in sub["items"]:
            k = sin_tildes(it["nombre"])
            if k in vistos:
                dup += 1
                print("  %s / %s: «%s» x2" % (cat["id"], sub["nombre"], it["nombre"]))
            vistos[k] = True
print("  duplicados: %d" % dup)

print("\n=== 2. Platos sin descripción ===")
sin_desc = [it["nombre"] for cat in datos["categorias"] for sub in cat["subs"] for it in sub["items"]
            if not it["desc"]]
for n in sin_desc:
    print("  -", n)
print("  total: %d" % len(sin_desc))

print("\n=== 3. Descripciones repetidas entre platos distintos ===")
mapa = {}
for cat in datos["categorias"]:
    for sub in cat["subs"]:
        for it in sub["items"]:
            if it["desc"]:
                mapa.setdefault(sin_tildes(it["desc"]), []).append(it["nombre"])
rep = 0
for d, nombres in mapa.items():
    if len(nombres) > 1:
        rep += 1
        print("  «%s» → %s" % (d[:70], " | ".join(nombres)))
print("  descripciones repetidas: %d" % rep)

print("\n=== 4. Platos sin precio ===")
for cat in datos["categorias"]:
    for sub in cat["subs"]:
        for it in sub["items"]:
            if it["precio"] is None:
                print("  - %s (%s) variantes=%d" % (it["nombre"], cat["id"], len(it.get("variantes", []))))

print("\n=== 5. Rango de precios ===")
precios = [it["precio"] for cat in datos["categorias"] for sub in cat["subs"] for it in sub["items"]
           if it["precio"]]
print("  mínimo S/ %.2f · máximo S/ %.2f · platos con precio: %d" % (min(precios), max(precios), len(precios)))

print("\n=== 6. Textos institucionales: palabras del original conservadas ===")
def solo_palabras(t):
    """deja únicamente letras y espacios, para comparar palabra a palabra"""
    t = sin_tildes(t)
    return re.sub(r"[^a-zñ ]+", " ", t).split()


original = io.open(os.path.join(RAIZ, "_review", "blog_texts.md"), encoding="utf-8").read()
palabras_origen = [w for w in solo_palabras(original) if len(w) > 4]
texto_nuevo = " ".join(" ".join([b["titulo"]] + b["parrafos"]) for b in datos["historia"])
nuevas = set(solo_palabras(texto_nuevo))
faltan = sorted({w for w in palabras_origen if w not in nuevas})
# se descartan palabras que sólo aparecen en los enlaces del pie del archivo origen
ruido = {"instagram", "youtube", "channel", "externos", "detectados", "https", "seguir", "leyendo",
         "enlaces", "grande"}
faltan = [w for w in faltan if w not in ruido]
print("  palabras significativas del original ausentes en el sitio: %d" % len(faltan))
if faltan:
    print("  ", ", ".join(faltan[:40]))
