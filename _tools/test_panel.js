/* ==========================================================================
   Pruebas del panel de contenido.
   Incluye un mini-DOM con nodos de texto (makeTreeWalker, createElement,
   localStorage, fetch) para poder ejecutar panel.js sin navegador.
   ========================================================================== */
const fs = require('fs');
const path = require('path');
const vm = require('vm');

const RAIZ = 'C:\\Users\\leonn\\Documents\\web\\senorlimon';
const VACIAS = ['area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'source', 'track', 'wbr'];
const TAG_RE = /<(\/?)([a-zA-Z][\w-]*)((?:\s+[^>]*?)?)(\/?)>/g;

let fallos = 0;
function comprobar(nombre, obtenido, esperado) {
  const ok = obtenido === esperado;
  if (!ok) { fallos++; }
  console.log((ok ? 'OK    ' : 'FALLA ') + nombre.padEnd(56, '.') + ' esperado=' + esperado + '  obtenido=' + obtenido);
}

/* ------------------------------ mini-DOM -------------------------------- */
class Nodo {
  constructor(tag, attrs, tipo) {
    this.nodeType = tipo || 1;
    this.tagName = (tag || '').toUpperCase();
    this.nodeName = tipo === 3 ? '#text' : this.tagName;
    this.nodeValue = tipo === 3 ? (tag || '') : '';
    this.attrs = attrs || {};
    this.childNodes = [];
    this.parentNode = null;
    this.style = {};
    this.value = this.attrs.value || '';
    this._html = '';
    this._eventos = {};
    this._onclick = null;
  }
  get children() { return this.childNodes.filter((n) => n.nodeType === 1); }
  get textContent() { return this.childNodes.map((n) => (n.nodeType === 3 ? n.nodeValue : n.textContent)).join(''); }
  set textContent(v) {
    this.childNodes = [];
    this._html = '';
    if (v !== '' && v !== null && v !== undefined) {
      const t = new Nodo(String(v), {}, 3);
      t.parentNode = this;
      this.childNodes.push(t);
    }
  }
  get previousElementSibling() {
    if (!this.parentNode) { return null; }
    const h = this.parentNode.children;
    const i = h.indexOf(this);
    return i > 0 ? h[i - 1] : null;
  }
  get parentElement() { return this.parentNode && this.parentNode.nodeType === 1 ? this.parentNode : null; }
  get outerHTML() {
    const attrs = Object.keys(this.attrs).map((k) => ' ' + k + '="' + this.attrs[k] + '"').join('');
    const t = this.tagName.toLowerCase();
    return '<' + t + attrs + '>' + this.innerHTML + '</' + t + '>';
  }
  get innerHTML() {
    if (!this.childNodes.length) { return this._html; }
    return this.childNodes.map((n) => (n.nodeType === 3 ? n.nodeValue : n.outerHTML)).join('');
  }
  set innerHTML(v) {
    this._html = String(v);
    this.childNodes = parsear(this._html, this).map((n) => { n.parentNode = this; return n; });
  }
  get classList() {
    const nodo = this;
    const leer = () => (nodo.attrs.class || '').split(/\s+/).filter(Boolean);
    return {
      add(c) { const l = leer(); if (l.indexOf(c) === -1) { l.push(c); nodo.attrs.class = l.join(' '); } },
      remove(c) { const l = leer().filter((x) => x !== c); nodo.attrs.class = l.join(' '); },
      toggle(c, on) { const t = leer().indexOf(c) > -1; const a = on === undefined ? !t : !!on; a ? this.add(c) : this.remove(c); return a; },
      contains(c) { return leer().indexOf(c) > -1; }
    };
  }
  /* en el DOM real asignar .id lo refleja como atributo; aquí igual */
  get id() { return this.attrs.id === undefined ? '' : this.attrs.id; }
  set id(v) { this.attrs.id = String(v); }
  getAttribute(n) { return this.attrs[n] === undefined ? null : this.attrs[n]; }
  setAttribute(n, v) { this.attrs[n] = String(v); if (n === 'value') { this.value = String(v); } }
  hasAttribute(n) { return this.attrs[n] !== undefined; }
  removeAttribute(n) { delete this.attrs[n]; }
  appendChild(n) { if (n.parentNode) { n.parentNode.removeChild(n); } n.parentNode = this; this.childNodes.push(n); return n; }
  insertBefore(n, ref) {
    if (n.parentNode) { n.parentNode.removeChild(n); }
    n.parentNode = this;
    const i = this.childNodes.indexOf(ref);
    if (i === -1) { this.childNodes.push(n); } else { this.childNodes.splice(i, 0, n); }
    return n;
  }
  removeChild(n) { const i = this.childNodes.indexOf(n); if (i > -1) { this.childNodes.splice(i, 1); n.parentNode = null; } return n; }
  addEventListener(t, f) { (this._eventos[t] = this._eventos[t] || []).push(f); }
  disparar(t, ev) { (this._eventos[t] || []).forEach((f) => f(ev || { target: this, preventDefault() {}, stopPropagation() {} })); }
  set onclick(f) { this._onclick = f; this._eventos.click = [f]; }
  get onclick() { return this._onclick; }
  closest(sel) {
    let n = this;
    while (n && n.nodeType === 1) { if (n.coincide(sel)) { return n; } n = n.parentNode; }
    return null;
  }
  /* soporta: tag, .clase, #id, tag.clase, [attr] y [attr="valor"] */
  coincideSimple(sel) {
    const m = sel.match(/^([a-zA-Z][\w-]*)?((?:[.#][\w-]+)*)((?:\[[^\]]+\])*)$/);
    if (!m) { return false; }
    if (m[1] && this.tagName !== m[1].toUpperCase()) { return false; }
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
        if (!this.hasAttribute(dentro)) { return false; }
      } else {
        const clave = dentro.slice(0, igual);
        const valor = dentro.slice(igual + 1).replace(/^["']|["']$/g, '');
        if (this.getAttribute(clave) !== valor) { return false; }
      }
    }
    return true;
  }
  coincide(sel) { return sel.split(',').some((s) => this.coincideSimple(s.trim())); }
  _ancestrosCoinciden(partes) {
    let i = partes.length - 1;
    let p = this.parentNode;
    while (p && i >= 0) {
      if (p.nodeType === 1 && p.coincideSimple(partes[i])) { i--; }
      p = p.parentNode;
    }
    return i < 0;
  }
  querySelectorAll(sel) {
    const grupos = sel.split(',').map((s) => s.trim()).filter(Boolean);
    const salida = [];
    const yo = this;
    (function rec(nodos) {
      nodos.forEach((n) => {
        if (n.nodeType !== 1) { return; }
        grupos.forEach((g) => {
          const partes = g.split(/\s+/);
          if (n.coincideSimple(partes[partes.length - 1]) && n._ancestrosCoinciden(partes.slice(0, -1))) {
            salida.push(n);
          }
        });
        rec(n.childNodes);
      });
    })(yo.childNodes);
    return salida.filter((n, i) => salida.indexOf(n) === i);
  }
  querySelector(sel) { return this.querySelectorAll(sel)[0] || null; }
  getBoundingClientRect() { return { top: 0, left: 0, right: 0, bottom: 0, width: 0, height: 0 }; }
  get offsetLeft() { return 0; }
  get offsetWidth() { return 0; }
  get clientWidth() { return 0; }
  focus() {}
  reset() {}
}

function parsear(html, padre) {
  const raiz = new Nodo('#raiz', {});
  const pila = [raiz];
  let ultimo = 0;
  let m;
  TAG_RE.lastIndex = 0;
  const meter = (n) => {
    const actual = pila[pila.length - 1];
    actual.childNodes.push(n);
    n.parentNode = actual;
  };
  while ((m = TAG_RE.exec(html)) !== null) {
    const texto = html.slice(ultimo, m.index);
    if (texto) { meter(new Nodo(texto, {}, 3)); }
    ultimo = TAG_RE.lastIndex;
    if (m[1] === '/') { if (pila.length > 1) { pila.pop(); } continue; }
    const attrs = {};
    const re = /([\w:-]+)(?:\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s>]+)))?/g;
    let a;
    while ((a = re.exec(m[3] || '')) !== null) {
      attrs[a[1]] = a[2] !== undefined ? a[2] : (a[3] !== undefined ? a[3] : (a[4] !== undefined ? a[4] : ''));
    }
    const nodo = new Nodo(m[2].toLowerCase(), attrs);
    meter(nodo);
    if (VACIAS.indexOf(nodo.tagName.toLowerCase()) === -1 && !m[4]) { pila.push(nodo); }
  }
  const resto = html.slice(ultimo);
  if (resto) { raiz.childNodes.push(new Nodo(resto, {}, 3)); }
  return raiz.childNodes;
}

/* ------------------------------ entorno --------------------------------- */
function montarEntorno(rutaHtml, almacen) {
  const raiz = new Nodo('#document', {});
  raiz.innerHTML = fs.readFileSync(rutaHtml, 'utf8');
  const cuerpo = raiz.querySelector('body') || raiz;

  const documento = {
    readyState: 'complete',
    documentElement: raiz,
    head: raiz.querySelector('head') || raiz,
    body: cuerpo,
    querySelector: (s) => (s.charAt(0) === '#' ? documento.getElementById(s.slice(1)) : raiz.querySelector(s)),
    querySelectorAll: (s) => raiz.querySelectorAll(s),
    getElementById: (id) => raiz.querySelectorAll('#' + id)[0] || null,
    createElement: (t) => new Nodo(t, {}),
    addEventListener() {},
    /* el filtro solo se aplica a los nodos del tipo pedido (whatToShow),
       igual que en un navegador */
    createTreeWalker: function (root, tipo, filtro) {
      const nodos = [];
      (function rec(lista) {
        lista.forEach((n) => {
          const seVisita = (tipo & (1 << (n.nodeType - 1))) !== 0;
          if (seVisita) {
            const res = filtro ? filtro.acceptNode(n) : 1;
            if (res === 1) { nodos.push(n); }
            else if (res === 2) { return; }   // REJECT: no baja al subárbol
          }
          rec(n.childNodes);
        });
      })(root.childNodes);
      let i = 0;
      return { nextNode: () => (i < nodos.length ? nodos[i++] : null) };
    }
  };

  global.NodeFilter = { SHOW_TEXT: 4, FILTER_ACCEPT: 1, FILTER_REJECT: 2, FILTER_SKIP: 3 };
  global.window = {
    SL_DATA: null, addEventListener() {}, scrollY: 0, scrollTo() {}, open() {},
    requestAnimationFrame: (f) => f(),
    matchMedia: (q) => ({ matches: false, media: q, addEventListener() {}, addListener() {} })
  };
  global.location = { hash: '', pathname: '/' + path.basename(rutaHtml) };
  global.fetch = function () { return Promise.reject(new Error('sin red en las pruebas')); };
  global.alert = function () {};
  global.confirm = function () { return true; };
  global.localStorage = almacen;
  global.document = documento;
  return documento;
}

function almacenFalso() {
  const datos = {};
  return {
    getItem: (k) => (datos[k] === undefined ? null : datos[k]),
    setItem: (k, v) => { datos[k] = String(v); },
    removeItem: (k) => { delete datos[k]; },
    _datos: datos
  };
}

function cargar(ruta, nombre) {
  vm.runInThisContext(fs.readFileSync(path.join(RAIZ, ruta), 'utf8'), { filename: nombre });
}

function ejecutarPanel(rutaHtml, almacen) {
  montarEntorno(rutaHtml, almacen);
  cargar('assets/js/data.js', 'data.js');
  cargar('assets/js/app.js', 'app.js');
  cargar('assets/js/panel.js', 'panel.js');
  return global.window.SL_PANEL;
}

/* ------------------------------ pruebas --------------------------------- */
const almacen = almacenFalso();
const api = ejecutarPanel(path.join(RAIZ, 'index.html'), almacen);

comprobar('index: el panel queda cerrado al cargar', api.estaAbierto(), false);
comprobar('index: se envuelven textos editables (>100)', api.contarEditables() > 100, true);
comprobar('index: se marcan las imágenes', api.contarImagenes() > 10, true);

// editar un texto
const claves = Object.keys(api.base().textos);
comprobar('index: hay contenido base registrado', claves.length > 100, true);


const claveHero = claves.filter((c) => /El sabor del mar peruano/.test(api.base().textos[c]))[0];
comprobar('index: se encuentra el titular del hero', !!claveHero, true);

const nodoHero = api.nodoPorClave(claveHero);
comprobar('index: la clave resuelve al nodo correcto', !!nodoHero && /El sabor del mar peruano/.test(nodoHero.innerHTML), true);

api.ponerTexto(nodoHero, 'Titular cambiado desde el panel');
comprobar('index: el texto cambió en pantalla', /Titular cambiado/.test(nodoHero.innerHTML), true);
comprobar('index: el cambio se guarda en el navegador',
  /Titular cambiado/.test(almacen.getItem('sl-contenido-v1') || ''), true);

// deshacer
api.quitarTexto(nodoHero);
comprobar('index: deshacer devuelve el texto original',
  /El sabor del mar peruano/.test(nodoHero.innerHTML), true);

// clave global del pie de página
api.ponerTexto(nodoHero, 'Otra vez cambiado');
const clavesGuardadas = Object.keys(api.estado().textos);
comprobar('index: la clave del titular no depende del pie', clavesGuardadas.length, 1);

const clavesGlobales = Object.keys(api.base().textos).filter((c) => c.indexOf('global:') === 0);
comprobar('index: hay textos globales (cabecera/pie)', clavesGlobales.length > 20, true);

// cambiar una imagen
const imgHero = api.nodoPorClave(Object.keys(api.base().imagenes)[0]);
const dataUrl = 'data:image/webp;base64,UklGRiIAAABXRUJQVlA4IBYAAAAwAQCdASoBAAEAAUAmJQBOgCHwAP7+4AAAAA==';
api.ponerImagenNueva(imgHero, dataUrl, 'hero-nueva.webp');
comprobar('index: la imagen apunta a la nueva', imgHero.getAttribute('src') === dataUrl, true);
comprobar('index: la imagen queda registrada', Object.keys(api.estado().imagenes).length, 1);

// exportar
let descargado = null;
global.Blob = function (partes, opciones) { this.partes = partes; this.type = (opciones || {}).type; };
global.URL = { createObjectURL: () => 'blob:x', revokeObjectURL() {} };
global.atob = (s) => Buffer.from(s, 'base64').toString('binary');
const protoOriginal = Nodo.prototype.click;
Nodo.prototype.click = function () { if (this.tagName === 'A' && this.download) { descargado = { nombre: this.download, contenido: '' }; } };
api.exportar(false);
comprobar('exportar: genera contenido.json', !!descargado && descargado.nombre === 'contenido.json', true);

// recarga: el contenido guardado debe aplicarse solo
const almacen2 = almacenFalso();
almacen2.setItem('sl-contenido-v1', almacen.getItem('sl-contenido-v1'));
const api2 = ejecutarPanel(path.join(RAIZ, 'index.html'), almacen2);
const nodoRecargado = api2.nodoPorClave(claveHero);
comprobar('recarga: el texto editado se aplica solo',
  !!nodoRecargado && /Otra vez cambiado/.test(nodoRecargado.innerHTML), true);

// otra página no hereda los cambios de main
const api3 = ejecutarPanel(path.join(RAIZ, 'carta.html'), almacenFalso());
comprobar('carta: carga sin errores', api3.contarEditables() > 100, true);
comprobar('carta: los platos son editables',
  Object.keys(api3.base().textos).filter((c) => /cebiche/i.test(api3.base().textos[c])).length > 0, true);

// el pie es común: la misma clave existe en otra página
const globalesCarta = Object.keys(api3.base().textos).filter((c) => c.indexOf('global:') === 0);
const comunes = globalesCarta.filter((c) => clavesGlobales.indexOf(c) > -1);
comprobar('el pie comparte claves entre páginas', comunes.length > 20, true);

/* --- casos límite detectados en la verificación ------------------------- */
// 1. nombre de página estable con y sin extensión
comprobar('carta.html da la clave "carta"', api3.paginaActual(), 'carta');
{
  const almacen4 = almacenFalso();
  montarEntorno(path.join(RAIZ, 'carta.html'), almacen4);
  global.location.pathname = '/carta';
  cargar('assets/js/data.js', 'data.js');
  cargar('assets/js/app.js', 'app.js');
  cargar('assets/js/panel.js', 'panel.js');
  comprobar('la URL /carta da la misma clave', global.window.SL_PANEL.paginaActual(), 'carta');
  const clavesCarta = Object.keys(global.window.SL_PANEL.base().textos);
  comprobar('todas las claves usan el prefijo "carta"',
    clavesCarta.every((c) => c.indexOf('carta|') === 0 || c.indexOf('global:') === 0), true);
}

// 2. importar un contenido sin datos de imagen no debe romper al descargar
const almacen5 = almacenFalso();
almacen5.setItem('sl-contenido-v1', JSON.stringify({
  textos: {}, imagenes: { 'index|main>div:1>img:1': { archivo: 'x.webp', data: '' } }
}));
const api5 = ejecutarPanel(path.join(RAIZ, 'index.html'), almacen5);
let mensaje = '';
global.alert = function (t) { mensaje = String(t); };
api5.exportarImagenes();
comprobar('descargar imágenes sin datos avisa y no falla', /no hay nada que descargar/i.test(mensaje), true);

// 3. una imagen publicada que no existe vuelve a la original
const api6 = ejecutarPanel(path.join(RAIZ, 'index.html'), almacenFalso());
{
  const claveImg = Object.keys(api6.base().imagenes)[0];
  const img = api6.nodoPorClave(claveImg);
  const original = api6.base().imagenes[claveImg];
  api6.aplicar();
  global.window.SL_PANEL.aplicarImagen(img, { archivo: 'no-existe.webp' }, claveImg);
  comprobar('imagen publicada ausente apunta al archivo nuevo',
    img.getAttribute('src') === 'assets/img/no-existe.webp', true);
  comprobar('y tiene respaldo a la imagen original', typeof img.onerror === 'function', true);
  img.onerror();
  comprobar('al fallar, vuelve a la original', img.getAttribute('src') === original, true);
}

// 4. ver el original no debe pisar una edición posterior
{
  const almacen7 = almacenFalso();
  const api7 = ejecutarPanel(path.join(RAIZ, 'index.html'), almacen7);
  const clave = Object.keys(api7.base().textos).filter((c) => /El sabor del mar/.test(api7.base().textos[c]))[0];
  const el = api7.nodoPorClave(clave);
  api7.ponerTexto(el, 'Primera edición');
  api7.abrir(true);
  api7.abrir(false);
  api7.ponerTexto(el, 'Segunda edición');
  comprobar('la edición nueva sobrevive', /Segunda edición/.test(el.innerHTML), true);
}

console.log('\n' + (fallos ? fallos + ' prueba(s) fallidas' : 'Todas las pruebas del panel pasaron'));
process.exit(fallos ? 1 : 0);
