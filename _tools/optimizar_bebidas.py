# -*- coding: utf-8 -*-
"""Convierte las bebidas generadas a WebP con el mismo tamaño que el resto de la carta"""
import os
from PIL import Image

RAIZ = r"C:\Users\leonn\Documents\web\senorlimon"
ORIGEN = os.path.join(RAIZ, "media-output")
DESTINO = os.path.join(RAIZ, "assets", "img")
os.makedirs(DESTINO, exist_ok=True)

# imagen generada -> nombre final en el sitio (nombres por tipo de bebida, no por marca)
MAPA = [
    ("img-mu4oce5u-0e8c2977.png", "bebida-lager-vaso.webp"),        # cerveza rubia en vaso
    ("img-mu4ocfhl-8739902e.png", "bebida-trigo-naranja.webp"),     # cerveza de trigo con naranja
    ("img-mu4oc99l-aeb4feef.png", "bebida-negra.webp"),             # cerveza negra
    ("img-mu4ocbiu-843c9c3b.png", "bebida-botella-ambar.webp"),     # botella ámbar fría
    ("img-mu4ocbnp-eb284adb.png", "bebida-botella-limon.webp"),     # botella clara con limón
    ("img-mu4odroq-91bff2cf.png", "bebida-botella-verde.webp"),     # botella verde con vaso
    ("img-mu4odalr-20a7bd11.png", "bebida-pilsner-vaso.webp"),      # vaso de pilsner
    ("img-mu4odfhz-0dff3d04.png", "bebida-botellas-hielo.webp"),    # botellas en hielera
    ("img-mu4odoki-8d2fa70d.png", "bebida-gaseosa-hielo.webp"),     # gaseosa con hielo
    ("img-mu4odplv-983a9312.png", "bebida-agua.webp"),              # agua embotellada
]

total_antes = total_despues = 0
print("%-32s %10s %10s" % ("archivo", "antes", "después"))
for origen, final in MAPA:
    ruta = os.path.join(ORIGEN, origen)
    if not os.path.exists(ruta):
        print("FALTA:", origen)
        continue
    im = Image.open(ruta).convert("RGB")
    if im.width > 900:
        alto = round(im.height * 900 / im.width)
        im = im.resize((900, alto), Image.LANCZOS)
    salida = os.path.join(DESTINO, final)
    im.save(salida, "WEBP", quality=78, method=6)
    a, b = os.path.getsize(ruta), os.path.getsize(salida)
    total_antes += a
    total_despues += b
    print("%-32s %9.0fK %9.0fK" % (final, a / 1024, b / 1024))

print("-" * 56)
print("total: %.2f MB -> %.2f MB" % (total_antes / 1048576, total_despues / 1048576))
