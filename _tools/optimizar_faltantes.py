# -*- coding: utf-8 -*-
"""Convierte a WebP las 16 imágenes generadas para los platos que no tenían foto"""
import os, json, io
from PIL import Image

RAIZ = r"C:\Users\leonn\Documents\web\senorlimon"
ORIGEN = os.path.join(RAIZ, "media-output")
DESTINO = os.path.join(RAIZ, "assets", "img")

MAPA = [
    ("img-mu4or1t9-db6e4161.png", "plato-cebiche-de-lenguado.webp", "CEBICHE DE LENGUADO"),
    ("img-mu4ornn4-ed149b6f.png", "plato-cebiche-de-charela.webp", "CEBICHE DE CHARELA"),
    ("img-mu4orlud-9a2609f9.png", "plato-tiradito-al-aji-amarillo.webp", "TIRADITO AL AJÍ AMARILLO (PESCA DEL DÍA)"),
    ("img-mu4or7ca-de9ae379.png", "plato-leche-de-tigre-criollo.webp", "LECHE DE TIGRE CRIOLLO"),
    ("img-mu4orito-68c1dfad.png", "plato-leche-de-tigre-norteno.webp", "LECHE DE TIGRE NORTEÑO"),
    ("img-mu4ot1o3-d581a51e.png", "plato-cabrilla-oriental.webp", "CABRILLA ORIENTAL"),
    ("img-mu4osrzd-1c3d831e.png", "plato-seco-de-asado-de-tira.webp", "SECO DE ASADO DE TIRA"),
    ("img-mu4osvxq-6c92323d.png", "plato-festival-de-sudado.webp", "FESTIVAL DE SUDADO"),
    ("img-mu4ot456-87358f69.png", "plato-sudado-de-chita.webp", "SUDADO DE CHITA"),
    ("img-mu4osre9-eea2801b.png", "plato-chita-al-ajo-crocante.webp", "CHITA AL AJO CROCANTE"),
    ("img-mu4oumo3-b5d79525.png", "plato-tacu-tacu-a-lo-macho.webp", "TACU TACU A LO MACHO"),
    ("img-mu4oue9f-ed64a390.png", "plato-tacu-tacu-con-lomo-saltado.webp", "TACU TACU CON LOMO SALTADO"),
    ("img-mu4oubry-4b9ba53a.png", "plato-charela-a-la-plancha.webp", "CHARELA A LA PLANCHA"),
    ("img-mu4oul1i-be8f46a2.png", "plato-milanesa-de-pescado.webp", "MILANESA DE PESCADO"),
    ("img-mu4ouih6-144eb532.png", "plato-pescado-en-salsa-cuatro-quesos.webp", "PESCADO EN SALSA CUATRO QUESOS"),
    ("img-mu4oujp8-4e6a967c.png", "plato-pulpo-a-la-parrilla.webp", "PULPO A LA PARRILLA"),
]

total_a = total_b = 0
asignacion = {}
print("%-48s %9s %9s" % ("archivo final", "antes", "después"))
for origen, final, plato in MAPA:
    ruta = os.path.join(ORIGEN, origen)
    if not os.path.exists(ruta):
        print("FALTA:", origen)
        continue
    im = Image.open(ruta).convert("RGB")
    if im.width > 900:
        im = im.resize((900, round(im.height * 900 / im.width)), Image.LANCZOS)
    salida = os.path.join(DESTINO, final)
    im.save(salida, "WEBP", quality=78, method=6)
    a, b = os.path.getsize(ruta), os.path.getsize(salida)
    total_a += a
    total_b += b
    asignacion[plato] = final
    print("%-48s %8.0fK %8.0fK" % (final, a / 1024, b / 1024))

print("-" * 68)
print("16 imágenes generadas: %.2f MB -> %.2f MB" % (total_a / 1048576, total_b / 1048576))
json.dump(asignacion, io.open(os.path.join(RAIZ, "_review", "fotos_generadas.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=2)
