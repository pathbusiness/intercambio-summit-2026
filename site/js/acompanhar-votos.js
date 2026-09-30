/* Painel de acompanhamento da votação (uso interno, somente leitura).
   A senha vai para a Edge Function summit-votos-admin, que confere o hash e devolve os
   números. Nada fica salvo além da senha na aba (sessionStorage), apagada ao sair. */
(function () {
  "use strict";
  var API = location.hostname === "localhost" || location.hostname === "127.0.0.1"
    ? "https://ildxeqtmpbartonjoiwc.supabase.co/functions/v1/summit-votos-admin"
    : "/api/votos-admin";
  var CHAVE = "summit_painel_senha";
  var senha = "", dados = { categorias: [] }, nomes = {}, catNomes = {}, timer = null;

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
      ["Votos válidos", t.votos_validos], ["Pessoas que votaram", t.eleitores],
      ["De agências", t.eleitores_agencia], ["De instituições", t.eleitores_instituicao],
      ["Votos invalidados", t.votos_invalidados]
    ];
    $("pv-kpis").innerHTML = itens.map(function (i) {
      return '<div class="pv-kpi"><span class="pv-kpi-n">' + n(i[1]) + '</span><span class="pv-kpi-l">' + esc(i[0]) + "</span></div>";
    }).join("");
  }

  function categorias(ranking) {
    $("pv-cats").innerHTML = dados.categorias.map(function (c) {
      var linhas = (ranking[c.id] || []).slice();
      var vistos = {};
      linhas.forEach(function (l) { vistos[l.finalista] = true; });
      c.finalistas.forEach(function (f) { if (!vistos[f.slug]) linhas.push({ finalista: f.slug, votos: 0 }); });
      var total = linhas.reduce(function (s, l) { return s + l.votos; }, 0);
      var max = linhas.length ? linhas[0].votos : 0;
      var html = '<article class="pv-cat"><h3>' + esc(c.nome) + '</h3><p class="pv-cat-sub">' + esc(c.trilha) +
        " · " + n(total) + (total === 1 ? " voto" : " votos") + "</p><ol>";
      linhas.forEach(function (l, i) {
        var pct = total ? Math.round(l.votos / total * 100) : 0;
        var w = max ? (l.votos / max * 100) : 0;
        html += '<li class="' + (i === 0 && l.votos > 0 ? "lider" : "") + '"><span class="pv-nome">' + esc(nomes[l.finalista] || l.finalista) +
          '</span><span class="pv-barra-v"><i style="width:' + w.toFixed(1) + '%"></i></span><span class="pv-v">' + n(l.votos) +
          '<small>' + pct + "%</small></span></li>";
      });
      return html + "</ol></article>";
    }).join("");
  }

  function porDia(lista) {
    if (!lista.length) { $("pv-dias").innerHTML = '<p class="pv-vazio">Ainda não há votos.</p>'; return; }
    var max = Math.max.apply(null, lista.map(function (d) { return d.votos; }));
    $("pv-dias").innerHTML = '<div class="pv-colunas">' + lista.map(function (d) {
      return '<div class="pv-col" title="' + esc(dia(d.dia)) + ": " + d.votos + " votos, " + d.eleitores + ' pessoas"><span class="pv-col-v">' + n(d.votos) +
        '</span><span class="pv-col-b" style="height:' + Math.max(4, d.votos / max * 100).toFixed(1) + '%"></span><span class="pv-col-d">' + esc(dia(d.dia)) + "</span></div>";
    }).join("") + "</div>";
  }

  function suspeitos(lista) {
    $("pv-suspeitos").innerHTML = lista.length
      ? '<div class="pv-tabela-wrap"><table class="pv-tabela"><thead><tr><th>Conexão</th><th>E-mails</th><th>Votos</th><th>Empresas</th></tr></thead><tbody>' +
        lista.map(function (s) {
          return "<tr><td><code>" + esc(s.conexao) + "</code></td><td>" + n(s.emails) + "</td><td>" + n(s.votos) + "</td><td>" + n(s.empresas) + "</td></tr>";
        }).join("") + "</tbody></table></div>"
      : '<p class="pv-vazio">Nenhuma conexão com 5 ou mais e-mails diferentes.</p>';
  }

  function recentes(lista) {
    $("pv-recentes").innerHTML = lista.length
      ? '<table class="pv-tabela"><thead><tr><th>Quando</th><th>Nome</th><th>E-mail</th><th>Empresa</th><th>Tipo</th><th>Categoria</th><th>Voto</th><th>Status</th></tr></thead><tbody>' +
        lista.map(function (v) {
          return "<tr" + (v.status !== "valido" ? ' class="inval"' : "") + "><td>" + esc(dataHora(v.quando)) + "</td><td>" + esc(v.nome) +
            "</td><td>" + esc(v.email) + "</td><td>" + esc(v.empresa) + "</td><td>" + (v.tipo === "agencia" ? "Agência" : "Instituição") +
            "</td><td>" + esc(catNomes[v.categoria] || v.categoria) + "</td><td>" + esc(nomes[v.finalista] || v.finalista) +
            "</td><td>" + (v.status === "valido" ? "Válido" : "Invalidado") + "</td></tr>";
        }).join("") + "</tbody></table>"
      : '<p class="pv-vazio">Ainda não há votos.</p>';
  }

  function mostrar(r) {
    kpis(r.totais); categorias(r.ranking); porDia(r.por_dia); suspeitos(r.suspeitos); recentes(r.recentes);
    $("pv-quando").textContent = "Atualizado às " + new Date(r.atualizado_em).toLocaleTimeString("pt-BR", { timeZone: "America/Sao_Paulo", hour: "2-digit", minute: "2-digit" });
  }

  /* ---------- fluxo ---------- */
  function carregar(silencioso) {
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
    clearInterval(timer); timer = setInterval(function () { carregar(true); }, 60000);
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
  $("pv-atualizar").addEventListener("click", function () { carregar(); });
  $("pv-sair").addEventListener("click", function () { sair(""); });
  $("pv-csv").addEventListener("click", function () {
    chamar({ acao: "exportar" }).then(function (res) {
      if (!res.j.ok) return erro($("pv-erro2"), "Não foi possível gerar o CSV agora.");
      var blob = new Blob(["﻿" + res.j.csv], { type: "text/csv;charset=utf-8" });
      var a = document.createElement("a");
      a.href = URL.createObjectURL(blob);
      a.download = "votos-" + new Date().toISOString().slice(0, 10) + ".csv";
      document.body.appendChild(a); a.click(); a.remove();
      setTimeout(function () { URL.revokeObjectURL(a.href); }, 2000);
    });
  });

  fetch("data/votacao.json").then(function (r) { return r.json(); }).then(function (d) {
    dados = d;
    d.categorias.forEach(function (c) {
      catNomes[c.id] = c.nome;
      c.finalistas.forEach(function (f) { nomes[f.slug] = f.nome; });
    });
  }).catch(function () {}).then(function () {
    var salva = ""; try { salva = sessionStorage.getItem(CHAVE) || ""; } catch (e) {}
    if (salva) { senha = salva; carregar().then(function (ok) { if (ok) entrar(); }); }
  });
})();
