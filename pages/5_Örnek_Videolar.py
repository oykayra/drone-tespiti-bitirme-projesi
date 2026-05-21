import streamlit as st
if not st.session_state.get("authentication_status"):
    st.warning("Bu sayfaya erişmek için giriş yapmanız gerekiyor.")
    st.stop()
import os

st.set_page_config(page_title="Örnek Videolar", layout="wide")

st.title("Örnek Drone Videoları")
st.markdown("Hazır drone videolarını seçip direkt analiz edebilirsin.")
st.divider()

ana_klasor = r"C:\Users\Öykü Kayra\drone_tespiti"

ornek_videolar = [
    {
        "baslik": "Trafik ve Arabalar",
        "aciklama": "Havadan çekilmiş trafik ve araç görüntüsü",
        "dosya": "247587.mov"
    },
    {
        "baslik": "Liman ve Gemiler",
        "aciklama": "Havadan çekilmiş liman ve gemi görüntüsü",
        "dosya": "33014-395456435.mp4"
    },
    {
        "baslik": "Yayalar ve İnsanlar",
        "aciklama": "Havadan çekilmiş yaya ve insan görüntüsü",
        "dosya": "27999-366978301_medium.mp4"
    }
]

for video in ornek_videolar:
    dosya_yolu = os.path.join(ana_klasor, video["dosya"])

    if not os.path.exists(dosya_yolu):
        st.warning(f"{video['baslik']} bulunamadı.")
        continue

    with st.container():
        col1, col2 = st.columns([2, 1])
        with col1:
            st.subheader(video["baslik"])
            st.markdown(video["aciklama"])
            st.video(dosya_yolu)
        with col2:
            st.markdown("###")
            st.markdown("###")
            if st.button("Bu Videoyu Analiz Et", key=video["baslik"]):
                st.session_state["ornek_video_yolu"] = dosya_yolu
                st.session_state["ornek_video_adi"] = video["baslik"]
                st.success("Video seçildi!")
                st.page_link("pages/1_Analiz.py", label="Analiz Sayfasına Git")
        st.divider()