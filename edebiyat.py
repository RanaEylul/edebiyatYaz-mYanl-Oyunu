import streamlit as st
import random

# Sayfa Yapılandırması ve Coderspace Tarzı Koyu Tema Tasarımı
st.set_page_config(
    page_title="ÖSYM Yazım Pratiği - Coderspace",
    page_icon="⌨️",
    layout="wide"
)

# CSS ile Coderspace Benzeri Şık Tasarım
st.markdown("""
    <style>
    .stApp {
        background-color: #13111c;
        color: #d1d0c5;
    }
    .kelime-alani {
        font-family: 'Courier New', monospace;
        font-size: 28px;
        letter-spacing: 2px;
        padding: 20px;
        background-color: #1a1625;
        border-radius: 12px;
        border: 1px solid #2c2738;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# ÖSYM'de Sıkça Karıştırılan Kelimelerin DOĞRU Halleri Havuzu
osym_dogru_kelimeler = [
    "yalnız", "yanlış", "herkes", "unvan", "orijinal", 
    "kılavuz", "şoför", "stajyer", "laboratuvar", "doküman", 
    "palyaço", "akaryakıt", "birdenbire", "birkaç", "hapishane", 
    "karpuz", "komite", "unutkan", "özgün", "esrar", 
    "kirpik", "poğaça", "savrulmak", "kolej", "dereotu", 
    "başyapıt", "taşeron", "mütevazi", "akıbet", "özveri"
]

# Oturum Durumu Yönetimi
if "oyun_basladi" not in st.session_state:
    st.session_state.oyun_basladi = False
if "secilen_sure" not in st.session_state:
    st.session_state.secilen_sure = 30
if "kelime_listesi" not in st.session_state:
    st.session_state.kelime_listesi = []

# Üst Menü / Kontrol Paneli (Coderspace Tarzı Süre ve Seçenekler)
col1, col2, col3 = st.columns([3, 2, 2])

with col1:
    st.markdown("### ⌨️ ÖSYM Yazım & Hız Stüdyosu")

with col2:
    # Süre Seçimi (15sn, 30sn, 60sn, 120sn, 180sn)
    sure_secenekleri = {15: "15 sn", 30: "30 sn", 60: "60 sn", 120: "120 sn", 180: "180 sn"}
    secilen_key = st.selectbox(
        "Süre Seçin:", 
        options=list(sure_secenekleri.keys()), 
        format_func=lambda x: sure_secenekleri[x],
        index=1
    )
    st.session_state.secilen_sure = secilen_key

with col3:
    st.write("")
    st.write("")
    if st.button("🔄 Yeniden Başlat / Yeni Kelimeler"):
        st.session_state.kelime_listesi = random.sample(osym_dogru_kelimeler, min(15, len(osym_dogru_kelimeler)))
        st.session_state.oyun_basladi = True
        st.rerun()

st.markdown("---")

# İlk açılışta veya liste boşsa kelimeleri doldur
if not st.session_state.kelime_listesi:
    st.session_state.kelime_listesi = random.sample(osym_dogru_kelimeler, min(15, len(osym_dogru_kelimeler)))

# Akacak Kelimeleri Ekrana Yazdırma (Coderspace Görünümü)
metin_gosterimi = " &nbsp;&nbsp; ".join([f"`{k}`" for k in st.session_state.kelime_listesi])
st.markdown(f"**Pratik Yapılacak ÖSYM Doğru Kelimeleri:**")
st.markdown(f'<div class="kelime-alani">{metin_gosterimi}</div>', unsafe_allow_html=True)

# Yazma ve Eşleştirme Alanı
st.markdown("### Kelimeleri Sırayla Yazarak Pratik Yapın:")

with st.form(key="coderspace_form", clear_on_submit=True):
    kullanici_girdisi = st.text_input("Yukarıdaki kelimeleri sırayla yazıp boşluk bırakın veya Enter'a basın:", placeholder="Yazmaya başla...")
    submit_btn = st.form_submit_button("Kelimeyi Kontrol Et / İlerle")

    if submit_btn and kullanici_girdisi:
        girilen_kelimeler = kullanici_girdisi.strip().split()
        dogru_bilinenler = 0
        
        for kelime in girilen_kelimeler:
            if st.session_state.kelime_listesi and kelime == st.session_state.kelime_listesi[0]:
                # Doğru bilinen kelimeyi listeden düş
                st.session_state.kelime_listesi.pop(0)
                dogru_bilinenler += 1

        # Eğer liste bittiyse yeni kelimeler yükle
        if not st.session_state.kelime_listesi:
            st.session_state.kelime_listesi = random.sample(osym_dogru_kelimeler, min(15, len(osym_dogru_kelimeler)))
            st.success("🎉 Harika! Yeni ÖSYM kelime havuzu yüklendi, hız kesmeden devam et!")
        else:
            st.info(f"Son yazdıklarından {dogru_bilinenler} tanesi doğru eşleşti. Devam et!")
        st.rerun()

# İstatistik Alanı (Coderspace Skor Kartları Gibi)
col_a, col_b, col_c = st.columns(3)
col_a.metric("Seçilen Süre", f"{st.session_state.secilen_sure} Saniye")
col_b.metric("Kalan Kelime Sayısı", len(st.session_state.kelime_listesi))
col_c.metric("Mod", "ÖSYM Sınav Yazım Pratiği")
