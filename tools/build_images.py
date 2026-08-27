#!/usr/bin/env python3
"""Pipeline de imagens do site Intercâmbio Summit 2026.

- Fotos do evento 2025: WebP em 3 larguras (2400/1600/900)
- Foto da Av. Paulista: corte da faixa superior esquerda (marca Citi) + 3 larguras
- Finalistas: recorte quadrado 800x800 com rosto detectado, olhos na linha do
  terço superior, tratamento unificado, WebP 800 e 400
"""
import os, re, sys, glob, unicodedata
from PIL import Image, ImageEnhance, ImageOps
import numpy as np
import cv2

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "site", "assets", "img")
BRAND_BLUE = (0, 68, 185)  # Summit Blue #0044B9 (manual da marca)

EVENT_WIDTHS = [2400, 1600, 900]
EVENT_PHOTOS = {
    "Intercambio Summit 1-42.jpg": "palco-telao",       # telão INTERCÂMBIO SUMMIT 2025
    "Intercambio Summit 1-7.jpg":  "trofeus",           # close dos troféus
    "Intercambio Summit 3-51.jpg": "palestra-plateia",  # palestrante + plateia de costas
    "Intercambio Summit 4-16.jpg": "plateia",           # plateia atenta, crachás
    "Intercambio Summit 4-75.jpg": "palestra-telao",    # 4ª Revolução Industrial
    "Intercambio Summit 5-17.jpg": "networking",        # foyer, banners patrocinadores
    "Intercambio Summit 5-68.jpg": "palestrante-close", # close ao microfone
    "Intercambio Summit 6-5.jpg":  "painel",            # painel com 4 no palco
    "Intercambio Summit 7-105.jpg": "premiados",        # 9 premiados com troféus
}

# finalista -> (arquivo, ajustes)
# soft=True: suavizar contraste (retratos sem sorriso)
# tight=True: enquadramento mais fechado (Guilherme Garcia, microfone sob o queixo)
FINALISTAS = {
    # Gestores de Instituições
    "anderson-bertin":    ("Finalistas - Gestores de Instituicoes/Anderson Bertin.jpeg", {}),
    "anderson-pacheco":   ("Finalistas - Gestores de Instituicoes/Anderson Pacheco.jpeg", {"soft": True}),
    "andressa-chantre":   ("Finalistas - Gestores de Instituicoes/Andressa Chantre.jpeg", {}),
    "camila-viana":       ("Finalistas - Gestores de Instituicoes/Camila Viana.jpeg", {}),
    "eddy-leite":         ("Finalistas - Gestores de Instituicoes/Eddy Leite.jpeg", {}),
    "erica-pereira":      ("Finalistas - Gestores de Instituicoes/Erica Pereira.jpeg", {}),
    "fabio-carola":       ("Finalistas - Gestores de Instituicoes/Fabio Carola.jpeg", {}),
    "francielly-gnoatto": ("Finalistas - Gestores de Instituicoes/Francielly Gnoatto.jpeg", {}),
    "guilherme-garcia":   ("Finalistas - Gestores de Instituicoes/Guilherme Garcia.jpeg", {"tight": True}),
    "gustavo-gandra":     ("Finalistas - Gestores de Instituicoes/Gustavo Gandra.jpeg", {}),
    "gustavo-machado":    ("Finalistas - Gestores de Instituicoes/Gustavo Machado.jpeg", {}),
    "igor-marinho":       ("Finalistas - Gestores de Instituicoes/Igor Marinho.jpg", {}),
    "murilo-fernandes":   ("Finalistas - Gestores de Instituicoes/Murilo Fernandes.jpeg", {}),
    "tatiana-menniti":    ("Finalistas - Gestores de Instituicoes/Tatiana Menniti .jpeg", {}),
    "vitor-alvarino":     ("Finalistas - Gestores de Instituicoes/Vitor Alvarino da Silva.png", {}),
    # Agentes de Intercâmbio
    "carla-mussoi":       ("Finalistas - Agentes de Intercambio/Carla Mussoi .jpeg", {}),
    "daniel-cuenca":      ("Finalistas - Agentes de Intercambio/Daniel Cuenca .jpeg", {}),
    "daniel-lara":        ("Finalistas - Agentes de Intercambio/Daniel Lara.jpeg", {}),
    "diego-paiva":        ("Finalistas - Agentes de Intercambio/Diego Paiva .jpeg", {}),
    "diogo-jansen":       ("Finalistas - Agentes de Intercambio/Diogo Jansen.jpeg", {}),
    "eduardo-frigo":      ("Finalistas - Agentes de Intercambio/Eduardo Frigo.jpeg", {}),
    "eduardo-henrique":   ("Finalistas - Agentes de Intercambio/Eduardo Henrique de Freitas Santos.jpeg", {"soft": True}),
    "fernanda-rocha":     ("Finalistas - Agentes de Intercambio/Fernanda Rocha.jpeg", {}),
    "hanna-alves":        ("Finalistas - Agentes de Intercambio/Hannah Alves.jpeg", {}),
    "karen-oliveira":     ("Finalistas - Agentes de Intercambio/Karen Oliveira .jpeg", {}),
    "karina-fiore":       ("Finalistas - Agentes de Intercambio/Karina Fiore.jpeg", {}),
    "matheus-campos":     ("Finalistas - Agentes de Intercambio/Matheus Campos.jpeg", {}),
    "myllena-pontes":     ("Finalistas - Agentes de Intercambio/Myllena Pontes.jpeg", {}),
    "rafaela-monteiro":   ("Finalistas - Agentes de Intercambio/Rafaela Monteiro.jpeg", {}),
    "victor-luraschi":    ("Finalistas - Agentes de Intercambio/Victor Luraschi.jpeg", {}),
    "vitor-cruz":         ("Finalistas - Agentes de Intercambio/Vitor Cruz.jpeg", {"soft": True}),
    "vivi-lac":           ("Finalistas - Agentes de Intercambio/Vivi Lac.jpeg", {}),
}

