# -*- coding: utf-8 -*-
"""Localiza las 8 direcciones con Nominatim (OpenStreetMap) y guarda las coordenadas"""
import io, json, os, ssl, time, urllib.parse, urllib.request

RAIZ = r"C:\Users\leonn\Documents\web\senorlimon"
SALIDA = os.path.join(RAIZ, "_review", "geocode.json")

CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE
UA = {"User-Agent": "senorlimon-web-redesign/1.0 (contacto: leonnnc@gmail.com)"}

DIRECCIONES = [
    ("La Molina", "Av. Javier Prado Este 5335", "7155320"),
    ("La Molina", "Av. Constructores 958", "6806332"),
    ("San Isidro", "Av. Guillermo Prescott 415", "7156340"),
    ("San Isidro", "Av. Guillermo Prescott 370", "6805373"),
    ("San Isidro", "Av. Conquistadores 299", "2218327"),
    ("San Miguel", "Av. Universitaria 722", "7139914"),
    ("San Miguel", "Av. La Mar 2311", "7155418"),
    ("Cercado de Lima", "Av. Naciones Unidas 1160", "6805554"),
]

resultado = {}
if os.path.exists(SALIDA):
    resultado = json.load(io.open(SALIDA, encoding="utf-8"))

for distrito, direccion, telefono in DIRECCIONES:
    clave = direccion
    if clave in resultado and resultado[clave].get("lat"):
        print("%-34s (ya estaba) %s, %s" % (direccion, resultado[clave]["lat"], resultado[clave]["lon"]))
        continue
    consulta = "%s, %s, Lima, Peru" % (direccion, distrito)
    url = ("https://nominatim.openstreetmap.org/search?format=json&limit=1&q=" +
           urllib.parse.quote(consulta))
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=45, context=CTX) as r:
            datos = json.loads(r.read().decode("utf-8"))
        if datos:
            resultado[clave] = {
                "distrito": distrito,
                "lat": float(datos[0]["lat"]),
                "lon": float(datos[0]["lon"]),
                "etiqueta": datos[0].get("display_name", "")[:110],
            }
            print("%-34s -> %.6f, %.6f" % (direccion, resultado[clave]["lat"], resultado[clave]["lon"]))
        else:
            print("%-34s -> SIN RESULTADO" % direccion)
            resultado.setdefault(clave, {"distrito": distrito, "lat": None, "lon": None})
    except Exception as e:
        print("%-34s -> ERROR %s" % (direccion, e))
    time.sleep(1.3)   # política de uso de Nominatim: máximo 1 petición por segundo

json.dump(resultado, io.open(SALIDA, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("guardado:", SALIDA)
