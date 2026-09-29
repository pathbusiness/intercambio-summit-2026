#!/usr/bin/env python3
"""Campanha Instagram 29/09 a 31/10/2026: feed, reels e stories.

Duas frentes intercaladas:
  - IA na operação (tema do Summit) -> desperta interesse e vende ingresso
  - Prêmio Melhores Profissionais   -> votação pública de 01/10 a 30/10

Monta criativos/out/campanha-outubro/ com uma pasta por publicação
(AAAA-MM-DD-slug), a arte renomeada (SUMMIT-AAAAMMDD-slug-NN.jpg), a
legenda.txt (feed/reel) ou nota.txt (story, com o sticker a colocar) e o
calendário CALENDARIO.md.

Fatos do Prêmio (Regulamento Oficial, Drive): votação pública entre os
finalistas de 01/10 a 30/10; vencedores em 11/11. Nenhuma peça afirma
como o voto pesa na decisão final além do que o regulamento diz.

Regra da casa: NADA é publicado sem aprovação explícita do Rodrigo, com
arte e legenda exatas mostradas antes.

Uso:  python3 criativos/build_campanha_outubro.py
      (reels: python3 criativos/render_reel.py reel-ia-perguntas.html
       out=criativos/out/reels/reel-ia-perguntas.mp4)
"""
import datetime as dt
import json
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from render import render_jobs, SIZES, ROOT, PROD, pasta_finalista  # noqa: E402

DST = os.path.join(PROD, "campanha-outubro")
F, S = SIZES["feed"], SIZES["story"]

SITE = "intercambiosummit.com.br"
CTA_SITE = f'<span class="cta">{SITE}</span>'
DIAS = ["seg", "ter", "qua", "qui", "sex", "sáb", "dom"]

H_PREMIO = ("#intercambiosummit #intercambio #premiomelhoresprofissionais #educacaointernacional "
            "#agenciadeintercambio #mercadodeintercambio #reconhecimento #saopaulo #summit2026 "
            "#votacao #profissionaisdeintercambio #b2b")
H_IA = ("#intercambiosummit #intercambio #inteligenciaartificial #ia #educacaointernacional "
        "#agenciadeintercambio #mercadodeintercambio #eventob2b #saopaulo #summit2026 #inovacao "
        "#automacao #vendas")
H_LOTE = ("#intercambiosummit #intercambio #educacaointernacional #agenciadeintercambio "
          "#mercadodeintercambio #eventob2b #saopaulo #summit2026 #networking #ingressos")

POST_DEF = dict(BG="painel-plateia", POS="center top", CANTO="", KICKER="", TSIZE=112,
                TITULO="", TEXTO="", PILL="", CTA="")
STORY_DEF = dict(POST_DEF, TOP=620, FAIXA="flex", ZONA="", TSIZE=140)
SLIDE_DEF = dict(POST_DEF, FAIXA="none", CANTO_SHOW="none", N=1, TOTAL=1, TSIZE=96,
                 RODAPE="Intercâmbio Summit 2026 · 11 de novembro · São Paulo")


def pill(preco, ou):
    return f'<div class="pill-preco">{preco} <span class="ou">{ou}</span></div>'


def prazo(txt):
    return f'<div class="prazo">{txt}</div>'


def feed(**kw):
    return ("campanha-post.html", dict(POST_DEF, **kw), F)


def story(**kw):
    return ("campanha-story.html", dict(STORY_DEF, **kw), S)


def slide(**kw):
    return ("campanha-slide.html", dict(SLIDE_DEF, **kw), F)


PIECES = []  # cada item: data, hora, slug, formato, imgs|copias, legenda|nota


def add(data, hora, slug, formato, imgs=(), copias=(), legenda="", nota=""):
    PIECES.append(dict(data=data, hora=hora, slug=slug, formato=formato,
                       imgs=list(imgs), copias=list(copias), legenda=legenda, nota=nota))


# ------------------------------------------------------------------ FEED

add("2026-09-29", "17h00", "teaser-votacao", "feed", [feed(
    BG="trofeus", CANTO="branco", KICKER="Prêmio Melhores Profissionais 2026",
    TITULO="A VOTAÇÃO<br>ABRE DIA 1º<br>DE OUTUBRO", TSIZE=112,
    TEXTO="32 finalistas em 6 categorias. Salve este post: <strong>abre quinta-feira.</strong>")],
    legenda=f"""A votação do Prêmio Melhores Profissionais abre quinta-feira, 1º de outubro.

São 32 finalistas em 6 categorias, os mais votados pelo mercado na primeira etapa. A partir de quinta, o público elegível escolhe entre eles, até 30 de outubro.

Vale salvar este post e voltar aqui na quinta.

Os vencedores serão anunciados ao vivo no Intercâmbio Summit 2026, em 11 de novembro, em São Paulo.

{H_PREMIO}""")

