/* =============================================================
   INTERCÂMBIO SUMMIT 2026 — CONFIGURAÇÃO DO EVENTO
   Este é o ÚNICO arquivo que precisa ser editado para:
   troca de lote, preço, prazo, link de checkout e palestrantes.
   Edite, salve, faça deploy. Nada de mexer no HTML.
   ============================================================= */
window.EVENTO = {
  nome: "Intercâmbio Summit 2026",
  data: "2026-11-11",
  dataExtenso: "11 de novembro de 2026",
  local: "Contentix",
  endereco: "Av. Paulista, 967 — 9º andar, Bela Vista",
  enderecoCompleto: "Avenida Paulista, 967 — 9º andar, Bela Vista, São Paulo/SP — CEP 01311-918",
  cidade: "São Paulo",

  // Link de checkout (Zoho Backstage).
  // Se esvaziado, o botão de compra volta a apontar para a captura de e-mail.
  checkoutUrl: "https://yourpath.zohobackstage.com/IntercambioSummit2026#/ingressos?lang=pt",

  // Checkout próprio no site (Pix e cartão via Mercado Pago, com registro
  // automático no Zoho Backstage). Com vendaNoSite = true os botões de
  // ingresso apontam para checkout.html em vez do checkoutUrl acima.
  // ATENÇÃO: os preços cobrados vêm da Edge Function summit-checkout
  // (supabase/functions/summit-checkout) — ao mudar os lotes abaixo,
  // espelhe lá e reimplante a função.
  vendaNoSite: true,
  checkoutApi: "/api/checkout",
  checkoutApiLocal: "https://ildxeqtmpbartonjoiwc.supabase.co/functions/v1/summit-checkout",

  // Endpoint do formulário de captura de e-mail (Supabase Edge Function,
  // projeto Forio, função summit-leads — grava na tabela summit_leads).
  // Em produção o envio passa pelo proxy do Vercel (/api/leads → Supabase,
  // ver vercel.json), o que dispensa liberar cada domínio novo no CORS.
  // Em localhost o site usa a URL absoluta abaixo.
  leadFormAction: "/api/leads",
  leadFormActionLocal: "https://ildxeqtmpbartonjoiwc.supabase.co/functions/v1/summit-leads",

  // Página de patrocínio (tem prioridade sobre o WhatsApp abaixo)
  patrocinioUrl: "https://pathbusiness.github.io/sponsorship/",

  // WhatsApp comercial para patrocínio (somente dígitos, com DDI)
  whatsappPatrocinio: "",

  // Votação pública do Prêmio dos Melhores Profissionais de Intercâmbio (Regulamento, etapa 3).
  // Datas em horário de Brasília; o servidor (Edge Function summit-votar) confere de novo.
  // Página: /votar (votacao.html). Endpoint: /api/votar -> summit-votar.
  // regulamentoUrl: link público do regulamento (vazio = não mostra o link).
  votacao: {
    inicio: "2026-10-01",
    fim: "2026-10-30",
    api: "/api/votar",
    apiLocal: "https://ildxeqtmpbartonjoiwc.supabase.co/functions/v1/summit-votar",
    regulamentoUrl: ""
  },

  // Lotes: o site seleciona o lote vigente automaticamente pela data.
  // parcelado vazio = lote só à vista (o card mostra "à vista")
  // Datas como foram ANUNCIADAS (Early Bird até 30/09). A prorrogação abaixo entra sozinha
  // no dia do anúncio, sem novo deploy: ver `prorrogacoes` e `lotesVigentes()`.
  lotes: [
    { nome: "Early Bird",    inicio: "2026-09-01", fim: "2026-09-30", avista: 350, parcelado: "5x R$ 70 sem juros" },
    { nome: "Segundo lote",  inicio: "2026-10-01", fim: "2026-10-24", avista: 450, parcelado: "5x R$ 90 sem juros" },
    { nome: "Terceiro lote", inicio: "2026-10-25", fim: "2026-11-10", avista: 550, parcelado: "5x R$ 110 sem juros" },
    { nome: "Dia do evento", inicio: "2026-11-11", fim: "2026-11-11", avista: 650, parcelado: "5x R$ 130 sem juros" }
  ],

  // Prorrogações: a partir do dia `anuncio` (horário local do visitante), o lote `lote` vai até `fim`
  // e o lote seguinte começa no dia depois. Até esse dia o site mostra as datas anunciadas.
  // ATENÇÃO: a função summit-checkout já cobra pelo calendário PRORROGADO (Early Bird até 02/10).
  prorrogacoes: [
    { lote: "Early Bird", anuncio: "2026-10-01", fim: "2026-10-02" }
  ],

  // Palestrantes 2026 — quando os retratos 800x800 chegarem, salvar em
  // site/assets/img/palestrantes/{slug}-800.webp e preencher foto: true
  palestrantes: [
    { nome: "Myrko Micali", cargo: "Empreendedor, referência em IA aplicada a negócios", empresa: "",
      tema: "IA para atendimento, marketing e vendas com toque humano",
      slug: "myrko-micali", foto: true },
    { nome: "Lucas Politi Wagner", cargo: "Account Executive", empresa: "Google Brasil",
      tema: "Google, IA e a gestão criativa na prática",
      slug: "lucas-politi-wagner", foto: true },
    { nome: "Gizelle Rezende", cargo: "Director of Strategic Partnerships, Americas & APAC", empresa: "The PIE",
      tema: "Tendências globais do mercado de educação internacional",
      slug: "gizelle-rezende", foto: true },
    { nome: "Roberto Bihari", cargo: "Presidente", empresa: "ABRAPEI",
      tema: "Painel principal: panorama do mercado de intercâmbio para 2027",
      slug: "roberto-bihari", foto: true },
    { nome: "Alexandre Argenta", cargo: "Presidente", empresa: "BELTA",
      tema: "Painel principal: panorama do mercado de intercâmbio para 2027",
      slug: "alexandre-argenta", foto: true },
    { nome: "Elaine Martins Fuzer", cargo: "CEO e Fundadora", empresa: "e_Consulting",
      tema: "Painel principal: panorama do mercado de intercâmbio para 2027",
      slug: "elaine-fuzer", foto: true },
    { nome: "Lucas Montani", cargo: "Managing Director LATAM", empresa: "Ollara Education Hub",
      tema: "Painel principal: panorama do mercado de intercâmbio para 2027",
      slug: "lucas-montani", foto: true },
    { nome: "Rodrigo Collaro", cargo: "Managing Director", empresa: "PATH",
      tema: "Mediador do painel principal",
      slug: "rodrigo-collaro", foto: true }
  ],

  // Programação oficial de 11 de novembro (renderizada na seção "Programação").
  // pausa: true = linha compacta cinza; destaque: "azul" | "navy" = bloco colorido.
  programacao: [
    { hora: "07h30", tipo: "Recepção", titulo: "Credenciamento & café de boas-vindas",
      desc: "Credenciamento oficial e registro dos participantes no foyer.", local: "Foyer" },
    { hora: "09h00", tipo: "Keynote", titulo: "IA para atendimento, marketing e vendas com toque humano",
      desc: "A jornada de aquisição do estudante de intercâmbio com uso de IA.",
      quem: "Myrko Micali · Empreendedor, referência em IA aplicada a negócios", local: "Auditório" },
    { hora: "09h50", pausa: true, titulo: "Coffee break",
      desc: "Pausa para networking e café no foyer.", local: "Foyer" },
    { hora: "10h20", tipo: "Painel", titulo: "Google, IA e a gestão criativa na prática",
      desc: "Ferramentas e exemplos reais para o dia a dia do mercado de viagens e intercâmbio.",
      quem: "Lucas Politi Wagner · Account Executive, Google Brasil", local: "Auditório" },
    { hora: "11h10", pausa: true, titulo: "Pausa técnica",
      desc: "Breve intervalo entre as sessões da manhã.", local: "Auditório" },
    { hora: "11h30", tipo: "Keynote", titulo: "Tendências globais do mercado de educação internacional",
      desc: "Dados globais do The PIE Insights e os deslocamentos entre destinos.",
      quem: "Gizelle Rezende · Director of Strategic Partnerships, Americas & APAC, The PIE", local: "Auditório" },
    { hora: "12h20", pausa: true, titulo: "Almoço livre",
      desc: "Consulte as opções de restaurantes locais (não incluído)." },
    { hora: "14h00", tipo: "Painel principal", destaque: "azul",
      titulo: "Panorama do mercado de intercâmbio para 2027 e uso da IA",
      desc: "Cenário do setor no Brasil pós-eleições e as tendências para o próximo ano.",
      quem: "Mediação: Rodrigo Collaro (PATH) · Debatedores: Roberto Bihari (ABRAPEI), Alexandre Argenta (BELTA), Elaine Martins Fuzer (e_Consulting) e Lucas Montani (Ollara Education Hub)",
      local: "Auditório" },
    { hora: "16h00", pausa: true, titulo: "Coffee break",
      desc: "Segunda pausa para networking e troca de cartões.", local: "Foyer" },
    { hora: "16h30", tipo: "Cerimônia", destaque: "navy",
      titulo: "Prêmio dos Melhores Profissionais de Intercâmbio 2026",
      desc: "Cerimônia oficial de premiação dos melhores do ano no setor.", local: "Auditório" },
    { hora: "18h40", tipo: "Encerramento", titulo: "Networking final",
      desc: "Encerramento das atividades e networking de fechamento.", local: "Foyer" }
  ],

  // Rastreamento de visitas e conversões. IDs vazios = desligado.
  // O rastreamento não roda em localhost (testes não sujam os dados).
  tracking: {
    // Google Tag Manager. Os eventos do site (begin_checkout, generate_lead,
    // patrocinio_click) chegam ao GTM via dataLayer.
    gtmId: "GTM-PVZLV4NW",
    // Meta Pixel do Business Manager da PATH (instalado direto no site —
    // NÃO adicione outra tag do Pixel dentro do GTM, senão dispara em dobro)
    metaPixelId: "949355509723847",
    // GA4 direto, SEM passar pelo GTM. Deixe vazio se o GA4 estiver
    // configurado dentro do GTM (o normal) — preencher os dois duplica dados.
    ga4Id: "",
    // PostHog: autocapture de cliques/pageviews + session replay + heatmap.
    // Ferramenta própria, não duplica com GTM/GA4/Meta (produtos diferentes).
    posthogKey: "phc_xh7GDxZfWq4cJuHhqYig4MLBFXchYtVcCn9ujY4EQtn4",
    posthogHost: "https://us.i.posthog.com"
  },

  // Apoiadores: os logotipos oficiais estão fixos no HTML (faixa "Apoio"),
  // arquivos em site/assets/img/marca/apoio-*.png, conforme o manual da marca.
  apoiadores: ["BELTA", "ABRAPEI", "IALC", "ALLY", "Edvisor"]
};

