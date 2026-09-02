#!/usr/bin/env python3
"""Renderizador dos criativos do Intercâmbio Summit 2026.

Cada peça é um template HTML editável em criativos/templates/ com
placeholders {{CHAVE}}. Este script substitui os placeholders, abre o
resultado no Chromium (Playwright) e exporta a imagem no tamanho exato.

Uso:
    python3 criativos/render.py aprovacao   # os 3 modelos do briefing (PNG)
    python3 criativos/render.py setembro    # campanha P1-P11
    python3 criativos/render.py premio      # 6 capas + 32 finalistas x 4 + textos
    python3 criativos/render.py premio DIAS=3   # regera stories "faltam X dias"
    python3 criativos/render.py kit         # co-branded dos 5 apoiadores
    python3 criativos/render.py tudo        # setembro + premio + kit
    python3 criativos/render.py <template.html> chave=valor ... out=arquivo.png

Volume sai em JPEG q92 (Instagram/LinkedIn recomprimem de qualquer forma);
aprovação e banner de e-mail saem em PNG.

Dependências: pip install playwright pillow numpy (Chromium já disponível no
ambiente em /opt/pw-browsers; localmente, `playwright install chromium`).
"""
import json
import os
import sys
import glob
import unicodedata

from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.abspath(__file__))
TPL = os.path.join(ROOT, "templates")
OUT = os.path.join(ROOT, "aprovacao")
PROD = os.path.join(ROOT, "out")

SIZES = {"feed": (1080, 1350), "story": (1080, 1920), "linkedin": (1200, 627),
         "banner": (600, 200)}

FOTO_FINALISTA = "../../site/assets/img/finalistas/%s-800.webp"


def _chromium_path():
    base = os.environ.get("PLAYWRIGHT_BROWSERS_PATH", "/opt/pw-browsers")
    if os.path.exists(os.path.join(base, "chromium")):
        return os.path.join(base, "chromium")
    hits = glob.glob(os.path.join(base, "chromium-*", "chrome-linux*", "chrome"))
    return hits[0] if hits else None


def render_jobs(jobs):
    """jobs: lista de (template, dados_dict, arquivo_de_saida, (w, h)).
    A extensão do arquivo decide o formato: .png ou .jpg (q92)."""
    with sync_playwright() as p:
        exe = _chromium_path()
        browser = p.chromium.launch(executable_path=exe) if exe else p.chromium.launch()
        page = browser.new_page(viewport={"width": 1080, "height": 1350}, device_scale_factor=1)
        for template, data, out_img, (w, h) in jobs:
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
                page.wait_for_timeout(220)
                os.makedirs(os.path.dirname(out_img), exist_ok=True)
                kw = {"clip": {"x": 0, "y": 0, "width": w, "height": h}}
                if out_img.endswith(".jpg"):
                    kw.update(type="jpeg", quality=92)
                page.screenshot(path=out_img, **kw)
                print("ok", os.path.relpath(out_img, ROOT), f"{w}x{h}")
            finally:
                os.remove(tmp)
        browser.close()


def _faixa_dados():
    fin = json.load(open(os.path.join(ROOT, "data", "finalistas.json"), encoding="utf-8"))
    return fin["_categorias"], fin["finalistas"]


def _ascii(nome):
    return unicodedata.normalize("NFKD", nome).encode("ascii", "ignore").decode()


def pasta_finalista(nome):
    """'Anderson Bertin' -> 'AndersonBertin' (regra da entrega: NomeSobrenome)."""
    return _ascii(nome).replace(" ", "")


# ---------------------------------------------------------------- aprovação

def jobs_aprovacao():
    """Os três modelos da primeira entrega (seção 7 do briefing)."""
    cats, fins = _faixa_dados()
    por_slug = {f["slug"]: f for f in fins}
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
        jobs.append(("modelo-c-finalista.html",
                     {"NOME": f["nome"], "CATEGORIA": cat["nome"],
                      "TRILHA": cat["trilha"], "FOTO": FOTO_FINALISTA % slug},
                     os.path.join(OUT, f"modelo-c-finalista-{slug}.png"), SIZES["feed"]))
    return jobs


# ---------------------------------------------------------------- setembro

# Frases dos cards 2-8 do carrossel P9b (texto do briefing, verbatim)
P9B = [
    "Perguntamos na pesquisa de 2025 qual sessão foi <strong>a mais valiosa.</strong>",
    "A resposta mais citada foi <strong>inteligência artificial.</strong>",
    "E vários pediram temas que <strong>saíssem da caixa</strong> do setor.",
    "Myrko é engenheiro. Fundou e escalou uma startup de logística para as <strong>5 regiões do Brasil.</strong>",
    "Hoje aplica IA dentro da operação de empresas e mede o resultado <strong>no caixa.</strong>",
    "Ele não conhece o intercâmbio por dentro. <strong>E é exatamente esse o ponto.</strong>",
    "Quem conhece por dentro somos nós. O que falta é <strong>ver o problema de fora.</strong>",
]


