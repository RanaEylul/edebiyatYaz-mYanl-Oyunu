import streamlit as st
import random

# Sayfa Yapılandırması
st.set_page_config(
    page_title="ÖSYM Yazım Hızı Pratiği",
    page_icon="⚡",
    layout="centered"
)

# ÖSYM'de Sıkça Karıştırılan Kelimelerin DOĞRU Halleri Havuzu
osym_dogru_kelimeler = [
    "yalnız", "yanlış", "herkes", "unvan", "orijinal", 
    "kılavuz", "şoför", "stajyer", "laboratuvar", "doküman", 
    "palyaço", "akaryakıt", "birdenbire", "birkaç", "hapishane", 
    "karpuz", "komite", "unutkan", "özgün", "esrar", 
    "kirpik", "poğaça", "savrulmak", "kolej", "dereotu", 
    "başyapıt", "taşeron", "mütevazi", "akıbet", "özveri"
]

# Oturum Durumu Tanımlamaları
if "kelime_listesi" not in st.session_state:
    st.session_state.kelime_listesi = random.sample(osym_dogru_kelimeler, 10)
if "dogru_sayisi" not in st.session_state:
    st.session_state.dogru_sayisi = 0

st.title("⚡ ÖSYM Yazım ve Hız Pratiği (.py)")
st.markdown("Bu Python dosyası Streamlit altyapısıyla çalışır. Kelimelerin **doğru hallerini** sırayla yazarak hızını geliştir.")

# Süre Seçimi
secilen_sure = st.selectbox("Süre Seçin:", [15, 30, 60, 120, 180], index=1)

# Akacak Kelimeler
st.markdown("### Pratik Yapılacak Kelimeler:")
gosterim_metni = "  /  ".join(st.session_state.kelime_listesi)
st.code(gosterim_metni, language="text")

# Yazma Alanı
with st.form(key="python_kod_formu", clear_on_submit=True):
    kullanici_girdisi = st.text_input("Yukarıdaki kelimelerden sıradakini yazın:", placeholder="Buraya yazıp enterla...")
    gonder_btn = st.form_submit_button("Kelimeyi Gönder")

    if gonder_btn and kullanici_girdisi:
        hedef_kelime = st.session_state.kelime_listesi[0]
        
        if kullanici_girdisi.strip().lower() == hedef_kelime:
            st.success(f"🎉 Harika! '{hedef_kelime}' doğru.")
            st.session_state.dogru_sayisi += 1
            st.session_state.kelime_listesi.pop(0)
        else:
            st.error(f"❌ Yanlış! Doğrusu **{hedef_kelime}** olacaktı.")
            st.session_state.kelime_listesi.pop(0)

        # Liste biterse yenile
        if not st.session_state.kelime_listesi:
            st.session_state.kelime_listesi = random.sample(osym_dogru_kelimeler, 10)
            st.balloons()
        
        st.rerun()

st.markdown("---")
st.metric("Doğru Bilinen Kelime", st.session_state.dogru_sayisi)

if st.button("Listeyi Yenile / Sıfırla"):
    st.session_state.kelime_listesi = random.sample(osym_dogru_kelimeler, 10)
    st.session_state.dogru_sayisi = 0
    st.rerun()
