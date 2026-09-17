# Revisión de senorlimon.com

**Fecha del análisis:** 16 de septiembre de 2026
**Método:** peticiones HTTP directas al sitio en vivo (cabeceras, HTML fuente, sitemap, peso real de imágenes). No es un análisis visual ni de Search Console.

---

## 1. Estado general

El sitio está **en línea y funcionando correctamente**. Es un WordPress sobre servidor LiteSpeed con tema tipo Eltdf ("Señor Limón"), HTTPS válido y caché de página activa.

| Aspecto | Resultado |
|---|---|
| Respuesta | `200 OK` |
| HTTPS | Activo, con redirección correcta |
| `http://senorlimon.com` | `301` → `https://senorlimon.com/` |
| `https://www.senorlimon.com` | `301` → `https://senorlimon.com/` |
| Página inexistente | `404` correcto (no redirige a home) |
| Caché | LiteSpeed Cache 6.4.1 (`x-litespeed-cache: hit`) |
| Compresión | Brotli activo (HTML de 87 KB → 20.6 KB) |
| Sitemap | `wp-sitemap.xml` (el nativo de WordPress) |
| TTFB medido | ~0.02 s con caché, ~0.64 s en la primera carga en frío |

**Conclusión rápida:** la base técnica del servidor es buena. Los problemas reales están en **el peso de las imágenes, los metadatos SEO ausentes y la cantidad de JavaScript/CSS**.

---

## 2. Lo que está bien

- **HTTPS y canonicalización correctas**: sin contenido duplicado por `www` o `http`.
- **Caché de página funcionando** y compresión Brotli aplicada al HTML.
- **robots.txt correcto** y sitemap declarado en él.
- **Cartas con precios en texto**, no en imagen: los platos y precios (ej. "CEBICHE MIXTO s/54") son indexables por Google.
- **Buen contenido de conversión**: banner "DELIVERY GRATIS HASTA 3.5 KM", teléfonos de locales, mapa, testimonios reales y enlace al canal de YouTube.
- **Viewport móvil configurado** con `user-scalable=yes` (permite zoom, buena accesibilidad).
- **Menú móvil presente** en el tema.

---

## 3. Problemas por prioridad

### 🔴 Crítico — peso de imágenes

| Recurso | Peso |
|---|---|
| `LOCALES-05.png` | 1.85 MB |
| `LOCALES-08.png` | 1.84 MB |
| `LOCALES-01.png` | 1.81 MB |
| `LOCALES-06.png` | 1.72 MB |
| `LOCALES-02.png` | 1.49 MB |
| `LOCALES-07.png` | 1.41 MB |
| `LOCALES-04.png` | 1.39 MB |
| `LOCALES-03.png` | 37 KB |
| **Total de los 8 PNG de locales** | **11.27 MB** |

La página **"Restaurantes" (contact-us)** carga esos 8 PNG, que suman **más de 11 MB**. En un celular con datos móviles esa página tarda muchísimo en abrir y consume datos del cliente. Además:

- No hay **ninguna** imagen en formato WebP (0 referencias en el HTML).
- `CEBICHE.jpg` pesa **490 KB** y `PIQUEOSS.jpg` **393 KB** — son fotos de carta que se muestran en miniatura.

### 🔴 Crítico — SEO on-page inexistente

Verificado en el HTML fuente de la home **y** de la página de locales:

| Elemento | Estado |
|---|---|
| `<meta name="description">` | **Ausente** (0 ocurrencias) |
| Open Graph (`og:`) | **Ausente** — al compartir el link por WhatsApp/Facebook no sale imagen ni descripción |
| Twitter Cards (`twitter:`) | **Ausente** |
| Datos estructurados JSON-LD | **Ausente** — no hay schema `Restaurant`/`LocalBusiness` |
| `<h1>` en la home | **Ausente** (los títulos grandes son `<h2>` de testimonios) |
| Plugin de SEO | No detectado (el sitio usa el sitemap nativo de WordPress) |

Para un restaurante, la falta de schema `Restaurant` y de meta description es lo que más limita la aparición en resultados enriquecidos de Google y en las búsquedas locales.

### 🟠 Alto — exceso de CSS y JavaScript

- **22 hojas de estilo** externas.
- **54 archivos JavaScript** externos.
- **12 bloques de CSS inline** dentro del HTML.
- Se carga el stack completo de Visual Composer + Revolution Slider + PixelYourSite + Contact Form 7, más animaciones jQuery sobre el menú fijo en cada scroll.

