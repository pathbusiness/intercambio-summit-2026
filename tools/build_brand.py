#!/usr/bin/env python3
"""Prepara os ativos de marca para o site a partir dos arquivos oficiais.

- Logo do Summit: recorta as margens do PNG oficial (versão primária em fundo
  branco e versão reversa em Summit Blue) e exporta em 2 tamanhos.
- Apoiadores (BELTA, ABRAPEI, IALC, Ally Hub, Edvisor): recorta margens,
  normaliza em altura única, exporta PNG (transparência preservada).
Regra do manual: reprodução fiel, sem recolorir, proporções originais.
"""
import os
from PIL import Image, ImageChops

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "/Users/rodrigocollaro/Documents/PATH BUS & MKT/Intercâmbio Summit"
OUT = os.path.join(ROOT, "site", "assets", "img", "marca")
os.makedirs(OUT, exist_ok=True)


def trim(im, tol=8):
    """Recorta margens de cor uniforme (fundo branco/azul) ou alfa vazio."""
    if im.mode == "RGBA":
        bbox = im.split()[3].getbbox()
        if bbox:
            return im.crop(bbox)
        im = im.convert("RGB")
    rgb = im.convert("RGB")
    bg = Image.new("RGB", rgb.size, rgb.getpixel((2, 2)))
    diff = ImageChops.difference(rgb, bg)
    bbox = diff.point(lambda p: 255 if p > tol else 0).getbbox()
    return im.crop(bbox) if bbox else im


def export(im, name, heights):
    for h in heights:
        w = round(im.width * h / im.height)
        out = im.resize((w, h), Image.LANCZOS)
        out.save(os.path.join(OUT, f"{name}-{h}.png"), optimize=True)
        print(f"{name}-{h}.png {w}x{h}")


# --- logo do Summit ---
logo1 = trim(Image.open(f"{BASE}/Branding/Logo/Intercambio Summit 2026 - Logo 1.png"))
export(logo1, "summit-logo-primario", [120, 240])

logo2 = Image.open(f"{BASE}/Branding/Logo/Intercambio Summit 2026 - Logo 2.png")
print("logo2 canto:", logo2.convert("RGB").getpixel((4, 4)))
logo2 = trim(logo2)
export(logo2, "summit-logo-reverso", [120, 240])

# --- apoiadores (arquivos oficiais escolhidos) ---
# Normalização por ÁREA visual: alturas iguais fazem logos verticais (IALC)
# parecerem pequenos e horizontais (ALLY) dominarem. Cada logo é escalado para
# a mesma área e centrado numa caixa uniforme (170x70 de exibição, 2x retina).
APOIO = [
    ("belta",   f"{BASE}/Apoiadores/BELTA - Logomarca.png"),
    ("abrapei", f"{BASE}/Apoiadores/ABRAPEI - Logomarca.png"),
    ("ialc",    f"{BASE}/Apoiadores/IALC - LogoUntitled design.png"),
    ("allyhub", f"{BASE}/Apoiadores/AllyHub - Logo.png"),
    ("edvisor", f"{BASE}/Apoiadores/Edvisor - Logo.png"),
]
import math
BOX_W, BOX_H = 170, 70          # caixa de exibição (px CSS)
AREA = 5200.0                   # área-alvo do logo em px CSS
MAX_W, MAX_H = 164, 66          # margens dentro da caixa
SCALE = 2                       # export retina 2x

for name, path in APOIO:
    im = trim(Image.open(path)).convert("RGBA")
    ar = im.width / im.height
    h = math.sqrt(AREA / ar)
    w = h * ar
    if w > MAX_W: h *= MAX_W / w; w = MAX_W
    if h > MAX_H: w *= MAX_H / h; h = MAX_H
    w2, h2 = round(w * SCALE), round(h * SCALE)
    logo = im.resize((w2, h2), Image.LANCZOS)
    canvas = Image.new("RGBA", (BOX_W * SCALE, BOX_H * SCALE), (0, 0, 0, 0))
    canvas.paste(logo, ((canvas.width - w2) // 2, (canvas.height - h2) // 2), logo)
    out = os.path.join(OUT, f"apoio-{name}-box.png")
    canvas.save(out, optimize=True)
    print(f"apoio-{name}-box.png  logo {round(w)}x{round(h)} css px (área {round(w*h)})")
