# -*- coding: utf-8 -*-
"""Comprueba que las etiquetas HTML de cada página estén balanceadas"""
import io, os, sys
from html.parser import HTMLParser

RAIZ = r"C:\Users\leonn\Documents\web\senorlimon"
VACIAS = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta",
          "source", "track", "wbr", "path", "circle", "rect", "line", "polygon"}


class Balance(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.pila = []
        self.errores = []

    def handle_starttag(self, tag, attrs):
        if tag not in VACIAS:
            self.pila.append((tag, self.getpos()[0]))

    def handle_startendtag(self, tag, attrs):
        pass

    def handle_endtag(self, tag):
        if tag in VACIAS:
            return
        if not self.pila:
            self.errores.append("cierre sin apertura: </%s> línea %d" % (tag, self.getpos()[0]))
            return
        if self.pila[-1][0] != tag:
            if any(t == tag for t, _ in self.pila):
                while self.pila and self.pila[-1][0] != tag:
                    t, ln = self.pila.pop()
                    self.errores.append("sin cerrar: <%s> abierto en línea %d" % (t, ln))
                if self.pila:
                    self.pila.pop()
            else:
                self.errores.append("cierre inesperado: </%s> línea %d" % (tag, self.getpos()[0]))
        else:
            self.pila.pop()


fallos = 0
for nombre in sorted(f for f in os.listdir(RAIZ) if f.endswith(".html")):
    p = Balance()
    p.feed(io.open(os.path.join(RAIZ, nombre), encoding="utf-8").read())
    pendientes = ["<%s> línea %d" % (t, ln) for t, ln in p.pila]
    if p.errores or pendientes:
        fallos += 1
        print("FALLA %s" % nombre)
        for e in p.errores[:8]:
            print("      ", e)
        if pendientes:
            print("       sin cerrar al final:", ", ".join(pendientes[:8]))
    else:
        print("OK    %s" % nombre)

sys.exit(1 if fallos else 0)
