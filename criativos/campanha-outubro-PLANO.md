# Campanha Instagram · 29/09 a 11/11/2026

Objetivo: encher as 144 cadeiras do Intercâmbio Summit (11/11, São Paulo) e sustentar a votação do
Prêmio Melhores Profissionais (01/10 a 30/10). **Um post de feed por dia, todos os dias**, mais reels
e stories.

Regra da casa: nada é publicado sem aprovação explícita, com arte e legenda exatas mostradas antes.
A publicação é manual (o conector do Instagram segue sem a permissão de publicar).

Calendário completo, com uma pasta por publicação (arte + `legenda.txt` ou `nota.txt`):
`criativos/out/campanha-outubro/CALENDARIO.md`

## Venda reversa: como os posts vendem

Em vez de empurrar o ingresso, o post qualifica, desafia ou deixa a conta à vista, e a pessoa se
convence sozinha. Seis técnicas, todas em uso:

| Técnica | Exemplo no calendário |
|---|---|
| Desqualificar | "Não é para quem já sabe tudo de IA" (03/10) · "Acha que IA é modismo? Venha." (10/10) |
| Autosseleção | "Se você é um destes, venha" (04/10) |
| Contra-intuitivo | "Não compre o Early Bird." (29/09) · "Pode esperar. O próximo lote é R$ 550." (08/10) |
| Conta à vista | "Amanhã, R$ 100 a mais." (30/09) · "5x de R$ 110 sem juros. Faça a conta." (26/10) |
| Escassez real | "São 144 lugares. Não tem 145." (15/10) |
| Franqueza | "O Summit não vai salvar a sua agência." (18/10) · "Não vamos te convencer mais." (07/11) |

**Limite de integridade:** a escassez só usa o que é verdade (144 lugares e as datas dos lotes). Não há
contagem de vendas inventada ("restam X vagas"). Se você me passar o número real de ingressos vendidos,
posso usar como prova social.

Degraus de preço usados: Early Bird R$ 350 (até 30/09) · Segundo lote R$ 450 (01/10 a 24/10) ·
Terceiro lote R$ 550 (25/10 a 10/11) · no dia R$ 650 (sujeito à disponibilidade).

## Parceiros nas artes

Todas as peças novas trazem a faixa em três níveis, como no site: **Patrocínio** (Ollara, CLIDA,
Ikon Institute of Australia + Australian Learning Group), **Media partner** (The PIE) e **Apoio**
(BELTA, ABRAPEI, IALC, Ally Hub, Edvisor). Está em feeds, carrosséis, palestrantes, stories (exceto os que
reservam espaço para sticker), nos 5 reels, nas capas das categorias do Prêmio e nos cards de finalista.

Não recebem a faixa, pelo briefing: cards individuais de voto e stories de voto por finalista.

Os logos são as versões brancas monocromáticas (`tools/build_criativos_marca.py`), o mesmo tratamento já
decidido para os apoiadores. **O manual de marca (seção 08) pede confirmação escrita do parceiro antes de
publicar material co-branded**; os quatro logos novos (Ollara, CLIDA, Ikon/ALG, The PIE) entram nessa lista.

## Variedade de imagens

Rotação de 9 fotos de evento (painel, painel-plateia, plateia, plateia-2, networking, palco-telão,
troféus, premiados). A foto aparece com clareza na faixa superior de cada peça, onde só há o logo, e o
véu escuro protege a zona do texto. Fora de uso por risco: `palestra-plateia` (o @ da palestrante aparece
no slide), `palestrante-close` (slide com dado de terceiros) e `palestra-telao` (slide legível).

## Ritmo por fase

| Fase | Datas | Foco |
|---|---|---|
| 1 | 29/09 a 30/09 | Early Bird em venda reversa, teaser da votação |
| 2 | 01/10 a 08/10 | Votação abre, Segundo lote, IA entra |
| 3 | 09/10 a 24/10 | Uma categoria do Prêmio a cada 3 a 4 dias, palestrantes, painel, Segundo lote fecha |
| 4 | 25/10 a 31/10 | Terceiro lote, reta final e encerramento da votação |
| 5 | 01/11 a 11/11 | Contagem regressiva, onde é, programa, último dia do lote, "é hoje" |

Feed: 43 posts prontos (7 carrosséis); 06/10 é o dia do reel. Os 44 dias de 29/09 a 11/11 estão cobertos. Stories: 41 peças (versões dos posts diários, contagens e
enquetes). Reels prontos: Prêmio (01/10) e IA em perguntas (06/10), mais os 4 de setembro.
**Ainda não produzidos:** reels novos para outubro e novembro (sugestões: último dia do Segundo lote 23/10,
Prêmio última semana 27/10, último dia de votação 30/10, contagem final 09/11).

## Precisa da sua decisão antes de publicar

1. **O site não tem interface de votação.** O `main` só lista os finalistas. Toda peça manda votar em
   `intercambiosummit.com.br`; isso precisa estar no ar em 01/10.
2. **Como o voto pesa.** As legendas só dizem que "a avaliação final combina esse voto com a análise técnica
   dos comitês". O post "Como funciona a votação" segue bloqueado até você confirmar: quem vota em qual
   trilha, se é um voto por categoria e o peso do voto público nos comitês.
3. **Venda no dia.** Os posts de 09/11 a 11/11 dizem "R$ 650, sujeito à disponibilidade". Confirme se haverá
   venda no dia e como.
4. **Horários.** A premiação às 16h30 vem do site. Se a votação tiver hora de corte no dia 30/10, me diga.
5. **Confirmação dos parceiros** para os logos novos (ver acima).
6. **Peças de setembro já feitas** (P1 a P11, pinados, kit) continuam com a faixa antiga, só de Apoio.
   Se quiser, atualizo todas.
7. **Ally Hub.** O press release do Drive cita "Apply Hub"; as artes usam Ally Hub.
8. **Conteúdo de IA.** As "3 frentes" descrevem o tema anunciado de forma geral. Nenhuma estatística
   externa foi usada. Vale conferir com os palestrantes.

## Como reproduzir

```
python3 criativos/build_campanha_outubro.py        # artes + legendas + CALENDARIO.md
python3 criativos/render.py premio                 # capas e cards de finalista
python3 criativos/render_reel.py reel-ia-perguntas.html out=criativos/out/reels/reel-ia-perguntas.mp4
```

Templates: `campanha-post.html`, `campanha-speaker.html`, `campanha-slide.html`, `campanha-story.html`.
A faixa de parceiros é um bloco único (`templates/_parceiros.html`, tag `{{PARCEIROS}}`): mudar lá muda em tudo.
Para trocar texto, data ou hora, edite `PIECES` e as chamadas `diario(...)` em `build_campanha_outubro.py`.
