# Limpeza do Forio: remover tudo do Intercâmbio Summit

Projeto **Forio** (conta EXP TOUR, ref `lvchpskxeohfmistppxl`). O Summit roda no projeto da PATH
(`ildxeqtmpbartonjoiwc`) desde 23/09; nada do Summit deve ficar no Forio.

## O que existe no Forio (inventário de 29/09)

| Tipo | Nome | Origem | Observação |
|---|---|---|---|
| Tabela | `public.summit_leads` | antes da migração | 1 linha em 29/09 |
| Tabela | `public.summit_orders` | antes da migração | 0 linhas |
| Tabela | `public.votacao_votos` | criada por engano em 29/09 | 0 linhas |
| View | `public.votacao_ranking` | criada por engano em 29/09 | |
| Função | `summit-leads` | antes da migração | |
| Função | `summit-checkout` | antes da migração (v1) + correção de datas em 29/09 (v2) | |
| Função | `summit-mp-webhook` | antes da migração | |
| Função | `summit-votar` | criada por engano em 29/09 | |
| Migração | `votacao_premio_2026` | registrada em `supabase_migrations.schema_migrations` | |
| Segredo | `MP_ACCESS_TOKEN` (e outros do Summit, se houver) | antes da migração | token do Mercado Pago; ver abaixo |

## Passo a passo

**1. Conferir os dados antes de apagar.** No SQL Editor do Forio:

```sql
select count(*) from public.summit_leads;    -- 1 em 29/09: confirme se esse e-mail já está no projeto da PATH
select count(*) from public.summit_orders;   -- 0
select count(*) from public.votacao_votos;   -- 0
```

Se `summit_leads` ou `summit_orders` tiverem dados que não estão na PATH, exporte em CSV antes (botão de download no resultado).

**2. Apagar tabelas, view e registro de migração:**

```sql
begin;
drop view  if exists public.votacao_ranking;
drop table if exists public.votacao_votos;
drop table if exists public.summit_orders;
drop table if exists public.summit_leads;
delete from supabase_migrations.schema_migrations where name = 'votacao_premio_2026';
commit;
```

**3. Apagar as 4 funções** (painel: Edge Functions → função → Delete; ou CLI logada na conta EXP TOUR):

```
supabase functions delete summit-leads      --project-ref lvchpskxeohfmistppxl
supabase functions delete summit-checkout   --project-ref lvchpskxeohfmistppxl
supabase functions delete summit-mp-webhook --project-ref lvchpskxeohfmistppxl
supabase functions delete summit-votar      --project-ref lvchpskxeohfmistppxl
```

**4. Segredos.** `supabase secrets list --project-ref lvchpskxeohfmistppxl`. Se `MP_ACCESS_TOKEN` estiver lá e nenhuma
outra função do Forio usar, remover com `supabase secrets unset MP_ACCESS_TOKEN --project-ref lvchpskxeohfmistppxl`.
É o token de produção do Mercado Pago da PATH; não deve ficar em projeto que não é do Summit.

**5. Conferir que não sobrou nada:**

```sql
select c.relname from pg_class c join pg_namespace n on n.oid = c.relnamespace
where n.nspname = 'public' and (c.relname ilike '%summit%' or c.relname ilike '%votacao%');   -- deve vir vazio
select name from supabase_migrations.schema_migrations where name ilike '%summit%' or name ilike '%votacao%';   -- deve vir vazio
```

E no painel, Edge Functions do Forio: nenhuma função `summit-*`.

## Antes de apagar `summit-mp-webhook`

Confirme no Mercado Pago (conta PATH) que nenhuma preferência ou pedido antigo ainda usa a URL de notificação do Forio
(`https://lvchpskxeohfmistppxl.supabase.co/functions/v1/summit-mp-webhook`). O checkout atual usa o webhook do projeto da PATH.
Como `summit_orders` do Forio tem 0 linhas, não há pedido a perder.
