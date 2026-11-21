# Probe: einige Karten auf eine A4-Seite
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import karten, json
from lib import *
S = SATZ
by = {k['id']: k for k in S['karten']}
proben = [by['bogenschuetze'], by['panzer'], by['markt'], by['land_eisen_gebirge'], by['land_oel_wueste'], S['wunder'][0], S['staaten'][1], S['ereignisse'][0], S['ereignisse'][8]]
c = canvas.Canvas('/tmp/probe.pdf', pagesize=A4)
for i, k in enumerate(proben):
    x = 10.5 * mm + (i % 3) * CW; y = 297 * mm - 16.5 * mm - (i // 3 + 1) * CH
    c.saveState(); c.translate(x, y); karten.zeichne_vorn(c, k); c.restoreState()
c.showPage()
for i, st in enumerate((1, 2, 3, 0)):
    x = 10.5 * mm + (i % 3) * CW; y = 297 * mm - 16.5 * mm - (i // 3 + 1) * CH
    c.saveState(); c.translate(x, y); karten.zeichne_ruecken(c, st); c.restoreState()
for i, (se, nr) in enumerate((('vorn', 1), ('hinten', 1))):
    x = 10.5 * mm + ((i + 4) % 3) * CW; y = 297 * mm - 16.5 * mm - ((i + 4) // 3 + 1) * CH
    c.saveState(); c.translate(x, y); karten.zeichne_hilfe(c, se, nr); c.restoreState()
c.save()
