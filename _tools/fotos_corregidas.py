# -*- coding: utf-8 -*-
"""Descarga fotos reales que estaban sin usar para quitar duplicados de la carta"""
import os, ssl, urllib.request, io
from PIL import Image

RAIZ = r"C:\Users\leonn\Documents\web\senorlimon"
DESTINO = os.path.join(RAIZ, "assets", "img")
TMP = os.path.join(RAIZ, "_raw", "faltantes")
os.makedirs(TMP, exist_ok=True)

CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36"}
BASE = "https://senorlimon.com/wp-content/uploads/"

MAPA = [
    ("2026/04/Festival-de-causa.jpg", "plato-festival-de-causa.webp", "FESTIVAL DE CAUSA"),
    ("2024/11/Jalea-Mixta.jpg", "plato-jalea-mixta.webp", "JALEA MIXTA"),
    ("2024/12/Sudado-de-Cabrilla-PARA-LLEVAR.jpg", "plato-sudado-de-cabrilla.webp", "SUDADO DE CABRILLA"),
]

for ruta, final, plato in MAPA:
    crudo = os.path.join(TMP, os.path.basename(ruta))
    try:
        if not os.path.exists(crudo):
            req = urllib.request.Request(BASE + ruta, headers=UA)
            with urllib.request.urlopen(req, timeout=40, context=CTX) as r:
                with open(crudo, "wb") as fh:
                    fh.write(r.read())
        im = Image.open(crudo).convert("RGB")
        if im.width > 900:
            im = im.resize((900, round(im.height * 900 / im.width)), Image.LANCZOS)
        salida = os.path.join(DESTINO, final)
        im.save(salida, "WEBP", quality=78, method=6)
        print("%-42s %-28s %6.0fK" % (final, plato, os.path.getsize(salida) / 1024))
    except Exception as e:
        print("ERROR %s: %s" % (final, e))
