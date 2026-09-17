/* ==========================================================================
   Prueba del sitio sin navegador:
   - mini-DOM (parser de etiquetas) para poder consultar el HTML que genera app.js
   - comprueba los recuentos de cada render
   - ejercita de verdad el buscador y los filtros de la carta
   ========================================================================== */
const fs = require('fs');
const path = require('path');
const vm = require('vm');

const RAIZ = 'C:\\Users\\leonn\\Documents\\web\\senorlimon';
const VACIO = ['area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'source', 'track', 'wbr'];

/* ------------------------------ mini-DOM -------------------------------- */
class Nodo {
  constructor(tag, attrs) {
    this.tag = (tag || '').toLowerCase();
    this.attrs = attrs || {};
    this.children = [];
    this.padre = null;
    this.style = {};
    this.textContent = '';
    this.value = this.attrs.value || '';
    this._html = '';
    this._eventos = {};
  }
  get classList() {
    const propias = (this.attrs.class || '').split(/\s+/).filter(Boolean);
    const nodo = this;
    return {
      add(c) { if (propias.indexOf(c) === -1) { propias.push(c); nodo.attrs.class = propias.join(' '); } },
      remove(c) { const i = propias.indexOf(c); if (i > -1) { propias.splice(i, 1); } nodo.attrs.class = propias.join(' '); },
      toggle(c, on) { const tiene = propias.indexOf(c) > -1; const activar = on === undefined ? !tiene : !!on; activar ? this.add(c) : this.remove(c); return activar; },
      contains(c) { return propias.indexOf(c) > -1; }
    };
  }
  get innerHTML() { return this._html; }
  set innerHTML(v) { this._html = String(v); this.children = parsear(this._html, this); }
  /* en el DOM real asignar .id lo refleja como atributo; aquí igual */
  get id() { return this.attrs.id === undefined ? '' : this.attrs.id; }
  set id(v) { this.attrs.id = String(v); }
  getAttribute(n) { return this.attrs[n] === undefined ? null : this.attrs[n]; }
  setAttribute(n, v) { this.attrs[n] = String(v); if (n === 'value') { this.value = String(v); } }
  hasAttribute(n) { return this.attrs[n] !== undefined; }
  removeAttribute(n) { delete this.attrs[n]; }
  addEventListener(tipo, fn) { (this._eventos[tipo] = this._eventos[tipo] || []).push(fn); }
  disparar(tipo, evento) { (this._eventos[tipo] || []).forEach((fn) => fn(evento || { target: this })); }
  /* soporta: tag, .clase, #id, tag.clase, [attr], [attr="valor"] y descendencia "a b" */
  coincideSimple(sel) {
    const m = sel.match(/^([a-zA-Z][\w-]*)?((?:[.#][\w-]+)*)((?:\[[^\]]+\])*)$/);
    if (!m) { return false; }
    if (m[1] && this.tag.toLowerCase() !== m[1].toLowerCase()) { return false; }
    const clases = (m[2] || '').match(/[.#][\w-]+/g) || [];
    const propias = (this.attrs.class || '').split(/\s+/);
    for (let i = 0; i < clases.length; i++) {
      const p = clases[i];
      if (p.charAt(0) === '.' && propias.indexOf(p.slice(1)) === -1) { return false; }
      if (p.charAt(0) === '#' && this.attrs.id !== p.slice(1)) { return false; }
    }
    const attrs = (m[3] || '').match(/\[[^\]]+\]/g) || [];
    for (let i = 0; i < attrs.length; i++) {
      const dentro = attrs[i].slice(1, -1);
      const igual = dentro.indexOf('=');
      if (igual === -1) {
        if (this.attrs[dentro] === undefined) { return false; }
      } else {
        const clave = dentro.slice(0, igual);
        const valor = dentro.slice(igual + 1).replace(/^["']|["']$/g, '');
        if (String(this.attrs[clave]) !== valor) { return false; }
      }
    }
    return true;
  }
  coincide(sel) { return sel.split(',').some((s) => this.coincideSimple(s.trim())); }
  closest(sel) {
    let n = this;
    while (n) { if (n.coincide && n.coincide(sel)) { return n; } n = n.padre; }
    return null;
  }
  _ancestrosCoinciden(partes) {
    let i = partes.length - 1;
    let p = this.padre;
    while (p && i >= 0) {
      if (p.coincideSimple && p.coincideSimple(partes[i])) { i--; }
      p = p.padre;
    }
    return i < 0;
  }
  querySelectorAll(sel) {
    const grupos = sel.split(',').map((s) => s.trim()).filter(Boolean);
    const salida = [];
    (function recorrer(nodos) {
      nodos.forEach((n) => {
        grupos.forEach((g) => {
          const partes = g.split(/\s+/);
          if (n.coincideSimple(partes[partes.length - 1]) && n._ancestrosCoinciden(partes.slice(0, -1))) {
            salida.push(n);
          }
        });
        recorrer(n.children);
      });
    })(this.children);
    return salida.filter((n, i) => salida.indexOf(n) === i);
  }
  querySelector(sel) { return this.querySelectorAll(sel)[0] || null; }
  appendChild(n) { n.padre = this; this.children.push(n); }
  getBoundingClientRect() { return { top: 0, left: 0, right: 0, bottom: 0, width: 0, height: 0 }; }
  get offsetLeft() { return 0; }
  get offsetWidth() { return 0; }
  get clientWidth() { return 0; }
  focus() {}
  reset() {}
}

const TAG_RE = /<(\/?)([a-zA-Z][\w-]*)((?:\s+[^>]*?)?)(\/?)>/g;

function parsear(html, padre) {
  const raiz = { children: [], padre: null, appendChild(n) { n.padre = this; this.children.push(n); } };
  const pila = [raiz];
  let ultimo = 0;
  TAG_RE.lastIndex = 0;
  let m;
  while ((m = TAG_RE.exec(html)) !== null) {
    const texto = html.slice(ultimo, m.index);
    if (texto.trim()) { pila[pila.length - 1]._texto = (pila[pila.length - 1]._texto || '') + texto; }
    ultimo = TAG_RE.lastIndex;
    const cierre = m[1] === '/';
    const tag = m[2].toLowerCase();
    const attrs = {};
    // admite atributos con valor y también sueltos (data-horario, data-anio…)
    const reAttr = /([\w:-]+)(?:\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s>]+)))?/g;
    let a;
    while ((a = reAttr.exec(m[3] || '')) !== null) {
      attrs[a[1]] = a[2] !== undefined ? a[2] : (a[3] !== undefined ? a[3] : (a[4] !== undefined ? a[4] : ''));
    }
    if (cierre) {
      if (pila.length > 1) { pila.pop(); }
      continue;
    }
    const nodo = new Nodo(tag, attrs);
    nodo.padre = pila[pila.length - 1];
    pila[pila.length - 1].children.push(nodo);
    if (!VACIO.includes(tag) && !m[4]) { pila.push(nodo); }
  }
  const hijos = raiz.children;
  /* ojo: hay que pasar el padre de verdad, no el índice del forEach */
  (function fijar(nodos, quien) {
    nodos.forEach((n) => { n.padre = quien; fijar(n.children, n); });
  })(hijos, padre);
  return hijos;
}

/* ------------------------------ entorno --------------------------------- */
function cargarDocumento(rutaHtml) {
  const html = fs.readFileSync(rutaHtml, 'utf8');
  const raiz = new Nodo('html', {});
  raiz.innerHTML = html;
  return raiz;
}

function preparar(rutaHtml) {
  const raiz = cargarDocumento(rutaHtml);
  const indice = {};
  raiz.querySelectorAll('*').forEach(function () {});
  (function indexar(nodos) { nodos.forEach((n) => { if (n.attrs.id) { indice[n.attrs.id] = n; } indexar(n.children); }); })(raiz.children);

  global.window = {
    SL_DATA: null, addEventListener() {}, scrollY: 0, scrollTo() {}, open() {},
    location: { hash: '' },
    requestAnimationFrame: (f) => f(),
    matchMedia: (q) => ({ matches: false, media: q, addEventListener() {}, addListener() {} })
  };
  global.location = global.window.location;
  const oyentesDocumento = {};
  global.document = {
    readyState: 'complete',
    body: raiz,
    // los elementos creados después (como el modal) no están en el índice:
    // se busca también en vivo
    querySelector: function (sel) {
      if (sel.charAt(0) === '#') { return indice[sel.slice(1)] || raiz.querySelectorAll(sel)[0] || null; }
      return raiz.querySelector(sel);
    },
    querySelectorAll: function (sel) { return raiz.querySelectorAll(sel); },
    createElement: function (t) { return new Nodo(t, {}); },
    addEventListener: function (tipo, fn) { (oyentesDocumento[tipo] = oyentesDocumento[tipo] || []).push(fn); },
    _disparar: function (tipo, ev) { (oyentesDocumento[tipo] || []).forEach(function (fn) { fn(ev); }); },
    getElementById: function (id) { return indice[id] || document.querySelector('#' + id); }
  };
  vm.runInThisContext(fs.readFileSync(path.join(RAIZ, 'assets', 'js', 'data.js'), 'utf8'), { filename: 'data.js' });
  vm.runInThisContext(fs.readFileSync(path.join(RAIZ, 'assets', 'js', 'app.js'), 'utf8'), { filename: 'app.js' });
  return indice;
}

/* ------------------------------ pruebas --------------------------------- */
let fallos = 0;
function comprobar(nombre, obtenido, esperado) {
  const ok = obtenido === esperado;
  if (!ok) { fallos++; }
  const linea = (ok ? 'OK    ' : 'FALLA ') + nombre.padEnd(52, '.') +
    ' esperado=' + esperado + '  obtenido=' + obtenido;
  console.log(linea);
}

const visuales = (cont) => cont.querySelectorAll('.plato').filter((p) => p.style.display !== 'none').length;

function pruebaHome() {
  const idx = preparar(path.join(RAIZ, 'index.html'));
  comprobar('home: tarjetas de categoría', idx['categorias-home'].querySelectorAll('.tarjeta-categoria').length, 10);
  comprobar('home: platos destacados', idx['destacados-home'].querySelectorAll('.tarjeta-plato').length, 6);
  comprobar('home: testimonios', idx['testimonios-home'].querySelectorAll('.tarjeta-testimonio').length, 3);
  comprobar('home: locales en el pie', idx['locales-pie'].children.length, 8);
  comprobar('home: zonas', idx['zonas-home'].children.length, 4);
  comprobar('home: imágenes de destacados', idx['destacados-home'].querySelectorAll('img').length, 6);
}

function pruebaNosotros() {
  const idx = preparar(path.join(RAIZ, 'nosotros.html'));
  const bloques = idx['historia-contenido'].querySelectorAll('.historia-bloque');
  comprobar('nosotros: bloques de historia', bloques.length, 3);
  comprobar('nosotros: párrafos en la historia',
    bloques.reduce((t, b) => t + b.querySelectorAll('p').length, 0), 13);
}

function pruebaCarta() {
  const idx = preparar(path.join(RAIZ, 'carta.html'));
  const cont = idx['carta-contenido'];
  const buscador = idx['buscador-carta'];
  const indice = idx['indice-categorias'];
  const vacio = idx['sin-resultados'];

  comprobar('carta: secciones', cont.querySelectorAll('.categoria-bloque').length, 10);
  comprobar('carta: subsecciones', cont.querySelectorAll('.subseccion__titulo').length, 21);
  comprobar('carta: platos', cont.querySelectorAll('.plato').length, 85);
  comprobar('carta: platos con foto', cont.querySelectorAll('.plato__foto').length, 85);
  comprobar('carta: ningún plato sin foto',
    cont.querySelectorAll('.plato').length - cont.querySelectorAll('.plato__foto').length, 0);
  comprobar('carta: todo visible al abrir', visuales(cont), 85);

  // índice de secciones (barra superior en móvil, columna en escritorio)
  const enlaces = indice.querySelectorAll('.carta-indice__enlace');
  comprobar('carta: índice con "Toda la carta" + 10 secciones', enlaces.length, 11);
  comprobar('carta: cada enlace apunta a algo que existe',
    enlaces.every((e) => {
      const d = e.getAttribute('data-ir');
      return d === 'carta-contenido' || !!cont.querySelector('#' + d);
    }), true);
  comprobar('carta: todos los enlaces tienen nombre',
    enlaces.filter((e) => e.querySelector('.carta-indice__nombre')).length, 11);
  comprobar('carta: las 10 secciones muestran su cuenta de platos',
    enlaces.filter((e) => e.querySelector('.carta-indice__cuenta')).length, 10);

  const enlacePiqueos = enlaces.filter((e) => e.getAttribute('data-ir') === 'piqueos')[0];
  indice.disparar('click', { target: enlacePiqueos });
  comprobar('carta: pulsar el índice no oculta el resto de secciones', visuales(cont), 85);

  // buscador
  buscador.value = 'cebiche';
  buscador.disparar('input');
  const conCebiche = visuales(cont);
  const todosSonCebiche = cont.querySelectorAll('.plato')
    .filter((p) => p.style.display !== 'none')
    .every((p) => p.getAttribute('data-plato').indexOf('cebiche') > -1);
  comprobar('carta: buscar "cebiche" filtra', conCebiche > 0 && conCebiche < 85, true);
  comprobar('carta: solo muestra coincidencias', todosSonCebiche, true);
  comprobar('carta: subtítulos ocultos sin coincidencias',
    cont.querySelectorAll('.subseccion').filter((s) => s.style.display === 'none').length > 0, true);

  // tildes
  buscador.value = 'ORIGENES';
  buscador.disparar('input');
  comprobar('carta: buscar "ORIGENES" (sin tilde) no rompe', visuales(cont) >= 0, true);

  // sin resultados
  buscador.value = 'zzzz';
  buscador.disparar('input');
  comprobar('carta: sin resultados muestra el aviso', visuales(cont) === 0 && vacio.style.display === '', true);

  // el botón del aviso de "sin resultados"
  idx['boton-ver-todo'].disparar('click');
  comprobar('carta: el botón del aviso devuelve los 85', visuales(cont), 85);
  comprobar('carta: y esconde el aviso', vacio.style.display, 'none');
}

function pruebaLocales() {
  const idx = preparar(path.join(RAIZ, 'locales.html'));
  const cont = idx['lista-locales'];
  comprobar('locales: tarjetas', cont.querySelectorAll('.tarjeta-local').length, 8);
  comprobar('locales: mapas por local', cont.querySelectorAll('.tarjeta-local__mapa img').length, 8);
  comprobar('locales: teléfonos', cont.querySelectorAll('.tarjeta-local__direccion a').length, 8);
  comprobar('locales: zonas de delivery (7, uno solo reserva)',
    cont.querySelectorAll('.tarjeta-local__zonas').length, 7);
  comprobar('locales: cada mapa tiene atribución de OpenStreetMap',
    cont.querySelectorAll('.tarjeta-local__mapa img').every((i) => /mapa-[\w-]+\.webp/.test(i.getAttribute('src'))), true);
  comprobar('locales: marcador de horario en la franja',
    idx['contenido'].querySelectorAll('[data-horario]').length >= 1, true);
}

function pruebaModalMapas() {
  const idx = preparar(path.join(RAIZ, 'locales.html'));
  const botones = idx['lista-locales'].querySelectorAll('[data-mapa]');

  comprobar('mapas: los 8 son botones ampliables', botones.length, 8);
  comprobar('mapas: no son enlaces (no navegan)', botones.every((b) => b.tag === 'button'), true);
  comprobar('mapas: abren la versión grande', botones.every((b) => /-grande\.webp$/.test(b.getAttribute('data-mapa'))), true);
  comprobar('mapas: llevan el enlace a Google Maps dentro',
    botones.every((b) => /google\.com\/maps/.test(b.getAttribute('data-enlace'))), true);

  global.document._disparar('click', { target: botones[0].querySelector('img') });
  const m = global.document.querySelector('#sl-modal');
  comprobar('mapas: el modal se abre', m.classList.contains('es-abierto'), true);
  comprobar('mapas: muestra el mapa grande',
    /assets\/img\/mapa-[\w-]+-grande\.webp/.test(global.document.querySelector('#sl-modal-img').getAttribute('src')), true);
  comprobar('mapas: titula con el local',
    /Señor Limón/.test(global.document.querySelector('#sl-modal-titulo').textContent), true);
  comprobar('mapas: ofrece abrir en Google Maps',
    /Google Maps/.test(global.document.querySelector('#sl-modal-acciones').innerHTML), true);
  comprobar('mapas: sin galería al ser una sola imagen', m.classList.contains('con-galeria'), false);
  comprobar('mapas: la página queda bloqueada detrás',
    global.document.body.classList.contains('modal-abierto'), true);

  m.disparar('click', { target: m.querySelector('.modal__cerrar') });
  comprobar('mapas: el modal se cierra', m.classList.contains('es-abierto'), false);
  comprobar('mapas: se libera el scroll de la página',
    global.document.body.classList.contains('modal-abierto'), false);
}

function pruebaModalCarta() {
  const idx = preparar(path.join(RAIZ, 'carta.html'));
  const fotos = idx['carta-contenido'].querySelectorAll('[data-foto]');
  comprobar('carta modal: las 85 fotos son ampliables', fotos.length, 85);
  comprobar('carta modal: son botones, no enlaces',
    fotos.every((b) => b.tag === 'button'), true);

  global.document._disparar('click', { target: fotos[3].querySelector('img') });
  const m = global.document.querySelector('#sl-modal');
  comprobar('carta modal: se abre en galería', m.classList.contains('con-galeria'), true);
  comprobar('carta modal: muestra el plato pulsado',
    global.document.querySelector('#sl-modal-img').getAttribute('src'),
    'assets/img/' + fotos[3].getAttribute('data-foto'));
  comprobar('carta modal: contador con la posición',
    /^4 de 85/.test(global.document.querySelector('#sl-modal-contador').textContent), true);
  comprobar('carta modal: sin enlace a Google Maps',
    global.document.querySelector('#sl-modal-acciones').innerHTML, '');

  m.disparar('click', { target: m.querySelector('.modal__flecha--despues') });
  comprobar('carta modal: avanza a la siguiente',
    global.document.querySelector('#sl-modal-img').getAttribute('src'),
    'assets/img/' + fotos[4].getAttribute('data-foto'));

  // desde la posición 5 se retrocede hasta la primera
  const contador = () => global.document.querySelector('#sl-modal-contador').textContent;
  for (let i = 0; i < 4; i++) { m.disparar('click', { target: m.querySelector('.modal__flecha--antes') }); }
  comprobar('carta modal: llega a la primera', /^1 de 85/.test(contador()), true);
  m.disparar('click', { target: m.querySelector('.modal__flecha--antes') });
  comprobar('carta modal: desde la primera vuelve a la última', /^85 de 85/.test(contador()), true);

  global.document._disparar('keydown', { key: 'Escape' });
  comprobar('carta modal: se cierra con Escape', m.classList.contains('es-abierto'), false);
}

function pruebaContacto() {
  const idx = preparar(path.join(RAIZ, 'contacto.html'));
  const select = idx['campo-distrito'];
  comprobar('contacto: select de zonas', select.querySelectorAll('option').length, 6); // 4 distritos + delivery + placeholder
  comprobar('contacto: teléfonos en la columna', idx['locales-pie'].children.length, 8);
}

pruebaHome();
pruebaNosotros();
pruebaCarta();
pruebaLocales();
pruebaModalMapas();
pruebaModalCarta();
pruebaContacto();

console.log('\n' + (fallos ? fallos + ' prueba(s) fallidas' : 'Todas las pruebas pasaron'));
process.exit(fallos ? 1 : 0);


