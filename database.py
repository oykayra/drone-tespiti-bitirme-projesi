import sqlite3
import json
from datetime import datetime
from config import VERITABANI_ADI


def veritabani_olustur():
    baglanti = sqlite3.connect(VERITABANI_ADI)
    imleç = baglanti.cursor()
    imleç.execute("""
        CREATE TABLE IF NOT EXISTS analizler (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tarih TEXT,
            video_adi TEXT,
            toplam_kare INTEGER,
            toplam_tespit INTEGER,
            nesne_sayaci TEXT,
            sure REAL,
            video_yolu TEXT
        )
    """)
    baglanti.commit()
    baglanti.close()


def analiz_kaydet(video_adi, toplam_kare, toplam_tespit, nesne_sayaci, sure, video_yolu=None):
    baglanti = sqlite3.connect(VERITABANI_ADI)
    imleç = baglanti.cursor()
    imleç.execute("""
        INSERT INTO analizler (tarih, video_adi, toplam_kare, toplam_tespit, nesne_sayaci, sure, video_yolu)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        video_adi,
        toplam_kare,
        toplam_tespit,
        json.dumps(nesne_sayaci),
        sure,
        video_yolu
    ))
    baglanti.commit()
    baglanti.close()


def analizleri_getir():
    baglanti = sqlite3.connect(VERITABANI_ADI)
    imleç = baglanti.cursor()
    imleç.execute("SELECT * FROM analizler ORDER BY id DESC")
    satirlar = imleç.fetchall()
    baglanti.close()

    sonuclar = []
    for satir in satirlar:
        sonuclar.append({
            "id": satir[0],
            "tarih": satir[1],
            "video_adi": satir[2],
            "toplam_kare": satir[3],
            "toplam_tespit": satir[4],
            "nesne_sayaci": json.loads(satir[5]),
            "sure": satir[6],
            "video_yolu": satir[7] if len(satir) > 7 else None
        })
    return sonuclar


def analiz_sil(analiz_id):
    baglanti = sqlite3.connect(VERITABANI_ADI)
    imleç = baglanti.cursor()
    imleç.execute("SELECT video_yolu FROM analizler WHERE id = ?", (analiz_id,))
    satir = imleç.fetchone()
    if satir and satir[0]:
        import os
        if os.path.exists(satir[0]):
            os.unlink(satir[0])
    imleç.execute("DELETE FROM analizler WHERE id = ?", (analiz_id,))
    baglanti.commit()
    baglanti.close()


def istatistikleri_getir():
    baglanti = sqlite3.connect(VERITABANI_ADI)
    imleç = baglanti.cursor()
    imleç.execute("SELECT COUNT(*) FROM analizler")
    toplam_analiz = imleç.fetchone()[0]
    imleç.execute("SELECT SUM(toplam_tespit) FROM analizler")
    toplam_tespit = imleç.fetchone()[0] or 0
    imleç.execute("SELECT SUM(toplam_kare) FROM analizler")
    toplam_kare = imleç.fetchone()[0] or 0
    baglanti.close()

    return {
        "toplam_analiz": toplam_analiz,
        "toplam_tespit": toplam_tespit,
        "toplam_kare": toplam_kare
    }