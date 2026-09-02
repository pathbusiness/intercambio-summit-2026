/* Intercâmbio Summit 2026 — comportamento do site
   Conteúdo editável vive em evento.config.js, não aqui. */
(function () {
  "use strict";
  var EV = window.EVENTO || {};

  /* ---------- utilidades de data (fuso local) ---------- */
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
  function hoje() {
    var n = new Date();
    return new Date(n.getFullYear(), n.getMonth(), n.getDate());
  }
  function brl(v) { return "R$ " + v.toLocaleString("pt-BR"); }

  /* ---------- campos data-evento ---------- */
  document.querySelectorAll("[data-evento]").forEach(function (el) {
    var k = el.getAttribute("data-evento");
    if (EV[k]) el.textContent = EV[k];
  });

  /* ---------- palestrantes ---------- */
  var spg = document.getElementById("speakers-grid");
  if (spg && EV.palestrantes) {
    EV.palestrantes.forEach(function (p) {
      var tba = !p.cargo && !p.empresa && /em breve/i.test(p.nome);
      var card = document.createElement("div");
      card.className = "speaker-card" + (tba ? " is-tba" : "");
      var foto;
      if (p.foto && p.slug) {
        foto = '<img loading="lazy" src="assets/img/palestrantes/' + p.slug + '-800.webp" alt="' + p.nome + '">';
      } else {
        var initials = tba ? "Em breve" : p.nome.split(/\s+/).map(function (n) { return n[0]; }).slice(0, 2).join("");
        foto = '<span class="speaker-initials">' + initials + "</span>";
      }
      card.innerHTML =
        '<div class="speaker-photo">' + foto + "</div>" +
        '<div class="speaker-info"><h3>' + p.nome + "</h3>" +
        "<p>" + [p.cargo, p.empresa].filter(Boolean).join(", ") + "</p>" +
        (p.tema ? '<p class="speaker-tema">' + p.tema + "</p>" : "") +
        "</div>";
      spg.appendChild(card);
    });
  }

  /* ---------- lotes ---------- */
  var lotes = EV.lotes || [];
  var agora = hoje();
  var loteAtual = null, proximoLote = null;
  lotes.forEach(function (l) {
    var ini = parseDia(l.inicio), fim = parseDia(l.fim);
    if (agora >= ini && agora <= fim && !loteAtual) loteAtual = l;
    if (agora < ini && !proximoLote) proximoLote = l;
  });

  var grid = document.getElementById("lotes-grid");
  if (grid) {
    lotes.forEach(function (l) {
      var card = document.createElement("div");
      var estado = "";
      if (loteAtual === l) estado = " is-current";
      else if (agora > parseDia(l.fim)) estado = " is-past";
      card.className = "lote-card" + estado;
      var flag = loteAtual === l ? '<span class="lote-flag">Lote atual</span>' :
                 (proximoLote === l ? '<span class="lote-flag lote-flag-prox">Próximo</span>' : "");
      var periodo = l.inicio === l.fim ? fmtDia(l.inicio) : fmtDia(l.inicio) + " a " + fmtDia(l.fim);
      card.innerHTML = flag +
        '<span class="lote-nome">' + l.nome + "</span>" +
        '<span class="lote-periodo">' + periodo + "</span>" +
        '<span class="lote-preco">' + brl(l.avista) + "</span>" +
        '<span class="lote-parcelado">' + (l.parcelado ? "ou " + l.parcelado : "à vista") + "</span>" +
        (loteAtual === l && EV.checkoutUrl
          ? '<a class="btn btn-cta lote-cta" href="' + EV.checkoutUrl + '">Comprar agora</a>' : "");
      grid.appendChild(card);
    });
  }

  /* selo do topo + status */
  var badge = document.getElementById("earlybird-badge");
  var status = document.getElementById("lote-status");
  var formTitle = document.getElementById("lead-form-title");
  var diasSemana = ["domingo","segunda","terça","quarta","quinta","sexta","sábado"];
  if (loteAtual) {
    var txtAtual = loteAtual.nome + " aberto: " + brl(loteAtual.avista) + " até " + fmtDia(loteAtual.fim);
    if (badge) badge.textContent = txtAtual;
    if (status) status.textContent = "Vendas abertas no lote " + loteAtual.nome + ". O próximo lote custa mais.";
    if (formTitle) formTitle.textContent = "Receba avisos de virada de lote";
  } else if (proximoLote) {
    var ini = parseDia(proximoLote.inicio);
    var txtProx = proximoLote.nome + " abre " + diasSemana[ini.getDay()] + ", " +
                  fmtDia(proximoLote.inicio) + ", por " + brl(proximoLote.avista);
    if (badge) badge.textContent = txtProx;
    if (status) status.textContent = "As vendas abrem em " + fmtDia(proximoLote.inicio) +
      ". Deixe seu e-mail e seja avisado na hora.";
    if (formTitle) formTitle.textContent = "Avise-me quando o " + proximoLote.nome + " abrir";
  } else {
    if (status) status.textContent = "Vendas encerradas para esta edição.";
  }

  /* CTAs de ingresso: checkout se existir, senão âncora nos ingressos */
  if (EV.checkoutUrl) {
    document.querySelectorAll('[data-cta="ingresso"]').forEach(function (a) {
      a.href = EV.checkoutUrl;
    });
  }

  /* patrocínio: página própria > WhatsApp > mailto padrão */
  var pat = document.getElementById("patrocinio-cta");
  if (pat && EV.patrocinioUrl) {
    pat.href = EV.patrocinioUrl;
    pat.target = "_blank";
    pat.rel = "noopener";
  } else if (pat && EV.whatsappPatrocinio) {
    pat.href = "https://wa.me/" + EV.whatsappPatrocinio +
      "?text=" + encodeURIComponent("Olá! Quero receber o media kit de patrocínio do " + EV.nome + ".");
  }

  /* ---------- formulário de captura ---------- */
  var form = document.getElementById("lead-form");
  if (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var email = document.getElementById("lead-email");
      var fb = document.getElementById("lead-feedback");
      if (!email.value || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email.value)) {
        fb.textContent = "Confira o e-mail digitado.";
        return;
      }
      if (EV.leadFormAction) {
        var hp = document.getElementById("lead-site");
        fetch(EV.leadFormAction, {
          method: "POST",
          headers: { "content-type": "application/json" },
          body: JSON.stringify({
            email: email.value,
            origem: "site-summit-2026",
            site: hp ? hp.value : ""
          })
        })
          .then(function (r) { return r.json(); })
          .then(function (r) {
            if (r && r.ok) {
              fb.textContent = "Pronto! Você será avisado em primeira mão.";
              form.reset();
            } else {
              fb.textContent = "Confira o e-mail digitado.";
            }
          })
          .catch(function () {
            fb.textContent = "Não foi possível enviar agora. Tente novamente em instantes.";
          });
      } else {
        fb.textContent = "Cadastro ainda não configurado — defina leadFormAction em evento.config.js.";
      }
    });
  }

  /* ---------- movimento ---------- */
  var reduz = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var mobile = window.matchMedia("(max-width: 767px)").matches;
  var temGsap = typeof gsap !== "undefined" && typeof ScrollTrigger !== "undefined";

  if (reduz || mobile || !temGsap) {
    /* fallback estático: primeira cena fixa, revelações por IntersectionObserver */
    document.documentElement.classList.add("no-motion");
    if ("IntersectionObserver" in window && !reduz) {
      document.documentElement.classList.remove("no-motion");
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (en) {
          if (en.isIntersecting) { en.target.classList.add("is-in"); io.unobserve(en.target); }
        });
      }, { rootMargin: "0px 0px -10% 0px" });
      document.querySelectorAll(".reveal").forEach(function (el) { io.observe(el); });
    }
    return;
  }

  gsap.registerPlugin(ScrollTrigger);

  /* smooth scroll */
  var lenis = new Lenis({ lerp: 0.11 });
  lenis.on("scroll", ScrollTrigger.update);
  gsap.ticker.add(function (t) { lenis.raf(t * 1000); });
  gsap.ticker.lagSmoothing(0);

  /* âncoras passam pelo Lenis */
  document.querySelectorAll('a[href^="#"]').forEach(function (a) {
    a.addEventListener("click", function (e) {
      var alvo = document.querySelector(a.getAttribute("href"));
      if (alvo) { e.preventDefault(); lenis.scrollTo(alvo, { offset: -60 }); }
    });
  });

  /* sequência da abertura: crossfade + Ken Burns controlados pela rolagem */
  var cenas = gsap.utils.toArray(".hero-scene");
  if (cenas.length > 1) {
    var tl = gsap.timeline({
      scrollTrigger: {
        trigger: "#hero",
        start: "top top",
        end: "+=180%",
        pin: true,
        scrub: 0.6
      }
    });
    cenas.forEach(function (cena, i) {
      gsap.set(cena, { opacity: i === 0 ? 1 : 0 });
      tl.fromTo(cena.querySelector("img"),
        { scale: 1.0 }, { scale: 1.09, ease: "none", duration: 1 }, i);
      if (i > 0) tl.to(cena, { opacity: 1, ease: "none", duration: 0.45 }, i - 0.3);
      if (i < cenas.length - 1) tl.to(cena, { opacity: 0, ease: "none", duration: 0.45 }, i + 0.7);
    });
    /* o texto da abertura recua suavemente no fim da sequência */
    tl.to(".hero-copy", { y: -40, opacity: 0.25, ease: "none", duration: 0.8 }, cenas.length - 0.8);
  }

  /* revelações */
  gsap.utils.toArray(".reveal").forEach(function (el) {
    gsap.fromTo(el, { opacity: 0, y: 28 }, {
      opacity: 1, y: 0, duration: 0.8, ease: "power2.out",
      scrollTrigger: { trigger: el, start: "top 82%" },
      onComplete: function () { el.classList.add("is-in"); }
    });
  });
})();
