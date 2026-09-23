// Edge Function "summit-mp-webhook" — recebe as notificações do Mercado Pago,
// confirma o pagamento consultando a API do MP (fonte da verdade; nunca
// confia no corpo da notificação) e, quando aprovado, cria o pedido no
// Zoho Backstage — o participante recebe o ingresso oficial por e-mail.
//
// Segredos necessários (Supabase → Edge Functions → Secrets):
//   MP_ACCESS_TOKEN          — Access Token de produção do Mercado Pago
//   ZOHO_CLIENT_ID           — Self Client no api-console.zoho.com
//   ZOHO_CLIENT_SECRET
//   ZOHO_REFRESH_TOKEN       — escopo ZohoBackstage.order.CREATE
//   BACKSTAGE_TICKETCLASS_ID — classe de ingresso (gratuita/oculta) que o
//                              site usa para emitir o ingresso no Backstage
import "jsr:@supabase/functions-js/edge-runtime.d.ts";
import { createClient } from "jsr:@supabase/supabase-js@2";

const BACKSTAGE_PORTAL_ID = Deno.env.get("BACKSTAGE_PORTAL_ID") ?? "888835921";
const BACKSTAGE_EVENT_ID = Deno.env.get("BACKSTAGE_EVENT_ID") ?? "175925000000749018";

const ok = () =>
  new Response(JSON.stringify({ ok: true }), {
    status: 200,
    headers: { "Content-Type": "application/json" },
  });

// Troca o refresh token por um access token válido (~1h; pedimos um novo
// a cada notificação — volume baixo, sem necessidade de cache).
async function zohoAccessToken(): Promise<string> {
  const params = new URLSearchParams({
    grant_type: "refresh_token",
    client_id: Deno.env.get("ZOHO_CLIENT_ID")!,
    client_secret: Deno.env.get("ZOHO_CLIENT_SECRET")!,
    refresh_token: Deno.env.get("ZOHO_REFRESH_TOKEN")!,
  });
  const r = await fetch("https://accounts.zoho.com/oauth/v2/token", {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: params,
  });
  const j = await r.json();
  if (!j.access_token) throw new Error("zoho-token: " + JSON.stringify(j).slice(0, 300));
  return j.access_token;
}

// Cria o pedido no Backstage (classe gratuita ⇒ sem pagamento a conciliar no Zoho)
async function criarNoBackstage(pedido: {
  nome: string; sobrenome: string; email: string;
  telefone: string; empresa: string;
}): Promise<string> {
  const token = await zohoAccessToken();
  const ticketClass = Deno.env.get("BACKSTAGE_TICKETCLASS_ID");
  if (!ticketClass) throw new Error("backstage-ticketclass-nao-configurada");

  const url = `https://www.zohoapis.com/backstage/v3/portals/${BACKSTAGE_PORTAL_ID}/events/${BACKSTAGE_EVENT_ID}/orders`;
  const payload = {
    buyer_details: {
      purchaser_first_name: pedido.nome,
      purchaser_last_name: pedido.sobrenome,
      purchaser_email: pedido.email,
      purchaser_company: pedido.empresa || undefined,
      purchaser_mobile_no: pedido.telefone || undefined,
    },
    tickets: [{
      ticketclass_id: ticketClass,
      data: {
        first_name: pedido.nome,
        last_name: pedido.sobrenome,
        email: pedido.email,
      },
    }],
  };
  const r = await fetch(url, {
    method: "POST",
    headers: {
      "Authorization": `Zoho-oauthtoken ${token}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });
  const texto = await r.text();
  if (!r.ok) throw new Error(`backstage ${r.status}: ${texto.slice(0, 500)}`);
  try {
    const j = JSON.parse(texto);
    return String(j?.order?.id ?? j?.data?.id ?? j?.id ?? "");
  } catch {
    return "";
  }
}

Deno.serve(async (req) => {
  // O MP notifica por POST (webhook, JSON {type, data.id}) e por GET/POST
  // com query string (IPN: ?topic=payment&id=...). Aceitamos os dois.
  const u = new URL(req.url);
  let tipo = u.searchParams.get("type") ?? u.searchParams.get("topic") ?? "";
  let pagamentoId = u.searchParams.get("data.id") ?? u.searchParams.get("id") ?? "";
  if (req.method === "POST") {
    try {
      const body = await req.json();
      tipo = String(body?.type ?? body?.topic ?? tipo);
      pagamentoId = String(body?.data?.id ?? pagamentoId);
    } catch { /* corpo vazio ou não-JSON: segue com a query string */ }
  }
  // merchant_order / plan / etc. não interessam — respondemos 200 para o MP não reenviar
  if (!/payment/.test(tipo) || !pagamentoId) return ok();

  const mpToken = Deno.env.get("MP_ACCESS_TOKEN");
  if (!mpToken) return ok();

  // Fonte da verdade: busca o pagamento direto na API do MP
  const pagResp = await fetch(`https://api.mercadopago.com/v1/payments/${pagamentoId}`, {
    headers: { "Authorization": `Bearer ${mpToken}` },
  });
  if (!pagResp.ok) return ok();
  const pag = await pagResp.json();
  const pedidoId = String(pag.external_reference ?? "");
  if (!pedidoId) return ok();

  const db = createClient(
    Deno.env.get("SUPABASE_URL")!,
    Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!,
  );
  const { data: pedido } = await db
    .from("summit_orders").select("*").eq("id", pedidoId).maybeSingle();
  if (!pedido) return ok();

  const agora = new Date().toISOString();

  // Estorno/cancelamento: só marca o status (tratamento manual no Backstage)
  if (["refunded", "charged_back", "cancelled"].includes(pag.status)) {
    await db.from("summit_orders").update({
      status: pag.status === "cancelled" ? "cancelado" : "reembolsado",
      mp_payment_id: String(pag.id), mp_status: pag.status, updated_at: agora,
    }).eq("id", pedidoId);
    return ok();
  }

  if (pag.status !== "approved") {
    await db.from("summit_orders").update({
      mp_payment_id: String(pag.id), mp_status: pag.status, updated_at: agora,
    }).eq("id", pedidoId);
    return ok();
  }

  // Idempotência: o MP reenvia notificações; se já registrou, encerra
  if (pedido.status === "registrado") return ok();

  await db.from("summit_orders").update({
    status: "pago", mp_payment_id: String(pag.id), mp_status: pag.status, updated_at: agora,
  }).eq("id", pedidoId);

  try {
    const backstageId = await criarNoBackstage(pedido);
    await db.from("summit_orders").update({
      status: "registrado", backstage_order_id: backstageId, erro: null,
      updated_at: new Date().toISOString(),
    }).eq("id", pedidoId);
  } catch (e) {
    // Pagamento está seguro; só o registro no Backstage falhou.
    // Fica em "erro_registro" para reprocessar (novo webhook do MP ou manual).
    await db.from("summit_orders").update({
      status: "erro_registro", erro: String(e).slice(0, 900),
      updated_at: new Date().toISOString(),
    }).eq("id", pedidoId);
  }
  return ok();
});
