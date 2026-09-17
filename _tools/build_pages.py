# -*- coding: utf-8 -*-
"""Genera locales.html, nosotros.html y contacto.html con cabecera y pie unicos"""
import io, os

RAIZ = r"C:\Users\leonn\Documents\web\senorlimon"

CABECERA = """
<header class="cabecera">
  <div class="contenedor cabecera__interior">
    <a class="cabecera__logo" href="index.html" aria-label="Señor Limón, ir al inicio">
      <img src="assets/img/logo.webp" alt="Señor Limón" width="560" height="126">
    </a>
    <nav class="nav" aria-label="Navegación principal">
      <a class="nav__enlace" href="index.html"{A_INICIO}>Inicio</a>
      <a class="nav__enlace" href="carta.html"{A_CARTA}>Carta</a>
      <a class="nav__enlace" href="locales.html"{A_LOCALES}>Locales</a>
      <a class="nav__enlace" href="nosotros.html"{A_NOSOTROS}>Nosotros</a>
      <a class="nav__enlace" href="contacto.html"{A_CONTACTO}>Contacto</a>
    </nav>
    <div class="cabecera__acciones">
      <a class="boton boton--whatsapp boton--sm" data-whatsapp href="#" target="_blank" rel="noopener">Pedir ahora</a>
      <button class="boton-menu" type="button" aria-expanded="false" aria-controls="nav-movil" aria-label="Abrir menú">
        <span></span>
      </button>
    </div>
  </div>
</header>

<div class="nav-movil" id="nav-movil" aria-hidden="true">
  <a href="index.html"{A_INICIO}>Inicio</a>
  <a href="carta.html"{A_CARTA}>Carta</a>
  <a href="locales.html"{A_LOCALES}>Locales</a>
  <a href="nosotros.html"{A_NOSOTROS}>Nosotros</a>
  <a href="contacto.html"{A_CONTACTO}>Contacto</a>
  <a class="boton boton--whatsapp boton--bloque" data-whatsapp href="#" target="_blank" rel="noopener">Pedir por WhatsApp</a>
</div>
"""

