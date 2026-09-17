# -*- coding: utf-8 -*-
"""Genera assets/js/data.js a partir del contenido real extraido del sitio actual"""
import json, os, re, io

REVIEW = r"C:\Users\leonn\Documents\web\senorlimon\_review"
OUT = r"C:\Users\leonn\Documents\web\senorlimon\assets\js\data.js"
os.makedirs(os.path.dirname(OUT), exist_ok=True)

menu = json.load(open(os.path.join(REVIEW, "menu.json"), encoding="utf-8"))

# --- limpieza de nombres y precios ---
def clean_name(n):
    n = n.replace("  ", " ").strip()
    n = re.sub(r"\s*\.00\s*$", "", n)
    n = re.sub(r"\s*-\s*$", "", n)
    n = re.sub(r"\s{2,}", " ", n)
    return n.strip(" .-")


def clean_desc(d):
    d = re.sub(r"\s{2,}", " ", d or "").strip()
    return d


DESC_ERRONEAS = {  # descripciones copiadas por error en el sitio original
    ("cebiches", "CLÁSICO DE CEBICHES"),
    ("especialidades", "CHARELA A LA PLANCHA"),
}


def build_items(page_slug, subs):
    items, seen = [], set()
    for it in subs["items"]:
        name = clean_name(it["name"])
        price = it["price"]
        if not name and price is not None and items and items[-1]["precio"] is None:
            items[-1]["precio"] = price          # nombre y precio en elementos separados
            continue
        if not name:
            continue
        key = (name.upper(), price)
        if key in seen:                           # duplicados exactos del original
            continue
        seen.add(key)
        desc = clean_desc(it["desc"])
        if (page_slug, name.upper()) in DESC_ERRONEAS:
            desc = ""
        entry = {"nombre": name, "precio": price, "desc": desc}
        # el pie de página mete imágenes ajenas a la carta (tarjetas de pago, logos):
        # si el parser las asignó a un plato, se descartan en vez de mostrarlas como foto
        img = it.get("img_key") or ""
        if img and not any(ruido in img for ruido in ("tarjetas", "logo", "descargable", "pixel")):
            entry["img"] = img + ".webp"
        if it.get("variants"):
            entry["variantes"] = [
                {"nombre": clean_name(v["name"]), "precio": v["price"]} for v in it["variants"]
            ]
        items.append(entry)
    return items


def subsections(slug, names=None):
    page = menu[slug]
    out = []
    for sub in page["subsections"]:
        label = clean_name(sub["name"])
        if names and label not in names:
            continue
        items = build_items(slug, sub)
        if items:
            out.append({"nombre": label, "items": items})
    return out


# La pagina /leche-de-tigre/ del sitio original es en realidad "Promociones":
# contiene PARA 2, LECHE DE TIGRE y un grupo de promociones sin encabezado.
lt = menu["leche-de-tigre"]
promo_subs, leche_subs = [], []
for sub in lt["subsections"]:
    label = clean_name(sub["name"])
    items = build_items("leche-de-tigre", sub)
    if not items:
        continue
    if label == "LECHE DE TIGRE":
        leche_subs.append({"nombre": label, "items": items})
    elif label == "PARA 2":
        promo_subs.append({"nombre": "Para compartir (2 personas)", "items": items})
    else:
        resto = [i for i in items if i["nombre"].upper().startswith(("TACU TACU", "CABRILLA", "SECO", "FESTIVAL"))]
        leche_items = [i for i in items if i not in resto]
        if leche_items:
            leche_subs[0]["items"].extend(leche_items) if leche_subs else leche_subs.append(
                {"nombre": label, "items": leche_items})
        if resto:
            promo_subs.append({"nombre": "Promociones de la casa", "items": resto})

