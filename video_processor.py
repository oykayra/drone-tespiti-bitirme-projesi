import cv2
import numpy as np
import tempfile
import os
import subprocess
from collections import Counter
from detector import DroneDetector, renk_uret

VIDEOS_KLASORU = r"C:\Users\Öykü Kayra\drone_tespiti\videos"


def video_isle(giris_yolu, guven=0.4, isi_haritasi_goster=True, ilerleme_callback=None, video_kaydet=True):
    dedektör = DroneDetector(guven=guven)

    cap = cv2.VideoCapture(giris_yolu)
    genislik = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    yukseklik = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    toplam_kare = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    isi_haritasi = np.zeros((yukseklik, genislik), dtype=np.float32)
    tum_kareler = []
    tum_tespitler = []
    kare_sayisi = 0

    while True:
        ret, kare = cap.read()
        if not ret:
            break
        tum_kareler.append(kare.copy())
        sonuclar = dedektör.model(kare, conf=guven, verbose=False)
        kare_tespitler = []
        for kutu in sonuclar[0].boxes:
            x1, y1, x2, y2 = map(int, kutu.xyxy[0])
            sinif_id = int(kutu.cls[0])
            guven_skoru = float(kutu.conf[0])
            sinif_adi = dedektör.sinif_isimleri[sinif_id]
            isi_haritasi[y1:y2, x1:x2] += 1
            kare_tespitler.append({
                "sinif": sinif_adi,
                "sinif_id": sinif_id,
                "guven": guven_skoru,
                "kutu": (x1, y1, x2, y2)
            })
        tum_tespitler.append(kare_tespitler)
        kare_sayisi += 1
        if ilerleme_callback and toplam_kare > 0:
            ilerleme_callback(
                kare_sayisi / toplam_kare / 2,
                f"Adım 1/2 — Analiz ediliyor: {kare_sayisi}/{toplam_kare}"
            )

    cap.release()

    isi_normalize = cv2.normalize(isi_haritasi, None, 0, 255, cv2.NORM_MINMAX)
    isi_normalize = np.uint8(isi_normalize)
    isi_renkli = cv2.applyColorMap(isi_normalize, cv2.COLORMAP_JET)
    isi_renkli = cv2.resize(isi_renkli, (genislik, yukseklik))

    avi_tmp = tempfile.NamedTemporaryFile(suffix=".avi", delete=False)
    avi_yolu = avi_tmp.name
    avi_tmp.close()

    out = cv2.VideoWriter(avi_yolu,
                          cv2.VideoWriter_fourcc(*"XVID"),
                          fps, (genislik, yukseklik))

    kare_sayisi = 0
    toplam_tespit = 0
    nesne_sayaci = Counter()

    for i, kare in enumerate(tum_kareler):
        islenmis = kare.copy()

        for t in tum_tespitler[i]:
            x1, y1, x2, y2 = t["kutu"]
            sinif_adi = t["sinif"]
            sinif_id = t["sinif_id"]
            guven_skoru = t["guven"]
            renk = renk_uret(sinif_id)

            cv2.rectangle(islenmis, (x1, y1), (x2, y2), renk, 2)
            etiket = f"{sinif_adi} {guven_skoru:.0%}"
            (gw, gh), _ = cv2.getTextSize(etiket, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 1)
            cv2.rectangle(islenmis, (x1, y1 - gh - 8), (x1 + gw + 4, y1), renk, -1)
            cv2.putText(islenmis, etiket, (x1 + 2, y1 - 4),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1, cv2.LINE_AA)

            nesne_sayaci[sinif_adi] += 1
            toplam_tespit += 1

        out.write(islenmis)
        kare_sayisi += 1

        if ilerleme_callback and len(tum_kareler) > 0:
            ilerleme_callback(
                0.5 + kare_sayisi / len(tum_kareler) / 2,
                f"Adım 2/2 — Video yazılıyor: {kare_sayisi}/{len(tum_kareler)}"
            )

    out.release()

    from datetime import datetime
    zaman_damgasi = datetime.now().strftime("%Y%m%d_%H%M%S")
    kalici_mp4 = os.path.join(VIDEOS_KLASORU, f"analiz_{zaman_damgasi}.mp4")

    subprocess.run([
        "ffmpeg", "-y",
        "-i", avi_yolu,
        "-vcodec", "libx264",
        "-pix_fmt", "yuv420p",
        "-crf", "18",
        kalici_mp4
    ], capture_output=True)

    os.unlink(avi_yolu)

    return {
        "toplam_kare": kare_sayisi,
        "toplam_tespit": toplam_tespit,
        "nesne_sayaci": dict(nesne_sayaci.most_common()),
        "isi_haritasi": isi_renkli,
        "video_yolu": kalici_mp4
    }