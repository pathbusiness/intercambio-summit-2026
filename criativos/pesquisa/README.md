# Pesquisa de avaliação — Intercâmbio Summit 2026

Formulário de avaliação do evento (anônimo, mobile-first) para os participantes responderem no celular via QR Code durante o encerramento.

## Links
- **Formulário (URL pública):** https://summit-avaliacao-2026-path-ce69.vercel.app
- **QR Code:** `criativos/telao/fechamento/qr-avaliacao.png` (entra no vídeo `fechamento-pesquisa-qr`)

## Hospedagem
- **Vercel** — projeto `summit-avaliacao-2026` (conta pathbusiness). Deploy estático (um `index.html`). Deployment Protection desligado para acesso público.
- Para republicar após editar `index.html`: novo deploy do projeto no Vercel (produção).

## Backend (Supabase)
- Projeto **Forio** (`lvchpskxeohfmistppxl`), tabela `public.summit2026_respostas`.
- **RLS:** apenas `INSERT` para `anon`/`authenticated` (ninguém lê pelo cliente). Leitura só via service role / painel Supabase.
- A chave embutida no formulário é a **publishable key** (segura para uso no cliente).

### Campos
| coluna | tipo | o que é |
|---|---|---|
| `nps` | 0–10 | recomendação (NPS) |
| `geral` | 1–5 | satisfação geral |
| `expectativas` | texto | Ficou abaixo / Atendeu / Superou |
| `conteudo` | 1–5 | conteúdo e palestras |
| `organizacao` | 1–5 | organização, estrutura e local |
| `networking` | 1–5 | networking |
| `divulgacao` | 1–5 | divulgação e comunicação |
| `proxima` | texto | intenção de voltar |
| `leva` | texto | aberto: "o que você leva" (depoimento) |
| `melhorar` | texto | aberto: "o que melhorar" |

## Como ler os resultados (exemplos SQL)
```sql
-- NPS: % promotores (9-10) menos % detratores (0-6)
select round(
  100.0 * (count(*) filter (where nps>=9) - count(*) filter (where nps<=6)) / nullif(count(nps),0)
) as nps
from summit2026_respostas;

-- médias por dimensão
select round(avg(geral),2) geral, round(avg(conteudo),2) conteudo,
       round(avg(organizacao),2) organizacao, round(avg(networking),2) networking,
       round(avg(divulgacao),2) divulgacao
from summit2026_respostas;

-- depoimentos
select leva from summit2026_respostas where leva is not null order by created_at desc;
```