PIE = """
<footer class="pie">
  <div class="contenedor">
    <div class="pie__rejilla">
      <div class="pie__marca">
        <img src="assets/img/marca.webp" alt="Señor Limón" width="512" height="512">
        <p>Cevichería y cocina marina peruana desde 2001. Cebiches, tiraditos, leche de tigre y piqueos en ocho locales de Lima.</p>
        <div class="pie__redes">
          <a class="pie__red" href="https://www.instagram.com/senorlimonoficial/" target="_blank" rel="noopener" aria-label="Instagram de Señor Limón">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor" stroke="none"/></svg>
          </a>
          <a class="pie__red" href="https://www.youtube.com/channel/UCTr-tHlAeg0u5ptyzKB5sug/videos" target="_blank" rel="noopener" aria-label="YouTube de Señor Limón">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M23 12s0-3.5-.4-5.2a2.6 2.6 0 0 0-1.8-1.9C19.1 4.5 12 4.5 12 4.5s-7.1 0-8.8.4A2.6 2.6 0 0 0 1.4 6.8C1 8.5 1 12 1 12s0 3.5.4 5.2a2.6 2.6 0 0 0 1.8 1.9c1.7.4 8.8.4 8.8.4s7.1 0 8.8-.4a2.6 2.6 0 0 0 1.8-1.9C23 15.5 23 12 23 12zM9.8 15.3V8.7l5.7 3.3-5.7 3.3z"/></svg>
          </a>
        </div>
      </div>
      <div>
        <h4>La carta</h4>
        <ul class="pie__lista">
          <li><a href="carta.html#cebiches">Cebiches y tiraditos</a></li>
          <li><a href="carta.html#piqueos">Piqueos</a></li>
          <li><a href="carta.html#leche-de-tigre">Leche de tigre</a></li>
          <li><a href="carta.html#sopas-y-sudados">Sopas y sudados</a></li>
          <li><a href="carta.html#pescados-enteros">Pescados enteros</a></li>
          <li><a href="carta.html#pastas-y-risottos">Pastas y risottos</a></li>
          <li><a href="carta.html#cervezas-y-gaseosas">Cervezas y gaseosas</a></li>
        </ul>
      </div>
      <div>
        <h4>Pedidos por teléfono</h4>
        <ul class="pie__lista" id="locales-pie"></ul>
      </div>
      <div>
        <h4>Pide y síguenos</h4>
        <p style="font-size:.92rem">Delivery gratis hasta 3.5 km. Aceptamos reservas y pedidos para llevar.</p>
        <p style="font-size:.92rem;margin-top:8px">Horario de atención: <span data-horario>12:00 a 5:30 p.m.</span></p>
        <div class="grupo-botones" style="margin-top:16px">
          <a class="boton boton--whatsapp boton--sm" data-whatsapp href="#" target="_blank" rel="noopener">WhatsApp</a>
          <a class="boton boton--borde boton--sm" style="color:#fff;border-color:rgba(255,255,255,.4)" href="contacto.html">Contacto</a>
        </div>
        <img class="pie__tarjetas" src="assets/img/tarjetas.webp" alt="Medios de pago aceptados" width="320" height="47" loading="lazy">
      </div>
    </div>
    <div class="pie__legal">
      <span>© <span data-anio>2026</span> Señor Limón. Todos los derechos reservados.</span>
      <span>Lima, Perú · Cevichería y cocina marina</span>
    </div>
  </div>
</footer>

<a class="boton-flotante" data-whatsapp href="#" target="_blank" rel="noopener" aria-label="Pedir por WhatsApp">
  <svg width="22" height="22" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a10 10 0 0 0-8.5 15.2L2 22l4.9-1.4A10 10 0 1 0 12 2zm5.6 14.2c-.2.7-1.4 1.3-2 1.4-.5.1-1.2.1-1.9-.1-.4-.1-1-.3-1.8-.6-3.1-1.3-5.1-4.4-5.3-4.6-.1-.2-1.2-1.6-1.2-3 0-1.4.7-2.1 1-2.4.2-.3.5-.4.7-.4h.5c.2 0 .4 0 .6.5l.8 2c.1.2.1.4 0 .5l-.3.5-.4.4c-.1.1-.3.3-.1.6.2.3.8 1.3 1.7 2.1 1.2 1 2.1 1.4 2.4 1.5.3.1.5.1.7-.1l.9-1c.2-.3.4-.2.6-.1l2 1c.3.1.5.2.5.3.1.1.1.6-.1 1.3z"/></svg>
  <span>Pedir por WhatsApp</span>
</a>
<button class="boton-subir" type="button" aria-label="Volver arriba">
  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 19V5M6 11l6-6 6 6"/></svg>
</button>
"""

