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

## Produção após aprovação (seção 8 do briefing)

- Setembro P1–P11: cada peça é um template novo sobre `base.css`
  (P4 = Modelo B; P9/P9b usam `palestrantes/myrko-micali-800.webp`).
- Prêmio: 32 cards = Modelo C via `data/finalistas.json`; cards de votação
  (sem faixa de apoiadores, selo VOTE, prazo 30/10) e stories (1080x1920,
  400px inferiores livres para o sticker) = variantes do mesmo template.
  Entrega: uma pasta `NomeSobrenome/` por finalista com os 4 arquivos +
  texto sugerido em `.txt` (o `render.py` ganhará o job `premio`).
- Kit co-branded: logo do apoiador no topo ao lado do Summit, sem faixa no
  rodapé; feed + story + banner 600x200.
