// Edge Function "summit-happyhour-admin": dados do painel de respostas do happy hour.
// Só para a organização: exige a senha do painel (a mesma do painel da votação, comparada
// por hash em tempo constante). A tabela tem nomes e e-mails, então nada aqui é público.
// Somente leitura. O segredo VOTOS_ADMIN_HASH, se existir no projeto, tem prioridade.
import "jsr:@supabase/functions-js/edge-runtime.d.ts";
import { createClient } from "jsr:@supabase/supabase-js@2";

const ALLOWED = [
  "https://intercambiosummit.com.br",
  "https://www.intercambiosummit.com.br",
  "http://localhost:8741",
];
const PREFIXO = "summit-votos-2026:";
const HASH_PADRAO = "ee946902fb987fe93ab300675a9af7d9072831bf7fa5eba3e7c1aee870384d86";
const COLUNAS = "nome,empresa,email,resposta,perfil,created_at,updated_at";

type Resposta = {
  nome: string;
  empresa: string | null;
  email: string;
  resposta: "sim" | "nao";
  perfil: "participante" | "palestrante";
  created_at: string;
  updated_at: string;
};

function cors(origin: string | null) {
  const o = origin && ALLOWED.includes(origin) ? origin : ALLOWED[0];
  return {
    "Access-Control-Allow-Origin": o,
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "content-type",
    "Content-Type": "application/json",
    "Cache-Control": "no-store",
  };
}

async function sha256(texto: string): Promise<string> {
  const buf = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(texto));
  return Array.from(new Uint8Array(buf)).map((b) => b.toString(16).padStart(2, "0")).join("");
}

function iguais(a: string, b: string): boolean {
  if (a.length !== b.length) return false;
  let d = 0;
  for (let i = 0; i < a.length; i++) d |= a.charCodeAt(i) ^ b.charCodeAt(i);
  return d === 0;
}

// células que começam com = + - @ viram texto no Excel; o apóstrofo evita fórmula
function celula(v: unknown): string {
  let t = String(v ?? "");
  if (/^[=+\-@]/.test(t)) t = "'" + t;
  return '"' + t.replace(/"/g, '""') + '"';
}

function paraCsv(linhas: Resposta[]): string {
  const cab = ["nome", "empresa", "email", "resposta", "perfil", "respondeu_em", "atualizado_em"];
  const corpo = linhas.map((l) =>
    [l.nome, l.empresa, l.email, l.resposta === "sim" ? "vai" : "nao vai", l.perfil, l.created_at, l.updated_at]
      .map(celula).join(",")
  );
  return "﻿" + [cab.join(","), ...corpo].join("\n");
}

function agregar(linhas: Resposta[]) {
  const conta = (resposta: string, perfil?: string) =>
    linhas.filter((l) => l.resposta === resposta && (!perfil || l.perfil === perfil)).length;
  const dias = new Map<string, { dia: string; sim: number; nao: number }>();
  for (const l of linhas) {
    // dia em Brasília (UTC-3), pela data da primeira resposta
    const dia = new Date(new Date(l.created_at).getTime() - 3 * 3600 * 1000).toISOString().slice(0, 10);
    const d = dias.get(dia) ?? { dia, sim: 0, nao: 0 };
    d[l.resposta]++;
    dias.set(dia, d);
  }
  const ordenadas = [...linhas].sort((a, b) => b.updated_at.localeCompare(a.updated_at));
  return {
    totais: {
      respostas: linhas.length,
      vao: conta("sim"),
      nao_vao: conta("nao"),
      vao_participantes: conta("sim", "participante"),
      vao_palestrantes: conta("sim", "palestrante"),
    },
    por_dia: [...dias.values()].sort((a, b) => a.dia.localeCompare(b.dia)),
    vao: ordenadas.filter((l) => l.resposta === "sim"),
    nao_vao: ordenadas.filter((l) => l.resposta === "nao"),
  };
}

Deno.serve(async (req) => {
  const headers = cors(req.headers.get("origin"));
  const resp = (obj: unknown, status = 200) => new Response(JSON.stringify(obj), { status, headers });

  if (req.method === "OPTIONS") return new Response(null, { status: 204, headers });
  if (req.method !== "POST") return resp({ error: "method" }, 405);

  let body: Record<string, unknown>;
  try {
    body = await req.json();
  } catch {
    return resp({ error: "json" }, 400);
  }

  const senha = String(body.senha ?? "").slice(0, 200);
  const esperado = Deno.env.get("VOTOS_ADMIN_HASH") ?? HASH_PADRAO;
  if (!senha || !iguais(await sha256(PREFIXO + senha), esperado)) {
    await new Promise((r) => setTimeout(r, 600)); // freia tentativa em série
    return resp({ error: "senha" }, 401);
  }

  const db = createClient(Deno.env.get("SUPABASE_URL")!, Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!);
  const linhas: Resposta[] = [];
  for (let de = 0; ; de += 1000) {
    const { data, error } = await db
      .from("summit_happyhour_rsvp").select(COLUNAS).order("created_at", { ascending: true }).range(de, de + 999);
    if (error) return resp({ error: "db" }, 500);
    linhas.push(...(data as Resposta[]));
    if (!data || data.length < 1000) break;
  }

  if (body.acao === "exportar") return resp({ ok: true, csv: paraCsv(linhas) });
  return resp({ ok: true, atualizado_em: new Date().toISOString(), ...agregar(linhas) });
});
