# -*- coding: utf-8 -*-
"""Comprueba que cada plato y precio del sitio nuevo exista en el HTML original"""
import io, json, os, re, unicodedata, sys

RAIZ = r"C:\Users\leonn\Documents\web\senorlimon"
REVIEW = os.path.join(RAIZ, "_review")

PAGINA = {
    "cebiches": "page-cebiches.html",
    "piqueos": "page-piqueos.html",
    "sopas-y-sudados": "page-sopas-y-sudados.html",
    "pescados-enteros": "page-pescados-enteros.html",
    "makis": "page-makis.html",
    "pastas-y-risottos": "page-pastas-y-risottos.html",
    "especialidades": "page-especialidades.html",
    "cervezas-y-gaseosas": "page-cervezas-y-gaseosas.html",
    "leche-de-tigre": "page-leche-de-tigre.html",
    "promociones": "page-leche-de-tigre.html",
}


def sin_tildes(t):
    t = unicodedata.normalize("NFKD", t)
    return "".join(c for c in t if not unicodedata.combining(c)).lower()


def limpio(t):
    t = re.sub(r"<[^>]+>", " ", t)
    t = (t.replace("&nbsp;", " ").replace("&amp;", "&").replace("&#8217;", "'")
         .replace("&iacute;", "i").replace("&oacute;", "o").replace("&ntilde;", "n")
         .replace("&aacute;", "a").replace("&eacute;", "e").replace("&uacute;", "u"))
    t = t.replace("\xa0", " ").replace("Ã±", "n").replace("Ã³", "o").replace("Ã¡", "a")
    t = t.replace("Ã©", "e").replace("Ã", "i").replace("Â", "")
    return re.sub(r"\s+", " ", t)


cache = {}


def texto_pagina(archivo):
    if archivo not in cache:
        html = io.open(os.path.join(REVIEW, archivo), encoding="utf-8").read()
        cache[archivo] = limpio(html)
    return cache[archivo]


datos = json.loads(io.open(os.path.join(RAIZ, "assets", "js", "data.js"), encoding="utf-8")
                   .read().split("=", 1)[1].rsplit(";", 1)[0])

problemas = []
revisados = 0
con_precio = 0

for cat in datos["categorias"]:
    archivo = PAGINA.get(cat["id"])
    if not archivo:
        problemas.append("categoría sin página de origen mapeada: %s" % cat["id"])
        continue
    fuente = sin_tildes(texto_pagina(archivo))
    for sub in cat["subs"]:
        for it in sub["items"]:
            revisados += 1
            nombre = sin_tildes(it["nombre"])
            nombre = re.sub(r"\s*\.00$", "", nombre).strip()
            # el nombre puede aparecer tambien dentro de la descripcion de otro plato:
            # se revisan todas las apariciones y basta con que una traiga el precio al lado
            apariciones = [m.start() for m in re.finditer(re.escape(nombre), fuente)]
            if not apariciones:
                problemas.append("[%s] nombre no encontrado en el origen: %s" % (cat["id"], it["nombre"]))
                continue
            if it["precio"] is None:
                continue
            con_precio += 1
            valor = "%g" % it["precio"]
            if not any(valor in fuente[p:p + 140] for p in apariciones):
                problemas.append("[%s] precio %s no aparece junto a %s (contexto: %r)"
                                 % (cat["id"], valor, it["nombre"], fuente[apariciones[0]:apariciones[0] + 90]))
            for v in it.get("variantes", []):
                vn = sin_tildes(v["nombre"])
                if vn and vn not in sin_tildes(texto_pagina(archivo)):
                    problemas.append("[%s] variante no encontrada: %s" % (cat["id"], v["nombre"]))

print("platos revisados contra el origen: %d (con precio: %d)" % (revisados, con_precio))
if problemas:
    print("DISCREPANCIAS (%d):" % len(problemas))
    for p in problemas:
        print("  -", p)
    sys.exit(1)
print("Todos los platos, variantes y precios coinciden con el sitio original.")
