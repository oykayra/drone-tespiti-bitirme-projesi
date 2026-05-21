import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from database import veritabani_olustur, istatistikleri_getir

veritabani_olustur()

config = {
    "credentials": {
        "usernames": {
            "admin": {
                "email": "admin@drone.com",
                "name": "Admin",
                "password": "$2b$12$tgO1YkFQKLRXwAIHoAGnC.fNLBnQhzFDEhJYkbkZQMvlKpSuDvV2i"
            },
            "kullanici": {
                "email": "kullanici@drone.com",
                "name": "Kullanici",
                "password": "$2b$12$tgO1YkFQKLRXwAIHoAGnC.fNLBnQhzFDEhJYkbkZQMvlKpSuDvV2i"
            }
        }
    },
    "cookie": {
        "expiry_days": 1,
        "key": "gizli_anahtar_123",
        "name": "drone_tespiti"
    }
}

auth = stauth.Authenticate(
    config["credentials"],
    config["cookie"]["name"],
    config["cookie"]["key"],
    config["cookie"]["expiry_days"]
)

auth.login()

if st.session_state["authentication_status"] == False:
    st.error("Kullanıcı adı veya şifre yanlış!")

elif st.session_state["authentication_status"] == None:
    st.warning("Lütfen kullanıcı adı ve şifre girin.")

elif st.session_state["authentication_status"]:
    st.set_page_config(
        page_title="İHA Nesne Tespiti",
        layout="wide"
    )

    auth.logout(location="sidebar")

    st.title("İHA / Drone Görüntüsü Nesne Tespiti Sistemi")
    st.markdown(f"Hoşgeldin **{st.session_state['name']}**!")
    st.markdown("YOLOv8 tabanlı gerçek zamanlı nesne tespiti ve analiz platformu.")
    st.divider()

    istatistikler = istatistikleri_getir()

    col1, col2, col3 = st.co