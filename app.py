import streamlit as st
from groq import Groq
from docx import Document
from io import BytesIO

# --- API AYARI ---
GROQ_API_KEY = client = Groq(api_key=st.secrets["GROQ_API_KEY"])
client = Groq(api_key=GROQ_API_KEY.strip())

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Enes Altun | AI CV Studio", page_icon="🚀", layout="wide")

# --- 1. BİLGİLENDİRİCİ GİRİŞ EKRANI ---
if 'animasyon_gecti' not in st.session_state:
    st.session_state['animasyon_gecti'] = False

if not st.session_state['animasyon_gecti']:
    st.balloons()
    st.title("🌟 AI CV Studio'ya Hoş Geldin!")
    st.markdown("""
    ### 📖 Bu Site Nasıl Çalışır?
    1. **Bilgilerini Gir:** Adını ve yeteneklerini eksiksiz yaz.
    2. **AI Sihri:** Yapay zeka senin için profesyonel maddeler oluşturur.
    3. **İndir:** Tek tıkla Word (.docx) formatında çıktını al.
    """)
    if st.button("Hemen Başla 🚀"):
        st.session_state['animasyon_gecti'] = True
        st.rerun()
else:
    # --- 2. YAN MENÜ (GERİ BİLDİRİM) ---
    with st.sidebar:
        st.title("💬 Geri Bildirim")
        puan = st.slider("Puanla", 1, 5, 5)
        mesaj = st.text_area("Mesajın", placeholder="Görüşlerini yaz...")
        if st.button("Gönder"):
            if mesaj:
                st.success("Geri bildirimin için teşekkürler!")
            else:
                st.warning("Lütfen bir mesaj yaz kanka.")

    # --- 3. ANA UYGULAMA ---
    st.title("📄 Profesyonel CV Oluşturucu")
    
    col1, col2 = st.columns(2)
    with col1:
        isim = st.text_input("Ad Soyad", placeholder="Enes Altun")
    with col2:
        pozisyon = st.text_input("Hedef Pozisyon", placeholder="Yazılım / Tasarım")

    deneyim = st.text_area("Yeteneklerin", placeholder="Neler yapabiliyorsun?", height=150)

    # WORD OLUŞTURMA FONKSİYONU
    def create_docx(isim, icerik):
        doc = Document()
        doc.add_heading(f'{isim} - Özgeçmiş', 0)
        for line in icerik.split('\n'):
            doc.add_paragraph(line)
        bio = BytesIO()
        doc.save(bio)
        return bio.getvalue()

    # İŞLEM BUTONU
    if st.button("✨ CV Yaz"):
        if not isim or not deneyim:
            st.warning("Lütfen boş alan bırakma kanka!")
        else:
            try:
                with st.spinner('Yapay zeka yazıyor...'):
                    completion = client.chat.completions.create(
                        model="llama-3.1-8b-instant",
                        messages=[
                            {"role": "system", "content": "Sen profesyonel bir TDK editörü ve İK uzmanısın. SADECE Türkçe karakterler kullan."},
                            {"role": "user", "content": f"İsim: {isim}. Deneyim: {deneyim}. Profesyonel CV yaz."}
                        ]
                    )
                    st.session_state['cv_sonuc'] = completion.choices[0].message.content
            except Exception as e:
                st.error(f"Hata: {e}")

    # SONUÇ GÖSTERİMİ
    if 'cv_sonuc' in st.session_state:
        st.divider()
        st.markdown("### 📄 CV Önizleme")
        st.info(st.session)
