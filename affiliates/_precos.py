# -*- coding: utf-8 -*-
"""Gera affiliates/precos.js (preços dos apps por país, usados no simulador de comissão).

Fonte: as planilhas de preços aprovadas em 27/10/2026 (C:\\DEV\\PRECOS_GOOGLE_CLIPIT_PROPOSTA.csv e a regra
do Lumora: só Brasil e EUA por enquanto). Regerar: python affiliates/_precos.py
Cada entrada: país -> [moeda, preço na loja, preço aproximado em US$]. É só para SIMULAÇÃO.
"""
import csv, io, json, os

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_CLIPIT = r"C:\DEV\PRECOS_GOOGLE_CLIPIT_PROPOSTA.csv"
BRL_POR_USD = 5.43  # câmbio de 27/10/2026, só para o "≈ US$" do simulador


def numero(txt):
    return float(txt.replace(".", "").replace(",", ".")) if txt.count(",") and txt.count(".") else float(txt.replace(",", "."))


def clipit():
    out = {}
    with io.open(CSV_CLIPIT, encoding="utf-8-sig", newline="") as f:
        for linha in csv.reader(f, delimiter=";"):
            if not linha or linha[0] == "regiao":
                continue
            regiao, moeda, _regra, _atual, proposto, _var, usd = linha[:7]
            out[regiao] = [moeda, round(numero(proposto), 2), round(numero(usd), 2)]
    return out


def lumora():
    return {
        "mensal": {"BR": ["BRL", 29.90, round(29.90 / BRL_POR_USD, 2)], "US": ["USD", 29.99, 29.99]},
        "anual": {"BR": ["BRL", 249.90, round(249.90 / BRL_POR_USD, 2)], "US": ["USD", 249.99, 249.99]},
    }


if __name__ == "__main__":
    dados = {"lumora": lumora(), "clipit": {"mensal": clipit()}}
    js = ("/* GERADO por affiliates/_precos.py — não editar à mão. Preços por país para o simulador de comissão. */\n"
          "window.AFF_PRECOS = " + json.dumps(dados, ensure_ascii=False, separators=(",", ":")) + ";\n")
    destino = os.path.join(RAIZ, "affiliates", "precos.js")
    with io.open(destino, "w", encoding="utf-8", newline="\n") as f:
        f.write(js)
    print("gerado:", os.path.relpath(destino, RAIZ), "-", len(dados["clipit"]["mensal"]), "países no Clipit")
