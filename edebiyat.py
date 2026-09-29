import streamlit as st
import random

# Sayfa Yapılandırması ve Coderspace/Monkeytype Teması
st.set_page_config(
    page_title="ÖSYM Yazım Hızı Pratiği - Coderspace",
    page_icon="⌨️",
    layout="wide"
)

# Gönderdiğin ekran görüntüsündeki koyu tema ve tasarımın CSS kodları
st.markdown("""
    <style>
    .stApp {
        background-color: #13111c;
        color: #d1d0c5;
    }
    h1, h2, h3, p, span, label {
        color: #d1d0c5 !important;
    }
    .kelime-kutu {
        background-color: #1a1625;
        border: 1px solid #2c2738;
        border-radius: 16px;
        padding: 30px;
        font-family: 'Courier New', monospace;
        font-size: 26px;
        line-height: 1.8;
        color: #646669;
        letter-spacing: 1px;
        margin-bottom: 25px;
    }
    .aktif-kelime {
        color: #d1d0c5;
        border-bottom: 2px solid #e2b714;
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
    "başyapıt", "taşeron", "mütevazi", "akıbet", "özveri",
    "tespit", "sezgi", "makine", "unutulmaz", "öngörü"
]

# Oturum Durumu Yönetimi
if "kelime_listesi" not in st.session_state:
    st.session_state.kelime_listesi = random.sample(osym_dogru_kelimeler, 20)
if "dogru_sayisi" not in st.session_state:
    st.session_state.dogru_sayisi = 0
if "toplam_deneme" not in st.session_state:
    st.session_state.toplam_deneme = 0

# --- ÜST MENÜ (Süreler ve Yeniden Başlat) ---
col_m1, col_m2, col_m3 = st.columns([3, 3, 2])

with col_m1:
    st.markdown("### ⚡ ÖSYM Yazım Stüdyosu")

with col_m2:
    # Süre Seçimi (15sn, 30sn, 60sn, 120sn, 180sn)
    secilen_sure = st.radio(
        "Süre Seçin:", 
        [15, 30, 60, 120, 180], 
        index=2, 
        horizontal=True,
        label_visibility="collapsed"
    )

with col_m3:
    if st.button("🔄 Yeniden Başlat"):
        st.session_state.kelime_listesi = random.sample(osym_dogru_kelimeler, 20)
        st.session_state.dogru_sayisi = 0
        st.session_state.toplam_deneme = 0
        st.rerun()

st.markdown("---")

# --- İSTATİSTİK KARTLARI (WPM, Doğruluk, Süre vb.) ---
c1, c2, c3, c4 = st.columns(4)
c1.metric("WPM (Kelime/Dakika)", f"{st.session_state.dogru_sayisi * 2}")
c2.metric("Doğruluk", "%100" if st.session_state.toplam_deneme == 0 else f"%{int((st.session_state.dogru_sayisi/st.session_state.toplam_deneme)*100)}")
c3.metric("Seçilen Süre", f"{secilen_sure} sn")
c4.metric("Doğru / Toplam", f"{st.session_state.dogru_sayisi} / {st.session_state.toplam_deneme}")

st.markdown("<br>", unsafe_allow_html=True)

# --- ORTA KELİME AKIŞ ALANI (Coderspace Görünümü) ---
gosterilecek_metinler = []
for i, k in enumerate(st.session_state.kelime_listesi):
    if i == 0:
        gosterilecek_metinler.append(f"<span class='aktif-kelime'>{k}</span>")
    else:
        gosterilecek_metinler.append(f"<span>{k}</span>")

akıs_html = " &nbsp;&nbsp; ".join(gosterilecek_metinler)
st.markdown(f'<div class="kelime-kutu">{akıs_html}</div>', unsafe_allow_html=True)

# --- YAZMA VE KONTROL ALANI ---
with st.form(key="coderspace_yazma_formu", clear_on_submit=True):
    kullanici_girdisi = st.text_input(
        "Yukarıda sarı çizgili olan kelimeyi yaz ve Enter'a bas:", 
        placeholder="Yazmaya başla ve enterla...",
        label_visibility="collapsed"
    )
    submit_btn = st.form_submit_button("Kelimeyi Gönder")

    if submit_btn and kullanici_girdisi:
        st.session_state.toplam_deneme += 1
        hedef = st.session_state.kelime_listesi[0]
        
        if kullanici_girdisi.strip().lower() == hedef:
            st.session_state.dogru_sayisi += 1
            st.session_state.kelime_listesi.pop(0) # Doğru bilineni listeden düşür, yenisi gelsin
        else:
            # Yanlış yazıldığında da ilerlesin ama uyarı versin
            st.warning(f"Doğrusu '{hedef}' olacaktı.")
            st.session_state.kelime_listesi.pop(0)

        # Liste azalırsa yenilerini ekle
        if len(st.session_state.kelime_listesi) < 5:
            st.session_state.kelime_listesi.extend(random.sample(osym_dogru_kelimeler, 15))
            
        st.rerun()

# --- EN ALTAKİ SANAL KLAVYE GÖRSELİ (Ekran Görüntüsündeki Gibi) ---
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
    <div style="display: flex; justify-content: center; gap: 5px; opacity: 0.6; font-family: monospace;">
        <span style="background: #1a1625; padding: 8px 12px; border-radius: 6px; border: 1px solid #2c2738;">Q</span>
        <span style="background: #1a1625; padding: 8px 12px; border-radius: 6px; border: 1px solid #2c2738;">W</span>
        <span style="background: #1a1625; padding: 8px 12px; border-radius: 6px; border: 1px solid #2c2738;">E</span>
        <span style="background: #1a1625; padding: 8px 12px; border-radius: 6px; border: 1px solid #2c2738;">R</span>
        <span style="background: #1a1625; padding: 8px 12px; border-radius: 6px; border: 1px solid #2c2738;">T</span>
        <span style="background: #1a1625; padding: 8px 12px; border-radius: 6px; border: 1px solid #2c2738;">Y</span>
        <span style="background: #1a1625; padding: 8px 12px; border-radius: 6px; border: 1px solid #2c2738;">U</span>
        <span style="background: #1a1625; padding: 8px 12px; border-radius: 6px; border: 1px solid #2c2738;">I</span>
        <span style="background: #1a1625; padding: 8px 12px; border-radius: 6px; border: 1px solid #2c2738;">O</span>
        <span style="background: #1a1625; padding: 8px 12px; border-radius: 6px; border: 1px solid #2c2738;">P</span>
        <span style="background: #1a1625; padding: 8px 12px; border-radius: 6px; border: 1px solid #2c2738;">Ğ</span>
        <span style="background: #1a1625; padding: 8px 12px; border-radius: 6px; border: 1px solid #2c2738;">Ü</span>
    </div>
""", unsafe_allow_html=True)