categorias = [
    {"id": "cebiches", "nombre": "Cebiches y Tiraditos", "icono": "ceviche",
     "subs": subsections("cebiches")},
    {"id": "piqueos", "nombre": "Piqueos", "icono": "piqueo",
     "subs": subsections("piqueos")},
    {"id": "leche-de-tigre", "nombre": "Leche de Tigre", "icono": "leche",
     "subs": leche_subs},
    {"id": "sopas-y-sudados", "nombre": "Sopas y Sudados", "icono": "sopa",
     "subs": subsections("sopas-y-sudados")},
    {"id": "pescados-enteros", "nombre": "Pescados Enteros", "icono": "pescado",
     "subs": subsections("pescados-enteros")},
    {"id": "makis", "nombre": "Makis", "icono": "maki",
     "subs": subsections("makis")},
    {"id": "pastas-y-risottos", "nombre": "Pastas, Risottos y Arroces", "icono": "pasta",
     "subs": subsections("pastas-y-risottos")},
    {"id": "especialidades", "nombre": "Especialidades de la Casa", "icono": "especial",
     "subs": subsections("especialidades")},
    {"id": "promociones", "nombre": "Promociones", "icono": "promo", "subs": promo_subs},
    {"id": "cervezas-y-gaseosas", "nombre": "Cervezas y Gaseosas", "icono": "bebida",
     "subs": subsections("cervezas-y-gaseosas")},
]

# --- fotos de bebidas ---
# El sitio original no tiene ni una foto de bebidas (esa sección quedaba en blanco).
# Estas diez imágenes se generaron para la web nueva: son genéricas y sin marca.
IMAGENES_BEBIDAS = {
    "CORONA": "bebida-botella-limon.webp",
    "CUSQUEÑA DORADA": "bebida-lager-vaso.webp",
    "CUSQUEÑA TRIGO": "bebida-trigo-naranja.webp",
    "STELLA ARTOIS": "bebida-botella-verde.webp",
    "MICHELOB ULTRA": "bebida-botella-ambar.webp",
    "PILSEN CALLAO": "bebida-pilsner-vaso.webp",
    "BUDWEISER": "bebida-botellas-hielo.webp",
    "CUSQUEÑA NEGRA": "bebida-negra.webp",
    "INCA KOLA O COCA COLA ZERO": "bebida-gaseosa-hielo.webp",
    "AGUA EMBOTELLADA": "bebida-agua.webp",
}

for cat in categorias:
    if cat["id"] != "cervezas-y-gaseosas":
        continue
    for sub in cat["subs"]:
        for it in sub["items"]:
            foto = IMAGENES_BEBIDAS.get(it["nombre"].upper())
            if foto:
                it["img"] = foto

# --- fotos para los 31 platos que salían sin imagen ---
# 15 salen de la biblioteca de medios del propio restaurante (fotos reales) y
# 16 se generaron porque no existía ninguna foto de ese plato en el sitio.
FOTOS_PLATOS = {
    # fotos reales de la biblioteca del sitio
    "CEBICHE DE CONCHAS NEGRAS": "plato-cebiche-de-conchas-negras-2.webp",
    "CEBICHE MIXTO DE LENGUADO": "plato-cebiche-mixto-de-lenguado.webp",
    "CEBICHE MIXTO DE CHARELA": "plato-cebiche-mixto-de-charela.webp",
    "COMBINACIÓN CLÁSICA": "plato-combinacion-clasica.webp",
    "LECHE DE TIGRE TRADICIONAL": "plato-leche-de-tigre-tradicional.webp",
    "LECHE DE TIGRE SEÑOR LIMÓN": "plato-leche-de-tigre-senor-limon.webp",
    "TACU TACU CON LOMO A LO POBRE": "plato-tacu-tacu-con-lomo-a-lo-pobre.webp",
    "CHUPE DE CAMARONES": "plato-chupe-de-camarones.webp",
    "SUDADO DE PESCADO": "plato-sudado-de-pescado.webp",
    "TRUCHA A LA PARRILLA": "plato-trucha-a-la-parrilla.webp",
    "RISOTTO A LA HUANCAINA CON LOMO SALTADO": "plato-risotto-a-la-huancaina-con-lomo-saltado.webp",
    "FILETE DE TRUCHA O PESCADO AL AJO CON LANGOSTINOS": "plato-filete-de-trucha-al-ajo-con-langostinos.webp",
    "LOMO SALTADO CRIOLLO": "plato-lomo-saltado-criollo.webp",
    "PESCADO EN SALSA DE CHAMPIÑONES": "plato-pescado-en-salsa-de-champinones.webp",
    "PARRILLA MARINA": "plato-parrilla-marina.webp",
    # imágenes generadas para la web nueva (no existían fotos de estos platos)
    "CEBICHE DE LENGUADO": "plato-cebiche-de-lenguado.webp",
    "CEBICHE DE CHARELA": "plato-cebiche-de-charela.webp",
    "TIRADITO AL AJÍ AMARILLO (PESCA DEL DÍA)": "plato-tiradito-al-aji-amarillo.webp",
    "LECHE DE TIGRE CRIOLLO": "plato-leche-de-tigre-criollo.webp",
    "LECHE DE TIGRE NORTEÑO": "plato-leche-de-tigre-norteno.webp",
    "CABRILLA ORIENTAL": "plato-cabrilla-oriental.webp",
    "SECO DE ASADO DE TIRA": "plato-seco-de-asado-de-tira.webp",
    "FESTIVAL DE SUDADO": "plato-festival-de-sudado.webp",
    "SUDADO DE CHITA": "plato-sudado-de-chita.webp",
    "CHITA AL AJO CROCANTE": "plato-chita-al-ajo-crocante.webp",
    "TACU TACU A LO MACHO": "plato-tacu-tacu-a-lo-macho.webp",
    "TACU TACU CON LOMO SALTADO": "plato-tacu-tacu-con-lomo-saltado.webp",
    "CHARELA A LA PLANCHA": "plato-charela-a-la-plancha.webp",
    "MILANESA DE PESCADO": "plato-milanesa-de-pescado.webp",
    "PESCADO EN SALSA CUATRO QUESOS": "plato-pescado-en-salsa-cuatro-quesos.webp",
    "PULPO A LA PARRILLA": "plato-pulpo-a-la-parrilla.webp",
}

