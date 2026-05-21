import streamlit as st
#if not st.session_state.get("authentication_status"):
    #st.warning("Bu sayfaya erişmek için giriş yapmanız gerekiyor.")
    #st.stop()
import pandas as pd
from collections import Counter
from database import analizleri_getir, istatistikleri_getir
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="İstatistikler", layout="wide")

st.title("İstatistikler")
st.markdown("Tüm analizlerin genel istatistikleri ve grafikleri.")
st.divider()

istatistikler = istatistikleri_getir()
analizler = analizleri_getir()

col1, col2, col3 = st.columns(3)
col1.metric("Toplam Analiz", istatistikler["toplam_analiz"])
col2.metric("Toplam Tespit", istatistikler["toplam_tespit"])
col3.metric("Toplam İşlenen Kare", istatistikler["toplam_kare"])

st.divider()

if not analizler:
    st.info("Henüz hiç analiz yapılmadı.")
else:
    st.subheader("Analize Göre Tespit Sayısı")
    tablo = pd.DataFrame([{
        "Tarih": a["tarih"],
        "Video": a["video_adi"],
        "Tespit": a["toplam_tespit"],
        "Kare": a["toplam_kare"],
        "Süre": a["sure"]
    } for a in analizler])

    fig1 = px.bar(
        tablo,
        x="Tarih",
        y="Tespit",
        color="Video",
        title="Analize Göre Tespit Sayısı",
        labels={"Tespit": "Tespit Sayısı", "Tarih": "Analiz Tarihi"}
    )
    st.plotly_chart(fig1, use_container_width=True)

    st.divider()
    st.subheader("Analiz Süresi Karşılaştırması")
    fig2 = px.bar(
        tablo,
        x="Tarih",
        y="Süre",
        color="Video",
        title="Analiz Süreleri (saniye)",
        labels={"Süre": "Süre (sn)", "Tarih": "Analiz Tarihi"}
    )
    st.plotly_chart(fig2, use_container_width=True)

    st.divider()
    st.subheader("En Çok Tespit Edilen Nesneler")

    toplam_nesne = Counter()
    for a in analizler:
        for nesne, sayi in a["nesne_sayaci"].items():
            toplam_nesne[nesne] += sayi

    if toplam_nesne:
        nesne_df = pd.DataFrame(
            toplam_nesne.most_common(10),
            columns=["Nesne", "Toplam Tespit"]
        )

        fig3 = px.bar(
            nesne_df,
            x="Nesne",
            y="Toplam Tespit",
            color="Nesne",
            title="En Çok Tespit Edilen 10 Nesne",
            labels={"Toplam Tespit": "Tespit Sayısı"}
        )
        st.plotly_chart(fig3, use_container_width=True)

        st.divider()
        st.subheader("Nesne Dağılımı (Pasta Grafik)")
        fig4 = px.pie(
            nesne_df,
            values="Toplam Tespit",
            names="Nesne",
            title="Nesne Dağılımı"
        )
        st.plotly_chart(fig4, use_container_width=True)

        st.divider()
        st.subheader("Detaylı Nesne Tablosu")
        st.dataframe(nesne_df, use_container_width=True)