PLANTILLA = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{TITULO}</title>
<meta name="description" content="{DESCRIPCION}">
<link rel="canonical" href="https://senorlimon.com/{ARCHIVO}">
<meta name="theme-color" content="#0e3a4c">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Señor Limón">
<meta property="og:locale" content="es_PE">
<meta property="og:title" content="{OG_TITULO}">
<meta property="og:description" content="{OG_DESC}">
<meta property="og:image" content="https://senorlimon.com/assets/img/hero-cebiche.webp">
<meta property="og:url" content="https://senorlimon.com/{ARCHIVO}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/png" href="assets/img/favicon.png">
<link rel="apple-touch-icon" href="assets/img/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Outfit:wght@600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/styles.css">
{EXTRA_HEAD}
</head>
<body>
<a class="saltar-a-contenido" href="#contenido">Saltar al contenido</a>
{CABECERA}
<main id="contenido">
{CONTENIDO}
</main>
{PIE}
<script src="assets/js/data.js"></script>
<script src="assets/js/app.js"></script>
<script src="assets/js/panel.js"></script>
</body>
</html>
"""

# ---------------------------------------------------------------- locales
LOCALES_JSONLD = """<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Restaurant",
  "name": "Señor Limón",
  "url": "https://senorlimon.com/",
  "image": "https://senorlimon.com/assets/img/hero-cebiche.webp",
  "servesCuisine": ["Peruana", "Marina", "Cevichería"],
  "department": [
    {"@type": "Restaurant", "name": "Señor Limón La Molina", "telephone": "+5116806332", "address": {"@type": "PostalAddress", "streetAddress": "Av. Constructores 958", "addressLocality": "La Molina", "addressRegion": "Lima", "addressCountry": "PE"}},
    {"@type": "Restaurant", "name": "Señor Limón Javier Prado", "telephone": "+5117155320", "address": {"@type": "PostalAddress", "streetAddress": "Av. Javier Prado Este 5335", "addressLocality": "La Molina", "addressRegion": "Lima", "addressCountry": "PE"}},
    {"@type": "Restaurant", "name": "Señor Limón Prescott 415", "telephone": "+5117156340", "address": {"@type": "PostalAddress", "streetAddress": "Av. Guillermo Prescott 415", "addressLocality": "San Isidro", "addressRegion": "Lima", "addressCountry": "PE"}},
    {"@type": "Restaurant", "name": "Señor Limón Prescott 370", "telephone": "+5116805373", "address": {"@type": "PostalAddress", "streetAddress": "Av. Guillermo Prescott 370", "addressLocality": "San Isidro", "addressRegion": "Lima", "addressCountry": "PE"}},
    {"@type": "Restaurant", "name": "Señor Limón Conquistadores", "telephone": "+5112218327", "address": {"@type": "PostalAddress", "streetAddress": "Av. Conquistadores 299", "addressLocality": "San Isidro", "addressRegion": "Lima", "addressCountry": "PE"}},
    {"@type": "Restaurant", "name": "Señor Limón Universitaria", "telephone": "+5117139914", "address": {"@type": "PostalAddress", "streetAddress": "Av. Universitaria 722", "addressLocality": "San Miguel", "addressRegion": "Lima", "addressCountry": "PE"}},
    {"@type": "Restaurant", "name": "Señor Limón La Mar", "telephone": "+5117155418", "address": {"@type": "PostalAddress", "streetAddress": "Av. La Mar 2311", "addressLocality": "San Miguel", "addressRegion": "Lima", "addressCountry": "PE"}},
    {"@type": "Restaurant", "name": "Señor Limón Naciones Unidas", "telephone": "+5116805554", "address": {"@type": "PostalAddress", "streetAddress": "Av. Naciones Unidas 1160", "addressLocality": "Cercado de Lima", "addressRegion": "Lima", "addressCountry": "PE"}}
  ]
}
</script>"""

CONTENIDO_LOCALES = """
  <section class="seccion--ajustada fondo-azul">
    <div class="contenedor">
      <p class="antetitulo">Restaurantes</p>
      <h1 style="font-size:clamp(1.9rem,5vw,3.1rem)">Nuestros locales en Lima</h1>
      <p class="entradilla" style="max-width:640px">Ocho locales en La Molina, San Isidro, San Miguel y Cercado de Lima. Todos atienden de <strong>12:00 a 5:30 p.m.</strong> Llama al local más cercano o escríbenos por WhatsApp.</p>
    </div>
  </section>

  <div class="franja">
    <div class="contenedor franja__interior">
      <span class="franja__item"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="6" cy="17" r="3"/><circle cx="18" cy="17" r="3"/><path d="M9 17h6l-3-8H7l2 8zM14 9h3l2 5"/></svg> Delivery gratis hasta 3.5 km</span>
      <span class="franja__item"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg> Abierto de <span data-horario>12:00 a 5:30 p.m.</span></span>
      <span class="franja__item">Aceptamos reservas y pedidos para llevar</span>
      <span class="franja__item"><a href="carta.html" style="text-decoration:underline">Ver la carta</a></span>
    </div>
  </div>

  <section class="seccion">
    <div class="contenedor">
      <div class="encabezado-seccion aparecer">
        <p class="antetitulo">Direcciones y teléfonos</p>
        <h2>Elige tu local</h2>
        <p class="entradilla">Los pedidos se toman por teléfono o WhatsApp. El local de Av. La Mar 2311 en San Miguel atiende además por WhatsApp.</p>
      </div>
      <div class="rejilla rejilla--locales" id="lista-locales"></div>
    </div>
  </section>

  <section class="seccion fondo-blanco">
    <div class="contenedor">
      <div class="bloque-historia">
        <div class="bloque-historia__texto aparecer">
          <p class="antetitulo">Cómo llegar</p>
          <h2>Estamos donde te queda más fácil</h2>
          <p class="entradilla">Cada tarjeta de local tiene un botón «Cómo llegar» que abre la ubicación exacta en Google Maps. Si prefieres, llámanos y te guiamos.</p>
          <ul class="lista-rasgos" style="margin-top:24px">
            <li><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6L9 17l-5-5"/></svg><span><strong>Zona corporativa</strong> Tres locales en San Isidro, ideales para el almuerzo de oficina.</span></li>
            <li><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6L9 17l-5-5"/></svg><span><strong>Zona residencial</strong> La Molina y San Miguel, con opción de delivery a domicilio.</span></li>
            <li><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6L9 17l-5-5"/></svg><span><strong>Delivery propio</strong> Repartimos sin costo dentro del radio de 3.5 km de cada local.</span></li>
          </ul>
        </div>
        <div class="bloque-historia__foto aparecer">
          <img src="assets/img/plato-restaurante-en-lima.webp" alt="Plato de Señor Limón servido en el restaurante" width="900" height="900" loading="lazy">
        </div>
      </div>
    </div>
  </section>

  <section class="seccion--ajustada">
    <div class="contenedor">
      <div class="llamada aparecer">
        <div class="llamada__interior">
          <div>
            <h2 style="font-size:clamp(1.4rem,3vw,2rem)">¿Te llevamos el pedido a casa?</h2>
            <p class="entradilla">Escríbenos por WhatsApp con tu dirección y te confirmamos si estás dentro del radio de delivery gratis.</p>
          </div>
          <div class="grupo-botones">
            <a class="boton boton--principal" data-whatsapp href="#" target="_blank" rel="noopener">Pedir por WhatsApp</a>
            <a class="boton boton--claro" href="contacto.html">Contacto</a>
          </div>
        </div>
      </div>
    </div>
  </section>
