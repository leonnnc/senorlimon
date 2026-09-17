# -*- coding: utf-8 -*-
"""Lista los platos de ciertas categorías con su foto actual"""
import io, json, os, sys

RAIZ = r"C:\Users\leonn\Documents\web\senorlimon"
CATS = sys.argv[1].split(",") if len(sys.argv) > 1 else None

datos = json.loads(io.open(os.path.join(RAIZ, "assets", "js", "data.js"), encoding="utf-8")
                   .read().split("=", 1)[1].rsplit(";", 1)[0])

for cat in datos["categorias"]:
    if CATS and cat["id"] not in CATS:
        continue
    print("== %s" % cat["nombre"])
    for sub in cat["subs"]:
        for it in sub["items"]:
            print("   %-48s %s" % (it["nombre"][:48], it.get("img") or "SIN FOTO"))
