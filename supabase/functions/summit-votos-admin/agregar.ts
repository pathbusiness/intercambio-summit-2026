// Agregações do painel de acompanhamento da votação (funções puras, testáveis em Node).
export type Voto = {
  categoria: string;
  finalista: string;
  nome: string;
  email: string;
  email_orig: string;
  empresa: string;
  tipo_empresa: string;
  ip_hash: string | null;
  status: string;
  motivo: string | null;
  created_at: string;
};

export const LIMITE_SUSPEITO = 5; // e-mails distintos na mesma conexão

// "AAAA-MM-DD" no fuso de São Paulo
export function diaSP(iso: string): string {
  return new Intl.DateTimeFormat("en-CA", {
    timeZone: "America/Sao_Paulo", year: "numeric", month: "2-digit", day: "2-digit",
  }).format(new Date(iso));
}

export function agregar(votos: Voto[]) {
  const validos = votos.filter((v) => v.status === "valido");
  const eleitores = new Set(validos.map((v) => v.email));

  const porTipo: Record<string, Set<string>> = { agencia: new Set(), instituicao: new Set() };
  for (const v of validos) (porTipo[v.tipo_empresa] ??= new Set()).add(v.email);

  const contagem = new Map<string, Map<string, number>>();
  for (const v of validos) {
    const cat = contagem.get(v.categoria) ?? new Map<string, number>();
    cat.set(v.finalista, (cat.get(v.finalista) ?? 0) + 1);
    contagem.set(v.categoria, cat);
  }
  const ranking: Record<string, { finalista: string; votos: number }[]> = {};
  for (const [cat, m] of contagem) {
    ranking[cat] = [...m].map(([finalista, votos]) => ({ finalista, votos }))
      .sort((a, b) => b.votos - a.votos || a.finalista.localeCompare(b.finalista));
  }

  const dias = new Map<string, { votos: number; eleitores: Set<string> }>();
  for (const v of validos) {
    const d = diaSP(v.created_at);
    const x = dias.get(d) ?? { votos: 0, eleitores: new Set<string>() };
    x.votos++; x.eleitores.add(v.email);
    dias.set(d, x);
  }
  const porDia = [...dias].map(([dia, x]) => ({ dia, votos: x.votos, eleitores: x.eleitores.size }))
    .sort((a, b) => a.dia.localeCompare(b.dia));

  const ips = new Map<string, { emails: Set<string>; votos: number; empresas: Set<string> }>();
  for (const v of validos) {
    if (!v.ip_hash) continue;
    const x = ips.get(v.ip_hash) ?? { emails: new Set<string>(), votos: 0, empresas: new Set<string>() };
    x.emails.add(v.email); x.votos++; x.empresas.add(v.empresa);
    ips.set(v.ip_hash, x);
  }
  const suspeitos = [...ips]
    .filter(([, x]) => x.emails.size >= LIMITE_SUSPEITO)
    .map(([ip, x]) => ({ conexao: ip.slice(0, 8), emails: x.emails.size, votos: x.votos, empresas: x.empresas.size }))
    .sort((a, b) => b.emails - a.emails);

  const recentes = [...votos]
    .sort((a, b) => b.created_at.localeCompare(a.created_at))
    .slice(0, 50)
    .map((v) => ({
      quando: v.created_at, nome: v.nome, email: v.email_orig || v.email, empresa: v.empresa,
      tipo: v.tipo_empresa, categoria: v.categoria, finalista: v.finalista, status: v.status,
    }));

  return {
    totais: {
      votos_validos: validos.length,
      votos_invalidados: votos.length - validos.length,
      eleitores: eleitores.size,
      eleitores_agencia: porTipo.agencia.size,
      eleitores_instituicao: porTipo.instituicao.size,
    },
    ranking, por_dia: porDia, suspeitos, recentes,
  };
}

// CSV com todos os votos (Excel BR: separador ";" e BOM aplicado no cliente)
export function paraCsv(votos: Voto[]): string {
  const cab = ["data_hora", "categoria", "finalista", "nome", "email", "empresa", "tipo", "status", "motivo"];
  const cel = (t: unknown) => {
    let s = String(t ?? "");
    if (/^[=+\-@\t\r]/.test(s)) s = "'" + s; // evita injeção de fórmula ao abrir no Excel
    return '"' + s.replace(/"/g, '""') + '"';
  };
  const linhas = [...votos].sort((a, b) => a.created_at.localeCompare(b.created_at)).map((v) =>
    [v.created_at, v.categoria, v.finalista, v.nome, v.email_orig || v.email, v.empresa, v.tipo_empresa, v.status, v.motivo]
      .map(cel).join(";"));
  return [cab.join(";"), ...linhas].join("\r\n");
}