# fotos corregidas: quitaban duplicados (dos platos distintos con la misma imagen)
FOTOS_CORREGIDAS = {
    "FESTIVAL DE CAUSA": "plato-festival-de-causa.webp",
    "JALEA MIXTA": "plato-jalea-mixta.webp",
    "SUDADO DE CABRILLA": "plato-sudado-de-cabrilla.webp",
    "CHICHARRÓN MIXTO": "plato-chicharron-mixto.webp",
}

for cat in categorias:
    for sub in cat["subs"]:
        for it in sub["items"]:
            nombre = it["nombre"].upper()
            foto = FOTOS_CORREGIDAS.get(nombre) or FOTOS_PLATOS.get(nombre)
            if foto:
                it["img"] = foto

# platos destacados para la portada (solo los que tienen foto real)
DESTACADOS = [
    ("cebiches", "CEBICHE MIXTO"),
    ("cebiches", "MATRIMONIO"),
    ("piqueos", "CHICHARRÓN DE CALAMAR"),
    ("sopas-y-sudados", "PARIHUELA"),
    ("pastas-y-risottos", "RISOTTO A LA HUANCAINA CON LOMO AL WOK"),
    ("especialidades", "PESCADO TUSAN"),
]

destacados = []
for cat_id, nombre in DESTACADOS:
    for cat in categorias:
        if cat["id"] != cat_id:
            continue
        for sub in cat["subs"]:
            for it in sub["items"]:
                if it["nombre"].upper() == nombre.upper():
                    destacados.append({
                        "nombre": it["nombre"], "precio": it["precio"], "desc": it["desc"],
                        "img": it.get("img"), "categoria": cat["nombre"], "catId": cat_id,
                    })

# Horario y zonas de reparto tomados de las fichas oficiales de cada local
# (imágenes LOCALES-01…08 del sitio original). Todos abren de 12:00 a 5:30 p.m.
HORARIO = "12:00 a 5:30 p.m."
ZONAS_SAN_ISIDRO = ["San Isidro", "Parque El Olivar", "Surquillo", "Salaverry", "Jesús María",
                    "Pueblo Libre", "Lince"]
ZONAS_SAN_MIGUEL = ["San Miguel", "Av. La Marina", "Bellavista", "La Perla", "Av. Universitaria",
                    "Av. Elmer Faucett", "Av. La Paz"]
ZONAS_LA_MOLINA_A = ["La Molina", "Av. Los Frutales", "Camacho", "San Borja", "Salamanca",
                     "Santa Anita", "Jockey"]
ZONAS_LA_MOLINA_B = ["La Molina", "Mayorazgo", "Puruchuco", "Ate", "Av. Los Ingenieros",
                     "Santa Anita", "Monumental"]
ZONAS_CERCADO = ["Cercado de Lima", "Breña", "Av. Arica", "Plaza 2 de Mayo", "Mirones Bajos",
                 "Av. Argentina", "Malvinas"]

