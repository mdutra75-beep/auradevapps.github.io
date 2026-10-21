/* Landing do Lumora — comportamento compartilhado. Sem dependências.
   Nada de dado pessoal vai para analytics. */
(function () {
  'use strict';

  var root = document.documentElement;
  var LANG = root.getAttribute('data-lang') || 'pt';
  var AUD = root.getAttribute('data-aud') || 'br';
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

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
     Sem nenhum dos dois, não faz nada. Eventos: page_view, audience_select,
     language_select, hero_cta_click, store_click, lead_form_start,
     lead_form_submit, faq_open, scroll_depth, video_play. */
  function track(name, params) {
    params = params || {};
    params.language = LANG;
    params.audience = AUD;
    try {
      if (typeof window.gtag === 'function') window.gtag('event', name, params);
      else if (Array.isArray(window.dataLayer)) window.dataLayer.push({ event: name, params: params });
    } catch (e) { /* analytics nunca pode quebrar a página */ }
  }
  window.lumoraTrack = track;
  track('page_view', { path: location.pathname });

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

  /* ---------- Menu superior: fica sólido depois do topo ---------- */
  var nav = document.getElementById('nav');
  var stickyCta = document.querySelector('.sticky-cta');
  function navState() {
    if (nav) nav.classList.toggle('solid', window.scrollY > 40);
    if (stickyCta) stickyCta.classList.toggle('show', window.scrollY > window.innerHeight * 0.7);
  }
  navState();
  window.addEventListener('scroll', navState, { passive: true });

  /* ---------- Menu de idioma: fecha ao clicar fora ---------- */
  var langMenu = document.querySelector('.lang-menu');
  if (langMenu) {
    document.addEventListener('click', function (e) { if (!langMenu.contains(e.target)) langMenu.open = false; });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') langMenu.open = false; });
  }

  /* ---------- FAQ: evento ao abrir ---------- */
  document.querySelectorAll('.faq details').forEach(function (d, i) {
    d.addEventListener('toggle', function () { if (d.open) track('faq_open', { question_id: 'faq_' + (i + 1) }); });
  });

  /* ---------- Profundidade de rolagem ---------- */
  var marks = [25, 50, 75, 90], done = {};
  window.addEventListener('scroll', function () {
    var h = root;
    var pct = ((h.scrollTop + window.innerHeight) / h.scrollHeight) * 100;
    marks.forEach(function (m) { if (pct >= m && !done[m]) { done[m] = true; track('scroll_depth', { percent: m }); } });
  }, { passive: true });

  /* ---------- Declaração: cada linha "acende" ao entrar na tela ---------- */
  var lit = document.querySelectorAll('.st-line, .st-end');
  if (reduce || !('IntersectionObserver' in window)) {
    lit.forEach(function (el) { el.classList.add('lit'); });
  } else {
    var io1 = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('lit'); io1.unobserve(e.target); } });
    }, { rootMargin: '0px 0px -30% 0px', threshold: 0.2 });
    lit.forEach(function (el) { io1.observe(el); });
  }

  /* ---------- Idiomas (EUA): seletor que troca a tela do celular ---------- */
  var ldBtns = document.querySelectorAll('.lang-chip');
  var ldImgs = document.querySelectorAll('.ld-img');
  if (ldBtns.length) {
    var order = ['pt', 'en', 'es'], cur = order.indexOf(LANG), timer = null, touched = false;
    var setLd = function (l) {
      cur = order.indexOf(l);
      ldBtns.forEach(function (b) { b.setAttribute('aria-pressed', b.dataset.set === l ? 'true' : 'false'); });
      ldImgs.forEach(function (img) { img.classList.toggle('on', img.dataset.lang === l); });
    };
    ldBtns.forEach(function (b) {
      b.addEventListener('click', function () { touched = true; clearInterval(timer); setLd(b.dataset.set); });
    });
    var box = document.getElementById('idiomas');
    if (!reduce && box && 'IntersectionObserver' in window) {
      new IntersectionObserver(function (entries) {
        entries.forEach(function (e) {
          clearInterval(timer);
          if (e.isIntersecting && !touched) timer = setInterval(function () { setLd(order[(cur + 1) % 3]); }, 3200);
        });
      }, { threshold: 0.4 }).observe(box);
    }
  }

  /* ---------- Carrosséis (Salão/Studio e jornada do cliente): setas ao lado dos cartões ---------- */
  document.querySelectorAll('.jwrap').forEach(function (wrap) {
    var jt = wrap.querySelector('.jtrack');
    var jprev = wrap.querySelector('.jprev'), jnext = wrap.querySelector('.jnext');
    if (!jt || !jprev || !jnext) return;
    var jstep = function () { var c = jt.querySelector('.jcard'); return c.getBoundingClientRect().width + 19; };
    var jupd = function () {
      jprev.disabled = jt.scrollLeft < 8;
      jnext.disabled = jt.scrollLeft + jt.clientWidth >= jt.scrollWidth - 8;
    };
    [jprev, jnext].forEach(function (b) {
      b.addEventListener('click', function () {
        jt.scrollBy({ left: Number(b.dataset.dir) * jstep(), behavior: reduce ? 'auto' : 'smooth' });
      });
    });
    jt.addEventListener('scroll', jupd, { passive: true });
    window.addEventListener('resize', jupd);
    jt.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowRight') jnext.click();
      if (e.key === 'ArrowLeft') jprev.click();
    });
    jupd();
  });

  /* ---------- QR code flutuante: dá para fechar e some no final ---------- */
  var qr = document.getElementById('qr-card');
  if (qr) {
    var closed = false;
    try { closed = sessionStorage.getItem('lumora_qr_closed') === '1'; } catch (e) {}
    if (closed) qr.classList.add('hide');
    qr.querySelector('.qr-x').addEventListener('click', function () {
      qr.classList.add('hide');
      try { sessionStorage.setItem('lumora_qr_closed', '1'); } catch (e) {}
    });
    var fin = document.getElementById('baixar');
    if (fin && 'IntersectionObserver' in window) {
      new IntersectionObserver(function (entries) {
        entries.forEach(function (e) { if (!closed) qr.classList.toggle('hide', e.isIntersecting); });
      }, { threshold: 0.15 }).observe(fin);
    }
  }

  /* ---------- Vídeo do topo: YouTube (id em videos.js -> LUMORA_HERO) ---------- */
  var heroBox = document.getElementById('hero-video');
  var cfg = (window.LUMORA_HERO && window.LUMORA_HERO[AUD]) || {};
  var saveData = navigator.connection && navigator.connection.saveData;
  if (heroBox && cfg.src) {
    // vídeo do próprio site (sem som, em loop, tela cheia); versão leve no celular
    heroBox.hidden = false;
    var vid = document.createElement('video');
    vid.muted = true; vid.defaultMuted = true; vid.loop = true; vid.autoplay = true;
    vid.setAttribute('loop', '');
    vid.addEventListener('ended', function () { vid.currentTime = 0; vid.play().catch(function () {}); });
    vid.setAttribute('playsinline', ''); vid.setAttribute('aria-label', heroBox.dataset.title || 'Lumora');
    vid.preload = reduce || saveData ? 'none' : 'auto';
    if (cfg.poster) vid.poster = cfg.poster;
    var small = window.matchMedia && window.matchMedia('(max-width: 700px)').matches && cfg.srcMobile;
    vid.src = small ? cfg.srcMobile : cfg.src;
    heroBox.appendChild(vid);
    if (reduce || saveData) {
      vid.controls = true; vid.autoplay = false;
    } else {
      var pl = vid.play(); if (pl && pl.catch) pl.catch(function () { vid.controls = true; });
    }
  } else if (heroBox && /^[A-Za-z0-9_-]{6,}$/.test(cfg.youtube || '')) {
    heroBox.hidden = false;
    var hid = cfg.youtube;
    var htitle = cfg.titulo || heroBox.dataset.title || 'Lumora';
    heroBox.style.backgroundImage = 'url(https://i.ytimg.com/vi/' + hid + '/hqdefault.jpg)';
    heroBox.style.backgroundSize = 'cover';
    heroBox.style.backgroundPosition = 'center';
    var mountHero = function (autoplay) {
      var f = document.createElement('iframe');
      var q = autoplay
        ? '?autoplay=1&mute=1&loop=1&playlist=' + hid + '&playsinline=1&rel=0&modestbranding=1'
        : '?autoplay=1&rel=0&modestbranding=1&playsinline=1';
      f.src = 'https://www.youtube-nocookie.com/embed/' + encodeURIComponent(hid) + q;
      f.title = htitle;
      f.allow = 'accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture; fullscreen';
      f.allowFullscreen = true;
      f.className = 'yt-frame';
      heroBox.innerHTML = '';
      heroBox.appendChild(f);
    };
    if (reduce || saveData) {
      // sem autoplay: mostra a capa e só carrega ao clicar
      var hb = document.createElement('button');
      hb.type = 'button';
      hb.className = 'yt-facade';
      hb.setAttribute('aria-label', (heroBox.dataset.playLabel || 'Play') + ': ' + htitle);
      hb.innerHTML = '<span class="yt-play" aria-hidden="true"></span>';
      hb.addEventListener('click', function () { track('video_play', { video_id: hid, where: 'hero' }); mountHero(false); });
      heroBox.appendChild(hb);
    } else {
      // autoplay mudo em loop (o visitante pode ligar o som nos controles do player)
      var go = function () { mountHero(true); };
      if (document.readyState === 'complete') go(); else window.addEventListener('load', go);
    }
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
  var shortBox = document.getElementById('short-video');
  var shortId = (window.LUMORA_SHORT || {})[AUD];
  if (shortBox && /^[A-Za-z0-9_-]{6,}$/.test(shortId || '')) {
    shortBox.hidden = false;
    mountVideo(shortBox, { id: shortId, titulo: shortBox.dataset.title || 'Lumora' });
  }
  var howBox = document.getElementById('how-video');
  var howCfg = window.LUMORA_HOW || {};
  if (howBox && /^[A-Za-z0-9_-]{6,}$/.test(howCfg.id || '')) {
    howBox.hidden = false;
    mountVideo(howBox, { id: howCfg.id, titulo: howCfg.titulo || howBox.dataset.title || 'Lumora' });
  }

  var YT = window.LUMORA_VIDEOS || {};
  var vids = (YT[AUD === 'br' ? 'br' : LANG] || []).filter(function (v) { return v && /^[A-Za-z0-9_-]{6,}$/.test(v.id || ''); });
  var vSection = document.getElementById('videos');
  if (vSection && vids.length) {
    vSection.hidden = false;
    document.querySelectorAll('[data-needs-videos]').forEach(function (n) { n.hidden = false; });
    var main = vSection.querySelector('.video-main');
    var list = vSection.querySelector('.video-list');
    var cap = vSection.querySelector('.video-caption');
    mountVideo(main, vids[0]);
    if (cap) cap.textContent = vids[0].titulo;
    vids.slice(1).forEach(function (v) {
      var b = document.createElement('button');
      b.type = 'button';
      b.className = 'video-thumb';
      b.innerHTML = '<img loading="lazy" width="112" height="63" alt="" src="' + ytThumb(v.id) + '"><span></span>';
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
      form.addEventListener('input', function () { if (!started) { started = true; track('lead_form_start'); } });
      form.addEventListener('submit', function (e) {
        e.preventDefault();
        var msg = document.getElementById('lead-msg');
        var btn = form.querySelector('button[type=submit]');
        var data = new FormData(form);
        if (data.get('website')) return; // honeypot anti-spam
        var email = (data.get('email') || '').toString().trim();
        var whats = (data.get('whatsapp') || '').toString().trim();
        if (!email && !whats) { msg.textContent = form.dataset.errContact; msg.className = 'form-msg err'; return; }
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
            origem: 'lumora-landing-' + AUD + '-' + LANG,
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