def jobs_setembro():
    d = os.path.join(PROD, "setembro")
    F = SIZES["feed"]
    jobs = [
        ("setembro-p1-save-the-date.html", {}, os.path.join(d, "p01-save-the-date.jpg"), F),
        ("setembro-p2-pauta.html", {}, os.path.join(d, "p02-pauta-escolhida.jpg"), F),
        ("setembro-p3-abertura.html", {}, os.path.join(d, "p03-abertura-de-vendas.jpg"), F),
        ("modelo-b-precos.html", {}, os.path.join(d, "p04-tabela-de-precos.jpg"), F),
        ("setembro-p5-atendimento.html", {}, os.path.join(d, "p05-primeiro-atendimento.jpg"), F),
        ("setembro-p6-prova-social.html", {}, os.path.join(d, "p06-prova-social.jpg"), F),
        ("setembro-p7-capa.html", {}, os.path.join(d, "p07-carrossel-01-capa.jpg"), F),
    ]
    temas = json.load(open(os.path.join(ROOT, "data", "sessoes.json"), encoding="utf-8"))["temas"]
    total = len(temas) + 2
    for i, t in enumerate(temas):
        jobs.append(("setembro-p7-tema.html",
                     {"NUM": t["num"], "TITULO": t["titulo"], "QUEM": t["quem"],
                      "PROGRESSO": f"{i + 2}/{total}"},
                     os.path.join(d, f"p07-carrossel-{i + 2:02d}-tema.jpg"), F))
    jobs += [
        ("setembro-p7-cta.html", {}, os.path.join(d, f"p07-carrossel-{total:02d}-cta.jpg"), F),
        ("setembro-p8-produtividade.html", {}, os.path.join(d, "p08-produtividade.jpg"), F),
        ("setembro-p9-myrko.html", {}, os.path.join(d, "p09-myrko-micali.jpg"), F),
        ("setembro-p9-frase.html", {}, os.path.join(d, "p09b-versao-frase.jpg"), F),
        ("setembro-p9b-capa.html", {}, os.path.join(d, "p09c-carrossel-1de9.jpg"), F),
    ]
    for i, txt in enumerate(P9B):
        jobs.append(("setembro-p9b-card.html",
                     {"TEXTO": txt, "PROGRESSO": f"{i + 2}/9"},
                     os.path.join(d, f"p09c-carrossel-{i + 2}de9.jpg"), F))
    jobs += [
        ("setembro-p9b-final.html", {}, os.path.join(d, "p09c-carrossel-9de9.jpg"), F),
        ("setembro-p10-formato.html", {}, os.path.join(d, "p10-formato-mudou.jpg"), F),
        ("setembro-p11-ultimo-dia.html", {"HEADLINE": "ÚLTIMO DIA"},
         os.path.join(d, "p11-ultimo-dia-2909.jpg"), F),
        ("setembro-p11-ultimo-dia.html", {"HEADLINE": "TERMINA HOJE, 23H59"},
         os.path.join(d, "p11-termina-hoje-3009.jpg"), F),
    ]
    return jobs


# ---------------------------------------------------------------- prêmio

# Endereço de votação confirmado pelo Rodrigo em 01/09.
# Se um dia mudar: trocar aqui e rodar `python3 criativos/render.py premio`.
URL_VOTACAO = "intercambiosummit.com.br"

TEXTO_SUGERIDO = """Estou entre os finalistas do Prêmio Melhores Profissionais 2026, na categoria {categoria} (trilha {trilha}).

O prêmio reconhece os profissionais que fizeram a diferença no mercado de intercâmbio no último ano, e a votação está aberta até 30 de outubro.

Se o meu trabalho já cruzou o seu caminho, seu voto significa muito: {url}

A entrega acontece no Intercâmbio Summit 2026, dia 11 de novembro, em São Paulo.

#IntercambioSummit2026 #PremioMelhoresProfissionais
"""


