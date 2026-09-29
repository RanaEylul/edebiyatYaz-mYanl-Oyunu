import streamlit as st
import random

# Sayfa Yapılandırması
st.set_page_config(
    page_title="Yazım ve Noktalama Pratik Stüdyosu",
    page_icon="✍️",
    layout="centered"
)

# Oturum Durumu (State) Tanımlamaları
if "yazim_skor" not in st.session_state:
    st.session_state.yazim_skor = 0
if "yazim_soru_index" not in st.session_state:
    st.session_state.yazim_soru_index = 0
if "aktif_yazim_sorusu" not in st.session_state:
    st.session_state.aktif_yazim_sorusu = None

# Örnek Veri Tabanı (Yazım Yanlışları & Doğruları)
yazim_sorulari = [
    {"soru": "herkes", "yanlis": "herkez", "ipucu": "Sonsuz ünsüzlerden 's' ile biter."},
    {"soru": "yalnız", "yanlis": "yanlız", "ipucu": "Yalın kelimesinden türemiştir."},
    {"soru": "yanlış", "yanlis": "yalnış", "ipucu": "Yanılmak kelimesinden türemiştir."},
    {"soru": "doküman", "yanlis": "doküman", "ipucu": "Fransızcadan gelen kelimelerde 'k' kullanılır."},
    {"soru": "birçok", "yanlis": "bir çok", "ipucu": "Bitişik yazılır."},
    {"soru": "herhangi", "yanlis": "her hangi", "ipucu": "Bitişik yazılır."}
]

# Örnek Veri Tabanı (Noktalama İşaretleri)
noktalama_sorulari = [
    {"cumle": "Ankara'ya yarın gideceğim", "dogru": "Ankara'ya yarın gideceğim.", "aciklama": "Özel isimlere gelen ekler kesme işaretiyle ayrılır ve cümlenin sonuna nokta konur."},
    {"cumle": "Kitabını, defterini ve kalemini aldı", "dogru": "Kitabını, defterini ve kalemini aldı.", "aciklama": "Eş görevli kelimeler arasına virgül konur."},
    {"cumle": "Eyvah, geç kaldım", "dogru": "Eyvah, geç kaldım!", "aciklama": "Ünlem bildiren kelimelerden sonra virgül, cümlenin sonuna ünlem konur."}
]

# Başlık
st.title("✍️ Yazım ve Noktalama Pratik Stüdyosu")
st.write("Coderspace tarzı interaktif pratik yapma platformuna hoş geldin!")

# Sekme Yapısı (Tabs)
tab1, tab2 = st.tabs(["✏️ Yazım Kuralları Pratiği", "📌 Noktalama İşaretleri Pratiği"])

# ----------------- 1. SEKME: YAZIM KURALLARI -----------------
with tab1:
    st.header("Yazım Yanlışları Pratiği")
    
    # Süre seçimi (Görsel simülasyon veya bilgi amaçlı)
    sure = st.selectbox("Süre Seçimi:", [30, 60, 90], key="yazim_suresi")
    
    if st.button("Yeni Soru Getir / Başlat", key="btn_yazim_baslat"):
        st.session_state.aktif_yazim_sorusu = random.choice(yazim_sorulari)
        st.rerun()

    if st.session_state.aktif_yazim_sorusu:
        soru_datasi = st.session_state.aktif_yazim_sorusu
        st.info(f"**Yanlış Yazılışı:** {soru_datasi['yanlis']}")
        st.caption(f"💡 İpucu: {soru_datasi['ipucu']}")
        
        kullanici_cevabi = st.text_input("Kelimenin DOĞRU halini yazın:", key="yazim_input")
        
        if st.button("Kontrol Et", key="btn_yazim_kontrol"):
            if kullanici_cevabi.strip().lower() == soru_datasi["soru"]:
                st.success("🎉 Doğru! Harika gidiyorsun.")
                st.session_state.yazim_skor += 1
            else:
                st.error(f"❌ Yanlış. Doğrusu: **{soru_datasi['soru']}** olmalıydı.")
        
        st.write(f"🏆 Toplam Doğru Sayısı: {st.session_state.yazim_skor}")

# ----------------- 2. SEKME: NOKTALAMA İŞARETLERİ -----------------
with tab2:
    st.header("Noktalama İşaretleri Pratiği")
    st.write("Aşağıdaki eksik noktalı cümleyi uygun noktalama işaretlerini ekleyerek yeniden yazın:")
    
    if "aktif_nokta" not in st.session_state:
        st.session_state.aktif_nokta = random.choice(noktalama_sorulari)

    nokta_datasi = st.session_state.aktif_nokta
    st.warning(f"Cümle: **{nokta_datasi['cumle']}**")
    
    kullanici_nokta = st.text_input("Doğru halini buraya yazın:", key="nokta_input")
    
    if st.button("Noktalamayı Kontrol Et", key="btn_nokta_kontrol"):
        if kullanici_nokta.strip() == nokta_datasi["dogru"]:
            st.success("✅ Mükemmel! Noktalama kurallarını tam uyguladın.")
        else:
            st.info(f"💡 İpucu / Örnek Doğru Hali: {nokta_datasi['dogru']} ({nokta_datasi['aciklama']})")
            
    if st.button("Sonraki Soruya Geç", key="btn_nokta_degistir"):
        st.session_state.aktif_nokta = random.choice(noktalama_sorulari)
        st.rerun()