# Palestrantes 2026: mesmo tratamento dos finalistas (recorte + Summit Blue)
# precrop_bottom corta uma fração do rodapé do original antes do recorte de
# fundo (faixas de borda); erode encolhe a máscara para matar halo de fundo claro
PALESTRANTES = {
    "lucas-politi-wagner": ("/Users/rodrigocollaro/Forio Site/Forio Site backup 2026-08-25/Lucas Politi Wagner - Foto 1.jpeg", {"precrop_bottom": 0.04}),
    "myrko-micali":        ("/Users/rodrigocollaro/Forio Site/Forio Site backup 2026-08-25/Myrko Micali - Foto 1.jpeg", {}),
    "roberto-bihari":      ("/Users/rodrigocollaro/Downloads/PATH/Beto Bihari - Foto 2.png", {}),
    "rodrigo-collaro":     ("/Users/rodrigocollaro/Downloads/PATH/Rodrigo Collaro - Photo (PATH).jpeg", {"erode": 3}),
}

YUNET = cv2.FaceDetectorYN_create(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "yunet.onnx"), "", (320, 320),
    score_threshold=0.6)


def save_webp(im, path, quality=78):
    im.save(path, "WEBP", quality=quality, method=6)


def build_event_photos():
    os.makedirs(os.path.join(OUT, "eventos"), exist_ok=True)
    for fname, slug in EVENT_PHOTOS.items():
        src = os.path.join(ROOT, fname)
        with Image.open(src) as im:
            im = ImageOps.exif_transpose(im).convert("RGB")
            for w in EVENT_WIDTHS:
                if w >= im.width:
                    out = im.copy()
                else:
                    out = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
                save_webp(out, os.path.join(OUT, "eventos", f"{slug}-{w}.webp"))
        print(f"evento: {slug}")


def build_paulista(crop_left=0.0, crop_top=0.0):
    os.makedirs(os.path.join(OUT, "local"), exist_ok=True)
    src = os.path.join(ROOT, "Avenida Paulista", "pexels-kelly-17291126.jpg")
    with Image.open(src) as im:
        im = ImageOps.exif_transpose(im).convert("RGB")
        l = round(im.width * crop_left)
        t = round(im.height * crop_top)
        im = im.crop((l, t, im.width, im.height))
        for w in EVENT_WIDTHS:
            out = im if w >= im.width else im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
            save_webp(out, os.path.join(OUT, "local", f"paulista-{w}.webp"))
    print("paulista ok")


def detect_face(im):
    """Retorna (cx, cy_olhos, altura_rosto) ou None. YuNet devolve
    [x, y, w, h, olho_d_x, olho_d_y, olho_e_x, olho_e_y, ...]."""
    arr = cv2.cvtColor(np.array(im.convert("RGB")), cv2.COLOR_RGB2BGR)
    scale = 640.0 / max(arr.shape[:2])
    small = cv2.resize(arr, (round(arr.shape[1] * scale), round(arr.shape[0] * scale)))
    YUNET.setInputSize((small.shape[1], small.shape[0]))
    _, faces = YUNET.detect(small)
    if faces is None or len(faces) == 0:
        return None
    f = max(faces, key=lambda r: r[2] * r[3]) / scale
    x, y, w, h = f[0], f[1], f[2], f[3]
    eye_y = (f[5] + f[7]) / 2.0
    return (x + w / 2, eye_y, h)


def grade(im, soft=False):
    """Tratamento unificado: contraste e cor levemente normalizados."""
    im = ImageOps.autocontrast(im, cutoff=1)
    im = ImageEnhance.Color(im).enhance(0.96)       # dessatura de leve, temperatura neutra
    im = ImageEnhance.Contrast(im).enhance(0.90 if soft else 1.0)
    im = ImageEnhance.Brightness(im).enhance(1.02 if soft else 1.0)
    return im


