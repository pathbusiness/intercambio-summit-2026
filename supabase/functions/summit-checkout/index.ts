// Edge Function "summit-checkout" — cria o pedido e devolve o link de
// pagamento do Mercado Pago (Checkout Pro: Pix, cartão em até 5x, boleto).
//
// O preço NUNCA vem do navegador: o lote vigente é calculado aqui pela
// data de São Paulo. Ao mudar os lotes em site/evento.config.js, espelhe
// a mudança na tabela LOTES abaixo e reimplante a função.
//
// Cupons: espelham os mesmos códigos cadastrados no Zoho Backstage
// (Códigos promocionais), já que a venda no site não passa mais pelo
// Backstage — os limites de uso e validade são reaplicados aqui.
// Ao mudar algo lá, espelhe em PROMO_CODES abaixo e reimplante.
//
// Segredos necessários (Supabase → Edge Functions → Secrets):
//   MP_ACCESS_TOKEN  — Access Token de produção do Mercado Pago (conta PATH)
import "jsr:@supabase/functions-js/edge-runtime.d.ts";
import { createClient } from "jsr:@supabase/supabase-js@2";

const SITE = "https://intercambiosummit.com.br";
const WEBHOOK_URL =
  "https://ildxeqtmpbartonjoiwc.supabase.co/functions/v1/summit-mp-webhook";

const LOTES = [
  { nome: "Early Bird",    inicio: "2026-09-01", fim: "2026-09-30", avista: 350 },
  { nome: "Segundo lote",  inicio: "2026-10-01", fim: "2026-10-24", avista: 450 },
  { nome: "Terceiro lote", inicio: "2026-10-25", fim: "2026-11-10", avista: 550 },
  { nome: "Dia do evento", inicio: "2026-11-11", fim: "2026-11-11", avista: 650 },
];

// Mesmos cupons do Zoho Backstage (Registros → Códigos promocionais).
// desconto: fração (0.10 = 10%). max_usos: mesmo limite de resgates de lá.
const PROMO_CODES: Record<string, { desconto: number; inicio: string; fim: string; max_usos: number }> = {
  ABRAPEI10: { desconto: 0.10, inicio: "2026-09-23", fim: "2026-10-31", max_usos: 10 },
  ALLY10:    { desconto: 0.10, inicio: "2026-09-23", fim: "2026-10-31", max_usos: 10 },
  BELTA10:   { desconto: 0.10, inicio: "2026-09-23", fim: "2026-10-31", max_usos: 10 },
  EARLY10:   { desconto: 0.10, inicio: "2026-09-23", fim: "2026-10-01", max_usos: 10 },
  EDVISOR10: { desconto: 0.10, inicio: "2026-09-23", fim: "2026-10-31", max_usos: 10 },
  IALC10:    { desconto: 0.10, inicio: "2026-09-23", fim: "2026-10-30", max_usos: 10 },
};