"""

# ---------------------------------------------------------------- nosotros
CONTENIDO_NOSOTROS = """
  <section class="seccion--ajustada fondo-azul">
    <div class="contenedor">
      <p class="antetitulo">Nosotros</p>
      <h1 style="font-size:clamp(1.9rem,5vw,3.1rem)">Veinticinco años de sabor peruano</h1>
      <p class="entradilla" style="max-width:640px">Nacimos en San Miguel el 1 de diciembre de 2001 con una idea simple: cocinar el mar peruano sin apuros y con insumos de verdad.</p>
    </div>
  </section>

  <section class="seccion">
    <div class="contenedor">
      <div style="max-width:760px;margin-inline:auto" id="historia-contenido"></div>
    </div>
  </section>

  <section class="seccion fondo-blanco">
    <div class="contenedor">
      <div class="encabezado-seccion encabezado-seccion--centrado aparecer">
        <p class="antetitulo">Nuestra cocina</p>
        <h2>Lo que nos identifica</h2>
      </div>
      <div class="rejilla rejilla--3">
        <article class="tarjeta-testimonio aparecer">
          <div class="dato-contacto__icono"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3l2 5 5 .7-3.7 3.4.9 4.9-4.2-2.3-4.2 2.3.9-4.9L4.8 8.7 9.8 8z"/></svg></div>
          <h3>Pesca del día</h3>
          <p>Elegimos el pescado cada mañana. Por eso algunos platos dependen de lo que llegue del mar: la carta se ajusta a la pesca.</p>
        </article>
        <article class="tarjeta-testimonio aparecer">
          <div class="dato-contacto__icono"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M8 14c1.5 1.6 5.5 1.6 8-2"/></svg></div>
          <h3>Limón sutil peruano</h3>
          <p>El limón peruano es el único capaz de darle a nuestro cebiche su cocción y su sabor. Es el insumo que da nombre a la casa.</p>
        </article>
        <article class="tarjeta-testimonio aparecer">
          <div class="dato-contacto__icono"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg></div>
          <h3>Ocho locales</h3>
          <p>Crecimos de un local en San Miguel a ocho restaurantes en Lima, manteniendo la misma cocina y el mismo trato.</p>
        </article>
      </div>
    </div>
  </section>

  <section class="seccion">
    <div class="contenedor">
      <div class="encabezado-seccion encabezado-seccion--centrado aparecer">
        <p class="antetitulo">Nuestra carta en fotos</p>
        <h2>Platos que hablan por nosotros</h2>
      </div>
      <div class="rejilla rejilla--4">
        <article class="tarjeta-plato aparecer"><div class="tarjeta-plato__foto"><img src="assets/img/plato-ceviche-mixto.webp" alt="Cebiche mixto" loading="lazy" width="900" height="675"></div><div class="tarjeta-plato__cuerpo"><h3>Cebiche mixto</h3><p>Pescado del día con mixtura de mariscos.</p></div></article>
        <article class="tarjeta-plato aparecer"><div class="tarjeta-plato__foto"><img src="assets/img/plato-causa-de-pulpa-de-cangrejo.webp" alt="Causa con pulpa de cangrejo" loading="lazy" width="900" height="675"></div><div class="tarjeta-plato__cuerpo"><h3>Causa con pulpa de cangrejo</h3><p>Papa amarilla, crema de ají amarillo y cangrejo.</p></div></article>
        <article class="tarjeta-plato aparecer"><div class="tarjeta-plato__foto"><img src="assets/img/plato-parihuela-restaurante.webp" alt="Parihuela" loading="lazy" width="900" height="675"></div><div class="tarjeta-plato__cuerpo"><h3>Parihuela</h3><p>Sopa contundente de mariscos y cangrejo.</p></div></article>
        <article class="tarjeta-plato aparecer"><div class="tarjeta-plato__foto"><img src="assets/img/plato-quiero-maki-acevichado.webp" alt="Maki acevichado" loading="lazy" width="900" height="675"></div><div class="tarjeta-plato__cuerpo"><h3>Maki acevichado</h3><p>Diez cortes con langostino, palta y atún.</p></div></article>
      </div>
      <div class="grupo-botones" style="justify-content:center;margin-top:34px">
        <a class="boton boton--oscuro" href="carta.html">Ver la carta completa</a>
      </div>
    </div>
  </section>

  <section class="seccion--ajustada">
    <div class="contenedor">
      <div class="llamada aparecer">
        <div class="llamada__interior">
          <div>
            <h2 style="font-size:clamp(1.4rem,3vw,2rem)">Ven a probarlo en persona</h2>
            <p class="entradilla">Ocho locales en Lima y delivery gratis hasta 3.5 km. Te esperamos.</p>
          </div>
          <div class="grupo-botones">
            <a class="boton boton--principal" href="locales.html">Ver locales</a>
            <a class="boton boton--claro" data-whatsapp href="#" target="_blank" rel="noopener">Pedir por WhatsApp</a>
          </div>
        </div>
      </div>
    </div>
  </section>
