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
VOTE = f"{SITE}/votar"  # página de votação (site/votacao.html, rewrite /votar)
CTA_VOTO = f'<span class="cta">{VOTE}</span>'
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


def _bg(kw):
    """BG chega como nome curto (painel, plateia-2...); o arquivo real leva o sufixo de tamanho."""
    b = kw.get("BG", "")
    if b and not b[-1].isdigit() or b == "plateia-2":
        kw = dict(kw, BG=b + ("-1600" if b == "plateia-2" else "-2400"))
    return kw


def feed(**kw):
    return ("campanha-post.html", dict(POST_DEF, **_bg(kw)), F)


def story(**kw):
    return ("campanha-story.html", dict(STORY_DEF, **_bg(kw)), S)


def slide(**kw):
    return ("campanha-slide.html", dict(SLIDE_DEF, **_bg(kw)), F)


def parceiros_slide(progresso=""):
    """Slide de parceiros (logos oficiais em cor, grandes): último ou penúltimo slide dos carrosséis."""
    return ("campanha-parceiros.html", dict(PROGRESSO=progresso, CTA=CTA_SITE), F)


def speaker_tpl(**kw):
    return ("campanha-speaker.html", dict(POST_DEF, **_bg(kw)), F)


PIECES = []  # cada item: data, hora, slug, formato, imgs|copias, legenda|nota


def add(data, hora, slug, formato, imgs=(), copias=(), legenda="", nota=""):
    PIECES.append(dict(data=data, hora=hora, slug=slug, formato=formato,
                       imgs=list(imgs), copias=list(copias), legenda=legenda, nota=nota))


# ------------------------------------------------------------------ FEED

add("2026-10-01", "09h30", "votacao-aberta", "feed", [feed(
    BG="trofeus", CANTO="branco", KICKER="Prêmio Melhores Profissionais 2026",
    TITULO="VOTAÇÃO<br>ABERTA", TSIZE=140,
    TEXTO="32 finalistas, 6 categorias. Vote até <strong>30 de outubro.</strong>", CTA=CTA_VOTO)],
    legenda=f"""Votação aberta: escolha os melhores profissionais de intercâmbio de 2026.

São 32 finalistas em 6 categorias, e a votação vai até 30 de outubro. O público elegível vota entre os finalistas, e a avaliação final combina esse voto com a análise técnica dos comitês.

Vote em {VOTE} (link na bio).

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

Lote Early Bird: R$ 350, ou 5x de R$ 70 sem juros, até 2 de outubro. Ingressos no link da bio.

{H_IA}""")

# ------------------------------------------------- CARROSSEL: IA em 3 frentes

