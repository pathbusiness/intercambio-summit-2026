#!/usr/bin/env python3
"""Renderiza os 5 totens elípticos 60x193cm do Intercâmbio Summit 2026.

Gabarito: Loja do Porta Banner, corte 600x1930mm, frente e verso
(mesma arte nos dois lados), dobras horizontais a cada 482,5mm.

Saída em criativos/out/totens/: PNG 3600x11580 (~152 dpi no formato
final) + PDF 600x1930mm com 2 páginas (frente/verso) por totem.

Uso: python3 criativos/totens/render_totens.py
"""
import os

import fitz
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "..", "out", "totens")

W, H = 1200, 3860          # 1px = 0,5mm
SCALE = 3                  # 3600x11580 px ≈ 152 dpi
MM_W, MM_H = 600, 1930
PT = 72 / 25.4             # mm -> pt

JOBS = [
    ("totem-patrocinador.html",
     {"NOME": "Ollara", "LOGO": "assets/ollara-cor.png", "LOGO_W": 820},
     "totem-patrocinador-ollara"),
    ("totem-patrocinador.html",
     {"NOME": "CLIDA", "LOGO": "assets/clida-cor.png", "LOGO_W": 800},
     "totem-patrocinador-clida"),
    ("totem-patrocinador.html",
     {"NOME": "Ikon Institute of Australia · Australian Learning Group",
      "LOGO": "assets/ikon-alg-cor.png", "LOGO_W": 1060},
     "totem-patrocinador-ikon-alg"),
    ("totem-sinalizacao.html",
     {"PALAVRA": "Credenciamento",
      "FONTE": 300,
      "SUPORTE": "Bem-vindo! Retire aqui a sua <strong>credencial</strong>"},
     "totem-sinalizacao-credenciamento"),
    ("totem-sinalizacao.html",
     {"PALAVRA": "Auditório",
      "FONTE": 450,
      "SUPORTE": "Palestras · Painéis · Networking"},
     "totem-sinalizacao-auditorio"),
]


def main():
    os.makedirs(OUT, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": W, "height": H},
                                device_scale_factor=SCALE)
        for template, data, nome in JOBS:
            html = open(os.path.join(ROOT, template), encoding="utf-8").read()
            for k, v in data.items():
                html = html.replace("{{%s}}" % k, str(v))
            tmp = os.path.join(ROOT, "__render__.html")
            with open(tmp, "w", encoding="utf-8") as f:
                f.write(html)
            page.goto("file://" + tmp)
            page.evaluate("document.fonts.ready.then(() => true)")
            page.wait_for_timeout(300)
            png = os.path.join(OUT, nome + ".png")
            page.screenshot(path=png, clip={"x": 0, "y": 0, "width": W, "height": H})
            os.remove(tmp)

            # PDF em escala real, frente e verso (mesma arte)
            pdf = fitz.open()
            rect = fitz.Rect(0, 0, MM_W * PT, MM_H * PT)
            for _ in range(2):
                pg = pdf.new_page(width=rect.width, height=rect.height)
                pg.insert_image(rect, filename=png)
            pdf.save(os.path.join(OUT, nome + ".pdf"), deflate=True)
            pdf.close()
            print(nome, "ok")
        browser.close()


if __name__ == "__main__":
    main()
