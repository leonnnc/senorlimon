# -*- coding: utf-8 -*-
"""Vuelca el flujo de tokens (encabezados, parrafos, imagenes) de una pagina de carta"""
import re, sys, io
from html import unescape

TOKEN_RE = re.compile(r'<img\b[^>]*?src="([^"]+)"[^>]*?>|<(h[1-6]|p|li|span|strong)\b[^>]*>(.*?)</\2\s*>', re.S | re.I)
PRICE_RE = re.compile(r"[sS]\s*/\s*(\d+(?:[.,]\d{2})?)")


def clean(t):
    t = re.sub(r"<[^>]+>", " ", t)
    t = unescape(t).replace("\xa0", " ")
    return re.sub(r"\s+", " ", t).strip()


def main():
    path = sys.argv[1]
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10 ** 9
    with open(path, encoding="utf-8") as fh:
        html = fh.read()
    m = re.search(r'eltdf-st-title[^>]*>\s*(.*?)\s*</h1>', html, re.S)
    start = m.end() if m else 0
    for marker in ["eltdf-testimonials-holder", "eltdf-footer-inner", "footer-bottom"]:
        i = html.find(marker, start)
        if i > 0:
            html = html[:i]
    region = html[start:]
    n = 0
    for t in TOKEN_RE.finditer(region):
        if t.group(1):
            print("IMG  %s" % t.group(1).split("/")[-1])
            n += 1
            continue
        tag = t.group(2).lower()
        txt = clean(t.group(3))
        if not txt:
            continue
        if tag in ("span", "strong") and len(txt) < 3:
            continue
        trunc = int(sys.argv[3]) if len(sys.argv) > 3 else 170
        print("%-6s %s" % (tag.upper(), txt[:trunc]))
        n += 1
        if n > limit:
            print("... (cortado)")
            break


main()
