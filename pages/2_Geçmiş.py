import streamlit as st
#if not st.session_state.get("authentication_status"):
    #st.warning("Bu sayfaya erişmek için giriş yapmanız gerekiyor.")
   # st.stop()
import pandas as pd
import os
from database import analizleri_getir, analiz_sil

st.set_page_config(page_title="Geçmiş Analizler", layout="wide")

st.title("Geçmiş Analizler")
st.markdown("Daha önce yapılan tüm analizler burada listelenir.")
st.divider()

analizler = analizleri_getir()

if not analizler:
    st.info("Henüz hiç analiz yapılmadı.")
else:
    tablo_verisi = []
    for a in analizler:
        tablo_verisi.append({
            "ID": a["id"],
            "Tarih": a["tarih"],
            "Video": a["video_adi"],
            "Kare": a["toplam_kare"],
            "Tespit": a["toplam_tespit"],
            "Süre (sn)": a["sure"],
            "Video Var mı": "✅" if a["video_yolu"] and os.path.exists(a["video_yolu"]) else "❌"
        })

    df = pd.DataFrame(tablo_verisi)
    st.dataframe(df, use_container_width=True)

    st.divider()
    st.subheader("Analiz Detayı")

    secilen_id = st.selectbox("Analiz seç", [a["id"] for a in analizler],
                               format_func=lambda x: f"ID {x} — {next(a['video_adi'] for a in analizler if a['id'] == x)}")
    secilen = next(a for a in analizler if a["id"] == secilen_id)

    col1, col2, col3 = st.columns(3)
    col1.metric("Toplam Kare", secilen["toplam_kare"])
    col2.metric("Toplam Tespit", secilen["toplam_tespit"])
    col3.metric("Süre", f"{secilen['sure']} sn")

    st.markdown("**Nesne Dağılımı**")
    if secilen["nesne_sayaci"]:
        for nesne, sayi in secilen["nesne_sayaci"].items():
            st.progress(
                sayi / secilen["toplam_tespit"],
                text=f"{nesne}: {sayi} tespit"
            )

    st.divider()

    if secilen["video_yolu"] and os.path.exists(secilen["video_yolu"]):
        st.subheader("İşlenmiş Video")
        with open(secilen["video_yolu"], "rb") as f:
            video_bytes = f.read()
        st.video(video_bytes)
        st.download_button("Videoyu İndir", video_bytes,
                           f"analiz_{secilen_id}.mp4", "video/mp4",
                           use_container_width=True)
    else:
        st.info("Bu analiz için video kaydedilmemiş.")

    st.divider()
    if st.button("Bu Analizi Sil", type="secondary"):
        analiz_sil(secilen_id)
        st.success("Analiz silindi!")
        st.rerun()