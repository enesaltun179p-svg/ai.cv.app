import streamlit as st
from groq import Groq
from docx import Document
from io import BytesIO

# --- API AYARI (GİZLİ KASADAN ÇEKER) ---
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Enes Altun | Yapay Zeka Destekli Özgeçmiş Stüdyosu", page_icon="🚀", layout="wide")

# --- CSS EFEKTLERİ (KUTUCUKLAR VE TASARIM) ---
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stButton>button { width: 100%; border-radius: 20px; height: 3em; background-color: #007bff; color: white; }
    .stTextInput>div>div>input { border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- UYGULAMA BAŞLIĞI ---
st.title("📄 Yapay Zeka Destekli CV Stüdyosu")
st.write("Bilgilerini gir, yapay zeka profesyonel özgeçmişini saniyeler içinde hazırlasın!")

# --- FORM KUTUCUKLARI ---
col1, col2 = st.columns(2)

with col1:
    ad_soyad = st.text_input("Adınız Soyadınız")
    eposta = st.text_input("E-posta Adresiniz")
    telefon = st.text_input("Telefon Numaranız")

with col2:
    egitim = st.text_area("Eğitim Bilgileriniz")
    deneyim = st.text_area("İş/Proje Deneyimleriniz")
    yetenekler = st.text_input("Yetenekleriniz (Virgülle ayırın)")

# --- CV OLUŞTURMA BUTONU ---
if st.button("Profesyonel CV Oluştur ✨"):
    if ad_soyad and eposta:
        with st.spinner('Yapay zeka CV\'ni hazırlıyor...'):
            # Yapay zekaya gönderilen mesaj
            prompt = f"Ad: {ad_soyad}\nE-posta: {eposta}\nEğitim: {egitim}\nDeneyim: {deneyim}\nYetenekler: {yetenekler}\nBu bilgilerle profesyonel bir CV taslağı oluştur."
            
            chat_completion = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama3-8b-8192",
            )
            
            cv_metni = chat_completion.choices[0].message.content
            st.subheader("İşte CV Taslağın:")
            st.write(cv_metni)
            
            # Word dosyası oluşturma
            doc = Document()
            doc.add_heading(ad_soyad, 0)
            doc.add_paragraph(cv_metni)
            
            buffer = BytesIO()
            doc.save(buffer)
            buffer.seek(0)
            
            st.download_button(
                label="Word Dosyası Olarak İndir 📥",
                data=buffer,
                file_name=f"{ad_soyad}_CV.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
    else:
        st.warning("Lütfen en azından adınızı ve e-postanızı girin!")
