# -*- coding: utf-8 -*-
"""Versión grande de cada mapa (más zoom) para mostrarla en el modal"""
import io, math, os, ssl, time, urllib.request
from PIL import Image, ImageDraw, ImageFont

RAIZ = r"C:\Users\leonn\Documents\web\senorlimon"
DESTINO = os.path.join(RAIZ, "assets", "img")
CACHE = os.path.join(RAIZ, "_raw", "tiles")
os.makedirs(CACHE, exist_ok=True)

CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE
UA = {"User-Agent": "senorlimon-web-redesign/1.0 (contacto: leonnc@gmail.com)"}

ZOOM = 17
ANCHO, ALTO = 1400, 800
ATRIBUCION = "© OpenStreetMap"

LOCALES = [
    ("javier-prado", -12.072315, -76.958133),
    ("constructores", -12.065462, -76.953904),
    ("prescott-415", -12.087375, -77.048284),
    ("prescott-370", -12.085360, -77.048624),
    ("conquistadores", -12.098985, -77.036149),
    ("universitaria", -12.081208, -77.082256),
    ("la-mar", -12.074100, -77.086134),
    ("naciones-unidas", -12.050960, -77.060405),
]


def a_mosaico(lat, lon, z):
    n = 2 ** z
    x = (lon + 180.0) / 360.0 * n
    lat_r = math.radians(lat)
    y = (1.0 - math.log(math.tan(lat_r) + 1.0 / math.cos(lat_r)) / math.pi) / 2.0 * n
    return x, y


def traer_mosaico(z, x, y):
    ruta = os.path.join(CACHE, "%d_%d_%d.png" % (z, x, y))
    if os.path.exists(ruta):
        return Image.open(ruta).convert("RGB")
    url = "https://tile.openstreetmap.org/%d/%d/%d.png" % (z, x, y)
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=45, context=CTX) as r:
        datos = r.read()
    with open(ruta, "wb") as fh:
        fh.write(datos)
    time.sleep(0.3)
    return Image.open(io.BytesIO(datos)).convert("RGB")


def dibujar_pin(mapa, cx, cy):
    capa = Image.new("RGBA", mapa.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(capa)
    d.ellipse([cx - 19, cy - 30, cx + 19, cy + 12], fill=(0, 0, 0, 55))
    d.polygon([(cx - 12, cy - 9), (cx + 12, cy - 9), (cx, cy + 24)], fill=(221, 83, 65, 255))
    d.ellipse([cx - 22, cy - 45, cx + 22, cy], fill=(221, 83, 65, 255))
    d.polygon([(cx - 12, cy - 9), (cx + 12, cy - 9), (cx, cy + 24)], outline=(255, 255, 255, 255))
    d.ellipse([cx - 22, cy - 45, cx + 22, cy], outline=(255, 255, 255, 255), width=4)
    d.ellipse([cx - 7, cy - 30, cx + 7, cy - 16], fill=(255, 255, 255, 255))
    return Image.alpha_composite(mapa.convert("RGBA"), capa).convert("RGB")


for nombre, lat, lon in LOCALES:
    xf, yf = a_mosaico(lat, lon, ZOOM)
    px, py = xf * 256.0, yf * 256.0
    izq, arriba = int(px - ANCHO / 2), int(py - ALTO / 2)

    lienzo = Image.new("RGB", (ANCHO, ALTO), (232, 234, 226))
    for tx in range(izq // 256, (izq + ANCHO) // 256 + 1):
        for ty in range(arriba // 256, (arriba + ALTO) // 256 + 1):
            try:
                lienzo.paste(traer_mosaico(ZOOM, tx, ty), (tx * 256 - izq, ty * 256 - arriba))
            except Exception as e:
                print("   mosaico %d/%d/%d falló: %s" % (ZOOM, tx, ty, e))

    lienzo = dibujar_pin(lienzo, int(px - izq), int(py - arriba))

    d = ImageDraw.Draw(lienzo, "RGBA")
    try:
        fuente = ImageFont.truetype(r"C:\Windows\Fonts\arial.ttf", 16)
    except Exception:
        fuente = ImageFont.load_default()
    ancho_texto = d.textlength(ATRIBUCION, font=fuente)
    d.rectangle([ANCHO - ancho_texto - 18, ALTO - 30, ANCHO, ALTO], fill=(255, 255, 255, 205))
    d.text((ANCHO - ancho_texto - 9, ALTO - 25), ATRIBUCION, fill=(60, 60, 60), font=fuente)

    salida = os.path.join(DESTINO, "mapa-%s-grande.webp" % nombre)
    lienzo.save(salida, "WEBP", quality=80, method=6)
    print("%-34s %5.0f KB" % ("mapa-%s-grande.webp" % nombre, os.path.getsize(salida) / 1024))
