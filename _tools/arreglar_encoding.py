# -*- coding: utf-8 -*-
"""Deshace la doble codificación que dejó PowerShell y añade createElement al simulador"""
import io, os

RUTA = r"C:\Users\leonn\Documents\web\senorlimon\_tools\test_render.js"

texto = io.open(RUTA, encoding="utf-8-sig").read()
print("antes:  'versión' presente:", "versión" in texto, "| mojibake:", "versiÃ³n" in texto)

if "versiÃ³n" in texto and "versión" not in texto:
    try:
        # PowerShell leyó el archivo como CP1252 y lo reescribió como UTF-8
        texto = texto.encode("cp1252").decode("utf-8")
        print("doble codificación revertida")
    except Exception as e:
        print("no se pudo revertir automáticamente:", e)

if "createElement" not in texto:
    texto = texto.replace(
        "    querySelectorAll: function (sel) { return raiz.querySelectorAll(sel); },",
        "    querySelectorAll: function (sel) { return raiz.querySelectorAll(sel); },\n"
        "    createElement: function (t) { return new Nodo(t, {}); },")
    print("createElement añadido al documento simulado")

io.open(RUTA, "w", encoding="utf-8", newline="\n").write(texto)
print("después: 'versión' presente:", "versión" in texto, "| mojibake:", "versiÃ³n" in texto)
print("createElement:", "createElement" in texto)
