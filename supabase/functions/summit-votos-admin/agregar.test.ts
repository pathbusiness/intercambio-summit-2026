// node --experimental-strip-types --no-warnings agregar.test.ts
import assert from "node:assert/strict";
import { agregar, paraCsv, diaSP, type Voto } from "./agregar.ts";

const v = (o: Partial<Voto>): Voto => ({
  categoria: "conector", finalista: "a", nome: "N", email: "x@y.com", email_orig: "x@y.com", empresa: "E",
  tipo_empresa: "agencia", ip_hash: "ip1", status: "valido", motivo: null, created_at: "2026-10-01T12:00:00Z", ...o,
});

// dia em Brasília: 01/10 02:30 UTC ainda é 30/09 à noite
assert.equal(diaSP("2026-10-01T02:30:00Z"), "2026-09-30");
assert.equal(diaSP("2026-10-01T03:00:00Z"), "2026-10-01");

const base = [
  v({ email: "a@x.com", finalista: "a" }),
  v({ email: "b@x.com", finalista: "b" }),
  v({ email: "c@x.com", finalista: "a", tipo_empresa: "instituicao" }),
  v({ email: "c@x.com", categoria: "iniciativa", finalista: "z", tipo_empresa: "instituicao" }),
  v({ email: "d@x.com", finalista: "b", status: "invalidado", motivo: "dup" }),
];
const r = agregar(base);
assert.deepEqual(r.totais, { votos_validos: 4, votos_invalidados: 1, eleitores: 3, eleitores_agencia: 2, eleitores_instituicao: 1 });
assert.deepEqual(r.ranking.conector, [{ finalista: "a", votos: 2 }, { finalista: "b", votos: 1 }]); // invalidado não conta
assert.equal(r.por_dia.length, 1);
assert.deepEqual(r.por_dia[0], { dia: "2026-10-01", votos: 4, eleitores: 3 });
assert.equal(r.suspeitos.length, 0); // 3 e-mails no mesmo IP < 5
assert.equal(r.recentes.length, 5);

const muitos = Array.from({ length: 6 }, (_, i) => v({ email: `u${i}@x.com`, ip_hash: "ipsuspeito123" }));
const s = agregar(muitos).suspeitos;
assert.deepEqual(s, [{ conexao: "ipsuspei", emails: 6, votos: 6, empresas: 1 }]);

const csv = paraCsv([v({ nome: '=HYPERLINK("x")', empresa: 'A "B"; C' })]);
assert.ok(csv.includes(`"'=HYPERLINK(""x"")"`)); // fórmula neutralizada
assert.ok(csv.includes('"A ""B""; C"'));
assert.equal(agregar([]).totais.eleitores, 0);
console.log("agregar.test.ts: ok");
