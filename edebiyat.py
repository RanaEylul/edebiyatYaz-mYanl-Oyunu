import streamlit as st
import random

# Sayfa Yapılandırması
st.set_page_config(
    page_title="ÖSYM Doğru Kelime Yazma Stüdyosu",
    page_icon="⌨️",
    layout="centered"
)

# Sadece ÖSYM Kelimelerinin DOĞRU Halleri Havuzu
osym_dogru_kelimeler = [
    "yalnız", "yanlış", "herkes", "unvan", "orijinal", 
    "kılavuz", "şoför", "stajyer", "laboratuvar", "doküman", 
    "palyaço", "akaryakıt", "birdenbire", "birkaç", "hapishane", 
    "karpuz", "komite", "unutkan", "özgün", "esrar", 
    "kirpik", "poğaça", "savrulmak", "kolej", "dereotu", 
    "başyapıt", "taşeron", "mütevazi", "akıbet", "özveri"
]

# Oturum Durumu Başlatma
if "hedef_kelime" not in st.session_state:
    st.session_state.hedef_kelime = random.choice(osym_dogru_kelimeler)
if "dogru_sayisi" not in st.session_state:
    st.session_state.dogru_sayisi = 0

st.title("⌨️ ÖSYM Doğru Kelimeler - Yazma Çalışması")
st.markdown("Aşağıda yazan kelimenin **doğru halini** kutuya yazarak klavye hızını ve kelime hafızanı geliştir.")

# Ekranda Gösterilecek Kelime (Doğru Hali)
st.markdown("### Yazılacak Kelime:")
st.markdown(f"<h1 style='color: #2ecc71; font-family: monospace;'>{st.session_state.hedef_kelime}</h1>", unsafe_allow_html=True)

# Yazma Alanı
with st.form(key="yazma_formu", clear_on_submit=True):
    kullanici_girdisi = st.text_input("Yukarıdaki kelimeyi birebir yazıp Enter'a bas:", placeholder="Buraya yaz...")
    submit = st.form_submit_button("Gönder")

    if submit:
        if kullanici_girdisi.strip().lower() == st.session_state.hedef_kelime:
            st.success("Harika! Doğru yazdın 🎯")
            st.session_state.dogru_sayisi += 1
            st.session_state.hedef_kelime = random.choice(osym_dogru_kelimeler)
            st.rerun()
        else:
            st.error(f"Hatalı yazdın! Doğru yazılışı: **{st.session_state.hedef_kelime}**")
            st.session_state.hedef_kelime = random.choice(osym_dogru_kelimeler)
            st.rerun()

st.markdown("---")
st.metric("Toplam Doğru Yazılan Kelime", st.session_state.dogru_sayisi)

if st.button("Yeniden Başlat / Sıfırla"):
    st.session_state.dogru_sayisi = 0
    st.session_state.hedef_kelime = random.choice(osym_dogru_kelimeler)
    st.rerun()
