#!/bin/bash
# Twitter/X Video Indirici - Kurulum Scripti
# Tum Linux distrolari icin

set -e

RENK_YESIL='\033[0;32m'
RENK_KIRMIZI='\033[0;31m'
RENK_SARI='\033[1;33m'
RENK_NORMAL='\033[0m'

echo "========================================="
echo "  Twitter/X Video Indirici - Kurulum"
echo "========================================="
echo ""

# Kullanici kontrolu
if [ "$EUID" -eq 0 ]; then
    echo -e "${RENK_KIRMIZI}HATA: Bu scripti root olarak calistirmayin!${RENK_NORMAL}"
    exit 1
fi

KURULUM_KLASORU="$HOME/.local/share/twitter-indirici"
MASAUSTU="$HOME/Masaüstü"
UYGULAMALAR="$HOME/.local/share/applications"
IKON_KLASORU="$HOME/.local/share/icons/hicolor"

# 1. Bagimlilik kontrolu
echo -e "${RENK_SARI}1. Bagimliliklar kontrol ediliyor...${RENK_NORMAL}"

EKSIK=0

# Python3
if ! command -v python3 &> /dev/null; then
    echo -e "  ${RENK_KIRMIZI}X python3 bulunamadi${RENK_NORMAL}"
    EKSIK=1
else
    echo -e "  ${RENK_YESIL}✓ python3${RENK_NORMAL}"
fi

# pip
if ! command -v pip3 &> /dev/null; then
    echo -e "  ${RENK_KIRMIZI}X pip3 bulunamadi${RENK_NORMAL}"
    EKSIK=1
else
    echo -e "  ${RENK_YESIL}✓ pip3${RENK_NORMAL}"
fi

# yt-dlp
if ! command -v yt-dlp &> /dev/null; then
    echo -e "  ${RENK_SARI}! yt-dlp yukleniyor...${RENK_NORMAL}"
    pip3 install --user yt-dlp 2>/dev/null || {
        echo -e "  ${RENK_KIRMIZI}X yt-dlp yuklenemedi${RENK_NORMAL}"
        EKSIK=1
    }
fi
if command -v yt-dlp &> /dev/null; then
    echo -e "  ${RENK_YESIL}✓ yt-dlp${RENK_NORMAL}"
fi

# ffmpeg
if ! command -v ffmpeg &> /dev/null; then
    echo -e "  ${RENK_SARI}! ffmpeg yukleniyor...${RENK_NORMAL}"
    # Distro'ya gore kurulum
    if command -v dnf &> /dev/null; then
        sudo dnf install -y ffmpeg 2>/dev/null || true
    elif command -v apt &> /dev/null; then
        sudo apt install -y ffmpeg 2>/dev/null || true
    elif command -v pacman &> /dev/null; then
        sudo pacman -S --noconfirm ffmpeg 2>/dev/null || true
    elif command -v zypper &> /dev/null; then
        sudo zypper install -y ffmpeg 2>/dev/null || true
    fi
fi
if command -v ffmpeg &> /dev/null; then
    echo -e "  ${RENK_YESIL}✓ ffmpeg${RENK_NORMAL}"
else
    echo -e "  ${RENK_KIRMIZI}X ffmpeg bulunamadi (manuel kurun: sudo apt/dnf/pacman install ffmpeg)${RENK_NORMAL}"
    EKSIK=1
fi

# tkinter
if ! python3 -c "import tkinter" 2>/dev/null; then
    echo -e "  ${RENK_SARI}! tkinter yukleniyor...${RENK_NORMAL}"
    if command -v dnf &> /dev/null; then
        sudo dnf install -y python3-tkinter 2>/dev/null || true
    elif command -v apt &> /dev/null; then
        sudo apt install -y python3-tk 2>/dev/null || true
    elif command -v pacman &> /dev/null; then
        sudo pacman -S --noconfirm tk 2>/dev/null || true
    fi
fi
if python3 -c "import tkinter" 2>/dev/null; then
    echo -e "  ${RENK_YESIL}✓ tkinter${RENK_NORMAL}"
else
    echo -e "  ${RENK_KIRMIZI}X tkinter bulunamadi${RENK_NORMAL}"
    EKSIK=1
fi

if [ $EKSIK -eq 1 ]; then
    echo ""
    echo -e "${RENK_KIRMIZI}Eksik bagimliliklar var. Lutfen yukleyin ve tekrar deneyin.${RENK_NORMAL}"
    exit 1
