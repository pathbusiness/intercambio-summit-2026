# Campanha Instagram · 29/09 a 11/11/2026

Objetivo: encher as 144 cadeiras do Intercâmbio Summit (11/11, São Paulo) e sustentar a votação do
Prêmio dos Melhores Profissionais de Intercâmbio (01/10 a 30/10). **Um post de feed por dia, todos os dias**, mais reels
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
| Conta à vista | "Amanhã, R$ 100 a mais." (02/10) · "5x de R$ 110 sem juros. Faça a conta." (26/10) |
| Tamanho como benefício | "144 pessoas. Dá para conversar com todas." (15/10) |
| Franqueza | "O Summit não vai salvar a sua agência." (18/10) · "Não vamos te convencer mais." (07/11) |

**Limite de integridade:** a urgência só usa o que é verdade: as datas dos lotes e o preço que sobe. Com poucos
ingressos vendidos, escassez de lugares seria falsa e enfraqueceria a credibilidade; por isso o tamanho do evento
virou benefício (conversar com todos), não alerta. Não há contagem de vendas inventada ("restam X vagas"). Se você me passar o número real de ingressos vendidos,
posso usar como prova social.

Degraus de preço usados: Early Bird R$ 350 (até **02/10**, prorrogado) · Segundo lote R$ 450 (**03/10** a 24/10) ·
Terceiro lote R$ 550 (25/10 a 10/11) · no dia R$ 650 (sujeito à disponibilidade).

## Parceiros nas artes

Os logos ficam **dentro de um slide do carrossel**, grandes e na cor oficial, e não mais numa faixa sobre cada
arte. Assim as artes de mensagem ficam com o espaço todo. Todo post de feed virou carrossel: slide 1 é a mensagem
e o **último slide (ou o penúltimo, nos carrosséis longos) é "Quem faz o Summit acontecer com a gente"**, com os
três níveis do site: Patrocínio (Ollara, CLIDA, Ikon Institute of Australia + Australian Learning Group), Media
partner (The PIE) e Apoio (BELTA, ABRAPEI, IALC, Ally Hub, Edvisor).

O slide usa os logos oficiais sem recolorir, sobre fundo branco (respeita o manual de marca, seção 08). Os
parceiros já assinaram a autorização de co-branding.

Stories e reels mantêm a faixa compacta em branco, porque não perdem espaço de mensagem.

## Variedade de imagens

Rotação de 9 fotos de evento (painel, painel-plateia, plateia, plateia-2, networking, palco-telão,
troféus, premiados). A foto aparece com clareza na faixa superior de cada peça, onde só há o logo, e o
véu escuro protege a zona do texto. Fora de uso por risco: `palestra-plateia` (o @ da palestrante aparece
no slide), `palestrante-close` (slide com dado de terceiros) e `palestra-telao` (slide legível).

## Ritmo por fase

| Fase | Datas | Foco |
|---|---|---|
| 1 | 29/09 a 02/10 | Early Bird em venda reversa, **anúncio da prorrogação em 01/10**, último dia em 02/10, votação abre |
| 2 | 03/10 a 08/10 | Segundo lote (a partir de 03/10), IA entra |
| 3 | 09/10 a 24/10 | Uma categoria do Prêmio a cada 3 a 4 dias, palestrantes, painel, Segundo lote fecha |
| 4 | 25/10 a 31/10 | Terceiro lote, reta final e encerramento da votação |
| 5 | 01/11 a 11/11 | Contagem regressiva, onde é, programa, último dia do lote, "é hoje" |

Feed: 43 posts prontos (7 carrosséis); 06/10 é o dia do reel. Os 44 dias de 29/09 a 11/11 estão cobertos. Stories: 41 peças (versões dos posts diários, contagens e
enquetes). Reels prontos: Prêmio (01/10) e IA em perguntas (06/10), mais os 4 de setembro.
**Ainda não produzidos:** reels novos para outubro e novembro (sugestões: último dia do Segundo lote 23/10,
Prêmio última semana 27/10, último dia de votação 30/10, contagem final 09/11).

