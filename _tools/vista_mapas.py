# -*- coding: utf-8 -*-
"""Montaje para revisar los 8 mapas generados"""
import os
from PIL import Image, ImageDraw, ImageFont

RAIZ = r"C:\Users\leonn\Documents\web\senorlimon"
IMG = os.path.join(RAIZ, "assets", "img")
SALIDA = os.path.join(RAIZ, "_raw", "montaje-mapas.png")

MAPAS = [
    ("La Molina · Av. Javier Prado Este 5335", "mapa-javier-prado.webp"),
    ("La Molina · Av. Constructores 958", "mapa-constructores.webp"),
    ("San Isidro · Av. Guillermo Prescott 415", "mapa-prescott-415.webp"),
    ("San Isidro · Av. Guillermo Prescott 370", "mapa-prescott-370.webp"),
    ("San Isidro · Av. Conquistadores 299", "mapa-conquistadores.webp"),
    ("San Miguel · Av. Universitaria 722", "mapa-universitaria.webp"),
    ("San Miguel · Av. La Mar 2311", "mapa-la-mar.webp"),
    ("Cercado de Lima · Av. Naciones Unidas 1160", "mapa-naciones-unidas.webp"),
]

ANCHO, ALTO = 440, 220
COLS, MARGEN, PIE = 2, 16, 30
FILAS = 4
lienzo = Image.new("RGB", (COLS * (ANCHO + MARGEN) + MARGEN,
                           FILAS * (ALTO + PIE + MARGEN) + MARGEN + 44), (14, 58, 76))
d = ImageDraw.Draw(lienzo)
titulo = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 22)
fuente = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 15)
d.text((MARGEN, 14), "Mapas por local (OpenStreetMap) — los pines caen en la avenida correcta", fill=(255, 255, 255), font=titulo)

for i, (etiqueta, archivo) in enumerate(MAPAS):
    ruta = os.path.join(IMG, archivo)
    if not os.path.exists(ruta):
        print("falta:", archivo)
        continue
    im = Image.open(ruta).convert("RGB").resize((ANCHO, ALTO), Image.LANCZOS)
    x = MARGEN + (i % COLS) * (ANCHO + MARGEN)
    y = 44 + MARGEN + (i // COLS) * (ALTO + PIE + MARGEN)
    lienzo.paste(im, (x, y))
    d.text((x, y + ALTO + 7), etiqueta, fill=(180, 215, 190), font=fuente)

lienzo.save(SALIDA, "PNG")
print("montaje:", SALIDA, round(os.path.getsize(SALIDA) / 1024, 1), "KB")
