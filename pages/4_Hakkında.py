import streamlit as st
if not st.session_state.get("authentication_status"):
    st.warning("Bu sayfaya erişmek için giriş yapmanız gerekiyor.")
    st.stop()
from config import APP_ADI, APP_VERSIYONU, APP_ACIKLAMA, ONEMLI_SINIFLAR

st.set_page_config(page_title="Hakkında", layout="wide")

st.title("Proje Hakkında")
st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("Proje Bilgileri")
    st.markdown(f"**Proje Adı:** {APP_ADI}")
    st.markdown(f"**Versiyon:** {APP_VERSIYONU}")
    st.markdown(f"**Açıklama:** {APP_ACIKLAMA}")

    st.divider()

    st.subheader("Amaç")
    st.markdown("""
    Bu proje, drone ve İHA görüntüleri üzerinde yapay zeka tabanlı
    nesne tespiti yapan bir web uygulamasıdır.

    Güvenlik, trafik izleme, afet bölgeleri ve kalabalık alan takibi
    gibi alanlarda kullanılmak üzere tasarlanmıştır.

    Sistem, yüklenen drone videolarını kare kare analiz ederek
    içindeki nesneleri otomatik olarak tespit eder ve işaretler.
    """)

with col2:
    st.subheader("Kullanılan Teknolojiler")
    st.markdown("""
    **YOLOv8 (Ultralytics)**
    Gerçek zamanlı nesne tespiti için kullanılan derin öğrenme modeli.
    COCO veri seti ile eğitilmiş olup 80 farklı nesne sınıfını tanıyabilir.

    **OpenCV**
    Video okuma, kare işleme ve görüntü manipülasyonu için kullanılır.

    **Streamlit**
    Python tabanlı web arayüzü geliştirme kütüphanesi.

    **SQLite**
    Analiz geçmişini saklamak için kullanılan hafif veritabanı sistemi.

    **NumPy**
    Görüntü verilerinin sayısal olarak işlenmesi için kullanılır.
    """)

st.divider()

st.subheader("Tespit Edilebilen Nesneler")
st.markdown("Sistem aşağıdaki nesne kategorilerini tespit edebilir:")

kolonlar = st.columns(4)
for i, sinif in enumerate(ONEMLI_SINIFLAR):
    kolonlar[i % 4].success(sinif)

st.divider()

st.subheader("Nasıl Çalışır?")
a1, a2, a3, a4 = st.columns(4)
with a1:
    st.markdown("**1. Video Yükle**")
    st.markdown("Drone videosunu sisteme yükle")
with a2:
    st.markdown("**2. Analiz Et**")
    st.markdown("YOLOv8 modeli videoyu analiz eder")
with a3:
    st.markdown("**3. Sonuçları Gör**")
    st.markdown("Tespit edilen nesneleri incele")
with a4:
    st.markdown("**4. Raporu İndir**")
    st.markdown("İşlenmiş videoyu indir")