TOT = 7
add("2026-10-07", "11h30", "ia-tres-frentes", "carrossel", [
    slide(N=1, TOTAL=TOT, BG="plateia", CANTO_SHOW="block", RODAPE="",
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
    parceiros_slide(f"6/{TOT}"),
    slide(N=7, TOTAL=TOT, BG="plateia", CANTO_SHOW="block", RODAPE="",
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
    for f in fins:  # card com destaque do dossiê (autorizado) quando existir; senão o card padrão
        pasta = os.path.join(PROD, "premio", "finalistas", pasta_finalista(f["nome"]))
        dossie = os.path.join(pasta, "card-dossie.jpg")
        copias.append(dossie if os.path.exists(dossie) else os.path.join(pasta, "card-finalista.jpg"))
    total = len(copias) + 2
    final = slide(N=total, TOTAL=total, BG="trofeus", CANTO="branco", CANTO_SHOW="block",
                  RODAPE="", KICKER=f"{cat['nome']} · {len(fins)} finalistas",
                  TITULO="VOTE ATÉ<br>30 DE OUTUBRO", TSIZE=112,
                  TEXTO="Prêmio Melhores Profissionais 2026.<br>Anúncio dos vencedores ao vivo em <strong>11 de novembro.</strong>",
                  CTA=CTA_VOTO)
    nomes = ", ".join(f["nome"] for f in fins)
    trilha = "Trilha Gestores de Instituições" if cat["trilha"] == "Instituições" else "Trilha Agentes de Intercâmbio"
    add(data, hora, f"premio-{key}", "carrossel", [parceiros_slide(), final], copias,
        legenda=f"""{cat['nome']}: conheça os {len(fins)} finalistas.

{cat['descricao']}

Arraste para ver todos, em ordem alfabética: {nomes}. Cada um foi um dos mais votados pelo mercado na primeira etapa do prêmio ({trilha}).

A votação segue aberta até 30 de outubro, em {VOTE} (link na bio).

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

Vote agora: {VOTE} (link na bio)

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
add("2026-09-30", "18h00", "story-teaser-2", "story", [story(
    BG="trofeus", CANTO="branco", KICKER=PREMIO_K, TITULO="AMANHÃ<br>ABRE A<br>VOTAÇÃO",
    TEXTO="32 finalistas. 6 categorias.")],
    nota="Opcional: sticker 'Lembrar' (lembrete) para 01/10.")
add("2026-10-01", "09h00", "story-votacao-aberta", "story", [story(
    BG="trofeus", CANTO="branco", KICKER=PREMIO_K, TITULO="VOTAÇÃO<br>ABERTA", TSIZE=150,
    TEXTO="Até <strong>30 de outubro.</strong>", TOP=420, FAIXA="none", ZONA="sticker")],
    nota=SP + " (zona livre y 1000 a 1500).")
add("2026-10-03", "12h00", "story-segundo-lote", "story", [story(
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
        TSIZE=150, TEXTO=texto, CTA=CTA_VOTO, TOP=520)],
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



# ------------------------------------------------------------ POSTS DIÁRIOS
# Estratégia de venda reversa: o post qualifica, desafia ou entrega a conta e
# deixa a pessoa se convencer sozinha. Escassez só a real (144 lugares, datas dos
# lotes). Nunca contagem de vendas inventada.


def diario(data, hora, slug, kicker, titulo, texto, legenda, tsize=118, bg="painel-plateia",
           pill_html="", cta=CTA_SITE, canto="", story_ok=True, story_hora="12h00", nota=None, story_ts=None):
    add(data, hora, slug, "feed", [feed(BG=bg, CANTO=canto, KICKER=kicker, TITULO=titulo,
                                        TSIZE=tsize, TEXTO=texto, PILL=pill_html, CTA=cta)],
        legenda=legenda)
    if story_ok:
        add(data, story_hora, f"story-{slug}", "story", [story(
            BG=bg, CANTO=canto, KICKER=kicker, TITULO=titulo, TSIZE=story_ts or int(tsize * 1.1),
            TEXTO=texto, PILL=pill_html, CTA=cta, TOP=520)],
            nota=nota or "Opcional: sticker de link. O endereço já está impresso na arte.")


EB_PILL = pill("R$ 350", "ou 5x de R$ 70 sem juros")

# Early Bird prorrogado até 02/10 (anúncio em 01/10). Os posts de 29 e 30/09 não citam
# data final: o prazo vigente ainda é 30/09 na comunicação, mas já está decidido que muda.
diario("2026-09-29", "19h00", "eb-nao-compre", "Lote Early Bird",
       "NÃO COMPRE<br>O EARLY BIRD.", tsize=124, bg="painel-plateia", pill_html=EB_PILL,
       texto="Se <strong>R$ 100 a mais</strong> não fazem diferença para você, espere. Depois do Early Bird, o mesmo ingresso custa R$ 450.",
       story_hora="19h30",
       legenda=f"""Não compre o Lote Early Bird se R$ 100 a mais não fazem diferença para você.

Sério: se o valor não pesa, pode esperar. Mas o lote não dura para sempre: depois dele, o ingresso do Intercâmbio Summit 2026 passa a R$ 450, depois R$ 550 e, no dia, R$ 650.

Hoje: R$ 350, ou 5x de R$ 70 sem juros.

11 de novembro · São Paulo · 144 lugares

Ingressos no link da bio.

{H_LOTE} #earlybird""")

diario("2026-09-30", "12h00", "eb-ainda-350", "Lote Early Bird",
       "AINDA É R$ 350.<br>NÃO VAI SER<br>PARA SEMPRE.", tsize=108, bg="plateia", pill_html=EB_PILL,
       texto="O evento é o mesmo e a sala também. Depois do Early Bird, o ingresso custa <strong>R$ 100 a mais.</strong>",
       story_hora="18h00", story_ts=108,
       legenda=f"""Ainda é R$ 350. Mas não vai ser para sempre.

O Lote Early Bird do Intercâmbio Summit 2026 está aberto: R$ 350, ou 5x de R$ 70 sem juros. Depois dele, o Segundo lote custa R$ 450. Mesmo dia, mesma sala, mesmas 144 cadeiras.

Não vamos insistir. Só deixar a conta à vista.

11 de novembro · São Paulo

Ingressos no link da bio.

{H_LOTE} #earlybird""")

diario("2026-10-01", "12h00", "eb-prorrogado", "Lote Early Bird · prorrogado",
       "EARLY BIRD<br>PRORROGADO<br>ATÉ 02/10.", tsize=104, bg="painel", story_hora="10h00", story_ts=112,
       pill_html=EB_PILL + prazo("Até sexta-feira, 02/10"),
       texto="Mais dois dias a <strong>R$ 350.</strong> Depois, o Segundo lote: R$ 450.",
       legenda=f"""Prorrogamos o Lote Early Bird até sexta-feira, 2 de outubro.

Mais dois dias para garantir o ingresso do Intercâmbio Summit 2026 por R$ 350, ou 5x de R$ 70 sem juros. Depois, o Segundo lote: R$ 450.

O que muda depois? Só o preço. O evento, a sala e as 144 cadeiras são os mesmos.

11 de novembro · São Paulo

Ingressos no link da bio.

{H_LOTE} #earlybird""")

diario("2026-10-02", "09h00", "eb-ultimo-dia", "Lote Early Bird · último dia",
       "AMANHÃ, R$ 100<br>A MAIS.", tsize=124, bg="plateia", story_hora="12h30", story_ts=124,
       pill_html=EB_PILL + prazo("Só até 23h59 de hoje"),
       texto="O evento é o mesmo. A sala é a mesma. O ingresso, <strong>não.</strong>",
       legenda=f"""Amanhã o mesmo ingresso custa R$ 100 a mais. O evento é o mesmo.

Hoje é o último dia do Lote Early Bird do Intercâmbio Summit 2026: R$ 350, ou 5x de R$ 70 sem juros, até 23h59.

A partir de amanhã, Segundo lote: R$ 450. Mesmo dia, mesma sala, mesmas 144 cadeiras.

11 de novembro · São Paulo

Ingressos no link da bio.

{H_LOTE} #earlybird #ultimodia""")

# --------------------------------------------- SÉRIE DIÁRIA 03/10 a 11/11
def leg(gancho, *paras, cta="Ingressos no link da bio.", tags=H_LOTE, local=True):
    partes = [gancho] + list(paras)
    if local:
        partes.append("11 de novembro · São Paulo · 144 lugares")
    if cta:
        partes.append(cta)
    partes.append(tags)
    return "\n\n".join(partes)


def speaker(data, hora, slug, foto, nome, cargo, kicker, titulo, texto, legenda, tsize=84):
    add(data, hora, slug, "feed", [speaker_tpl(
        BG="painel-plateia", SLUG=foto, NOME=nome, CARGO=cargo, KICKER=kicker, TITULO=titulo,
        TSIZE=tsize, TEXTO=texto, CTA=CTA_SITE)], legenda=legenda)


L2 = prazo("Segundo lote · R$ 450 · até 24/10")
L3 = prazo("Terceiro lote · R$ 550 · até 10/11")
P3 = pill("R$ 550", "ou 5x de R$ 110 sem juros")
H_PAINEL = ("#intercambiosummit #intercambio #belta #abrapei #ollara #econsulting #mercadodeintercambio "
            "#educacaointernacional #agenciadeintercambio #saopaulo #summit2026 #eventob2b #painel")

diario("2026-10-08", "11h30", "segundo-lote", "Segundo lote",
       "PODE ESPERAR.<br>O PRÓXIMO LOTE<br>É R$ 550.", tsize=100, bg="painel",
       texto="Segundo lote: <strong>R$ 450</strong>, ou 5x de R$ 90 sem juros, até 24 de outubro.",
       legenda=leg("Pode esperar. O próximo lote do Intercâmbio Summit 2026 é R$ 550.",
                   "O Segundo lote está aberto: R$ 450, ou 5x de R$ 90 sem juros, até 24 de outubro. Depois disso, R$ 550. No dia, R$ 650.",
                   "Um dia sobre IA na operação, o painel principal sobre o mercado em 2027 e a premiação dos melhores profissionais. A escolha é sua."))

diario("2026-10-03", "11h30", "nao-e-para-quem-sabe", "Antes de comprar o ingresso",
       "NÃO É PARA<br>QUEM JÁ SABE<br>TUDO DE IA.", tsize=104, bg="plateia-2", pill_html=L2,
       texto="Se a sua operação já roda no piso que você quer, pule este post. Se ainda tem <strong>trabalho repetitivo demais</strong>, o dia 11/11 é para você.",
       legenda=leg("Este evento não é para quem já sabe tudo sobre IA.",
                   "Se a sua operação já roda no nível que você quer, pode pular o Intercâmbio Summit 2026. Se ainda tem trabalho repetitivo demais no atendimento, no marketing e nas vendas, o tema de 11 de novembro é o seu.",
                   "Segundo lote: R$ 450, ou 5x de R$ 90 sem juros, até 24 de outubro.", tags=H_IA))

diario("2026-10-04", "11h30", "quem-deve-estar", "Quem deve estar na sala",
       "SE VOCÊ É<br>UM DESTES,<br>VENHA.", tsize=112, bg="networking",
       texto="Donos e gestores de agências<br>Instituições internacionais<br>Consultores e vendedores<br>Prestadores de serviço do setor",
       legenda=leg("Quem deve estar na sala em 11 de novembro?",
                   "Donos e gestores de agências. Instituições internacionais. Consultores e vendedores. Prestadores de serviço do setor, como seguro, câmbio, tecnologia e acomodação.",
                   "Se você não se reconhece em nenhum deles, tudo bem. Se reconhece, o Segundo lote (R$ 450, até 24 de outubro) é o momento."))

diario("2026-10-10", "11h30", "cetico", "Para céticos e ansiosos",
       "ACHA QUE IA<br>É MODISMO?<br>VENHA.", tsize=118, bg="painel-plateia", pill_html=L2,
       texto="Acha que é ameaça? Venha também. Só não venha se <strong>já tem todas as respostas.</strong>",
       legenda=leg("Acha que IA é modismo? Venha ao Summit mesmo assim.",
                   "Acha que é ameaça? Venha também. O tema de 2026, IA na operação com toque humano, é para quem tem dúvida, não para quem já tem certeza.",
                   "Segundo lote: R$ 450, ou 5x de R$ 90 sem juros, até 24 de outubro.", tags=H_IA))

diario("2026-10-11", "11h30", "voto-consciente", PREMIO_K,
       "NÃO VOTE EM<br>QUEM VOCÊ<br>NÃO CONHECE.", tsize=104, bg="premiados", canto="branco",
       texto="Vote em quem fez diferença no seu ano. Votação até <strong>30 de outubro.</strong>",
       legenda=leg("Não vote em quem você não conhece. Vote em quem fez diferença no seu ano.",
                   "São 32 finalistas em 6 categorias, e a votação vai até 30 de outubro. O regulamento não permite compra de votos nem manipulação de resultados.",
                   "Os vencedores serão anunciados ao vivo no Intercâmbio Summit 2026, em 11 de novembro, em São Paulo.",
                   cta=f"Vote em {VOTE} (link na bio).", tags=H_PREMIO, local=False), cta=CTA_VOTO)

diario("2026-10-12", "11h30", "ia-nao-fecha-venda", "IA na operação",
       "IA NÃO<br>FECHA VENDA.", tsize=132, bg="networking", pill_html=L2,
       texto="Quem fecha é a sua equipe, com o tempo que a IA devolveu. <strong>O Summit é sobre essa conta.</strong>",
       legenda=leg("IA não fecha venda. Quem fecha é a sua equipe.",
                   "O que a IA pode fazer é devolver tempo: menos trabalho repetitivo, mais conversa com o cliente. O Intercâmbio Summit 2026 é sobre essa conta, no atendimento, no marketing e nas vendas.",
                   "Segundo lote: R$ 450, ou 5x de R$ 90 sem juros, até 24 de outubro.", tags=H_IA))

speaker("2026-10-14", "11h30", "speaker-lucas-politi", "lucas-politi-wagner", "Lucas Politi Wagner",
        "Account Executive · Google Brasil", "Keynote · manhã de 11/11",
        "O CASO<br>GOOGLE:<br>IA EM<br>ATENDIMENTO<br>E VENDAS",
        "Se a sua agência já domina o tema, pode pular esta sessão.",
        leg("O caso Google de IA em atendimento e vendas, com Lucas Politi Wagner.",
            "Lucas Politi Wagner é Account Executive do Google Brasil e participa da programação da manhã do Intercâmbio Summit 2026, com IA aplicada a atendimento e vendas.",
            "Se a sua agência já domina o tema, pode pular esta sessão. Se não, ela merece um lugar na sua agenda.", tags=H_IA))

diario("2026-10-15", "11h30", "144-pessoas", "O tamanho do evento",
       "144 PESSOAS.<br>DÁ PARA<br>CONVERSAR COM<br>TODAS.", tsize=104, bg="painel", pill_html=L2,
       texto="Uma sala, um dia e intervalos mais longos para conhecer <strong>quem decide no setor.</strong>",
       legenda=leg("144 pessoas. Dá para conversar com todas.",
                   "O Intercâmbio Summit tem 144 lugares: uma sala, um dia e intervalos mais longos para conhecer quem decide no setor, sem multidão e sem correria.",
                   "Segundo lote: R$ 450, ou 5x de R$ 90 sem juros, até 24 de outubro.", local=False))

diario("2026-10-17", "11h30", "lote2-em-7-dias", "Segundo lote · faltam 7 dias",
       "EM 7 DIAS,<br>R$ 100<br>A MAIS.", tsize=130, bg="plateia-2", story_ok=False,
       pill_html=pill("R$ 450", "ou 5x de R$ 90 sem juros"),
       texto="Até 24 de outubro, R$ 450. Depois, <strong>R$ 550.</strong>",
       legenda=leg("Em 7 dias, o mesmo ingresso custa R$ 100 a mais.",
                   "O Segundo lote do Intercâmbio Summit 2026 vai até 24 de outubro: R$ 450, ou 5x de R$ 90 sem juros. Depois, Terceiro lote a R$ 550.",
                   "Mesmo evento, mesma sala. Só a data muda o preço."))

diario("2026-10-18", "11h30", "promessa-honesta", "Promessa honesta",
       "O SUMMIT NÃO<br>VAI SALVAR<br>SUA AGÊNCIA.", tsize=108, bg="painel-plateia", pill_html=L2,
       texto="Quem aplica o que ouve, sim. É um dia de conteúdo e contatos: <strong>o resto é com você.</strong>",
       legenda=leg("O Summit não vai salvar a sua agência. Quem aplica o que ouve, sim.",
                   "Prometemos um dia de conteúdo, painel e contatos do setor. O que muda na sua operação depende do que você levar dali para a segunda-feira.",
                   "Segundo lote: R$ 450, ou 5x de R$ 90 sem juros, até 24 de outubro."))

diario("2026-10-19", "11h30", "painel-2027", "Painel principal · tarde de 11/11",
       "MERCADO 2027:<br>QUEM ESTARÁ<br>NO PALCO.", tsize=96, bg="painel", story_ok=False,
       texto="<strong>Roberto Bihari</strong>, presidente da ABRAPEI<br><strong>Alexandre Argenta</strong>, presidente da BELTA<br><strong>Elaine Martins Fuzer</strong>, e_Consulting<br><strong>Lucas Montani</strong>, Ollara Education Hub<br>Mediação: <strong>Rodrigo Collaro</strong>, PATH",
       legenda=leg("Mercado de intercâmbio em 2027: quem estará no palco do painel principal.",
                   "Roberto Bihari (presidente da ABRAPEI), Alexandre Argenta (presidente da BELTA), Elaine Martins Fuzer (e_Consulting) e Lucas Montani (Ollara Education Hub), com mediação de Rodrigo Collaro (PATH).",
                   "Se você prefere planejar 2027 sem ouvir quem lidera o setor, pode pular este painel.", tags=H_PAINEL))

speaker("2026-10-21", "11h30", "speaker-gizelle-rezende", "gizelle-rezende", "Gizelle Rezende",
        "Director of Strategic Partnerships, Americas & APAC · The PIE", "Keynote · manhã de 11/11",
        "TENDÊNCIAS<br>GLOBAIS DA<br>EDUCAÇÃO<br>INTERNACIONAL",
        "Se o seu planejamento ignora o que acontece lá fora, este é o lugar.",
        leg("Tendências globais da educação internacional, com Gizelle Rezende, do The PIE.",
            "Gizelle Rezende é Director of Strategic Partnerships, Americas & APAC, do The PIE, media partner do Intercâmbio Summit 2026, e traz as tendências mundiais do setor na programação da manhã.",
            "Se o seu planejamento ignora o que acontece lá fora, este é o lugar.", tags=H_IA + " #thepie"), tsize=78)

diario("2026-10-22", "11h30", "lote2-ate-domingo", "Segundo lote · faltam 3 dias",
       "SE ESPERAR<br>ATÉ DOMINGO,<br>PAGA R$ 100<br>A MAIS.", tsize=98, bg="networking",
       texto="Sábado, 24 de outubro, é o último dia a <strong>R$ 450.</strong>", story_ts=100,
       legenda=leg("Se esperar até domingo, você paga R$ 100 a mais pelo mesmo ingresso.",
                   "Sábado, 24 de outubro, é o último dia do Segundo lote do Intercâmbio Summit 2026: R$ 450, ou 5x de R$ 90 sem juros. No domingo, o Terceiro lote começa a R$ 550."))

diario("2026-10-24", "11h30", "lote2-ultimo-dia-post", "Segundo lote · último dia",
       "AMANHÃ SÃO<br>R$ 550.", tsize=132, bg="painel-plateia", story_ok=False,
       pill_html=pill("R$ 450", "ou 5x de R$ 90 sem juros") + prazo("Só até 23h59 de hoje"),
       texto="Hoje ainda são <strong>R$ 450</strong>, ou 5x de R$ 90 sem juros.",
       legenda=leg("Amanhã o ingresso do Summit custa R$ 550. Hoje ainda são R$ 450.",
                   "Último dia do Segundo lote do Intercâmbio Summit 2026: R$ 450, ou 5x de R$ 90 sem juros, até 23h59.",
                   "Não vamos insistir. Só deixar a conta à vista."))

diario("2026-10-25", "11h30", "lote3-post", "Terceiro lote",
       "VOCÊ ESPEROU.<br>TUDO BEM.", tsize=118, bg="plateia-2", story_ok=False,
       pill_html=P3 + prazo("Até 10 de novembro"),
       texto="Agora são <strong>R$ 550.</strong> O evento continua o mesmo.",
       legenda=leg("Você esperou. Tudo bem. Agora o ingresso é R$ 550.",
                   "O Terceiro lote do Intercâmbio Summit 2026 está aberto: R$ 550, ou 5x de R$ 110 sem juros, até 10 de novembro. No dia do evento, R$ 650.",
                   "O evento continua o mesmo: IA na operação, painel sobre 2027 e o Prêmio Melhores Profissionais."))

diario("2026-10-26", "11h30", "a-conta", "A conta",
       "5X DE R$ 110<br>SEM JUROS.", tsize=124, bg="networking", pill_html=L3,
       texto="Quanto vale, para a sua agência, <strong>um contato que vira parceria?</strong> Faça a conta antes de decidir.",
       legenda=leg("5x de R$ 110 sem juros. Faça a conta antes de decidir.",
                   "Quanto vale, para a sua agência, um contato que vira parceria? Ou uma ideia de IA que economiza horas da equipe toda semana?",
                   "Terceiro lote do Intercâmbio Summit 2026: R$ 550, ou 5x de R$ 110 sem juros, até 10 de novembro."))

diario("2026-10-27", "11h30", "premio-faltam-3-post", "Votação até 30 de outubro",
       "FALTAM 3 DIAS.<br>NÃO DEIXE PARA<br>O ÚLTIMO.", tsize=104, bg="trofeus", canto="branco", story_ok=False,
       texto="32 finalistas, 6 categorias.",
       legenda=leg("Faltam 3 dias para a votação do Prêmio Melhores Profissionais.",
                   "São 32 finalistas em 6 categorias, e a votação vai até 30 de outubro. Não deixe para o último dia.",
                   "Os vencedores serão anunciados ao vivo em 11 de novembro, em São Paulo.",
                   cta=f"Vote em {VOTE} (link na bio).", tags=H_PREMIO, local=False), cta=CTA_VOTO)

diario("2026-10-28", "11h30", "o-dia-em-tres-atos", "11 de novembro · Contentix, Av. Paulista",
       "O DIA,<br>EM TRÊS<br>ATOS.", tsize=118, bg="painel", pill_html=L3,
       texto="<strong>Manhã:</strong> keynotes de IA e dados globais<br><strong>Tarde:</strong> painel principal sobre 2027<br><strong>16h30:</strong> Prêmio Melhores Profissionais",
       legenda=leg("O dia 11 de novembro, em três atos.",
                   "Manhã: keynotes de IA e dados globais. Tarde: painel principal sobre o mercado em 2027. 16h30: Prêmio Melhores Profissionais.",
                   "Contentix, Av. Paulista, 967, 9º andar, São Paulo.",
                   "Terceiro lote: R$ 550, ou 5x de R$ 110 sem juros, até 10 de novembro.", local=False))

diario("2026-10-29", "11h30", "premio-amanha-ultimo-post", "Votação até 30 de outubro",
       "AMANHÃ É O<br>ÚLTIMO DIA<br>PARA VOTAR.", tsize=110, bg="premiados", canto="branco", story_ok=False,
       texto="32 finalistas, 6 categorias.",
       legenda=leg("Amanhã é o último dia para votar no Prêmio Melhores Profissionais.",
                   "São 32 finalistas em 6 categorias. A votação termina em 30 de outubro.",
                   "Os vencedores serão anunciados ao vivo em 11 de novembro, em São Paulo.",
                   cta=f"Vote em {VOTE} (link na bio).", tags=H_PREMIO, local=False), cta=CTA_VOTO)

diario("2026-10-30", "11h30", "premio-ultimo-dia-post", "Votação até 30 de outubro",
       "ÚLTIMO DIA<br>PARA VOTAR.", tsize=126, bg="trofeus", canto="branco", story_ok=False,
       texto="Votação até 30 de outubro. Depois, só resta torcer.",
       legenda=leg("Último dia para votar no Prêmio Melhores Profissionais 2026.",
                   "Depois de hoje, só resta torcer. Os vencedores serão anunciados ao vivo no Intercâmbio Summit, em 11 de novembro, em São Paulo.",
                   cta=f"Vote em {VOTE} (link na bio).", tags=H_PREMIO, local=False), cta=CTA_VOTO)

diario("2026-10-31", "11h30", "votacao-encerrada-post", PREMIO_K,
       "VOTAÇÃO<br>ENCERRADA.", tsize=126, bg="premiados", canto="branco", story_ok=False, pill_html=L3,
       texto="Obrigado a quem votou. Os vencedores serão anunciados ao vivo em <strong>11 de novembro,</strong> às 16h30.",
       legenda=leg("Votação encerrada. Obrigado a quem votou.",
                   "Os vencedores do Prêmio Melhores Profissionais 2026 serão anunciados ao vivo no Intercâmbio Summit, em 11 de novembro, às 16h30, em São Paulo.",
                   "Terceiro lote: R$ 550, ou 5x de R$ 110 sem juros, até 10 de novembro.", tags=H_PREMIO))

diario("2026-11-01", "11h30", "faltam-10-dias", "Terceiro lote",
       "FALTAM<br>10 DIAS.", tsize=134, bg="painel-plateia", pill_html=P3,
       texto="Em 10 dias, a sala se enche de quem decide no setor. <strong>Você vai estar nela?</strong>",
       legenda=leg("Faltam 10 dias. Você vai estar na sala?",
                   "Em 11 de novembro, o Intercâmbio Summit 2026 reúne quem decide no setor de intercâmbio. Terceiro lote: R$ 550, ou 5x de R$ 110 sem juros, até 10 de novembro."))

diario("2026-11-02", "11h30", "onde-e", "Onde",
       "CONTENTIX,<br>AV. PAULISTA,<br>967.", tsize=112, bg="plateia", pill_html=L3,
       texto="9º andar, Bela Vista, São Paulo. <strong>Quarta-feira, 11 de novembro.</strong> A manhã já começa com keynotes.",
       legenda=leg("Onde é: Contentix, Av. Paulista, 967, 9º andar, Bela Vista, São Paulo.",
                   "Quarta-feira, 11 de novembro. A manhã já começa com keynotes, então vale chegar cedo.",
                   "Terceiro lote: R$ 550, ou 5x de R$ 110 sem juros, até 10 de novembro.", local=False))

diario("2026-11-03", "11h30", "quem-leva-o-trofeu", PREMIO_K,
       "QUEM LEVA<br>O TROFÉU?", tsize=126, bg="trofeus", canto="branco",
       texto="32 finalistas, 6 categorias. Saberemos <strong>ao vivo, às 16h30</strong> do dia 11.",
       legenda=leg("Quem leva o troféu do Prêmio Melhores Profissionais 2026?",
                   "São 32 finalistas em 6 categorias. Saberemos ao vivo, às 16h30 do dia 11 de novembro, no Intercâmbio Summit, em São Paulo.",
                   "Terceiro lote: R$ 550, ou 5x de R$ 110 sem juros, até 10 de novembro.", tags=H_PREMIO))

speaker("2026-11-04", "11h30", "speaker-myrko-micali", "myrko-micali", "Myrko Micali",
        "Empreendedor, referência em IA aplicada a negócios", "Palestrante principal",
        "ELE NÃO<br>CONHECE O<br>INTERCÂMBIO<br>POR DENTRO.<br>É O PONTO.",
        "Quem conhece por dentro somos nós. O que falta é <strong>ver o problema de fora.</strong>",
        leg("Myrko Micali não conhece o intercâmbio por dentro. É exatamente esse o ponto.",
            "Quem conhece o intercâmbio por dentro somos nós. O que falta é ver o problema de fora, e é isso que ele traz: IA aplicada a atendimento, marketing e vendas, com toque humano.",
            "Terceiro lote: R$ 550, ou 5x de R$ 110 sem juros, até 10 de novembro.", tags=H_IA + " #myrkomicali"), tsize=76)

diario("2026-11-05", "11h30", "faltam-6-dias", "Terceiro lote",
       "FALTAM 6 DIAS.<br>144 LUGARES.", tsize=112, bg="painel", pill_html=P3,
       texto="R$ 550 até 10/11. No dia do evento, <strong>R$ 650.</strong>",
       legenda=leg("Faltam 6 dias. São 144 lugares.",
                   "Terceiro lote do Intercâmbio Summit 2026: R$ 550, ou 5x de R$ 110 sem juros, até 10 de novembro. No dia do evento, R$ 650."))

diario("2026-11-06", "11h30", "intervalos-longos", "O que mudou em 2026",
       "MENOS<br>PALESTRAS.<br>INTERVALOS<br>MAIS LONGOS.", tsize=98, bg="networking", pill_html=L3,
       texto="Foi o que vocês pediram na pesquisa de 2025: <strong>tempo para conversar.</strong>",
       legenda=leg("Menos palestras. Intervalos mais longos. Foi o que vocês pediram.",
                   "Na pesquisa de 2025, o pedido mais repetido foi mais tempo para conversar. Em 2026, o formato mudou para dar espaço ao networking.",
                   "Terceiro lote: R$ 550, ou 5x de R$ 110 sem juros, até 10 de novembro."))

diario("2026-11-07", "11h30", "nao-vamos-convencer", "Última conversa franca",
       "NÃO VAMOS<br>TE CONVENCER<br>MAIS.", tsize=114, bg="plateia-2", pill_html=P3,
       texto="Você já viu o programa, os palestrantes e a conta. <strong>Se faz sentido, o Terceiro lote vai até 10/11.</strong>",
       legenda=leg("Não vamos te convencer mais.",
                   "Você já viu o programa, os palestrantes e a conta. Se faz sentido, o Terceiro lote do Intercâmbio Summit 2026 vai até 10 de novembro: R$ 550, ou 5x de R$ 110 sem juros."))

diario("2026-11-08", "11h30", "faltam-3-dias", "Terceiro lote",
       "FALTAM<br>3 DIAS.", tsize=140, bg="painel-plateia", pill_html=P3,
       texto="Terça-feira, 10 de novembro, é o último dia do Terceiro lote.",
       legenda=leg("Faltam 3 dias para o Intercâmbio Summit 2026.",
                   "Terça-feira, 10 de novembro, é o último dia do Terceiro lote: R$ 550, ou 5x de R$ 110 sem juros."))

diario("2026-11-09", "11h30", "amanha-ultimo-lote3", "Terceiro lote · penúltimo dia",
       "AMANHÃ É O<br>ÚLTIMO DIA<br>DO TERCEIRO<br>LOTE.", tsize=100, bg="painel",
       texto="No dia do evento, o ingresso é <strong>R$ 650</strong>, sujeito à disponibilidade de lugares.",
       legenda=leg("Amanhã é o último dia do Terceiro lote.",
                   "Hoje ainda é R$ 550, ou 5x de R$ 110 sem juros. No dia do evento, o ingresso é R$ 650, sujeito à disponibilidade de lugares."))

diario("2026-11-10", "11h30", "ultimo-dia-lote3", "Terceiro lote · último dia",
       "ÚLTIMO DIA<br>DO TERCEIRO<br>LOTE.", tsize=116, bg="networking", pill_html=P3 + prazo("Só até 23h59 de hoje"),
       texto="Amanhã: <strong>R$ 650</strong> na porta, se ainda houver lugar.",
       legenda=leg("Último dia do Terceiro lote. Amanhã, R$ 650.",
                   "Hoje o ingresso do Intercâmbio Summit 2026 ainda custa R$ 550, ou 5x de R$ 110 sem juros, até 23h59. No dia do evento, R$ 650, sujeito à disponibilidade de lugares."))

diario("2026-11-11", "08h00", "e-hoje", "11 de novembro · Contentix, Av. Paulista",
       "É HOJE.", tsize=160, bg="painel-plateia", story_hora="08h00",
       texto="Keynotes pela manhã, painel à tarde e o Prêmio às 16h30. <strong>Ingresso no dia: R$ 650</strong>, sujeito à disponibilidade.",
       legenda=leg("É hoje. Intercâmbio Summit 2026.",
                   "Keynotes pela manhã, painel principal à tarde e o Prêmio Melhores Profissionais às 16h30. Contentix, Av. Paulista, 967, 9º andar.",
                   "Ingresso no dia: R$ 650, sujeito à disponibilidade de lugares.", local=False))

# ------------------------------------------------------------------ build

POOL_GERAL = [("painel", "center top"), ("plateia-2", "35% top"), ("networking", "60% top"),
              ("painel-plateia", "40% top"), ("plateia", "70% top"), ("painel", "70% top"),
              ("palco-telao", "center top")]
POOL_PREMIO = [("trofeus", "center top"), ("premiados", "center top")]


def variar():
    """Fotos diferentes de uma peça para outra. Peças de IA/lote que ficaram no padrão
    (painel-plateia, plateia) entram na rotação; o Prêmio alterna troféus e premiados.
    Todos os slides de um carrossel usam a mesma foto."""
    gi = pi = 0
    for p in sorted(PIECES, key=lambda p: (p["data"], p["hora"], p["slug"])):
        if not p["imgs"]:
            continue
        bgs = {d.get("BG") for t, d, _ in p["imgs"] if t != "campanha-parceiros.html"}
        if bgs & {"painel-plateia-2400", "plateia-2400"} and len(bgs) == 1:
            nome, pos = POOL_GERAL[gi % len(POOL_GERAL)]
            gi += 1
        elif bgs == {"trofeus-2400"} and "premio-" in p["slug"] or bgs == {"trofeus-2400"} and "story-" in p["slug"]:
            nome, pos = POOL_PREMIO[pi % len(POOL_PREMIO)]
            pi += 1
        else:
            continue
        suf = "-1600" if nome == "plateia-2" else "-2400"
        for t, d, _ in p["imgs"]:
            if t != "campanha-parceiros.html":
                d["BG"], d["POS"] = nome + suf, pos


def com_parceiros():
    """Todo post de feed de imagem única ganha o slide de parceiros como 2º slide."""
    for p in PIECES:
        if p["formato"] == "feed" and len(p["imgs"]) == 1 and not p["copias"]:
            p["imgs"].append(parceiros_slide())
            p["formato"] = "carrossel"


def main():
    com_parceiros()
    variar()
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
