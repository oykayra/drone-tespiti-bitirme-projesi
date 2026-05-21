import streamlit as st
from database import veritabani_olustur, istatistikleri_getir

veritabani_olustur()

st.set_page_config(
    page_title="İHA Nesne Tespiti",
    layout="wide"
)

st.title("İHA / Drone Görüntüsü Nesne Tespiti Sistemi")
st.markdown("YOLOv8 tabanlı gerçek zamanlı nesne tespiti ve analiz platformu.")
st.divider()

istatistikler = istatistikleri_getir()

col1, col2, col3 = st.columns(3)