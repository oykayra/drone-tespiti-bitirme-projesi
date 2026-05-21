import cv2
import numpy as np
from ultralytics import YOLO
from config import VARSAYILAN_MODEL, VARSAYILAN_GUVEN, ONEMLI_SINIFLAR


def renk_uret(sinif_id):
    np.random.seed(sinif_id)
    return tuple(int(c) for c in np.random.randint(50, 255, 3))


class DroneDetector:
    def __init__(self, model_yolu=VARSAYILAN_MODEL, guven=VARSAYILAN_GUVEN):
        self.model = YOLO(model_yolu)
        self.guven = guven
        self.sinif_isimleri = self.model.names

    def kare_analiz_et(self, kare):
        sonuclar = self.model(kare, conf=self.guven, verbose=False)
        tespitler = []

        for sonuc in sonuclar:
            for kutu in sonuc.boxes:
                sinif_id = int(kutu.cls[0])
                guven_skoru = float(kutu.conf[0])
                x1, y1, x2, y2 = map(int, kutu.xyxy[0])
                sinif_adi = self.sinif_isimleri[sinif_id]
                renk = renk_uret(sinif_id)

                cv2.rectangle(kare, (x1, y1), (x2, y2), renk, 2)
                etiket = f"{sinif_adi} {guven_skoru:.0%}"
                (gw, gh), _ = cv2.getTextSize(etiket, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 1)
                cv2.rectangle(kare, (x1, y1 - gh - 8), (x1 + gw + 4, y1), renk, -1)
                cv2.putText(kare, etiket, (x1 + 2, y1 - 4),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1, cv2.LINE_AA)

                tespitler.append({
                    "sinif": sinif_adi,
                    "guven": guven_skoru,
                    "kutu": (x1, y1, x2, y2),
                    "onemli": sinif_adi in ONEMLI_SINIFLAR
                })

        return kare, tespitler