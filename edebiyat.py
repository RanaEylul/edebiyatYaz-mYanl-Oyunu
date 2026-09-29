import tkinter as tk
from tkinter import ttk, messagebox
import random

class PratikUygulamasi:
    def __init__(self, root):
        self.root = root
        self.root.title("Yazım ve Noktalama Pratik Stüdyosu")
        self.root.geometry("750x550")
        self.root.config(bg="#f4f6f9")

        # Örnek Veri Tabanı (Yazım Yanlışları & Doğruları)
        self.yazim_sorulari = [
            {"soru": "herkes", "yanlis": "herkez", "ipucu": "Sonsuz ünsüzlerden 's' ile biter."},
            {"soru": "yalnız", "yanlis": "yanlız", "ipucu": " Yalın kelimesinden türemiştir."},
            {"soru": "yanlış", "yanlis": "yalnış", "ipucu": "Yanılmak kelimesinden türemiştir."},
            {"soru": "doküman", "yanlis": "doküman", "ipucu": "Fransızcadan gelen kelimelerde 'k' kullanılır."},
            {"soru": "birçok", "yanlis": "bir çok", "ipucu": "Bitişik yazılır."},
            {"soru": "herhangi", "yanlis": "her hangi", "ipucu": "Bitişik yazılır."}
        ]

        # Örnek Veri Tabanı (Noktalama İşaretleri)
        self.noktalama_sorulari = [
            {"cumle": "Ankara'ya yarın gideceğim", "aciklama": "Özel isimlere gelen ekler kesme işaretiyle ayrılır."},
            {"cumle": "Kitabını, defterini ve kalemini aldı.", "aciklama": "Eş görevli kelimeler arasına virgül konur."},
            {"cumle": "Eyvah, geç kaldım!", "aciklama": "Ünlem bildiren kelimelerden sonra virgül, cümlenin sonuna ünlem konur."}
        ]

        self.secilen_sure = 30  # Varsayılan süre
        self.kalan_sure = 30
        self.timer_aktif = False

        # Sekme Yapısı (Notebook)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Sekmeler
        self.tab_yazim = ttk.Frame(self.notebook)
        self.tab_noktalama = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_yazim, text="✏️ Yazım Kuralları Pratiği")
        self.notebook.add(self.tab_noktalama, text="📌 Noktalama İşaretleri Pratiği")

        self.ArayuzYazimOlustur()
        self.ArayuzNoktalamaOlustur()

    def ArayuzYazimOlustur(self):
        # Başlık
        lbl_baslik = tk.Label(self.tab_yazim, text="Yazım Yanlışları Pratiği", font=("Arial", 16, "bold"), bg="#f4f6f9", fg="#333")
        lbl_baslik.pack(pady=15)

        # Süre Seçimi
        frame_sure = tk.Frame(self.tab_yazim, bg="#f4f6f9")
        frame_sure.pack(pady=5)
        tk.Label(frame_sure, text="Süre Seçin: ", font=("Arial", 11), bg="#f4f6f9").pack(side=tk.LEFT)
        
        self.sure_var = tk.StringVar(value="30")
        for s in ["30", "60", "90"]:
            rb = tk.Radiobutton(frame_sure, text=f"{s} Saniye", variable=self.sure_var, value=s, command=self.SureGuncelle, bg="#f4f6f9")
            rb.pack(side=tk.LEFT, padx=5)

        self.lbl_timer = tk.Label(self.tab_yazim, text="Kalan Süre: 30 sn", font=("Arial", 12, "bold"), fg="#e74c3c", bg="#f4f6f9")
        self.lbl_timer.pack(pady=5)

        # Soru Alanı
        self.lbl_soru_gosterge = tk.Label(self.tab_yazim, text="Kelimenin DOĞRU halini yazın:", font=("Arial", 12), bg="#f4f6f9")
        self.lbl_soru_gosterge.pack(pady=10)

        self.lbl_kelime = tk.Label(self.tab_yazim, text="", font=("Arial", 22, "bold"), fg="#2980b9", bg="#f4f6f9")
        self.lbl_kelime.pack(pady=10)

        # Giriş Kutusu
        self.entry_yazim = tk.Entry(self.tab_yazim, font=("Arial", 16), justify="center", width=25)
        self.entry_yazim.pack(pady=10)
        self.entry_yazim.bind("<Return>", self.YazimKontrolEt)

        # Başlat Butonu
        self.btn_baslat = tk.Button(self.tab_yazim, text="Pratiği Başlat", font=("Arial", 12, "bold"), bg="#2ecc71", fg="white", padx=15, pady=5, command=self.YazimPratikBaslat)
        self.btn_baslat.pack(pady=15)

        self.lbl_yazim_sonuc = tk.Label(self.tab_yazim, text="", font=("Arial", 12), bg="#f4f6f9")
        self.lbl_yazim_sonuc.pack(pady=5)

    def ArayuzNoktalamaOlustur(self):
        # Başlık
        lbl_baslik = tk.Label(self.tab_noktalama, text="Noktalama İşaretleri Pratiği", font=("Arial", 16, "bold"), bg="#f4f6f9", fg="#333")
        lbl_baslik.pack(pady=15)

        tk.Label(self.tab_noktalama, text="Aşağıdaki cümleyi doğru noktalama işaretleriyle tekrar yazın:", font=("Arial", 12), bg="#f4f6f9").pack(pady=10)

        self.lbl_nokta_cumle = tk.Label(self.tab_noktalama, text="Cümle buraya gelecek...", font=("Arial", 14, "italic"), fg="#8e44ad", bg="#f4f6f9")
        self.lbl_nokta_cumle.pack(pady=10)

        self.entry_nokta = tk.Entry(self.tab_noktalama, font=("Arial", 14), width=45)
        self.entry_nokta.pack(pady=10)

        btn_nokta_kontrol = tk.Button(self.tab_noktalama, text="Kontrol Et", font=("Arial", 12, "bold"), bg="#3498db", fg="white", padx=15, pady=5, command=self.NoktalamayiKontrolEt)
        btn_nokta_kontrol.pack(pady=15)

        self.lbl_nokta_sonuc = tk.Label(self.tab_noktalama, text="", font=("Arial", 12), bg="#f4f6f9")
        self.lbl_nokta_sonuc.pack(pady=5)

        self.YeniNoktalamaSorusuGetir()

    def SureGuncelle(self):
        self.secilen_sure = int(self.sure_var.get())
        self.kalan_sure = self.secilen_sure
        self.lbl_timer.config(text=f"Kalan Süre: {self.kalan_sure} sn")

    def YazimPratikBaslat(self):
        self.SureGuncelle()
        self.timer_aktif = True
        self.YeniYazimSorusuGetir()
        self.btn_baslat.config(state=tk.DISABLED)
        self.GeriSayimBaslat()

    def GeriSayimBaslat(self):
        if self.timer_aktif and self.kalan_sure > 0:
            self.kalan_sure -= 1
            self.lbl_timer.config(text=f"Kalan Süre: {self.kalan_sure} sn")
            self.root.after(1000, self.GeriSayimBaslat)
        elif self.kalan_sure == 0 and self.timer_aktif:
            self.timer_aktif = False
            self.btn_baslat.config(state=tk.NORMAL)
            messagebox.showinfo("Süre Bitti", "Pratik süreniz tamamlandı! Tebrikler.")

    def YeniYazimSorusuGetir(self):
        secim = random.choice(self.yazim_sorulari)
        self.aktif_dogru_kelime = secim["soru"]
        # Ekrana yanlış yazılışını veya ipucunu yansıtarak doğrusunu isteyelim
        self.lbl_kelime.config(text=f"Yanlış Hali: {secim['yanlis']} (İpucu: {secim['ipucu']})")
        self.entry_yazim.delete(0, tk.END)

    def YazimKontrolEt(self, event=None):
        if not self.timer_aktif:
            return
        
        kullanici_cevabi = self.entry_yazim.get().strip().lower()
        if kullanici_cevabi == self.aktif_dogru_kelime:
            self.lbl_yazim_sonuc.config(text="✅ Doğru!", fg="green")
        else:
            self.lbl_yazim_sonuc.config(text=f"❌ Yanlış! Doğrusu: {self.aktif_dogru_kelime}", fg="red")
        
        self.YeniYazimSorusuGetir()

    def YeniNoktalamaSorusuGetir(self):
        self.aktif_nokta_soru = random.choice(self.noktalama_sorulari)
        self.lbl_nokta_cumle.config(text=self.aktif_nokta_soru["cumle"])
        self.entry_nokta.delete(0, tk.END)

    def NoktalamayiKontrolEt(self):
        # Basit bir kontrol simülasyonu
        kullanici_cevabi = self.entry_nokta.get().strip()
        if len(kullanici_cevabi) > 5:
            self.lbl_nokta_sonuc.config(text="🎉 Harika, noktalama kurallarına dikkat ettin!", fg="green")
            self.root.after(1500, self.YeniNoktalamaSorusuGetir)
        else:
            self.lbl_nokta_sonuc.config(text="⚠️ Lütfen eksiksiz bir şekilde yazmayı dene.", fg="orange")

if __name__ == "__main__":
    root = tk.Tk()
    app = PratikUygulamasi(root)
    root.mainloop()