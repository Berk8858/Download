# Twitter/X Video Indirici

Tweet, video ve GIF'leri kolayca indirin.

![Versiyon](https://img.shields.io/badge/versiyon-1.4-blue)
![Lisans](https://img.shields.io/badge/lisans-MIT-green)
![Linux](https://img.shields.io/badge/linux-tum%C3%BC%20dag%C4%B1t%C4%B1mlar-yellow)

## Ozellikler

- Tweet video ve GIF'lerini indirme
- Cozunurluk secimi (otomatik en iyi kalite)
- Sadece ses indirme (MP3)
- Coklu dil destegi (7 dil)
- Otomatik tarayici algilama
- Modern GUI arayuzu

## Kurulum

### Yontem 1: Otomatik Kurulum (Onerilen)

```bash
# Dosyalari indirin ve calistirin
git clone https://github.com/Berk8858/Download.git
cd Download
bash kur.sh
```

### Yontem 2: Manuel Kurulum

```bash
# Bagimliliklari yukleyin
pip3 install --user yt-dlp
sudo apt install ffmpeg python3-tk  # Debian/Ubuntu
sudo dnf install ffmpeg python3-tkinter  # Fedora

# Programi calistirin
python3 twitter-indirici.py
```

## Kullanim

1. Tweet linkini yapistirin
2. "Cozunurlukleri Getir" butonuna tiklayin
3. Istediniz cozunurlugu secin
4. "INDIR" butonuna tiklayin

## Gereksinimler

- Python 3.8+
- yt-dlp
- ffmpeg
- tkinter

## Desteklenen Diller

- Turkce
- Ispanyolca
- Portekizce
- Italyanca
- Japonca
- Korece
- Cince

## Lisans

MIT License
