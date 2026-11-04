// Edge Function "summit-happyhour" — RSVP do happy hour pós-Summit.
// Mesmas proteções da summit-leads: allowlist de origem no CORS, honeypot,
// validação e limites de tamanho no servidor. Upsert por e-mail: a última resposta vale.
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

const json = (body: unknown, status: number, headers: HeadersInit) =>
  new Response(JSON.stringify(body), { status, headers });

Deno.serve(async (req) => {
  const headers = cors(req.headers.get("origin"));
  if (req.method === "OPTIONS") return new Response(null, { status: 204, headers });
  if (req.method !== "POST") return json({ error: "method" }, 405, headers);

  let body: Record<string, unknown>;
  try {
    body = await req.json();
  } catch {
    return json({ error: "json" }, 400, headers);
  }

  // honeypot: bots preenchem o campo oculto "site"; responde ok sem gravar
  if (typeof body.site === "string" && body.site !== "") return json({ ok: true }, 200, headers);

  const nome = String(body.nome ?? "").trim().slice(0, 80);
  const email = String(body.email ?? "").trim().toLowerCase().slice(0, 254);
  const empresa = String(body.empresa ?? "").trim().slice(0, 100) || null;
  const resposta = body.resposta === "sim" || body.resposta === "nao" ? body.resposta : "";
  const perfil = body.perfil === "palestrante" ? "palestrante" : "participante";

  if (nome.length < 2) return json({ error: "nome" }, 400, headers);
  if (!/^[^@\s]+@[^@\s]+\.[^@\s]{2,}$/.test(email)) return json({ error: "email" }, 400, headers);
  if (!resposta) return json({ error: "resposta" }, 400, headers);

  const db = createClient(
    Deno.env.get("SUPABASE_URL")!,
    Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!,
  );
  const { error } = await db.from("summit_happyhour_rsvp").upsert(
    {
      email,
      nome,
      empresa,
      resposta,
      perfil,
      user_agent: (req.headers.get("user-agent") ?? "").slice(0, 200),
      updated_at: new Date().toISOString(),
    },
    { onConflict: "email" },
  );
  if (error) return json({ error: "db" }, 500, headers);
  return json({ ok: true, resposta }, 200, headers);
});
