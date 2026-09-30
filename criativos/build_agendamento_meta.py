#!/usr/bin/env python3
"""Planilha de agendamento da campanha para o Meta Business Suite.

Lê criativos/out/campanha-outubro/ (uma pasta por publicação: artes, legenda.txt ou
nota.txt) e gera AGENDAMENTO-META.xlsx com uma linha por publicação: data, hora,
formato, arquivos na ordem de upload, legenda pronta para colar, como publicar e
dependências. Também gera um .zip por semana (artes + textos), abaixo de 30 MB.

Regra da casa: NADA é agendado sem aprovação explícita do Rodrigo, com arte e legenda exatas.

Uso: python3 criativos/build_agendamento_meta.py [pasta_de_saida_dos_zips]
"""
import datetime as dt
import glob
import os
import sys
import zipfile

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "out", "campanha-outubro")
DIAS = ["seg", "ter", "qua", "qui", "sex", "sáb", "dom"]

# depende de / observações por slug
DEPENDE = {
    "premio-como-funciona": "Publicar o adendo ao Regulamento antes (ou junto). Confirmar as 3 pendências da minuta.",
    "eb-ainda-350": "Último dia do Early Bird (decisão do Rodrigo).",
    "story-eb-ainda-350": "Último dia do Early Bird (decisão do Rodrigo).",
    "eb-prorrogado": "Só a partir de 01/10: anuncia a prorrogação até 02/10.",
    "story-eb-prorrogado": "Só a partir de 01/10: anuncia a prorrogação até 02/10.",
    "eb-ultimo-dia": "Vale porque o Early Bird prorrogado termina em 02/10 (23h59).",
    "story-eb-ultimo-dia": "Vale porque o Early Bird prorrogado termina em 02/10 (23h59).",
    "votacao-aberta": "Votação abre 01/10 00:00. Site com /votar no ar (merge feito).",
    "story-votacao-aberta": "Votação abre 01/10 00:00. Site com /votar no ar (merge feito).",
    "reel-premio": "Reel sem áudio: escolher a trilha no app.",
    "reel-ia-perguntas": "Reel sem áudio: escolher a trilha no app.",
}


def arquivos_da_pasta(pasta):
    return sorted(f for f in os.listdir(pasta) if f.startswith("SUMMIT-") and f.rsplit(".", 1)[-1] in ("jpg", "png", "mp4"))


def ler(pasta, nome):
    p = os.path.join(pasta, nome)
    return open(p, encoding="utf-8").read().strip() if os.path.exists(p) else ""


def linhas():
    out = []
    for pasta in sorted(glob.glob(os.path.join(SRC, "2026-*"))):
        nome = os.path.basename(pasta)
        data, slug = nome[:10], nome[11:]
        arqs = arquivos_da_pasta(pasta)
        # hora e formato vêm do CALENDARIO.md
        out.append(dict(data=data, slug=slug, pasta=nome, arqs=arqs,
                        legenda=ler(pasta, "legenda.txt"), nota=ler(pasta, "nota.txt")))
    cal = {}
    for ln in open(os.path.join(SRC, "CALENDARIO.md"), encoding="utf-8"):
        c = [x.strip() for x in ln.strip().strip("|").split("|")]
        if len(c) >= 6 and c[0].startswith("2026-"):
            cal[(c[0], c[4])] = (c[2], c[3])
    for r in out:
        r["hora"], r["formato"] = cal[(r["data"], r["slug"])]
    return sorted(out, key=lambda r: (r["data"], r["hora"], r["slug"]))


def como_publicar(r):
    if r["formato"] == "story":
        n = r["nota"].lower()
        if n.startswith("sem sticker") or n.startswith("opcional"):
            return "Business Suite (Story agendado)"
        return "App do Instagram, no dia (precisa de sticker)"
    if r["formato"] == "reel":
        return "Business Suite (Reel agendado); trilha pelo app"
    return "Business Suite (Feed agendado)"


