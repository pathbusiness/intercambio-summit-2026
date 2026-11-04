# Campanha 03: finalistas do Prêmio Melhores Profissionais de Intercâmbio 2026 que ainda não compraram

## Configuração
- **Nome no Zoho:** Summit 2026 | C03 Finalistas | E01 / E02 / E03
- **Segmento:** [32 finalistas MENOS inscritos e compradores do Summit 2026; e-mails dos finalistas a confirmar]
- **Remetente:** Rodrigo Collaro, rodrigo@yourpath.com.br
- **Envios (Brasília):** E01 04/11 (qua) 9h | E02 07/11 (sáb) 10h | E03 10/11 (ter) 9h
- **UTM:** utm_campaign=finalistas, utm_content=email01/02/03
- **Formato:** HTML quase de e-mail escrito à mão (sem banner, sem logos), para parecer pessoal.

## Campo personalizado de categoria ($[CATEGORIA]$)
Criar no Zoho Campaigns antes do envio:
1. Contatos > Todos os contatos > ícone de configurações da tabela (ou Configurações > Campos de contato) > **Campos personalizados** > **Adicionar campo**.
2. Nome do campo: `CATEGORIA` | Tipo: **Texto de uma linha**.
3. Preencher para os 32 finalistas (importar CSV com e-mail + CATEGORIA, ou editar contato a contato) com o nome da categoria, por exemplo "Espírito Inovador (trilha Agências)".
4. Nos e-mails, a tag é `$[CATEGORIA|Melhores Profissionais]$` (o texto após a barra é o fallback se o campo estiver vazio). Conferir no dropdown "Tags de mesclagem".
5. Categorias (finalistas.json): Conector(a) do Ano, Iniciativa do Ano, Mente Inovadora (trilha Instituições); Transformador(a) de Vidas, Acelerador(a) de Resultados, Espírito Inovador (trilha Agências).

## Riscos ou inconsistências (confirmar antes de enviar)
1. **Categorias:** o briefing diz 7 categorias; criativos/data/finalistas.json tem 6 categorias e 32 finalistas.
2. **E-mails dos finalistas:** não constam no repositório; precisam estar no Zoho com o campo CATEGORIA preenchido.
3. **[CONDIÇÃO_FINALISTA]:** não há condição especial conhecida; o parágrafo foi omitido.
4. **[HORÁRIO_PREMIAÇÃO]:** 16h30 (programação do site).
5. **Texto "independentemente do resultado":** mantido conforme o briefing; sem sugerir que a presença afeta o prêmio ("é um convite, não uma exigência").
6. **Vagas:** sem número de lugares restantes.
7. **Preço:** Terceiro lote R$ 550 (5x R$ 110) até 10/11; dia do evento R$ 650.
8. **Sobreposição:** finalistas que também estão nas campanhas 01 ou 02 receberiam mais de uma sequência; excluí-los dessas.
9. **Exemplos do E02:** vêm das descrições das sessões no site.

## Textos
- **E01 (04/11 9h)** assunto: Você é finalista. O palco é seu. | preheader: A entrega do Prêmio Melhores Profissionais é no Summit, dia 11/11. | CTA: Garantir minha vaga
- **E02 (07/11 10h)** assunto: O que uma referência leva do Summit para 2027 | preheader: IA aplicada ao seu trabalho em 2027: três exemplos das sessões. | CTA: Comprar meu ingresso
- **E03 (10/11 9h)** assunto: Amanhã, seu nome no palco | preheader: Cerimônia às 16h30, Av. Paulista. Último dia do Terceiro lote. | CTA: Comprar agora
