-- RSVP do happy hour pós-Summit (11/11, bar Eu, Tu, Eles).
-- Uma linha por e-mail: quem responde de novo atualiza a resposta (vale a última).
-- Acesso só pela Edge Function "summit-happyhour" (service role): RLS ligada e sem políticas.
create table if not exists public.summit_happyhour_rsvp (
  id          bigint generated always as identity primary key,
  created_at  timestamptz not null default now(),
  updated_at  timestamptz not null default now(),
  email       text not null unique,       -- minúsculas
  nome        text not null,
  empresa     text,
  resposta    text not null check (resposta in ('sim', 'nao')),
  perfil      text not null default 'participante' check (perfil in ('participante', 'palestrante')),
  user_agent  text
);

alter table public.summit_happyhour_rsvp enable row level security;
revoke all on public.summit_happyhour_rsvp from anon, authenticated;

-- Resumo para a organização (SQL editor / service role).
create or replace view public.summit_happyhour_resumo as
  select resposta, perfil, count(*) as total
  from public.summit_happyhour_rsvp
  group by resposta, perfil
  order by resposta desc, perfil;
revoke all on public.summit_happyhour_resumo from anon, authenticated;
