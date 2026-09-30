// Edge Function "summit-votos-admin": dados do painel de acompanhamento da votação.
// Só para a organização: exige a senha do painel (comparada por hash, tempo constante).
// A tabela votacao_votos tem e-mails, então nada aqui é público. Somente leitura.
// Para trocar a senha: gerar novo hash (ver supabase/VOTACAO.md) ou definir o segredo
// VOTOS_ADMIN_HASH no projeto (tem prioridade sobre o hash abaixo).
import "jsr:@supabase/functions-js/edge-runtime.d.ts";
import { createClient } from "jsr:@supabase/supabase-js@2";
import { agregar, paraCsv, type Voto } from "./agregar.ts";

const ALLOWED = [
  "https://intercambiosummit.com.br",
  "https://www.intercambiosummit.com.br",
  "http://localhost:8741",
];
const PREFIXO = "summit-votos-2026:";
const HASH_PADRAO = "ee946902fb987fe93ab300675a9af7d9072831bf7fa5eba3e7c1aee870384d86";
const COLUNAS = "categoria,finalista,nome,email,email_orig,empresa,tipo_empresa,ip_hash,status,motivo,created_at";

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
  const votos: Voto[] = [];
  for (let de = 0; ; de += 1000) {
    const { data, error } = await db
      .from("votacao_votos").select(COLUNAS).order("created_at", { ascending: true }).range(de, de + 999);
    if (error) return resp({ error: "db" }, 500);
    votos.push(...(data as Voto[]));
    if (!data || data.length < 1000) break;
  }

  if (body.acao === "exportar") return resp({ ok: true, csv: paraCsv(votos) });
  return resp({ ok: true, atualizado_em: new Date().toISOString(), ...agregar(votos) });
});
