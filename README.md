# Download

Twitter/X'ten video indirme aracı. Yapıştırılan tweet linkindeki mevcut çözünürlükleri listeler, seçilen kalitede indirir.

## Özellikler
- Link yapıştır (Paste butonu, sağ tık, Ctrl+V) ve Clear ile temizle
- Mevcut çözünürlükleri listele (En iyi kalite, 720p, 360p, 270p, Sadece ses MP3)
- Seçilen çözünürlükte indir
- İlerleme çubuğu ve durum göstergesi
- Kayıt klasörü seçimi (varsayılan: sistem indirme klasörü otomatik bulunur)
- İptal desteği
- Brave tarayıcı cookies desteği
- Türkçe hata mesajları

## Gereksinimler
- Python 3 + Tkinter
- yt-dlp
- ffmpeg
- secretstorage (Brave cookies için)

## Kurulum (Debian/Fedora tabanlı)
```bash
sudo apt install python3-tk ffmpeg   # Debian/Ubuntu
sudo dnf install python3-tk ffmpeg   # Fedora
pip install --user yt-dlp secretstorage
```

## Kullanım
```bash
python3 twitter-indirici.py
```

## Hazır Kurulum (Linux - tek dosya)
Kaynak kodla uğraşmadan direkt çalıştırmak için **Releases** bölümünden indir:
`Download-linux-x86_64` (tek çalıştırılabilir dosya, ~50 MB)

```bash
chmod +x Download-linux-x86_64
./Download-linux-x86_64
```

Not: Tek dosya sürümü yt-dlp + ffmpeg'i kendi içinde barındırır, ayrı kurulum gerekmez.

## Terminalden İndirme ve Kurma

### Seçenek 1: Hazır tek dosya (önerilen)
```bash
curl -sL https://github.com/Berk8858/Download/releases/latest/download/Download-linux-x86_64 -o Download
chmod +x Download
./Download
```

### Seçenek 2: Kaynak kodu klonla
```bash
git clone https://github.com/Berk8858/Download.git
cd Download
pip install --user yt-dlp secretstorage
python3 twitter-indirici.py
```

### Seçenek 3: Repoyu ZIP indir (git olmadan)
```bash
wget https://github.com/Berk8858/Download/archive/refs/heads/main.zip
unzip main.zip && cd Download-main
pip install --user yt-dlp secretstorage
python3 twitter-indirici.py
```

## Versiyonlar

### v1.1 (2026-08-24)
- Brave tarayıcı desteği eklendi
- Türkçe hata mesajları eklendi
- `cookiesfrombrowser` özelliği

### v1.0
- İlk versiyon
- Firefox desteği
- Çözünurlük seçimi
- GUI arayüzü

## Lisans

MIT