fi

# 2. Dosyalari kopyala
echo ""
echo -e "${RENK_SARI}2. Dosyalar kuruluyor...${RENK_NORMAL}"

mkdir -p "$KURULUM_KLASORU"

# Script dizinindeki dosyalari bul
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Python dosyasini kopyala
cp "$SCRIPT_DIR/twitter-indirici.py" "$KURULUM_KLASORU/"
chmod +x "$KURULUM_KLASORU/twitter-indirici.py"

# Icon dosyalarini kopyala
for boyut in 16 32 48 64 128 256 512; do
    if [ -f "$SCRIPT_DIR/download-icon-${boyut}.png" ]; then
        cp "$SCRIPT_DIR/download-icon-${boyut}.png" "$KURULUM_KLASORU/"
    fi
done
[ -f "$SCRIPT_DIR/download-icon.svg" ] && cp "$SCRIPT_DIR/download-icon.svg" "$KURULUM_KLASORU/"
[ -f "$SCRIPT_DIR/download-icon.ico" ] && cp "$SCRIPT_DIR/download-icon.ico" "$KURULUM_KLASORU/"

echo -e "  ${RENK_YESIL}✓ Dosyalar kopyalandi${RENK_NORMAL}"

# 3. .desktop dosyasi olustur
echo -e "${RENK_SARI}3. Masaustu kisayolu olusturuluyor...${RENK_NORMAL}"

mkdir -p "$UYGULAMALAR"

cat > "$UYGULAMALAR/twitter-indirici.desktop" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Twitter/X Video Indirici
Comment=Tweet video/GIF indir (yt-dlp)
Exec=python3 $KURULUM_KLASORU/twitter-indirici.py
Icon=$KURULUM_KLASORU/download-icon-48.png
Terminal=false
Categories=Utility;AudioVideo;
StartupNotify=true
EOF

chmod +x "$UYGULAMALAR/twitter-indirici.desktop"

# 4. Iconlari sistem klasorune kopyala
echo -e "${RENK_SARI}4. Iconlar ayarlaniyor...${RENK_NORMAL}"

for boyut in 16 32 48 64 128; do
    if [ -f "$KURULUM_KLASORU/download-icon-${boyut}.png" ]; then
        mkdir -p "$IKON_KLASORU/${boyut}x${boyut}/apps/"
        cp "$KURULUM_KLASORU/download-icon-${boyut}.png" "$IKON_KLASORU/${boyut}x${boyut}/apps/twitter-indirici.png"
    fi
done

# Icon cache guncelle
gtk-update-icon-cache -f -t "$IKON_KLASORU" 2>/dev/null || true

# 5. Masaustu kisayolu
if [ -d "$MASAUSTU" ]; then
    cp "$UYGULAMALAR/twitter-indirici.desktop" "$MASAUSTU/"
    chmod +x "$MASAUSTU/twitter-indirici.desktop"
    echo -e "  ${RENK_YESIL}✓ Masaustu kisayolu olusturuldu${RENK_NORMAL}"
fi

# 6. PATH'e ekle (opsiyonel)
BIN_KLASORU="$HOME/.local/bin"
mkdir -p "$BIN_KLASORU"
cat > "$BIN_KLASORU/twitter-indirici" << 'EOF'
#!/bin/bash
exec python3 "$HOME/.local/share/twitter-indirici/twitter-indirici.py" "$@"
EOF
chmod +x "$BIN_KLASORU/twitter-indirici"

# .bashrc'ye PATH ekle (eğer yoksa)
if ! grep -q ".local/bin" ~/.bashrc 2>/dev/null; then
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
fi

echo ""
echo "========================================="
echo -e "  ${RENK_YESIL}Kurulum tamamlandi!${RENK_NORMAL}"
echo "========================================="
echo ""
echo "  Calistirmak icin:"
echo "    - Masaustu kisayoluna tiklayin"
echo "    - veya: twitter-indirici"
echo "    - veya: python3 $KURULUM_KLASORU/twitter-indirici.py"
echo ""
echo "  Kaldirmak icin:"
echo "    rm -rf $KURULUM_KLASORU"
echo "    rm $UYGULAMALAR/twitter-indirici.desktop"
echo "    rm $MASAUSTU/twitter-indirici.desktop"
echo "    rm $BIN_KLASORU/twitter-indirici"
echo ""
