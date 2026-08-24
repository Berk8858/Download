# Download

Twitter/X'ten video indirme aracı. Yapıştırılan tweet linkindeki mevcut çözünürlükleri listeler, seçilen kalitede indirir.

## v1.2 Güncelleme (2026-08-24)
- Tüm tarayıcılar destekleniyor
- Tarayıcı seçim dropdown'ı eklendi
- Otomatik tarayıcı algılama

## Desteklenen Tarayıcılar
| Tarayıcı | Durum |
|----------|-------|
| Firefox / Firefox ESR | ✅ |
| Google Chrome | ✅ |
| Chromium | ✅ |
| Brave Browser | ✅ |
| Microsoft Edge | ✅ |
| Opera / Opera GX | ✅ |
| Vivaldi | ✅ |

## Desteklenen Linux Dağıtımları
| Dağıtıma | Minimum Versiyon |
|----------|------------------|
| Fedora | 36+ |
| Ubuntu | 20.04+ |
| Debian | 11+ |
| Linux Mint | 20+ |
| Arch Linux / Manjaro | Rolling |
| openSUSE Leap | 15+ |
| Pop!_OS | 22.04+ |
| Elementary OS | 7+ |

## Özellikler
- Tweet/X linkinden video indirme
- Çözünurlük seçimi (en iyi kalite, 720p, 480p, sadece ses)
- Tarayıcı seçimi (otomatik algılama)
- Brave/Firefox/Chrome vb. cookies desteği
- Türkçe hata mesajları
- İlerleme çubuğu
- Otomatik dosya adlandırma

## Terminalden Kurulum

### Fedora
```bash
sudo dnf install python3-tkinter ffmpeg
pip install --user yt-dlp secretstorage
python3 twitter-indirici.py
```

### Debian / Ubuntu / Linux Mint
```bash
sudo apt install python3-tk ffmpeg
pip install --user yt-dlp secretstorage
python3 twitter-indirici.py
```

### Arch Linux / Manjaro
```bash
sudo pacman -S python tk ffmpeg
pip install --user yt-dlp secretstorage
python3 twitter-indirici.py
```

### openSUSE
```bash
sudo zypper install python3-tk ffmpeg
pip install --user yt-dlp secretstorage
python3 twitter-indirici.py
```

## Gereksinimler
- Python 3.8+
- tkinter (GUI)
- yt-dlp (video indirme)
- ffmpeg (video birlestirme)
- secretstorage (Linux keyring erisimi)

## Hazır Kurulum (Linux - tek dosya)
```bash
curl -sL https://github.com/Berk8858/Download/releases/latest/download/Download-linux-x86_64 -o Download
chmod +x Download
./Download
```

## Kaynak Kodu Klonla
```bash
git clone https://github.com/Berk8858/Download.git
cd Download
pip install --user yt-dlp secretstorage
python3 twitter-indirici.py
```

## ZIP İndir
```bash
wget https://github.com/Berk8858/Download/archive/refs/heads/main.zip
unzip main.zip && cd Download-main
pip install --user yt-dlp secretstorage
python3 twitter-indirici.py
```

## Versiyonlar
### v1.2 (2026-08-24)
- Tüm tarayıcılar destekleniyor (Firefox, Chrome, Brave, Edge, Opera, Vivaldi, Chromium)
- Tarayıcı seçim dropdown'ı
- Otomatik tarayıcı algılama

### v1.1 (2026-08-24)
- Brave tarayıcı desteği
- Türkçe hata mesajları

### v1.0
- İlk versiyon
- Firefox desteği
- Çözünurlük seçimi
- GUI arayüzü

## Lisans
MIT