Esto penaliza la velocidad en móvil, especialmente combinado con las imágenes de 11 MB.

### 🟠 Alto — carta en PDF desactualizada

En todas las páginas hay un enlace de descarga a:
`/wp-content/uploads/2020/12/Senor-Limon-2020-comprimido1.pdf`

Es la **carta de 2020**, mientras que los precios publicados en la web se actualizaron hasta 2026. Un cliente puede descargar precios incorrectos. Además, el PDF es "comprimido", así que probablemente se ve borroso.

### 🟡 Medio — HTML con contenido duplicado

En la home y en las páginas de carta, el bloque de testimonios aparece **repetido 3 veces** (es un carrusel que duplica las diapositivas en el HTML). Infla el documento y envía señales repetidas a los buscadores.

### 🟡 Medio — detalles técnicos menores

- **1 imagen sin atributo `alt`** en la home.
- **1 recurso cargado por `http://`** (`descargable-1.png`) en páginas servidas por HTTPS: provoca una petición extra. Verificado: la versión https existe y responde `200`, así que se arregla cambiando la URL.
- Payload manejado con **HTTP/1.1**; el servidor anuncia HTTP/3 vía `alt-svc`.
- Aviso de Google en la página: *"reCAPTCHA is changing its terms of service"* — pendiente de migración en la cuenta de reCAPTCHA.

### 🟡 Medio — páginas sin actualizar

Según `lastmod` del sitemap:

| Página | Última modificación |
|---|---|
| `/about-us/` | 17 nov 2020 |
| `/blog/` | 25 ene 2021 |
| `/postres-y-bebidas/` | 12 dic 2021 |
| `/contact-us/` | 20 mar 2025 |
| `/` (home) | 1 sep 2026 |

Las páginas de carta sí se mantienen al día (2026), pero "Nosotros" lleva casi 6 años sin tocarse y el blog está abandonado.

---

## 4. Plan de acción sugerido

**Ronda 1 — impacto inmediato, bajo esfuerzo**
1. Comprimir los 8 PNG de locales y convertirlos a WebP (de 11.27 MB se puede bajar a menos de 1 MB sin pérdida visible). Igual con `CEBICHE.jpg` y `PIQUEOSS.jpg`.
2. Añadir `meta description` a home y a cada página de carta (150–160 caracteres, con distrito y plato estrella).
3. Añadir etiquetas Open Graph con una foto de plato como imagen (`og:image`), así el link se ve bien al compartirlo por WhatsApp.
4. Corregir la URL `http://` del `descargable-1.png`.

**Ronda 2 — visibilidad en Google**
5. Instalar un plugin de SEO (Rank Math o Yoast) y declarar el schema `Restaurant` con dirección, horarios, teléfono y rango de precios de cada local.
6. Añadir un `<h1>` real a la home (por ejemplo "Cevichería Señor Limón — Lima").
7. Actualizar la carta PDF a 2026 (y comprimirla bien, no "comprimida" como la de 2020).

**Ronda 3 — rendimiento y contenido**
8. Consolidar/minificar CSS y JS, cargar los scripts de forma diferida y quitar lo que no se use (revisar si Revolution Slider aporta algo hoy).
9. Desduplicar los testimonios en el HTML.
10. Actualizar "Nosotros" y decidir qué hacer con el blog (reactivarlo o retirarlo del menú).

---

## 5. Anexo — archivos de evidencia

Los archivos descargados durante el análisis están en `_review/`:
- `home.html` — HTML fuente de la portada (87 KB)
- `contact.html` — HTML fuente de la página de locales
- `sitemap.xml` — índice de sitemaps de WordPress
- `pages.xml` — inventario de las 14 páginas con fechas de modificación

---

# Anexo — Hallazgos adicionales detectados al reconstruir el sitio

Estos problemas aparecieron al extraer el contenido de las 14 páginas para construir la web nueva. Complementan los del informe anterior.

## 🔴 Enlaces del menú que llevan a páginas que no existen

El menú del sitio actual tiene cuatro enlaces rotos. Verificado con peticiones directas, todos devuelven `404`:

| Enlace del menú | URL | Estado |
|---|---|---|
| Acompañamientos | `/acompanamientos` | `404` |
| Combinados | `/combinados` | `404` |
| Tiraditos | `/tiraditos` | `404` |
| Promociones (segundo enlace) | `/promo` | `404` |

Los platos de "Combinados" y "Tiraditos" sí existen, pero están dentro de la página de Cebiches. "Promociones" apunta en cambio a `/leche-de-tigre`, que sí funciona. La web nueva elimina estos enlaces y deja esas secciones dentro de la carta, donde el contenido realmente está.

