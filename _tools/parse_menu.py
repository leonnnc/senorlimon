# -*- coding: utf-8 -*-
"""Extrae platos, precios, descripciones y fotos de las paginas de carta de senorlimon.com"""
import json, re, os, sys
from html import unescape

REVIEW = r"C:\Users\leonn\Documents\web\senorlimon\_review"

PAGES = {
    "leche-de-tigre": "Leche de Tigre",
    "cebiches": "Cebiches y Tiraditos",
    "piqueos": "Piqueos",
    "sopas-y-sudados": "Sopas y Sudados",
    "pescados-enteros": "Pescados Enteros",
    "makis": "Makis",
    "pastas-y-risottos": "Pastas, Risottos y Arroces",
    "especialidades": "Especialidades",
    "postres-y-bebidas": "Postres y Bebidas",
    "cervezas-y-gaseosas": "Cervezas y Gaseosas",
}

PRICE_RE = re.compile(r"[sS]\s*/\s*(\d+(?:[.,]\d{2})?)")
TOKEN_RE = re.compile(r'<img\b[^>]*?src="([^"]+)"[^>]*?>|<(h[1-6]|p|li)\b[^>]*>(.*?)</\2\s*>', re.S | re.I)


def clean(t):
    t = re.sub(r"<[^>]+>", " ", t)
    t = unescape(t)
    t = t.replace("\xa0", " ").replace("\u200b", "")
    return re.sub(r"\s+", " ", t).strip()


def body_region(html):
    """Recorta desde el titulo de seccion hasta los testimonios / footer"""
    m = re.search(r'eltdf-st-title[^>]*>\s*(.*?)\s*</h1>', html, re.S)
    start = m.end() if m else 0
    end = len(html)
    for marker in ["eltdf-testimonials-holder", "eltdf-testimonial", "eltdf-footer-inner", "footer-bottom"]:
        i = html.find(marker, start)
        if i > 0:
            end = min(end, i)
    return html[start:end], (clean(m.group(1)) if m else None)


def parse_page(path):
    with open(path, encoding="utf-8") as fh:
        html = fh.read()
    region, page_title = body_region(html)
    subsections = []
    current_sub = None
    last_item = None
    for m in TOKEN_RE.finditer(region):
        if m.group(1):  # imagen
            src = m.group(1)
            ruido = ("logo", "tarjetas", "descargable", "pixel", "favicon")
            if (last_item is not None and not last_item.get("img")
                    and not any(r in src.lower() for r in ruido)):
                last_item["img"] = src
            continue
        tag = m.group(2).lower()
        text = clean(m.group(3))
        if not text:
            continue
        if tag == "h1":
            current_sub = {"name": text, "items": []}
            subsections.append(current_sub)
            last_item = None
            continue
        if tag in ("h2", "h3"):
            # titulos de seccion alternativos
            if len(text) < 60 and not PRICE_RE.search(text):
                current_sub = {"name": text, "items": []}
                subsections.append(current_sub)
                last_item = None
                continue
        if tag in ("h4", "h5", "h6"):
            pm = PRICE_RE.search(text)
            name = PRICE_RE.sub("", text).strip(" -–—.")
            item = {
                "name": name,
                "price": (float(pm.group(1).replace(",", ".")) if pm else None),
                "desc": "",
                "img": None,
                "variants": [],
            }
            if current_sub is None:
                current_sub = {"name": page_title or "", "items": []}
                subsections.append(current_sub)
            current_sub["items"].append(item)
            last_item = item
            continue
        if tag == "p":
            if last_item is None:
                continue
            if PRICE_RE.search(text) and len(text) < 220:
                parts = [clean(x) for x in re.split(r"(?<=[\d.])\s{2,}|(?<=[a-zA-Z)])\s+(?=[A-ZÁÉÍÓÚÑ][^.]*?[sS]\s*/)", text) if clean(x)]
                for p in parts:
                    vm = PRICE_RE.search(p)
                    if vm:
                        last_item["variants"].append({
                            "name": PRICE_RE.sub("", p).strip(" -–—."),
                            "price": float(vm.group(1).replace(",", ".")),
                        })
                if not last_item["variants"]:
                    last_item["desc"] = (last_item["desc"] + " " + text).strip()
            else:
                last_item["desc"] = (last_item["desc"] + " " + text).strip()
    return {"title": page_title, "subsections": subsections}


def main():
    out = {}
    for slug, title in PAGES.items():
        path = os.path.join(REVIEW, "page-%s.html" % slug)
        if not os.path.exists(path):
            print("FALTA: %s" % path, file=sys.stderr)
            continue
        data = parse_page(path)
        data["label"] = title
        data["slug"] = slug
        out[slug] = data

    dest = r"C:\Users\leonn\Documents\web\senorlimon\_review\menu.json"
    with open(dest, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=2)

    total_items = 0
    total_price = 0
    for slug, data in out.items():
        n = sum(len(s["items"]) for s in data["subsections"])
        total_items += n
        total_price += sum(1 for s in data["subsections"] for i in s["items"] if i["price"])
        print("%-20s %-30s subsecciones=%2d platos=%3d" % (slug, data["title"], len(data["subsections"]), n))
    print("TOTAL platos=%d con_precio=%d" % (total_items, total_price))


if __name__ == "__main__":
    main()