const ALLOWED = [
  "https://intercambiosummit.com.br",
  "https://www.intercambiosummit.com.br",
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

// Data de hoje no fuso de São Paulo, como "AAAA-MM-DD"
function hojeSP(): string {
  return new Intl.DateTimeFormat("en-CA", {
    timeZone: "America/Sao_Paulo",
    year: "numeric", month: "2-digit", day: "2-digit",
  }).format(new Date());
}

function loteVigente() {
  const hoje = hojeSP();
  return LOTES.find((l) => hoje >= l.inicio && hoje <= l.fim) ?? null;
}

// Valida o cupom (existência, validade, limite de usos já confirmados/pagos).
// Retorna { erro } ou { codigo, desconto }.
async function validarCupom(
  db: ReturnType<typeof createClient>,
  codigoBruto: unknown,
): Promise<{ erro: string } | { codigo: string; desconto: number } | null> {
  const codigo = String(codigoBruto ?? "").trim().toUpperCase();
  if (!codigo) return null; // sem cupom informado

  const regra = PROMO_CODES[codigo];
  if (!regra) return { erro: "cupom-invalido" };

  const hoje = hojeSP();
  if (hoje < regra.inicio || hoje > regra.fim) return { erro: "cupom-expirado" };

  const { count, error } = await db
    .from("summit_orders")
    .select("id", { count: "exact", head: true })
    .eq("promo_code", codigo)
    .in("status", ["pago", "registrado"]);
  if (error) return { erro: "cupom-indisponivel" };
  if ((count ?? 0) >= regra.max_usos) return { erro: "cupom-esgotado" };

  return { codigo, desconto: regra.desconto };
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
    return new Response(JSON.stringify({ ok: true, url: SITE }), { status: 200, headers });

  const lote = loteVigente();
  if (!lote)
    return new Response(JSON.stringify({ error: "vendas-encerradas" }), { status: 409, headers });

  const db = createClient(
    Deno.env.get("SUPABASE_URL")!,
    Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!,
  );

  const cupomResultado = await validarCupom(db, body.codigo);
  if (cupomResultado && "erro" in cupomResultado)
    return new Response(JSON.stringify({ error: cupomResultado.erro }), { status: 400, headers });

  const descontoPct = cupomResultado?.desconto ?? 0;
  const precoFinal = Math.round(lote.avista * (1 - descontoPct) * 100) / 100;

  // Prévia: só valida o cupom e devolve o preço, sem criar pedido nem cobrar.
  // Usado pelo botão "Aplicar" do cupom no checkout, antes de ir para o pagamento.
  if (body.dryRun) {
    return new Response(JSON.stringify({
      ok: true, lote: lote.nome, valor: precoFinal,
      valorOriginal: lote.avista, desconto: descontoPct,
      codigo: cupomResultado?.codigo ?? null,
    }), { status: 200, headers });
  }

  const nome = String(body.nome ?? "").trim().slice(0, 80);
  const sobrenome = String(body.sobrenome ?? "").trim().slice(0, 80);
  const email = String(body.email ?? "").trim().toLowerCase().slice(0, 254);
  const telefone = String(body.telefone ?? "").replace(/\D/g, "").slice(0, 15);
  const empresa = String(body.empresa ?? "").trim().slice(0, 120);

  if (nome.length < 2)
    return new Response(JSON.stringify({ error: "nome" }), { status: 400, headers });
  if (sobrenome.length < 2)
    return new Response(JSON.stringify({ error: "sobrenome" }), { status: 400, headers });
  if (!/^[^@\s]+@[^@\s]+\.[^@\s]{2,}$/.test(email))
    return new Response(JSON.stringify({ error: "email" }), { status: 400, headers });
  if (telefone.length < 10)
    return new Response(JSON.stringify({ error: "telefone" }), { status: 400, headers });

  const mpToken = Deno.env.get("MP_ACCESS_TOKEN");
  if (!mpToken)
    return new Response(
      JSON.stringify({ error: "pagamento-nao-configurado" }),
      { status: 503, headers },
    );

  const { data: pedido, error: dbErr } = await db
    .from("summit_orders")
    .insert({
      nome, sobrenome, email, telefone, empresa,
      lote: lote.nome, valor: precoFinal, quantidade: 1,
      promo_code: cupomResultado?.codigo ?? null, desconto_pct: descontoPct,
    })
    .select("id")
    .single();
  if (dbErr || !pedido)
    return new Response(JSON.stringify({ error: "db" }), { status: 500, headers });

  // Preferência do Checkout Pro. O comprador escolhe Pix, cartão (até 5x
  // sem juros para ele — custo do parcelamento configurado na conta MP) ou boleto.
  const sucesso = `${SITE}/obrigado.html?lote=${encodeURIComponent(lote.nome)}&valor=${precoFinal}`;
  const tituloCupom = cupomResultado?.codigo ? ` (cupom ${cupomResultado.codigo})` : "";
  const pref = {
    items: [{
      id: "summit-2026",
      title: `Ingresso Intercâmbio Summit 2026 — ${lote.nome}${tituloCupom}`,
      description: "11 de novembro de 2026 · Contentix, Av. Paulista 967, São Paulo",
      category_id: "tickets",
      quantity: 1,
      currency_id: "BRL",
      unit_price: precoFinal,
    }],
    payer: {
      name: nome,
      surname: sobrenome,
      email,
      phone: { area_code: telefone.slice(0, 2), number: telefone.slice(2) },
    },
    external_reference: pedido.id,
    back_urls: {
      success: sucesso,
      pending: sucesso,
      failure: `${SITE}/checkout.html?pagamento=erro`,
    },
    auto_return: "approved",
    notification_url: WEBHOOK_URL,
    statement_descriptor: "SUMMIT2026",
    payment_methods: { installments: 5 },
    metadata: { origem: "site-summit-2026", promo_code: cupomResultado?.codigo ?? null },
  };

  const mpResp = await fetch("https://api.mercadopago.com/checkout/preferences", {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${mpToken}`,
      "Content-Type": "application/json",
      "X-Idempotency-Key": pedido.id,
    },
    body: JSON.stringify(pref),
  });
  if (!mpResp.ok) {
    const detalhe = await mpResp.text();
    await db.from("summit_orders")
      .update({ status: "erro_mp", erro: detalhe.slice(0, 900), updated_at: new Date().toISOString() })
      .eq("id", pedido.id);
    return new Response(JSON.stringify({ error: "mp" }), { status: 502, headers });
  }

  const mp = await mpResp.json();
  await db.from("summit_orders")
    .update({ mp_preference_id: mp.id, updated_at: new Date().toISOString() })
    .eq("id", pedido.id);

  return new Response(
    JSON.stringify({ ok: true, url: mp.init_point }),
    { status: 200, headers },
  );
});
