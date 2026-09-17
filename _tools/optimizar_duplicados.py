# -*- coding: utf-8 -*-
"""Reemplaza las fotos que estaban repetidas por imágenes propias de cada plato"""
import os
from PIL import Image

RAIZ = r"C:\Users\leonn\Documents\web\senorlimon"
ORIGEN = os.path.join(RAIZ, "media-output")
DESTINO = os.path.join(RAIZ, "assets", "img")

MAPA = [
    ("img-mu4pf9yg-e97e66e9.png", "plato-chicharron-mixto.webp", "CHICHARRÓN MIXTO (nueva)"),
    ("img-mu4pf6x4-b2ecfc7a.png", "plato-cebiche-mixto-de-charela.webp", "CEBICHE MIXTO DE CHARELA (reemplaza la copia)"),
    ("img-mu4pfb06-0a87ee19.png", "plato-risotto-a-la-huancaina-con-lomo-saltado.webp", "RISOTTO A LA HUANCAÍNA CON LOMO SALTADO (reemplaza la copia)"),
]

for origen, final, nota in MAPA:
    ruta = os.path.join(ORIGEN, origen)
    if not os.path.exists(ruta):
        print("FALTA:", origen)
        continue
    im = Image.open(ruta).convert("RGB")
    if im.width > 900:
        im = im.resize((900, round(im.height * 900 / im.width)), Image.LANCZOS)
    salida = os.path.join(DESTINO, final)
    im.save(salida, "WEBP", quality=78, method=6)
    print("%-52s %6.0fK  %s" % (final, os.path.getsize(salida) / 1024, nota))
