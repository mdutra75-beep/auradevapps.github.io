#!/usr/bin/env python3
"""Gera as páginas de afiliados a partir de UM template (mesma ideia do lumora/_build.py).

    python affiliates/_build.py

Saída:
  affiliates-clipit-sports/index.html
  affiliates-lumora/index.html
  affiliate-terms/index.html
  (e acrescenta as 3 URLs ao sitemap.xml, se ainda não estiverem lá)

Os TEXTOS ficam em affiliates/i18n.js (EN/PT/ES). Aqui só vai estrutura e SEO em inglês.
"""
import os, re

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://aura-dev-app.com"
DESCRICAO = ("Apply to become an approved affiliate, receive a personal referral code "
             "and earn 30% on the first two eligible monthly payments, then 10% for up to 12 months.")

PRODUTOS = {
    "clipit": {
        "pasta": "affiliates-clipit-sports",
        "nome": "ClipIt Sports",
        "titulo": "ClipIt Sports Affiliate Program | Earn With Your Audience",
        "og": "og-clipit.jpg",
        "logo": "logo-clipit.webp",
        "visual": """
        <div class="phone" role="img" data-i18n-aria="p.clipit.mock" aria-label="ClipIt Sports app preview">
          <div class="rec" data-pi18n="rec">Recording</div>
          <div class="pitch" aria-hidden="true"></div>
          <div class="chips" aria-hidden="true">
            <span data-pi18n="chip.1">Goal</span><span data-pi18n="chip.2">Dribble</span><span data-pi18n="chip.3">Great save</span>
          </div>
          <div class="markbtn" aria-hidden="true" data-pi18n="mark">Mark</div>
        </div>""",
    },
    "lumora": {
        "pasta": "affiliates-lumora",
        "nome": "Lumora",
        "titulo": "Lumora Affiliate Program | Earn With Your Audience",
        "og": "og-lumora.jpg",
        "logo": "logo-lumora.webp",
        "visual": """
        <div class="shots" role="img" data-i18n-aria="p.lumora.mock" aria-label="Lumora app screens">
          <img data-img="lumora-agenda" src="/affiliates/img/lumora-agenda-en.webp" alt="" width="420" height="817" loading="lazy">
          <img data-img="lumora-meulink" src="/affiliates/img/lumora-meulink-en.webp" alt="" width="420" height="817" loading="lazy">
          <img data-img="lumora-financeiro" src="/affiliates/img/lumora-financeiro-en.webp" alt="" width="420" height="817" loading="lazy">
        </div>""",
    },
}

ICONES = {
    "code": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20.6 13.4 13.4 20.6a2 2 0 0 1-2.8 0L3 13V3h10l7.6 7.6a2 2 0 0 1 0 2.8Z"/><circle cx="7.5" cy="7.5" r="1.2"/></svg>',
    "image": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="4" width="18" height="16" rx="2"/><circle cx="9" cy="10" r="1.6"/><path d="m21 16-5-5-8 9"/></svg>',
    "chart": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 3v18h18"/><path d="m7 15 4-4 3 3 5-6"/></svg>',
    "wallet": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 7H5a2 2 0 0 1 0-4h13v4Z"/><path d="M3 5v14a2 2 0 0 0 2 2h15V7"/><circle cx="16.5" cy="14" r="1.2"/></svg>',
}

CABECALHO = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{titulo}</title>
<meta name="description" content="{descricao}">
<link rel="canonical" href="{url}">
<meta name="robots" content="{robots}">
<link rel="icon" href="/images/Logo_Aura_Dev.png">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Aura Dev Apps">
<meta property="og:title" content="{titulo}">
<meta property="og:description" content="{descricao}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{og}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{titulo}">
<meta name="twitter:description" content="{descricao}">
<meta name="twitter:image" content="{og}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Sora:wght@400;600;700;800&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/affiliates/affiliates.css">
</head>
<body{body_attr}>
<a class="skip" href="#main" data-i18n="c.skip">Skip to content</a>
<div class="bg-grid" aria-hidden="true"></div>
<div class="bg-glow" aria-hidden="true"></div>
<header class="top">
  <div class="top-in">
    <a class="brand" href="{site}/"><img src="/images/Logo_Aura_Dev.png" alt="" width="30" height="30"><span>Aura Dev Apps</span></a>
    <span class="top-sp"></span>
    <div class="lang" role="group" aria-label="Language">
      <button type="button" data-lang="en" aria-pressed="true">EN</button>
      <button type="button" data-lang="pt" aria-pressed="false">PT</button>
      <button type="button" data-lang="es" aria-pressed="false">ES</button>
    </div>
    {cta_topo}
  </div>
