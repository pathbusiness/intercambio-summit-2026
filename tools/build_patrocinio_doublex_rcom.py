#!/usr/bin/env python3
"""Logos dos patrocinadores Double X e RCOM (fontes em Sponsors/).

Saídas:
  site/assets/img/marca/patrocinio-doublex-box.png   faixa de patrocínio do site (fundo branco)
  site/assets/img/marca/patrocinio-rcom-box.png      idem (RCOM sem fundo; frase e ondas em cinza-escuro)
  criativos/assets/marca/cor-patrocinio-rcom.png     logo da RCOM para fundos claros
  criativos/assets/marca/cor-patrocinio-doublex.png  logo colorido, recortado (fundos claros)
  criativos/assets/marca/patrocinio-rcom-branco.png  logo da RCOM sem o fundo (fundos escuros/azul)
"""
import os
import numpy as np
from PIL import Image

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

# 2) versão para fundo claro (faixa branca do site): sem fundo, e as partes claras (frase e ondas)
#    passam para cinza-escuro; o laranja é mantido
sat = a.max(axis=2) - a.min(axis=2)
neutro = sat < 28
alfa_n = np.clip((mx - 40) / (217 - 40), 0, 1)
alfa2 = np.where(neutro, alfa_n, alfa)
cor2 = np.where(neutro[..., None], np.array([42.0, 42.0, 42.0]), cor)
rgba2 = np.dstack([cor2, alfa2 * 255]).astype("uint8")
claro = trim_alpha(Image.fromarray(rgba2))
claro.save(os.path.join(CRIA, "cor-patrocinio-rcom.png"))
pad = round(0.06 * claro.height)
canvas = Image.new("RGBA", (claro.width + 2 * pad, claro.height + 2 * pad), (0, 0, 0, 0))
canvas.paste(claro, (pad, pad), claro)
H = 360
canvas.resize((round(canvas.width * H / canvas.height), H), Image.LANCZOS).save(os.path.join(SITE, "patrocinio-rcom-box.png"))
print("ok", dx.size, sem_fundo.size, canvas.size)
