from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import tempfile
import os
import shutil
from database import veritabani_olustur, analiz_kaydet, analizleri_getir, istatistikleri_getir, analiz_sil
from video_processor import video_isle
import time

app = FastAPI(
    title="İHA Nesne Tespiti API",
    description="Drone görüntülerinde nesne tespiti yapan REST API",
    version="1.0.0"
)

veritabani_olustur()


@app.get("/")
def ana_sayfa():
    return {
        "mesaj": "İHA Nesne Tespiti API'ye Hoşgeldiniz",
        "versiyon": "1.0.0",
        "durum": "aktif"
    }


@app.get("/istatistikler")
def istatistikleri_getir_endpoint():
    return istatistikleri_getir()


@app.get("/analizler")
def analizleri_getir_endpoint():
    return analizleri_getir()


@app.delete("/analizler/{analiz_id}")
def analiz_sil_endpoint(analiz_id: int):
    analiz_sil(analiz_id)
    return {"mesaj": f"{analiz_id} numaralı analiz silindi"}


@app.post("/analiz-et")
async def analiz_et(
    video: UploadFile = File(...),
    guven: float = 0.4,
    isi_haritasi: bool = True
):
    if not video.filename.endswith((".mp4", ".avi", ".mov")):
        raise HTTPException(status_code=400, detail="Geçersiz dosya formatı")

    with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as tmp:
        shutil.copyfileobj(video.file, tmp)
        giris_yolu = tmp.name

    try:
        baslangic = time.time()
        sonuclar = video_isle(
            giris_yolu=giris_yolu,
            guven=guven,
            isi_haritasi_goster=isi_haritasi
        )
        sure = round(time.time() - baslangic, 2)

        analiz_kaydet(
            video_adi=video.filename,
            toplam_kare=sonuclar["toplam_kare"],
            toplam_tespit=sonuclar["toplam_tespit"],
            nesne_sayaci=sonuclar["nesne_sayaci"],
            sure=sure
        )

        return {
            "durum": "basarili",
            "video_adi": video.filename,
            "toplam_kare": sonuclar["toplam_kare"],
            "toplam_tespit": sonuclar["toplam_tespit"],
            "nesne_sayaci": sonuclar["nesne_sayaci"],
            "sure": sure
        }

    finally:
        os.unlink(giris_yolu)
        if os.path.exists(sonuclar.get("video_yolu", "")):
            os.unlink(sonuclar["video_yolu"])


@app.get("/saglik")
def saglik_kontrolu():
    return {"durum": "saglikli", "servis": "IHA Nesne Tespiti API"}