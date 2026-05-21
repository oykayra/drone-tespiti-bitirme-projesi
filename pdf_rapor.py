from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.units import cm
from datetime import datetime
import tempfile
import os


def pdf_olustur(video_adi, toplam_kare, toplam_tespit, nesne_sayaci, sure):
    tmp = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False)
    pdf_yolu = tmp.name
    tmp.close()

    doc = SimpleDocTemplate(pdf_yolu, pagesize=A4,
                            rightMargin=2*cm, leftMargin=2*cm,
                            topMargin=2*cm, bottomMargin=2*cm)

    stiller = getSampleStyleSheet()
    baslik_stili = ParagraphStyle(
        "Baslik",
        parent=stiller["Title"],
        fontSize=20,
        textColor=colors.HexColor("#FF4B4B"),
        spaceAfter=10
    )
    alt_baslik_stili = ParagraphStyle(
        "AltBaslik",
        parent=stiller["Heading2"],
        fontSize=14,
        textColor=colors.HexColor("#0068C9"),
        spaceAfter=8
    )
    normal_stili = ParagraphStyle(
        "Normal",
        parent=stiller["Normal"],
        fontSize=11,
        spaceAfter=6
    )

    icerik = []

    icerik.append(Paragraph("IHA / Drone Goruntusu Nesne Tespiti", baslik_stili))
    icerik.append(Paragraph("Analiz Raporu", alt_baslik_stili))
    icerik.append(HRFlowable(width="100%", thickness=1, color=colors.grey))
    icerik.append(Spacer(1, 0.5*cm))

    icerik.append(Paragraph("Rapor Bilgileri", alt_baslik_stili))
    bilgi_verisi = [
        ["Rapor Tarihi", datetime.now().strftime("%d.%m.%Y %H:%M")],
        ["Video Adi", video_adi],
        ["Analiz Suresi", f"{sure} saniye"],
    ]
    bilgi_tablosu = Table(bilgi_verisi, colWidths=[5*cm, 12*cm])
    bilgi_tablosu.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#F0F0F0")),
        ("TEXTCOLOR", (0, 0), (0, -1), colors.HexColor("#333333")),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 11),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("PADDING", (0, 0), (-1, -1), 8),
    ]))
    icerik.append(bilgi_tablosu)
    icerik.append(Spacer(1, 0.5*cm))

    icerik.append(Paragraph("Analiz Sonuclari", alt_baslik_stili))
    sonuc_verisi = [
        ["Toplam Kare", str(toplam_kare)],
        ["Toplam Tespit", str(toplam_tespit)],
        ["Farkli Nesne Sayisi", str(len(nesne_sayaci))],
    ]
    sonuc_tablosu = Table(sonuc_verisi, colWidths=[5*cm, 12*cm])
    sonuc_tablosu.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#F0F0F0")),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 11),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("PADDING", (0, 0), (-1, -1), 8),
    ]))
    icerik.append(sonuc_tablosu)
    icerik.append(Spacer(1, 0.5*cm))

    icerik.append(Paragraph("Tespit Edilen Nesneler", alt_baslik_stili))
    nesne_verisi = [["Nesne", "Tespit Sayisi", "Yuzde"]]
    for nesne, sayi in nesne_sayaci.items():
        yuzde = f"%{sayi / toplam_tespit * 100:.1f}"
        nesne_verisi.append([nesne, str(sayi), yuzde])

    nesne_tablosu = Table(nesne_verisi, colWidths=[6*cm, 5*cm, 6*cm])
    nesne_tablosu.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#FF4B4B")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 11),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("PADDING", (0, 0), (-1, -1), 8),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F9F9F9")]),
    ]))
    icerik.append(nesne_tablosu)
    icerik.append(Spacer(1, 1*cm))

    icerik.append(HRFlowable(width="100%", thickness=1, color=colors.grey))
    icerik.append(Spacer(1, 0.3*cm))
    icerik.append(Paragraph("Bu rapor IHA Nesne Tespiti Sistemi tarafindan otomatik olusturulmustur.", normal_stili))

    doc.build(icerik)
    return pdf_yolu