locales = [
    {"distrito": "La Molina", "direccion": "Av. Javier Prado Este 5335", "telefono": "7155320",
     "tel": "7155320", "horario": HORARIO, "atencion": "Delivery", "zonas": ZONAS_LA_MOLINA_A,
     "lat": -12.072315, "lon": -76.958133, "mapa": "mapa-javier-prado.webp"},
    {"distrito": "La Molina", "direccion": "Av. Constructores 958", "telefono": "6806332",
     "tel": "6806332", "horario": HORARIO, "atencion": "Delivery", "zonas": ZONAS_LA_MOLINA_B,
     "lat": -12.065462, "lon": -76.953904, "mapa": "mapa-constructores.webp"},
    {"distrito": "San Isidro", "direccion": "Av. Guillermo Prescott 415", "telefono": "7156340",
     "tel": "7156340", "horario": HORARIO, "atencion": "Delivery", "zonas": ZONAS_SAN_ISIDRO,
     "lat": -12.087375, "lon": -77.048284, "mapa": "mapa-prescott-415.webp"},
    {"distrito": "San Isidro", "direccion": "Av. Guillermo Prescott 370", "telefono": "6805373",
     "tel": "6805373", "horario": HORARIO, "atencion": "Reservas", "zonas": ZONAS_SAN_ISIDRO,
     "lat": -12.085360, "lon": -77.048624, "mapa": "mapa-prescott-370.webp"},
    {"distrito": "San Isidro", "direccion": "Av. Conquistadores 299", "telefono": "2218327",
     "tel": "2218327", "horario": HORARIO, "atencion": "Reservas", "zonas": [],
     "lat": -12.098985, "lon": -77.036149, "mapa": "mapa-conquistadores.webp"},
    {"distrito": "San Miguel", "direccion": "Av. Universitaria 722", "telefono": "7139914",
     "tel": "7139914", "horario": HORARIO, "atencion": "Delivery", "zonas": ZONAS_SAN_MIGUEL,
     "lat": -12.081208, "lon": -77.082256, "mapa": "mapa-universitaria.webp"},
    {"distrito": "San Miguel", "direccion": "Av. La Mar 2311", "telefono": "7155418",
     "tel": "7155418", "whatsapp": "51913624377", "horario": HORARIO, "atencion": "Delivery",
     "zonas": ZONAS_SAN_MIGUEL, "lat": -12.074100, "lon": -77.086134, "mapa": "mapa-la-mar.webp"},
    {"distrito": "Cercado de Lima", "direccion": "Av. Naciones Unidas 1160", "telefono": "6805554",
     "tel": "6805554", "horario": HORARIO, "atencion": "Delivery", "zonas": ZONAS_CERCADO,
     "lat": -12.050960, "lon": -77.060405, "mapa": "mapa-naciones-unidas.webp"},
]

# cada mapa tiene una versión ampliada para el modal
for l in locales:
    if l.get("mapa"):
        l["mapaGrande"] = l["mapa"].replace(".webp", "-grande.webp")