## 🔴 La carta de postres y bebidas no tiene carta

`/postres-y-bebidas/` no muestra ningún plato: la página contiene el texto institucional ("Gastronomía Peruana", "¿Te imaginas un Cebiche sin LIMÓN?", "Nuestros ORiGENES"), el mismo bloque que aparece en la página "Nosotros". Es decir, **el contenido de esa sección se perdió** en algún momento.

En la web nueva esa categoría no se incluye porque no hay datos reales que publicar. Necesitamos que nos pases la carta de postres y bebidas para añadirla (es un archivo de datos, se agrega en minutos).

## 🟠 Imágenes fuera de lugar en la carta

Tres platos tenían como foto la imagen de **tarjetas de pago** del pie de página, porque en el HTML original aparecían sin foto propia y el maquetado les asignaba la siguiente imagen del documento:

- Trucha a la parrilla
- Tacu tacu con lomo saltado
- Parrilla marina

Estos tres ya no muestran foto incorrecta. Además, la misma imagen de tarjetas se estaba cargando una vez por página desde una URL `http://` en un sitio `https://`.

## 🟡 Icono de Facebook que lleva a Instagram

En el pie de página, el icono de Facebook apunta a `instagram.com/senorlimonoficial`. En el sitio nuevo solo se enlazan Instagram y YouTube, que son las cuentas que realmente existen.

## 🟡 Carta en PDF de 2020 enlazada en todas las páginas

El enlace de descarga apunta a `Senor-Limon-2020-comprimido1.pdf`, seis años por detrás de los precios publicados en la web. Es preferible retirarlo o reemplazarlo por un PDF actualizado; un cliente que lo descargue ve precios equivocados.

## 🟡 Los horarios existen, pero solo dentro de imágenes

No hay ningún horario como texto en el sitio. Sin embargo, al abrir las fichas de cada local (`LOCALES-01` a `LOCALES-08`, que son imágenes) sí aparece: **todos los locales atienden de 12:00 a 5:30 p.m.**

El problema es que, al estar dentro de una imagen, Google no puede leerlo, no se puede buscar en la página y un cliente con mala conexión ni lo ve. En la web nueva ese horario ya es texto en cada tarjeta de local, en la franja superior, en el pie de todas las páginas y en la página de contacto.

Las mismas fichas incluyen las **zonas de reparto de cada local** (por ejemplo, en San Isidro: San Isidro, Parque El Olivar, Surquillo, Salaverry, Jesús María, Pueblo Libre y Lince), que tampoco eran visibles para los buscadores. Ya están publicadas como texto en cada tarjeta.

## 🟡 Claves de API de Google Maps expuestas en el código

El HTML servido al navegador incluye dos claves de Google Maps:

- Una en la URL de mapas estáticas de la página de restaurantes
- Otra en el script del mapa (`maps.googleapis.com/maps/api/js?key=…`)

Es habitual en mapas de Google, pero conviene revisar en la consola de Google Cloud que estén restringidas por dominio. Si no lo están, cualquiera puede usarlas y consumir la cuota de la cuenta.

## 🟡 Dos platos con descripción equivocada o duplicada

- **Clásico de cebiches**: tenía la misma descripción que "Cebiche de conchas negras" (texto copiado de otro plato).
- **Charela a la plancha**: tenía la descripción del filete de trucha al ajo.

En el sitio nuevo se dejaron sin descripción en lugar de publicar un texto incorrecto. Hay que redactarlas.

También hay dos pares de platos que comparten descripción literal en el original (Jalea mixta / Jalea mixta Señor Limón y Cabrilla entera frita / Chita entera frita). Se mantuvieron tal cual están en el sitio actual.

## Lo que la web nueva ya resuelve

- Imágenes optimizadas a WebP: las fotos de platos pasan de **36.51 MB a 6.98 MB** y la foto principal de **8.1 MB a 225 KB**.
- Las 8 imágenes de locales (11.27 MB en PNG) se sustituyen por tarjetas con dirección, teléfono y enlace a Google Maps.
- `meta description`, Open Graph, Twitter Cards y datos estructurados `Restaurant` con los 8 locales en JSON-LD.
- Un `<h1>` real por página.
- Sin las 22 hojas de estilo ni los 54 scripts del tema anterior: ahora son **1 CSS y 2 JS**.
- Los cuatro enlaces rotos del menú desaparecen.
- Navegación con menú móvil, buscador de platos y filtros por sección.
