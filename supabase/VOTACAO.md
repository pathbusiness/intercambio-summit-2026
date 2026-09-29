# Votação do Prêmio Melhores Profissionais 2026

Regras (Regulamento Oficial, etapa 3): votação pública **entre os finalistas**, de **01/10 a 30/10/2026**,
um voto por categoria por pessoa, votos duplicados ou suspeitos podem ser invalidados (seção 9).
Vencedores anunciados em 11/11.

Decisões de projeto (Rodrigo, 29/09): cadastro simples (nome, e-mail e empresa, sem confirmação por
e-mail) e **voto cruzado**: quem é de agência vota nas categorias de instituições e vice-versa.

## Peças

| Peça | Arquivo |
|---|---|
| Página de votação (`/votar`) | `site/votacao.html`, `site/js/votacao.js`, estilos em `site/css/styles.css` |
| Endpoint (`/api/votar`) | `supabase/functions/summit-votar/` (`index.ts` + `validar.ts`) |
| Tabela e ranking | `supabase/migrations/20261001000000_votacao.sql` |
| Dados dos finalistas | `tools/build_votacao_data.py` gera `site/data/votacao.json` e `finalistas.ts` |
| Datas e endpoint no site | bloco `votacao` em `site/evento.config.js` |
| Rewrites | `site/vercel.json` (`/votar`, `/api/votar`) |

## O que a votação garante

- Janela de datas conferida no servidor (horário de Brasília; fim em 30/10 às 23:59:59).
- Elegibilidade por trilha conferida no servidor; finalista tem que pertencer à categoria.
- Um voto por categoria por e-mail (índice único). E-mail normalizado: Gmail sem pontos e sem `+tag`,
  domínios de e-mail descartável bloqueados. Quem já votou não é sobrescrito: vale o primeiro voto.
- Limite de 25 e-mails distintos por IP por hora (escritórios compartilham IP; só barra automação).
- Honeypot, allowlist de origem, sem leitura pública da tabela (RLS ligada, sem políticas).
- Trilha de auditoria: e-mail original, hash do IP (com sal), user agent e horário de cada voto.

**Limite conhecido:** sem confirmação por e-mail, qualquer pessoa pode votar com um e-mail que não é dela.
A defesa é a auditoria depois da votação (regulamento permite invalidar). Se quiser subir a barreira, o
próximo passo é código de confirmação por e-mail ou links únicos por eleitor.

## Aplicar em produção (ordem)

1. Migração: `supabase/migrations/20261001000000_votacao.sql` (SQL editor ou `supabase db push`).
2. Deploy da função `summit-votar` (`supabase functions deploy summit-votar`). Variáveis opcionais:
   `VOTACAO_SALT` (sal do hash de IP), `VOTACAO_INICIO` e `VOTACAO_FIM` (só para testes).
3. Publicar o site (merge na `main`): página `/votar`, rewrites, botão na seção do Prêmio.
4. Teste ponta a ponta antes de 01/10 00:00 com `VOTACAO_INICIO` no passado, depois **apagar os votos de teste**:
   `delete from public.votacao_votos where email like '%@teste.local';`

## Acompanhar e auditar (SQL editor, só organização)

```sql
-- ranking parcial
select categoria, finalista, votos from public.votacao_ranking order by categoria, votos desc;

-- votos por dia
select date_trunc('day', created_at at time zone 'America/Sao_Paulo') dia, count(*) from public.votacao_votos group by 1 order by 1;

-- suspeitos: muitos e-mails no mesmo IP
select ip_hash, count(distinct email) emails, count(*) votos from public.votacao_votos group by 1 having count(distinct email) >= 5 order by 2 desc;

-- invalidar (regulamento, seção 9) sem apagar
update public.votacao_votos set status = 'invalidado', motivo = 'voto duplicado/fraudulento' where email = 'fulano@x.com';
```

## Dossiês nos criativos

`criativos/data/dossies-resumos.json` (não versionado até existir), um item por finalista:

```json
{ "slug-do-finalista": { "empresa": "", "cargo": "", "resumo": "até 240 caracteres", "aprovado": true } }
```

Só entra quem tem `"aprovado": true` (autorização do finalista). Depois:

```
python3 tools/build_votacao_data.py           # o resumo aparece na página /votar ("Ver destaque do dossiê")
python3 criativos/render.py dossies           # gera card-dossie.jpg de cada aprovado
python3 criativos/build_campanha_outubro.py   # os carrosséis de categoria usam o card com dossiê
```

O guia do dossiê promete uso "exclusivamente para fins da premiação". Por isso só o que o finalista aprovar
por escrito, no mesmo formato para todos, sem dado financeiro nem depoimento de terceiros.
