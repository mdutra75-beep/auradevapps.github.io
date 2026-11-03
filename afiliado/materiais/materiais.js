/* Materiais para divulgação: lê materiais.json (imagens, vídeos, textos, arquivos) e mostra por app.
   Se o afiliado estiver logado, {CODIGO} nos textos vira o código dele. */
(function () {
  'use strict';

  var API = 'https://estoque-backend-production-90aa.up.railway.app';
  var qs = new URLSearchParams(location.search);
  if (/^(localhost|127\.0\.0\.1)$/.test(location.hostname) && qs.get('api')) API = qs.get('api');
  var LANGS = ['en', 'pt', 'es'];
  var S = {
    en: { title: 'Promotion materials', intro: 'Images, videos and ready-made texts to help you promote. Always disclose that you may earn a commission (for example #ad).', back: 'Back to my area', all: 'All', copy: 'Copy', copied: 'Copied!', download: 'Download', open: 'Open', empty: 'No materials in this language yet.', matLang: 'Materials language', secLogo: 'Logos', secPrints: 'App screenshots', secDiv: 'Promotion materials', codeHint: 'Sign in to your affiliate area and your code replaces {CODIGO} in the texts.', code: 'YOURCODE' },
    pt: { title: 'Materiais para divulgação', intro: 'Imagens, vídeos e textos prontos para ajudar na divulgação. Sempre avise que você pode ganhar comissão (por exemplo #publi).', back: 'Voltar à minha área', all: 'Todos', copy: 'Copiar', copied: 'Copiado!', download: 'Baixar', open: 'Abrir', empty: 'Ainda não há materiais neste idioma.', matLang: 'Idioma dos materiais', secLogo: 'Logos', secPrints: 'Prints do app', secDiv: 'Materiais de divulgação', codeHint: 'Entre na sua área do afiliado e o seu código substitui {CODIGO} nos textos.', code: 'SEUCODIGO' },
    es: { title: 'Materiales para promocionar', intro: 'Imágenes, videos y textos listos para ayudarte a promocionar. Avisa siempre que puedes ganar una comisión (por ejemplo #publi).', back: 'Volver a mi área', all: 'Todos', copy: 'Copiar', copied: '¡Copiado!', download: 'Descargar', open: 'Abrir', empty: 'Aún no hay materiales en este idioma.', matLang: 'Idioma de los materiales', secLogo: 'Logos', secPrints: 'Capturas de pantalla', secDiv: 'Materiales de promoción', codeHint: 'Entra a tu área de afiliado y tu código reemplaza {CODIGO} en los textos.', code: 'TUCODIGO' },
  };
  var APP_NAMES = { lumora: 'Lumora', clipit: 'ClipIt Sports' };
  var LANG_NAMES = { pt: 'Português', en: 'English', es: 'Español' };

  var lang = 'en', itens = [], filtro = 'todos', codigo = null, meusApps = null;
  var root = document.getElementById('app');
  // Página própria de um app (/afiliado/materiais/lumora/ ou /clipit/): mostra só os materiais dele.
  var fixo = root.getAttribute('data-app');
  if (fixo && !APP_NAMES[fixo]) fixo = null;

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

  // Material com "idioma" (texto ou lista, ex.: "pt" ou ["pt","es"]) só aparece nesse(s) idioma(s);
  // sem "idioma", aparece em todos (e título/arquivo/texto podem trazer uma versão por idioma).
  function noIdioma(m) {
    if (!m.idioma) return true;
    return (Array.isArray(m.idioma) ? m.idioma : [m.idioma]).indexOf(lang) >= 0;
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
    var tituloPagina = t('title') + (fixo ? ' · ' + APP_NAMES[fixo] : '');
    document.title = tituloPagina + ' | Aura Dev Apps';
    Array.prototype.forEach.call(document.querySelectorAll('.lang button'), function (b) { b.setAttribute('aria-pressed', String(b.getAttribute('data-lang') === lang)); });
    var back = el('a', 'linkbtn', '← ' + t('back')); back.href = '/afiliado/?lang=' + lang;
    add(root, back, el('h1', null, tituloPagina), el('p', 'muted', t('intro')));
    // Seletor de idioma bem visível: os materiais são separados por idioma.
    var lb = el('div', 'bar'); lb.style.justifyContent = 'flex-start'; lb.style.alignItems = 'center';
    var ll = el('span', 'muted', t('matLang') + ':'); ll.style.marginRight = '.4rem'; add(lb, ll);
    LANGS.slice().sort(function (a, b) { return ['pt', 'en', 'es'].indexOf(a) - ['pt', 'en', 'es'].indexOf(b); }).forEach(function (l) {
      var b = el('button', 'btn sm', LANG_NAMES[l]); b.type = 'button';
      b.setAttribute('aria-pressed', String(l === lang));
      if (l !== lang) b.style.opacity = '.55';
      b.addEventListener('click', function () { lang = l; try { localStorage.setItem('aff_lang', lang); } catch (e) {} render(); });
      add(lb, b);
    });
    add(root, lb);
    if (!codigo) add(root, el('p', 'hint', t('codeHint')));

    // Afiliado logado vê só o(s) app(s) dele; com um app só, nem aparece o filtro.
    var apps = ['todos'].concat(meusApps || Object.keys(APP_NAMES));
    if ((meusApps && meusApps.length === 1) || fixo) apps = [];
    var bar = el('div', 'bar');
    apps.forEach(function (a) {
      var b = el('button', 'btn sm', a === 'todos' ? t('all') : APP_NAMES[a]); b.type = 'button';
      if (a !== filtro) b.style.opacity = '.55';
      b.addEventListener('click', function () { filtro = a; render(); });
      add(bar, b);
    });
    bar.style.justifyContent = 'flex-start';
    if (apps.length) add(root, bar);

    var lista = itens.filter(function (m) {
      if (!noIdioma(m)) return false;
      if (fixo) return !m.app || m.app === 'todos' || m.app === fixo;
      if (meusApps && m.app && m.app !== 'todos' && meusApps.indexOf(m.app) < 0) return false;
      return filtro === 'todos' || !m.app || m.app === 'todos' || m.app === filtro;
    });
    if (!lista.length) add(root, el('p', 'muted', t('empty')));
    // Seções: logos, prints e materiais de divulgação (sem "secao": imagens = prints, o resto = divulgação).
    var SECOES = [['logo', 'secLogo'], ['prints', 'secPrints'], ['divulgacao', 'secDiv']];
    function secaoDe(m) { return m.secao || (m.tipo === 'imagem' ? 'prints' : 'divulgacao'); }
    SECOES.forEach(function (sc) {
      var grupo = lista.filter(function (m) { return secaoDe(m) === sc[0]; });
      if (!grupo.length) return;
      add(root, el('h2', 'mat-sec', t(sc[1])));
      grupo.forEach(function (m) { add(root, item(m)); });
    });
  }

  Array.prototype.forEach.call(document.querySelectorAll('.lang button'), function (b) {
    b.addEventListener('click', function () { lang = b.getAttribute('data-lang'); try { localStorage.setItem('aff_lang', lang); } catch (e) {} render(); });
  });
  lang = detectLang();

  var sessao = null; try { sessao = localStorage.getItem('aff_sessao'); } catch (e) {}
  Promise.all([
    fetch('/afiliado/materiais/materiais.json', { cache: 'no-cache' }).then(function (r) { return r.json(); }).catch(function () { return { itens: [] }; }),
    sessao ? fetch(API + '/portal/resumo', { headers: { Authorization: 'Bearer ' + sessao } }).then(function (r) { return r.ok ? r.json() : null; }).catch(function () { return null; }) : Promise.resolve(null),
  ]).then(function (res) {
    itens = (res[0] && res[0].itens) || [];
    codigo = res[1] && res[1].afiliado ? res[1].afiliado.codigo : null;
    if (res[1] && res[1].afiliado) meusApps = res[1].afiliado.apps.map(function (a) { return a === 'beleza' ? 'lumora' : a; });
    render();
  });
})();
