APP_ADI = "IHA / Drone Goruntusu Nesne Tespiti"
APP_VERSIYONU = "1.0.0"
APP_ACIKLAMA = "YOLOv8 tabanli gercek zamanli nesne tespiti sistemi"

VARSAYILAN_MODEL = "runs/detect/train/weights/best.pt"
VARSAYILAN_GUVEN = 0.15
MIN_GUVEN = 0.1
MAX_GUVEN = 0.9

MAKS_VIDEO_BOYUTU = 200
DESTEKLENEN_FORMATLAR = ["mp4", "avi", "mov"]

VERITABANI_ADI = "drone_tespiti.db"

RENKLER = {
    "birincil": "#FF4B4B",
    "ikincil": "#0068C9",
    "basari": "#09AB3B",
    "uyari": "#FF8700",
    "arka_plan": "#0E1117",
    "kart": "#1E2130"
}

ONEMLI_SINIFLAR = [
    "person",
    "car",
    "truck",
    "bus",
    "motorcycle",
    "bicycle",
    "airplane",
    "boat"
]