def jobs_premio(dias="7"):
    cats, fins = _faixa_dados()
    jobs = []
    F, S = SIZES["feed"], SIZES["story"]

    for key, cat in cats.items():
        jobs.append(("premio-capa-categoria.html",
                     {"CATEGORIA": cat["nome"], "DESCRICAO": cat["descricao"],
                      "TRILHA": cat["trilha"]},
                     os.path.join(PROD, "premio", "capas", f"capa-{key}.jpg"), F))

    for f in fins:
        cat = cats[f["categoria"]]
        pasta = os.path.join(PROD, "premio", "finalistas", pasta_finalista(f["nome"]))
        dados = {"NOME": f["nome"], "CATEGORIA": cat["nome"], "TRILHA": cat["trilha"],
                 "FOTO": FOTO_FINALISTA % f["slug"], "URL": URL_VOTACAO, "DIAS": dias}
        jobs += [
            ("modelo-c-finalista.html", dados, os.path.join(pasta, "card-finalista.jpg"), F),
            ("premio-vote-card.html", dados, os.path.join(pasta, "card-votacao.jpg"), F),
            ("premio-story-votacao.html", dados, os.path.join(pasta, "story-votacao.jpg"), S),
            ("premio-story-faltam.html", dados,
             os.path.join(pasta, f"story-faltam-{dias}-dias.jpg"), S),
        ]
    return jobs


def escreve_textos():
    cats, fins = _faixa_dados()
    for f in fins:
        cat = cats[f["categoria"]]
        pasta = os.path.join(PROD, "premio", "finalistas", pasta_finalista(f["nome"]))
        os.makedirs(pasta, exist_ok=True)
        with open(os.path.join(pasta, "texto-sugerido.txt"), "w", encoding="utf-8") as fh:
            fh.write(TEXTO_SUGERIDO.format(categoria=cat["nome"], trilha=cat["trilha"],
                                           url=URL_VOTACAO))
    print(f"textos sugeridos: {len(fins)} arquivos")


# ---------------------------------------------------------------- kit

# QUEM: BELTA/ABRAPEI/IALC são associações; Ally Hub e Edvisor são empresas
# (confirmar redação com cada parceiro antes de publicar)
APOIADORES = [
    {"id": "belta",   "NOME": "BELTA",    "QUEM": "Associados", "LOGO_H": 62, "LOGO_H_STORY": 70, "LOGO_H_BANNER": 38},
    {"id": "abrapei", "NOME": "ABRAPEI",  "QUEM": "Associados", "LOGO_H": 72, "LOGO_H_STORY": 82, "LOGO_H_BANNER": 44},
    {"id": "ialc",    "NOME": "IALC",     "QUEM": "Associados", "LOGO_H": 76, "LOGO_H_STORY": 86, "LOGO_H_BANNER": 46},
    {"id": "allyhub", "NOME": "Ally Hub", "QUEM": "Clientes",   "LOGO_H": 56, "LOGO_H_STORY": 64, "LOGO_H_BANNER": 34},
    {"id": "edvisor", "NOME": "Edvisor",  "QUEM": "Clientes",   "LOGO_H": 68, "LOGO_H_STORY": 78, "LOGO_H_BANNER": 42},
]


def jobs_kit():
    jobs = []
    for a in APOIADORES:
        d = os.path.join(PROD, "kit-apoiadores", a["id"])
        dados = dict(a, LOGO=f"../assets/marca/apoio-{a['id']}-branco.png")
        jobs += [
            ("kit-apoiador-feed.html", dados, os.path.join(d, "feed-1080x1350.jpg"), SIZES["feed"]),
            ("kit-apoiador-story.html", dados, os.path.join(d, "story-1080x1920.jpg"), SIZES["story"]),
            ("kit-apoiador-banner.html", dados, os.path.join(d, "banner-email-600x200.png"), SIZES["banner"]),
        ]
    return jobs


# ---------------------------------------------------------------- cli

def main():
    args = sys.argv[1:]
    extra = dict(a.split("=", 1) for a in args[1:] if "=" in a)
    alvo = args[0] if args else ""

    if alvo == "aprovacao":
        render_jobs(jobs_aprovacao())
    elif alvo == "setembro":
        render_jobs(jobs_setembro())
    elif alvo == "premio":
        render_jobs(jobs_premio(dias=extra.get("DIAS", "7")))
        escreve_textos()
    elif alvo == "kit":
        render_jobs(jobs_kit())
    elif alvo == "tudo":
        render_jobs(jobs_setembro() + jobs_premio(dias=extra.get("DIAS", "7")) + jobs_kit())
        escreve_textos()
    elif alvo.endswith(".html"):
        data, out_img, size = {}, None, SIZES["feed"]
        for k, v in extra.items():
            if k == "out":
                out_img = v
            elif k == "size":
                size = SIZES[v]
            else:
                data[k] = v
        render_jobs([(alvo, data, out_img or "/tmp/render.png", size)])
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
