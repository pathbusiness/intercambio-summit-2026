/* Intercâmbio Summit 2026 — página de checkout próprio.
   O preço exibido vem de evento.config.js; o preço COBRADO é recalculado
   no servidor (Edge Function summit-checkout) — o navegador nunca manda valor. */
(function () {
  "use strict";
  var EV = window.EVENTO || {};
  var form = document.getElementById("checkout-form");
  if (!form) return;

  var emProducao = location.hostname !== "localhost" && location.hostname !== "127.0.0.1";

  function brl(v) { return "R$ " + v.toLocaleString("pt-BR"); }
  function parseDia(iso) {
    var p = iso.split("-");
    return new Date(+p[0], +p[1] - 1, +p[2]);
  }
  function fmtDia(iso) {
    var d = parseDia(iso);
    var meses = ["janeiro","fevereiro","março","abril","maio","junho","julho",
                 "agosto","setembro","outubro","novembro","dezembro"];
    return d.getDate() + " de " + meses[d.getMonth()];
  }

  /* ---------- resumo do lote vigente ---------- */
  var hoje = (function () {
    var n = new Date();
    return new Date(n.getFullYear(), n.getMonth(), n.getDate());
  })();
  var loteAtual = null, proximoLote = null;
  (EV.lotes || []).forEach(function (l) {
    if (hoje >= parseDia(l.inicio) && hoje <= parseDia(l.fim) && !loteAtual) loteAtual = l;
    if (hoje < parseDia(l.inicio) && !proximoLote) proximoLote = l;
  });

  var elLote = document.getElementById("resumo-lote");
  var elPreco = document.getElementById("resumo-preco");
  var elParc = document.getElementById("resumo-parcelado");
  var elVirada = document.getElementById("resumo-virada");
  var btn = document.getElementById("checkout-btn");

  function atualizarResumo() {
    if (!loteAtual) return;
    if (cupomValidado) {
      elPreco.innerHTML = '<s class="checkout-resumo-original">' + brl(loteAtual.avista) + "</s> " + brl(cupomValidado.valor);
    } else {
      elPreco.textContent = brl(loteAtual.avista);
    }
  }

  if (loteAtual) {
    elLote.textContent = loteAtual.nome;
    atualizarResumo();
    if (loteAtual.parcelado) elParc.textContent = "ou " + loteAtual.parcelado;
    if (proximoLote) {
      elVirada.textContent = "Este preço vale até " + fmtDia(loteAtual.fim) +
        ". Depois, " + proximoLote.nome.toLowerCase() + " por " + brl(proximoLote.avista) + ".";
    }
  } else {
    elLote.textContent = "Vendas encerradas";
    elPreco.textContent = "—";
    btn.disabled = true;
    btn.textContent = "Vendas encerradas";
  }

  /* ---------- cupom promocional ---------- */
  var elCupomInput = document.getElementById("ck-cupom");
  var elCupomBtn = document.getElementById("cupom-aplicar");
  var elCupomFb = document.getElementById("cupom-feedback");
  var cupomValidado = null; // { codigo, valor } do último "Aplicar" bem-sucedido

  var CUPOM_MSGS = {
    "cupom-invalido": "Cupom não encontrado.",
    "cupom-expirado": "Este cupom não está mais disponível.",
    "cupom-esgotado": "Este cupom já atingiu o limite de usos.",
    "cupom-indisponivel": "Não foi possível validar o cupom agora. Tente novamente.",
    "vendas-encerradas": "As vendas online foram encerradas.",
  };

  function aplicarCupom() {
    var codigo = elCupomInput.value.trim().toUpperCase();
    elCupomFb.className = "checkout-cupom-feedback";
    if (!codigo) { elCupomFb.textContent = ""; cupomValidado = null; atualizarResumo(); return; }
    if (!loteAtual) return;

    var ehLocal = !emProducao;
    var destino = ehLocal && EV.checkoutApiLocal ? EV.checkoutApiLocal : EV.checkoutApi;
    if (!destino) return;

    elCupomFb.textContent = "Verificando…";
    elCupomBtn.disabled = true;
    fetch(destino, {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ codigo: codigo, dryRun: true })
    })
      .then(function (r) { return r.json().then(function (j) { return { status: r.status, body: j }; }); })
      .then(function (r) {
        elCupomBtn.disabled = false;
        if (r.body && r.body.ok) {
          cupomValidado = { codigo: r.body.codigo || codigo, valor: r.body.valor };
          var pct = Math.round((r.body.desconto || 0) * 100);
          elCupomFb.textContent = "Cupom aplicado: " + pct + "% de desconto.";
          elCupomFb.className = "checkout-cupom-feedback is-ok";
        } else {
          cupomValidado = null;
          var erro = r.body && r.body.error;
          elCupomFb.textContent = CUPOM_MSGS[erro] || "Não foi possível aplicar este cupom.";
          elCupomFb.className = "checkout-cupom-feedback is-erro";
        }
        atualizarResumo();
      })
      .catch(function () {
        elCupomBtn.disabled = false;
        cupomValidado = null;
        elCupomFb.textContent = "Falha de conexão ao validar o cupom.";
        elCupomFb.className = "checkout-cupom-feedback is-erro";
        atualizarResumo();
      });
  }
  if (elCupomBtn) elCupomBtn.addEventListener("click", aplicarCupom);
  if (elCupomInput) {
    elCupomInput.addEventListener("input", function () {
      if (cupomValidado) { cupomValidado = null; elCupomFb.textContent = ""; atualizarResumo(); }
    });
    elCupomInput.addEventListener("keydown", function (e) {
      if (e.key === "Enter") { e.preventDefault(); aplicarCupom(); }
    });
  }

  /* cupom vindo por link (ex.: e-mail de parceiro, ?cupom=IALC10) */
  var cupomNaUrl = new URLSearchParams(location.search).get("cupom");
  if (cupomNaUrl && elCupomInput) {
    elCupomInput.value = cupomNaUrl.toUpperCase();
    aplicarCupom();
  }

  /* ---------- aviso vindo do retorno do Mercado Pago ---------- */
  var alerta = document.getElementById("checkout-alert");
  if (new URLSearchParams(location.search).get("pagamento") === "erro" && alerta) {
    alerta.textContent = "O pagamento não foi concluído. Nenhum valor foi cobrado — você pode tentar novamente abaixo.";
    alerta.hidden = false;
  }

  /* ---------- rastreamento leve (GTM/Pixel carregados pelo main.js) ---------- */
  function rastrear(evento, dados) {
    if (!emProducao) return;
    if (window.dataLayer) window.dataLayer.push(Object.assign({ event: evento }, dados || {}));
    if (window.fbq) window.fbq("track", "InitiateCheckout", dados || {});
    if (window.posthog) window.posthog.capture(evento, dados || {});
  }

  /* ---------- envio ---------- */
  var fb = document.getElementById("checkout-feedback");
  var MSGS = {
    nome: "Confira o nome digitado.",
    sobrenome: "Confira o sobrenome digitado.",
    email: "Confira o e-mail digitado.",
    telefone: "Confira o celular digitado (com DDD).",
    "vendas-encerradas": "As vendas online foram encerradas.",
    "pagamento-nao-configurado": "O pagamento online está em manutenção. Tente novamente em instantes.",
    "cupom-invalido": "Cupom não encontrado.",
    "cupom-expirado": "Este cupom não está mais disponível.",
    "cupom-esgotado": "Este cupom já atingiu o limite de usos.",
  };

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    fb.textContent = "";

    var dados = {
      nome: document.getElementById("ck-nome").value.trim(),
      sobrenome: document.getElementById("ck-sobrenome").value.trim(),
      email: document.getElementById("ck-email").value.trim(),
      telefone: document.getElementById("ck-telefone").value.trim(),
      empresa: document.getElementById("ck-empresa").value.trim(),
      site: document.getElementById("ck-site").value
    };
    // só envia o cupom se ele foi validado com sucesso e não foi editado depois
    var cupomDigitado = elCupomInput ? elCupomInput.value.trim().toUpperCase() : "";
    if (cupomValidado && cupomValidado.codigo === cupomDigitado) dados.codigo = cupomDigitado;

    if (dados.nome.length < 2) { fb.textContent = MSGS.nome; return; }
    if (dados.sobrenome.length < 2) { fb.textContent = MSGS.sobrenome; return; }
    if (!/^[^@\s]+@[^@\s]+\.[^@\s]{2,}$/.test(dados.email)) { fb.textContent = MSGS.email; return; }
    if (dados.telefone.replace(/\D/g, "").length < 10) { fb.textContent = MSGS.telefone; return; }

    var ehLocal = !emProducao;
    var destino = ehLocal && EV.checkoutApiLocal ? EV.checkoutApiLocal : EV.checkoutApi;
    if (!destino) { fb.textContent = "Checkout ainda não configurado."; return; }

    btn.disabled = true;
    var rotulo = btn.textContent;
    btn.textContent = "Gerando link de pagamento…";
    rastrear("begin_checkout", {
      currency: "BRL",
      value: dados.codigo && cupomValidado ? cupomValidado.valor : (loteAtual ? loteAtual.avista : undefined)
    });

    fetch(destino, {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify(dados)
    })
      .then(function (r) { return r.json().then(function (j) { return { status: r.status, body: j }; }); })
      .then(function (r) {
        if (r.body && r.body.ok && r.body.url) {
          btn.textContent = "Abrindo o Mercado Pago…";
          location.href = r.body.url;
          return;
        }
        var erro = r.body && r.body.error;
        fb.textContent = MSGS[erro] || "Não foi possível iniciar o pagamento. Tente novamente em instantes.";
        btn.disabled = false;
        btn.textContent = rotulo;
      })
      .catch(function () {
        fb.textContent = "Falha de conexão. Verifique sua internet e tente novamente.";
        btn.disabled = false;
        btn.textContent = rotulo;
      });
  });
})();
