# IHA / Drone Goruntusu Nesne Tespiti Sistemi

YOLOv8 tabanli gercek zamanli nesne tespiti ve analiz platformu.

---

## Proje Hakkinda

Bu proje, drone ve IHA goruntulerindeki nesneleri otomatik olarak tespit eden bir web uygulamasidir. Sistem yuklenen drone videolarini kare kare analiz ederek icindeki nesneleri tespit eder, etrafina kutu cizer ve istatistiksel analiz sunar.

### Neden Bu Proje?

Drone goruntuleri guvenlik, trafik izleme, afet bolgesi takibi gibi kritik alanlarda kullanilmaktadir. Ancak bu goruntuleri manuel olarak incelemek zaman alici ve verimsizdir. Bu sistem bu sureci otomatiklestirmektedir.

---

## Ozellikler

- Drone videosu yukleme ve analiz
- YOLOv8 ile gercek zamanli nesne tespiti
- Isi haritasi analizi
- Istatistik grafikleri (Plotly)
- PDF rapor ciktisi
- Analiz gecmisi (SQLite)
- Ornek drone videolari
- Kullanici girisi sistemi
- REST API (FastAPI)

---

## Kullanilan Teknolojiler

| Teknoloji | Aciklama |
|-----------|----------|
| Python 3.12 | Ana programlama dili |
| YOLOv8 (Ultralytics) | Nesne tespiti modeli |
| OpenCV | Video isleme |
| Streamlit | Web arayuzu |
| FastAPI | REST API backend |
| SQLite | Veritabani |
| Plotly | Istatistik grafikleri |
| ReportLab | PDF rapor |
| FFmpeg | Video donusturme |

---

## Kurulum

### Gereksinimler
- Python 3.9+
- FFmpeg

### Adimlar


```bash
git clone https://github.com/oykayra/drone-tespiti-bitirme-projesi.git
cd drone-tespiti-bitirme-projesi

pip install ultralytics streamlit opencv-python fastapi uvicorn python-multipart plotly reportlab streamlit-authenticator

streamlit run Ana_Sayfa.py
```

### API icin

```bash
uvicorn api:app --reload --port 8000
```

---

## Kullanim

1. Uygulamayi baslat
2. Kullanici adi ve sifre ile giris yap
3. Sol menuuden Analiz sayfasina gec
4. Drone videosu yukle veya ornek video sec
5. Analiz Et butonuna bas
6. Sonuclari incele, PDF raporu indir

---

## Proje Yapisi
drone_tespiti/
├── Ana_Sayfa.py
├── api.py
├── config.py
├── database.py
├── detector.py
├── video_processor.py
├── pdf_rapor.py
└── pages/
├── 1_Analiz.py
├── 2_Gecmis.py
├── 3_Istatistik.py
├── 4_Hakkinda.py
└── 5_Ornek_Videolar.py

---

## Model

Bu projede VisDrone veri seti ile egitilmis YOLOv8 modeli kullanilmaktadir. Model asagidaki nesne siniflarini tespit edebilir:

- pedestrian (yaya)
- people (insan)
- bicycle (bisiklet)
- car (araba)
- van (minibus)
- truck (kamyon)
- tricycle (uc tekerlekli)
- bus (otobus)
- motor (motosiklet)

---

## Gelistirici

Oykü Kayra
Bilgisayar Programciligi Bitirme Projesi
