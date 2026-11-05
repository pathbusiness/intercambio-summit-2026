# Avaliação por palestra — Intercâmbio Summit 2026

Vídeos de telão (2304×576) com QR Code para avaliação rápida de **cada palestra**, para rodar logo após cada apresentação. Um vídeo e um QR por palestra; todas as respostas caem numa tabela só, identificadas pela coluna `palestra`.

## Formulário
- **URL base:** https://summit-palestras-2026-path-ce69.vercel.app/?p=`<slug>`
- Um formulário só, que mostra a palestra conforme o parâmetro `?p=` do QR.
- Fonte: `criativos/pesquisa/palestras.html` · Hospedagem: Vercel (projeto `summit-palestras-2026`, Deployment Protection desligado).

## Palestras (slug → vídeo/QR)
| slug | palestra | vídeo | QR |
|---|---|---|---|
| `raphael-cavaco` | Raphael Cavaco — Mídias sociais e IA | palestra-raphael-cavaco | qr-raphael-cavaco |
| `myrko-micali` | Myrko Micali — IA para atendimento, mkt e vendas | palestra-myrko-micali | qr-myrko-micali |
| `lucas-politi-wagner` | Lucas Politi Wagner — Google, IA e gestão criativa | palestra-lucas-politi-wagner | qr-lucas-politi-wagner |
| `gizelle-rezende` | Gizelle Rezende — Tendências globais | palestra-gizelle-rezende | qr-gizelle-rezende |
| `painel` | Painel — Panorama 2027 e uso da IA | palestra-painel | qr-painel |

## Backend (Supabase)
- Projeto **Forio** (`lvchpskxeohfmistppxl`), tabela `public.summit2026_palestras` (RLS só `INSERT` anônimo).
- Campos: `palestra` (slug), `nota` (1–5), `aplicar` (1–5), `didatica` (1–5), `comentario` (texto).

### SQL — médias por palestra
```sql
select palestra,
       count(*) respostas,
       round(avg(nota),2) nota,
       round(avg(aplicar),2) aplicabilidade,
       round(avg(didatica),2) didatica
from summit2026_palestras
group by palestra
order by nota desc;

-- comentários de uma palestra
select comentario from summit2026_palestras
where palestra = 'raphael-cavaco' and comentario is not null
order by created_at desc;
```

## Template
`palestra.html` — self-contained, seleciona a palestra pelo hash (`#<slug>`); fundo animado (rede de partículas). Para regerar um vídeo, renderizar `palestra.html#<slug>`.
