// Regras da votação, sem dependências de runtime (testável em Node e Deno).
import { FINALISTAS, TRILHA } from "./finalistas.ts";

export type Tipo = "agencia" | "instituicao";
export type Voto = { categoria: string; finalista: string };
export type Erro = { ok: false; status: number; erro: string; detalhe?: string };
export type Ok = {
  ok: true;
  dados: { nome: string; email: string; emailOrig: string; empresa: string; tipo: Tipo; votos: Voto[] };
};

// Quem é de agência vota nas categorias de instituições e vice-versa (como na 1ª etapa).
const TRILHA_ELEGIVEL: Record<Tipo, string> = { agencia: "Instituições", instituicao: "Agências" };

const DESCARTAVEIS = new Set([
  "mailinator.com", "guerrillamail.com", "10minutemail.com", "tempmail.com", "temp-mail.org",
  "yopmail.com", "trashmail.com", "sharklasers.com", "getnada.com", "dispostable.com",
  "maildrop.cc", "throwawaymail.com", "fakeinbox.com",
]);

export function normalizarEmail(bruto: string): string {
  const e = bruto.trim().toLowerCase();
  const [local, dominio] = e.split("@");
  if (dominio === "gmail.com" || dominio === "googlemail.com") {
    return local.split("+")[0].replaceAll(".", "") + "@gmail.com";
  }
  return e;
}

export function janela(agora: Date, inicio: Date, fim: Date): "antes" | "aberta" | "depois" {
  if (agora < inicio) return "antes";
  if (agora > fim) return "depois";
  return "aberta";
}

export function validar(body: Record<string, unknown>): Ok | Erro {
  const nome = String(body.nome ?? "").trim().replace(/\s+/g, " ");
  const empresa = String(body.empresa ?? "").trim().replace(/\s+/g, " ");
  const emailOrig = String(body.email ?? "").trim().slice(0, 254);
  const tipo = body.tipo as Tipo;

  if (nome.length < 3 || nome.length > 80 || !nome.includes(" "))
    return { ok: false, status: 400, erro: "nome", detalhe: "Informe nome e sobrenome." };
  if (empresa.length < 2 || empresa.length > 100)
    return { ok: false, status: 400, erro: "empresa", detalhe: "Informe a empresa ou instituição." };
  if (!/^[^@\s]+@[^@\s]+\.[^@\s]{2,}$/.test(emailOrig))
    return { ok: false, status: 400, erro: "email", detalhe: "E-mail inválido." };
  const email = normalizarEmail(emailOrig);
  if (DESCARTAVEIS.has(email.split("@")[1]))
    return { ok: false, status: 400, erro: "email", detalhe: "Use um e-mail profissional." };
  if (tipo !== "agencia" && tipo !== "instituicao")
    return { ok: false, status: 400, erro: "tipo", detalhe: "Informe se você é de agência ou instituição." };

  const bruto = body.votos;
  if (!bruto || typeof bruto !== "object" || Array.isArray(bruto))
    return { ok: false, status: 400, erro: "votos", detalhe: "Escolha ao menos um finalista." };
  const votos: Voto[] = [];
  for (const [categoria, finalista] of Object.entries(bruto as Record<string, unknown>)) {
    if (!(categoria in TRILHA) || typeof finalista !== "string" || FINALISTAS[finalista] !== categoria)
      return { ok: false, status: 400, erro: "voto_invalido", detalhe: categoria };
    if (TRILHA[categoria] !== TRILHA_ELEGIVEL[tipo])
      return { ok: false, status: 403, erro: "elegibilidade", detalhe: categoria };
    votos.push({ categoria, finalista });
  }
  if (votos.length === 0)
    return { ok: false, status: 400, erro: "votos", detalhe: "Escolha ao menos um finalista." };

  return { ok: true, dados: { nome: nome.slice(0, 80), email, emailOrig, empresa: empresa.slice(0, 100), tipo, votos } };
}