add("2026-10-01", "11h30", "votacao-aberta", "feed", [feed(
    BG="trofeus", CANTO="branco", KICKER="Prêmio Melhores Profissionais 2026",
    TITULO="VOTAÇÃO<br>ABERTA", TSIZE=140,
    TEXTO="32 finalistas, 6 categorias. Vote até <strong>30 de outubro.</strong>", CTA=CTA_SITE)],
    legenda=f"""Votação aberta: escolha os melhores profissionais de intercâmbio de 2026.

São 32 finalistas em 6 categorias, e a votação vai até 30 de outubro. O público elegível vota entre os finalistas, e a avaliação final combina esse voto com a análise técnica dos comitês.

Vote em {SITE} (link na bio).

Os vencedores serão anunciados ao vivo no Intercâmbio Summit 2026, em 11 de novembro, em São Paulo.

{H_PREMIO}""")

add("2026-10-02", "11h30", "ia-lead-23h", "feed", [feed(
    BG="plateia", KICKER="IA na operação",
    TITULO="QUEM RESPONDE<br>O LEAD<br>ÀS 23H?", TSIZE=118,
    TEXTO="Se a resposta é <strong>“de manhã”</strong>, a inteligência artificial já é assunto da sua operação.",
    PILL=prazo("11 de novembro · São Paulo · 144 lugares"), CTA=CTA_SITE)],
    legenda=f"""Quem responde o lead que chegou às 23h na sua agência?

Se a resposta é "de manhã, quando a equipe chega", a inteligência artificial já é assunto da sua operação, quer você tenha decidido isso ou não.

O Intercâmbio Summit 2026 dedica o dia inteiro a esse tema: IA no atendimento, no marketing e nas vendas, com toque humano.

11 de novembro · São Paulo · 144 lugares

Segundo lote: R$ 450, ou 5x de R$ 90 sem juros, até 24 de outubro. Ingressos no link da bio.

{H_IA}""")

add("2026-10-08", "11h30", "segundo-lote", "feed", [feed(
    BG="painel-plateia", KICKER="Intercâmbio Summit 2026",
    TITULO="SEGUNDO<br>LOTE", TSIZE=124,
    TEXTO="11 de novembro · São Paulo · 144 lugares",
    PILL=pill("R$ 450", "ou 5x de R$ 90 sem juros") + prazo("Até 24 de outubro"), CTA=CTA_SITE)],
    legenda=f"""O Segundo lote do Intercâmbio Summit 2026 está aberto.

R$ 450, ou 5x de R$ 90 sem juros, até 24 de outubro. Depois disso, o Terceiro lote sobe para R$ 550.

Um dia inteiro sobre IA na operação de agências e instituições, o painel principal sobre o mercado em 2027 e a premiação dos melhores profissionais do setor. São 144 lugares.

11 de novembro · São Paulo

Ingressos no link da bio.

{H_LOTE}""")

# ------------------------------------------------- CARROSSEL: IA em 3 frentes

TOT = 6
add("2026-10-07", "11h30", "ia-tres-frentes", "carrossel", [
    slide(N=1, TOTAL=TOT, BG="plateia", CANTO_SHOW="block", FAIXA="flex", RODAPE="",
          KICKER="IA na operação", TITULO="3 FRENTES.<br>UM TEMA.", TSIZE=124,
          TEXTO="Onde a inteligência artificial entra na rotina de uma agência."),
    slide(N=2, TOTAL=TOT, BG="plateia", KICKER="01 · Atendimento",
          TITULO="PRIMEIRA<br>RESPOSTA<br>RÁPIDA",
          TEXTO="Triagem e retorno inicial mais ágeis, para a consultora entrar na conversa já com o contexto do estudante."),
    slide(N=3, TOTAL=TOT, BG="plateia", KICKER="02 · Marketing",
          TITULO="MAIS CONTEÚDO,<br>MENOS<br>RETRABALHO",
          TEXTO="Campanhas e posts com mais produção, com a voz da sua agência preservada."),
    slide(N=4, TOTAL=TOT, BG="plateia", KICKER="03 · Vendas",
          TITULO="FOLLOW-UP<br>E ORÇAMENTO<br>MAIS ÁGEIS",
          TEXTO="Comparativos e retornos que saem mais rápido, com a decisão final na mão de quem conhece o cliente."),
    slide(N=5, TOTAL=TOT, BG="plateia", KICKER="O que não muda",
          TITULO="A IA DEVOLVE<br>TEMPO. O VÍNCULO<br>É SEU.", TSIZE=88,
          TEXTO="Por isso o tema do Summit é IA na operação <strong>com toque humano.</strong>"),
    slide(N=6, TOTAL=TOT, BG="plateia", CANTO_SHOW="block", FAIXA="flex", RODAPE="",
          KICKER="Intercâmbio Summit 2026", TITULO="11 DE<br>NOVEMBRO", TSIZE=124,
          TEXTO="São Paulo · 144 lugares.<br>Segundo lote: <strong>R$ 450</strong> ou 5x de R$ 90 sem juros, até 24/10.",
          CTA=CTA_SITE),
], legenda=f"""Onde a inteligência artificial entra na rotina de uma agência? Em três frentes.

Atendimento: primeira resposta e triagem mais ágeis. Marketing: mais conteúdo com menos retrabalho. Vendas: follow-up e orçamento mais rápidos.

Em todas elas, o que fecha a venda continua sendo o vínculo da sua equipe com o cliente. Por isso o tema do Summit é IA na operação com toque humano.

11 de novembro · São Paulo · 144 lugares

Segundo lote: R$ 450, ou 5x de R$ 90 sem juros, até 24 de outubro. Ingressos no link da bio.

{H_IA}""")

