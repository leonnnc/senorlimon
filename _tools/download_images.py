# -*- coding: utf-8 -*-
"""Descarga las imagenes reales del sitio actual (platos, portada, tiles, logos)"""
import json, os, re, urllib.request, urllib.error, ssl, sys

REVIEW = r"C:\Users\leonn\Documents\web\senorlimon\_review"
RAW = r"C:\Users\leonn\Documents\web\senorlimon\_raw\img"
os.makedirs(RAW, exist_ok=True)

CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36"}

FIXED = {
    "logo": "https://senorlimon.com/wp-content/uploads/2020/10/logo2.png",
    "logo-footer": "https://senorlimon.com/wp-content/uploads/2020/10/logo-3.png",
    "tarjetas": "https://senorlimon.com/wp-content/uploads/2020/10/tarjetas-300x44.png",
    "hero-portada": "https://senorlimon.com/wp-content/uploads/2025/03/oficial-portada.png",
    "hero-alt": "https://senorlimon.com/wp-content/uploads/2024/08/opcion-3.png",
    "hero-comida": "https://senorlimon.com/wp-content/uploads/2022/11/TODOOOO.jpg",
    "tile-carta": "https://senorlimon.com/wp-content/uploads/2022/09/nuestra-carta.jpg",
    "tile-promociones": "https://senorlimon.com/wp-content/uploads/2022/08/promociones.jpg",
    "tile-piqueos": "https://senorlimon.com/wp-content/uploads/2022/08/PIQUEOSS.jpg",
    "tile-cebiches": "https://senorlimon.com/wp-content/uploads/2022/08/CEBICHE.jpg",
    "tile-especialidades": "https://senorlimon.com/wp-content/uploads/2022/08/ESPECIALIDADES.jpg",
    "tile-risottos": "https://senorlimon.com/wp-content/uploads/2022/08/RISOTTOSS.jpg",
    "tile-pescados": "https://senorlimon.com/wp-content/uploads/2022/08/PESCADOS-ENTEROS.jpg",
    "tile-makis": "https://senorlimon.com/wp-content/uploads/2022/08/MAKISS.jpg",
    "tile-sopas": "https://senorlimon.com/wp-content/uploads/2022/08/SOPASS.jpg",
}


def slugify(url):
    name = url.split("/")[-1]
    name = re.sub(r"-\d+x\d+(?=\.)", "", name)
    name = re.sub(r"\.(jpe?g|png|webp)$", "", name, flags=re.I)
    name = re.sub(r"[^A-Za-z0-9]+", "-", name).strip("-").lower()
    return name or "img"


def fetch(url, dest):
    if os.path.exists(dest) and os.path.getsize(dest) > 0:
        return "skip"
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=30, context=CTX) as r:
            data = r.read()
        if len(data) < 200:
            return "too-small"
        with open(dest, "wb") as fh:
            fh.write(data)
        return "ok:%d" % len(data)
    except Exception as e:
        return "err:%s" % e
    return "err"


manifest = {}

# --- imagenes fijas ---
for key, url in FIXED.items():
    ext = os.path.splitext(url.split("/")[-1])[1].lower()
    dest = os.path.join(RAW, key + ext)
    res = fetch(url, dest)
    manifest[key] = {"url": url, "file": os.path.basename(dest), "res": res}
    print("%-22s %s" % (key, res))

# --- imagenes de platos ---
menu = json.load(open(os.path.join(REVIEW, "menu.json"), encoding="utf-8"))
seen = {}
for slug, page in menu.items():
    for sub in page["subsections"]:
        for it in sub["items"]:
            src = it.get("img")
            if not src:
                continue
            if "logo" in src.lower():
                continue
            full = re.sub(r"-\d+x\d+(?=\.(?:jpe?g|png))", "", src)
            base = slugify(full)
            if base in seen:
                it["img_key"] = seen[base]
                continue
            ext = os.path.splitext(full.split("/")[-1])[1].lower()
            dest = os.path.join(RAW, "plato-" + base + ext)
            res = fetch(full, dest)
            if res.startswith("err") or res == "too-small":
                dest = os.path.join(RAW, "plato-" + base + os.path.splitext(src.split("/")[-1])[1].lower())
                res = fetch(src, dest)
                full = src
            seen[base] = "plato-" + base
            it["img_key"] = "plato-" + base
            manifest["plato-" + base] = {"url": full, "file": os.path.basename(dest), "res": res}
            print("%-22s %s" % ("plato-" + base, res))

json.dump(menu, open(os.path.join(REVIEW, "menu.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
json.dump(manifest, open(os.path.join(REVIEW, "images.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("total descargadas:", len(manifest))