/* Lotes já com as prorrogações aplicadas para o dia `hoje` (Date; padrão: agora).
   Devolve cópias: o lote prorrogado ganha prorrogado:true e fimAnunciado. */
window.EVENTO.lotesVigentes = function (hoje) {
  function dia(iso) { var p = iso.split("-"); return new Date(+p[0], +p[1] - 1, +p[2]); }
  function iso(d) {
    return d.getFullYear() + "-" + ("0" + (d.getMonth() + 1)).slice(-2) + "-" + ("0" + d.getDate()).slice(-2);
  }
  var n = hoje || new Date(), d0 = new Date(n.getFullYear(), n.getMonth(), n.getDate());
  var lotes = this.lotes.map(function (l) { return Object.assign({}, l); });
  (this.prorrogacoes || []).forEach(function (p) {
    if (d0 < dia(p.anuncio)) return;
    var i = lotes.findIndex(function (l) { return l.nome === p.lote; });
    if (i < 0) return;
    lotes[i].fimAnunciado = lotes[i].fim;
    lotes[i].fim = p.fim;
    lotes[i].prorrogado = true;
    var seguinte = new Date(dia(p.fim).getTime()); seguinte.setDate(seguinte.getDate() + 1);
    for (var j = i + 1; j < lotes.length; j++) {
      if (dia(lotes[j].inicio) <= dia(p.fim)) lotes[j].inicio = iso(seguinte);
    }
  });
  return lotes;
};