# ------------------------------- CARROSSEL: uma categoria do Prêmio por vez


def carrossel_categoria(key, data, hora):
    d = json.load(open(os.path.join(ROOT, "data", "finalistas.json"), encoding="utf-8"))
    cat = d["_categorias"][key]
    fins = sorted((f for f in d["finalistas"] if f["categoria"] == key), key=lambda f: f["nome"])
    copias = [os.path.join(PROD, "premio", "capas", f"capa-{key}.jpg")]
    copias += [os.path.join(PROD, "premio", "finalistas", pasta_finalista(f["nome"]), "card-finalista.jpg")
               for f in fins]
    total = len(copias) + 1
    final = slide(N=total, TOTAL=total, BG="trofeus", CANTO="branco", CANTO_SHOW="block",
                  FAIXA="flex", RODAPE="", KICKER=f"{cat['nome']} · {len(fins)} finalistas",
                  TITULO="VOTE ATÉ<br>30 DE OUTUBRO", TSIZE=112,
                  TEXTO="Prêmio Melhores Profissionais 2026.<br>Anúncio dos vencedores ao vivo em <strong>11 de novembro.</strong>",
                  CTA=CTA_SITE)
    nomes = ", ".join(f["nome"] for f in fins)
    trilha = "Trilha Gestores de Instituições" if cat["trilha"] == "Instituições" else "Trilha Agentes de Intercâmbio"
    add(data, hora, f"premio-{key}", "carrossel", [final], copias,
        legenda=f"""{cat['nome']}: conheça os {len(fins)} finalistas.

{cat['descricao']}

Arraste para ver todos, em ordem alfabética: {nomes}. Cada um foi um dos mais votados pelo mercado na primeira etapa do prêmio ({trilha}).

A votação segue aberta até 30 de outubro, em {SITE} (link na bio).

Os vencedores serão anunciados ao vivo no Intercâmbio Summit 2026, em 11 de novembro, em São Paulo.

{H_PREMIO}""")


carrossel_categoria("transformador", "2026-10-05", "11h30")
carrossel_categoria("conector",      "2026-10-09", "11h30")
carrossel_categoria("acelerador",    "2026-10-13", "11h30")
carrossel_categoria("iniciativa",    "2026-10-16", "11h30")
carrossel_categoria("espirito",      "2026-10-20", "11h30")
carrossel_categoria("mente",         "2026-10-23", "11h30")

# ------------------------------------------------------------------ REELS

add("2026-10-01", "17h00", "reel-premio", "reel", copias=["reels/reel-premio.mp4"],
    legenda=f"""A votação do Prêmio Melhores Profissionais 2026 está aberta.

São 32 finalistas em 6 categorias, e a votação vai até 30 de outubro. O público elegível vota entre os finalistas, e a avaliação final combina esse voto com a análise técnica dos comitês.

Os vencedores serão anunciados ao vivo no Intercâmbio Summit 2026, em 11 de novembro, em São Paulo.

Vote agora: {SITE} (link na bio)

{H_PREMIO}""")

