# -*- coding: utf-8 -*-
"""Vista previa etiquetada de las fotos nuevas de la carta"""
import os
from PIL import Image, ImageDraw, ImageFont

RAIZ = r"C:\Users\leonn\Documents\web\senorlimon"
IMG = os.path.join(RAIZ, "assets", "img")
SALIDA = os.path.join(RAIZ, "vista-previa-platos.png")

FOTOS = [
    ("Cebiche de conchas negras", "plato-cebiche-de-conchas-negras-2.webp"),
    ("Cebiche de lenguado", "plato-cebiche-de-lenguado.webp"),
    ("Cebiche mixto de lenguado", "plato-cebiche-mixto-de-lenguado.webp"),
    ("Cebiche de charela", "plato-cebiche-de-charela.webp"),
    ("Cebiche mixto de charela", "plato-cebiche-mixto-de-charela.webp"),
    ("Combinación clásica", "plato-combinacion-clasica.webp"),
    ("Tiradito al ají amarillo", "plato-tiradito-al-aji-amarillo.webp"),
    ("Leche de tigre tradicional", "plato-leche-de-tigre-tradicional.webp"),
    ("Leche de tigre Señor Limón", "plato-leche-de-tigre-senor-limon.webp"),
    ("Leche de tigre criollo", "plato-leche-de-tigre-criollo.webp"),
    ("Leche de tigre norteño", "plato-leche-de-tigre-norteno.webp"),
    ("Cabrilla oriental", "plato-cabrilla-oriental.webp"),
    ("Seco de asado de tira", "plato-seco-de-asado-de-tira.webp"),
    ("Festival de sudado", "plato-festival-de-sudado.webp"),
    ("Tacu tacu con lomo a lo pobre", "plato-tacu-tacu-con-lomo-a-lo-pobre.webp"),
    ("Chupe de camarones", "plato-chupe-de-camarones.webp"),
    ("Sudado de pescado", "plato-sudado-de-pescado.webp"),
    ("Sudado de chita", "plato-sudado-de-chita.webp"),
    ("Chita al ajo crocante", "plato-chita-al-ajo-crocante.webp"),
    ("Trucha a la parrilla", "plato-trucha-a-la-parrilla.webp"),
    ("Risotto a la huancaína con lomo", "plato-risotto-a-la-huancaina-con-lomo-saltado.webp"),
    ("Tacu tacu a lo macho", "plato-tacu-tacu-a-lo-macho.webp"),
    ("Tacu tacu con lomo saltado", "plato-tacu-tacu-con-lomo-saltado.webp"),
    ("Filete de trucha al ajo", "plato-filete-de-trucha-al-ajo-con-langostinos.webp"),
    ("Charela a la plancha", "plato-charela-a-la-plancha.webp"),
    ("Lomo saltado criollo", "plato-lomo-saltado-criollo.webp"),
    ("Milanesa de pescado", "plato-milanesa-de-pescado.webp"),
    ("Pescado en salsa cuatro quesos", "plato-pescado-en-salsa-cuatro-quesos.webp"),
    ("Pescado en salsa de champiñones", "plato-pescado-en-salsa-de-champinones.webp"),
    ("Pulpo a la parrilla", "plato-pulpo-a-la-parrilla.webp"),
    ("Parrilla marina", "plato-parrilla-marina.webp"),
]

LADO, COLS, MARGEN, PIE = 250, 6, 16, 46
FILAS = (len(FOTOS) + COLS - 1) // COLS
ANCHO = COLS * LADO + (COLS + 1) * MARGEN
ALTO = FILAS * (LADO + PIE) + (FILAS + 1) * MARGEN + 56

fuente = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 14)
titulo = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 24)

lienzo = Image.new("RGB", (ANCHO, ALTO), (14, 58, 76))
dibujo = ImageDraw.Draw(lienzo)
dibujo.text((MARGEN, 18), "Carta — 31 platos que antes no tenían foto", fill=(255, 255, 255), font=titulo)

for i, (etiqueta, archivo) in enumerate(FOTOS):
    ruta = os.path.join(IMG, archivo)
    if not os.path.exists(ruta):
        print("falta:", archivo)
        continue
    im = Image.open(ruta).convert("RGB").resize((LADO, LADO), Image.LANCZOS)
    x = MARGEN + (i % COLS) * (LADO + MARGEN)
    y = 56 + MARGEN + (i // COLS) * (LADO + PIE + MARGEN)
    lienzo.paste(im, (x, y))
    texto = etiqueta
    if dibujo.textlength(texto, font=fuente) > LADO:
        while dibujo.textlength(texto + "…", font=fuente) > LADO and len(texto) > 5:
            texto = texto[:-1]
        texto += "…"
    dibujo.text((x, y + LADO + 7), texto, fill=(230, 240, 235), font=fuente)

lienzo.save(SALIDA, "PNG")
print("vista previa:", SALIDA, round(os.path.getsize(SALIDA) / 1024, 1), "KB", "| celdas:", len(FOTOS))
