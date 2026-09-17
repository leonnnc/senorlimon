# -*- coding: utf-8 -*-
"""Busca en la biblioteca de medios del sitio fotos que empiecen por ciertas palabras"""
import io, json, os, re, sys, unicodedata

REVIEW = r"C:\Users\leonn\Documents\web\senorlimon\_review"
CLAVES = ["tiradito", "lenguado", "charela", "milanesa", "pulpo", "seco", "macho", "tacu",
          "cabrilla", "festival", "chita", "sudado", "leche", "risotto", "rissotto", "lomo",
          "aji", "aji-amarillo", "camaron", "chupe", "parihuela", "chicharron", "jalea",
          "causa", "parmesana", "acevichado", "california", "furai", "arroz", "chaufa",
          "fetuccini", "pesto", "trucha", "pescado", "combinado", "conchas"]


def normal(t):
    t = unicodedata.normalize("NFKD", t or "")
    return "".join(c for c in t if not unicodedata.combining(c)).lower()


medios = []
for n in (1, 2, 3):
    ruta = os.path.join(REVIEW, "media-all-%d.json" % n)
    if os.path.exists(ruta):
        medios.extend(json.load(io.open(ruta, encoding="utf-8")))

vistos = set()
for clave in CLAVES:
    print("\n=== %s ===" % clave)
    encontrados = 0
    for m in medios:
        url = m.get("source_url") or ""
        archivo = url.split("/")[-1]
        if clave in normal(archivo) and url not in vistos:
            if re.search(r"-\d+x\d+\.", archivo):
                continue
            vistos.add(url)
            encontrados += 1
            print("   %-56s %s" % (archivo[:56], url))
    if not encontrados:
        print("   (ninguna)")
