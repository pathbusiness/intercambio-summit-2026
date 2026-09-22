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

  // Endpoint do formulário de captura de e-mail (Supabase Edge Function,
  // projeto Forio, função summit-leads — grava na tabela summit_leads).
  // Em produção o envio passa pelo proxy do Vercel (/api/leads → Supabase,
  // ver vercel.json), o que dispensa liberar cada domínio novo no CORS.
  // Em localhost o site usa a URL absoluta abaixo.
  leadFormAction: "/api/leads",
  leadFormActionLocal: "https://lvchpskxeohfmistppxl.supabase.co/functions/v1/summit-leads",

  // Página de patrocínio (tem prioridade sobre o WhatsApp abaixo)
  patrocinioUrl: "https://pathbusiness.github.io/sponsorship/",

  // WhatsApp comercial para patrocínio (somente dígitos, com DDI)
  whatsappPatrocinio: "",

  // Lotes: o site seleciona o lote vigente automaticamente pela data.
  // parcelado vazio = lote só à vista (o card mostra "à vista")
  lotes: [
    { nome: "Early Bird",    inicio: "2026-09-01", fim: "2026-09-30", avista: 350, parcelado: "5x R$ 70 sem juros" },
    { nome: "Segundo lote",  inicio: "2026-10-01", fim: "2026-10-24", avista: 450, parcelado: "5x R$ 90 sem juros" },
    { nome: "Terceiro lote", inicio: "2026-10-25", fim: "2026-11-10", avista: 550, parcelado: "5x R$ 110 sem juros" },
    { nome: "Dia do evento", inicio: "2026-11-11", fim: "2026-11-11", avista: 650, parcelado: "5x R$ 130 sem juros" }
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
      quem: "Mediação: Rodrigo Collaro (PATH) · Debatedores: Roberto Bihari (ABRAPEI), Alexandre Argenta (BELTA) e Elaine Martins Fuzer (e_Consulting)",
      local: "Auditório" },
    { hora: "16h00", pausa: true, titulo: "Coffee break",
      desc: "Segunda pausa para networking e troca de cartões.", local: "Foyer" },
    { hora: "16h30", tipo: "Cerimônia", destaque: "navy",
      titulo: "Prêmio Melhores Profissionais 2026",
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
    ga4Id: ""
  },

  // Apoiadores: os logotipos oficiais estão fixos no HTML (faixa "Apoio"),
  // arquivos em site/assets/img/marca/apoio-*.png, conforme o manual da marca.
  apoiadores: ["BELTA", "ABRAPEI", "IALC", "ALLY", "Edvisor"]
};
