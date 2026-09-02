#!/usr/bin/env python3
"""Pacote de agendamento de setembro para o Canva Content Planner.

Monta criativos/out/setembro-planner/ com uma pasta por post
(AAAA-MM-DD-tema), os arquivos renomeados na convenção da casa
(SUMMIT-AAAAMMDD-tema-NN.jpg) e a legenda pronta em legenda.txt,
mais o calendário editorial AGENDAMENTO.md.

Regra da skill de publicação: NADA é agendado/publicado sem aprovação
explícita do Rodrigo, com arte e legenda exatas mostradas antes.
"""
import os
import shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "out", "setembro")
DST = os.path.join(ROOT, "out", "setembro-planner")

HASH_BASE = "#intercambiosummit #intercambio"

# (data, hora sugerida, slug, [arquivos de origem], legenda)
POSTS = [
    ("2026-09-02", "11h30", "save-the-date", ["p01-save-the-date.jpg"], """O Intercâmbio Summit 2026 tem data marcada: 11 de novembro, em São Paulo.

Um dia inteiro para donos de agências, representantes de instituições e gestores de internacionalização, com o tema que o próprio mercado escolheu: inteligência artificial na operação de quem vende intercâmbio.

São 144 lugares, e as inscrições já estão abertas: Lote Early Bird por R$ 350, ou 5x de R$ 70 sem juros, até 30 de setembro.

11 de novembro · São Paulo

Ingressos no link da bio.

""" + HASH_BASE + " #educacaointernacional #studyabroad #agenciadeintercambio #mercadodeintercambio #eventocorporativo #saopaulo #summit2026 #ia #networking #b2b"),

    ("2026-09-04", "11h30", "pauta-escolhida", ["p02-pauta-escolhida.jpg"], """A pauta de 2026 não fomos nós que escolhemos. Foram vocês.

Na pesquisa pós-evento de 2025, perguntamos qual sessão tinha sido a mais valiosa. A resposta mais citada foi inteligência artificial.

Em 2026, ela deixou de ser uma sessão e virou o evento inteiro: IA aplicada a atendimento, marketing e vendas na operação real de agências e instituições.

11 de novembro · São Paulo

Lote Early Bird até 30 de setembro, ingressos no link da bio.

""" + HASH_BASE + " #inteligenciaartificial #ia #educacaointernacional #agenciadeintercambio #mercadodeintercambio #studyabroad #eventob2b #saopaulo #summit2026 #inovacao"),

    ("2026-09-02", "17h00", "abertura-de-vendas", ["p03-abertura-de-vendas.jpg"], """Inscrições abertas para o Intercâmbio Summit 2026.

O encontro do mercado brasileiro de intercâmbio, agora com um dia inteiro dedicado à inteligência artificial na operação: atendimento, marketing e vendas.

São 144 lugares. Em 2025 foram 70 participantes e NPS 92, este ano a sala é maior e o formato tem mais tempo de networking.

Lote Early Bird: R$ 350 ou 5x de R$ 70 sem juros, até 30 de setembro.

11 de novembro · São Paulo

Ingressos no link da bio.

""" + HASH_BASE + " #educacaointernacional #agenciadeintercambio #studyabroad #mercadodeintercambio #eventob2b #saopaulo #summit2026 #ia #networking #earlybird"),

    ("2026-09-08", "11h30", "tabela-de-precos", ["p04-tabela-de-precos.jpg"], """O preço sobe. O evento é o mesmo.

A tabela de lotes do Intercâmbio Summit 2026 é uma escada: quem decide cedo paga R$ 350, quem deixa para a porta paga R$ 650.

Todos os lotes parcelam em 5x sem juros.

Mesmo preço do ano passado, para quem decide agora.

11 de novembro · São Paulo · 144 lugares

Ingressos no link da bio.

""" + HASH_BASE + " #educacaointernacional #agenciadeintercambio #mercadodeintercambio #studyabroad #eventob2b #saopaulo #summit2026 #earlybird #networking #gestao"),

    ("2026-09-10", "11h30", "primeiro-atendimento", ["p05-primeiro-atendimento.jpg"], """O primeiro atendimento do seu aluno já aconteceu. E não foi com você.

Antes de chamar a sua agência no WhatsApp, o estudante já perguntou destino, escola, visto e orçamento para uma inteligência artificial. A conversa que costumava começar no seu balcão agora começa em outro lugar.

O Intercâmbio Summit 2026 existe para discutir exatamente isso: como a operação de agências e instituições entra nessa nova jornada, sem perder o toque humano que fecha a venda.

11 de novembro · São Paulo

Lote Early Bird até 30 de setembro, ingressos no link da bio.

""" + HASH_BASE + " #inteligenciaartificial #ia #atendimento #agenciadeintercambio #educacaointernacional #mercadodeintercambio #studyabroad #saopaulo #summit2026 #vendas"),

    ("2026-09-12", "11h30", "prova-social", ["p06-prova-social.jpg"], """Intercâmbio Summit 2025, avaliado por quem esteve lá: 9,3 de 10 em satisfação, NPS 92, nenhum detrator.

Esses números vieram da pesquisa respondida pelos participantes, e ela também trouxe o pedido mais repetido: mais tempo para conversar.

Por isso 2026 muda o formato: menos palestras, intervalos mais longos. Foi o que vocês pediram.

11 de novembro · São Paulo · 144 lugares

Lote Early Bird até 30 de setembro, ingressos no link da bio.

""" + HASH_BASE + " #nps #educacaointernacional #agenciadeintercambio #mercadodeintercambio #studyabroad #eventob2b #networking #saopaulo #summit2026 #provasocial"),

    ("2026-09-16", "11h30", "temas-das-sessoes", [
        "p07-carrossel-01-capa.jpg", "p07-carrossel-02-tema.jpg",
        "p07-carrossel-03-tema.jpg", "p07-carrossel-04-tema.jpg",
        "p07-carrossel-05-cta.jpg"], """Os temas das sessões do Intercâmbio Summit 2026.

IA e Automação com Myrko Micali, a jornada do viajante no Google com Lucas Politi Wagner, e o painel principal sobre o panorama do mercado para 2027 com Roberto Bihari.

Arraste para ver o que já está confirmado. Os demais temas saem em breve.

11 de novembro · São Paulo · 144 lugares

Lote Early Bird até 30 de setembro, ingressos no link da bio.

""" + HASH_BASE + " #educacaointernacional #agenciadeintercambio #inteligenciaartificial #ia #google #mercadodeintercambio #studyabroad #saopaulo #summit2026 #networking"),

    ("2026-09-18", "11h30", "produtividade", ["p08-produtividade.jpg"], """Quanto tempo sua consultora leva para montar um comparativo de cinco escolas, em três destinos, com câmbio do dia, taxas, seguro e acomodação?

Se a resposta for mais de dez minutos, esse é o custo de não ter mudado nada ainda.

No Intercâmbio Summit 2026, o tema central é exatamente esse: onde a IA devolve horas para a sua equipe vender, sem robotizar o atendimento.

11 de novembro · São Paulo

Lote Early Bird até 30 de setembro, ingressos no link da bio.

""" + HASH_BASE + " #produtividade #inteligenciaartificial #ia #agenciadeintercambio #educacaointernacional #mercadodeintercambio #studyabroad #gestao #saopaulo #summit2026"),

    ("2026-09-23", "11h30", "myrko-micali", ["p09-myrko-micali.jpg", "p09b-versao-frase.jpg"], """Myrko Micali é o palestrante principal do Intercâmbio Summit 2026.

Engenheiro, fundador da Alfred Delivery, hoje à frente da doubleX e da NovaIA, ele aplica inteligência artificial dentro da operação de empresas e mede o resultado no caixa.

A sessão dele dá nome ao tema do ano: IA e Automação, atendimento, marketing e vendas com toque humano.

11 de novembro · São Paulo

Lote Early Bird até 30 de setembro, ingressos no link da bio.

""" + HASH_BASE + " #myrkomicali #inteligenciaartificial #ia #palestrante #educacaointernacional #agenciadeintercambio #mercadodeintercambio #saopaulo #summit2026 #automacao"),

    ("2026-09-23", "17h00", "carrossel-myrko", [
        "p09c-carrossel-1de9.jpg", "p09c-carrossel-2de9.jpg", "p09c-carrossel-3de9.jpg",
        "p09c-carrossel-4de9.jpg", "p09c-carrossel-5de9.jpg", "p09c-carrossel-6de9.jpg",
        "p09c-carrossel-7de9.jpg", "p09c-carrossel-8de9.jpg", "p09c-carrossel-9de9.jpg"], """Por que um engenheiro de logística é o palestrante principal de um evento de intercâmbio?

Arraste. A resposta está na pesquisa que vocês responderam em 2025.

Myrko Micali não conhece o intercâmbio por dentro. E é exatamente esse o ponto: quem conhece por dentro somos nós, o que falta é ver o problema de fora.

11 de novembro · São Paulo · 144 lugares

Early Bird até 30 de setembro, ingressos no link da bio.

""" + HASH_BASE + " #myrkomicali #inteligenciaartificial #ia #educacaointernacional #agenciadeintercambio #mercadodeintercambio #inovacao #saopaulo #summit2026 #networking"),

    ("2026-09-25", "11h30", "formato-mudou", ["p10-formato-mudou.jpg"], """Menos palestras. Intervalos mais longos.

O feedback de 2025 foi claro: o conteúdo era excelente, mas faltava tempo para conversar. Em um evento onde o networking fecha negócio, isso não é detalhe, é o produto.

Então mudamos o formato: 2026 tem menos tempo de palco e mais tempo de café, com 144 profissionais do mercado na mesma sala.

11 de novembro · São Paulo

Lote Early Bird até 30 de setembro, ingressos no link da bio.

""" + HASH_BASE + " #networking #educacaointernacional #agenciadeintercambio #mercadodeintercambio #studyabroad #eventob2b #saopaulo #summit2026 #relacionamento #negocios"),

    ("2026-09-29", "09h00", "ultimo-dia-early-bird", ["p11-ultimo-dia-2909.jpg"], """Último dia do Lote Early Bird.

R$ 350 hoje. R$ 650 na porta, dia 11 de novembro.

A diferença é de R$ 300 por uma decisão que você já sabe que vai tomar.

Amanhã, 30 de setembro, às 23h59, o lote vira.

11 de novembro · São Paulo · 144 lugares

Ingressos no link da bio.

""" + HASH_BASE + " #earlybird #educacaointernacional #agenciadeintercambio #mercadodeintercambio #studyabroad #eventob2b #saopaulo #summit2026 #ultimodia #networking"),

    ("2026-09-30", "08h00", "termina-hoje", ["p11-termina-hoje-3009.jpg"], """Termina hoje, 23h59: Lote Early Bird do Intercâmbio Summit 2026.

R$ 350 hoje, ou 5x de R$ 70 sem juros. Na porta, dia 11 de novembro, R$ 650.

A diferença é de R$ 300 por uma decisão que você já sabe que vai tomar.

11 de novembro · São Paulo · 144 lugares

Ingressos no link da bio.

""" + HASH_BASE + " #earlybird #terminahoje #educacaointernacional #agenciadeintercambio #mercadodeintercambio #studyabroad #saopaulo #summit2026 #eventob2b #ultimachamada"),
]


