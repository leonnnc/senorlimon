# -*- coding: utf-8 -*-
"""Genera una vista previa con el nombre de cada bebida y su foto asignada"""
import os
from PIL import Image, ImageDraw, ImageFont

RAIZ = r"C:\Users\leonn\Documents\web\senorlimon"
IMG = os.path.join(RAIZ, "assets", "img")
SALIDA = os.path.join(RAIZ, "vista-previa-bebidas.png")

BEBIDAS = [
    ("CORONA", "S/ 14", "bebida-botella-limon.webp"),
    ("CUSQUEÑA DORADA", "S/ 12", "bebida-lager-vaso.webp"),
    ("CUSQUEÑA TRIGO", "S/ 12", "bebida-trigo-naranja.webp"),
    ("STELLA ARTOIS", "S/ 14", "bebida-botella-verde.webp"),
    ("MICHELOB ULTRA", "S/ 14", "bebida-botella-ambar.webp"),
    ("PILSEN CALLAO", "S/ 12", "bebida-pilsner-vaso.webp"),
    ("BUDWEISER", "S/ 14", "bebida-botellas-hielo.webp"),
    ("CUSQUEÑA NEGRA", "S/ 12", "bebida-negra.webp"),
    ("INCA KOLA / COCA COLA ZERO", "S/ 8", "bebida-gaseosa-hielo.webp"),
    ("AGUA EMBOTELLADA", "S/ 8", "bebida-agua.webp"),
]

LADO, COLS, MARGEN, PIE = 300, 5, 20, 52
FILAS = 2
ANCHO = COLS * LADO + (COLS + 1) * MARGEN
ALTO = FILAS * (LADO + PIE) + (FILAS + 1) * MARGEN + 60

fuente = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 17)
fuente_titulo = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 26)

lienzo = Image.new("RGB", (ANCHO, ALTO), (14, 58, 76))
dibujo = ImageDraw.Draw(lienzo)
dibujo.text((MARGEN, 20), "Bebidas — nuevas fotos de la carta", fill=(255, 255, 255), font=fuente_titulo)

for i, (nombre, precio, archivo) in enumerate(BEBIDAS):
    ruta = os.path.join(IMG, archivo)
    if not os.path.exists(ruta):
        print("falta:", archivo)
        continue
    im = Image.open(ruta).convert("RGB").resize((LADO, LADO), Image.LANCZOS)
    x = MARGEN + (i % COLS) * (LADO + MARGEN)
    y = 60 + MARGEN + (i // COLS) * (LADO + PIE + MARGEN)
    lienzo.paste(im, (x, y))
    texto = nombre
    if dibujo.textlength(texto, font=fuente) > LADO:
        while dibujo.textlength(texto + "…", font=fuente) > LADO and len(texto) > 4:
            texto = texto[:-1]
        texto += "…"
    dibujo.text((x, y + LADO + 8), texto, fill=(255, 255, 255), font=fuente)
    dibujo.text((x, y + LADO + 27), precio, fill=(150, 206, 68), font=fuente)

lienzo.save(SALIDA, "PNG")
print("vista previa:", SALIDA, round(os.path.getsize(SALIDA) / 1024, 1), "KB")
