# Dashboard de resultados — Intercâmbio Summit 2026

Painel visual dos resultados das pesquisas (geral + por palestra): NPS, médias por dimensão, expectativas, intenção de voltar, ranking das palestras e depoimentos.

- **Link (artifact, privado do dono):** https://claude.ai/artifact/Pr1H2A6bXMixr1qQ6SzmZ1
- **Fonte:** `dashboard.html` (os dados ficam embutidos em `const DATA = {...}` no topo do `<script>`).

## Como atualizar (sob demanda)
O painel é um **snapshot**: os números ficam embutidos no HTML e são atualizados ao **republicar o artifact**. Durante/depois do evento, é só pedir ao Claude **"atualiza o dashboard"** — ele:
1. Lê os agregados no Supabase (tabelas `summit2026_respostas` e `summit2026_palestras`) via conector.
2. Substitui o `const DATA` e republica o mesmo artifact (mesmo link).

> Auto-refresh agendado não é usado: rotinas na nuvem não têm acesso ao conector do Supabase nem republicam o artifact. Por isso a atualização é sob demanda (rápida e segura — não expõe o banco publicamente).

## Compartilhar com a equipe
O artifact é privado do dono. Para a equipe ver, use o menu **Share** da página do artifact.
