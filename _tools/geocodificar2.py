# -*- coding: utf-8 -*-
"""Segunda pasada: afina las direcciones que quedaron imprecisas"""
import io, json, os, ssl, time, urllib.parse, urllib.request

RAIZ = r"C:\Users\leonn\Documents\web\senorlimon"
SALIDA = os.path.join(RAIZ, "_review", "geocode.json")
CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE
UA = {"User-Agent": "senorlimon-web-redesign/1.0 (contacto: leonnc@gmail.com)"}

VARIANTES = {
    "Av. Guillermo Prescott 415": [
        "Guillermo Prescott 415, San Isidro, Lima",
        "Avenida Guillermo Prescott 415, San Isidro, Lima, Peru",
    ],
    "Av. Guillermo Prescott 370": [
        "Avenida Guillermo Prescott 370, San Isidro, Lima, Peru",
        "Guillermo Prescott 370, Lima",
    ],
    "Av. Naciones Unidas 1160": [
        "Avenida Naciones Unidas 1160, Lima, Peru",
        "Naciones Unidas 1160, Jesus Maria, Lima, Peru",
        "Avenida Naciones Unidas, Lima, Peru",
    ],
}


def buscar(consulta):
    url = ("https://nominatim.openstreetmap.org/search?format=json&addressdetails=1&limit=3&q=" +
           urllib.parse.quote(consulta))
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=45, context=CTX) as r:
        return json.loads(r.read().decode("utf-8"))


for clave, consultas in VARIANTES.items():
    print("\n== %s" % clave)
    for consulta in consultas:
        try:
            datos = buscar(consulta)
            for d in datos[:3]:
                tipo = d.get("type", "")
                num = (d.get("address") or {}).get("house_number", "-")
                print("   [%s/%s casa=%s] %.6f, %.6f  %s" % (
                    d.get("class"), tipo, num, float(d["lat"]), float(d["lon"]),
                    d.get("display_name", "")[:80]))
            if not datos:
                print("   (sin resultados) %s" % consulta)
        except Exception as e:
            print("   ERROR %s" % e)
        time.sleep(1.3)