</header>
"""

RODAPE = """
<footer>
  <div>
    <a href="/affiliate-terms/" data-i18n="c.foot.terms">Affiliate Terms</a>
    <a href="/#privacy" data-i18n="c.foot.privacy">Privacy</a>
    <a href="mailto:affiliates@aura-dev-app.com" data-i18n="c.foot.contact">Contact</a>
  </div>
  <p style="margin-top:.8rem">&copy; 2026 Aura Dev Apps</p>
</footer>
<script src="/affiliates/i18n.js"></script>
<script src="/affiliates/precos.js"></script>
<script src="/affiliates/affiliates.js"></script>
</body>
</html>
"""

CORPO_PRODUTO = """<main id="main">
  <section class="hero">
    <div>
      <img class="hero-logo" src="/affiliates/img/{logo}" alt="{nome} logo" width="84" height="84">
      <p class="eyebrow" data-i18n="c.eyebrow">Affiliate program</p>
      <h1 data-pi18n="headline">Become a {nome} Affiliate</h1>
      <p class="lead" data-pi18n="sub"></p>
      <a class="btn" href="#apply" data-cta="hero" data-i18n="c.cta">Apply to become an affiliate</a>
      <p class="note" data-i18n="c.disclaimer"></p>
      <p class="short" style="margin-top:1.4rem" data-pi18n="short"></p>
    </div>
    <div class="visual">{visual}
    </div>
  </section>

  <section id="why">
    <h2 data-i18n="c.why.title">Why become an affiliate</h2>
    <div class="grid4">
      <div class="card"><div class="ico">{i_code}</div><h3 data-i18n="c.why.1.t"></h3><p data-i18n="c.why.1.d"></p></div>
      <div class="card"><div class="ico">{i_image}</div><h3 data-i18n="c.why.2.t"></h3><p data-i18n="c.why.2.d"></p></div>
      <div class="card"><div class="ico">{i_chart}</div><h3 data-i18n="c.why.3.t"></h3><p data-i18n="c.why.3.d"></p></div>
      <div class="card"><div class="ico">{i_wallet}</div><h3 data-i18n="c.why.4.t"></h3><p data-i18n="c.why.4.d"></p></div>
    </div>
  </section>

  <section id="how">
    <h2 data-i18n="c.how.title">How it works</h2>
    <ol class="steps">
      <li><h3 data-i18n="c.how.1.t"></h3><p data-i18n="c.how.1.d"></p></li>
      <li><h3 data-i18n="c.how.2.t"></h3><p data-i18n="c.how.2.d"></p></li>
      <li><h3 data-i18n="c.how.3.t"></h3><p data-i18n="c.how.3.d"></p></li>
      <li><h3 data-i18n="c.how.4.t"></h3><p data-i18n="c.how.4.d"></p></li>
      <li><h3 data-i18n="c.how.5.t"></h3><p data-i18n="c.how.5.d"></p></li>
    </ol>
  </section>

  <section id="terms">
    <h2 data-i18n="c.terms.title">Commission terms</h2>
    <div class="terms-grid">
      <div class="card"><h3 data-i18n="c.terms.1.t"></h3><p data-i18n="c.terms.1.d"></p></div>
      <div class="card"><h3 data-i18n="c.terms.2.t"></h3><p data-i18n="c.terms.2.d"></p></div>
      <div class="card"><h3 data-i18n="c.terms.3.t"></h3><p data-i18n="c.terms.3.d"></p></div>
      <div class="card"><h3 data-i18n="c.terms.4.t"></h3><p data-i18n="c.terms.4.d"></p></div>
      <div class="card"><h3 data-i18n="c.terms.5.t"></h3><p data-i18n="c.terms.5.d"></p></div>
    </div>
    <p class="foot-note"><span data-i18n="c.terms.foot"></span> <a href="/affiliate-terms/" data-i18n="c.terms.link">Affiliate Terms</a>.</p>
  </section>

  <section id="simulator">
    <h2 data-i18n="sim.title">Estimate your earnings</h2>
    <p class="muted" style="margin:-.8rem 0 1.4rem" data-i18n="sim.intro"></p>
    <div class="sim-box">
      <div class="sim-controls">
        <div><label for="sim-country" data-i18n="sim.country"></label><select id="sim-country"></select></div>
        <div id="sim-plan-wrap"><label for="sim-plan" data-i18n="sim.plan"></label><select id="sim-plan"></select></div>
        <div><label for="sim-ret" data-i18n="sim.ret"></label><select id="sim-ret"></select></div>
      </div>
      <p id="sim-price" class="sim-price"></p>
      <div id="sim-out" class="sim-out" aria-live="polite"></div>
      <p id="sim-rule" class="sim-small"></p>
      <p id="sim-disc" class="sim-small"></p>
      <p class="sim-warn" data-i18n="sim.disclaimer"></p>
    </div>
  </section>

  <section id="who">
    <h2 data-i18n="c.who.title">Who we are looking for</h2>
    <ul class="who">
      <li data-i18n="c.who.1"></li>
      <li data-pi18n="who.1"></li>
      <li data-pi18n="who.2"></li>
      <li data-i18n="c.who.2"></li>
    </ul>
  </section>

  <section id="apply">
    <div class="form-wrap">
      <h2 data-i18n="c.form.title">Application form</h2>
      <p class="muted" style="margin:-.8rem 0 1.4rem" data-i18n="c.form.intro"></p>
      <form id="aff-form" novalidate autocomplete="on">
        <div class="row">
          <div><label class="req" for="f-name" data-i18n="c.f.name"></label><input type="text" id="f-name" name="nome" maxlength="200" autocomplete="name" required></div>
          <div><label class="req" for="f-email" data-i18n="c.f.email"></label><input type="email" id="f-email" name="email" maxlength="254" autocomplete="email" required></div>
        </div>
        <div class="row">
          <div><label class="req" for="f-country" data-i18n="c.f.country"></label><select id="f-country" name="pais" autocomplete="country" required></select></div>
          <div><label class="req" for="f-channel" data-i18n="c.f.channel"></label><select id="f-channel" name="canal" required></select></div>
        </div>
        <div>
          <label class="req" for="f-link-1" data-i18n="c.f.links"></label>
          <div id="links-list" class="links-list"></div>
          <button type="button" id="add-link" class="linkbtn" data-i18n="c.f.links.add"></button>
        </div>
        <div class="row">
          <div><label class="req" for="f-audience" data-i18n="c.f.audience"></label><select id="f-audience" name="audiencia" required></select></div>
          <div><label class="req" for="f-lang" data-i18n="c.f.lang"></label><select id="f-lang" name="idioma_conteudo" required></select></div>
        </div>
        <div><label class="req" for="f-audc" data-i18n="c.f.aud_countries"></label><input type="text" id="f-audc" name="paises_audiencia" maxlength="300" data-i18n-ph="c.f.aud_countries.ph" required></div>
        <fieldset><legend class="req" data-i18n="c.f.categories"></legend><div id="f-categories" class="checks"></div></fieldset>
        <div><label class="req" for="f-plan" data-i18n="c.f.promote"></label><textarea id="f-plan" name="plano" maxlength="2000" data-i18n-ph="c.f.promote.ph" required></textarea></div>
        <div class="trap" aria-hidden="true"><label>Company website<input type="text" name="empresa_site" tabindex="-1" autocomplete="off"></label></div>
        <label class="agree"><input type="checkbox" name="aceite_divulgacao" required><span data-i18n="c.f.disclosure"></span></label>
        <label class="agree"><input type="checkbox" name="aceite_termos" required><span id="consent-text"></span></label>
        <p class="privacy" data-i18n="c.f.privacy"></p>
        <div id="form-msg" class="msg" role="status" aria-live="polite"></div>
        <button type="submit" id="f-submit" class="btn" data-i18n="c.f.submit">Submit application</button>
      </form>
    </div>
  </section>

  <section id="faq">
    <h2 data-i18n="c.faq.title">Frequently asked questions</h2>
    <div class="faq">
      <details><summary data-i18n="c.faq.1.q"></summary><p data-i18n="c.faq.1.a"></p></details>
      <details><summary data-i18n="c.faq.2.q"></summary><p data-i18n="c.faq.2.a"></p></details>
      <details><summary data-i18n="c.faq.3.q"></summary><p data-i18n="c.faq.3.a"></p></details>
      <details><summary data-i18n="c.faq.4.q"></summary><p data-i18n="c.faq.4.a"></p></details>
      <details><summary data-i18n="c.faq.5.q"></summary><p data-i18n="c.faq.5.a"></p></details>
      <details><summary data-i18n="c.faq.6.q"></summary><p data-i18n="c.faq.6.a"></p></details>
    </div>
  </section>

  <section class="final">
    <h2 data-i18n="c.final.title">Ready to join?</h2>
    <a class="btn" href="#apply" data-cta="final" data-i18n="c.cta">Apply to become an affiliate</a>
    <p class="muted"><span data-i18n="c.final.contact">Questions? Write to</span> <a href="mailto:affiliates@aura-dev-app.com">affiliates@aura-dev-app.com</a></p>
  </section>
