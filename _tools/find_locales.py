# -*- coding: utf-8 -*-
"""Muestra el contexto de las imagenes LOCALES-xx en la pagina de restaurantes"""
import re
html = open(r"C:\Users\leonn\Documents\web\senorlimon\_review\page-contact-us.html", encoding="utf-8").read()
for m in re.finditer(r"LOCALES-0\d[^\"']*", html):
    i = m.start()
    frag = re.sub(r"\s+", " ", html[max(0, i - 400):i + 200])
    print("---")
    print(frag)
