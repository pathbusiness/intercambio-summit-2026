#!/usr/bin/env python3
"""Gera os certificados de participação do Intercâmbio Summit 2026 (um PDF por pessoa).

Uso:
  python3 gerar.py --amostra "Nome Sobrenome"         # um certificado de teste em saida/amostra.pdf
  python3 gerar.py checkin.csv                         # todos do CSV de check-in do Backstage
Saída: saida/<codigo>.pdf e saida/links.csv (nome, e-mail, código, link) para importar no Zoho.
O código é derivado do e-mail com um segredo local (.segredo); o PDF só é achado por quem tem o link.
"""
import argparse, csv, hashlib, hmac, html, os, secrets, shutil, subprocess, sys, tempfile, unicodedata
from pathlib import Path

AQUI = Path(__file__).resolve().parent
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
BASE_URL = "https://intercambiosummit.com.br/certificados"

def segredo() -> bytes:
    f = AQUI / ".segredo"
    if not f.exists():
        f.write_text(secrets.token_hex(32))
    return f.read_text().strip().encode()

def codigo(email: str) -> str:
    return hmac.new(segredo(), email.strip().lower().encode(), hashlib.sha256).hexdigest()[:14]

def titulo(nome: str) -> str:
    # "MARIA da SILVA" -> "Maria da Silva", preservando partículas
    mini = {"da", "de", "do", "das", "dos", "e"}
    partes = nome.strip().split()
    return " ".join(p.lower() if i and p.lower() in mini else p[:1].upper() + p[1:].lower() for i, p in enumerate(partes))

def pdf(nome: str, cod: str, destino: Path):
    modelo = (AQUI / "modelo.html").read_text(encoding="utf-8")
    pagina = modelo.replace("{{NOME}}", html.escape(nome)).replace("{{CODIGO}}", cod.upper())
    tmp = AQUI / f"_tmp_{cod}.html"
    tmp.write_text(pagina, encoding="utf-8")
    perfil = tempfile.mkdtemp(prefix="cert-chrome-")  # perfil próprio: não briga com o Chrome aberto
    try:
        for tentativa in range(3):
            r = subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                                f"--user-data-dir={perfil}", f"--print-to-pdf={destino}", tmp.as_uri()],
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=90)
            if r.returncode == 0 and destino.exists():
                return
        raise RuntimeError(f"Chrome falhou ao gerar {destino.name}")
    finally:
        tmp.unlink(missing_ok=True)
        shutil.rmtree(perfil, ignore_errors=True)

def achar(cabecalho, *opcoes):
    norm = lambda s: unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower().strip()
    for i, c in enumerate(cabecalho):
        if any(norm(c) == o or o in norm(c) for o in opcoes):
            return i
    return None

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv", nargs="?")
    ap.add_argument("--amostra")
    a = ap.parse_args()
    saida = AQUI / "saida"; saida.mkdir(exist_ok=True)
    if a.amostra:
        pdf(a.amostra, codigo("amostra@exemplo.test"), saida / "amostra.pdf"); print("saida/amostra.pdf"); return
    if not a.csv:
        sys.exit("Informe o CSV de check-in ou use --amostra.")
    with open(a.csv, newline="", encoding="utf-8-sig") as f:
        amostra = f.read(4096); f.seek(0)
        dialeto = csv.Sniffer().sniff(amostra, delimiters=",;\t")
        linhas = list(csv.reader(f, dialeto))
    cab, dados = linhas[0], linhas[1:]
    i_nome, i_sob, i_mail = achar(cab, "primeiro nome", "first name", "nome"), achar(cab, "sobrenome", "last name"), achar(cab, "email", "e-mail")
    if i_mail is None or i_nome is None:
        sys.exit(f"Não achei nome/e-mail no cabeçalho: {cab}")
    vistos, links = set(), []
    for l in dados:
        mail = l[i_mail].strip().lower()
        if not mail or mail in vistos:
            continue
        vistos.add(mail)
        nome = titulo(f"{l[i_nome]} {l[i_sob] if i_sob is not None else ''}".strip())
        cod = codigo(mail)
        pdf(nome, cod, saida / f"{cod}.pdf")
        links.append([nome, mail, cod, f"{BASE_URL}/{cod}.pdf"])
        print("ok", nome)
    with open(saida / "links.csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f); w.writerow(["nome", "email", "codigo", "link_certificado"]); w.writerows(links)
    print(f"{len(links)} certificados em {saida}")

main()
