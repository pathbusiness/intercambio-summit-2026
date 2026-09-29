// Edge Function "summit-votar": recebe os votos do Prêmio Melhores Profissionais.
// Regras (Regulamento Oficial): votação pública entre os finalistas de 01/10 a 30/10;
// um voto por categoria por pessoa; votos duplicados ou suspeitos podem ser invalidados.
// Proteções: allowlist de origem (CORS), honeypot, janela de datas, elegibilidade por
// trilha, unicidade (e-mail, categoria) no banco, limite por IP e trilha de auditoria.
import "jsr:@supabase/functions-js/edge-runtime.d.ts";
import { createClient } from "jsr:@supabase/supabase-js@2";
import { janela, validar } from "./validar.ts";

const ALLOWED = [
  "https://intercambiosummit.com.br",
  "https://www.intercambiosummit.com.br",
  "https://pathbusiness.github.io",
  "http://localhost:8741",
];

// Horário de Brasília (UTC-3). Sobrescrevível por variável de ambiente para testes.
const INICIO = new Date(Deno.env.get("VOTACAO_INICIO") ?? "2026-10-01T00:00:00-03:00");
const FIM = new Date(Deno.env.get("VOTACAO_FIM") ?? "2026-10-30T23:59:59-03:00");
const LIMITE_EMAILS_POR_IP_HORA = 25; // escritórios compartilham IP: limite folgado, só barra automação

function cors(origin: string | null) {
  const o = origin && ALLOWED.includes(origin) ? origin : ALLOWED[0];
  return {
    "Access-Control-Allow-Origin": o,
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "content-type",
    "Content-Type": "application/json",
  };
}

async function sha256(texto: string): Promise<string> {
  const buf = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(texto));
  return Array.from(new Uint8Array(buf)).map((b) => b.toString(16).padStart(2, "0")).join("");
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

  // honeypot: bots preenchem o campo oculto "site"; responde ok sem gravar
  if (typeof body.site === "string" && body.site !== "") return resp({ ok: true, registrados: [], ja_votou: [] });

  const estado = janela(new Date(), INICIO, FIM);
  if (estado !== "aberta") return resp({ error: "janela", estado }, 403);

  const v = validar(body);
  if (!v.ok) return resp({ error: v.erro, detalhe: v.detalhe }, v.status);
  const { nome, email, emailOrig, empresa, tipo, votos } = v.dados;

  const db = createClient(Deno.env.get("SUPABASE_URL")!, Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!);

  const ip = (req.headers.get("x-forwarded-for") ?? "").split(",")[0].trim() || "sem-ip";
  const ipHash = await sha256(ip + (Deno.env.get("VOTACAO_SALT") ?? "summit-2026"));
  const ua = (req.headers.get("user-agent") ?? "").slice(0, 200);

  // limite por IP: e-mails distintos na última hora
  const desde = new Date(Date.now() - 3600_000).toISOString();
  const { data: recentes } = await db
    .from("votacao_votos").select("email").eq("ip_hash", ipHash).gte("created_at", desde).limit(500);
  const distintos = new Set((recentes ?? []).map((r: { email: string }) => r.email));
  if (!distintos.has(email) && distintos.size >= LIMITE_EMAILS_POR_IP_HORA)
    return resp({ error: "limite" }, 429);

  const linhas = votos.map((x) => ({
    categoria: x.categoria, finalista: x.finalista, nome, email, email_orig: emailOrig,
    empresa, tipo_empresa: tipo, ip_hash: ipHash, user_agent: ua,
  }));
  // ignoreDuplicates: quem já votou na categoria não é sobrescrito; select() devolve só o que entrou
  const { data, error } = await db
    .from("votacao_votos")
    .upsert(linhas, { onConflict: "email,categoria", ignoreDuplicates: true })
    .select("categoria");
  if (error) return resp({ error: "db" }, 500);

  const registrados = (data ?? []).map((r: { categoria: string }) => r.categoria);
  const jaVotou = votos.map((x) => x.categoria).filter((c) => !registrados.includes(c));
  return resp({ ok: true, registrados, ja_votou: jaVotou });
});