CUTOUTS = os.path.join(ROOT, "tools", "cutouts")
_session = None


def cutout(slug, path, precrop_bottom=0.0):
    """Remove o fundo (cache em tools/cutouts) e assenta sobre o azul de marca."""
    global _session
    os.makedirs(CUTOUTS, exist_ok=True)
    cpath = os.path.join(CUTOUTS, f"{slug}.png")
    if not os.path.exists(cpath):
        from rembg import remove, new_session
        if _session is None:
            _session = new_session("u2net_human_seg")
        with Image.open(path) as raw:
            raw = ImageOps.exif_transpose(raw).convert("RGB")
            if precrop_bottom:
                raw = raw.crop((0, 0, raw.width, round(raw.height * (1 - precrop_bottom))))
            out = remove(raw, session=_session)
        out.save(cpath)
    return Image.open(cpath)


def crop_finalista(slug, path, opts):
    if os.environ.get("SUMMIT_BG") == "blue":
        from PIL import ImageFilter
        rgba = cutout(slug, path, precrop_bottom=opts.get("precrop_bottom", 0.0))
        # tratamento no sujeito ANTES do assentamento, para o azul ficar idêntico em todos
        rgb = grade(rgba.convert("RGB"), soft=opts.get("soft", False))
        alpha = rgba.split()[3]
        if opts.get("erode"):
            alpha = alpha.filter(ImageFilter.MinFilter(opts["erode"]))
        alpha = alpha.filter(ImageFilter.GaussianBlur(1.2))
        im = Image.new("RGB", rgba.size, BRAND_BLUE)
        im.paste(rgb, (0, 0), alpha)
        graded = True
    else:
        graded = False
        with Image.open(path) as raw:
            raw = ImageOps.exif_transpose(raw)
            if raw.mode == "RGBA":
                base = Image.new("RGB", raw.size, BRAND_BLUE)
                base.paste(raw, (0, 0), raw)
                im = base
            else:
                im = raw.convert("RGB")

    det = detect_face(im)
    W, H = im.size
    factor = 2.05 if opts.get("tight") else 2.55  # lado do quadrado em alturas de rosto
    if det:
        cx, eye_y, fh = det
        side = min(round(fh * factor), W, H)
        top = round(eye_y - side / 3.0)
        left = round(cx - side / 2.0)
    else:
        side = min(W, H)
        left = (W - side) // 2
        top = 0
        print(f"  AVISO: rosto não detectado em {slug}, corte central superior")

    left = max(0, min(left, W - side))
    top = max(0, min(top, H - side))
    im = im.crop((left, top, left + side, top + side))
    im = im.resize((800, 800), Image.LANCZOS)
    if not graded:
        im = grade(im, soft=opts.get("soft", False))

    d = os.path.join(OUT, opts.get("pasta", "finalistas"))
    os.makedirs(d, exist_ok=True)
    save_webp(im, os.path.join(d, f"{slug}-800.webp"), quality=82)
    save_webp(im.resize((400, 400), Image.LANCZOS), os.path.join(d, f"{slug}-400.webp"), quality=82)
    return im


def build_finalistas():
    thumbs = []
    for slug, (rel, opts) in FINALISTAS.items():
        im = crop_finalista(slug, os.path.join(ROOT, rel), opts)
        thumbs.append((slug, im.resize((220, 220), Image.LANCZOS)))
        print(f"finalista: {slug}")
    # folha de contato para conferência
    cols = 8
    rows = (len(thumbs) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * 230 + 10, rows * 250 + 10), (24, 24, 28))
    from PIL import ImageDraw
    dr = ImageDraw.Draw(sheet)
    for i, (slug, th) in enumerate(thumbs):
        x = 10 + (i % cols) * 230
        y = 10 + (i // cols) * 250
        sheet.paste(th, (x, y))
        dr.text((x + 2, y + 224), slug, fill=(230, 230, 230))
    sheet.save(os.path.join(ROOT, "tools", "contact-sheet.png"))
    print("contact sheet ok")


def build_palestrantes():
    for slug, (path, opts) in PALESTRANTES.items():
        opts = dict(opts, pasta="palestrantes")
        crop_finalista(slug, path, opts)
        print(f"palestrante: {slug}")


if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "all"
    if what in ("all", "eventos"):
        build_event_photos()
    if what in ("all", "finalistas"):
        build_finalistas()
    if what in ("all", "palestrantes"):
        build_palestrantes()
    if what in ("all", "paulista"):
        cl = float(sys.argv[2]) if len(sys.argv) > 2 else 0.0
        ct = float(sys.argv[3]) if len(sys.argv) > 3 else 0.0
        build_paulista(cl, ct)
