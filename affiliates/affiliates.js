/* Páginas de afiliados: idioma (EN/PT/ES), formulário, anti-spam, UTM e contagem de eventos.
   Os eventos vão pro NOSSO backend, agregados e sem dados pessoais. */
(function () {
  'use strict';

  var API = 'https://estoque-backend-production-90aa.up.railway.app';
  var qs = new URLSearchParams(location.search);
  // Só pra testes locais: ?api=http://localhost:3000
  if (/^(localhost|127\.0\.0\.1)$/.test(location.hostname) && qs.get('api')) API = qs.get('api');

  var PRODUCT = document.body.getAttribute('data-product'); // 'clipit' | 'lumora' | null (termos)
  var I18N = window.AFF_I18N || {};
  var LANGS = ['en', 'pt', 'es'];
  var loadedAt = Date.now();
  var lang = 'en';

  function $(s, r) { return (r || document).querySelector(s); }
  function $$(s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); }
  function t(key) {
    return (I18N[lang] && I18N[lang][key]) || (I18N.en && I18N.en[key]) || key;
  }
  function pt(key) { return t('p.' + PRODUCT + '.' + key); }

  // ── Idioma ────────────────────────────────────────────────────────────────
  function detectLang() {
    var q = (qs.get('lang') || '').toLowerCase();
    if (LANGS.indexOf(q) >= 0) return q;
    try {
      var saved = localStorage.getItem('aff_lang');
      if (LANGS.indexOf(saved) >= 0) return saved;
    } catch (e) {}
    // Idiomas do aparelho, na ordem de preferência: vale o primeiro que a página tem.
    var prefs = (navigator.languages && navigator.languages.length) ? navigator.languages : [navigator.language || 'en'];
    for (var i = 0; i < prefs.length; i++) {
      var n = String(prefs[i] || '').slice(0, 2).toLowerCase();
      if (LANGS.indexOf(n) >= 0) return n;
    }
    // Nenhum idioma do aparelho bate: usa o fuso horário como pista da localização
    // (não pede permissão e não consulta o IP).
    var c = tzCountry();
    if (PT_COUNTRIES.indexOf(c) >= 0) return 'pt';
    if (ES_COUNTRIES.indexOf(c) >= 0) return 'es';
    return 'en';
  }

  var TZ_COUNTRY = {
    'America/Sao_Paulo': 'BR', 'America/Bahia': 'BR', 'America/Fortaleza': 'BR', 'America/Recife': 'BR', 'America/Manaus': 'BR',
    'America/Belem': 'BR', 'America/Cuiaba': 'BR', 'America/Campo_Grande': 'BR', 'America/Porto_Velho': 'BR', 'America/Rio_Branco': 'BR',
    'America/Noronha': 'BR', 'America/Araguaina': 'BR', 'America/Maceio': 'BR', 'America/Boa_Vista': 'BR', 'America/Santarem': 'BR',
    'Europe/Lisbon': 'PT', 'Atlantic/Azores': 'PT', 'Atlantic/Madeira': 'PT', 'Africa/Luanda': 'AO', 'Africa/Maputo': 'MZ',
    'Europe/Madrid': 'ES', 'Atlantic/Canary': 'ES',
    'America/Mexico_City': 'MX', 'America/Cancun': 'MX', 'America/Monterrey': 'MX', 'America/Merida': 'MX', 'America/Tijuana': 'MX',
    'America/Chihuahua': 'MX', 'America/Hermosillo': 'MX', 'America/Mazatlan': 'MX',
    'America/Buenos_Aires': 'AR', 'America/Santiago': 'CL', 'America/Bogota': 'CO', 'America/Lima': 'PE', 'America/Montevideo': 'UY',
    'America/Asuncion': 'PY', 'America/La_Paz': 'BO', 'America/Guayaquil': 'EC', 'America/Caracas': 'VE', 'America/Costa_Rica': 'CR',
    'America/Guatemala': 'GT', 'America/Panama': 'PA', 'America/Santo_Domingo': 'DO', 'America/El_Salvador': 'SV',
    'America/Tegucigalpa': 'HN', 'America/Managua': 'NI', 'America/Havana': 'CU',
    'America/New_York': 'US', 'America/Chicago': 'US', 'America/Denver': 'US', 'America/Los_Angeles': 'US', 'America/Phoenix': 'US',
    'America/Anchorage': 'US', 'America/Detroit': 'US', 'Pacific/Honolulu': 'US', 'Europe/London': 'GB'
  };
  var PT_COUNTRIES = ['BR', 'PT', 'AO', 'MZ'];
  var ES_COUNTRIES = ['ES', 'MX', 'AR', 'CL', 'CO', 'PE', 'UY', 'PY', 'BO', 'EC', 'VE', 'CR', 'GT', 'PA', 'DO', 'SV', 'HN', 'NI', 'CU'];
  function tzCountry() {
    try {
      var tz = Intl.DateTimeFormat().resolvedOptions().timeZone || '';
      if (TZ_COUNTRY[tz]) return TZ_COUNTRY[tz];
      if (tz.indexOf('America/Argentina/') === 0) return 'AR';
    } catch (e) {}
    return '';
  }

  function setLang(l, persist) {
    lang = LANGS.indexOf(l) >= 0 ? l : 'en';
    if (persist) { try { localStorage.setItem('aff_lang', lang); } catch (e) {} }
    document.documentElement.lang = lang === 'pt' ? 'pt-BR' : lang;
    $$('.lang button').forEach(function (b) { b.setAttribute('aria-pressed', String(b.getAttribute('data-lang') === lang)); });
    applyText();
    if (PRODUCT) { buildSelects(); renderConsent(); setImages(); buildSim(); }
    renderTerms();
  }

  function applyText() {
    $$('[data-i18n]').forEach(function (el) { el.textContent = t(el.getAttribute('data-i18n')); });
    $$('[data-pi18n]').forEach(function (el) { el.textContent = pt(el.getAttribute('data-pi18n')); });
    $$('[data-i18n-ph]').forEach(function (el) { el.setAttribute('placeholder', t(el.getAttribute('data-i18n-ph'))); });
    $$('[data-i18n-aria]').forEach(function (el) { el.setAttribute('aria-label', t(el.getAttribute('data-i18n-aria'))); });
    if (PRODUCT) document.title = pt('title');
  }

  function setImages() {
    $$('[data-img]').forEach(function (img) {
      img.src = '/affiliates/img/' + img.getAttribute('data-img') + '-' + lang + '.webp';
    });
  }

  // ── UTM (preservado até o envio da inscrição) ─────────────────────────────
  var UTM_KEYS = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content', 'ref'];
  function captureUtm() {
    var found = {};
    UTM_KEYS.forEach(function (k) { var v = qs.get(k); if (v) found[k] = v.slice(0, 100); });
    try {
      if (Object.keys(found).length) sessionStorage.setItem('aff_utm', JSON.stringify(found));
      return JSON.parse(sessionStorage.getItem('aff_utm') || '{}');
    } catch (e) { return found; }
  }
  var utm = captureUtm();

  // ── Eventos (sem dados pessoais; respeita Do Not Track) ───────────────────
  function regionFromBrowser() {
    var p = (navigator.language || '').split('-');
    return p[1] && p[1].length === 2 ? p[1].toUpperCase() : tzCountry();
  }
  function track(evento, extra) {
    if (!PRODUCT || navigator.doNotTrack === '1') return;
    var body = {
      produto: PRODUCT, evento: evento, idioma: lang,
      pais: (extra && extra.pais) || regionFromBrowser(),
      canal: (extra && extra.canal) || '',
      placement: (extra && extra.placement) || '',
      utm_source: utm.utm_source || '', utm_campaign: utm.utm_campaign || ''
    };
    try {
      fetch(API + '/afiliados/evento', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body), keepalive: true
      }).catch(function () {});
    } catch (e) {}
  }

  // ── Simulador de comissão ─────────────────────────────────────────────────
  // É uma SIMULAÇÃO: usa o preço do app no país do afiliado (precos.js) e supõe que ~70% do
  // preço chega até nós depois das taxas das lojas e dos impostos (a Apple BR repassou 71%).
  var SIM_NET = 0.70;
  var SIM_USERS = [50, 200, 500, 1000];
  var ZERO_DECIMAL = ['JPY', 'KRW', 'VND', 'IDR', 'CLP', 'PYG', 'UGX', 'RWF', 'XAF', 'XOF', 'XPF', 'KMF', 'GNF', 'BIF', 'DJF'];
  var simState = { country: '', plan: 'mensal', ret: 1 };
  var simBound = false;

  function simPlans() {
    var d = window.AFF_PRECOS && window.AFF_PRECOS[PRODUCT];
    return d ? Object.keys(d) : [];
  }
  function simTable(plan) {
    var d = window.AFF_PRECOS && window.AFF_PRECOS[PRODUCT];
    return (d && d[plan]) || null;
  }
  function locale() { return lang === 'pt' ? 'pt-BR' : lang === 'es' ? 'es' : 'en'; }
  function money(v, cur, digits) {
    var d = ZERO_DECIMAL.indexOf(cur) >= 0 ? 0 : digits;
    try {
      return new Intl.NumberFormat(locale(), { style: 'currency', currency: cur, minimumFractionDigits: d, maximumFractionDigits: d }).format(v);
    } catch (e) { return v.toFixed(d) + ' ' + cur; }
  }
  // Comissão por assinante, na moeda do preço. Mensal: 30% x2 e 10% da 3ª à 12ª (só quem continua).
  // Anual: 10% do primeiro pagamento. No Lumora o código dá 10% de desconto nos primeiros pagamentos.
  function simPerUser(plan, price, ret) {
    var disc = PRODUCT === 'lumora' ? 0.9 : 1;
    if (plan === 'anual') return price * disc * SIM_NET * 0.10;
    return price * disc * SIM_NET * 0.30 * 2 + price * SIM_NET * 0.10 * 10 * ret;
  }

  function simDefaultCountry(table) {
    var guess = qs.get('country') || regionFromBrowser();
    guess = String(guess || '').toUpperCase();
    if (table[guess]) return guess;
    if (PRODUCT === 'lumora') return lang === 'pt' ? 'BR' : 'US';
    return table.US ? 'US' : Object.keys(table)[0];
  }

  function buildSim() {
    var root = $('#simulator'); if (!root || !window.AFF_PRECOS) return;
    var plans = simPlans(); if (!plans.length) return;
    if (plans.indexOf(simState.plan) < 0) simState.plan = plans[0];
    var table = simTable(simState.plan); if (!table) return;
    if (!simState.country || !table[simState.country]) simState.country = simDefaultCountry(table);

    var regions = displayNames(lang, 'region');
    var countries = Object.keys(table).map(function (c) { return { value: c, label: regions ? (regions.of(c) || c) : c }; })
      .sort(function (a, b) { return a.label.localeCompare(b.label, lang); });
    var selC = $('#sim-country'); selC.innerHTML = '';
    countries.forEach(function (it) { var o = document.createElement('option'); o.value = it.value; o.textContent = it.label; selC.appendChild(o); });
    selC.value = simState.country;

    var selP = $('#sim-plan'); selP.innerHTML = '';
    plans.forEach(function (p) {
      var o = document.createElement('option'); o.value = p; o.textContent = t(p === 'anual' ? 'sim.plan.annual' : 'sim.plan.monthly'); selP.appendChild(o);
    });
    selP.value = simState.plan;
    $('#sim-plan-wrap').style.display = plans.length > 1 ? '' : 'none';

    var selR = $('#sim-ret'); selR.innerHTML = '';
    [['1', 'sim.ret.100'], ['0.7', 'sim.ret.70'], ['0.5', 'sim.ret.50']].forEach(function (r) {
      var o = document.createElement('option'); o.value = r[0]; o.textContent = t(r[1]); selR.appendChild(o);
    });
    selR.value = String(simState.ret);

    if (!simBound) {
      simBound = true;
      selC.addEventListener('change', function () { simState.country = selC.value; renderSim(); });
      selP.addEventListener('change', function () { simState.plan = selP.value; simState.country = ''; buildSim(); });
      selR.addEventListener('change', function () { simState.ret = parseFloat(selR.value) || 1; renderSim(); });
    }
    renderSim();
  }

  function renderSim() {
    var table = simTable(simState.plan); if (!table) return;
    var row = table[simState.country]; if (!row) return;
    var cur = row[0], price = row[1], usd = row[2];
    var annual = simState.plan === 'anual';
    $('#sim-ret').disabled = annual;

    var priceEl = $('#sim-price'); priceEl.innerHTML = '';
    priceEl.appendChild(document.createTextNode(t('sim.price') + ' '));
    var strong = document.createElement('strong');
    strong.textContent = money(price, cur, 2) + ' ' + t(annual ? 'sim.per.year' : 'sim.per.month');
    priceEl.appendChild(strong);

    var perUser = simPerUser(simState.plan, price, simState.ret);
    var out = $('#sim-out'); out.innerHTML = '';
    SIM_USERS.forEach(function (n) {
      var total = perUser * n;
      var card = document.createElement('div'); card.className = 'sim-card';
      function line(cls, text) { var d = document.createElement('div'); d.className = cls; d.textContent = text; card.appendChild(d); return d; }
      line('n', t('sim.users').replace('{n}', n.toLocaleString(locale())) + ' · ' + t('sim.total'));
      line('v', money(total, cur, total < 100 ? 2 : 0));
      if (cur !== 'USD' && usd > 0) line('u', '≈ ' + money(total * usd / price, 'USD', 0));
      // Média mensal = total acumulado ÷ 12 (só uma ideia: os 2 primeiros meses pagam 30% e os outros 10%).
      var mensal = total / 12;
      line('p', t('sim.per.sub').replace('{v}', money(mensal, cur, mensal < 100 ? 2 : 0)));
      out.appendChild(card);
    });

    $('#sim-rule').textContent = t(annual ? 'sim.annual.rule' : 'sim.monthly.rule');
    var extra = [];
    if (PRODUCT === 'lumora') { extra.push(t('sim.disc.lumora')); extra.push(t('sim.only.lumora')); }
    $('#sim-disc').textContent = extra.join(' ');
  }

  // ── Formulário ────────────────────────────────────────────────────────────
  var COUNTRY_CODES = 'AF AL DZ AD AO AG AR AM AU AT AZ BS BH BD BB BY BE BZ BJ BT BO BA BW BR BN BG BF BI KH CM CA CV CF TD CL CN CO KM CG CD CR CI HR CU CY CZ DK DJ DM DO EC EG SV GQ ER EE SZ ET FJ FI FR GA GM GE DE GH GR GD GT GN GW GY HT HN HU IS IN ID IR IQ IE IL IT JM JP JO KZ KE KI KW KG LA LV LB LS LR LY LI LT LU MG MW MY MV ML MT MH MR MU MX FM MD MC MN ME MA MZ MM NA NR NP NL NZ NI NE NG KP MK NO OM PK PW PS PA PG PY PE PH PL PT QA RO RU RW KN LC VC WS SM ST SA SN RS SC SL SG SK SI SB SO ZA KR SS ES LK SD SR SE CH SY TW TJ TZ TH TL TG TO TT TN TR TM TV UG UA AE GB US UY UZ VU VA VE VN YE ZM ZW PR HK'.split(' ');
  var LANG_CODES = ['en', 'pt', 'es', 'fr', 'de', 'it', 'nl', 'ru', 'pl', 'tr', 'ar', 'hi', 'id', 'ja', 'ko', 'zh', 'sv'];
  var CHANNELS = ['instagram', 'tiktok', 'youtube', 'website', 'newsletter', 'community', 'other'];
  var AUDIENCES = ['lt1k', '1k-10k', '10k-50k', '50k-200k', 'gt200k', 'building'];
  var CATEGORIES = ['productivity', 'sports', 'creators', 'business', 'education', 'technology', 'beauty', 'other'];

  function displayNames(locale, type) {
    try { return new Intl.DisplayNames([locale], { type: type }); } catch (e) { return null; }
  }

  function fillSelect(sel, placeholderKey, items) {
    var current = sel.value;
    sel.innerHTML = '';
    var ph = document.createElement('option');
    ph.value = ''; ph.textContent = t(placeholderKey);
    sel.appendChild(ph);
    items.forEach(function (it) {
      var o = document.createElement('option');
      o.value = it.value; o.textContent = it.label;
      sel.appendChild(o);
    });
    if (current) sel.value = current;
  }

  function buildSelects() {
    var form = $('#aff-form'); if (!form) return;
    var regions = displayNames(lang, 'region');
    var countries = COUNTRY_CODES.map(function (c) {
      return { value: c, label: regions ? (regions.of(c) || c) : c };
    }).sort(function (a, b) { return a.label.localeCompare(b.label, lang); });
    fillSelect($('#f-country'), 'c.f.country.ph', countries);

    fillSelect($('#f-channel'), 'c.f.channel.ph', CHANNELS.map(function (c) {
      return { value: c, label: t('c.opt.channel.' + c) };
    }));
    fillSelect($('#f-audience'), 'c.f.audience.ph', AUDIENCES.map(function (c) {
      return { value: c, label: t('c.opt.aud.' + c) };
    }));

    // Idioma do conteúdo: rótulo localizado, mas o VALOR enviado é sempre o nome em inglês (admin lê em inglês).
    var inEn = displayNames('en', 'language'), inLang = displayNames(lang, 'language');
    fillSelect($('#f-lang'), 'c.f.lang.ph', LANG_CODES.map(function (c) {
      var en = inEn ? inEn.of(c) : c;
      return { value: en, label: inLang ? inLang.of(c) : en };
    }).concat([{ value: 'Other', label: t('c.opt.channel.other') }]));

    // Categorias (checkboxes): reconstrói preservando o que estava marcado
    var box = $('#f-categories');
    var marked = $$('input:checked', box).map(function (i) { return i.value; });
    box.innerHTML = '';
    CATEGORIES.forEach(function (c) {
      var l = document.createElement('label');
      var i = document.createElement('input');
      i.type = 'checkbox'; i.name = 'categorias'; i.value = c; i.checked = marked.indexOf(c) >= 0;
      l.appendChild(i); l.appendChild(document.createTextNode(' ' + t('c.opt.cat.' + c)));
      box.appendChild(l);
    });
  }

  function renderConsent() {
    var el = $('#consent-text'); if (!el) return;
    var tpl = t('c.f.consent');
    var terms = '<a href="/affiliate-terms/?lang=' + lang + '" target="_blank" rel="noopener">' + esc(t('c.f.consent.terms')) + '</a>';
    var priv = '<a href="/#privacy" target="_blank" rel="noopener">' + esc(t('c.f.consent.privacy')) + '</a>';
    el.innerHTML = esc(tpl).replace('{terms}', terms).replace('{privacy}', priv);
  }
  function esc(s) { return String(s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }

  function addLinkInput(value) {
    var list = $('#links-list');
    if ($$('input', list).length >= 5) return;
    var inp = document.createElement('input');
    inp.id = 'f-link-' + ($$('input', list).length + 1);
    inp.type = 'text'; inp.name = 'links'; inp.inputMode = 'url'; inp.autocomplete = 'off';
    inp.setAttribute('data-i18n-ph', 'c.f.links.ph'); inp.placeholder = t('c.f.links.ph');
    inp.setAttribute('aria-label', t('c.f.links'));
    if (value) inp.value = value;
    list.appendChild(inp);
  }

  var EMAIL_RE = /^[^\s@<>"',;]{1,64}@[^\s@<>"',;]{1,255}\.[A-Za-z]{2,24}$/;
  // Quem digita "instagram.com/perfil" (sem https://) também vale: completamos sozinhos.
  function normUrl(s) {
    s = String(s || '').trim().replace(/^@/, '');
    return s && !/^[a-z][a-z0-9+.-]*:\/\//i.test(s) ? 'https://' + s : s;
  }
  function validUrl(s) {
    try { var u = new URL(s); return /^https?:$/.test(u.protocol) && u.hostname.indexOf('.') > 0; } catch (e) { return false; }
  }

  function showMsg(kind, text) {
    var m = $('#form-msg');
    m.className = 'msg show ' + (kind === 'ok' ? 'ok' : 'err');
    m.textContent = text;
  }

  function collect() {
    var f = $('#aff-form');
    return {
      produto: PRODUCT,
      nome: f.nome.value.trim(),
      email: f.email.value.trim(),
      pais: f.pais.value,
      canal_principal: f.canal.value,
      links: $$('#links-list input').map(function (i) { return normUrl(i.value); }).filter(Boolean),
      audiencia: f.audiencia.value,
      idioma_conteudo: f.idioma_conteudo.value,
      paises_audiencia: f.paises_audiencia.value.trim(),
      categorias: $$('#f-categories input:checked').map(function (i) { return i.value; }),
      plano_divulgacao: f.plano.value.trim(),
      aceite_divulgacao: f.aceite_divulgacao.checked,
      aceite_termos: f.aceite_termos.checked,
      idioma_pagina: lang,
      utm: utm,
      empresa_site: f.empresa_site.value,
      tempo_preenchimento_ms: Date.now() - loadedAt
    };
  }

  function validate(d) {
    var bad = [];
    var f = $('#aff-form');
    function mark(el, cond) { if (el) el.setAttribute('aria-invalid', cond ? 'true' : 'false'); if (cond && el) bad.push(el); }
    mark(f.nome, !d.nome);
    mark(f.email, !EMAIL_RE.test(d.email));
    mark(f.pais, !d.pais);
    mark(f.canal, !d.canal_principal);
    mark(f.audiencia, !d.audiencia);
    mark(f.idioma_conteudo, !d.idioma_conteudo);
    mark(f.paises_audiencia, !d.paises_audiencia);
    mark(f.plano, !d.plano_divulgacao);
    var firstLink = $('#links-list input');
    mark(firstLink, d.links.length === 0 || !d.links.every(validUrl));
    if (d.categorias.length === 0) bad.push($('#f-categories input'));
    if (!d.aceite_divulgacao) bad.push(f.aceite_divulgacao);
    if (!d.aceite_termos) bad.push(f.aceite_termos);
    return bad;
  }

  function onSubmit(ev) {
    ev.preventDefault();
    var f = $('#aff-form');
    var d = collect();
    var bad = validate(d);
    if (bad.length) {
      showMsg('err', t('c.f.invalid'));
      if (bad[0] && bad[0].focus) bad[0].focus();
      return;
    }
    var btn = $('#f-submit');
    btn.disabled = true; btn.textContent = t('c.f.sending');
    track('form_submit', { pais: d.pais, canal: d.canal_principal });
    fetch(API + '/afiliados/inscricao', {
      method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(d)
    }).then(function (r) {
      if (r.status === 201) {
        track('application_success', { pais: d.pais, canal: d.canal_principal });
        f.reset();
        $$('#links-list input').forEach(function (i, idx) { if (idx > 0) i.remove(); });
        showMsg('ok', t('c.f.success'));
        $('#form-msg').scrollIntoView({ behavior: 'smooth', block: 'center' });
      } else if (r.status === 400) {
        showMsg('err', t('c.f.invalid'));
      } else {
        showMsg('err', t('c.f.error'));
      }
    }).catch(function () {
      showMsg('err', t('c.f.error'));
    }).then(function () {
      btn.disabled = false; btn.textContent = t('c.f.submit');
    });
  }

  function initForm() {
    var f = $('#aff-form'); if (!f) return;
    addLinkInput();
    $('#add-link').addEventListener('click', function () { addLinkInput(); var i = $$('#links-list input'); i[i.length - 1].focus(); });
    var started = false;
    f.addEventListener('focusin', function () { if (!started) { started = true; track('form_start'); } });
    f.addEventListener('submit', onSubmit);
  }

  // ── Termos ────────────────────────────────────────────────────────────────
  function renderTerms() {
    var root = $('#terms-root'); if (!root || !window.AFF_TERMS) return;
    var T = window.AFF_TERMS[lang] || window.AFF_TERMS.en;
    var html = '<h1>' + esc(T.title) + '</h1><p class="muted">' + esc(T.updated) + '</p>';
    T.sections.forEach(function (s) {
      html += '<h2>' + esc(s[0]) + '</h2>' + s[1].map(function (p) { return '<p>' + esc(p) + '</p>'; }).join('');
    });
    root.innerHTML = html;
    document.title = T.title + ' | Aura Dev Apps';
  }

  // ── Início ────────────────────────────────────────────────────────────────
  document.addEventListener('DOMContentLoaded', function () {
    $$('.lang button').forEach(function (b) {
      b.addEventListener('click', function () { setLang(b.getAttribute('data-lang'), true); });
    });
    $$('[data-cta]').forEach(function (a) {
      a.addEventListener('click', function () { track('cta_click', { placement: a.getAttribute('data-cta') }); });
    });
    initForm();
    setLang(detectLang(), false);
    track('page_view');
  });
})();
