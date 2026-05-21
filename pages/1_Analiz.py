import streamlit as st
if not st.session_state.get("authentication_status"):
    st.warning("Bu sayfaya erişmek için giriş yapmanız gerekiyor.")
    st.stop()
import tempfile
import os
import time
import cv2
from database import analiz_kaydet
from video_processor import video_isle
from pdf_rapor import pdf_olustur

st.set_page_config(page_title="Analiz", layout="wide")

st.title("Video Analizi")
st.markdown("Drone videosu yükle ve nesne tespiti yap.")
st.divider()

with st.sidebar:
    st.header("Ayarlar")
    guven = st.slider("Güven Eşiği", 0.1, 0.9, 0.4, 0.05)
    isi_goster = st.checkbox("Isı Haritasını Göster", value=True)
    st.markdown("Güven eşiği: Modelin ne kadar emin olması gerektiğini belirler.")

ornek_video_var = "ornek_video_yolu" in st.session_state

if ornek_video_var:
    st.info(f"Örnek video seçildi: {st.session_state['ornek_video_adi']}")
    if st.button("Örnek Videoyu Kaldır"):
        del st.session_state["ornek_video_yolu"]
        del st.session_state["ornek_video_adi"]
        st.rerun()

yuklenen = st.file_uploader("Drone videosu seç (MP4, AVI, MOV)", type=["mp4", "avi", "mov"])

if yuklenen:
    with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as tmp:
        tmp.write(yuklenen.read())
        giris_yolu = tmp.name
    video_adi = yuklenen.name
elif ornek_video_var:
    giris_yolu = st.session_state["ornek_video_yolu"]
    video_adi = st.session_state["ornek_video_adi"]
else:
    giris_yolu = None
    video_adi = None

if giris_yolu:
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Orijinal Video**")
        st.video(giris_yolu)

    if st.button("Analiz Et", type="primary", use_container_width=True):
        st.divider()
        ilerleme = st.progress(0, text="Başlıyor...")
        baslangic = time.time()

        def ilerleme_guncelle(oran, metin):
            ilerleme.progress(oran, text=metin)

        sonuclar = video_isle(
            giris_yolu=giris_yolu,
            guven=guven,
            isi_haritasi_goster=isi_goster,
            ilerleme_callback=ilerleme_guncelle
        )

        sure = round(time.time() - baslangic, 2)
        ilerleme.progress(1.0, text="Tamamlandı!")

        analiz_kaydet(
            video_adi=video_adi,
            toplam_kare=sonuclar["toplam_kare"],
            toplam_tespit=sonuclar["toplam_tespit"],
            nesne_sayaci=sonuclar["nesne_sayaci"],
            sure=sure,
            video_yolu=sonuclar["video_yolu"]
        )

        st.subheader("Analiz Sonuçları")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Toplam Kare", sonuclar["toplam_kare"])
        m2.metric("Toplam Tespit", sonuclar["toplam_tespit"])
        m3.metric("Farklı Nesne", len(sonuclar["nesne_sayaci"]))
        m4.metric("Süre", f"{sure} sn")

        if sonuclar["nesne_sayaci"]:
            st.markdown("**Tespit Edilen Nesneler**")
            for nesne, sayi in sonuclar["nesne_sayaci"].items():
                st.progress(
                    sayi / sonuclar["toplam_tespit"],
                    text=f"{nesne}: {sayi} tespit"
                )

        with col2:
            st.markdown("**İşlenmiş Video**")
            with open(sonuclar["video_yolu"], "rb") as f:
                video_bytes = f.read()
            st.video(video_bytes)

        st.divider()
        st.subheader("Isı Haritası")
        st.markdown("Kırmızı = en çok nesne tespit edilen bölge")
        isi_rgb = cv2.cvtColor(sonuclar["isi_haritasi"], cv2.COLOR_BGR2RGB)
        st.image(isi_rgb, width=800)

        st.divider()
        st.subheader("Raporlar")
        ind1, ind2 = st.columns(2)

        with ind1:
            st.download_button(
                "Videoyu İndir",
                video_bytes,
                "sonuc.mp4",
                "video/mp4",
                use_container_width=True
            )

        with ind2:
            pdf_yolu = pdf_olustur(
                video_adi=video_adi,
                toplam_kare=sonuclar["toplam_kare"],
                toplam_tespit=sonuclar["toplam_tespit"],
                nesne_sayaci=sonuclar["nesne_sayaci"],
                sure=sure
            )
            with open(pdf_yolu, "rb") as f:
                pdf_bytes = f.read()
            st.download_button(
                "PDF Raporu İndir",
                pdf_bytes,
                "analiz_raporu.pdf",
                "application/pdf",
                use_container_width=True
            )
            os.unlink(pdf_yolu)

        if yuklenen:
            os.unlink(giris_yolu)

else:
    st.info("Başlamak için bir video yükle veya Örnek Videolar sayfasından bir video seç.")