## Early Bird prorrogado até 02/10 (anúncio em 01/10)

| Data | Peça |
|---|---|
| 29/09 e 30/09 | "Não compre o Early Bird" e "Ainda é R$ 350": **sem data final**, só "depois do Early Bird, R$ 100 a mais" |
| 01/10 | Feed 12h e story 10h: "Early Bird prorrogado até 02/10" |
| 02/10 | Feed 9h e story 12h30: "Amanhã, R$ 100 a mais" (último dia, 23h59) |
| 03/10 | Story "Segundo lote" (R$ 450 até 24/10) |

**Não publicar** os dois P11 do pacote de setembro ("último dia" 29/09 e "termina hoje" 30/09): afirmam
prazo final que deixou de valer. Estão marcados como bloqueados no `AGENDAMENTO.md` de setembro.

**Dependência técnica.** O site troca de lote pela data e a função de checkout cobra pelo mesmo calendário.
As datas já estão editadas no repositório (`site/evento.config.js` e `supabase/functions/summit-checkout/index.ts`:
Early Bird até 02/10, Segundo lote a partir de 03/10), mas **nada foi publicado**. Para o preço não virar
R$ 450 à meia-noite de 30/09, o site e a função precisam estar atualizados antes disso. Se ficarem para
depois, quem comprar em 01/10 paga R$ 450 enquanto o post diz R$ 350.

**Artes antigas com "até 30/09"** (não regeneradas): panorama e demais posts fixados, capa do P7/P9, convites e
e-mails de parceiros, reels de abertura e prova social. Ficam desatualizadas a partir de 03/10.

## Precisa da sua decisão antes de publicar

1. **Votação: backend publicado, falta o site na `main`.** A migração e a função `summit-votar` já estão no Supabase da PATH
   (`ildxeq…`) desde 29/09, e a `summit-checkout` (v23) já cobra Early Bird até 02/10, com `EARLY10` até 02/10. Falta
   **fazer o merge do PR do site** (página `/votar`, rewrites) antes de 01/10 00:00. As artes de voto já apontam para
   `intercambiosummit.com.br/votar`. O teste com voto real só é possível depois da abertura (01/10).
2. **Regras do Prêmio: fechadas em 30/09.** Voto cruzado também na Etapa 3; nome oficial **Prêmio dos Melhores Profissionais de
   Intercâmbio 2026**; 6 finalistas em Acelerador de Resultados e Espírito Inovador (o Regulamento previa 5). Por categoria são 6 votos:
   o público inteiro vale 1 (finalista mais votado) e cada um dos 5 avaliadores do comitê vale 1. Empate no topo: vence o escolhido
   pelo público. Empate no público: o comitê decide. Empate sem o escolhido do público entre os empatados: prevalece o voto da
   organização. Corte: 30/10 às 23:59:59 (Brasília). O Regulamento não diz isso; a minuta de adendo está em
   `regulamento/ADENDO-ETAPA-3.md`. **Publicar o carrossel de 06/10 junto com o adendo** (ou antes).
3. **Venda no dia.** Os posts de 09/11 a 11/11 dizem "R$ 650, sujeito à disponibilidade". Confirme se haverá
   venda no dia e como.
4. **Horários.** A premiação às 16h30 vem do site. Se a votação tiver hora de corte no dia 30/10, me diga.
5. **Peças de setembro já feitas** (P1 a P11, pinados, kit, convites) ficam como estão, com a faixa antiga (só de Apoio) e o
   nome antigo do prêmio (decisão do Rodrigo em 30/09: só as artes de 30/09 em diante usam o nome oficial e a faixa nova).
6. **Ally Hub.** O press release do Drive cita "Apply Hub"; as artes usam Ally Hub.
7. **Conteúdo de IA.** As "3 frentes" descrevem o tema anunciado de forma geral. Nenhuma estatística
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
