# -*- coding: utf-8 -*-
"""Vista previa de los platos que cambiaron de foto al quitar duplicados"""
import os
from PIL import Image, ImageDraw, ImageFont

RAIZ = r"C:\Users\leonn\Documents\web\senorlimon"
IMG = os.path.join(RAIZ, "assets", "img")
SALIDA = os.path.join(RAIZ, "vista-previa-corregidas.png")

FOTOS = [
    ("Festival de causa", "plato-festival-de-causa.webp", "antes repetía la foto de Matrimonio"),
    ("Jalea mixta", "plato-jalea-mixta.webp", "antes repetía la de Chicharrón mixto"),
    ("Sudado de cabrilla", "plato-sudado-de-cabrilla.webp", "antes repetía la de Sudado de pescado"),
    ("Chicharrón mixto", "plato-chicharron-mixto.webp", "foto nueva"),
    ("Cebiche mixto de charela", "plato-cebiche-mixto-de-charela.webp", "foto nueva (era copia exacta)"),
    ("Risotto a la huancaína con lomo saltado", "plato-risotto-a-la-huancaina-con-lomo-saltado.webp", "foto nueva (era copia exacta)"),
]

LADO, COLS, MARGEN, PIE = 300, 3, 18, 62
FILAS = 2
ANCHO = COLS * LADO + (COLS + 1) * MARGEN
ALTO = FILAS * (LADO + PIE) + (FILAS + 1) * MARGEN + 54

fuente = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 15)
fuente2 = ImageFont.truetype(r"C:\Windows\Fonts\arial.ttf", 13)
titulo = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 22)

lienzo = Image.new("RGB", (ANCHO, ALTO), (14, 58, 76))
dibujo = ImageDraw.Draw(lienzo)
dibujo.text((MARGEN, 16), "Fotos corregidas: ningún plato comparte imagen", fill=(255, 255, 255), font=titulo)

for i, (etiqueta, archivo, nota) in enumerate(FOTOS):
    ruta = os.path.join(IMG, archivo)
    if not os.path.exists(ruta):
        print("falta:", archivo)
        continue
    im = Image.open(ruta).convert("RGB").resize((LADO, LADO), Image.LANCZOS)
    x = MARGEN + (i % COLS) * (LADO + MARGEN)
    y = 54 + MARGEN + (i // COLS) * (LADO + PIE + MARGEN)
    lienzo.paste(im, (x, y))
    texto = etiqueta
    if dibujo.textlength(texto, font=fuente) > LADO:
        while dibujo.textlength(texto + "…", font=fuente) > LADO and len(texto) > 5:
            texto = texto[:-1]
        texto += "…"
    dibujo.text((x, y + LADO + 8), texto, fill=(255, 255, 255), font=fuente)
    dibujo.text((x, y + LADO + 29), nota, fill=(150, 206, 68), font=fuente2)

lienzo.save(SALIDA, "PNG")
print("vista previa:", SALIDA, round(os.path.getsize(SALIDA) / 1024, 1), "KB")
