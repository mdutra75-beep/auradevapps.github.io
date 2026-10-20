/* Landing do Lumora — comportamento compartilhado (PT/EN/ES).
   Sem dependências. Nada de dado pessoal vai para analytics. */
(function () {
  'use strict';

  var LANG = document.documentElement.getAttribute('data-lang') || 'pt';

  /* ---------- Configuração editável ---------- */
  var CONFIG = {
    // Formulário de leads (POST /leads do estoque-backend).
    // Enquanto leadAppId for null, o formulário fica escondido e a página
    // mostra só o botão "Falar com a equipe" (e-mail).
    leadEndpoint: 'https://estoque-backend-production-90aa.up.railway.app/leads',
    leadAppId: null,
  };

  /* ---------- Analytics (sem ferramenta de terceiros por padrão) ----------
     track(evento, parametros) envia para gtag / dataLayer SE existirem na
     página (ex.: depois que um GA4/GTM for adicionado, com consentimento).
     Sem nenhum dos dois, não faz nada. Eventos: page_view, language_select,
     hero_cta_click, store_click, booking_demo_click, lead_form_start,
     lead_form_submit, faq_open, scroll_depth, video_play. */
  function track(name, params) {
    params = params || {};
    params.language = LANG;
    try {
      if (typeof window.gtag === 'function') window.gtag('event', name, params);
      else if (Array.isArray(window.dataLayer)) window.dataLayer.push({ event: name, params: params });
    } catch (e) { /* analytics nunca pode quebrar a página */ }
  }
  window.lumoraTrack = track;

  track('page_view', { path: location.pathname });

  /* ---------- Cliques rastreados via data-track ---------- */
  document.addEventListener('click', function (ev) {
    var el = ev.target.closest('[data-track]');
    if (!el) return;
    var p = {};
    if (el.dataset.store) p.store = el.dataset.store;
    if (el.dataset.platform) p.platform = el.dataset.platform;
    if (el.dataset.destination) p.destination = el.dataset.destination;
    if (el.dataset.to) { p.from = LANG; p.to = el.dataset.to; }
    track(el.dataset.track, p);
  });

  /* ---------- Idioma: lembra a escolha manual ---------- */
  try {
    document.querySelectorAll('.lang-switch a').forEach(function (a) {
      a.addEventListener('click', function () {
        localStorage.setItem('lumora_landing_lang', a.dataset.to);
      });
    });
    // Na raiz (/lumora/), se a pessoa nunca escolheu e o navegador não é PT,
    // sugere o idioma certo sem forçar (banner discreto, não redireciona).
    if (location.pathname.replace(/\/+$/, '') === '/lumora') {
      var saved = localStorage.getItem('lumora_landing_lang');
      var nav = (navigator.language || 'pt').slice(0, 2).toLowerCase();
      var want = saved || (nav === 'en' || nav === 'es' ? nav : 'pt');
      if (want !== 'pt') {
        var link = document.querySelector('.lang-switch a[data-to="' + want + '"]');
        if (link) {
          var bar = document.getElementById('lang-suggest');
          if (bar) {
            bar.hidden = false;
            var a = bar.querySelector('a');
            a.href = link.href;
            a.textContent = link.dataset.suggest || a.textContent;
          }
        }
      }
    }
  } catch (e) { /* localStorage pode estar bloqueado */ }

  /* ---------- FAQ: evento ao abrir ---------- */
  document.querySelectorAll('.faq details').forEach(function (d, i) {
    d.addEventListener('toggle', function () {
      if (d.open) track('faq_open', { question_id: 'faq_' + (i + 1) });
    });
  });

  /* ---------- Profundidade de rolagem ---------- */
  var marks = [25, 50, 75, 90], done = {};
  function onScroll() {
    var h = document.documentElement;
    var pct = ((h.scrollTop + window.innerHeight) / h.scrollHeight) * 100;
    marks.forEach(function (m) {
      if (pct >= m && !done[m]) { done[m] = true; track('scroll_depth', { percent: m }); }
    });
  }
  window.addEventListener('scroll', onScroll, { passive: true });

  /* ---------- Entrada suave dos blocos (respeita reduced-motion) ---------- */
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var items = document.querySelectorAll('.reveal');
  if (reduce || !('IntersectionObserver' in window)) {
    items.forEach(function (el) { el.classList.add('in'); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
      });
    }, { threshold: 0.12 });
    items.forEach(function (el) { io.observe(el); });
  }

  /* ---------- Vídeos do YouTube (lista em videos.js) ---------- */
  function ytThumb(id) { return 'https://i.ytimg.com/vi/' + id + '/hqdefault.jpg'; }
  function mountVideo(box, v) {
    box.innerHTML = '';
    var btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'yt-facade';
    btn.setAttribute('aria-label', (box.dataset.playLabel || 'Play') + ': ' + v.titulo);
    btn.style.backgroundImage = 'url(' + ytThumb(v.id) + ')';
    btn.innerHTML = '<span class="yt-play" aria-hidden="true"></span>';
    btn.addEventListener('click', function () {
      track('video_play', { video_id: v.id });
      var f = document.createElement('iframe');
      f.src = 'https://www.youtube-nocookie.com/embed/' + encodeURIComponent(v.id) + '?autoplay=1&rel=0';
      f.title = v.titulo;
      f.allow = 'accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture; fullscreen';
      f.allowFullscreen = true;
      f.className = 'yt-frame';
      box.innerHTML = '';
      box.appendChild(f);
    });
    box.appendChild(btn);
  }
  var vids = (window.LUMORA_VIDEOS && window.LUMORA_VIDEOS[LANG]) || [];
  vids = vids.filter(function (v) { return v && /^[A-Za-z0-9_-]{6,}$/.test(v.id || ''); });
  var vSection = document.getElementById('videos');
  if (vSection && vids.length) {
    vSection.hidden = false;
    document.querySelectorAll('[data-needs-videos]').forEach(function (n) { n.hidden = false; });
    var main = vSection.querySelector('.video-main');
    var list = vSection.querySelector('.video-list');
    mountVideo(main, vids[0]);
    var cap = vSection.querySelector('.video-caption');
    if (cap) cap.textContent = vids[0].titulo;
    vids.slice(1).forEach(function (v) {
      var b = document.createElement('button');
      b.type = 'button';
      b.className = 'video-thumb';
      b.innerHTML = '<img loading="lazy" width="160" height="90" alt="" src="' + ytThumb(v.id) + '"><span></span>';
      b.lastChild.textContent = v.titulo;
      b.addEventListener('click', function () {
        mountVideo(main, v);
        if (cap) cap.textContent = v.titulo;
        main.querySelector('.yt-facade').click();
      });
      list.appendChild(b);
    });
  }

  /* ---------- Formulário de leads ---------- */
  var form = document.getElementById('lead-form');
  var fallback = document.getElementById('lead-fallback');
  if (form) {
    if (!CONFIG.leadAppId) {
      form.hidden = true;
      if (fallback) fallback.hidden = false;
    } else {
      var started = false;
      form.addEventListener('input', function () {
        if (!started) { started = true; track('lead_form_start'); }
      });
      form.addEventListener('submit', function (e) {
        e.preventDefault();
        var msg = document.getElementById('lead-msg');
        var btn = form.querySelector('button[type=submit]');
        var data = new FormData(form);
        if (data.get('website')) return; // honeypot anti-spam
        var email = (data.get('email') || '').toString().trim();
        var whats = (data.get('whatsapp') || '').toString().trim();
        if (!email && !whats) {
          msg.textContent = form.dataset.errContact;
          msg.className = 'form-msg err';
          return;
        }
        btn.disabled = true;
        msg.textContent = '';
        fetch(CONFIG.leadEndpoint, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            app_id: CONFIG.leadAppId,
            nome: (data.get('nome') || '').toString().trim() || null,
            email: email || null,
            whatsapp: whats || null,
            origem: 'lumora-landing-' + LANG,
            opt_in_email: !!data.get('opt_in'),
            opt_in_whatsapp: false,
          }),
        }).then(function (r) {
          if (!r.ok) throw new Error('http ' + r.status);
          track('lead_form_submit');
          form.reset();
          msg.textContent = form.dataset.ok;
          msg.className = 'form-msg ok';
        }).catch(function () {
          msg.textContent = form.dataset.errSend;
          msg.className = 'form-msg err';
        }).then(function () { btn.disabled = false; });
      });
    }
  }
})();
