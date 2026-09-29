/* Intercâmbio Summit 2026 — página de votação (/votar).
   Regras (Regulamento Oficial): votação pública entre os finalistas, um voto por
   categoria; quem é de agência vota nas categorias de instituições e vice-versa.
   O navegador só envia as escolhas: elegibilidade, janela de datas e unicidade são
   conferidas de novo no servidor (Edge Function summit-votar). */
(function () {
  "use strict";
  var EV = window.EVENTO || {};
  var CFG = EV.votacao || {};
  var form = document.getElementById("votacao-form");
  if (!form) return;

  var emProducao = location.hostname !== "localhost" && location.hostname !== "127.0.0.1";
  var elEstado = document.getElementById("vt-estado");
  var elErro = document.getElementById("vt-erro");
  var elCats = document.getElementById("vt-categorias");
  var elRodape = document.getElementById("vt-rodape");
  var elContagem = document.getElementById("vt-contagem");
  var btn = document.getElementById("vt-enviar");
  var dados = { categorias: [] };
  var enviando = false;

  // trilha em que cada tipo de eleitor pode votar (voto cruzado, como na 1ª etapa)
  var TRILHA_ELEGIVEL = { agencia: "Instituições", instituicao: "Agências" };

  function fmtDia(iso) {
    var p = iso.split("-"), meses = ["janeiro","fevereiro","março","abril","maio","junho","julho",
      "agosto","setembro","outubro","novembro","dezembro"];
    return +p[2] + " de " + meses[+p[1] - 1];
  }
  function janela() {
    var ini = new Date((CFG.inicio || "2026-10-01") + "T00:00:00-03:00");
    var fim = new Date((CFG.fim || "2026-10-30") + "T23:59:59-03:00");
    var agora = new Date();
    return agora < ini ? "antes" : agora > fim ? "depois" : "aberta";
  }
  function esc(t) {
    return String(t == null ? "" : t).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }
  function erro(msg) {
    elErro.textContent = msg || "";
    elErro.hidden = !msg;
    if (msg) elErro.scrollIntoView({ behavior: "smooth", block: "center" });
  }

  /* ---------- estado da votação ---------- */
  var estado = janela();
  if (estado !== "aberta") {
    elEstado.hidden = false;
    elEstado.textContent = estado === "antes"
      ? "A votação abre em " + fmtDia(CFG.inicio || "2026-10-01") + ". Volte nesse dia para votar."
      : "A votação foi encerrada em " + fmtDia(CFG.fim || "2026-10-30") + ". Obrigado a quem votou! Os vencedores serão anunciados em 11 de novembro.";
    // fora da janela: mostra os finalistas, mas não deixa enviar
  }
  if (CFG.regulamentoUrl) {
    document.getElementById("vt-reg").innerHTML = 'Leia o <a href="' + esc(CFG.regulamentoUrl) + '" target="_blank" rel="noopener">regulamento</a>.';
  }

  /* ---------- categorias e finalistas ---------- */
  function tipoAtual() {
    var r = form.querySelector('input[name="tipo"]:checked');
    return r ? r.value : "";
  }

  function renderCategorias() {
    var tipo = tipoAtual();
    if (!tipo) return;
    var trilha = TRILHA_ELEGIVEL[tipo];
    var html = "";
    dados.categorias.filter(function (c) { return c.trilha === trilha; }).forEach(function (c, i) {
      html += '<fieldset class="vt-cat" data-cat="' + esc(c.id) + '">' +
        "<legend>" + (i + 2) + ". " + esc(c.nome) + "</legend>" +
        '<p class="vt-cat-desc">' + esc(c.descricao) + "</p>" +
        '<div class="vt-grid">';
      c.finalistas.forEach(function (f) {
        var resumo = f.resumo
          ? "<details><summary>Ver destaque do dossiê</summary><p>" + esc(f.resumo) + "</p></details>" : "";
        var sub = [f.cargo, f.empresa].filter(Boolean).join(" · ");
        html += '<div class="vt-card"><label>' +
          '<input type="radio" name="cat-' + esc(c.id) + '" value="' + esc(f.slug) + '" required>' +
          '<img loading="lazy" src="assets/img/finalistas/' + esc(f.slug) + '-400.webp" srcset="assets/img/finalistas/' +
          esc(f.slug) + "-400.webp 400w, assets/img/finalistas/" + esc(f.slug) + '-800.webp 800w" sizes="(max-width:640px) 45vw, 190px" alt="' + esc(f.nome) + '">' +
          '<span class="vt-nome">' + esc(f.nome) + "</span>" +
          (sub ? '<span class="vt-empresa">' + esc(sub) + "</span>" : "") +
          "</label>" + resumo + "</div>";
      });
      html += "</div></fieldset>";
    });
    elCats.innerHTML = html;
    elRodape.hidden = false;
    btn.disabled = estado !== "aberta";
    atualizaContagem();
  }

  function selecoes() {
    var v = {};
    Array.prototype.forEach.call(elCats.querySelectorAll(".vt-cat"), function (fs) {
      var r = fs.querySelector("input:checked");
      if (r) v[fs.getAttribute("data-cat")] = r.value;
    });
    return v;
  }
  function atualizaContagem() {
    var total = elCats.querySelectorAll(".vt-cat").length;
    var n = Object.keys(selecoes()).length;
    elContagem.textContent = total ? n + " de " + total + " categorias escolhidas" : "";
  }

  form.addEventListener("change", function (e) {
    if (e.target.name === "tipo") { erro(""); renderCategorias(); }
    else if (e.target.name && e.target.name.indexOf("cat-") === 0) atualizaContagem();
  });

  /* ---------- envio ---------- */
  var MENSAGENS = {
    nome: "Informe seu nome e sobrenome.",
    empresa: "Informe a empresa ou instituição onde você trabalha.",
    email: "Confira o e-mail. Use um e-mail profissional válido.",
    tipo: "Informe se você trabalha em agência ou em instituição.",
    votos: "Escolha ao menos um finalista.",
    voto_invalido: "Um dos finalistas escolhidos não é válido. Recarregue a página e tente de novo.",
    elegibilidade: "Você só pode votar nas categorias do outro tipo de empresa (agência vota em instituições e vice-versa).",
    janela: "A votação não está aberta neste momento.",
    limite: "Muitos votos vieram desta conexão em pouco tempo. Tente novamente mais tarde.",
    db: "Não conseguimos registrar agora. Tente de novo em instantes."
  };

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    if (enviando || estado !== "aberta") return;
    erro("");
    var payload = {
      nome: form.nome.value, email: form.email.value, empresa: form.empresa.value,
      tipo: tipoAtual(), votos: selecoes(), site: form.site.value
    };
    if (payload.nome.trim().split(/\s+/).length < 2) return erro(MENSAGENS.nome);
    if (!/^[^@\s]+@[^@\s]+\.[^@\s]{2,}$/.test(payload.email.trim())) return erro(MENSAGENS.email);
    if (payload.empresa.trim().length < 2) return erro(MENSAGENS.empresa);
    if (!payload.tipo) return erro(MENSAGENS.tipo);
    if (!Object.keys(payload.votos).length) return erro(MENSAGENS.votos);

    enviando = true; btn.disabled = true; btn.textContent = "Enviando...";
    var destino = !emProducao && CFG.apiLocal ? CFG.apiLocal : CFG.api;
    fetch(destino, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(payload) })
      .then(function (r) { return r.json().catch(function () { return {}; }).then(function (j) { return { ok: r.ok, j: j }; }); })
      .then(function (res) {
        if (!res.ok || !res.j.ok) {
          var cod = res.j.error;
          erro(cod === "janela" && res.j.estado === "depois" ? "A votação foi encerrada."
            : (MENSAGENS[cod] || "Não foi possível enviar. Tente novamente."));
          return;
        }
        mostrarSucesso(res.j);
      })
      .catch(function () { erro("Sem conexão. Verifique sua internet e tente de novo."); })
      .then(function () { enviando = false; btn.disabled = false; btn.textContent = "Enviar meus votos"; });
  });

  function nomeCategoria(id) {
    var c = dados.categorias.filter(function (x) { return x.id === id; })[0];
    return c ? c.nome : id;
  }
  function nomeFinalista(id, slug) {
    var c = dados.categorias.filter(function (x) { return x.id === id; })[0];
    var f = c && c.finalistas.filter(function (x) { return x.slug === slug; })[0];
    return f ? f.nome : slug;
  }
  /* lote vigente + dados da pessoa levados ao checkout (só nesta aba, sessionStorage) */
  function prepararIngresso() {
    var hoje = new Date(), d0 = new Date(hoje.getFullYear(), hoje.getMonth(), hoje.getDate());
    function dia(iso) { var p = iso.split("-"); return new Date(+p[0], +p[1] - 1, +p[2]); }
    var lote = null;
    (EV.lotes || []).forEach(function (l) { if (!lote && d0 >= dia(l.inicio) && d0 <= dia(l.fim)) lote = l; });
    var el = document.getElementById("vt-ingresso-lote");
    if (lote) {
      el.innerHTML = "<strong>" + esc(lote.nome) + ":</strong> R$ " + lote.avista.toLocaleString("pt-BR") +
        (lote.parcelado ? ", ou " + esc(lote.parcelado) : " à vista") +
        (lote.inicio !== lote.fim ? ". Vale até " + fmtDia(lote.fim) + "." : ".");
    } else {
      document.getElementById("vt-ingresso").hidden = true;
    }
    try {
      var partes = form.nome.value.trim().split(/\s+/);
      sessionStorage.setItem("summit_prefill", JSON.stringify({
        nome: partes[0] || "", sobrenome: partes.slice(1).join(" "),
        email: form.email.value.trim(), empresa: form.empresa.value.trim()
      }));
    } catch (e) { /* sem storage: o checkout abre em branco */ }
  }

  function mostrarSucesso(j) {
    var sel = selecoes();
    var ul = document.getElementById("vt-sucesso-lista");
    ul.innerHTML = (j.registrados || []).map(function (c) {
      return "<li><strong>" + esc(nomeCategoria(c)) + ":</strong> " + esc(nomeFinalista(c, sel[c])) + "</li>";
    }).join("");
    var ja = document.getElementById("vt-sucesso-ja");
    ja.textContent = (j.ja_votou && j.ja_votou.length)
      ? "Você já tinha votado em " + j.ja_votou.map(nomeCategoria).join(", ") + ". Vale o primeiro voto de cada categoria."
      : "";
    prepararIngresso();
    form.hidden = true;
    document.querySelector(".votacao-lead").hidden = true;
    document.getElementById("vt-sucesso").hidden = false;
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  /* ---------- dados dos finalistas ---------- */
  fetch("data/votacao.json").then(function (r) { return r.json(); }).then(function (d) {
    dados = d;
    if (tipoAtual()) renderCategorias();
  }).catch(function () {
    erro("Não foi possível carregar os finalistas. Recarregue a página.");
  });
})();
