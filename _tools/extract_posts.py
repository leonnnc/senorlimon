# -*- coding: utf-8 -*-
"""Extrae el texto completo de los posts del blog y los enlaces sociales del pie"""
import re, io
from html import unescape


def clean(t):
    t = re.sub(r"<[^>]+>", " ", t)
    t = unescape(t).replace("\xa0", " ").replace("\u200b", "")
    return re.sub(r"\s+", " ", t).strip()


POSTS = {
    "nuestros-origenes": "Nuestros orígenes",
    "sobre-los-platos": "¿Te imaginas un cebiche sin limón?",
    "gastronomia-peruana": "Gastronomía peruana",
}

REVIEW = r"C:\Users\leonn\Documents\web\senorlimon\_review"
out = io.StringIO()

for slug, label in POSTS.items():
    html = open("%s\\post-%s.html" % (REVIEW, slug), encoding="utf-8").read()
    # recorta el cuerpo del articulo: entre el H1 "Senor Limon" y los productos
    start = html.find("Productos")
    m = re.search(r"<h2[^>]*>(.*?)</h2>", html, re.S)
    title = clean(m.group(1)) if m else label
    body_start = m.end() if m else 0
    end = html.find("eltdf-blog-single-navigation", body_start)
    if end < 0:
        end = html.find("Productos", body_start)
    body = html[body_start:end if end > 0 else len(html)]
    paras = [clean(p) for p in re.findall(r"<p[^>]*>(.*?)</p>", body, re.S)]
    paras = [p for p in paras if len(p) > 3]
    out.write("\n## %s\n\n" % title)
    for p in paras:
        out.write("%s\n\n" % p)

# enlaces sociales y externos del pie
html = open("%s\\page-about-us.html" % REVIEW, encoding="utf-8").read()
socials = {}
for m in re.finditer(r'href="(https?://(?:www\.)?(?:facebook|instagram|twitter|youtube|tiktok)\.com[^"]*)"', html):
    socials[m.group(1)] = True
out.write("\n## Enlaces externos detectados\n\n")
for s in sorted(socials):
    out.write("- %s\n" % s)

open("%s\\blog_texts.md" % REVIEW, "w", encoding="utf-8").write(out.getvalue())
print("ok", len(out.getvalue()))