"""

# ---------------------------------------------------------------- contacto
CONTENIDO_CONTACTO = """
  <section class="seccion--ajustada fondo-azul">
    <div class="contenedor">
      <p class="antetitulo">Contacto</p>
      <h1 style="font-size:clamp(1.9rem,5vw,3.1rem)">Hablemos de tu pedido</h1>
      <p class="entradilla" style="max-width:640px">Escríbenos por WhatsApp, llámanos a tu local más cercano o déjanos tu mensaje en el formulario.</p>
    </div>
  </section>

  <section class="seccion">
    <div class="contenedor">
      <div class="bloque-historia" style="align-items:start">
        <div class="aparecer">
          <div class="encabezado-seccion" style="margin-bottom:22px">
            <p class="antetitulo">Formulario</p>
            <h2 style="font-size:clamp(1.4rem,3vw,1.9rem)">Cuéntanos qué necesitas</h2>
            <p class="entradilla">Al enviar, se abre WhatsApp con tu mensaje ya escrito. Solo tienes que pulsar enviar.</p>
          </div>
          <form class="formulario" id="formulario-contacto" novalidate>
            <div class="formulario__fila formulario__fila--2">
              <div class="campo">
                <label for="nombre">Nombre</label>
                <input type="text" id="nombre" name="nombre" placeholder="Tu nombre" autocomplete="name" required>
                <p class="campo__error">Escribe tu nombre (mínimo 3 letras).</p>
              </div>
              <div class="campo">
                <label for="telefono">Teléfono</label>
                <input type="tel" id="telefono" name="telefono" placeholder="999 999 999" autocomplete="tel" required>
                <p class="campo__error">Escribe un teléfono válido para contactarte.</p>
              </div>
            </div>
            <div class="formulario__fila formulario__fila--2">
              <div class="campo">
                <label for="campo-distrito">Local o zona</label>
                <select id="campo-distrito" name="distrito" required>
                  <option value="">Elige un local…</option>
                </select>
                <p class="campo__error">Elige el local o zona de entrega.</p>
              </div>
              <div class="campo">
                <label for="motivo">Motivo</label>
                <select id="motivo" name="motivo">
                  <option value="Pedido para llevar">Pedido para llevar</option>
                  <option value="Delivery a domicilio">Delivery a domicilio</option>
                  <option value="Reserva de mesa">Reserva de mesa</option>
                  <option value="Consulta general">Consulta general</option>
                </select>
              </div>
            </div>
            <div class="campo">
              <label for="mensaje">Mensaje</label>
              <textarea id="mensaje" name="mensaje" placeholder="Cuéntanos qué quieres pedir, para cuántas personas y a qué hora." required></textarea>
              <p class="campo__error">Escribe un mensaje de al menos 10 caracteres.</p>
            </div>
            <p class="formulario__aviso" id="aviso-formulario" role="status" aria-live="polite"></p>
            <div class="grupo-botones">
              <button class="boton boton--whatsapp" type="submit">Enviar por WhatsApp</button>
            </div>
            <p class="formulario__nota">No guardamos tus datos en este sitio: el mensaje se envía directamente por WhatsApp.</p>
          </form>
        </div>

        <div class="datos-contacto aparecer">
          <div class="dato-contacto">
            <div class="dato-contacto__icono"><svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a10 10 0 0 0-8.5 15.2L2 22l4.9-1.4A10 10 0 1 0 12 2zm5.6 14.2c-.2.7-1.4 1.3-2 1.4-.5.1-1.2.1-1.9-.1-.4-.1-1-.3-1.8-.6-3.1-1.3-5.1-4.4-5.3-4.6-.1-.2-1.2-1.6-1.2-3 0-1.4.7-2.1 1-2.4.2-.3.5-.4.7-.4h.5c.2 0 .4 0 .6.5l.8 2c.1.2.1.4 0 .5l-.3.5-.4.4c-.1.1-.3.3-.1.6.2.3.8 1.3 1.7 2.1 1.2 1 2.1 1.4 2.4 1.5.3.1.5.1.7-.1l.9-1c.2-.3.4-.2.6-.1l2 1c.3.1.5.2.5.3.1.1.1.6-.1 1.3z"/></svg></div>
            <div>
              <strong>WhatsApp de pedidos</strong>
              <a data-whatsapp href="#" target="_blank" rel="noopener">Abrir conversación</a>
              <p style="font-size:.9rem;color:var(--gris-500)">Atención en horario de tienda de cada local.</p>
            </div>
          </div>
          <div class="dato-contacto">
            <div class="dato-contacto__icono"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg></div>
            <div>
              <strong>Nuestros ocho locales</strong>
              <ul class="pie__lista" id="locales-pie" style="margin-top:8px;color:inherit"></ul>
            </div>
          </div>
          <div class="dato-contacto">
            <div class="dato-contacto__icono"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="6" cy="17" r="3"/><circle cx="18" cy="17" r="3"/><path d="M9 17h6l-3-8H7l2 8zM14 9h3l2 5"/></svg></div>
            <div>
              <strong>Delivery gratis hasta 3.5 km</strong>
              <p style="font-size:.92rem;color:var(--gris-700)">Repartimos con servicio propio alrededor de cada local. Consúltanos si tu dirección entra en el radio.</p>
            </div>
          </div>
          <div class="dato-contacto">
            <div class="dato-contacto__icono"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg></div>
            <div>
              <strong>Horario de atención</strong>
              <p style="font-size:.92rem;color:var(--gris-700)">Todos los locales abren de <span data-horario>12:00 a 5:30 p.m.</span></p>
            </div>
          </div>
          <div class="dato-contacto">
            <div class="dato-contacto__icono"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor" stroke="none"/></svg></div>
            <div>
              <strong>Redes sociales</strong>
              <p style="font-size:.92rem"><a href="https://www.instagram.com/senorlimonoficial/" target="_blank" rel="noopener">Instagram @senorlimonoficial</a><br>
              <a href="https://www.youtube.com/channel/UCTr-tHlAeg0u5ptyzKB5sug/videos" target="_blank" rel="noopener">Canal de YouTube</a></p>
            </div>
          </div>
          <div class="dato-contacto">
            <div class="dato-contacto__icono"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="5" width="20" height="14" rx="2"/><path d="M2 10h20"/></svg></div>
            <div>
              <strong>Medios de pago</strong>
              <img src="assets/img/tarjetas.webp" alt="Tarjetas aceptadas en Señor Limón" width="320" height="47" loading="lazy" style="margin-top:8px">
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <section class="seccion--ajustada">
    <div class="contenedor">
      <div class="llamada aparecer">
        <div class="llamada__interior">
          <div>
            <h2 style="font-size:clamp(1.4rem,3vw,2rem)">¿Prefieres llamar?</h2>
            <p class="entradilla">Marca al local más cercano y toma tu pedido en minutos.</p>
          </div>
          <div class="grupo-botones">
            <a class="boton boton--principal" href="locales.html">Ver teléfonos</a>
            <a class="boton boton--claro" href="carta.html">Ver la carta</a>
          </div>
        </div>
      </div>
    </div>
  </section>
