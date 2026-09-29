// Edge Function "summit-leads" — endpoint público de captura de e-mail.
// Proteções próprias: allowlist de origem no CORS, honeypot, validação e
// limites de tamanho no servidor, upsert idempotente por e-mail.
import "jsr:@supabase/functions-js/edge-runtime.d.ts";
import { createClient } from "jsr:@supabase/supabase-js@2";

const ALLOWED = [
  "https://intercambiosummit.com.br",
  "https://www.intercambiosummit.com.br",
  "https://pathbusiness.github.io",
  "http://localhost:8741",
];

function cors(origin: string | null) {
  const o = origin && ALLOWED.includes(origin) ? origin : ALLOWED[0];
  return {
    "Access-Control-Allow-Origin": o,
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "content-type",
    "Content-Type": "application/json",
  };
}

Deno.serve(async (req) => {
  const headers = cors(req.headers.get("origin"));
  if (req.method === "OPTIONS") return new Response(null, { status: 204, headers });
  if (req.method !== "POST")
    return new Response(JSON.stringify({ error: "method" }), { status: 405, headers });

  let body: Record<string, unknown>;
  try {
    body = await req.json();
  } catch {
    return new Response(JSON.stringify({ error: "json" }), { status: 400, headers });
  }

  // honeypot: bots preenchem o campo oculto "site"; responde ok sem gravar
  if (typeof body.site === "string" && body.site !== "")
    return new Response(JSON.stringify({ ok: true }), { status: 200, headers });

  const email = String(body.email ?? "").trim().toLowerCase().slice(0, 254);
  const origem = String(body.origem ?? "site-summit-2026").slice(0, 64);
  if (!/^[^@\s]+@[^@\s]+\.[^@\s]{2,}$/.test(email))
    return new Response(JSON.stringify({ error: "email" }), { status: 400, headers });

  const db = createClient(
    Deno.env.get("SUPABASE_URL")!,
    Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!,
  );
  const { error } = await db
    .from("summit_leads")
    .upsert({ email, origem }, { onConflict: "email", ignoreDuplicates: true });
  if (error)
    return new Response(JSON.stringify({ error: "db" }), { status: 500, headers });
  return new Response(JSON.stringify({ ok: true }), { status: 200, headers });
});