</main>
"""

CORPO_TERMOS = """<main id="main">
  <section class="doc">
    <div id="terms-root"></div>
    <p style="margin-top:2rem"><a class="btn sm" href="{site}/" >&larr; aura-dev-app.com</a></p>
  </section>
</main>
"""


def montar_produto(chave, p):
    url = f"{SITE}/{p['pasta']}/"
    html = CABECALHO.format(
        titulo=p["titulo"], descricao=DESCRICAO, url=url, robots="index, follow",
        og=f"{SITE}/affiliates/img/{p['og']}", body_attr=f' data-product="{chave}"', site=SITE,
        cta_topo='<a class="btn sm" href="#apply" data-cta="nav" data-i18n="c.nav.apply">Apply</a>',
    )
    html += CORPO_PRODUTO.format(
        nome=p["nome"], logo=p["logo"], visual=p["visual"],
        i_code=ICONES["code"], i_image=ICONES["image"], i_chart=ICONES["chart"], i_wallet=ICONES["wallet"],
    )
    html += RODAPE
    return html


def montar_termos():
    html = CABECALHO.format(
        titulo="Affiliate Program Terms | Aura Dev Apps",
        descricao="Terms of the Lumora and ClipIt Sports affiliate program.",
        url=f"{SITE}/affiliate-terms/", robots="index, follow",
        og=f"{SITE}/affiliates/img/og-lumora.jpg", body_attr="", site=SITE, cta_topo="",
    )
    html += CORPO_TERMOS.format(site=SITE)
    html += RODAPE
    return html


def escrever(caminho, conteudo):
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    with open(caminho, "w", encoding="utf-8", newline="\n") as f:
        f.write(conteudo)
    print("gerado:", os.path.relpath(caminho, RAIZ))


def atualizar_sitemap(urls):
    caminho = os.path.join(RAIZ, "sitemap.xml")
    with open(caminho, encoding="utf-8") as f:
        xml = f.read()
    novas = ""
    for u in urls:
        if f"<loc>{u}</loc>" not in xml:
            novas += f"  <url><loc>{u}</loc><changefreq>monthly</changefreq><priority>0.6</priority></url>\n"
    if novas:
        xml = xml.replace("</urlset>", novas + "</urlset>")
        with open(caminho, "w", encoding="utf-8", newline="\n") as f:
            f.write(xml)
        print("sitemap.xml: acrescentadas", novas.count("<url>"), "URLs")


if __name__ == "__main__":
    urls = []
    for chave, p in PRODUTOS.items():
        escrever(os.path.join(RAIZ, p["pasta"], "index.html"), montar_produto(chave, p))
        urls.append(f"{SITE}/{p['pasta']}/")
    escrever(os.path.join(RAIZ, "affiliate-terms", "index.html"), montar_termos())
    urls.append(f"{SITE}/affiliate-terms/")
    atualizar_sitemap(urls)