"""

PAGINAS = [
    {
        "archivo": "locales.html",
        "titulo": "Locales y delivery | Señor Limón — 8 restaurantes en Lima",
        "descripcion": "Direcciones, teléfonos y delivery de los 8 locales de Señor Limón en La Molina, San Isidro, San Miguel y Cercado de Lima. Delivery gratis hasta 3.5 km.",
        "og_titulo": "Locales y delivery | Señor Limón",
        "og_desc": "8 locales en Lima con delivery gratis hasta 3.5 km. Direcciones y teléfonos para pedir.",
        "extra_head": LOCALES_JSONLD,
        "contenido": CONTENIDO_LOCALES,
        "activo": "A_LOCALES",
    },
    {
        "archivo": "nosotros.html",
        "titulo": "Nosotros | Señor Limón — cevichería peruana desde 2001",
        "descripcion": "La historia de Señor Limón: del primer local en Av. La Mar 2311, San Miguel, en 2001, a ocho restaurantes de cocina marina peruana en Lima.",
        "og_titulo": "Nosotros | Señor Limón",
        "og_desc": "Nacimos en San Miguel en 2001. Hoy somos ocho locales de cocina marina peruana en Lima.",
        "extra_head": "",
        "contenido": CONTENIDO_NOSOTROS,
        "activo": "A_NOSOTROS",
    },
    {
        "archivo": "contacto.html",
        "titulo": "Contacto y pedidos | Señor Limón",
        "descripcion": "Pide por WhatsApp, llámanos o déjanos tu mensaje. Pedidos para llevar, delivery y reservas en los 8 locales de Señor Limón en Lima.",
        "og_titulo": "Contacto y pedidos | Señor Limón",
        "og_desc": "Pide por WhatsApp o teléfono. Delivery gratis hasta 3.5 km y reservas de mesa.",
        "extra_head": "",
        "contenido": CONTENIDO_CONTACTO,
        "activo": "A_CONTACTO",
    },
]

for pag in PAGINAS:
    cabecera = CABECERA
    for clave in ("A_INICIO", "A_CARTA", "A_LOCALES", "A_NOSOTROS", "A_CONTACTO"):
        cabecera = cabecera.replace("{" + clave + "}",
                                    ' aria-current="page"' if clave == pag["activo"] else "")
    html = (PLANTILLA
            .replace("{TITULO}", pag["titulo"])
            .replace("{DESCRIPCION}", pag["descripcion"])
            .replace("{OG_TITULO}", pag["og_titulo"])
            .replace("{OG_DESC}", pag["og_desc"])
            .replace("{ARCHIVO}", pag["archivo"])
            .replace("{EXTRA_HEAD}", pag["extra_head"])
            .replace("{CABECERA}", cabecera)
            .replace("{CONTENIDO}", pag["contenido"])
            .replace("{PIE}", PIE))
    destino = os.path.join(RAIZ, pag["archivo"])
    io.open(destino, "w", encoding="utf-8").write(html)
    print("%-16s %6.1f KB" % (pag["archivo"], os.path.getsize(destino) / 1024))
