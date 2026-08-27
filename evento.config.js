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
  leadFormAction: "https://lvchpskxeohfmistppxl.supabase.co/functions/v1/summit-leads",

  // Página de patrocínio (tem prioridade sobre o WhatsApp abaixo)
  patrocinioUrl: "https://pathbusiness.github.io/sponsorship/",

  // WhatsApp comercial para patrocínio (somente dígitos, com DDI)
  whatsappPatrocinio: "",

  // Lotes: o site seleciona o lote vigente automaticamente pela data.
  lotes: [
    { nome: "Early Bird",    inicio: "2026-09-01", fim: "2026-09-30", avista: 350, parcelado: "5x R$ 70" },
    { nome: "Segundo lote",  inicio: "2026-10-01", fim: "2026-10-24", avista: 450, parcelado: "5x R$ 90" },
    { nome: "Terceiro lote", inicio: "2026-10-25", fim: "2026-11-10", avista: 550, parcelado: "5x R$ 110" },
    { nome: "Dia do evento", inicio: "2026-11-11", fim: "2026-11-11", avista: 650, parcelado: "5x R$ 130" }
  ],

  // Palestrantes 2026 — quando os retratos 800x800 chegarem, salvar em
  // site/assets/img/palestrantes/{slug}-800.webp e preencher foto: true
  palestrantes: [
    { nome: "Myrko Micali", cargo: "Empreendedor, referência em IA aplicada a negócios", empresa: "",
      tema: "IA para atendimento, marketing e vendas com toque humano",
      slug: "myrko-micali", foto: true },
    { nome: "Lucas Politi Wagner", cargo: "Account Executive", empresa: "Google Brasil",
      tema: "Google, marketing digital e IA: a jornada do viajante",
      slug: "lucas-politi-wagner", foto: true },
    { nome: "Roberto Bihari", cargo: "Presidente", empresa: "ABRAPEI",
      tema: "Painel principal: panorama do mercado de intercâmbio para 2027",
      slug: "roberto-bihari", foto: true },
    { nome: "Rodrigo Collaro", cargo: "Managing Director", empresa: "PATH",
      tema: "Mediador do painel principal",
      slug: "rodrigo-collaro", foto: true },
    { nome: "Em breve", cargo: "", empresa: "", slug: "", foto: false },
    { nome: "Em breve", cargo: "", empresa: "", slug: "", foto: false },
    { nome: "Em breve", cargo: "", empresa: "", slug: "", foto: false },
    { nome: "Em breve", cargo: "", empresa: "", slug: "", foto: false }
  ],

  // Apoiadores: os logotipos oficiais estão fixos no HTML (faixa "Apoio"),
  // arquivos em site/assets/img/marca/apoio-*.png, conforme o manual da marca.
  apoiadores: ["BELTA", "ABRAPEI", "IALC", "ALLY", "Edvisor"]
};
