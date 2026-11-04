/* Contador de visitas anônimo do aura-dev-app.com (alimenta a aba "Visitas" do Dashboard).
   Sem cookie e sem identificador guardado no navegador. Só conta no site de verdade (não em localhost/preview),
   não conta quem pede "Do Not Track" nem navegador automatizado.
   Para NÃO contar as suas próprias visitas neste navegador, abra uma vez: https://aura-dev-app.com/?nocount=1
   (para voltar a contar: ?nocount=0). */
(function () {
  'use strict';
  var API = 'https://estoque-backend-production-90aa.up.railway.app/visitas';
  var ls = null;
  try {
    if (!/^(www\.)?aura-dev-app\.com$/.test(location.hostname)) return;
    if (navigator.webdriver || navigator.doNotTrack === '1') return;
    try { ls = window.localStorage; } catch (e) { ls = null; }
    if (ls && /[?&]nocount=1/.test(location.search)) ls.setItem('aura_nocount', '1');
    if (ls && /[?&]nocount=0/.test(location.search)) ls.removeItem('aura_nocount');
    if (ls && ls.getItem('aura_nocount') === '1') return;
  } catch (e) { return; }

  function origem() {
    try {
      var q = new URLSearchParams(location.search);
      var u = q.get('utm_source') || q.get('ref');
      if (u) return String(u).slice(0, 40).replace(/[^a-zA-Z0-9.\-_]/g, '');
      if (document.referrer) {
        var h = new URL(document.referrer).hostname.replace(/^www\./, '');
        if (h && !/(^|\.)aura-dev-app\.com$/.test(h)) return h;
      }
    } catch (e) {}
    return '';
  }

  var ultima = { k: '', t: 0 };
  function enviar(pagina) {
    try {
      var agora = Date.now();
      if (pagina === ultima.k && agora - ultima.t < 3000) return; // evita contar 2x a mesma tela
      ultima = { k: pagina, t: agora };
      var corpo = JSON.stringify({ p: pagina, l: (document.documentElement.lang || '').slice(0, 2).toLowerCase(), r: origem() });
      if (navigator.sendBeacon && navigator.sendBeacon(API, new Blob([corpo], { type: 'text/plain;charset=UTF-8' }))) return;
      fetch(API, { method: 'POST', headers: { 'Content-Type': 'text/plain;charset=UTF-8' }, body: corpo, keepalive: true }).catch(function () {});
    } catch (e) {}
  }
  window.auraTrack = enviar; // a home chama isto ao abrir a página de detalhes de um app (#app/<slug>)

  function paginaAtual() {
    var h = location.hash || '';
    return location.pathname + (/^#app\/[a-z0-9_\-]+$/i.test(h) ? h : '');
  }
  // Espera a página aplicar o idioma (home e afiliados trocam o idioma ao carregar) antes de contar.
  function inicio() { setTimeout(function () { enviar(paginaAtual()); }, 500); }
  if (document.readyState === 'complete') inicio(); else window.addEventListener('load', inicio);
})();
