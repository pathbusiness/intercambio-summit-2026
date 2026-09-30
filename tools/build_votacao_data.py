#!/usr/bin/env python3
"""Gera os dados da votação a partir de criativos/data/finalistas.json.

Saídas (não editar à mão):
  site/data/votacao.json                          -> página /votar
  supabase/functions/summit-votar/finalistas.ts   -> validação no servidor

Resumos dos dossiês (opcional): criativos/data/dossies-resumos.json
  { "slug-do-finalista": { "empresa": "", "cargo": "", "resumo": "", "aprovado": true } }
Só entra na página quem tiver "aprovado": true (autorização do finalista).
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
fin = json.load(open(os.path.join(ROOT, "criativos", "data", "finalistas.json"), encoding="utf-8"))
cats, fins = fin["_categorias"], fin["finalistas"]

dossies = {}
p = os.path.join(ROOT, "criativos", "data", "dossies-resumos.json")
if os.path.exists(p):
    dossies = {k: v for k, v in json.load(open(p, encoding="utf-8")).items() if v.get("aprovado") is True}

categorias = []
for key, c in cats.items():
    lista = sorted((f for f in fins if f["categoria"] == key), key=lambda f: f["nome"])
    categorias.append({
        "id": key, "nome": c["nome"], "trilha": c["trilha"], "descricao": c["descricao"],
        "finalistas": [{
            "slug": f["slug"], "nome": f["nome"],
            "empresa": dossies.get(f["slug"], {}).get("empresa", ""),
            "cargo": dossies.get(f["slug"], {}).get("cargo", ""),
            "resumo": dossies.get(f["slug"], {}).get("resumo", ""),
        } for f in lista],
    })

os.makedirs(os.path.join(ROOT, "site", "data"), exist_ok=True)
json.dump({"categorias": categorias}, open(os.path.join(ROOT, "site", "data", "votacao.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)

ts = ["// GERADO por tools/build_votacao_data.py. Não editar à mão.",
      "export const TRILHA: Record<string, string> = {"]
ts += [f'  {json.dumps(c["id"])}: {json.dumps(c["trilha"], ensure_ascii=False)},' for c in categorias]
ts += ["};", "", "// slug do finalista -> categoria", "export const FINALISTAS: Record<string, string> = {"]
ts += [f'  {json.dumps(f["slug"])}: {json.dumps(c["id"])},' for c in categorias for f in c["finalistas"]]
ts += ["};", ""]
open(os.path.join(ROOT, "supabase", "functions", "summit-votar", "finalistas.ts"), "w", encoding="utf-8").write("\n".join(ts))
print(f"{len(categorias)} categorias, {sum(len(c['finalistas']) for c in categorias)} finalistas, {len(dossies)} resumos aprovados")
