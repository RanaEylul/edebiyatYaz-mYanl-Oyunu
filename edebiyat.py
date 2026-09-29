import streamlit as st
import random

# Sayfa Yapılandırması
st.set_page_config(
    page_title="ÖSYM Hız ve Yazım Pratiği (Coderspace Modu)",
    page_icon="⚡",
    layout="centered"
)

# ÖSYM'de En Çok Çıkan / Karıştırılan Genişletilmiş Kelime Havuzu
osym_kelimeler = [
    {"dogru": "yalnız", "yanlis": "yanlız", "ipucu": "Yalın kelimesinden türemiştir."},
    {"dogru": "yanlış", "yanlis": "yalnış", "ipucu": "Yanılmak kelimesinden türemiştir."},
    {"dogru": "herkes", "yanlis": "herkez", "ipucu": "Sonsuz ünsüzlerden 's' ile biter."},
    {"dogru": "unvan", "yanlis": "üvan", "ipucu": "Başında 'n' harfi vardır."},
    {"dogru": "orijinal", "yanlis": "orjinal", "ipucu": "Araya 'i' harfi girer."},
    {"dogru": "kılavuz", "yanlis": "klavuz", "ipucu": "Arasında 'ı' harfi bulunur."},
    {"dogru": "şoför", "yanlis": "şöför", "ipucu": "Fransızcadan gelir, 'ö' ile yazılır."},
    {"dogru": "stajyer", "yanlis": "stajor", "ipucu": "Sonu '-yer' ile biter."},
    {"dogru": "laboratuvar", "yanlis": "laboratuar", "ipucu": "İçinde iki tane 'a' vardır."},
    {"dogru": "doküman", "yanlis": "döküman", "ipucu": "İlk harf düzdür ('doküman')."},
    {"dogru": "palyaço", "yanlis": "palyanço", "ipucu": "Doğrusu palyaçodur ('n' harfi yok)."},
    {"dogru": "akaryakıt", "yanlis": "akar yakıt", "ipucu": "Bitişik yazılır."},
    {"dogru": "birdenbire", "yanlis": "birden bire", "ipucu": "Bitişik yazılır."},
    {"dogru": "birkaç", "yanlis": "bir kaç", "ipucu": "Bitişik yazılır."},
    {"dogru": "pekçok", "yanlis": "pek çok", "ipucu": "Yazımına dikkat, genelde ayrı sanılır ama birleşik/ayrı kullanımına dikkat (pek çok ayrı yazılır, birçok bitişik). Doğrusu: pek çok / birçok."},
    {"dogru": "unvan", "yanlis": " ünvan", "ipucu": "Başında 'u' değil 'ü' değil, direkt unvan."},
    {"dogru": "hapishane", "yanlis": te "haphane", "ipucu": "Araya 'is' sesi girer."},
    {"dogru": "karpuz", "yanlis": "kabruz", "ipucu": "Sıralamaya dikkat."},
    {"dogru": "komite", "yanlis": "komit", "ipucu": "Sonu -e ile biter."},
    {"dogru": "unutkan", "yanlis": "unutgan", "ipucu": "Sert ünsüz uyumuna dikkat (-kan)."},
    {"dogru": "özgün", "yanlis": "öçgün", "ipucu": "Özgün (orijinal anlamında)."},
    {"dogru": "esrar", "yanlis": "israr", "ipucu": "Israr (diretme), esrar (gizli şey) farklıdır."},
    {"dogru": "kiprik", "yanlis": "kirpik", "ipucu": "Doğrusu 'kirpik'tir (p-r yer değiştirebilir tuzağına dikkat, kirpik düzdür)."},
    {"dogru": "poğaça", "yanlis": "pohça", "ipucu": "Yumuşak g (ğ) içerir."},
    {"dogru": "savrulmak", "yanlis": "savurmak", "ipucu": "Araya 'l' harfi alır."},
    {"dogru": "şehrazat", "yanlis": "şehrizat", "ipucu": "Orta hecesi a ile."}
]

# Oturum Durumu Yönetimi
if "oyun_aktif" not in st.session_state:
    st.session_state.oyun_aktif = False
if "dogru_sayisi" not in st.session_state:
    st.session_state.dogru_sayisi = 0
if "toplam_deneme" not in st.session_state:
    st.session_state.toplam_deneme = 0
if "aktif_kelime" not in st.session_state:
    st.session_state.aktif_kelime = random.choice(osym_kelimeler)

st.title("⚡ ÖSYM Yazım Hızı Pratiği (Coderspace Modu)")
st.markdown("Süreye karşı yarışarak ÖSYM'nin en çok tuzağa düşürdüğü kelimelerin **doğru yazılışlarını** seri bir şekilde yaz.")

# --- KONTROL PANELİ (Süre Seçimi ve Başlatma) ---
col_s1, col_s2 = st.columns([2, 1])

with col_s1:
    secilen_sure = st.selectbox(
        "⏱️ Pratik Süresini Seçin (Saniye):",
        [14, 30, 60, 120, 180],
        index=1  # Varsayılan 30 saniye
    )

with col_s2:
    st.write("")
    st.write("")
    baslat_btn = st.button("🚀 Pratiği Başlat", type="primary")

if baslat_btn:
    st.session_state.oyun_aktif = True
    st.session_state.dogru_sayisi = 0
    st.session_state.toplam_deneme = 0
    # Her başlatmada tamamen rastgele yeni bir kelime seçilir
    st.session_state.aktif_kelime = random.choice(osym_kelimeler)
    st.rerun()

# --- OYUN / PRATİK ALANI ---
if st.session_state.oyun_aktif:
    st.markdown("---")
    st.info(f"Seçilen Süre: **{secilen_sure} Saniye** | Seri bir şekilde kelimelerin DOĞRU halini yazıp Enter'a bas!")
    
    kelime_datasi = st.session_state.aktif_kelime
    
    # Coderspace tarzı büyük ve dikkat çekici yanlış gösterimi
    st.markdown(f"### Karıştırılan / Yanlış Hali:")
    st.error(f"## ❌ {kelime_datasi['yanlis'].upper()}")
    st.caption(f"💡 İpucu: {kelime_datasi['ipucu']}")

    # Form kullanarak Enter tuşuna basıldığında hızlı akış sağlanması
    with st.form(key="hizli_yazma_formu", clear_on_submit=True):
        kullanici_girdisi = st.text_input("Kelimenin DOĞRU halini yazın ve Enter'a basın:", placeholder="Buraya yazıp enterla...")
        gonder = st.form_submit_button("Gönder / Sonraki")

        if gonder:
            st.session_state.toplam_deneme += 1
            if kullanici_girdisi.strip().lower() == kelime_datasi["dogru"]:
                st.session_state.dogru_sayisi += 1
                st.success("Doğru! 🎯")
            else:
                st.warning(f"Yanlıştı! Doğrusu: **{kelime_datasi['dogru']}** olacaktı.")
            
            # Her gönderimden sonra havuzdan rastgele başka bir kelime getir
            st.session_state.aktif_kelime = random.choice(osym_kelimeler)
            st.rerun()

    # Skor Tablosu
    st.markdown("---")
    col_m1, col_m2 = st.columns(2)
    col_m1.metric("Toplam Kelime", st.session_state.toplam_deneme)
    col_m2.metric("Doğru Bilinen", st.session_state.dogru_sayisi)

    if st.button("Pratiği Bitir / Sıfırla"):
        st.session_state.oyun_aktif = False
        st.rerun()
else:
    st.markdown("---")
    st.warning("Pratiğe başlamak için yukarıdan süreyi seçip **'Pratiği Başlat'** butonuna tıkla!")
