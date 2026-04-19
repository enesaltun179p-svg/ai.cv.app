import streamlit as st
from groq import Groq
from docx import Document
from io import BytesIO

# --- API AYARI ---
# Burası senin 'Sırlar' (Secrets) kısmındaki anahtarı çeker
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Enes Altun | Yapay Zeka Destekli Özgeçmiş Stüdyosu", page_icon="🚀", layout="wide")

# --- OTURUM DURUMU KONTROLÜ ---
if 'animasyon_gecti' not in st.session_state:
    st.session_state['animasyon_gecti'] = False

# --- ANA EKRAN ---
if not st.session_state['animasyon_gecti']:
    st.title("🚀 Yapay Zeka CV Oluşturucuya Hoş Geldin!")
    st.write("Profesyonel bir CV hazırlamak hiç bu kadar kolay olmamıştı.")
    if st.button("Hadi Başlayalım!"):
        st.session_state['animasyon_gecti'] = True
        st.rerun()
else:
    st.success("Sistem Hazır! CV bilgilerini doldurmaya başlayabilirsin.")
    # Buraya uygulamanın geri kalan form özelliklerini ekleyebilirsin.
