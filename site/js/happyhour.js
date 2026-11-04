/* Intercâmbio Summit 2026 — RSVP do happy hour pós-Summit (/happyhour).
   O link do e-mail traz só a resposta (?r=sim|nao) e o perfil (?p=palestrante),
   sem dados pessoais. Validação e gravação ficam na Edge Function summit-happyhour. */
(function () {
  "use strict";
  var EV = window.EVENTO || {};
  var CFG = EV.happyhour || {};
  var form = document.getElementById("hh-form");
  if (!form) return;

  var elErro = document.getElementById("hh-erro");
  var btn = document.getElementById("hh-enviar");
  var emProducao = location.hostname !== "localhost" && location.hostname !== "127.0.0.1";
  var enviando = false;

  var MENSAGENS = {
    nome: "Informe seu nome e sobrenome.",
    email: "Confira o e-mail: parece que há um erro.",
    resposta: "Escolha entre \"Eu vou\" e \"Não vou\".",
    db: "Não foi possível registrar agora. Tente novamente em instantes."
  };

  function erro(msg) {
    elErro.textContent = msg || "";
    elErro.hidden = !msg;
    if (msg) elErro.scrollIntoView({ behavior: "smooth", block: "center" });
  }

  // pré-seleção vinda do botão do e-mail
  var params = new URLSearchParams(location.search);
  var r = params.get("r");
  if (r === "sim" || r === "nao") {
    var radio = form.querySelector('input[name="resposta"][value="' + r + '"]');
    if (radio) radio.checked = true;
  }
  var perfil = params.get("p") === "palestrante" ? "palestrante" : "participante";

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    if (enviando) return;
    erro("");
    var marcada = form.querySelector('input[name="resposta"]:checked');
    var payload = {
      resposta: marcada ? marcada.value : "",
      nome: form.nome.value.trim(),
      email: form.email.value.trim(),
      empresa: form.empresa.value.trim(),
      perfil: perfil,
      site: form.site.value
    };
    if (!payload.resposta) return erro(MENSAGENS.resposta);
    if (payload.nome.length < 2) return erro(MENSAGENS.nome);
    if (!/^[^@\s]+@[^@\s]+\.[^@\s]{2,}$/.test(payload.email)) return erro(MENSAGENS.email);

    enviando = true;
    btn.disabled = true;
    btn.textContent = "Enviando…";
    var destino = emProducao ? CFG.api : (CFG.apiLocal || CFG.api);
    fetch(destino, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(payload) })
      .then(function (res) { return res.json().catch(function () { return {}; }).then(function (j) { return { ok: res.ok, j: j }; }); })
      .then(function (res) {
        if (!res.ok || !res.j.ok) {
          erro(MENSAGENS[res.j.error] || "Não foi possível enviar. Tente novamente.");
          return;
        }
        var vai = payload.resposta === "sim";
        document.getElementById("hh-sucesso-titulo").textContent = vai ? "Presença confirmada!" : "Resposta registrada";
        document.getElementById("hh-sucesso-texto").textContent = vai
          ? "Nos vemos no Eu, Tu, Eles, na Alameda Joaquim Eugênio de Lima, 612, logo depois do Summit. Mudou de ideia? Responda de novo com o mesmo e-mail."
          : "Obrigado por avisar. Se mudar de ideia, é só responder de novo com o mesmo e-mail.";
        form.hidden = true;
        var s = document.getElementById("hh-sucesso");
        s.hidden = false;
        s.scrollIntoView({ behavior: "smooth", block: "center" });
      })
      .catch(function () { erro("Sem conexão. Verifique sua internet e tente de novo."); })
      .then(function () { enviando = false; btn.disabled = false; btn.textContent = "Enviar minha resposta"; });
  });
})();
