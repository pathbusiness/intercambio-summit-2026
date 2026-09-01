#!/usr/bin/env python3
"""Renderizador dos criativos do Intercâmbio Summit 2026.

Cada peça é um template HTML editável em criativos/templates/ com
placeholders {{CHAVE}}. Este script substitui os placeholders, abre o
resultado no Chromium (Playwright) e exporta PNG no tamanho exato.

Uso:
    python3 criativos/render.py aprovacao   # os 3 modelos do briefing
    python3 criativos/render.py <template.html> chave=valor ... out=arquivo.png

Dependências: pip install playwright pillow (Chromium já disponível no
ambiente em /opt/pw-browsers; localmente, `playwright install chromium`).
"""
import json
import os
import sys
import glob

from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.abspath(__file__))
TPL = os.path.join(ROOT, "templates")
OUT = os.path.join(ROOT, "aprovacao")

SIZES = {"feed": (1080, 1350), "story": (1080, 1920), "linkedin": (1200, 627)}


def _chromium_path():
    base = os.environ.get("PLAYWRIGHT_BROWSERS_PATH", "/opt/pw-browsers")
    if os.path.exists(os.path.join(base, "chromium")):
        return os.path.join(base, "chromium")
    hits = glob.glob(os.path.join(base, "chromium-*", "chrome-linux*", "chrome"))
    return hits[0] if hits else None


def render_jobs(jobs):
    """jobs: lista de (template, dados_dict, png_de_saida, (w, h))."""
    with sync_playwright() as p:
        exe = _chromium_path()
        browser = p.chromium.launch(executable_path=exe) if exe else p.chromium.launch()
        page = browser.new_page(viewport={"width": 1080, "height": 1350}, device_scale_factor=1)
        for template, data, out_png, (w, h) in jobs:
            tpl_path = os.path.join(TPL, template)
            html = open(tpl_path, encoding="utf-8").read()
            for k, v in data.items():
                html = html.replace("{{%s}}" % k, str(v))
            tmp = tpl_path.replace(".html", ".__render__.html")
            with open(tmp, "w", encoding="utf-8") as f:
                f.write(html)
            try:
                page.set_viewport_size({"width": w, "height": h})
                page.goto("file://" + tmp)
                page.evaluate("document.fonts.ready.then(() => true)")
                page.wait_for_timeout(250)
                os.makedirs(os.path.dirname(out_png), exist_ok=True)
                page.screenshot(path=out_png, clip={"x": 0, "y": 0, "width": w, "height": h})
                print("ok", os.path.relpath(out_png, ROOT), f"{w}x{h}")
            finally:
                os.remove(tmp)
        browser.close()


def jobs_aprovacao():
    """Os três modelos da primeira entrega (seção 7 do briefing)."""
    fin = json.load(open(os.path.join(ROOT, "data", "finalistas.json"), encoding="utf-8"))
    cats = fin["_categorias"]
    por_slug = {f["slug"]: f for f in fin["finalistas"]}

    # Modelo C nos três piores casos de foto (validar no pior, não no melhor):
    # - vitor-cruz: estúdio profissional (e expressão séria -> tratamento soft)
    # - anderson-bertin: celular em fundo branco
    # - guilherme-garcia: recorte manual (microfone sob o queixo, fundo poluído)
    casos_c = ["vitor-cruz", "anderson-bertin", "guilherme-garcia"]

    jobs = [
        ("modelo-a-institucional.html",
         {"FOTO": "../../site/assets/img/eventos/plateia-2400.webp"},
         os.path.join(OUT, "modelo-a-institucional.png"), SIZES["feed"]),
        ("modelo-b-precos.html", {},
         os.path.join(OUT, "modelo-b-tabela-precos.png"), SIZES["feed"]),
    ]
    for slug in casos_c:
        f = por_slug[slug]
        cat = cats[f["categoria"]]
        jobs.append((
            "modelo-c-finalista.html",
            {
                "NOME": f["nome"],
                "CATEGORIA": cat["nome"],
                "TRILHA": cat["trilha"],
                "FOTO": f"../../site/assets/img/finalistas/{slug}-800.webp",
            },
            os.path.join(OUT, f"modelo-c-finalista-{slug}.png"),
            SIZES["feed"],
        ))
    return jobs


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "aprovacao":
        render_jobs(jobs_aprovacao())
        return
    if len(sys.argv) > 1 and sys.argv[1].endswith(".html"):
        data, out_png, size = {}, None, SIZES["feed"]
        for arg in sys.argv[2:]:
            k, _, v = arg.partition("=")
            if k == "out":
                out_png = v
            elif k == "size":
                size = SIZES[v]
            else:
                data[k] = v
        render_jobs([(sys.argv[1], data, out_png or "/tmp/render.png", size)])
        return
    print(__doc__)


if __name__ == "__main__":
    main()
