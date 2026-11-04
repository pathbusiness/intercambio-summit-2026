/* Painel das respostas do happy hour (uso interno, somente leitura).
   A senha vai para a Edge Function summit-happyhour-admin, que confere o hash e devolve os
   números. Nada fica salvo além da senha na aba (sessionStorage), apagada ao sair. */
(function () {
  "use strict";
  var API = location.hostname === "localhost" || location.hostname === "127.0.0.1"
    ? "https://ildxeqtmpbartonjoiwc.supabase.co/functions/v1/summit-happyhour-admin"
    : "/api/happyhour-admin";
  var CHAVE = "summit_painel_happyhour_senha";
  var senha = "", timer = null;

  function $(id) { return document.getElementById(id); }
  function esc(t) {
    return String(t == null ? "" : t).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }
  function n(v) { return Number(v).toLocaleString("pt-BR"); }
  function dataHora(iso) {
    return new Date(iso).toLocaleString("pt-BR", { timeZone: "America/Sao_Paulo", day: "2-digit", month: "2-digit", hour: "2-digit", minute: "2-digit" });
  }
  function dia(iso) { var p = iso.split("-"); return p[2] + "/" + p[1]; }
  function erro(el, msg) { el.textContent = msg || ""; el.hidden = !msg; }

  function chamar(corpo) {
    corpo.senha = senha;
    return fetch(API, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(corpo) })
      .then(function (r) { return r.json().catch(function () { return {}; }).then(function (j) { return { status: r.status, j: j }; }); });
  }

  /* ---------- desenho ---------- */
  function kpis(t) {
    var itens = [
      ["Vão ao happy hour", t.vao], ["Não vão", t.nao_vao], ["Total de respostas", t.respostas],
      ["Participantes que vão", t.vao_participantes], ["Palestrantes que vão", t.vao_palestrantes]
    ];
    $("pv-kpis").innerHTML = itens.map(function (i) {
      return '<div class="pv-kpi"><span class="pv-kpi-n">' + n(i[1]) + '</span><span class="pv-kpi-l">' + esc(i[0]) + "</span></div>";
    }).join("");
  }

  function porDia(lista) {
    if (!lista.length) { $("pv-dias").innerHTML = '<p class="pv-vazio">Ainda não há respostas.</p>'; return; }
    var max = Math.max.apply(null, lista.map(function (d) { return d.sim + d.nao; }));
    $("pv-dias").innerHTML = '<div class="pv-colunas">' + lista.map(function (d) {
      var t = d.sim + d.nao;
      return '<div class="pv-col" title="' + esc(dia(d.dia)) + ": " + d.sim + " vão, " + d.nao + ' não vão"><span class="pv-col-v">' + n(t) +
        '</span><span class="pv-col-b" style="height:' + Math.max(4, t / max * 100).toFixed(1) + '%"></span><span class="pv-col-d">' + esc(dia(d.dia)) + "</span></div>";
    }).join("") + "</div>";
  }

  function tabela(el, lista, vazio) {
    el.innerHTML = lista.length
      ? '<table class="pv-tabela"><thead><tr><th>Nome</th><th>Empresa</th><th>E-mail</th><th>Perfil</th><th>Respondeu</th></tr></thead><tbody>' +
        lista.map(function (l) {
          return "<tr><td>" + esc(l.nome) + "</td><td>" + esc(l.empresa || "") + "</td><td>" + esc(l.email) + "</td><td>" +
            (l.perfil === "palestrante" ? "Palestrante" : "Participante") + "</td><td>" + esc(dataHora(l.updated_at)) + "</td></tr>";
        }).join("") + "</tbody></table>"
      : '<p class="pv-vazio">' + esc(vazio) + "</p>";
  }

  function mostrar(r) {
    kpis(r.totais); porDia(r.por_dia);
    tabela($("pv-vao"), r.vao, "Ninguém confirmou ainda.");
    tabela($("pv-nao"), r.nao_vao, "Ninguém recusou ainda.");
    $("pv-quando").textContent = "Atualizado às " + new Date(r.atualizado_em).toLocaleTimeString("pt-BR", { timeZone: "America/Sao_Paulo", hour: "2-digit", minute: "2-digit" });
  }

  /* ---------- fluxo ---------- */
  function carregar() {
    return chamar({}).then(function (res) {
      if (res.status === 401) { sair("Senha incorreta."); return false; }
      if (!res.j.ok) { erro($("pv-erro2"), "Não foi possível carregar agora. Tente atualizar em instantes."); return false; }
      erro($("pv-erro2"), ""); mostrar(res.j); return true;
    }).catch(function () {
      erro($("pv-erro2"), "Sem conexão. Tente atualizar em instantes."); return false;
    });
  }

  function entrar() {
    $("pv-login").hidden = true; $("pv-painel").hidden = false;
    clearInterval(timer); timer = setInterval(carregar, 60000);
  }
  function sair(msg) {
    senha = ""; clearInterval(timer);
    try { sessionStorage.removeItem(CHAVE); } catch (e) {}
    $("pv-painel").hidden = true; $("pv-login").hidden = false; $("pv-senha").value = "";
    erro($("pv-erro"), msg || "");
  }

  $("pv-form").addEventListener("submit", function (e) {
    e.preventDefault();
    senha = $("pv-senha").value; if (!senha) return;
    var b = $("pv-entrar"); b.disabled = true; b.textContent = "Entrando...";
    erro($("pv-erro"), "");
    carregar().then(function (ok) {
      if (ok) { try { sessionStorage.setItem(CHAVE, senha); } catch (x) {} entrar(); }
      else if ($("pv-login").hidden === false && !$("pv-erro").textContent) erro($("pv-erro"), "Não foi possível entrar agora. Tente de novo.");
    }).then(function () { b.disabled = false; b.textContent = "Entrar"; });
  });
  $("pv-atualizar").addEventListener("click", carregar);
  $("pv-sair").addEventListener("click", function () { sair(""); });
  $("pv-csv").addEventListener("click", function () {
    chamar({ acao: "exportar" }).then(function (res) {
      if (!res.j.ok) return erro($("pv-erro2"), "Não foi possível gerar o CSV agora.");
      var blob = new Blob([res.j.csv], { type: "text/csv;charset=utf-8" });
      var a = document.createElement("a");
      a.href = URL.createObjectURL(blob);
      a.download = "happyhour-" + new Date().toISOString().slice(0, 10) + ".csv";
      document.body.appendChild(a); a.click(); a.remove();
      setTimeout(function () { URL.revokeObjectURL(a.href); }, 2000);
    });
  });

  var salva = ""; try { salva = sessionStorage.getItem(CHAVE) || ""; } catch (e) {}
  if (salva) { senha = salva; carregar().then(function (ok) { if (ok) entrar(); }); }
})();
