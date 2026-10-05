"""Génère le bon de commande et le catalogue PDF (tarifs repris de l'ancienne e-boutique).
Usage : pip install reportlab && python3 tools/make_pdfs.py
"""
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas

OUT = Path(__file__).resolve().parent.parent / "src" / "static" / "docs"
WINE, INK, STONE, LINE = HexColor("#7b1e2b"), HexColor("#15120f"), HexColor("#6b6158"), HexColor("#d8cfc0")
EMAIL, MOBILE = "contact@domainedesabbat.fr", "+33 6 75 48 19 74"
ADDR = "24 boulevard Carnot, 66720 Latour-de-France"

# (cuvée, millésime, appellation, couleur, prix TTC)
CUVEES = [
    ("Mi Cariña", "2023", "Vin de France", "Rouge", 14),
    ("Domaine de Sabbat Rosé", "2022", "I.G.P. Côtes Catalanes", "Rosé", 14),
    ("100 % Grenache", "2021", "I.G.P. Côtes Catalanes", "Rouge", 16),
    ("Domaine de Sabbat Rouge", "2016", "A.O.P. Côtes du Roussillon Villages", "Rouge", 16),
    ("Natural Born Syrah", "2020", "Vin de France", "Rouge", 16),
    ("Lladoner Pelut", "2020", "Vin de France", "Rouge", 18),
    ("Domaine de Sabbat Blanc", "2019", "A.O.P. Côtes du Roussillon", "Blanc", 20),
    ("Cuvée Printemps 1900'", "2018", "A.O.P. Côtes du Roussillon Villages", "Rouge", 20),
    ("Rivesaltes Tuilé", "2011", "A.O.P. Rivesaltes", "Vin doux naturel", 20),
    ("Naughty by Nature", "2018", "A.O.P. Côtes du Roussillon Villages", "Rouge", 30),
]


def header(c, title, sub):
    w, h = A4
    c.setFillColor(WINE); c.rect(0, h - 32 * mm, w, 32 * mm, stroke=0, fill=1)
    c.setFillColor(HexColor("#f6f0e6"))
    c.setFont("Times-Bold", 24); c.drawString(20 * mm, h - 16 * mm, "Domaine de Sabbat")
    c.setFont("Times-Roman", 11); c.drawString(20 * mm, h - 23 * mm, "Vins biologiques et vins nature · Vallée de l'Agly · Roussillon")
    c.setFillColor(INK); c.setFont("Times-Bold", 20); c.drawString(20 * mm, h - 46 * mm, title)
    c.setFillColor(STONE); c.setFont("Helvetica", 9); c.drawString(20 * mm, h - 52 * mm, sub)


def footer(c):
    c.setFillColor(STONE); c.setFont("Helvetica", 8)
    c.drawCentredString(A4[0] / 2, 12 * mm, f"Domaine de Sabbat · Sylvain Lejeune · {ADDR} · {MOBILE} · {EMAIL}")


def order_form():
    c = canvas.Canvas(str(OUT / "bon-de-commande.pdf"), pagesize=A4)
    c.setTitle("Bon de commande — Domaine de Sabbat")
    w, h = A4
    header(c, "Bon de commande", f"À renvoyer par e-mail à {EMAIL}")
    y = h - 62 * mm
    c.setFillColor(INK); c.setFont("Helvetica", 9)
    for lab in ("Nom / Société :", "Adresse de livraison :", "Téléphone (obligatoire) :", "E-mail :"):
        c.drawString(20 * mm, y, lab); c.setStrokeColor(LINE); c.line(62 * mm, y - 1.5, w - 20 * mm, y - 1.5); y -= 8 * mm
    y -= 2 * mm
    cols = [20 * mm, 92 * mm, 140 * mm, 160 * mm, w - 20 * mm]
    c.setFillColor(WINE); c.rect(cols[0], y - 2 * mm, cols[4] - cols[0], 7 * mm, stroke=0, fill=1)
    c.setFillColor(HexColor("#f6f0e6")); c.setFont("Helvetica-Bold", 8.5)
    c.drawString(cols[0] + 2 * mm, y, "Cuvée"); c.drawString(cols[1] + 2 * mm, y, "Appellation")
    c.drawRightString(cols[3] - 2 * mm, y, "Prix TTC"); c.drawString(cols[3] + 2 * mm, y, "Quantité")
    y -= 9 * mm
    for name, vint, app, col, price in CUVEES:
        c.setFillColor(INK); c.setFont("Helvetica-Bold", 8.5); c.drawString(cols[0] + 2 * mm, y, f"{name} {vint}")
        c.setFont("Helvetica", 7.5); c.setFillColor(STONE); c.drawString(cols[1] + 2 * mm, y, app)
        c.setFillColor(INK); c.setFont("Helvetica", 9); c.drawRightString(cols[3] - 2 * mm, y, f"{price:.2f} €".replace(".", ","))
        c.setStrokeColor(LINE); c.rect(cols[3] + 2 * mm, y - 2 * mm, 20 * mm, 7 * mm, stroke=1, fill=0)
        c.line(cols[0], y - 3.5 * mm, cols[4], y - 3.5 * mm) if False else None
        y -= 10 * mm
    y -= 2 * mm
    c.setFont("Helvetica", 9); c.setFillColor(INK)
    c.drawString(20 * mm, y, "Commentaire / digicode :"); c.line(62 * mm, y - 1.5, w - 20 * mm, y - 1.5)
    y -= 12 * mm
    c.setFont("Helvetica-Bold", 9); c.drawString(20 * mm, y, "Conditions")
    c.setFont("Helvetica", 8.5)
    for t in ("Minimum de 6 bouteilles par commande. Livraison en France métropolitaine uniquement.",
              "Paiement : chèque bancaire ou virement (demander un RIB). La commande est expédiée dès réception du règlement.",
              "Délai de réception d'environ 4 à 6 jours ouvrés. Vins garantis contre la casse lors du transport.",
              "Tarifs TTC par bouteille de 75 cl, indicatifs et susceptibles d'évoluer selon les stocks et millésimes."):
        y -= 5 * mm; c.drawString(20 * mm, y, "• " + t)
    footer(c); c.showPage(); c.save()


def catalog():
    c = canvas.Canvas(str(OUT / "catalogue-cuvees.pdf"), pagesize=A4)
    c.setTitle("Catalogue des cuvées — Domaine de Sabbat")
    w, h = A4
    header(c, "Nos cuvées", "Tarifs TTC par bouteille de 75 cl")
    y = h - 66 * mm
    for name, vint, app, col, price in CUVEES:
        c.setFillColor(INK); c.setFont("Times-Bold", 14); c.drawString(20 * mm, y, f"{name} {vint}")
        c.setFillColor(WINE); c.setFont("Times-Bold", 14); c.drawRightString(w - 20 * mm, y, f"{price:.2f} €".replace(".", ","))
        c.setFillColor(STONE); c.setFont("Helvetica", 9); c.drawString(20 * mm, y - 5.5 * mm, f"{col} · {app}")
        c.setStrokeColor(LINE); c.line(20 * mm, y - 9 * mm, w - 20 * mm, y - 9 * mm)
        y -= 17 * mm
    c.setFillColor(INK); c.setFont("Helvetica", 9)
    c.drawString(20 * mm, y, f"Commandes : bon de commande à renvoyer à {EMAIL} ou par téléphone au {MOBILE}.")
    footer(c); c.showPage(); c.save()


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    order_form(); catalog()
