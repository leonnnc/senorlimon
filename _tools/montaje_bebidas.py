# -*- coding: utf-8 -*-
"""Monta las 10 bebidas generadas en una rejilla numerada para revisarlas de un vistazo"""
import os
from PIL import Image, ImageDraw

RAIZ = r"C:\Users\leonn\Documents\web\senorlimon"
SALIDA = os.path.join(RAIZ, "media-output", "montaje-bebidas.png")

ARCHIVOS = [
    "img-mu4oce5u-0e8c2977.png",  # 1
    "img-mu4ocfhl-8739902e.png",  # 2
    "img-mu4oc99l-aeb4feef.png",  # 3
    "img-mu4ocbiu-843c9c3b.png",  # 4
    "img-mu4ocbnp-eb284adb.png",  # 5
    "img-mu4odroq-91bff2cf.png",  # 6
    "img-mu4odalr-20a7bd11.png",  # 7
    "img-mu4odfhz-0dff3d04.png",  # 8
    "img-mu4odoki-8d2fa70d.png",  # 9
    "img-mu4odplv-983a9312.png",  # 10
]

LADO = 320
COLS = 5
FILAS = 2
MARGEN = 26

lienzo = Image.new("RGB", (COLS * LADO, FILAS * (LADO + MARGEN)), (18, 40, 52))
dibujo = ImageDraw.Draw(lienzo)

for i, nombre in enumerate(ARCHIVOS):
    ruta = os.path.join(RAIZ, "media-output", nombre)
    if not os.path.exists(ruta):
        print("falta:", nombre)
        continue
    im = Image.open(ruta).convert("RGB")
    im = im.resize((LADO, LADO), Image.LANCZOS)
    x = (i % COLS) * LADO
    y = (i // COLS) * (LADO + MARGEN) + MARGEN
    lienzo.paste(im, (x, y))
    dibujo.text((x + 8, y - MARGEN + 4), "N.%d" % (i + 1), fill=(255, 255, 255))

lienzo.save(SALIDA, "PNG")
print("montaje:", SALIDA, round(os.path.getsize(SALIDA) / 1024, 1), "KB")
