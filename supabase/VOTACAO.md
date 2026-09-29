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

**Supabase, projeto "Forio"** (ref `lvchpskxeohfmistppxl`, região us-west-2), tabela **`public.votacao_votos`**.

- Ver: https://supabase.com/dashboard/project/lvchpskxeohfmistppxl/editor → Table Editor → `votacao_votos`.
- Consultar/exportar: SQL Editor (consultas abaixo); o resultado tem botão para baixar CSV.
- Cada linha: categoria, finalista (slug), nome, e-mail (normalizado e original), empresa, tipo (agência ou
  instituição), hash do IP, navegador, data/hora, `status` (`valido` ou `invalidado`) e `motivo`.
- O site nunca lê essa tabela; só a função `summit-votar` escreve (service role). Anon e authenticated não têm acesso.

Atenção: o projeto Forio também guarda outros sistemas da PATH (contratos, alunos, cotações). Quem tiver acesso ao
painel vê tudo isso. Para terceiros (conferência, comitê), compartilhe um CSV exportado, não o acesso ao painel.

## Estado em produção

| Item | Situação |
|---|---|
| Migração `votacao_premio_2026` (tabela, índices, RLS, view de ranking) | **Aplicada em 29/09** no projeto Forio |
| Função `summit-votar` (v1, `verify_jwt: false`, teto 300 e-mails/IP/hora) | **Publicada em 29/09** (ativa; responde "janela: antes" até 01/10 00:00 de Brasília) |
| Site (página `/votar`, rewrites, botão no Prêmio, convite pós-voto) | **Falta publicar** (merge na `main`) |

`site/vercel.json` e `evento.config.js` apontam `/api/votar` para o projeto Forio, onde a função está.
**Aviso:** as demais rotas do site (`/api/leads`, `/api/checkout`) apontam para outro identificador de projeto
(`ildxeqtmpbartonjoiwc`), e a função `summit-checkout` publicada no Forio é uma versão anterior à do repositório
(sem quantidade de ingressos e com o Early Bird ainda até 30/09). Conferir antes de 01/10.

Teste ponta a ponta após publicar o site: votar uma vez com e-mail `@teste.local` e depois apagar:
`delete from public.votacao_votos where email like '%@teste.local';`
(o teste com votos reais só é possível a partir de 01/10 00:00; antes disso a função recusa).

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
