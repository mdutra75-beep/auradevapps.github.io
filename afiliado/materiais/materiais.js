/* Materiais para divulgação: lê materiais.json (imagens, vídeos, textos, arquivos) e mostra por app.
   Se o afiliado estiver logado, {CODIGO} nos textos vira o código dele. */
(function () {
  'use strict';

  var API = 'https://estoque-backend-production-90aa.up.railway.app';
  var qs = new URLSearchParams(location.search);
  if (/^(localhost|127\.0\.0\.1)$/.test(location.hostname) && qs.get('api')) API = qs.get('api');
  var LANGS = ['en', 'pt', 'es'];
  var S = {
    en: { title: 'Promotion materials', intro: 'Images, videos and ready-made texts to help you promote. Always disclose that you may earn a commission (for example #ad).', back: 'Back to my area', all: 'All', copy: 'Copy', copied: 'Copied!', download: 'Download', open: 'Open', empty: 'No materials yet.', codeHint: 'Sign in to your affiliate area and your code replaces {CODIGO} in the texts.', code: 'YOURCODE' },
    pt: { title: 'Materiais para divulgação', intro: 'Imagens, vídeos e textos prontos para ajudar na divulgação. Sempre avise que você pode ganhar comissão (por exemplo #publi).', back: 'Voltar à minha área', all: 'Todos', copy: 'Copiar', copied: 'Copiado!', download: 'Baixar', open: 'Abrir', empty: 'Ainda não há materiais.', codeHint: 'Entre na sua área do afiliado e o seu código substitui {CODIGO} nos textos.', code: 'SEUCODIGO' },
    es: { title: 'Materiales para promocionar', intro: 'Imágenes, videos y textos listos para ayudarte a promocionar. Avisa siempre que puedes ganar una comisión (por ejemplo #publi).', back: 'Volver a mi área', all: 'Todos', copy: 'Copiar', copied: '¡Copiado!', download: 'Descargar', open: 'Abrir', empty: 'Aún no hay materiales.', codeHint: 'Entra a tu área de afiliado y tu código reemplaza {CODIGO} en los textos.', code: 'TUCODIGO' },
  };
  var APP_NAMES = { lumora: 'Lumora', clipit: 'ClipIt Sports' };

  var lang = 'en', itens = [], filtro = 'todos', codigo = null;
  var root = document.getElementById('app');

  function t(k) { return S[lang][k]; }
  function pick(v) { return (v && typeof v === 'object') ? (v[lang] || v.en || v.pt || '') : (v || ''); }
  function el(tag, cls, text) { var e = document.createElement(tag); if (cls) e.className = cls; if (text != null) e.textContent = text; return e; }
  function add(p) { for (var i = 1; i < arguments.length; i++) if (arguments[i]) p.appendChild(arguments[i]); return p; }
  // Só caminhos do próprio site ou https (o json é nosso, mas nunca monta URL perigosa).
  function seguro(u) { return /^(\/[^/]|https:\/\/)/.test(u) ? u : ''; }

  function detectLang() {
    var q = (qs.get('lang') || '').toLowerCase();
    if (LANGS.indexOf(q) >= 0) return q;
    try { var s = localStorage.getItem('aff_lang'); if (LANGS.indexOf(s) >= 0) return s; } catch (e) {}
    var p = (navigator.languages && navigator.languages.length) ? navigator.languages : [navigator.language || 'en'];
    for (var i = 0; i < p.length; i++) { var n = String(p[i] || '').slice(0, 2).toLowerCase(); if (LANGS.indexOf(n) >= 0) return n; }
    return 'en';
  }

  function copyBtn(texto) {
    var b = el('button', 'btn sm', t('copy')); b.type = 'button';
    b.addEventListener('click', function () {
      function ok() { b.textContent = t('copied'); setTimeout(function () { b.textContent = t('copy'); }, 1600); }
      if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(texto).then(ok);
    });
    return b;
  }

  function item(m) {
    var c = el('div', 'card'), row = el('div', 'mat-item'), body = el('div');
    var titulo = pick(m.titulo), url = seguro(pick(m.arquivo));
    var nomeApp = m.app && APP_NAMES[m.app];
    add(body, el('h3', null, titulo + (nomeApp && titulo.indexOf(nomeApp) < 0 ? ' · ' + nomeApp : '')));
    if (m.descricao) add(body, el('p', 'muted', pick(m.descricao)));
    if (m.tipo === 'imagem' && url) {
      var img = el('img'); img.src = url; img.alt = titulo; img.loading = 'lazy'; add(row, img);
      var a = el('a', 'btn sm', t('download')); a.href = url; a.setAttribute('download', ''); add(body, a);
    } else if (m.tipo === 'video' && url) {
      if (/\.(mp4|webm|mov)(\?|$)/i.test(url)) { var v = el('video'); v.src = url; v.controls = true; v.preload = 'metadata'; add(row, v); }
      var a2 = el('a', 'btn sm', /\.(mp4|webm|mov)(\?|$)/i.test(url) ? t('download') : t('open')); a2.href = url; a2.target = '_blank'; a2.rel = 'noopener'; add(body, a2);
    } else if (m.tipo === 'texto') {
      var txt = pick(m.texto).split('{CODIGO}').join(codigo || t('code'));
      add(body, el('div', 'txt', txt), copyBtn(txt));
    } else if (url) {
      var a3 = el('a', 'btn sm', t('download')); a3.href = url; a3.setAttribute('download', ''); add(body, a3);
    }
    return add(c, add(row, body));
  }

  function render() {
    root.textContent = '';
    document.documentElement.lang = lang === 'pt' ? 'pt-BR' : lang;
    document.title = t('title') + ' | Aura Dev Apps';
    Array.prototype.forEach.call(document.querySelectorAll('.lang button'), function (b) { b.setAttribute('aria-pressed', String(b.getAttribute('data-lang') === lang)); });
    var back = el('a', 'linkbtn', '← ' + t('back')); back.href = '/afiliado/?lang=' + lang;
    add(root, back, el('h1', null, t('title')), el('p', 'muted', t('intro')));
    if (!codigo) add(root, el('p', 'hint', t('codeHint')));

    var apps = ['todos'].concat(Object.keys(APP_NAMES));
    var bar = el('div', 'bar');
    apps.forEach(function (a) {
      var b = el('button', 'btn sm', a === 'todos' ? t('all') : APP_NAMES[a]); b.type = 'button';
      if (a !== filtro) b.style.opacity = '.55';
      b.addEventListener('click', function () { filtro = a; render(); });
      add(bar, b);
    });
    bar.style.justifyContent = 'flex-start';
    add(root, bar);

    var lista = itens.filter(function (m) { return filtro === 'todos' || !m.app || m.app === 'todos' || m.app === filtro; });
    if (!lista.length) add(root, el('p', 'muted', t('empty')));
    lista.forEach(function (m) { add(root, item(m)); });
  }

  Array.prototype.forEach.call(document.querySelectorAll('.lang button'), function (b) {
    b.addEventListener('click', function () { lang = b.getAttribute('data-lang'); try { localStorage.setItem('aff_lang', lang); } catch (e) {} render(); });
  });
  lang = detectLang();

  var sessao = null; try { sessao = localStorage.getItem('aff_sessao'); } catch (e) {}
  Promise.all([
    fetch('materiais.json', { cache: 'no-cache' }).then(function (r) { return r.json(); }).catch(function () { return { itens: [] }; }),
    sessao ? fetch(API + '/portal/resumo', { headers: { Authorization: 'Bearer ' + sessao } }).then(function (r) { return r.ok ? r.json() : null; }).catch(function () { return null; }) : Promise.resolve(null),
  ]).then(function (res) {
    itens = (res[0] && res[0].itens) || [];
    codigo = res[1] && res[1].afiliado ? res[1].afiliado.codigo : null;
    render();
  });
})();
