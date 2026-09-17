# -*- coding: utf-8 -*-
"""Busca en la biblioteca de medios del sitio original imágenes de bebidas"""
import io, json, os, re, unicodedata

REVIEW = r"C:\Users\leonn\Documents\web\senorlimon\_review"
CLAVES = ["cervez", "gaseos", "bebida", "botella", "vaso", "inka", "coca", "agua", "limonada",
          "chicha", "cristal", "cusquen", "corona", "pilsen", "stella", "michelob", "budweiser",
          "soda", "jugo", "refresco", "pisco", "coctel", "trago", "vino", "chicha", "sprite",
          "fanta", "sanche", "bebidas"]

items = []
for n in (1, 2, 3):
    ruta = os.path.join(REVIEW, "media-all-%d.json" % n)
    if os.path.exists(ruta):
        try:
            items.extend(json.load(io.open(ruta, encoding="utf-8")))
        except Exception as e:
            print("error leyendo %s: %s" % (ruta, e))


def normal(t):
    t = unicodedata.normalize("NFKD", t or "")
    return "".join(c for c in t if not unicodedata.combining(c)).lower()


print("medios totales: %d" % len(items))
print("\n=== coincidencias con bebidas ===")
vistos = set()
for it in items:
    titulo = (it.get("title") or {}).get("rendered") or ""
    url = it.get("source_url") or ""
    clave = normal(titulo + " " + url.split("/")[-1])
    if any(k in clave for k in CLAVES):
        if url in vistos:
            continue
        vistos.add(url)
        print("  %-46s %s" % (titulo[:46], url.split("/")[-1]))

print("\n=== todos los títulos de la biblioteca (para revisar a ojo) ===")
for it in sorted(items, key=lambda x: ((x.get("title") or {}).get("rendered") or "")):
    titulo = (it.get("title") or {}).get("rendered") or ""
    url = it.get("source_url") or ""
    print("  %-52s %s" % (titulo[:52], url.split("/")[-1][:60]))
