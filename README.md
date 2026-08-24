# Twitter/X Video Indirici

yt-dlp tabanlı, Python tkinter ile yazılmış video indirici.

## Özellikler

- Tweet/X linklerinden video indirme
- Çözünurlük seçimi (en iyi kalite, 720p, 480p, sadece ses)
- Brave tarayıcı cookies desteği
- Türkçe hata mesajları
- İlerleme çubuğu
- Otomatik dosya adlandırma

## Gereksinimler

```bash
pip install yt-dlp secretstorage
sudo dnf install ffmpeg
```

## Kullanım

```bash
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
