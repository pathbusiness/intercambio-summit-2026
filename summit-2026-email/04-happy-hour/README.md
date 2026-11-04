# Campanha 04: RSVP do happy hour pós-Summit (Eu, Tu, Eles)

## Configuração
- **Nome no Zoho:** Summit 2026 | C04 Happy Hour | E01 Participantes / E02 Palestrantes
- **Listas:** E01 = inscritos/compradores do Summit 2026 (Zoho Backstage) MENOS palestrantes; E02 = palestrantes e painelistas. Quem estiver nas duas listas recebe só o E02.
- **Remetente:** Rodrigo Collaro, rodrigo@yourpath.com.br
- **Merge tag de primeiro nome:** `$[FNAME|você]$` | **Descadastro:** `$[LI:UNSUBSCRIBE]$`
- **Envios sugeridos (Brasília):** E02 palestrantes 04/11 (qua) 15h | E01 participantes 05/11 (qui) 10h
- **UTM:** utm_campaign=happyhour, utm_content=participantes / palestrantes
- Rodapé igual ao da campanha 02 (patrocínio, media partner, apoio).

## Como a resposta chega até você
Cada e-mail tem dois botões, **Eu vou** e **Não vou**, que abrem `intercambiosummit.com.br/happyhour` com a resposta já marcada. A pessoa informa nome e e-mail e envia (dois cliques). O link não leva dado pessoal. Responder de novo com o mesmo e-mail atualiza a resposta (vale a última).

As respostas ficam na tabela **`summit_happyhour_rsvp`** (Supabase PATH, projeto `ildxeqtmpbartonjoiwc`): nome, e-mail, empresa, resposta (`sim`/`nao`), perfil (`participante`/`palestrante`) e data/hora.

- **Ver:** Dashboard → Table Editor → `summit_happyhour_rsvp` (exporta CSV).
- **Contagem rápida:** `select * from public.summit_happyhour_resumo;`
- **Lista de confirmados:** `select nome, empresa, email, perfil from public.summit_happyhour_rsvp where resposta = 'sim' order by nome;`
- **Quem não respondeu** (para um lembrete): exporte a tabela e exclua esses e-mails da lista do Zoho antes do reenvio.

## Para entrar no ar (nada disso foi publicado ainda)
1. Supabase → SQL Editor: rodar `supabase/migrations/20261103000000_happyhour_rsvp.sql`.
2. Publicar a função: `supabase functions deploy summit-happyhour --no-verify-jwt` (ou colar `supabase/functions/summit-happyhour/index.ts` em Edge Functions, com *Verify JWT* desligado).
3. Publicar o site (commit e deploy na Vercel) com `site/happyhour.html`, `site/js/happyhour.js`, o bloco `happyhour` em `site/evento.config.js` e os rewrites `/happyhour` e `/api/happyhour` em `site/vercel.json`.
4. Teste ponta a ponta antes do envio: abrir a página, responder com `teste@teste.local` e apagar: `delete from public.summit_happyhour_rsvp where email like '%@teste.local';`

## Confirmar antes de enviar
1. **Horário (confirmado):** a partir das 19h.
2. **Quem paga (confirmado):** cada um paga o próprio consumo; os e-mails e a página dizem isso.
3. **Reserva e capacidade:** os e-mails não citam número de vagas. Se o bar tem limite, a contagem de "sim" mostra o tamanho do grupo antes de fechar a reserva.
4. **Nome do local do Summit:** os e-mails dizem "250 metros do local do Summit" e não citam o prédio, como nas campanhas anteriores.
5. **Palestrantes sem e-mail no Zoho:** a lista de palestrantes precisa ser montada à parte (não está no repositório).

## Textos
- **E01 Participantes** assunto: Depois do Summit, um happy hour. Você vai? | preheader: Quarta, 11/11, no Eu, Tu, Eles, a 250 metros do evento. Confirme em um clique. | CTAs: Eu vou / Não vou
- **E02 Palestrantes** assunto: Você é do programa. Fique para o happy hour. | preheader: igual ao E01 | CTAs: Eu vou / Não vou (link com `p=palestrante`)

Corpo: ver `email-01-participantes.html` e `email-02-palestrantes.html`.
