-- Votação pública do Prêmio Melhores Profissionais 2026 (etapa 3: 01/10 a 30/10).
-- Um voto por pessoa (e-mail normalizado) por categoria. Acesso só pela Edge Function
-- "summit-votar" (service role): RLS ligada e sem políticas, nada exposto ao anon.
create table if not exists public.votacao_votos (
  id           uuid primary key default gen_random_uuid(),
  created_at   timestamptz not null default now(),
  categoria    text not null,
  finalista    text not null,
  nome         text not null,
  email        text not null,             -- normalizado (minúsculas; gmail sem pontos/+tag)
  email_orig   text not null,             -- como a pessoa digitou (auditoria)
  empresa      text not null,
  tipo_empresa text not null check (tipo_empresa in ('agencia', 'instituicao')),
  ip_hash      text,
  user_agent   text,
  status       text not null default 'valido' check (status in ('valido', 'invalidado')),
  motivo       text                        -- preenchido ao invalidar (regulamento, seção 9)
);

create unique index if not exists votacao_um_voto_por_categoria
  on public.votacao_votos (email, categoria);
create index if not exists votacao_ranking_idx
  on public.votacao_votos (categoria, finalista) where status = 'valido';
create index if not exists votacao_ip_idx
  on public.votacao_votos (ip_hash, created_at);

alter table public.votacao_votos enable row level security;
revoke all on public.votacao_votos from anon, authenticated;

-- Ranking parcial, só para a organização (SQL editor / service role).
-- security_invoker: a view respeita a RLS da tabela e não vaza para o anon.
create or replace view public.votacao_ranking
  with (security_invoker = true) as
select categoria, finalista, count(*) as votos
from public.votacao_votos
where status = 'valido'
group by categoria, finalista;
revoke all on public.votacao_ranking from anon, authenticated;
