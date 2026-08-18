# Download - Twitter/X Video Indirici

Twitter/X'ten video indirme aracı. Yapıştırılan tweet linkindeki mevcut çözünürlükleri listeler, seçilen kalitede indirir.

## Özellikler
- Link yapıştır (Paste butonu, sağ tık, Ctrl+V) ve Clear ile temizle
- Mevcut çözünürlükleri listele (En iyi kalite, 720p, 360p, 270p, Sadece ses MP3)
- Seçilen çözünürlükte indir
- İlerleme çubuğu ve durum göstergesi
- Kayıt klasörü seçimi (varsayılan: sistem indirme klasörü otomatik bulunur)
- İptal desteği

## Gereksinimler
- Python 3 + Tkinter
- yt-dlp
- ffmpeg

## Kurulum (Debian/Fedora tabanlı)
```bash
sudo apt install python3-tk ffmpeg   # Debian/Ubuntu
sudo dnf install python3-tk ffmpeg   # Fedora
pip install --user yt-dlp
```

## Kullanım
```bash
python3 download.py
```

## Hazır Kurulum (Linux - tek dosya)
Kaynak kodla uğraşmadan direkt çalıştırmak için **Releases** bölümünden indir:
`Download-linux-x86_64` (tek çalıştırılabilir dosya, ~50 MB)

```bash
chmod +x Download-linux-x86_64
./Download-linux-x86_64
```

Not: Tek dosya sürümü yt-dlp + ffmpeg'i kendi içinde barındırır, ayrı kurulum gerekmez.