def main():
    dados = linhas()
    wb = Workbook()
    ws = wb.active
    ws.title = "Agenda"
    cab = ["#", "Data", "Dia", "Hora", "Formato", "Peça", "Arquivos (ordem de upload)", "Pasta",
           "Legenda (colar)", "Nota / sticker", "Como publicar", "Depende de / atenção", "Agendado? (marque)"]
    ws.append(cab)
    azul = PatternFill("solid", fgColor="0044B9")
    for c in ws[1]:
        c.font = Font(bold=True, color="FFFFFF"); c.fill = azul
        c.alignment = Alignment(vertical="center", wrap_text=True)
    formato_pt = {"carrossel": "Carrossel", "feed": "Feed", "reel": "Reel", "story": "Story"}
    for i, r in enumerate(dados, 1):
        d = dt.date.fromisoformat(r["data"])
        aviso = DEPENDE.get(r["slug"], "")
        if r["data"] <= "2026-09-29":
            aviso = ("Data já passou: só publicar à mão se ainda fizer sentido. " + aviso).strip()
        ws.append([i, d.strftime("%d/%m/%Y"), DIAS[d.weekday()], r["hora"].replace("h", ":"),
                   formato_pt.get(r["formato"], r["formato"]), r["slug"], "\n".join(r["arqs"]), r["pasta"],
                   r["legenda"], r["nota"], como_publicar(r), aviso, ""])
    larg = [5, 12, 6, 7, 11, 28, 46, 34, 70, 40, 34, 46, 14]
    for i, w in enumerate(larg, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    for row in ws.iter_rows(min_row=2):
        for c in row:
            c.alignment = Alignment(vertical="top", wrap_text=True)
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = ws.dimensions

    g = wb.create_sheet("Como agendar")
    passos = [
        "COMO AGENDAR NO META BUSINESS SUITE (confira os nomes dos botões, que a Meta muda de vez em quando)",
        "",
        "Antes de começar",
        "1. Entre em business.facebook.com e abra o Meta Business Suite com a conta do Instagram @intercambiosummit conectada.",
        "2. Confira o fuso horário da conta (Brasília) e que o link da bio é intercambiosummit.com.br (as legendas dizem 'link na bio').",
        "3. Baixe o .zip da semana e abra a planilha 'Agenda'. Cada linha é uma publicação: a pasta tem as artes e a legenda.",
        "4. Só agende o que você aprovou: veja a arte e a legenda exatas antes. Se algo mudar, me avise que eu ajusto.",
        "",
        "Feed e carrossel",
        "1. Criar publicação > Feed do Instagram.",
        "2. Envie os arquivos na ordem da coluna 'Arquivos' (o -01 é a capa; o penúltimo/último é o slide de parceiros e o de chamada).",
        "3. Cole a legenda da coluna 'Legenda' (ela já traz as hashtags; máx. 2.200 caracteres, e todas estão abaixo de 800).",
        "4. Em agendamento, escolha 'Agendar' e informe a data e a hora da planilha. Confirme.",
        "",
        "Reel",
        "1. Criar reel, envie o .mp4 (12 s, sem áudio), cole a legenda, agende.",
        "2. Os reels não têm trilha. Escolha uma em alta pelo app do Instagram, ou publique o reel pelo app para incluir o áudio.",
        "",
        "Story",
        "1. Criar story, envie a arte 1080x1920 e agende (a coluna 'Como publicar' diz quais dá para agendar).",
        "2. Stories com enquete, caixa de perguntas, link ou lembrete precisam do sticker: publique pelo app do Instagram no horário.",
        "   O Business Suite não coloca sticker interativo; se o seu permitir, siga a coluna 'Nota / sticker'.",
        "",
        "Depois de agendar",
        "1. Marque 'Agendado?' na planilha. O Planner do Business Suite mostra o calendário para conferir.",
        "2. Se um post depende de algo ('Depende de'), só agende depois de resolver: 06/10 espera o adendo ao Regulamento.",
        "3. Prorrogação do Early Bird: o post de 01/10 só vale a partir de 01/10; o de 30/09 é 'último dia'.",
        "4. O agendamento prévio no Business Suite tem limite de dias à frente; se o seu não deixar agendar tudo, faça por blocos.",
    ]
    for ln in passos:
        g.append([ln])
    g.column_dimensions["A"].width = 130
    for row in g.iter_rows():
        row[0].alignment = Alignment(wrap_text=True, vertical="top")
        if row[0].value and not str(row[0].value).startswith((" ", "1", "2", "3", "4")) and row[0].value.strip():
            row[0].font = Font(bold=True)

    saida = sys.argv[1] if len(sys.argv) > 1 else SRC
    os.makedirs(saida, exist_ok=True)
    xlsx = os.path.join(SRC, "AGENDAMENTO-META.xlsx")
    wb.save(xlsx)

    # um zip por semana (segunda a domingo; a 1ª semana começa em 29/09)
    def semana(dstr):
        d = dt.date.fromisoformat(dstr)
        ini = d - dt.timedelta(days=d.weekday())
        return max(ini, dt.date(2026, 9, 29))
    grupos = {}
    for r in dados:
        grupos.setdefault(semana(r["data"]), []).append(r)
    zips = []
    for ini, rs in sorted(grupos.items()):
        fim = max(dt.date.fromisoformat(r["data"]) for r in rs)
        nome = f"Meta-{ini.strftime('%d-%m')}-a-{fim.strftime('%d-%m')}.zip"
        caminho = os.path.join(saida, nome)
        with zipfile.ZipFile(caminho, "w", zipfile.ZIP_STORED) as z:
            for r in rs:
                for f in sorted(os.listdir(os.path.join(SRC, r["pasta"]))):
                    z.write(os.path.join(SRC, r["pasta"], f), f"{r['pasta']}/{f}")
        zips.append((caminho, os.path.getsize(caminho) / 1e6))
    print(f"{len(dados)} publicações; planilha: {xlsx}")
    for c, mb in zips:
        print(f"  {os.path.basename(c)}  {mb:.1f} MB")


if __name__ == "__main__":
    main()
