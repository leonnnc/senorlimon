/* ==========================================================================
   Señor Limón — panel de contenido oculto
   Permite editar los textos y las imágenes de todo el sitio, guardar los
   cambios en este navegador y publicarlos exportando un archivo.

   NO aparece enlazado en ninguna página. Para abrirlo:
     · añade  #panel  a la dirección (por ejemplo: carta.html#panel)
     · o pulsa  Ctrl + Alt + E
     · o haz 5 clics seguidos sobre el personaje del pie de página
   ========================================================================== */
(function () {
  'use strict';

  var CLAVE = 'sl-contenido-v1';
  var ARCHIVO_PUBLICADO = 'contenido.json';
  var OMITIR = { script: 1, style: 1, option: 1, textarea: 1, svg: 1, noscript: 1, iframe: 1, path: 1 };
  var MAX_IMAGEN = 1400;      // lado máximo al guardar una imagen nueva
  var PESO_AVISO = 4 * 1024 * 1024;

  var estado = { textos: {}, imagenes: {} };   // cambios locales
  var base = { textos: {}, imagenes: {} };     // contenido original, para restaurar
  var publicado = { textos: {}, imagenes: {} };
  var panel = null;
  var modoEdicion = false;
  var avisoAlmacen = '';
  var temporizadorVista = null;
  var desactualizados = [];

  /* ---------------------------------------------------------------- utils */
  function $(sel, ctx) { return (ctx || document).querySelector(sel); }
  function $$(sel, ctx) { return Array.prototype.slice.call((ctx || document).querySelectorAll(sel)); }

  /* nombre estable de la página: carta.html, /carta y /carta?x=1 dan la misma clave */
  function pagina() {
    var ruta = location.pathname.split('?')[0].split('#')[0];
    var partes = ruta.split('/').filter(Boolean);
    var nombre = (partes.pop() || '').replace(/\.html?$/i, '').toLowerCase();
    return nombre || 'inicio';
  }

  function esRaizGlobal(el) {
    if (el.closest('footer.pie')) { return 'global:pie'; }
    if (el.closest('header.cabecera')) { return 'global:cabecera'; }
    if (el.closest('#nav-movil')) { return 'global:navmovil'; }
    return null;
  }

  function raizDe(el) {
    var g = esRaizGlobal(el);
    if (g) { return { prefijo: g, nodo: el.closest('footer.pie, header.cabecera, #nav-movil') }; }
    var main = el.closest('main');
    return { prefijo: pagina(), nodo: main || document.body };
  }

  function rutaDe(raiz, el) {
    var partes = [];
    var n = el;
    while (n && n !== raiz && n.nodeType === 1) {
      var i = 1;
      var h = n;
      while ((h = h.previousElementSibling)) {
        if (h.nodeName === n.nodeName) { i++; }
      }
      partes.unshift(n.nodeName.toLowerCase() + ':' + i);
      n = n.parentElement;
    }
    return partes.join('>');
  }

  function claveDe(el) {
    var r = raizDe(el);
    return r.prefijo + '|' + rutaDe(r.nodo, el);
  }

  function nodoPorClave(clave) {
    var corte = clave.indexOf('|');
    var prefijo = clave.slice(0, corte);
    var ruta = clave.slice(corte + 1);
    var raiz;
    if (prefijo === 'global:pie') { raiz = $('footer.pie'); }
    else if (prefijo === 'global:cabecera') { raiz = $('header.cabecera'); }
    else if (prefijo === 'global:navmovil') { raiz = $('#nav-movil'); }
    else { raiz = $('main') || document.body; }

    if (!raiz) { return null; }
    var actual = raiz;
    var partes = ruta.split('>');
    for (var i = 0; i < partes.length; i++) {
      var trozo = partes[i].split(':');
      var tag = trozo[0].toUpperCase();
      var indice = parseInt(trozo[1], 10) || 1;
      var encontrados = 0;
      var hijo = null;
      var lista = actual.children;
      for (var j = 0; j < lista.length; j++) {
        if (lista[j].nodeName === tag) {
          encontrados++;
          if (encontrados === indice) { hijo = lista[j]; break; }
        }
      }
      if (!hijo) { return null; }
      actual = hijo;
    }
    return actual;
  }

  /* --------------------------------------------------------------- almacén */
  function guardar() {
    try {
      localStorage.setItem(CLAVE, JSON.stringify(estado));
      avisoAlmacen = '';
      return true;
    } catch (e) {
      avisoAlmacen = 'No se pudo guardar en este navegador (' + e.name +
        '). Los cambios siguen en pantalla: usa «Exportar» antes de cerrar.';
      return false;
    }
  }

  function cargar() {
    try {
      var crudo = localStorage.getItem(CLAVE);
      if (crudo) {
        var datos = JSON.parse(crudo);
        estado.textos = datos.textos || {};
        estado.imagenes = datos.imagenes || {};
      }
    } catch (e) {
      avisoAlmacen = 'No se pudo leer el contenido guardado en este navegador.';
    }
  }

  function pesoTotal() {
    try { return (localStorage.getItem(CLAVE) || '').length; } catch (e) { return 0; }
  }

  /* ------------------------------------------------- marcar el contenido */
  function raices() {
    return ['header.cabecera', '#nav-movil', 'main', 'footer.pie']
      .map(function (s) { return $(s); })
      .filter(Boolean);
  }

  function envolverTextos() {
    raices().forEach(function (raiz) {
      var paseador = document.createTreeWalker(raiz, NodeFilter.SHOW_TEXT, {
        acceptNode: function (nodo) {
          if (!nodo.nodeValue || !nodo.nodeValue.trim()) { return NodeFilter.FILTER_REJECT; }
          var p = nodo.parentNode;
          if (!p || p.nodeType !== 1) { return NodeFilter.FILTER_REJECT; }
          if (OMITIR[p.nodeName.toLowerCase()]) { return NodeFilter.FILTER_REJECT; }
          if (p.hasAttribute('data-ed')) { return NodeFilter.FILTER_REJECT; }
          return NodeFilter.FILTER_ACCEPT;
        }
      });
      var pendientes = [];
      var n;
      while ((n = paseador.nextNode())) { pendientes.push(n); }
      pendientes.forEach(function (nodo) {
        var envoltorio = document.createElement('span');
        envoltorio.setAttribute('data-ed', '1');
        nodo.parentNode.insertBefore(envoltorio, nodo);
        envoltorio.appendChild(nodo);
      });
    });
  }

  function marcarImagenes() {
    raices().forEach(function (raiz) {
      $$('img', raiz).forEach(function (img) {
        if (!img.hasAttribute('data-ed-img')) { img.setAttribute('data-ed-img', '1'); }
      });
    });
  }

  function recolectarBase() {
    $$('[data-ed]').forEach(function (el) { base.textos[claveDe(el)] = el.innerHTML; });
    $$('[data-ed-img]').forEach(function (el) { base.imagenes[claveDe(el)] = el.getAttribute('src'); });
  }

  /* si el texto original guardado ya no coincide con el de la web, la clave pudo
     desplazarse al cambiar el HTML: se avisa en lugar de aplicar a ciegas */
  function detectarDesactualizados() {
    desactualizados = [];
    Object.keys(estado.textos).forEach(function (c) {
      var guardado = estado.textos[c].original;
      var actual = base.textos[c];
      if (guardado && actual !== undefined && guardado !== actual) { desactualizados.push(c); }
    });
  }

  /* ------------------------------------------------------------ aplicar */
  /* si falta el archivo publicado, la imagen vuelve a la original en lugar de
     quedarse rota para los visitantes */
  function ponerImagen(img, valor, clave) {
    if (!valor) { return; }
    var original = (clave && base.imagenes[clave]) || '';
    if (typeof valor === 'string') { img.setAttribute('src', valor); return; }
    if (valor.data) { img.setAttribute('src', valor.data); return; }
    if (valor.archivo) {
      img.onerror = function () {
        img.onerror = null;
        if (original) { img.setAttribute('src', original); }
      };
      img.setAttribute('src', 'assets/img/' + valor.archivo);
    }
  }

  /* devuelve una imagen a su estado original solo si se conoce el original */
  function restaurarImagen(img, clave) {
    var original = base.imagenes[clave];
    img.onerror = null;
    if (original) { img.setAttribute('src', original); }
  }

  function aplicarTextos(fuente) {
    Object.keys(fuente).forEach(function (clave) {
      var el = nodoPorClave(clave);
      if (!el) { return; }
      var valor = fuente[clave];
      if (valor && typeof valor === 'object' && valor.valor !== undefined) { valor = valor.valor; }
      if (typeof valor === 'string') { el.innerHTML = valor; }
    });
  }

  function aplicarImagenes(fuente) {
    Object.keys(fuente).forEach(function (clave) {
      var el = nodoPorClave(clave);
      if (el) { ponerImagen(el, fuente[clave], clave); }
    });
  }

  function aplicar() {
    aplicarTextos(publicado.textos);
    aplicarImagenes(publicado.imagenes);
    aplicarTextos(estado.textos);
    aplicarImagenes(estado.imagenes);
  }

  function leerPublicado() {
    // abriendo los archivos en local no hay nada publicado que leer
    if (location.protocol !== 'http:' && location.protocol !== 'https:') { return null; }
    return fetch(ARCHIVO_PUBLICADO, { cache: 'no-store' })
      .then(function (r) { return r.ok ? r.json() : null; })
      .then(function (datos) {
        if (!datos) { return false; }
        publicado.textos = datos.textos || {};
        publicado.imagenes = datos.imagenes || {};
        aplicar();
        if (panel) { refrescarPanel(); }
        return true;
      })
      .catch(function () { return false; });
  }

  /* -------------------------------------------------------- cambio de datos */
  function ponerTexto(el, valor) {
    cancelarVistaOriginal();
    var clave = claveDe(el);
    estado.textos[clave] = { valor: valor, original: base.textos[clave] || '' };
    el.innerHTML = valor;
    guardar();
    refrescarPanel();
  }

  function quitarTexto(el) {
    cancelarVistaOriginal();
    var clave = claveDe(el);
    delete estado.textos[clave];
    if (base.textos[clave] !== undefined) { el.innerHTML = base.textos[clave]; }
    guardar();
    refrescarPanel();
  }

  function ponerImagenNueva(img, dataUrl, nombre) {
    var clave = claveDe(img);
    estado.imagenes[clave] = {
      data: dataUrl,
      archivo: nombre,
      original: base.imagenes[clave] || ''
    };
    img.setAttribute('src', dataUrl);
    guardar();
    refrescarPanel();
  }

  function quitarImagen(img) {
    cancelarVistaOriginal();
    var clave = claveDe(img);
    delete estado.imagenes[clave];
    restaurarImagen(img, clave);
    guardar();
    refrescarPanel();
  }

  /* --------------------------------------------------------- redimensionar */
  function prepararImagen(archivo, alTerminar) {
    var lector = new FileReader();
    lector.onload = function () {
      var im = new Image();
      im.onload = function () {
        var escala = Math.min(1, MAX_IMAGEN / Math.max(im.width, im.height));
        var lienzo = document.createElement('canvas');
        lienzo.width = Math.round(im.width * escala);
        lienzo.height = Math.round(im.height * escala);
        var ctx = lienzo.getContext('2d');
        ctx.drawImage(im, 0, 0, lienzo.width, lienzo.height);
        var salida = lienzo.toDataURL('image/webp', 0.78);
        if (salida.indexOf('image/webp') === -1) { salida = lienzo.toDataURL('image/jpeg', 0.85); }
        var nombre = archivo.name.replace(/\.[^.]+$/, '').replace(/[^\w-]+/g, '-').toLowerCase();
        alTerminar(salida, nombre + '.webp');
      };
      im.src = lector.result;
    };
    lector.readAsDataURL(archivo);
  }

  /* ------------------------------------------------------------- descargas */
  function descargar(nombre, contenido, tipo) {
    var blob = contenido instanceof Blob ? contenido : new Blob([contenido], { type: tipo || 'application/json' });
    var url = URL.createObjectURL(blob);
    var a = document.createElement('a');
    a.href = url;
    a.download = nombre;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    setTimeout(function () { URL.revokeObjectURL(url); }, 4000);
  }

  function dataUrlABlob(dataUrl) {
    if (!dataUrl || typeof dataUrl !== 'string' || dataUrl.indexOf(',') === -1) { return null; }
    var partes = dataUrl.split(',');
    var mime = partes[0].match(/:(.*?);/)[1];
    var bin = atob(partes[1]);
    var bytes = new Uint8Array(bin.length);
    for (var i = 0; i < bin.length; i++) { bytes[i] = bin.charCodeAt(i); }
    return new Blob([bytes], { type: mime });
  }

  function nombreArchivoSalida(nombre) {
    return (nombre || 'imagen').replace(/\.(webp|jpe?g|png)$/i, '') + '-nueva.webp';
  }

  /* ======================================================================
     A partir de aquí, la interfaz del panel
     ====================================================================== */
  var ESTILOS = '\
#sl-panel, #sl-panel * { box-sizing: border-box; }\
#sl-panel { position: fixed; top: 0; right: 0; bottom: 0; width: 390px; max-width: 100vw; z-index: 9999;\
  background: #0d2b38; color: #eaf2f5; font-family: "Inter", system-ui, sans-serif; font-size: 14px;\
  display: flex; flex-direction: column; box-shadow: -14px 0 40px rgba(0,0,0,.35); transform: translateX(102%);\
  transition: transform .28s cubic-bezier(.2,.7,.3,1); }\
#sl-panel.es-abierto { transform: none; }\
#sl-panel h2 { font-family: "Outfit", system-ui, sans-serif; font-size: 16px; margin: 0; color: #fff; }\
#sl-panel .sl-cab { display: flex; align-items: center; justify-content: space-between; gap: 10px;\
  padding: 16px 18px; border-bottom: 1px solid rgba(255,255,255,.12); background: #0a222c; }\
#sl-panel .sl-cab small { display: block; color: #8fb3c0; font-size: 11px; margin-top: 3px; letter-spacing: .04em; }\
#sl-panel .sl-cuerpo { overflow-y: auto; padding: 16px 18px 24px; flex: 1; }\
#sl-panel button { font: inherit; cursor: pointer; border-radius: 10px; border: 1px solid transparent; padding: 9px 13px;\
  background: rgba(255,255,255,.09); color: #eaf2f5; transition: background .2s, transform .2s; }\
#sl-panel button:hover { background: rgba(255,255,255,.18); }\
#sl-panel button.sl-principal { background: #7ab929; color: #08240a; font-weight: 600; }\
#sl-panel button.sl-principal:hover { background: #96ce44; }\
#sl-panel button.sl-peligro { background: rgba(221,83,65,.22); color: #ffb3a8; }\
#sl-panel button.sl-activo { background: #f0b429; color: #3a2a00; font-weight: 600; }\
#sl-panel button[disabled] { opacity: .45; cursor: not-allowed; }\
#sl-panel .sl-fila { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 14px; }\
#sl-panel .sl-bloque { border-top: 1px solid rgba(255,255,255,.1); padding-top: 14px; margin-top: 14px; }\
#sl-panel .sl-bloque h3 { font-family: "Outfit", system-ui, sans-serif; font-size: 12px; text-transform: uppercase;\
  letter-spacing: .12em; color: #8fb3c0; margin: 0 0 10px; }\
#sl-panel .sl-nota { font-size: 12px; color: #9fbec9; line-height: 1.55; }\
#sl-panel .sl-aviso { background: rgba(240,180,41,.15); color: #ffd98a; border-radius: 10px; padding: 10px 12px;\
  font-size: 12px; margin-bottom: 12px; line-height: 1.5; }\
#sl-panel .sl-item { display: flex; gap: 10px; align-items: flex-start; padding: 9px 0;\
  border-bottom: 1px solid rgba(255,255,255,.08); font-size: 12px; }\
#sl-panel .sl-item span { flex: 1; color: #cfe2e8; word-break: break-word; }\
#sl-panel .sl-item b { color: #fff; font-weight: 600; }\
#sl-panel .sl-item button { padding: 4px 9px; font-size: 11px; }\
#sl-panel .sl-vacio { color: #7fa0ad; font-size: 12px; padding: 6px 0; }\
#sl-panel .sl-cerrar { width: 34px; height: 34px; padding: 0; display: grid; place-items: center; font-size: 17px; }\
#sl-panel .sl-pie { padding: 12px 18px; border-top: 1px solid rgba(255,255,255,.12); background: #0a222c;\
  font-size: 11px; color: #7fa0ad; }\
#sl-editor { position: fixed; inset: 0; z-index: 10001; background: rgba(4,20,28,.72); display: none;\
  align-items: center; justify-content: center; padding: 20px; }\
#sl-editor.es-abierto { display: flex; }\
#sl-editor .sl-caja { background: #10323f; border-radius: 16px; padding: 20px; width: 620px; max-width: 100%;\
  max-height: 90vh; display: flex; flex-direction: column; gap: 12px; box-shadow: 0 24px 60px rgba(0,0,0,.45); }\
#sl-editor h3 { font-family: "Outfit", system-ui, sans-serif; margin: 0; font-size: 17px; color: #fff; }\
#sl-editor textarea { width: 100%; min-height: 150px; border-radius: 10px; border: 1px solid rgba(255,255,255,.18);\
  background: #0a222c; color: #eaf2f5; padding: 12px; font: inherit; resize: vertical; }\
#sl-editor .sl-chico { font-size: 12px; color: #9fbec9; line-height: 1.5; }\
#sl-editor img { max-height: 260px; border-radius: 12px; object-fit: contain; background: #0a222c; }\
#sl-editor .sl-fila { display: flex; gap: 10px; flex-wrap: wrap; justify-content: flex-end; }\
#sl-editor button { font: inherit; cursor: pointer; border-radius: 10px; padding: 10px 15px; border: 1px solid transparent;\
  background: rgba(255,255,255,.12); color: #eaf2f5; }\
#sl-editor button.sl-principal { background: #7ab929; color: #08240a; font-weight: 600; }\
body.sl-editando [data-ed]:hover { outline: 2px dashed #f0b429; outline-offset: 2px; background: rgba(240,180,41,.1); cursor: text; }\
body.sl-editando [data-ed-img]:hover { outline: 3px dashed #7ab929; outline-offset: 2px; cursor: pointer; }\
body.sl-editando a, body.sl-editando button { pointer-events: none; }\
body.sl-editando [data-ed], body.sl-editando [data-ed-img] { pointer-events: auto; }\
body.sl-editando::after { content: "MODO EDICIÓN — haz clic en cualquier texto o imagen"; position: fixed;\
  left: 50%; bottom: 16px; transform: translateX(-50%); z-index: 9998; background: #f0b429; color: #3a2a00;\
  font: 600 12px/1 "Inter", system-ui, sans-serif; padding: 11px 18px; border-radius: 999px;\
  box-shadow: 0 10px 26px rgba(0,0,0,.3); }';

  function inyectarEstilos() {
    if ($('#sl-estilos')) { return; }
    var estilo = document.createElement('style');
    estilo.id = 'sl-estilos';
    estilo.textContent = ESTILOS;
    document.head.appendChild(estilo);
  }

  function crearPanel() {
    inyectarEstilos();
    panel = document.createElement('aside');
    panel.id = 'sl-panel';
    panel.setAttribute('aria-hidden', 'true');
    panel.innerHTML =
      '<div class="sl-cab">' +
        '<div><h2>Panel de contenido</h2><small>Señor Limón · edita y publica</small></div>' +
        '<button class="sl-cerrar" type="button" data-accion="cerrar" aria-label="Cerrar panel">✕</button>' +
      '</div>' +
      '<div class="sl-cuerpo">' +
        '<div class="sl-fila">' +
          '<button type="button" class="sl-principal" data-accion="modo">Activar modo edición</button>' +
          '<button type="button" data-accion="ver">Ver original</button>' +
        '</div>' +
        '<div class="sl-nota">Con el modo edición activado, haz clic en cualquier texto o imagen de la página para cambiarlo. Los cambios se guardan en este navegador.</div>' +
        '<div class="sl-bloque">' +
          '<h3>Cambios sin publicar</h3>' +
          '<div id="sl-lista"></div>' +
        '</div>' +
        '<div class="sl-bloque">' +
          '<h3>Publicar</h3>' +
          '<div class="sl-nota" style="margin-bottom:10px">Descarga el archivo y súbelo a la raíz de tu web. Las imágenes van a <b>assets/img/</b>. Mientras no lo hagas, los cambios solo se ven en este navegador.<br><br>Si dejas la casilla sin marcar se descargarán también las imágenes: <b>súbelas a assets/img/</b> o esas fotos volverán a las anteriores.</div>' +
          '<div class="sl-fila">' +
            '<button type="button" class="sl-principal" data-accion="exportar">Descargar contenido.json</button>' +
            '<button type="button" data-accion="exportar-img">Descargar imágenes</button>' +
          '</div>' +
          '<label class="sl-nota" style="display:flex;gap:8px;align-items:flex-start">' +
            '<input type="checkbox" id="sl-incluir"> <span>Incluir las imágenes dentro del archivo (más pesado, pero se publica con un solo archivo)</span>' +
          '</label>' +
        '</div>' +
        '<div class="sl-bloque">' +
          '<h3>Copias de seguridad</h3>' +
          '<div class="sl-fila">' +
            '<button type="button" data-accion="importar">Importar archivo…</button>' +
            '<button type="button" class="sl-peligro" data-accion="restablecer">Restablecer todo</button>' +
          '</div>' +
          '<input type="file" id="sl-archivo" accept="application/json,.json" hidden>' +
        '</div>' +
      '</div>' +
      '<div class="sl-pie" id="sl-pie"></div>';
    document.body.appendChild(panel);

    var editor = document.createElement('div');
    editor.id = 'sl-editor';
    editor.innerHTML = '<div class="sl-caja" id="sl-caja"></div>';
    document.body.appendChild(editor);

    panel.addEventListener('click', alPulsar);
    editor.addEventListener('click', function (e) {
      if (e.target === editor) { cerrarEditor(); }
    });

    var entrada = $('#sl-archivo');
    entrada.addEventListener('change', function () {
      if (entrada.files && entrada.files[0]) { importar(entrada.files[0]); }
      entrada.value = '';
    });
  }

  function refrescarPanel() {
    if (!panel) { return; }
    var total = Object.keys(estado.textos).length + Object.keys(estado.imagenes).length;
    var lista = $('#sl-lista');
    var html = '';

    if (desactualizados.length) {
      html += '<div class="sl-aviso">' + desactualizados.length +
        ' cambio(s) pueden haberse desplazado porque la web se actualizó después. ' +
        'Ábrelos y vuelve a guardarlos para asegurarte.</div>';
    }

    Object.keys(estado.textos).forEach(function (clave) {
      var v = estado.textos[clave].valor || '';
      html += '<div class="sl-item"><span><b>Texto</b> · ' + escapar(v.slice(0, 74)) +
        (v.length > 74 ? '…' : '') + '</span><button type="button" data-deshacer="' + escapar(clave) + '">Deshacer</button></div>';
    });
    Object.keys(estado.imagenes).forEach(function (clave) {
      var v = estado.imagenes[clave];
      html += '<div class="sl-item"><span><b>Imagen</b> · ' + escapar(v.archivo || 'nueva imagen') +
        '</span><button type="button" data-deshacer-img="' + escapar(clave) + '">Deshacer</button></div>';
    });

    lista.innerHTML = html || '<div class="sl-vacio">Todavía no has cambiado nada.</div>';

    var pie = $('#sl-pie');
    var texto = total + (total === 1 ? ' cambio guardado' : ' cambios guardados');
    if (avisoAlmacen) { texto = '⚠ ' + avisoAlmacen; }
    else if (pesoTotal() > PESO_AVISO) { texto = texto + ' · ocupa ' + Math.round(pesoTotal() / 1048576 * 10) / 10 + ' MB, conviene publicar pronto'; }
    pie.textContent = texto;
  }

  function escapar(t) {
    return String(t === undefined || t === null ? '' : t)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }

  /* ----------------------------------------------------------- interacción */
  function alPulsar(e) {
    var deshacerTexto = e.target.closest('[data-deshacer]');
    if (deshacerTexto) {
      var clave = deshacerTexto.getAttribute('data-deshacer');
      var el = nodoPorClave(clave);
      if (el && base.textos[clave] !== undefined) { el.innerHTML = base.textos[clave]; }
      delete estado.textos[clave];
      guardar(); refrescarPanel();
      return;
    }
    var deshacerImagen = e.target.closest('[data-deshacer-img]');
    if (deshacerImagen) {
      var claveImg = deshacerImagen.getAttribute('data-deshacer-img');
      var img = nodoPorClave(claveImg);
      if (img) { restaurarImagen(img, claveImg); }
      delete estado.imagenes[claveImg];
      guardar(); refrescarPanel();
      return;
    }
    var boton = e.target.closest('[data-accion]');
    if (!boton) { return; }
    var accion = boton.getAttribute('data-accion');
    if (accion === 'cerrar') { abrir(false); }
    else if (accion === 'modo') { activarEdicion(!modoEdicion); }
    else if (accion === 'ver') { verOriginal(); }
    else if (accion === 'exportar') { exportar(!!($('#sl-incluir') && $('#sl-incluir').checked)); }
    else if (accion === 'exportar-img') { exportarImagenes(); }
    else if (accion === 'importar') { $('#sl-archivo').click(); }
    else if (accion === 'restablecer') { restablecer(); }
  }

  function activarEdicion(activar) {
    modoEdicion = activar;
    document.body.classList.toggle('sl-editando', activar);
    var boton = panel && panel.querySelector('[data-accion="modo"]');
    if (boton) {
      boton.textContent = activar ? 'Desactivar modo edición' : 'Activar modo edición';
      boton.classList.toggle('sl-activo', activar);
    }
  }

  function verOriginal() {
    Object.keys(estado.textos).forEach(function (c) {
      var el = nodoPorClave(c);
      if (el && base.textos[c] !== undefined) { el.innerHTML = base.textos[c]; }
    });
    Object.keys(estado.imagenes).forEach(function (c) {
      var el = nodoPorClave(c);
      if (el) { restaurarImagen(el, c); }
    });
    cancelarVistaOriginal();
    temporizadorVista = setTimeout(aplicar, 2500);
  }

  /* si se edita algo mientras se ve el original, se cancela la vuelta atrás */
  function cancelarVistaOriginal() {
    if (temporizadorVista) { clearTimeout(temporizadorVista); temporizadorVista = null; }
  }

  function abrirEditor(html) {
    var caja = $('#sl-caja');
    caja.innerHTML = html;
    $('#sl-editor').classList.add('es-abierto');
  }

  function cerrarEditor() {
    $('#sl-editor').classList.remove('es-abierto');
    $('#sl-caja').innerHTML = '';
  }

  /* -------------------------------------------------------------- edición */
  function claveEditableDe(nodo) {
    var el = nodo.nodeType === 1 ? nodo : nodo.parentElement;
    if (!el) { return null; }
    var img = el.closest('[data-ed-img]');
    if (img) { return { tipo: 'imagen', el: img }; }
    var texto = el.closest('[data-ed]');
    if (texto) { return { tipo: 'texto', el: texto }; }
    return null;
  }

  function alClicEdicion(e) {
    if (!modoEdicion) { return; }
    if (e.target.closest('#sl-panel') || e.target.closest('#sl-editor')) { return; }
    var objetivo = claveEditableDe(e.target);
    if (!objetivo) { return; }
    e.preventDefault();
    e.stopPropagation();
    if (objetivo.tipo === 'texto') { editarTexto(objetivo.el); }
    else { editarImagen(objetivo.el); }
  }

  function editarTexto(el) {
    var actual = el.innerHTML;
    abrirEditor(
      '<h3>Editar texto</h3>' +
      '<div class="sl-chico">Puedes escribir texto normal. Si necesitas negrita usa &lt;b&gt;texto&lt;/b&gt;.</div>' +
      '<textarea id="sl-texto"></textarea>' +
      '<div class="sl-fila">' +
        '<button type="button" data-ed="cancelar">Cancelar</button>' +
        '<button type="button" data-ed="restaurar">Volver al original</button>' +
        '<button type="button" class="sl-principal" data-ed="guardar">Guardar</button>' +
      '</div>');
    var area = $('#sl-texto');
    area.value = (estado.textos[claveDe(el)] && estado.textos[claveDe(el)].valor) || actual;
    area.focus();
    area.setSelectionRange(area.value.length, area.value.length);

    $('#sl-caja').onclick = function (ev) {
      var b = ev.target.closest('[data-ed]');
      if (!b) { return; }
      var accion = b.getAttribute('data-ed');
      if (accion === 'cancelar') { cerrarEditor(); }
      else if (accion === 'guardar') { ponerTexto(el, area.value); cerrarEditor(); }
      else if (accion === 'restaurar') { quitarTexto(el); cerrarEditor(); }
    };
  }

  function editarImagen(img) {
    var clave = claveDe(img);
    var actual = (estado.imagenes[clave] && estado.imagenes[clave].data) || img.getAttribute('src');
    abrirEditor(
      '<h3>Cambiar imagen</h3>' +
      '<div class="sl-chico">Elige una foto de tu equipo. Se reduce y se convierte sola para que la web siga rápida.</div>' +
      '<img id="sl-vista" src="' + escapar(actual) + '" alt="Vista previa">' +
      '<input type="file" id="sl-img" accept="image/*">' +
      '<div id="sl-estado-img" class="sl-chico"></div>' +
      '<div class="sl-fila">' +
        '<button type="button" data-ed="cancelar">Cancelar</button>' +
        '<button type="button" data-ed="restaurar">Volver al original</button>' +
        '<button type="button" class="sl-principal" data-ed="guardar" disabled>Guardar</button>' +
      '</div>');

    var pendiente = null;
    var entrada = $('#sl-img');
    entrada.addEventListener('change', function () {
      if (!entrada.files || !entrada.files[0]) { return; }
      $('#sl-estado-img').textContent = 'Preparando la imagen…';
      prepararImagen(entrada.files[0], function (dataUrl, nombre) {
        pendiente = { dataUrl: dataUrl, nombre: nombre };
        $('#sl-vista').src = dataUrl;
        $('#sl-estado-img').textContent = 'Lista: ' + nombre + ' (' + Math.round(dataUrl.length / 1024) + ' KB). Pulsa Guardar.';
        $('#sl-caja').querySelector('[data-ed="guardar"]').disabled = false;
      });
    });

    $('#sl-caja').onclick = function (ev) {
      var b = ev.target.closest('[data-ed]');
      if (!b) { return; }
      var accion = b.getAttribute('data-ed');
      if (accion === 'cancelar') { cerrarEditor(); }
      else if (accion === 'restaurar') { quitarImagen(img); cerrarEditor(); }
      else if (accion === 'guardar' && pendiente) {
        ponerImagenNueva(img, pendiente.dataUrl, pendiente.nombre);
        cerrarEditor();
      }
    };
  }

  /* -------------------------------------------------------------- publicar */
  function exportar(conImagenes) {
    var textos = {};
    Object.keys(estado.textos).forEach(function (c) {
      textos[c] = { valor: estado.textos[c].valor, original: estado.textos[c].original };
    });
    var imagenes = {};
    Object.keys(estado.imagenes).forEach(function (c) {
      var v = estado.imagenes[c];
      imagenes[c] = conImagenes ? { data: v.data } : { archivo: nombreArchivoSalida(v.archivo) };
    });
    var datos = { version: 1, generado: new Date().toISOString(), textos: textos, imagenes: imagenes };
    descargar('contenido.json', JSON.stringify(datos, null, 2), 'application/json');
    if (!conImagenes) { setTimeout(exportarImagenes, 700); }
  }

  function exportarImagenes() {
    var claves = Object.keys(estado.imagenes);
    if (!claves.length) { alert('No hay imágenes nuevas que descargar.'); return; }
    var conDatos = claves.filter(function (c) { return !!estado.imagenes[c].data; });
    var sinDatos = claves.length - conDatos.length;
    if (!conDatos.length) {
      alert('Las imágenes que has cambiado se guardaron solo como nombre de archivo ' +
        '(así se exportó el contenido que importaste), por lo que no hay nada que descargar.\n\n' +
        'Vuelve a elegir esas fotos desde el panel para poder descargarlas.');
      return;
    }
    conDatos.forEach(function (c, i) {
      var v = estado.imagenes[c];
      var blob = dataUrlABlob(v.data);
      if (!blob) { return; }
      setTimeout(function () {
        descargar(nombreArchivoSalida(v.archivo), blob, 'image/webp');
      }, i * 600);
    });
    if (sinDatos) {
      alert('Se descargarán ' + conDatos.length + ' imágenes. Otras ' + sinDatos +
        ' no tienen datos guardados en este navegador; vuelve a elegirlas desde el panel ' +
        'si necesitas descargarlas.');
    }
  }

  function importar(archivo) {
    var lector = new FileReader();
    lector.onload = function () {
      try {
        var datos = JSON.parse(lector.result);
        estado.textos = {};
        estado.imagenes = {};
        Object.keys(datos.textos || {}).forEach(function (c) {
          var v = datos.textos[c];
          estado.textos[c] = { valor: typeof v === 'string' ? v : v.valor, original: base.textos[c] || '' };
        });
        Object.keys(datos.imagenes || {}).forEach(function (c) {
          var v = datos.imagenes[c];
          estado.imagenes[c] = { data: v.data || '', archivo: v.archivo || '', original: base.imagenes[c] || '' };
        });
        guardar();
        detectarDesactualizados();
        aplicar();
        refrescarPanel();
        alert('Contenido importado correctamente.');
      } catch (e) {
        alert('No se pudo leer el archivo: ' + e.message);
      }
    };
    lector.readAsText(archivo);
  }

  function restablecer() {
    if (!confirm('¿Seguro que quieres borrar todos los cambios guardados en este navegador? La web volverá a como está ahora.')) { return; }
    cancelarVistaOriginal();
    Object.keys(estado.textos).forEach(function (c) {
      var el = nodoPorClave(c);
      if (el && base.textos[c] !== undefined) { el.innerHTML = base.textos[c]; }
    });
    Object.keys(estado.imagenes).forEach(function (c) {
      var el = nodoPorClave(c);
      if (el) { restaurarImagen(el, c); }
    });
    estado = { textos: {}, imagenes: {} };
    desactualizados = [];
    guardar();
    refrescarPanel();
  }

  /* ----------------------------------------------------------- abrir/cerrar */
  function abrir(si) {
    if (!panel) { crearPanel(); }
    panel.classList.toggle('es-abierto', si);
    panel.setAttribute('aria-hidden', si ? 'false' : 'true');
    if (si) { refrescarPanel(); }
    else { activarEdicion(false); }
  }

  function alTeclear(e) {
    if (e.key === 'Escape') {
      if ($('#sl-editor') && $('#sl-editor').classList.contains('es-abierto')) { cerrarEditor(); return; }
      if (panel && panel.classList.contains('es-abierto')) { abrir(false); }
    }
    if (e.altKey && (e.ctrlKey || e.metaKey) && (e.key === 'e' || e.key === 'E' || e.key === 'p' || e.key === 'P')) {
      e.preventDefault();
      abrir(!(panel && panel.classList.contains('es-abierto')));
    }
  }

  function vigilarLogoDelPie() {
    var marca = $('footer.pie .pie__marca img');
    if (!marca) { return; }
    var pulsaciones = 0;
    var reloj = null;
    marca.addEventListener('click', function () {
      pulsaciones++;
      clearTimeout(reloj);
      reloj = setTimeout(function () { pulsaciones = 0; }, 1200);
      if (pulsaciones >= 5) { pulsaciones = 0; abrir(true); }
    });
  }

  /* ---------------------------------------------------------------- arranque */
  function iniciar() {
    cargar();
    envolverTextos();
    marcarImagenes();
    recolectarBase();
    detectarDesactualizados();
    aplicar();
    document.addEventListener('click', alClicEdicion, true);
    document.addEventListener('keydown', alTeclear);
    vigilarLogoDelPie();
    leerPublicado();
    if (/^#(panel|admin)$/i.test(location.hash)) { abrir(true); }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () { setTimeout(iniciar, 0); });
  } else {
    iniciar();
  }

  /* API mínima: la usan las pruebas automáticas y sirve para automatizar
     cambios en bloque desde la consola del navegador. */
  window.SL_PANEL = {
    abrir: abrir,
    estaAbierto: function () { return !!(panel && panel.classList.contains('es-abierto')); },
    estaEditando: function () { return modoEdicion; },
    estado: function () { return estado; },
    base: function () { return base; },
    aplicar: aplicar,
    ponerTexto: ponerTexto,
    quitarTexto: quitarTexto,
    ponerImagenNueva: ponerImagenNueva,
    quitarImagen: quitarImagen,
    aplicarImagen: ponerImagen,
    exportar: exportar,
    exportarImagenes: exportarImagenes,
    restablecer: restablecer,
    paginaActual: pagina,
    desactualizados: function () { return desactualizados.slice(); },
    claveDe: claveDe,
    nodoPorClave: nodoPorClave,
    contarEditables: function () { return $$('[data-ed]').length; },
    contarImagenes: function () { return $$('[data-ed-img]').length; }
  };
})();
