# -*- coding: utf-8 -*-
"""Comprueba que las clases usadas en HTML/JS existan en el CSS y que el CSS esté balanceado"""
import io, os, re

RAIZ = r"C:\Users\leonn\Documents\web\senorlimon"
css = io.open(os.path.join(RAIZ, "assets", "css", "styles.css"), encoding="utf-8").read()

# el panel de administración inyecta sus propios estilos desde panel.js:
# se añaden aquí para que sus clases cuenten como definidas
panel_js = io.open(os.path.join(RAIZ, "assets", "js", "panel.js"), encoding="utf-8").read()
bloque = re.search(r"var ESTILOS = '(.*?)';\n", panel_js, re.S)
if bloque:
    css += bloque.group(1)

# balance de llaves
if css.count("{") != css.count("}"):
    print("ERROR: llaves desbalanceadas en styles.css (%d abre, %d cierra)" % (css.count("{"), css.count("}")))
else:
    print("CSS balanceado: %d reglas" % css.count("{"))

# valores inválidos comunes
for m in re.finditer(r":\s*([^;{}]*\b(?:murky|undefined|NaN)\b[^;{}]*)", css):
    print("ERROR valor sospechoso en CSS:", m.group(1).strip())

definidas = set(re.findall(r"\.([a-zA-Z][\w-]*)", css))

fuentes = [os.path.join(RAIZ, f) for f in os.listdir(RAIZ) if f.endswith(".html")]
fuentes += [os.path.join(RAIZ, "assets", "js", "app.js")]

usadas = {}
for ruta in fuentes:
    txt = io.open(ruta, encoding="utf-8").read()
    for m in re.finditer(r'class="([^"]*)"', txt):
        for c in m.group(1).split():
            # el JS arma clases por concatenación: se toman solo los tokens válidos
            c = re.match(r"[a-zA-Z][\w-]*", c)
            if c:
                usadas.setdefault(c.group(0), set()).add(os.path.basename(ruta))

faltan = {c: v for c, v in usadas.items() if c not in definidas}
if faltan:
    print("\nERROR: clases usadas sin definir en CSS (%d):" % len(faltan))
    for c in sorted(faltan):
        print("  - .%s  (%s)" % (c, ", ".join(sorted(faltan[c]))))
else:
    print("Todas las clases usadas están definidas en el CSS (%d clases)" % len(usadas))

# ids referenciados por el JS
app = io.open(os.path.join(RAIZ, "assets", "js", "app.js"), encoding="utf-8").read()
ids_js = set(re.findall(r"\$\('#([\w-]+)'", app)) | set(re.findall(r"getElementById\('([\w-]+)'", app))
ids_html = set()
for ruta in [os.path.join(RAIZ, f) for f in os.listdir(RAIZ) if f.endswith(".html")]:
    ids_html |= set(re.findall(r'id="([^"]+)"', io.open(ruta, encoding="utf-8").read()))

# el modal se construye en tiempo de ejecución, así que sus ids no están en el HTML
dinamicos = {"sl-modal", "sl-modal-img", "sl-modal-titulo", "sl-modal-contador", "sl-modal-acciones",
             "sl-panel", "sl-editor", "sl-caja", "sl-texto", "sl-img", "sl-vista", "sl-lista",
             "sl-pie", "sl-archivo", "sl-incluir", "sl-estilos", "sl-estado-img"}
sin_id = sorted(i for i in ids_js if i not in ids_html and i not in dinamicos)
print("\nIDs que el JS busca y no existen en el HTML: %s" % (sin_id if sin_id else "ninguno"))
