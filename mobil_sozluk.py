import streamlit as st
st.set_page_config(page_title="İngilizce-Türkçe Sözlük", layout="centered")

import random
import os

# Özel font ve emoji desteği
st.markdown("""
    <style>
    @font-face {
        font-family: 'Inter';
        src: url('fonts/Inter-Regular.ttf') format('truetype');
    }
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    </style>
""", unsafe_allow_html=True)

# Sözlük dosyasını yükleme
def sozlugu_yukle():
    sozluk = {}
    if os.path.exists("sozluk.txt"):
        with open("sozluk.txt", "r", encoding="utf-8") as f:
            for satir in f:
                try:
                    kelime, anlam = satir.strip().split(":")
                    sozluk[kelime] = anlam
                except ValueError:
                    continue
    return sozluk

# Sözlüğü kaydetme
def sozlugu_kaydet(sozluk):
    with open("sozluk.txt", "w", encoding="utf-8") as f:
        for kelime, anlam in sozluk.items():
            f.write(f"{kelime}:{anlam}\n")

# Sayfa başlığı
st.set_page_config(page_title="İngilizce-Türkçe Sözlük", layout="centered")

# Sayfa seçici
sayfa = st.sidebar.selectbox("📂 Sayfa Seçiniz", ["🏠 Ana Sayfa", "📖 Sözlük", "📝 Quiz Modu"])

# Sözlük verisi
sozluk = sozlugu_yukle()
ters_sozluk = {v: k for k, v in sozluk.items()}

# 🏠 Ana Sayfa
if sayfa == "🏠 Ana Sayfa":
    st.markdown("## 📚 İngilizce-Türkçe Sözlük")
    st.markdown("Bu uygulama ile kelime arayabilir, yeni kelime ekleyebilir ve quiz modunda kendinizi test edebilirsiniz.")

# 📖 Sözlük Ekranı
elif sayfa == "📖 Sözlük":
    st.subheader("🔍 Kelime Ara")
    kelime = st.text_input("Kelime giriniz:")
    if st.button("Ara"):
        anlam = sozluk.get(kelime.capitalize(), ters_sozluk.get(kelime.capitalize(), "Kelime bulunamadı."))
        st.success(f"**{kelime.capitalize()} ➜ {anlam}**")

    st.subheader("➕ Yeni Kelime Ekle")
    yeni_kelime = st.text_input("Yeni Kelime:")
    yeni_anlam = st.text_input("Anlamı:")
    if st.button("Ekle"):
        if yeni_kelime and yeni_anlam:
            sozluk[yeni_kelime.capitalize()] = yeni_anlam.capitalize()
            sozlugu_kaydet(sozluk)
            st.success(f"✅ '{yeni_kelime.capitalize()}' eklendi!")

    st.subheader("➖ Kelime Sil")
    sil_kelime = st.text_input("Silinecek Kelime:")
    if st.button("Sil"):
        if sil_kelime.capitalize() in sozluk:
            del sozluk[sil_kelime.capitalize()]
            sozlugu_kaydet(sozluk)
            st.warning(f"❌ '{sil_kelime.capitalize()}' silindi!")
        else:
            st.error("Kelime bulunamadı.")

# 📝 Quiz Modu
elif sayfa == "📝 Quiz Modu":
    st.subheader("🧠 Quiz Modu")

    if "quiz_kelime" not in st.session_state:
        st.session_state.quiz_kelime = ""
        st.session_state.quiz_cevap = ""
        st.session_state.soru_tipi = ""
        st.session_state.sec_options = []

    def yeni_soru():
        if random.choice([True, False]):
            st.session_state.soru_tipi = "ing-tr"
            st.session_state.quiz_kelime, st.session_state.quiz_cevap = random.choice(list(sozluk.items()))
            secenekler = random.sample(list(sozluk.values()), 3)
        else:
            st.session_state.soru_tipi = "tr-ing"
            st.session_state.quiz_kelime, st.session_state.quiz_cevap = random.choice(list(ters_sozluk.items()))
            secenekler = random.sample(list(ters_sozluk.values()), 3)

        if st.session_state.quiz_cevap not in secenekler:
            secenekler[random.randint(0, 2)] = st.session_state.quiz_cevap

        random.shuffle(secenekler)
        st.session_state.sec_options = secenekler

    if st.button("🔄 Yeni Soru"):
        yeni_soru()

    if st.session_state.quiz_kelime:
        st.markdown(f"**❓ {st.session_state.quiz_kelime} ne anlama gelir?**")
        for secenek in st.session_state.sec_options:
            if st.button(secenek):
                if secenek == st.session_state.quiz_cevap:
                    st.success("✅ Doğru!")
                else:
                    st.error(f"❌ Yanlış! Doğru cevap: {st.session_state.quiz_cevap}")
                st.session_state.quiz_kelime = ""