add("2026-10-06", "17h00", "reel-ia-perguntas", "reel", copias=["reels/reel-ia-perguntas.mp4"],
    legenda=f"""Quem responde o lead que chegou às 23h na sua agência?

Quantos orçamentos a sua equipe refaz do zero por semana? Quanto tempo sobra para vender?

Essas são as perguntas por trás do tema do Intercâmbio Summit 2026: IA na operação, no atendimento, no marketing e nas vendas, com toque humano.

11 de novembro, em São Paulo. Segundo lote: R$ 450, ou 5x de R$ 90 sem juros, até 24 de outubro.

Ingressos: {SITE} (link na bio)

{H_IA}""")

# ---------------------------------------------------------------- STORIES

SP = "Adicionar sticker de link: " + SITE
PREMIO_K = "Prêmio Melhores Profissionais 2026"

add("2026-09-29", "12h00", "story-teaser-1", "story", [story(
    BG="trofeus", CANTO="branco", KICKER=PREMIO_K, TITULO="DIA 1º<br>ABRE A<br>VOTAÇÃO",
    TEXTO="32 finalistas. 6 categorias.")], nota="Sem sticker.")
add("2026-09-30", "12h00", "story-earlybird-hoje", "story", [story(
    BG="painel-plateia", KICKER="Lote Early Bird", TITULO="TERMINA<br>HOJE",
    PILL=pill("R$ 350", "ou 5x de R$ 70 sem juros") + prazo("Até 23h59"), CTA=CTA_SITE,
    TOP=560, FAIXA="none")], nota="Opcional: sticker de contagem regressiva até 23h59.")
add("2026-09-30", "18h00", "story-teaser-2", "story", [story(
    BG="trofeus", CANTO="branco", KICKER=PREMIO_K, TITULO="AMANHÃ<br>ABRE A<br>VOTAÇÃO",
    TEXTO="32 finalistas. 6 categorias.")],
    nota="Opcional: sticker 'Lembrar' (lembrete) para 01/10.")
add("2026-10-01", "09h00", "story-votacao-aberta", "story", [story(
    BG="trofeus", CANTO="branco", KICKER=PREMIO_K, TITULO="VOTAÇÃO<br>ABERTA", TSIZE=150,
    TEXTO="Até <strong>30 de outubro.</strong>", TOP=420, FAIXA="none", ZONA="sticker")],
    nota=SP + " (zona livre y 1000 a 1500).")
add("2026-10-01", "12h00", "story-segundo-lote", "story", [story(
    BG="painel-plateia", KICKER="Intercâmbio Summit 2026", TITULO="SEGUNDO<br>LOTE", TSIZE=150,
    PILL=pill("R$ 450", "ou 5x de R$ 90 sem juros") + prazo("Até 24 de outubro"),
    TOP=420, FAIXA="none", ZONA="sticker")],
    nota=SP + " (ou link do checkout) na zona livre y 1000 a 1500.")
add("2026-10-02", "12h00", "story-enquete-ia", "story", [story(
    BG="plateia", KICKER="IA na operação", TITULO="SUA AGÊNCIA<br>JÁ USA IA NO<br>ATENDIMENTO?",
    TSIZE=112, TOP=420, FAIXA="none", ZONA="sticker")],
    nota="Sticker de ENQUETE na zona livre: 'Sim' / 'Ainda não'. Reagir aos votos no dia seguinte.")
add("2026-10-06", "12h00", "story-caixa-perguntas", "story", [story(
    BG="plateia", KICKER="IA na operação", TITULO="O QUE VOCÊ<br>QUER VER<br>SOBRE IA<br>NO PALCO?",
    TSIZE=112, TOP=420, FAIXA="none", ZONA="sticker")],
    nota="Sticker CAIXA DE PERGUNTAS na zona livre. Respostas viram conteúdo para a semana seguinte.")


def contagem_premio(data, grande, texto="32 finalistas. 6 categorias.", hora="12h00", slug=None):
    add(data, hora, slug or f"story-premio-{grande.lower().replace(' ', '-')}", "story", [story(
        BG="trofeus", CANTO="branco", KICKER="Votação até 30 de outubro", TITULO=grande,
        TSIZE=150, TEXTO=texto, CTA=CTA_SITE, TOP=520)],
        nota="Opcional: sticker de link. O endereço já está impresso na arte.")


contagem_premio("2026-10-07", "FALTAM<br>23 DIAS", slug="story-premio-faltam-23")
contagem_premio("2026-10-16", "FALTAM<br>14 DIAS", slug="story-premio-faltam-14")
contagem_premio("2026-10-23", "FALTAM<br>7 DIAS", slug="story-premio-faltam-7")
contagem_premio("2026-10-27", "FALTAM<br>3 DIAS", slug="story-premio-faltam-3")
contagem_premio("2026-10-28", "FALTAM<br>2 DIAS", slug="story-premio-faltam-2")
contagem_premio("2026-10-29", "AMANHÃ É O<br>ÚLTIMO DIA", slug="story-premio-amanha-ultimo-dia")
contagem_premio("2026-10-30", "ÚLTIMO DIA<br>PARA VOTAR", slug="story-premio-ultimo-dia",
                texto="Votação até 30 de outubro.")


