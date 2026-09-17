# -*- coding: utf-8 -*-
"""Descarga y optimiza las fotos reales de la biblioteca del sitio para los platos sin foto"""
import io, json, os, re, ssl, urllib.request
from PIL import Image

RAIZ = r"C:\Users\leonn\Documents\web\senorlimon"
DESTINO = os.path.join(RAIZ, "assets", "img")
TMP = os.path.join(RAIZ, "_raw", "faltantes")
os.makedirs(DESTINO, exist_ok=True)
os.makedirs(TMP, exist_ok=True)

CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36"}
BASE = "https://senorlimon.com/wp-content/uploads/"

# plato -> (url de la foto real, nombre de archivo final)
MAPA = {
    "CEBICHE DE CONCHAS NEGRAS": ("2024/11/Cebiche-de-Conchas-Negras.jpg", "plato-cebiche-de-conchas-negras-2.webp"),
    "CEBICHE MIXTO DE LENGUADO": ("2024/11/Cebiche-Mixto.jpg", "plato-cebiche-mixto-de-lenguado.webp"),
    "CEBICHE MIXTO DE CHARELA": ("2026/04/ceviche-mixto.png", "plato-cebiche-mixto-de-charela.webp"),
    "COMBINACIÓN CLÁSICA": ("2024/11/COMBINACION-CLASICA.jpg", "plato-combinacion-clasica.webp"),
    "LECHE DE TIGRE TRADICIONAL": ("2024/11/Leches-de-Tigre.jpg", "plato-leche-de-tigre-tradicional.webp"),
    "LECHE DE TIGRE SEÑOR LIMÓN": ("2024/11/Leches-de-Tigre-2.jpg", "plato-leche-de-tigre-senor-limon.webp"),
    "TACU TACU CON LOMO A LO POBRE": ("2026/04/tacu-tacu-con.jpg", "plato-tacu-tacu-con-lomo-a-lo-pobre.webp"),
    "CHUPE DE CAMARONES": ("2024/11/Chupe-de-Camarones.jpg", "plato-chupe-de-camarones.webp"),
    "SUDADO DE PESCADO": ("2026/04/sudado-de-pescado.jpg", "plato-sudado-de-pescado.webp"),
    "TRUCHA A LA PARRILLA": ("2026/04/trucha-a-la-parrilla.jpg", "plato-trucha-a-la-parrilla.webp"),
    "RISOTTO A LA HUANCAINA CON LOMO SALTADO": ("2026/04/lomo-con-rissotto-a-la-huancaina.jpg", "plato-risotto-a-la-huancaina-con-lomo-saltado.webp"),
    "FILETE DE TRUCHA O PESCADO AL AJO CON LANGOSTINOS": ("2026/04/trucha-con-langostinos.jpg", "plato-filete-de-trucha-al-ajo-con-langostinos.webp"),
    "LOMO SALTADO CRIOLLO": ("2026/04/LOMO-SALTADO.jpg", "plato-lomo-saltado-criollo.webp"),
    "PESCADO EN SALSA DE CHAMPIÑONES": ("2026/04/Pescado-en-salsa-de-champinones.jpg", "plato-pescado-en-salsa-de-champinones.webp"),
    "PARRILLA MARINA": ("2024/12/Parrilla-Marina.jpg", "plato-parrilla-marina.webp"),
}


def fetch(url, dest):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=40, context=CTX) as r:
        data = r.read()
    with open(dest, "wb") as fh:
        fh.write(data)
    return len(data)


print("%-46s %9s %9s" % ("archivo final", "original", "webp"))
total_a = total_b = 0
resultado = {}
for plato, (ruta, final) in MAPA.items():
    url = BASE + ruta
    crudo = os.path.join(TMP, ruta.split("/")[-1])
    try:
        if not os.path.exists(crudo):
            fetch(url, crudo)
        im = Image.open(crudo).convert("RGB")
        if im.width > 900:
            im = im.resize((900, round(im.height * 900 / im.width)), Image.LANCZOS)
        salida = os.path.join(DESTINO, final)
        im.save(salida, "WEBP", quality=78, method=6)
        a, b = os.path.getsize(crudo), os.path.getsize(salida)
        total_a += a
        total_b += b
        resultado[plato] = final
        print("%-46s %8.0fK %8.0fK" % (final, a / 1024, b / 1024))
    except Exception as e:
        print("%-46s ERROR: %s" % (final, e))

print("-" * 68)
print("%d fotos reales: %.2f MB -> %.2f MB" % (len(resultado), total_a / 1048576, total_b / 1048576))
json.dump(resultado, io.open(os.path.join(RAIZ, "_review", "fotos_reales.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=2)
