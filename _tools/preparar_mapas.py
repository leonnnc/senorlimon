# -*- coding: utf-8 -*-
"""Descarga las imágenes de locales del sitio original y arma un montaje para identificar cada una"""
import os, ssl, urllib.request
from PIL import Image, ImageDraw, ImageFont

RAIZ = r"C:\Users\leonn\Documents\web\senorlimon"
CRUDO = os.path.join(RAIZ, "_raw", "locales")
os.makedirs(CRUDO, exist_ok=True)

CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36"}
BASE = "https://senorlimon.com/wp-content/uploads/2025/03/LOCALES-%02d.png"

for n in range(1, 9):
    destino = os.path.join(CRUDO, "LOCALES-%02d.png" % n)
    if os.path.exists(destino):
        continue
    try:
        req = urllib.request.Request(BASE % n, headers=UA)
        with urllib.request.urlopen(req, timeout=60, context=CTX) as r:
            with open(destino, "wb") as fh:
                fh.write(r.read())
    except Exception as e:
        print("ERROR LOCALES-%02d: %s" % (n, e))

# montaje: cada imagen reducida a 360 px de ancho, con su número
ANCHO_CELDA = 360
ALTO_CELDA = 470
COLS = 4
FILAS = 2
MARGEN = 14
PIE = 26

fuente = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 18)
lienzo = Image.new("RGB", (COLS * (ANCHO_CELDA + MARGEN) + MARGEN,
                           FILAS * (ALTO_CELDA + PIE + MARGEN) + MARGEN), (14, 58, 76))
dibujo = ImageDraw.Draw(lienzo)

for i in range(1, 9):
    ruta = os.path.join(CRUDO, "LOCALES-%02d.png" % i)
    if not os.path.exists(ruta):
        continue
    im = Image.open(ruta).convert("RGB")
    print("LOCALES-%02d: %dx%d  %.0f KB" % (i, im.width, im.height,
                                            os.path.getsize(ruta) / 1024))
    # se reduce a lo ancho y, si no cabe de alto, se recorta por abajo
    escala = ANCHO_CELDA / im.width
    alto = round(im.height * escala)
    im = im.resize((ANCHO_CELDA, alto), Image.LANCZOS)
    if alto > ALTO_CELDA:
        im = im.crop((0, 0, ANCHO_CELDA, ALTO_CELDA))
    x = MARGEN + ((i - 1) % COLS) * (ANCHO_CELDA + MARGEN)
    y = MARGEN + ((i - 1) // COLS) * (ALTO_CELDA + PIE + MARGEN)
    lienzo.paste(im, (x, y))
    dibujo.text((x + 6, y + ALTO_CELDA + 4), "LOCALES-%02d" % i, fill=(255, 255, 255), font=fuente)

salida = os.path.join(RAIZ, "_raw", "montaje-locales.png")
lienzo.save(salida, "PNG")
print("montaje:", salida, round(os.path.getsize(salida) / 1024, 1), "KB")