data = {
    "marca": {
        "nombre": "Señor Limón",
        "lema": "Cevichería y cocina marina peruana",
        "desde": 2001,
        "whatsapp": "51913624377",
        "instagram": "https://www.instagram.com/senorlimonoficial/",
        "youtube": "https://www.youtube.com/channel/UCtr-tHlAeg0u5ptyzKB5sug/videos",
        "delivery": "Delivery gratis hasta 3.5 km",
        "horarios": "12:00 a 5:30 p.m.",
    },
    "locales": locales,
    "categorias": categorias,
    "destacados": destacados,
    "testimonios": [
        {"texto": "Hoy pedí un arroz chaufa con pescado. Quedé satisfecha. El local muy lindo y el trato muy bueno.",
         "autor": "Lucero Maynas"},
        {"texto": "El restaurante es A1, 100% recomendado. La comida el especial en matrimonio riquísimo. Me dejaron parquear mi carrito y súper amables desde el ingreso.",
         "autor": "Jhon Fausto"},
        {"texto": "Su atención y la comida son espectaculares, es uno de mis restaurantes favoritos. Lo recomiendo 100%.",
         "autor": "Maria Felix Briceño"},
    ],
    "historia": [
        {"titulo": "Nuestros orígenes", "parrafos": [
            "La cadena de restaurantes Señor Limón nace por iniciativa de un apasionado cocinero que inició sus labores gastronómicas a partir de los 16 años. Señor Limón inicia sus actividades comerciales un 1 de diciembre del 2001, en la Av. La Mar 2311, San Miguel, debiendo su crecimiento a sus sabores propios fusionados de comidas orientales y peruanas, las cuales mantiene desde el primer día de operaciones, siempre con mejoras sublimes.",
            "Es así que un 31 de mayo del 2003 inaugurábamos el segundo local, ubicado en la Av. Guillermo Prescott 415, en San Isidro, zona con mucha actividad corporativa. Desde ese momento Señor Limón comienza su despegue organizacional."
        ]},
        {"titulo": "¿Te imaginas un cebiche sin limón?", "parrafos": [
            "Es imposible; es más, si no hay limón no hay cebiche, acotará cualquier peruano orgulloso de saber que el inigualable sabor del limón peruano es el único capaz de otorgarle la cocción y el sabor singular a este reconocido plato en el mundo.",
            "El limón peruano o limón sutil es un tipo de limón que crece únicamente en nuestro país, que posee propiedades sin igual y es solicitado a nivel mundial.",
            "Lo que hace especial a nuestro limón es la tierra. «Nuestro limón vino con la conquista, pero cuando fue sembrado en nuestra tierra le dio propiedades que no le da en otras partes del mundo: su sabor, su acidez, la cantidad de jugo, su cáscara fina, su lindo color, aroma y tamaño».",
            "El distrito de Tambogrande está ubicado en el Valle de San Lorenzo, 85 kilómetros al norte de Piura, y es considerado uno de los principales productores de limón del país, así como el valle del Alto Piura y el valle de Olmos en Lambayeque. Considerando los tres valles contamos con aprox. 25,000 hectáreas de producción de limón peruano de excelente calidad.",
            "Es por ello que el equipo de colaboradores de la cadena de restaurantes se rinde ante el insumo peruano de inobjetable sabor único, para otorgarle el lugar que se merece, enseñoreando su nombre. Es allí cuando nace el nombre comercial indiscutible."
        ]},
        {"titulo": "Gastronomía peruana", "parrafos": [
            "La gastronomía peruana es una celebración del Perú. Un país con una tradición milenaria y un promisorio futuro que no pierde de vista sus raíces y donde el arte del buen comer destaca entre sus habitantes como uno de los signos más distintivos de su identidad.",
            "La gastronomía peruana ha sido postulada para ser declarada Patrimonio de la Humanidad (2011).",
            "El pueblo peruano es famoso por su paladar exigente y refinado, el cual proviene de épocas inmemoriales. Las técnicas precolombinas permitieron la preparación de sopas, guisos y pescados crudos. El procesamiento de la comida era parte común de la vida diaria, al contar con conocimientos para salar carne, deshidratar y cocer en hornos de tierra natural.",
            "Con la colonización española, unida a la migración africana, china, italiana y japonesa, la cocina peruana acogió diferentes formas de ver el mundo y nuevas técnicas de preparación. Destaca la influencia de España y de China, que originó gastronomías con denominación propia: comida criolla y chifa, respectivamente.",
            "La riqueza de la cocina peruana se sustenta en el mestizaje de sus culturas, así como en la existencia de una de las mayores biodiversidades de la Tierra, lo que ha producido el nacimiento y evolución de gastronomías únicas.",
            "La cocina costeña data de épocas virreinales, sobresaliendo dulces de gran acogida como la mazamorra, el turrón y los picarones. De igual modo, destacan los pescados crudos preparados en un platillo que ha dado la vuelta al mundo: el cebiche."
        ]},
    ],
}

header = ("/* Datos de Señor Limón generados desde el contenido real de senorlimon.com.\n"
          "   Editar este archivo para actualizar precios, platos o locales.\n"
          "   Los platos sin precio en el origen quedan con precio: null. */\n")
js = header + "window.SL_DATA = " + json.dumps(data, ensure_ascii=False, indent=2) + ";\n"
open(OUT, "w", encoding="utf-8").write(js)

n_cat = len(categorias)
n_items = sum(len(s["items"]) for c in categorias for s in c["subs"])
n_con_precio = sum(1 for c in categorias for s in c["subs"] for i in s["items"] if i["precio"])
n_fotos = sum(1 for c in categorias for s in c["subs"] for i in s["items"] if i.get("img"))
print("categorias=%d subsecciones=%d platos=%d con_precio=%d con_foto=%d destacados=%d locales=%d"
      % (n_cat, sum(len(c["subs"]) for c in categorias), n_items, n_con_precio, n_fotos,
         len(destacados), len(locales)))
print("data.js ->", round(os.path.getsize(OUT) / 1024, 1), "KB")
