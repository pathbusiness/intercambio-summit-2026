# Criativos — Intercâmbio Summit 2026

Sistema visual da campanha de divulgação (briefing de set/2026). Templates
HTML **editáveis** + renderizador headless: é assim que os 130+ criativos
saem consistentes — editar dado, rodar script, sair PNG no pixel exato.

## Primeira entrega (aprovação)

`criativos/aprovacao/` contém as três peças-modelo do briefing:

| Arquivo | Modelo |
|---|---|
| `modelo-a-institucional.png` | A — institucional, foto de plateia tratada |
| `modelo-b-tabela-precos.png` | B — escada de lotes, sem foto |
| `modelo-c-finalista-vitor-cruz.png` | C — caso foto de estúdio (expressão séria) |
| `modelo-c-finalista-anderson-bertin.png` | C — caso foto de celular em fundo branco |
| `modelo-c-finalista-guilherme-garcia.png` | C — caso recorte manual (pior caso) |

## Como renderizar

```bash
pip install playwright pillow numpy   # Chromium: playwright install chromium
python3 criativos/render.py aprovacao
# peça avulsa:
python3 criativos/render.py modelo-c-finalista.html \
  NOME="Vivi Lac" CATEGORIA="Espírito Inovador" TRILHA="Agências" \
  FOTO="../../site/assets/img/finalistas/vivi-lac-800.webp" out=/tmp/teste.png
```

Tamanhos: feed/carrossel 1080x1350 · story 1080x1920 · LinkedIn 1200x627
(`size=story` etc. no comando).

## Estrutura

- `templates/base.css` — tokens da marca (Brand Guidelines v1.0) + regras do
  briefing: 120px inferiores livres, mensagem entre 30–55% da altura,
  faixa de apoiadores, CTA verde (uso exclusivo do Action Green).
- `templates/modelo-*.html` — um template por família de peça; placeholders
  `{{CHAVE}}` substituídos pelo `render.py`.
- Fundos sem foto são lisos (Summit Blue / Deep Navy) com o **dispositivo
  angular 45°** do manual (seção 06): triângulos nos cantos, sempre em
  Summit Blue ou branco, nunca sobre conteúdo, máx. 2 por peça
  (`.canto-45` e `.plano-45` no `base.css`). Decisão de 01/09: sem
  textura/mosaico de fundo.
- `assets/marca/apoio-*-branco.png` — logos dos apoiadores em mono branco,
  equalizados por peso óptico (gerar de novo: `tools/build_criativos_marca.py`).
- `assets/marca/summit-logo-branco.png` — logo do Summit todo branco com
  fundo transparente, para uso sobre as fotos tratadas (pedido do Rodrigo,
  01/09; o manual prevê o mapa pontilhado só em Map Grey na versão para
  fundo preto — desvio consciente do brand owner).
- `assets/fonts/` — Rajdhani (OFL) local, para render determinístico.
- `data/finalistas.json` — os 32 finalistas x 6 categorias (fonte: site).

## Decisões que dependem de aprovação

1. **Lockup do Prêmio**: não existe arquivo de logo do "Prêmio Melhores
   Profissionais"; o card usa lockup tipográfico em Rajdhani. Se houver
   logo oficial, substituir no `modelo-c-finalista.html`.
2. **Headline do Modelo B** ("O preço sobe. O evento é o mesmo.") é
   proposta de copy — o briefing fixava apenas o fechamento.
3. **Faixa de apoiadores em mono branco** sobre azul: pedido do briefing,
   mas o Brand Guidelines (seção 08) proíbe recolorir/alterar logos de
   parceiros e exige confirmação POR ESCRITO de cada um antes de publicar
   material co-brandado. Publicar só com esse aceite (ou trocar a faixa
   pelos logos coloridos sobre régua branca, que é o formato do manual).
4. **Guilherme Garcia** (pior caso): halo de recorte visível no contorno —
   o refino de borda precisa dos ORIGINAIS das fotos, que não estão neste
   repositório (ver `tools/build_images.py`, caminhos locais do Rodrigo).

## Produção (aprovada em 01/09) — `criativos/out/`

- `out/setembro/` — P1 a P11 (26 arquivos: inclui carrossel P7 de 5 cards,
  P9 em 2 versões, carrossel P9b de 9 cards e P11 em 2 versões de data).
- `out/premio/capas/` — 6 capas de categoria.
- `out/premio/finalistas/NomeSobrenome/` — por finalista: card-finalista,
  card-votacao (sem faixa, selo VOTE), story-votacao (400px inferiores
  livres p/ sticker, sem URL escrita), story-faltam-N-dias e
  texto-sugerido.txt. Regerar contagem: `render.py premio DIAS=3`.
- `out/kit-apoiadores/<id>/` — feed 1080x1350, story 1080x1920 e banner
  de e-mail 600x200 por apoiador (logo no topo, sem faixa no rodapé).

Volume em JPEG q92; banner de e-mail em PNG. Regerar tudo:
`python3 criativos/render.py tudo`.

### Pendências para publicar
1. **Link curto de votação**: os cards usam `intercambiosummit.com.br`
   (constante `URL_VOTACAO` no `render.py`). Confirmar o endereço final e
   regerar (`render.py premio`).
2. **Temas do carrossel P7**: hoje são os 3 confirmados no site
   (`data/sessoes.json`); acrescentar os demais quando fecharem.
3. **Kit**: para Ally Hub e Edvisor o texto diz "Clientes da", não
   "Associados da" (são empresas) — validar redação com os parceiros,
   junto com o aceite por escrito do co-branding (manual, seção 08).
4. **Direito de imagem**: os fundos usam fotos de 2025 com pessoas
   identificáveis (`plateia`, `painel`, `networking`) — pendência já
   registrada no README do site vale para estas peças.
