/* ==========================================================================
   Señor Limón — comportamiento del sitio
   Funciona sin dependencias y sin peticiones de red: los datos viven en
   assets/js/data.js, así que el sitio abre igual desde file:// o desde un
   servidor.
   ========================================================================== */
(function () {
  'use strict';

  var D = window.SL_DATA || {};
  var marca = D.marca || {};
  var categorias = D.categorias || [];
  var locales = D.locales || [];

  /* ---------- utilidades ------------------------------------------------- */
  function $(sel, ctx) { return (ctx || document).querySelector(sel); }
  function $$(sel, ctx) { return Array.prototype.slice.call((ctx || document).querySelectorAll(sel)); }

  function normalizar(txt) {
    return (txt || '').toString().toLowerCase()
      .normalize('NFD').replace(/[\u0300-\u036f]/g, '');
  }

  function precio(valor) {
    if (valor === null || valor === undefined) { return 'Consultar'; }
    return 'S/ ' + (Number.isInteger(valor) ? valor : valor.toFixed(2));
  }

  function telHref(local) {
    return 'tel:+511' + (local.tel || local.telefono || '');
  }

  function tarjetaHref(direccion, distrito) {
    return 'https://www.google.com/maps/search/?api=1&query=' +
      encodeURIComponent(direccion + ', ' + distrito + ', Lima, Perú');
  }

  function waHref(mensaje) {
    var num = (marca.whatsapp || '').replace(/\D/g, '');
    return 'https://wa.me/' + num + (mensaje ? '?text=' + encodeURIComponent(mensaje) : '');
  }

  function escapar(txt) {
    return (txt || '').toString()
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  var ICONOS = {
    pin: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>',
    telefono: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.3-1.2a2 2 0 0 1 2.1-.5c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/></svg>',
    whatsapp: '<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a10 10 0 0 0-8.5 15.2L2 22l4.9-1.4A10 10 0 1 0 12 2zm5.6 14.2c-.2.7-1.4 1.3-2 1.4-.5.1-1.2.1-1.9-.1-.4-.1-1-.3-1.8-.6-3.1-1.3-5.1-4.4-5.3-4.6-.1-.2-1.2-1.6-1.2-3 0-1.4.7-2.1 1-2.4.2-.3.5-.4.7-.4h.5c.2 0 .4 0 .6.5l.8 2c.1.2.1.4 0 .5l-.3.5-.4.4c-.1.1-.3.3-.1.6.2.3.8 1.3 1.7 2.1 1.2 1 2.1 1.4 2.4 1.5.3.1.5.1.7-.1l.9-1c.2-.3.4-.2.6-.1l2 1c.3.1.5.2.5.3.1.1.1.6-.1 1.3z"/></svg>',
    flecha: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
    flechaIzq: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 12H5M11 6l-6 6 6 6"/></svg>',
    estrella: '<svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2l2.9 6.3 6.9.8-5.1 4.7 1.4 6.8L12 17.2 5.9 20.6l1.4-6.8L2.2 9.1l6.9-.8z"/></svg>',
    check: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6L9 17l-5-5"/></svg>',
    reloj: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>',
    moto: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="6" cy="17" r="3"/><circle cx="18" cy="17" r="3"/><path d="M9 17h6l-3-8H7l2 8zM14 9h3l2 5"/></svg>',
    busqueda: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/></svg>',
    cerrar: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"><path d="M6 6l12 12M18 6L6 18"/></svg>',
    arriba: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 19V5M6 11l6-6 6 6"/></svg>',
    info: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M12 11v5M12 8h.01"/></svg>',
    ig: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor" stroke="none"/></svg>',
    yt: '<svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M23 12s0-3.5-.4-5.2a2.6 2.6 0 0 0-1.8-1.9C19.1 4.5 12 4.5 12 4.5s-7.1 0-8.8.4A2.6 2.6 0 0 0 1.4 6.8C1 8.5 1 12 1 12s0 3.5.4 5.2a2.6 2.6 0 0 0 1.8 1.9c1.7.4 8.8.4 8.8.4s7.1 0 8.8-.4a2.6 2.6 0 0 0 1.8-1.9C23 15.5 23 12 23 12zM9.8 15.3V8.7l5.7 3.3-5.7 3.3z"/></svg>'
  };

  /* ---------- cabecera, menú móvil y detalles globales ------------------- */
  function iniciarCabecera() {
    var cabecera = $('.cabecera');
    var boton = $('.boton-menu');
    var panel = $('#nav-movil');
    var subir = $('.boton-subir');

    if (boton && panel) {
      boton.addEventListener('click', function () {
        // el menú móvil necesita la cabecera a la vista
        document.body.classList.remove('cabecera-oculta');
        var abierto = panel.classList.toggle('es-abierto');
        boton.setAttribute('aria-expanded', abierto ? 'true' : 'false');
        panel.setAttribute('aria-hidden', abierto ? 'false' : 'true');
      });
      $$('a', panel).forEach(function (a) {
        a.addEventListener('click', function () {
          panel.classList.remove('es-abierto');
          boton.setAttribute('aria-expanded', 'false');
        });
      });
    }

    var ultimoY = 0;
    function alDesplazar() {
      var y = window.scrollY || window.pageYOffset;
      if (cabecera) { cabecera.classList.toggle('es-fija', y > 20); }
      if (subir) { subir.classList.toggle('es-visible', y > 620); }
      // la cabecera se aparta al bajar y vuelve al subir: así se ve más contenido
      if (y > ultimoY + 4 && y > 340) {
        document.body.classList.add('cabecera-oculta');
      } else if (y < ultimoY - 4 || y < 340) {
        document.body.classList.remove('cabecera-oculta');
      }
      ultimoY = y;
    }
    window.addEventListener('scroll', alDesplazar, { passive: true });
    alDesplazar();

    if (subir) {
      subir.addEventListener('click', function () {
        window.scrollTo({ top: 0, behavior: 'smooth' });
      });
    }
  }

  function iniciarAnimaciones() {
    var elementos = $$('.aparecer');
    if (!elementos.length) { return; }
    if (!('IntersectionObserver' in window)) {
      elementos.forEach(function (el) { el.classList.add('es-visible'); });
      return;
    }
    var observador = new IntersectionObserver(function (entradas) {
      entradas.forEach(function (e) {
        if (e.isIntersecting) {
          e.target.classList.add('es-visible');
          observador.unobserve(e.target);
        }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: .08 });
    elementos.forEach(function (el) { observador.observe(el); });
  }

  /* ---------- enlaces de contacto --------------------------------------- */
  function iniciarContacto() {
    var wa = waHref('Hola, quisiera hacer un pedido a Señor Limón.');
    $$('[data-whatsapp]').forEach(function (a) { a.setAttribute('href', wa); });
    var anio = $('[data-anio]');
    if (anio) { anio.textContent = new Date().getFullYear(); }
    var horario = marca.horarios || '12:00 a 5:30 p.m.';
    $$('[data-horario]').forEach(function (el) { el.textContent = horario; });
    var tel = $('[data-telefono-central]');
    var local = locales.filter(function (l) { return l.distrito === 'La Molina'; })[0] || locales[0];
    if (tel && local) {
      tel.textContent = local.telefono;
      tel.setAttribute('href', telHref(local));
    }
  }

  /* ---------- modal de imágenes (mapas y fotos de la carta) -------------- */
  var modal = null;
  var galeria = [];
  var galeriaIndice = 0;

  function crearModal() {
    if (modal) { return modal; }
    modal = document.createElement('div');
    modal.className = 'modal';
    modal.id = 'sl-modal';
    modal.setAttribute('role', 'dialog');
    modal.setAttribute('aria-modal', 'true');
    modal.setAttribute('aria-hidden', 'true');
    modal.innerHTML =
      '<div class="modal__velo" data-modal="cerrar"></div>' +
      '<div class="modal__caja">' +
        '<div class="modal__marco">' +
          '<img id="sl-modal-img" alt="">' +
          '<button class="modal__flecha modal__flecha--antes" type="button" data-modal="antes" aria-label="Imagen anterior">' + ICONOS.flechaIzq + '</button>' +
          '<button class="modal__flecha modal__flecha--despues" type="button" data-modal="despues" aria-label="Imagen siguiente">' + ICONOS.flecha + '</button>' +
        '</div>' +
        '<button class="modal__cerrar" type="button" data-modal="cerrar" aria-label="Cerrar">' + ICONOS.cerrar + '</button>' +
        '<div class="modal__pie">' +
          '<p class="modal__texto"><strong id="sl-modal-titulo"></strong><span class="modal__contador" id="sl-modal-contador"></span></p>' +
          '<div class="modal__acciones" id="sl-modal-acciones"></div>' +
        '</div>' +
      '</div>';
    document.body.appendChild(modal);

    modal.addEventListener('click', function (e) {
      var boton = e.target.closest('[data-modal]');
      if (!boton) { return; }
      var accion = boton.getAttribute('data-modal');
      if (accion === 'cerrar') { cerrarModal(); }
      else if (accion === 'antes') { moverGaleria(-1); }
      else if (accion === 'despues') { moverGaleria(1); }
    });

    document.addEventListener('keydown', function (e) {
      if (!modal.classList.contains('es-abierto')) { return; }
      if (e.key === 'Escape') { cerrarModal(); }
      else if (e.key === 'ArrowLeft') { moverGaleria(-1); }
      else if (e.key === 'ArrowRight') { moverGaleria(1); }
    });
    return modal;
  }

  function pintarModal(dato) {
    var img = $('#sl-modal-img');
    img.setAttribute('src', dato.src);
    img.setAttribute('alt', dato.titulo || '');
    img.style.maxWidth = '';
    img.onload = function () {
      // la foto nunca se estira por encima de su resolución real
      img.style.maxWidth = Math.min(img.naturalWidth || 1120, 1120) + 'px';
    };
    $('#sl-modal-titulo').textContent = dato.titulo || '';
    $('#sl-modal-contador').textContent = galeria.length > 1
      ? (galeriaIndice + 1) + ' de ' + galeria.length + (dato.nota ? ' · ' + dato.nota : '')
      : (dato.nota || '');
    $('#sl-modal-acciones').innerHTML = dato.enlace
      ? '<a class="boton boton--principal boton--sm" href="' + escapar(dato.enlace) + '" target="_blank" rel="noopener">' + ICONOS.pin + ' Abrir en Google Maps</a>'
      : '';
  }

  function abrirModal(dato) {
    var caja = crearModal();
    galeria = dato.galeria || [];
    galeriaIndice = dato.indice || 0;
    caja.classList.toggle('con-galeria', galeria.length > 1);
    pintarModal(dato);
    caja.classList.add('es-abierto');
    caja.setAttribute('aria-hidden', 'false');
    document.body.classList.add('modal-abierto');
    var cerrar = $('.modal__cerrar', caja);
    if (cerrar) { cerrar.focus(); }
  }

  function moverGaleria(paso) {
    if (galeria.length < 2) { return; }
    galeriaIndice = (galeriaIndice + paso + galeria.length) % galeria.length;
    pintarModal(galeria[galeriaIndice]);
  }

  function cerrarModal() {
    if (!modal) { return; }
    modal.classList.remove('es-abierto');
    modal.setAttribute('aria-hidden', 'true');
    document.body.classList.remove('modal-abierto');
    var img = $('#sl-modal-img');
    if (img) { img.removeAttribute('src'); }
  }

  /* abre la galería de la carta empezando por la foto pulsada */
  function abrirFotoCarta(boton) {
    var fotos = $$('[data-foto]').filter(function (b) {
      var plato = b.closest('.plato');
      return !plato || plato.style.display !== 'none';
    });
    if (!fotos.length) { return; }
    var lista = fotos.map(function (b) {
      return {
        src: 'assets/img/' + b.getAttribute('data-foto'),
        titulo: b.getAttribute('data-titulo'),
        nota: b.getAttribute('data-nota')
      };
    });
    var i = fotos.indexOf(boton);
    if (i < 0) { i = 0; }
    abrirModal({ src: lista[i].src, titulo: lista[i].titulo, nota: lista[i].nota, galeria: lista, indice: i });
  }

  function iniciarModal() {
    document.addEventListener('click', function (e) {
      var mapa = e.target.closest('[data-mapa]');
      if (mapa) {
        abrirModal({
          src: 'assets/img/' + mapa.getAttribute('data-mapa'),
          titulo: mapa.getAttribute('data-titulo'),
          nota: mapa.getAttribute('data-nota'),
          enlace: mapa.getAttribute('data-enlace')
        });
        return;
      }
      var foto = e.target.closest('[data-foto]');
      if (foto) { abrirFotoCarta(foto); }
    });
  }

  /* ---------- render: locales ------------------------------------------- */
  function htmlLocal(l, conBotonMapa) {
    var destinos = tarjetaHref(l.direccion, l.distrito);
    var pie = '';
    pie += '<a class="boton boton--oscuro boton--sm" href="' + telHref(l) + '">' + ICONOS.telefono + ' Llamar</a>';
    if (l.whatsapp) {
      pie += '<a class="boton boton--whatsapp boton--sm" href="' + waHref('Hola, quisiera hacer un pedido al local de ' + l.direccion + '.') + '" target="_blank" rel="noopener">' + ICONOS.whatsapp + ' WhatsApp</a>';
    }
    if (conBotonMapa) {
      pie += '<a class="boton boton--borde boton--sm" href="' + destinos + '" target="_blank" rel="noopener">' + ICONOS.pin + ' Cómo llegar</a>';
    }

    // el mapa se amplía en un modal; el enlace a Google Maps va dentro del modal
    var mapa = l.mapa
      ? '<button class="tarjeta-local__mapa" type="button"' +
        ' data-mapa="' + escapar(l.mapaGrande || l.mapa) + '"' +
        ' data-titulo="Señor Limón ' + escapar(l.distrito) + ' · ' + escapar(l.direccion) + '"' +
        ' data-nota="' + escapar(l.horario || '') + '"' +
        ' data-enlace="' + escapar(destinos) + '"' +
        ' aria-label="Ampliar el mapa de ' + escapar(l.direccion) + '">' +
        '<img src="assets/img/' + l.mapa + '" alt="Mapa de la ubicación del local de ' + escapar(l.distrito) + ', ' + escapar(l.direccion) + '" loading="lazy" width="640" height="320">' +
        '<span class="tarjeta-local__mapa-pista">Ampliar el mapa ' + ICONOS.flecha + '</span></button>'
      : '';

    var zonas = '';
    if (l.zonas && l.zonas.length) {
      zonas = '<details class="tarjeta-local__zonas"><summary>Zonas con delivery</summary><ul>' +
        l.zonas.map(function (z) { return '<li>' + escapar(z) + '</li>'; }).join('') +
        '</ul><p class="tarjeta-local__nota">Y otros aledaños</p></details>';
    }

    return '<article class="tarjeta-local aparecer">' +
      '<div class="tarjeta-local__cuerpo">' +
      '<div class="tarjeta-local__cabecera">' +
      '<span class="etiqueta etiqueta--verde">' + escapar(l.distrito) + '</span>' +
      (l.atencion ? '<span class="etiqueta">' + escapar(l.atencion) + '</span>' : '') +
      '</div>' +
      '<h3 class="tarjeta-local__zona">' + escapar(l.direccion) + '</h3>' +
      '<p class="tarjeta-local__direccion">' + ICONOS.telefono + ' <a href="' + telHref(l) + '">(01) ' + escapar(l.telefono) + '</a></p>' +
      (l.horario ? '<p class="tarjeta-local__direccion">' + ICONOS.reloj + ' ' + escapar(l.horario) + '</p>' : '') +
      zonas +
      '<div class="tarjeta-local__pie">' + pie + '</div>' +
      '</div>' + mapa + '</article>';
  }

  function pintarLocales() {
    var cont = $('#lista-locales');
    if (cont) {
      cont.innerHTML = locales.map(function (l) { return htmlLocal(l, true); }).join('');
    }
    var pie = $('#locales-pie');
    if (pie) {
      pie.innerHTML = locales.map(function (l) {
        return '<li>' + ICONOS.pin + '<span>' + escapar(l.distrito) + ': ' + escapar(l.direccion) +
          ' — <a href="' + telHref(l) + '">' + escapar(l.telefono) + '</a></span></li>';
      }).join('');
    }
    var zonas = $('#zonas-home');
    if (zonas) {
      var vistos = [];
      locales.forEach(function (l) { if (vistos.indexOf(l.distrito) === -1) { vistos.push(l.distrito); } });
      zonas.innerHTML = vistos.map(function (z) {
        var n = locales.filter(function (l) { return l.distrito === z; }).length;
        return '<li>' + ICONOS.check + '<span><strong>' + escapar(z) + '</strong> — ' + n +
          (n === 1 ? ' local' : ' locales') + '</span></li>';
      }).join('');
    }
  }

  /* ---------- render: home --------------------------------------------- */
  function imagenCategoria(cat) {
    for (var i = 0; i < cat.subs.length; i++) {
      for (var j = 0; j < cat.subs[i].items.length; j++) {
        if (cat.subs[i].items[j].img) { return cat.subs[i].items[j].img; }
      }
    }
    return 'hero-cebiche.webp';
  }

  function contarPlatos(cat) {
    return cat.subs.reduce(function (t, s) { return t + s.items.length; }, 0);
  }

  function pintarHome() {
    var contCat = $('#categorias-home');
    if (contCat) {
      contCat.innerHTML = categorias.map(function (cat) {
        return '<a class="tarjeta-categoria aparecer" href="carta.html#' + cat.id + '">' +
          '<img src="assets/img/' + imagenCategoria(cat) + '" alt="' + escapar(cat.nombre) + '" loading="lazy" width="900" height="675">' +
          '<div class="tarjeta-categoria__cuerpo">' +
          '<h3>' + escapar(cat.nombre) + '</h3>' +
          '<p>' + contarPlatos(cat) + ' platos</p>' +
          '<span class="tarjeta-categoria__flecha">Ver la carta ' + ICONOS.flecha + '</span>' +
          '</div></a>';
      }).join('');
    }

    var contDest = $('#destacados-home');
    if (contDest && D.destacados) {
      contDest.innerHTML = D.destacados.map(function (p) {
        return '<article class="tarjeta-plato aparecer">' +
          (p.img ? '<div class="tarjeta-plato__foto"><img src="assets/img/' + p.img + '" alt="' + escapar(p.nombre) + '" loading="lazy" width="900" height="675"></div>' : '') +
          '<div class="tarjeta-plato__cuerpo">' +
          '<span class="etiqueta">' + escapar(p.categoria) + '</span>' +
          '<h3 style="margin-top:10px">' + escapar(p.nombre) + '</h3>' +
          '<p>' + escapar(p.desc) + '</p>' +
          '<div class="tarjeta-plato__pie"><span class="precio">' + precio(p.precio) + '</span>' +
          '<a class="boton boton--borde boton--sm" href="carta.html#' + p.catId + '">Ver más</a></div>' +
          '</div></article>';
      }).join('');
    }

    var contTes = $('#testimonios-home');
    if (contTes && D.testimonios) {
      contTes.innerHTML = D.testimonios.map(function (t) {
        return '<figure class="tarjeta-testimonio aparecer">' +
          '<div class="tarjeta-testimonio__estrellas">' + ICONOS.estrella + ICONOS.estrella + ICONOS.estrella + ICONOS.estrella + ICONOS.estrella + '</div>' +
          '<blockquote>«' + escapar(t.texto) + '»</blockquote>' +
          '<figcaption>' + escapar(t.autor) + '<span>Cliente de Señor Limón</span></figcaption>' +
          '</figure>';
      }).join('');
    }
  }

  /* ---------- render: historia (página Nosotros) ------------------------ */
  function pintarHistoria() {
    var cont = $('#historia-contenido');
    if (!cont || !D.historia) { return; }
    cont.innerHTML = D.historia.map(function (bloque) {
      return '<article class="historia-bloque aparecer">' +
        '<h2>' + escapar(bloque.titulo) + '</h2>' +
        bloque.parrafos.map(function (p) { return '<p>' + escapar(p) + '</p>'; }).join('') +
        '</article>';
    }).join('');
  }

  /* ---------- render: carta con filtros --------------------------------- */
  function htmlPlato(p) {
    var conFoto = !!p.img;
    var etiquetaPrecio = precio(p.precio);
    var variantes = '';
    if (p.variantes && p.variantes.length) {
      variantes = '<div class="plato__variantes">' + p.variantes.map(function (v) {
        return '<div class="plato__variante"><span>' + escapar(v.nombre) + '</span><span>' + precio(v.precio) + '</span></div>';
      }).join('') + '</div>';
    }
    return '<article class="plato' + (conFoto ? ' plato--con-foto' : '') + '" data-plato="' + escapar(normalizar(p.nombre + ' ' + (p.desc || ''))) + '">' +
      (conFoto ? '<button class="plato__foto" type="button" data-foto="' + escapar(p.img) + '"' +
        ' data-titulo="' + escapar(p.nombre) + '" data-nota="' + escapar(etiquetaPrecio) + '"' +
        ' aria-label="Ampliar la foto de ' + escapar(p.nombre) + '">' +
        '<img src="assets/img/' + p.img + '" alt="' + escapar(p.nombre) + '" loading="lazy" width="900" height="675"></button>' : '') +
      '<div class="plato__info">' +
      '<h4 class="plato__nombre">' + escapar(p.nombre) + '</h4>' +
      (p.desc ? '<p class="plato__desc">' + escapar(p.desc) + '</p>' : '') +
      '</div>' +
      '<span class="plato__precio">' + precio(p.precio) + '</span>' +
      variantes +
      '</article>';
  }

  /* carta en escritorio: el índice va en una columna lateral fija */
  function esEscritorio() { return window.matchMedia('(min-width: 1080px)').matches; }

  /* alto real de lo que queda pegado arriba (cabecera y, en móvil, la barra) */
  function offsetCarta() {
    var cabecera = $('.cabecera');
    var alto = (cabecera && !document.body.classList.contains('cabecera-oculta'))
      ? cabecera.getBoundingClientRect().height : 0;
    var lateral = $('.carta-lateral');
    if (lateral && !esEscritorio()) { alto += lateral.getBoundingClientRect().height; }
    return Math.round(alto + 16);
  }

  function irACategoria(id) {
    var destino = document.getElementById(id);
    if (!destino) { return; }
    var y = destino.getBoundingClientRect().top + window.scrollY - offsetCarta();
    window.scrollTo({ top: Math.max(0, y), behavior: 'smooth' });
  }

  function pintarCarta() {
    var cont = $('#carta-contenido');
    if (!cont) { return; }

    cont.innerHTML = categorias.map(function (cat) {
      var subs = cat.subs.map(function (sub) {
        return '<div class="subseccion"><h3 class="subseccion__titulo">' + escapar(sub.nombre) + '</h3>' +
          '<div class="lista-platos">' + sub.items.map(htmlPlato).join('') + '</div></div>';
      }).join('');
      return '<section class="categoria-bloque" id="' + cat.id + '" data-categoria="' + cat.id + '">' +
        '<div class="categoria-bloque__titulo"><h2>' + escapar(cat.nombre) + '</h2>' +
        '<span class="etiqueta etiqueta--verde">' + contarPlatos(cat) + ' platos</span></div>' +
        subs + '</section>';
    }).join('');

    var indice = $('#indice-categorias');
    var buscador = $('#buscador-carta');
    var limpiar = $('#limpiar-busqueda');
    var cuenta = $('#carta-cuenta');
    var vacio = $('#sin-resultados');
    var etiquetaActual = $('#categoria-actual');
    var bloques = $$('.categoria-bloque', cont);

    if (indice) {
      indice.innerHTML = '<button class="carta-indice__enlace" type="button" data-ir="carta-contenido">' +
        '<span class="carta-indice__nombre">Toda la carta</span></button>' +
        categorias.map(function (cat) {
          return '<button class="carta-indice__enlace" type="button" data-ir="' + cat.id + '">' +
            '<span class="carta-indice__nombre">' + escapar(cat.nombre) + '</span>' +
            '<span class="carta-indice__cuenta">' + contarPlatos(cat) + '</span></button>';
        }).join('');
      indice.addEventListener('click', function (e) {
        var boton = e.target.closest('[data-ir]');
        if (boton) { irACategoria(boton.getAttribute('data-ir')); }
      });
    }

    /* la sección que está arriba se marca sola en el índice */
    function marcarActual() {
      var limite = window.scrollY + offsetCarta() + 24;
      var activa = '';
      var nombre = '';
      bloques.forEach(function (b) {
        if (b.style.display === 'none') { return; }
        if (b.getBoundingClientRect().top + window.scrollY <= limite) { activa = b.id; }
      });
      categorias.forEach(function (c) { if (c.id === activa) { nombre = c.nombre; } });
      if (etiquetaActual) { etiquetaActual.textContent = nombre; }
      if (!indice) { return; }
      var activo = null;
      $$('[data-ir]', indice).forEach(function (b) {
        if (b.getAttribute('data-ir') === activa) {
          b.setAttribute('aria-current', 'true');
          activo = b;
        } else {
          b.removeAttribute('aria-current');
        }
      });
      if (activo && !esEscritorio()) {
        indice.scrollLeft = activo.offsetLeft - indice.clientWidth / 2 + activo.offsetWidth / 2;
      }
    }

    var pendiente = false;
    function alDesplazarCarta() {
      if (pendiente) { return; }
      pendiente = true;
      window.requestAnimationFrame(function () { pendiente = false; marcarActual(); });
    }

    function aplicar() {
      var consulta = normalizar(buscador && buscador.value ? buscador.value.trim() : '');
      var visibles = 0;
      if (limpiar) { limpiar.classList.toggle('es-visible', consulta.length > 0); }

      bloques.forEach(function (bloque) {
        var enBloque = 0;
        $$('.plato', bloque).forEach(function (plato) {
          var visible = !consulta || plato.getAttribute('data-plato').indexOf(consulta) !== -1;
          plato.style.display = visible ? '' : 'none';
          if (visible) { enBloque++; }
        });
        $$('.subseccion', bloque).forEach(function (sub) {
          var hay = $$('.plato', sub).some(function (p) { return p.style.display !== 'none'; });
          sub.style.display = hay ? '' : 'none';
        });
        bloque.style.display = enBloque ? '' : 'none';
        visibles += enBloque;
      });

      if (cuenta) {
        cuenta.innerHTML = '<strong>' + visibles + '</strong> ' + (visibles === 1 ? 'plato' : 'platos') +
          (consulta ? ' encontrados' : ' en la carta');
      }
      if (vacio) { vacio.style.display = visibles ? 'none' : ''; }
      marcarActual();
    }

    if (buscador) {
      buscador.addEventListener('input', aplicar);
      buscador.addEventListener('keydown', function (e) {
        if (e.key === 'Escape') { buscador.value = ''; aplicar(); }
      });
    }
    if (limpiar) {
      limpiar.addEventListener('click', function () {
        buscador.value = '';
        buscador.focus();
        aplicar();
      });
    }
    var botonTodo = $('#boton-ver-todo');
    if (botonTodo) {
      botonTodo.addEventListener('click', function () {
        if (buscador) { buscador.value = ''; }
        aplicar();
      });
    }

    window.addEventListener('scroll', alDesplazarCarta, { passive: true });
    window.addEventListener('resize', marcarActual);

    aplicar();

    // al abrir con #seccion en la dirección, se coloca respetando las barras
    if (location.hash && document.getElementById(location.hash.replace('#', ''))) {
      setTimeout(function () { irACategoria(location.hash.replace('#', '')); }, 280);
    }
  }

  /* ---------- formulario de contacto ------------------------------------ */
  function iniciarFormulario() {
    var form = $('#formulario-contacto');
    if (!form) { return; }
    var aviso = $('#aviso-formulario');
    var selector = $('#campo-distrito');

    if (selector) {
      var distritos = [];
      locales.forEach(function (l) { if (distritos.indexOf(l.distrito) === -1) { distritos.push(l.distrito); } });
      selector.innerHTML = '<option value="">Elige un local…</option>' + distritos.map(function (d) {
        return '<option value="' + escapar(d) + '">' + escapar(d) + '</option>';
      }).join('') + '<option value="Delivery a domicilio">Delivery a domicilio</option>';
    }

    function marcarError(campo, hay) {
      var envoltorio = campo.closest('.campo');
      if (envoltorio) { envoltorio.classList.toggle('es-error', hay); }
      return !hay;
    }

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var nombre = form.elements.nombre;
      var telefono = form.elements.telefono;
      var distrito = form.elements.distrito;
      var motivo = form.elements.motivo;
      var mensaje = form.elements.mensaje;

      var ok = true;
      ok = marcarError(nombre, nombre.value.trim().length < 3) && ok;
      ok = marcarError(telefono, !/^[\d\s()+-]{6,15}$/.test(telefono.value.trim())) && ok;
      ok = marcarError(distrito, !distrito.value) && ok;
      ok = marcarError(mensaje, mensaje.value.trim().length < 10) && ok;

      if (!ok) {
        if (aviso) {
          aviso.className = 'formulario__aviso formulario__aviso--error es-visible';
          aviso.textContent = 'Revisa los campos marcados para poder enviar tu mensaje.';
        }
        return;
      }

      var texto = 'Hola Señor Limón, les escribo desde la web.\n' +
        'Nombre: ' + nombre.value.trim() + '\n' +
        'Teléfono: ' + telefono.value.trim() + '\n' +
        'Local o zona: ' + distrito.value + '\n' +
        'Motivo: ' + (motivo ? motivo.value : 'Consulta') + '\n' +
        'Mensaje: ' + mensaje.value.trim();

      window.open(waHref(texto), '_blank', 'noopener');
      if (aviso) {
        aviso.className = 'formulario__aviso formulario__aviso--ok es-visible';
        aviso.textContent = 'Listo. Abrimos WhatsApp con tu mensaje; solo tienes que pulsar enviar.';
      }
      form.reset();
    });

    $$('input, select, textarea', form).forEach(function (campo) {
      campo.addEventListener('input', function () {
        var envoltorio = campo.closest('.campo');
        if (envoltorio) { envoltorio.classList.remove('es-error'); }
      });
    });
  }

  /* ---------- arranque -------------------------------------------------- */
  function iniciar() {
    iniciarCabecera();
    iniciarContacto();
    iniciarModal();
    pintarLocales();
    pintarHome();
    pintarHistoria();
    pintarCarta();
    iniciarFormulario();
    iniciarAnimaciones();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', iniciar);
  } else {
    iniciar();
  }
})();
