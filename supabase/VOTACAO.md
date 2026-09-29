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
- Teto de 300 e-mails distintos por IP por hora (atrás do proxy da Vercel o IP pode ser compartilhado; só barra automação pesada, o resto se vê na auditoria por ip_hash).
- Honeypot, allowlist de origem, sem leitura pública da tabela (RLS ligada, sem políticas).
- Trilha de auditoria: e-mail original, hash do IP (com sal), user agent e horário de cada voto.

**Limite conhecido:** sem confirmação por e-mail, qualquer pessoa pode votar com um e-mail que não é dela.
A defesa é a auditoria depois da votação (regulamento permite invalidar). Se quiser subir a barreira, o
próximo passo é código de confirmação por e-mail ou links únicos por eleitor.

## Onde ficam os votos

**Supabase da PATH** (projeto "PATH BUS MKT", ref `ildxeqtmpbartonjoiwc`), tabela **`public.votacao_votos`**: o mesmo
projeto que o site já usa desde 23/09 para leads e checkout (commit `978e96c`). O projeto antigo (Forio, conta EXP TOUR)
não é mais usado pelo site.

- Ver: Table Editor do projeto → `votacao_votos`. Consultar/exportar: SQL Editor (consultas abaixo; o resultado baixa em CSV).
- Cada linha: categoria, finalista (slug), nome, e-mail (normalizado e original), empresa, tipo (agência ou instituição),
  hash do IP, navegador, data/hora, `status` (`valido` ou `invalidado`) e `motivo`.
- O site nunca lê a tabela; só a função `summit-votar` escreve (service role). Anon e authenticated não têm acesso.

## Estado em produção (atualizado em 29/09)

| Item | Situação |
|---|---|
| Projeto PATH (`ildxeq…`): migração `20261001000000_votacao.sql` | **PENDENTE** (não aplicada; ação em produção bloqueada pelo controle de permissões da sessão) |
| Projeto PATH: função `summit-votar` | **PENDENTE** |
| Projeto PATH: função `summit-checkout` com Early Bird até 02/10 | **Publicada em 29/09 (v22)**: só as datas mudaram sobre a v21 (Early Bird até 02/10, Segundo lote de 03/10). **Não foi possível reler a v22 para conferir**: conferir no painel (Edge Functions → summit-checkout → versões, comparar v21 e v22). |
| Site (página `/votar`, rewrites, botão no Prêmio, convite pós-voto) | Neste PR |
| Projeto antigo Forio (`lvchp…`) | Recebeu por engano, em 29/09, a migração, a `summit-votar` e uma correção de datas na `summit-checkout` (v2). Não é usado pelo site. Tabela vazia. Pode ser limpo. |

**Cupom a decidir:** `EARLY10` (10% no Early Bird) vale só até 01/10 em `PROMO_CODES`; com o Early Bird até 02/10, decidir se estende.

### Como aplicar no projeto da PATH

Com a CLI do Supabase logada na conta da PATH:

```
supabase link --project-ref ildxeqtmpbartonjoiwc
supabase db push                                     # ou colar supabase/migrations/20261001000000_votacao.sql no SQL Editor
supabase functions deploy summit-votar --no-verify-jwt
supabase functions deploy summit-checkout --no-verify-jwt   # traz Early Bird até 02/10 e Segundo lote a partir de 03/10
```

Variáveis opcionais da votação: `VOTACAO_SALT` (sal do hash de IP), `VOTACAO_INICIO` e `VOTACAO_FIM` (só para testes).
O código de `summit-checkout` do repositório já tem as datas novas.

Teste ponta a ponta depois de publicar o site: votar uma vez com e-mail `@teste.local` (só a partir de 01/10 00:00; antes
disso a função recusa) e apagar: `delete from public.votacao_votos where email like '%@teste.local';`

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