def contagem_lote(data, grande, slug, nome="Segundo lote", preco="R$ 450",
                  ou="ou 5x de R$ 90 sem juros", ate="Até 24 de outubro"):
    add(data, "12h00", slug, "story", [story(
        BG="painel-plateia", KICKER=f"Intercâmbio Summit 2026 · {nome}", TITULO=grande,
        TSIZE=150, PILL=pill(preco, ou) + prazo(ate), CTA=CTA_SITE, TOP=520)],
        nota="Opcional: sticker de link. O endereço já está impresso na arte.")


contagem_lote("2026-10-17", "FALTAM<br>7 DIAS", "story-lote2-faltam-7")
contagem_lote("2026-10-21", "FALTAM<br>3 DIAS", "story-lote2-faltam-3")
contagem_lote("2026-10-24", "ÚLTIMO DIA<br>DO SEGUNDO<br>LOTE", "story-lote2-ultimo-dia")
contagem_lote("2026-10-25", "TERCEIRO<br>LOTE", "story-lote3-aberto", nome="Terceiro lote",
              preco="R$ 550", ou="ou 5x de R$ 110 sem juros", ate="Até 10 de novembro")

add("2026-10-31", "12h00", "story-votacao-encerrada", "story", [story(
    BG="trofeus", CANTO="branco", KICKER=PREMIO_K, TITULO="VOTAÇÃO<br>ENCERRADA", TSIZE=130,
    TEXTO="Obrigado a quem votou. Os vencedores serão anunciados ao vivo em <strong>11 de novembro.</strong>",
    CTA=CTA_SITE, TOP=520)], nota="Sem sticker.")


# ------------------------------------------------------------------ build

def main():
    if os.path.exists(DST):
        shutil.rmtree(DST)
    os.makedirs(DST)
    jobs, linhas = [], []
    for p in sorted(PIECES, key=lambda p: (p["data"], p["hora"], p["slug"])):
        pasta = os.path.join(DST, f"{p['data']}-{p['slug']}")
        os.makedirs(pasta)
        compact = p["data"].replace("-", "")
        arquivos = []
        # cópias primeiro (capa/cards existentes ou mp4), depois artes novas
        for src in p["copias"]:
            origem = src if os.path.isabs(src) else os.path.join(PROD, src)
            arquivos.append(("copia", origem))
        for tpl, dados, size in p["imgs"]:
            arquivos.append(("render", (tpl, dados, size)))
        for i, (tipo, item) in enumerate(arquivos, 1):
            if tipo == "copia":
                ext = os.path.splitext(item)[1]
                shutil.copy2(item, os.path.join(pasta, f"SUMMIT-{compact}-{p['slug']}-{i:02d}{ext}"))
            else:
                tpl, dados, size = item
                jobs.append((tpl, dados, os.path.join(pasta, f"SUMMIT-{compact}-{p['slug']}-{i:02d}.jpg"), size))
        if p["legenda"]:
            open(os.path.join(pasta, "legenda.txt"), "w", encoding="utf-8").write(p["legenda"].strip() + "\n")
        if p["nota"]:
            open(os.path.join(pasta, "nota.txt"), "w", encoding="utf-8").write(p["nota"].strip() + "\n")
        dia = DIAS[dt.date.fromisoformat(p["data"]).weekday()]
        linhas.append(f"| {p['data']} | {dia} | {p['hora']} | {p['formato']} | {p['slug']} | "
                      f"{len(arquivos)} | aguardando aprovação |")
    render_jobs(jobs)
    cab = ["# Campanha de outubro · calendário (29/09 a 31/10)", "",
           "Nada é publicado sem aprovação explícita, com arte e legenda exatas mostradas antes.",
           "Feed, carrossel e reel: colar `legenda.txt`. Story: seguir o `nota.txt` (sticker a colocar).", "",
           "| Data | Dia | Hora | Formato | Peça | Arquivos | Status |", "|---|---|---|---|---|---|---|"]
    open(os.path.join(DST, "CALENDARIO.md"), "w", encoding="utf-8").write("\n".join(cab + linhas) + "\n")
    print(f"{len(PIECES)} publicações preparadas em {os.path.relpath(DST, ROOT)}")


if __name__ == "__main__":
    main()
