# Degisiklik Kaydi

## v1.6K2 (2026-08-25)

### Kritik Duzeltmeler
- **Guncelleme mekanizmasi tamamen yeniden yazildi**
- **Versiyon ayristirma hatasi duzeltildi** — "1.6K" gibi ekli versiyonlari dogru parse eder
- **GitHub API dogru kullaniliyor** — Release asset'lerinden dogru download URL aliniyor
- **SHA256 dogrulama eklendi** — Indirilen EXE'nin hash'i GitHub digest ile karsilastiriliyor
- **Progress gosterimi** — Indirme sirasinda yuzde bazli ilerleme gosterilir
- **User-Agent header** — GitHub API rate-limit onlenir
- **EXE guncelleme (Windows)** — Batch script ile guvenli degistirme (calisan EXE uzerine yazi)
- **Hata temizleme** — Basarisiz indirmelerde gecici dosyalar temizlenir
- **Ayrintili loglama** — Her adim log dosyasina yazilir

### Iyilestirmeler
- Daha anlamlı hata mesajlari
- Internet baglantisi hatasi ayri yakalanir
- Dogrulama basarisizsa indirilen dosya silinir

---

## v1.6K (2026-08-25)

### Kritik Duzeltmeler
- **self.master hatasi duzeltildi** — Guncelleme sonrasi program cope atma hatasi giderildi
- **_iptal() duzeltildi** — Iptal edildiginde arka plan process'i artik dogru olduruluyor
- **GitHub Actions permissions eklendi** — Release olusturma artik calisacak
- **Versiyon tutarsizligi giderildi** — Tum dosyalarda v1.6K olarak guncellendi

### Iyilestirmeler
- Iptal butonu artik durumunu dogru guncelliyor
- Process yonetimi guclendirildi

---

## v1.5.3 (2026-08-25)

### Yeni Ozellikler
- **Otomatik guncelleme** — Yeni versiyonu GitHub'dan ceker, yedekler, gunceller, yeniden baslatir
- **Cookie hatasi cozumu** — Chrome acikken cookie hatasi alinirsa cookiesiz devam eder
- **Windows tarayici algilama** — Chrome, Edge, Firefox, Brave, Opera, Vivaldi

### Duzeltmeler
- Guncelleme: EXE indirme → dogrudan .py kodu guncelleme
- Cookie hatasi: coinsiz fallback eklendi
- README v1.5.3 guncellendi

---

## v1.5.1 (2026-08-24)

### Windows
- **Multi-Downloader.exe** — Kurulumsuz Windows versiyonu (84MB)
- yt-dlp ve ffmpeg dahil
- Tek dosya, Python gerekmez

### Duzeltmeler
- Help menusu messagebox ile degistirildi
- Guncelleme kontrolu: git ls-remote kullanildi
- Dil menu: Ulke isimleri duzeltildi
- Guvenlik analizi tamamlandi

---

## v1.5 (2026-08-24)

### Yeni Ozellikler
- **Multi Downloader** olarak yeniden adlandirma
- **Coklu platform destegi** — YouTube, Instagram, TikTok, Facebook, Twitter/X, Reddit, Pinterest, Vimeo, Dailymotion, Twitch ve 1000+ site
- **Platform otomatik algilama** — Linki yapistirin, platformu otomatik tanir
- **Yeni multi-platform icon** — 4 platform simgesi (YouTube, Instagram, TikTok, Twitter)

### Iyilestirmeler
- Tum dil cevirileri guncellendi
- URL etiketi tum platformlari gosterecek sekilde genisletildi

---

## v1.4 (2026-08-24)

### Yeni Ozellikler
- Otomatik tarayici algilama
- Kurulum scripti (kur.sh)
- 7 dil destegi

---

## v1.3 (2026-08-24)

### Yeni Ozellikler
- Coklu dil destegi (7 dil)
- Bayrakli dil secici
- Help menusu

---

## v1.2 (2026-08-24)

### Yeni Ozellikler
- Tum tarayicilar destekleniyor
- Linux dagitim listesi

---

## v1.1 (2026-08-24)

### Iyilestirmeler
- Brave tarayici destegi
- Turkce hata mesajlari

---

## v1.0 (2026-08-24)

### Ilk versiyon
- Temel video indirme
- Cozunurluk secimi
- GUI arayuzu
