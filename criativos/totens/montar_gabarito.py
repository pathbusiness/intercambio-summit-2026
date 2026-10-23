#!/usr/bin/env python3
"""Monta as artes dos totens no gabarito da Loja do Porta Banner.

Usa assets/gabarito-base.pdf (template 1900x2800mm com as caixas de corte
FRENTE/VERSO de 600x1930mm) e insere o PNG de cada totem nas duas caixas.
Também gera o PDF simples 600x1930mm com 2 páginas (frente/verso).

Uso: python3 criativos/totens/montar_gabarito.py [nome ...]
     (sem argumentos monta todos os totens de criativos/out/totens)
"""
import glob
import os
import sys

import fitz

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "..", "out", "totens")
BASE = os.path.join(ROOT, "assets", "gabarito-base.pdf")

# caixas de corte no gabarito (pt), medidas do PDF original da gráfica
FRENTE = fitz.Rect(812.3017, 1107.1914, 2513.0891, 6578.0571)
VERSO = fitz.Rect(3322.9077, 1107.1914, 5023.6953, 6578.0571)
MM_W, MM_H = 600, 1930
PT = 72 / 25.4


def montar(nome):
    png = os.path.join(OUT, nome + ".png")
    # PDF simples 600x1930, frente e verso
    pdf = fitz.open()
    rect = fitz.Rect(0, 0, MM_W * PT, MM_H * PT)
    for _ in range(2):
        pg = pdf.new_page(width=rect.width, height=rect.height)
        pg.insert_image(rect, filename=png)
    pdf.save(os.path.join(OUT, nome + ".pdf"), deflate=True)
    pdf.close()
    # arte montada no gabarito da gráfica
    d = fitz.open(BASE)
    pg = d[0]
    xref = pg.insert_image(FRENTE, filename=png)
    pg.insert_image(VERSO, xref=xref)
    os.makedirs(os.path.join(OUT, "gabarito"), exist_ok=True)
    d.save(os.path.join(OUT, "gabarito", nome + "-GABARITO.pdf"),
           deflate=True, garbage=3)
    print(nome, "ok")


def main():
    nomes = sys.argv[1:]
    if not nomes:
        nomes = sorted(os.path.splitext(os.path.basename(p))[0]
                       for p in glob.glob(os.path.join(OUT, "totem-*.png")))
    for nome in nomes:
        montar(nome)


if __name__ == "__main__":
    main()
