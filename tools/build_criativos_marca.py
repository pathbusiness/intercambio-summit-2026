#!/usr/bin/env python3
"""Ativos de marca para os criativos de mídia social (pasta criativos/).

Gera as versões monocromáticas BRANCAS dos logos dos apoiadores para a
faixa de rodapé sobre a cenografia azul (pedido do briefing de criativos;
os PNGs coloridos oficiais de site/assets/img/marca/ continuam intactos
para uso sobre branco, conforme o manual).

Como funciona a conversão: tinta = alfa x (1 - luminância). Assim os traços
coloridos/escuros viram branco sólido e os miolos brancos (texto do balão
IALC, sorriso do Edvisor) viram vazado, deixando o azul aparecer — que é o
comportamento correto de um logo mono reverso.

Equalização por PESO ÓPTICO, não por altura: cada logo recebe um fator
individual (OPTICAL) calibrado à mão para que os cinco pareçam do mesmo
tamanho na faixa. Ajustar aqui e rodar de novo se algum parceiro reclamar.
"""
import os
import numpy as np
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "site", "assets", "img", "marca")
OUT = os.path.join(ROOT, "criativos", "assets", "marca")
os.makedirs(OUT, exist_ok=True)

# altura-base da faixa (px @1080 de largura de arte) x fator óptico individual
BASE_H = 46
OPTICAL = {
    "belta":   1.00,   # horizontal, texto grande
    "abrapei": 1.18,   # wordmark fino + símbolo pequeno: precisa crescer
    "ialc":    1.24,   # bloco compacto e estreito: precisa crescer
    "allyhub": 0.90,   # glifos muito largos e pesados: encolher
    "edvisor": 1.10,   # empilhado (símbolo sobre wordmark)
}


def white_mono(im):
    a = np.asarray(im.convert("RGBA"), dtype=np.float32) / 255.0
    lum = 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]
    ink = a[..., 3] * np.clip((1.0 - lum) * 1.6, 0.0, 1.0) ** 0.75
    out = np.zeros_like(a)
    out[..., 0:3] = 1.0
    out[..., 3] = ink
    return Image.fromarray((out * 255).astype(np.uint8), "RGBA")


def trim(im):
    bbox = im.split()[3].getbbox()
    return im.crop(bbox) if bbox else im


def main():
    for slug, k in OPTICAL.items():
        im = trim(Image.open(os.path.join(SRC, f"apoio-{slug}-box.png")))
        mono = white_mono(im)
        h = round(BASE_H * k) * 2          # exporta em 2x para nitidez
        w = round(mono.width * h / mono.height)
        mono = mono.resize((w, h), Image.LANCZOS)
        mono.save(os.path.join(OUT, f"apoio-{slug}-branco.png"))
        print(f"apoio-{slug}-branco.png {w}x{h}")

    # tira de conferência sobre Summit Blue
    logos = [Image.open(os.path.join(OUT, f"apoio-{s}-branco.png")) for s in OPTICAL]
    gap, pad = 56, 40
    W = sum(l.width for l in logos) + gap * (len(logos) - 1) + pad * 2
    H = max(l.height for l in logos) + pad * 2
    sheet = Image.new("RGB", (W, H), (0, 68, 185))
    x = pad
    for l in logos:
        sheet.paste(l, (x, (H - l.height) // 2), l)
        x += l.width + gap
    sheet.save(os.path.join(ROOT, "tools", "faixa-apoio-teste.png"))
    print("faixa-apoio-teste.png ok")


if __name__ == "__main__":
    main()
