/* Área do afiliado: login por link no e-mail (sem senha), resumo, links, comissões e cadastro de pagamento.
   Todo texto vindo do servidor entra por textContent (nunca innerHTML). */
(function () {
  'use strict';

  var API = 'https://estoque-backend-production-90aa.up.railway.app';
  var qs = new URLSearchParams(location.search);
  if (/^(localhost|127\.0\.0\.1)$/.test(location.hostname) && qs.get('api')) API = qs.get('api');
  var KEY = 'aff_sessao';
  var LANGS = ['en', 'pt', 'es'];

  var S = {
    en: {
      title: 'Affiliate area', loginT: 'Sign in to your affiliate area',
      loginD: 'Type the email you used in your application. We send you a sign-in link (no password).',
      email: 'Your email', send: 'Send sign-in link', sent: 'If this email belongs to an approved affiliate, a sign-in link is on its way. It expires in 15 minutes.',
      badLink: 'This link is invalid or has expired. Ask for a new one below.', wait: 'Please wait…', err: 'Something went wrong. Try again.',
      hello: 'Hi, {n}', out: 'Sign out', yourCode: 'Your referral code', apps: 'Your links',
      android: 'Android link (the app reads your code automatically)', copy: 'Copy', copied: 'Copied!',
      ios: 'iPhone: your audience types this code in the app (Settings or the subscription screen) and taps "Redeem discount".',
      iosM: 'Monthly plan code', iosA: 'Annual plan code',
      results: 'Your results', linked: 'Accounts that used your code', paying: 'Paying subscribers',
      money: 'Your commissions', toReceive: 'Accruing', toPay: 'Approved, to be paid', paid: 'Paid',
      moneyHint: 'Commissions are counted on the amount we actually receive from the stores, and paid by PayPal within 5 days after we receive it. Values can take some weeks to appear (store reporting delay).',
      awaiting: '{n} sale(s) still waiting for the store to report the net amount.',
      recent: 'Latest commissions', period: 'Month', app: 'App', month: 'Sub. month', pct: '%', value: 'Commission', status: 'Status', acct: 'Account',
      st: { devida: 'Accruing', fechada: 'Approved', aguardando_liquido: 'Waiting store data', estornada: 'Refunded' },
      none: 'No commissions yet. They appear after someone who used your code pays for a subscription.',
      pay: 'Payout', payD: 'Where do you want to receive your commissions? We pay through PayPal.',
      payTutorial: 'No PayPal yet? Create a free account at paypal.com (personal or business), confirm your email, and type that same email below. Make sure it can receive international payments.',
      payEmail: 'PayPal account email', paySave: 'Save', paySaved: 'Saved. We will pay to this account.', payBad: 'Please type a valid email.',
      payCurrent: 'Current: PayPal · {c}', payNone: 'Not set yet. Payouts only go out after you fill this in.',
      mats: 'Promotion materials', matsD: 'Images, videos and ready-made texts to help you promote.', matsGo: 'Open materials',
    },
    pt: {
      title: 'Área do afiliado', loginT: 'Entre na sua área do afiliado',
      loginD: 'Digite o e-mail que você usou na inscrição. Enviamos um link de acesso (sem senha).',
      email: 'Seu e-mail', send: 'Enviar link de acesso', sent: 'Se este e-mail for de um afiliado aprovado, um link de acesso está a caminho. Ele vale 15 minutos.',
      badLink: 'Este link é inválido ou expirou. Peça um novo abaixo.', wait: 'Aguarde…', err: 'Algo deu errado. Tente de novo.',
      hello: 'Olá, {n}', out: 'Sair', yourCode: 'Seu código de indicação', apps: 'Seus links',
      android: 'Link do Android (o app lê seu código sozinho)', copy: 'Copiar', copied: 'Copiado!',
      ios: 'iPhone: seu público digita este código no app (Configurações ou tela de assinatura) e toca em "Resgatar desconto".',
      iosM: 'Código do plano mensal', iosA: 'Código do plano anual',
      results: 'Seus resultados', linked: 'Contas que usaram seu código', paying: 'Assinantes pagantes',
      money: 'Suas comissões', toReceive: 'Acumulando', toPay: 'Aprovado, a pagar', paid: 'Pago',
      moneyHint: 'As comissões são contadas sobre o valor que de fato recebemos das lojas e pagas por PayPal em até 5 dias depois que recebemos. Os valores podem levar algumas semanas para aparecer (atraso dos relatórios das lojas).',
      awaiting: '{n} venda(s) ainda esperando a loja informar o valor líquido.',
      recent: 'Últimas comissões', period: 'Mês', app: 'App', month: 'Mês da assin.', pct: '%', value: 'Comissão', status: 'Situação', acct: 'Conta',
      st: { devida: 'Acumulando', fechada: 'Aprovada', aguardando_liquido: 'Aguardando a loja', estornada: 'Estornada' },
      none: 'Ainda não há comissões. Elas aparecem depois que alguém que usou seu código paga uma assinatura.',
      pay: 'Pagamento', payD: 'Onde você quer receber suas comissões? Pagamos por PayPal.',
      payTutorial: 'Ainda não tem PayPal? Crie uma conta gratuita em paypal.com (pessoal ou empresarial), confirme o e-mail e digite o mesmo e-mail abaixo. Confira se ela pode receber pagamentos do exterior.',
      payEmail: 'E-mail da sua conta PayPal', paySave: 'Salvar', paySaved: 'Salvo. Vamos pagar nesta conta.', payBad: 'Digite um e-mail válido.',
      payCurrent: 'Atual: PayPal · {c}', payNone: 'Ainda não cadastrado. Os pagamentos só saem depois que você preencher isto.',
      mats: 'Materiais para divulgação', matsD: 'Imagens, vídeos e textos prontos para ajudar na divulgação.', matsGo: 'Abrir materiais',
    },
    es: {
      title: 'Área del afiliado', loginT: 'Entra a tu área de afiliado',
      loginD: 'Escribe el correo que usaste en tu solicitud. Te enviamos un enlace de acceso (sin contraseña).',
      email: 'Tu correo', send: 'Enviar enlace de acceso', sent: 'Si este correo es de un afiliado aprobado, un enlace de acceso va en camino. Vale 15 minutos.',
      badLink: 'Este enlace no es válido o venció. Pide uno nuevo abajo.', wait: 'Espera…', err: 'Algo salió mal. Inténtalo de nuevo.',
      hello: 'Hola, {n}', out: 'Salir', yourCode: 'Tu código de referido', apps: 'Tus enlaces',
      android: 'Enlace de Android (la app lee tu código sola)', copy: 'Copiar', copied: '¡Copiado!',
      ios: 'iPhone: tu audiencia escribe este código en la app (Ajustes o pantalla de suscripción) y toca "Canjear descuento".',
      iosM: 'Código del plan mensual', iosA: 'Código del plan anual',
      results: 'Tus resultados', linked: 'Cuentas que usaron tu código', paying: 'Suscriptores que pagan',
      money: 'Tus comisiones', toReceive: 'Acumulando', toPay: 'Aprobado, por pagar', paid: 'Pagado',
      moneyHint: 'Las comisiones se calculan sobre el monto que realmente recibimos de las tiendas y se pagan por PayPal dentro de 5 días después de recibirlo. Los valores pueden tardar unas semanas en aparecer (retraso de los reportes de las tiendas).',
      awaiting: '{n} venta(s) esperando que la tienda informe el monto neto.',
      recent: 'Últimas comisiones', period: 'Mes', app: 'App', month: 'Mes de susc.', pct: '%', value: 'Comisión', status: 'Estado', acct: 'Cuenta',
      st: { devida: 'Acumulando', fechada: 'Aprobada', aguardando_liquido: 'Esperando la tienda', estornada: 'Reembolsada' },
      none: 'Aún no hay comisiones. Aparecen cuando alguien que usó tu código paga una suscripción.',
      pay: 'Pago', payD: '¿Dónde quieres recibir tus comisiones? Pagamos por PayPal.',
      payTutorial: '¿Aún no tienes PayPal? Crea una cuenta gratis en paypal.com (personal o empresa), confirma tu correo y escribe ese mismo correo abajo. Verifica que pueda recibir pagos del exterior.',
      payEmail: 'Correo de tu cuenta PayPal', paySave: 'Guardar', paySaved: 'Guardado. Pagaremos a esta cuenta.', payBad: 'Escribe un correo válido.',
      payCurrent: 'Actual: PayPal · {c}', payNone: 'Aún sin registrar. Los pagos solo salen después de llenar esto.',
      mats: 'Materiales para promocionar', matsD: 'Imágenes, videos y textos listos para ayudarte a promocionar.', matsGo: 'Abrir materiales',
    },
  };

  var lang = 'en';
  var root = document.getElementById('app');
  function t(k) { return (S[lang] && S[lang][k]) || S.en[k] || k; }
  function fill(s, o) { return String(s).replace(/\{(\w+)\}/g, function (_, k) { return o[k]; }); }

  function detectLang() {
    var q = (qs.get('lang') || '').toLowerCase();
    if (LANGS.indexOf(q) >= 0) return q;
    try { var s = localStorage.getItem('aff_lang'); if (LANGS.indexOf(s) >= 0) return s; } catch (e) {}
    var p = (navigator.languages && navigator.languages.length) ? navigator.languages : [navigator.language || 'en'];
    for (var i = 0; i < p.length; i++) { var n = String(p[i] || '').slice(0, 2).toLowerCase(); if (LANGS.indexOf(n) >= 0) return n; }
    return 'en';
  }
  function setLang(l) {
    lang = l;
    try { localStorage.setItem('aff_lang', l); } catch (e) {}
    document.documentElement.lang = l === 'pt' ? 'pt-BR' : l;
    document.title = t('title') + ' | Aura Dev Apps';
    Array.prototype.forEach.call(document.querySelectorAll('.lang button'), function (b) { b.setAttribute('aria-pressed', String(b.getAttribute('data-lang') === l)); });
    render();
  }

  // ── helpers de DOM ─────────────────────────────────────────────────────────
  function el(tag, cls, text) { var e = document.createElement(tag); if (cls) e.className = cls; if (text != null) e.textContent = text; return e; }
  function add(p) { for (var i = 1; i < arguments.length; i++) if (arguments[i]) p.appendChild(arguments[i]); return p; }
  function card() { return el('div', 'card'); }
  function money(v, cur) {
    try { return new Intl.NumberFormat(lang === 'pt' ? 'pt-BR' : lang, { style: 'currency', currency: cur }).format(Number(v)); } catch (e) { return v + ' ' + cur; }
  }
  function copyRow(value) {
    var row = el('div', 'row-copy');
    var inp = el('input'); inp.type = 'text'; inp.readOnly = true; inp.value = value;
    var b = el('button', 'btn sm', t('copy')); b.type = 'button';
    b.addEventListener('click', function () {
      function ok() { b.textContent = t('copied'); setTimeout(function () { b.textContent = t('copy'); }, 1600); }
      if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(value).then(ok, function () { inp.select(); document.execCommand('copy'); ok(); });
      else { inp.select(); document.execCommand('copy'); ok(); }
    });
    return add(row, inp, b);
  }

  // ── API ────────────────────────────────────────────────────────────────────
  function sessao() { try { return localStorage.getItem(KEY); } catch (e) { return null; } }
  function api(path, body, auth) {
    var h = { 'Content-Type': 'application/json' };
    if (auth) h.Authorization = 'Bearer ' + auth;
    return fetch(API + path, { method: body === undefined ? 'GET' : 'POST', headers: h, body: body === undefined ? undefined : JSON.stringify(body) })
      .then(function (r) { return r.json().catch(function () { return {}; }).then(function (j) { return { status: r.status, data: j }; }); });
  }

  // ── telas ──────────────────────────────────────────────────────────────────
  var flash = '';
  function render() {
    root.textContent = '';
    var s = sessao();
    if (!s) return renderLogin();
    root.appendChild(el('p', 'muted', t('wait')));
    api('/portal/resumo', undefined, s).then(function (r) {
      if (r.status === 401) { try { localStorage.removeItem(KEY); } catch (e) {} return renderLogin(); }
      if (r.status !== 200) { root.textContent = ''; return add(root, el('div', 'msg err show', t('err'))); }
      renderPainel(r.data);
    }).catch(function () { root.textContent = ''; add(root, el('div', 'msg err show', t('err'))); });
  }

  function renderLogin() {
    root.textContent = '';
    var c = card();
    add(c, el('h1', null, t('loginT')), el('p', 'muted', t('loginD')));
    if (flash) { add(c, el('div', 'msg err show', flash)); flash = ''; }
    var form = el('form'); form.noValidate = true;
    var lab = el('label', null, t('email')); lab.setAttribute('for', 'em');
    var inp = el('input'); inp.type = 'email'; inp.id = 'em'; inp.autocomplete = 'email'; inp.maxLength = 254; inp.required = true;
    var msg = el('div', 'msg'); msg.style.marginTop = '.8rem';
    var btn = el('button', 'btn', t('send')); btn.type = 'submit'; btn.style.marginTop = '1rem';
    add(form, lab, inp, btn, msg);
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!inp.value || inp.value.indexOf('@') < 1) { msg.className = 'msg err show'; msg.textContent = t('err'); return; }
      btn.disabled = true; msg.className = 'msg';
      api('/portal/entrar', { email: inp.value.trim(), idioma: lang }).then(function (r) {
        btn.disabled = false;
        msg.className = 'msg ' + (r.status === 200 ? 'ok' : 'err') + ' show';
        msg.textContent = r.status === 200 ? t('sent') : t('err');
      }).catch(function () { btn.disabled = false; msg.className = 'msg err show'; msg.textContent = t('err'); });
    });
    add(c, form); add(root, c);
  }

  function renderPainel(d) {
    root.textContent = '';
    var bar = el('div', 'bar');
    add(bar, el('h1', null, fill(t('hello'), { n: String(d.afiliado.nome).split(' ')[0] })));
    var out = el('button', 'linkbtn', t('out')); out.type = 'button';
    out.addEventListener('click', function () {
      api('/portal/sair', {}, sessao()).catch(function () {});
      try { localStorage.removeItem(KEY); } catch (e) {} renderLogin();
    });
    add(bar, out); add(root, bar);

    // Código e links
    add(root, el('h2', null, t('apps')));
    d.links.forEach(function (l) {
      var c = card();
      add(c, el('h3', null, l.nome), el('div', 'lbl', t('yourCode')), el('div', 'code', l.codigo));
      add(c, el('div', 'lbl', t('android')), copyRow(l.android));
      add(c, el('p', 'hint', t('ios')));
      var g = el('div', 'grid2');
      var a1 = el('div'); add(a1, el('div', 'lbl', t('iosM')), el('div', 'code', l.ios_codigo_mensal));
      add(g, a1);
      if (l.ios_codigo_anual) { var a2 = el('div'); add(a2, el('div', 'lbl', t('iosA')), el('div', 'code', l.ios_codigo_anual)); add(g, a2); }
      add(c, g); add(root, c);
    });

    // Resultados
    add(root, el('h2', null, t('results')));
    var gr = el('div', 'grid2');
    d.links.forEach(function (l) {
      var v = d.conversoes[l.app] || { contas_vinculadas: 0, assinantes_pagantes: 0 };
      var c = card();
      add(c, el('div', 'lbl', l.nome + ' · ' + t('linked')), el('div', 'big', String(v.contas_vinculadas)),
        el('div', 'lbl', t('paying')), el('div', 'big', String(v.assinantes_pagantes)));
      add(gr, c);
    });
    add(root, gr);

    // Dinheiro
    add(root, el('h2', null, t('money')));
    var gm = el('div', 'grid2');
    if (!d.valores.length) { var z = card(); add(z, el('div', 'lbl', t('toReceive')), el('div', 'big', '—')); add(gm, z); }
    d.valores.forEach(function (v) {
      var c = card();
      add(c, el('div', 'lbl', t('toReceive')), el('div', 'big', money(v.a_receber, v.moeda)),
        el('div', 'lbl', t('toPay')), el('div', 'big', money(v.a_pagar, v.moeda)),
        el('div', 'lbl', t('paid')), el('div', 'big', money(v.pago, v.moeda)));
      add(gm, c);
    });
    add(root, gm, el('p', 'hint', t('moneyHint')));
    if (d.aguardando_liquido > 0) add(root, el('p', 'hint', fill(t('awaiting'), { n: d.aguardando_liquido })));

    add(root, el('h2', null, t('recent')));
    if (!d.recentes.length) add(root, el('p', 'muted', t('none')));
    else {
      var tb = el('table', 'tbl'), hd = el('tr');
      ['period', 'app', 'month', 'pct', 'value', 'status', 'acct'].forEach(function (k) { add(hd, el('th', null, t(k))); });
      add(tb, hd);
      d.recentes.forEach(function (r) {
        var tr = el('tr');
        add(tr, el('td', null, r.periodo), el('td', null, r.app === 'beleza' ? 'Lumora' : 'ClipIt'), el('td', null, String(r.mes_n)), el('td', null, r.percentual + '%'),
          el('td', null, r.comissao == null ? '—' : money(r.comissao, r.moeda || 'USD')), el('td', null, (t('st')[r.status]) || r.status), el('td', null, r.conta));
        add(tb, tr);
      });
      var wrap = el('div'); wrap.style.overflowX = 'auto'; add(wrap, tb); add(root, wrap);
    }

    // Pagamento
    add(root, el('h2', null, t('pay')));
    var pc = card();
    add(pc, el('p', null, t('payD')), el('p', 'hint', t('payTutorial')));
    add(pc, el('p', 'hint', d.pagamento.conta ? fill(t('payCurrent'), { c: d.pagamento.conta }) : t('payNone')));
    var f = el('form'); f.noValidate = true;
    var lab = el('label', null, t('payEmail')); lab.setAttribute('for', 'pp');
    var inp = el('input'); inp.type = 'email'; inp.id = 'pp'; inp.maxLength = 254; inp.autocomplete = 'off';
    var m = el('div', 'msg'); m.style.marginTop = '.8rem';
    var sv = el('button', 'btn sm', t('paySave')); sv.type = 'submit'; sv.style.marginTop = '.9rem';
    add(f, lab, inp, sv, m);
    f.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!inp.value || inp.value.indexOf('@') < 1) { m.className = 'msg err show'; m.textContent = t('payBad'); return; }
      sv.disabled = true;
      api('/portal/pagamento', { metodo: 'paypal', conta: inp.value.trim() }, sessao()).then(function (r) {
        sv.disabled = false;
        m.className = 'msg ' + (r.status === 200 ? 'ok' : 'err') + ' show';
        m.textContent = r.status === 200 ? t('paySaved') : (r.status === 400 ? t('payBad') : t('err'));
        if (r.status === 200) inp.value = '';
      }).catch(function () { sv.disabled = false; m.className = 'msg err show'; m.textContent = t('err'); });
    });
    add(pc, f); add(root, pc);

    // Materiais
    add(root, el('h2', null, t('mats')));
    var mc = card(); var a = el('a', 'btn sm', t('matsGo')); a.href = '/afiliado/materiais/?lang=' + lang;
    add(mc, el('p', 'muted', t('matsD')), a); add(root, mc);
  }

  // ── início ─────────────────────────────────────────────────────────────────
  Array.prototype.forEach.call(document.querySelectorAll('.lang button'), function (b) {
    b.addEventListener('click', function () { setLang(b.getAttribute('data-lang')); });
  });
  lang = detectLang();
  var m = /[#&]t=([A-Za-z0-9_-]{20,100})/.exec(location.hash);
  if (m) {
    // Troca o link do e-mail por uma sessão e já tira o token da barra de endereço.
    history.replaceState(null, '', location.pathname + location.search);
    api('/portal/sessao', { token: m[1] }).then(function (r) {
      if (r.status === 200 && r.data.sessao) { try { localStorage.setItem(KEY, r.data.sessao); } catch (e) {} } else { flash = S[lang].badLink; }
      setLang(lang);
    }).catch(function () { flash = S[lang].err; setLang(lang); });
  } else setLang(lang);
})();
