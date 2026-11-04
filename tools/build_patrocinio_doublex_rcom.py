#!/usr/bin/env python3
"""Logos dos patrocinadores Double X e RCOM (fontes em Sponsors/).

Saídas:
  site/assets/img/marca/patrocinio-doublex-box.png   faixa de patrocínio do site (fundo branco)
  site/assets/img/marca/patrocinio-rcom-box.png      idem; o logo da RCOM é para fundo escuro, então vai em tile escuro
  criativos/assets/marca/cor-patrocinio-doublex.png  logo colorido, recortado (fundos claros)
  criativos/assets/marca/patrocinio-rcom-branco.png  logo da RCOM sem o fundo (fundos escuros/azul)
"""
import os
import numpy as np
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site", "assets", "img", "marca")
CRIA = os.path.join(ROOT, "criativos", "assets", "marca")
BG = 27  # cinza do fundo do arquivo da RCOM


def trim_alpha(im):
    return im.crop(im.split()[3].getbbox())


def box(im, w=460, h=168, ocupa_w=0.92, ocupa_h=0.70):
    """Centraliza o logo numa caixa transparente (mesmo padrão dos outros patrocinadores)."""
    s = min(w * ocupa_w / im.width, h * ocupa_h / im.height)
    r = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    out.paste(r, ((w - r.width) // 2, (h - r.height) // 2), r)
    return out


# ---- Double X: o arquivo já tem fundo transparente
dx = trim_alpha(Image.open(os.path.join(ROOT, "Sponsors", "Double X", "doubleX-logo.png")).convert("RGBA"))
dx.save(os.path.join(CRIA, "cor-patrocinio-doublex.png"))
box(dx, ocupa_w=0.90, ocupa_h=0.60).save(os.path.join(SITE, "patrocinio-doublex-box.png"))

# ---- RCOM: fundo cinza-escuro com grade sutil
src = Image.open(os.path.join(ROOT, "Sponsors", "RCOM", "RCOM-logo.png")).convert("RGB")
a = np.array(src).astype(float)
mx = a.max(axis=2)

# 1) versão sem fundo (para peças em fundo escuro): alfa pela luminosidade acima do fundo
alfa = np.clip((mx - 40) / (255 - 40), 0, 1)
cor = np.clip((a - (1 - alfa[..., None]) * BG) / np.maximum(alfa[..., None], 1e-3), 0, 255)
rgba = np.dstack([cor, alfa * 255]).astype("uint8")
sem_fundo = trim_alpha(Image.fromarray(rgba))
sem_fundo.save(os.path.join(CRIA, "patrocinio-rcom-branco.png"))

# 2) tile escuro, recorte justo com respiro, cantos arredondados (para a faixa branca do site)
ys, xs = np.where(mx > 60)
x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
pad = round(0.14 * (y1 - y0))
crop = src.crop((max(0, x0 - pad), max(0, y0 - pad), min(src.width, x1 + pad), min(src.height, y1 + pad)))
H = 360
tile = crop.resize((round(crop.width * H / crop.height), H), Image.LANCZOS).convert("RGBA")
m = Image.new("L", tile.size, 0)
ImageDraw.Draw(m).rounded_rectangle((0, 0, tile.width - 1, tile.height - 1), radius=26, fill=255)
tile.putalpha(m)
tile.save(os.path.join(SITE, "patrocinio-rcom-box.png"))
print("ok", dx.size, sem_fundo.size, tile.size)