def main():
    if os.path.exists(DST):
        shutil.rmtree(DST)
    os.makedirs(DST)
    linhas = ["# Agendamento de setembro · Canva Content Planner",
              "",
              "Fluxo: canva.com/planner > conta do Instagram do Summit > data e hora >",
              "subir os arquivos da pasta do post > colar a legenda.txt > conferir preview > agendar.",
              "Horários são sugestão (público consome no meio do expediente); ajustar à vontade.",
              "",
              "| Data | Hora | Post | Arquivos | Status |",
              "|---|---|---|---|---|"]
    for data, hora, slug, arquivos, legenda in POSTS:
        pasta = os.path.join(DST, f"{data}-{slug}")
        os.makedirs(pasta)
        compact = data.replace("-", "")
        for i, arq in enumerate(arquivos, 1):
            shutil.copy2(os.path.join(SRC, arq),
                         os.path.join(pasta, f"SUMMIT-{compact}-{slug}-{i:02d}.jpg"))
        with open(os.path.join(pasta, "legenda.txt"), "w", encoding="utf-8") as f:
            f.write(legenda.strip() + "\n")
        linhas.append(f"| {data} | {hora} | {slug} | {len(arquivos)} | aguardando agendamento |")
    linhas += ["",
               "Observações:",
               "- Vendas abertas desde 02/09: P1 (11h30) anuncia e P3 (17h00) converte no mesmo dia.",
               "- 23/09 tem dois posts (anúncio do Myrko e carrossel 9 cards), manhã e fim de tarde.",
               "- O post do Myrko inclui a versão B (card de frase) como arquivo 02, opcional.",
               "- P11 tem versão do dia 29 (Último dia) e do dia 30 (Termina hoje, 23h59)."]
    with open(os.path.join(DST, "AGENDAMENTO.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(linhas) + "\n")
    print(f"{len(POSTS)} posts preparados em {os.path.relpath(DST, ROOT)}")


if __name__ == "__main__":
    main()
