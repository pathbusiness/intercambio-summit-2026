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
  var elQtdTexto = document.getElementById("resumo-qtd-texto");
  var btn = document.getElementById("checkout-btn");

  /* ---------- quantidade de ingressos ---------- */
  var elQtd = document.getElementById("ck-quantidade");
  var elQtdMenos = document.getElementById("ck-qtd-menos");
  var elQtdMais = document.getElementById("ck-qtd-mais");
  var elExtras = document.getElementById("checkout-participantes-extra");
  var QTD_MAX = 10;

  function quantidadeAtual() {
    var n = parseInt(elQtd && elQtd.value, 10);
    if (!n || n < 1) n = 1;
    if (n > QTD_MAX) n = QTD_MAX;
    return n;
  }

  function renderParticipantesExtra() {
    if (!elExtras) return;
    var n = quantidadeAtual();
    // remove blocos além da quantidade atual
    Array.prototype.slice.call(elExtras.children).forEach(function (bloco) {
      var idx = parseInt(bloco.getAttribute("data-participante"), 10);
      if (idx > n) elExtras.removeChild(bloco);
    });
    // adiciona blocos que faltam
    for (var i = 2; i <= n; i++) {
      if (elExtras.querySelector('[data-participante="' + i + '"]')) continue;
      var bloco = document.createElement("div");
      bloco.className = "checkout-participante";
      bloco.setAttribute("data-participante", String(i));
      bloco.innerHTML =
        '<p class="checkout-participante-titulo">Ingresso ' + i + '</p>' +
        '<div class="checkout-row">' +
          '<label>Nome <span>*</span><input type="text" id="ck-nome-' + i + '" autocomplete="off" required maxlength="80" placeholder="Nome"></label>' +
          '<label>Sobrenome <span>*</span><input type="text" id="ck-sobrenome-' + i + '" autocomplete="off" required maxlength="80" placeholder="Sobrenome"></label>' +
        '</div>' +
        '<label>E-mail <span>*</span><input type="email" id="ck-email-' + i + '" autocomplete="off" inputmode="email" required maxlength="254" placeholder="participante' + i + '@empresa.com.br"></label>';
      elExtras.appendChild(bloco);
    }
    if (elQtdTexto) elQtdTexto.textContent = n === 1 ? "1 ingresso" : n + " ingressos";
  }
  renderParticipantesExtra();
  if (elQtd) {
    elQtd.addEventListener("input", function () { renderParticipantesExtra(); atualizarResumo(); });
    elQtd.addEventListener("blur", function () { elQtd.value = quantidadeAtual(); });
  }
  if (elQtdMenos) elQtdMenos.addEventListener("click", function () {
    elQtd.value = Math.max(1, quantidadeAtual() - 1);
    renderParticipantesExtra(); atualizarResumo();
  });
  if (elQtdMais) elQtdMais.addEventListener("click", function () {
    elQtd.value = Math.min(QTD_MAX, quantidadeAtual() + 1);
    renderParticipantesExtra(); atualizarResumo();
  });

  function parcelaTexto(precoUnitario, qtd) {
    if (!loteAtual.parcelado) return "";
    var n = parseInt(/^(\d+)x/.exec(loteAtual.parcelado)[1], 10);
    var totalParcela = Math.round((precoUnitario * qtd / n) * 100) / 100;
    return "ou " + n + "x " + brl(totalParcela) + " sem juros";
  }

  function atualizarResumo() {
    if (!loteAtual) return;
    var qtd = quantidadeAtual();
    var precoUnitario = cupomValidado ? cupomValidado.valor : loteAtual.avista;
    if (cupomValidado) {
      elPreco.innerHTML = '<s class="checkout-resumo-original">' + brl(loteAtual.avista * qtd) + "</s> " + brl(cupomValidado.valor * qtd);
    } else {
      elPreco.textContent = brl(loteAtual.avista * qtd);
    }
    elParc.textContent = parcelaTexto(precoUnitario, qtd);
  }

  if (loteAtual) {
    elLote.textContent = loteAtual.nome;
    atualizarResumo();
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

    var qtd = quantidadeAtual();
    var dados = {
      nome: document.getElementById("ck-nome").value.trim(),
      sobrenome: document.getElementById("ck-sobrenome").value.trim(),
      email: document.getElementById("ck-email").value.trim(),
      telefone: document.getElementById("ck-telefone").value.trim(),
      empresa: document.getElementById("ck-empresa").value.trim(),
      quantidade: qtd,
      site: document.getElementById("ck-site").value
    };
    // só envia o cupom se ele foi validado com sucesso e não foi editado depois
    var cupomDigitado = elCupomInput ? elCupomInput.value.trim().toUpperCase() : "";
    if (cupomValidado && cupomValidado.codigo === cupomDigitado) dados.codigo = cupomDigitado;

    if (dados.nome.length < 2) { fb.textContent = MSGS.nome; return; }
    if (dados.sobrenome.length < 2) { fb.textContent = MSGS.sobrenome; return; }
    if (!/^[^@\s]+@[^@\s]+\.[^@\s]{2,}$/.test(dados.email)) { fb.textContent = MSGS.email; return; }
    if (dados.telefone.replace(/\D/g, "").length < 10) { fb.textContent = MSGS.telefone; return; }

    var participantes = [{ nome: dados.nome, sobrenome: dados.sobrenome, email: dados.email }];
    for (var i = 2; i <= qtd; i++) {
      var pNome = (document.getElementById("ck-nome-" + i) || {}).value || "";
      var pSobrenome = (document.getElementById("ck-sobrenome-" + i) || {}).value || "";
      var pEmail = (document.getElementById("ck-email-" + i) || {}).value || "";
      pNome = pNome.trim(); pSobrenome = pSobrenome.trim(); pEmail = pEmail.trim();
      if (pNome.length < 2) { fb.textContent = "Confira o nome do ingresso " + i + "."; return; }
      if (pSobrenome.length < 2) { fb.textContent = "Confira o sobrenome do ingresso " + i + "."; return; }
      if (!/^[^@\s]+@[^@\s]+\.[^@\s]{2,}$/.test(pEmail)) { fb.textContent = "Confira o e-mail do ingresso " + i + "."; return; }
      participantes.push({ nome: pNome, sobrenome: pSobrenome, email: pEmail });
    }
    dados.participantes = participantes;

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
