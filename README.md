# Site Intercâmbio Summit 2026

Página estática, sem framework. GSAP + ScrollTrigger + Lenis vendorizados em `js/vendor/`.

## Como editar preço, lote, data e links

Tudo em **`evento.config.js`**. O site escolhe o lote vigente pela data do
visitante e atualiza sozinho o selo do topo, os cards de ingresso e o texto do
formulário. Trocar de lote = não fazer nada. Trocar preço/prazo = editar o
array `lotes` e fazer deploy.

Campos já configurados em `evento.config.js`:

- `checkoutUrl` — Zoho Backstage (ingressos).
- `leadFormAction` — Supabase Edge Function `summit-leads` (projeto Forio);
  grava na tabela `summit_leads`. Exportar leads: SQL
  `select email, created_at from summit_leads order by created_at`.
- `patrocinioUrl` — página de patrocínio no GitHub Pages.
- `palestrantes` — 4 confirmados; para os demais, foto 800x800 WebP em
  `assets/img/palestrantes/{slug}-800.webp` e marcar `foto: true`.

## Deploy

GitHub Pages, repositório `pathbusiness/intercambio-summit-2026`.
Push no `main` → GitHub Actions publica `site/` no branch `gh-pages` →
Pages serve em https://pathbusiness.github.io/intercambio-summit-2026/.
Fonte do Pages nas Settings: branch `gh-pages`, pasta root.

## Rodar localmente

```bash
python3 -m http.server 8741 --directory site
```

## Pipeline de imagens (pasta `tools/` na raiz do projeto)

- `tools/build_images.py` — gera tudo a partir dos originais na raiz:
  - `eventos` — 9 fotos de 2025 em WebP 900/1600/2400
  - `finalistas` — recorte de fundo (rembg, cache em `tools/cutouts/`),
    assentamento sobre Summit Blue `#0044B9`, corte quadrado com rosto
    detectado (YuNet, olhos na linha do terço), tratamento unificado,
    WebP 400/800. Rodar com `SUMMIT_BG=blue python3 tools/build_images.py finalistas`
  - `paulista` — corte de 9% do topo (remove a marca Citi) + variantes
- `tools/make_worldmap.py` — regenera `assets/svg/world-dots.svg`
  (mapa-múndi pontilhado, ativo de marca)

Dependências Python: `pillow`, `opencv-python-headless`, `numpy`, `rembg`,
`onnxruntime` (instaladas com `pip install --user`).

## Identidade (Brand Guidelines v1.0, abr/2026 — manda sobre o plano v2)

- **Paleta oficial**: Summit Blue `#0044B9` (títulos, estrutura, fundo das
  fotos dos finalistas), Charcoal `#231F20` (texto, nunca `#000`), Action
  Green `#0ACE00` (EXCLUSIVO para CTAs, nunca texto pequeno), Deep Navy
  `#00235C`, neutros Cloud `#F4F6FB` / Mid `#D0D5E8` / Text Grey `#6B7280`.
- **Tipografia**: Rajdhani, única família (Google Fonts), fallback
  Arial/Helvetica Neue. Títulos em caixa alta, nunca só minúsculas.
- **Logo**: `assets/img/marca/summit-logo-*` recortados dos PNGs oficiais.
  Reverso sobre Summit Blue no cabeçalho e rodapé (o azul exato do arquivo é
  `#0044BA`, usado como fundo para assentar sem emenda). Fundos aprovados:
  branco, preto, Summit Blue.
- **Mapa pontilhado só dentro do logotipo** — o manual proíbe extraí-lo como
  textura. O `world-dots.svg` antigo foi removido dos assets (o gerador
  `tools/make_worldmap.py` fica arquivado, não usar).
- **Dispositivo angular 45°**: cantos apenas, máx. 2 por layout (hero e
  ingressos).
- **Apoio (Tier 2)**: BELTA, ABRAPEI, IALC, ALLY, Edvisor em faixa horizontal
  única, tamanhos equivalentes, separados por filetes, sobre branco —
  arquivos oficiais em `assets/img/marca/apoio-*.png`, sem recolorir.
  O manual pede confirmação por escrito de cada parceiro antes de publicar
  material co-brandado.
- Fotos de 2025 sempre rotuladas "Intercâmbio Summit 2025".
- Teaser vertical NÃO entra no site. A abertura usa sequência de 3 fotos com
  Ken Burns + crossfade por rolagem, com fallback estático para mobile e
  `prefers-reduced-motion`.

## Pendências de conteúdo antes de publicar

1. Confirmar nomes públicos: **Vivi Lac** (arquivo anterior dizia Vivian
   Castro) e **Hanna Alves** (arquivo diz Hannah). O site usa "Vivi Lac" e
   "Hanna Alves".
2. Confirmar direito de uso de imagem das fotos com rostos identificáveis
   (`plateia`/4-16 e `premiados`/7-105) em site e mídia paga.
3. Retratos dos 8 palestrantes 2026.
4. Foto real do Contentix para o bloco de local (hoje usa a aérea da Paulista).
5. Definir plataforma de checkout e endpoint de captura de e-mail.
