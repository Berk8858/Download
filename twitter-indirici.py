#!/usr/bin/env python3
"""
Multi Downloader - GUI
yt-dlp tabanli coklu platform video indirici

=== VERSIYON v1.6K6 (2026-08-26) ===

DESTEKLENEN PLATFORMLAR:
  YouTube, Instagram, TikTok, Facebook, Twitter/X, Reddit,
  Pinterest, Vimeo, Dailymotion, Twitch, ve 1000+ site (yt-dlp)

DEGISIKLIKLER:
  - v1.6K6: Acik/Koyu tema secenegi (Gorunum menusu, JSON tercihi)
  - v1.5: Multi Downloader olarak yeniden adlandirma
  - v1.5: Coklu platform destegi (YouTube, Instagram, TikTok, vb.)
  - v1.5: Platform otomatik algilama
  - v1.5: Desteklenen platformlar listesi
  - v1.4: Otomatik tarayici algilama
  - v1.4: Kurulum scripti (kur.sh)
  - v1.3: Coklu dil destegi (7 dil)
  - v1.2: Tum tarayicilar destekleniyor
  - v1.0: Ilk versiyon

Lisans: MIT
"""

import os
import json
import locale
import shutil
import subprocess
import sys
import queue
import threading
from pathlib import Path

# PyInstaller frozen bundle kontrolu
if getattr(sys, 'frozen', False):
    BUNDLE_DIR = Path(sys._MEIPASS)
    os.environ["PATH"] = str(BUNDLE_DIR) + os.pathsep + os.environ.get("PATH", "")
else:
    BUNDLE_DIR = None

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinter.scrolledtext import ScrolledText

try:
    from yt_dlp import YoutubeDL
    HAS_YTDLP = True
except ImportError:
    HAS_YTDLP = False
    # PyInstaller bundle'da yt-dlp modulu bulunamadi
    # yt-dlp.exe subprocess ile kullanilacak

# ============================================================
# VERSIYON
# ============================================================
VERSION = "1.6K6"
APP_NAME = "Multi Downloader"
GITHUB_URL = "https://github.com/Berk8858/Download"

# ============================================================
# BAYRAK KODLARI (emoji desteksiz ortamlar icin)
# ============================================================
BAYRAKLAR = {
    "tr": "TR",
    "es": "ES",
    "pt": "BR",
    "it": "IT",
    "ja": "JP",
    "ko": "KR",
    "zh": "CN",
}

BAYRAK_RENKLERI = {
    "tr": "#E30A17",
    "es": "#AA151B",
    "pt": "#009B3A",
    "it": "#008C45",
    "ja": "#BC002D",
    "ko": "#003478",
    "zh": "#DE2910",
}

# ============================================================
# TEMA (ACIK / KOYU)
# ============================================================
TEMA_ISIMLERI = {
    "acik": {
        "arka": "#f5f5f5",
        "yazi": "#1a1a1a",
        "buton_bg": "#e1e1e1",
        "baslik": "#4a90d9",
        "giris_bg": "#ffffff",
        "log_bg": "#ffffff",
        "kenarlik": "#c9c9c9",
        "buton_ustune": "#d4d4d4",
        "buton_pasif": "#ececec",
        "secim_bg": "#4a90d9",
        "pasif_yazi": "#8a8a8a",
    },
    "koyu": {
        "arka": "#2b2b2b",
        "yazi": "#e0e0e0",
        "buton_bg": "#404040",
        "baslik": "#6ab0ff",
        "giris_bg": "#1e1e1e",
        "log_bg": "#1e1e1e",
        "kenarlik": "#505050",
        "buton_ustune": "#4d4d4d",
        "buton_pasif": "#333333",
        "secim_bg": "#3a6ea5",
        "pasif_yazi": "#7f7f7f",
    },
}
TEMA_VARSAYILAN = "acik"

AYAR_DOSYASI = Path.home() / ".multi_downloader_ayar.json"


def tema_tercihi_yukle():
    """JSON ayar dosyasindan tema tercihini yukle"""
    try:
        if AYAR_DOSYASI.exists():
            veri = json.loads(AYAR_DOSYASI.read_text(encoding="utf-8"))
            tema = veri.get("tema")
            if tema in TEMA_ISIMLERI:
                return tema
    except Exception:
        pass
    return TEMA_VARSAYILAN


def tema_tercihi_kaydet(tema_adi):
    """Tema tercihini JSON ayar dosyasina kaydet"""
    try:
        AYAR_DOSYASI.write_text(
            json.dumps({"tema": tema_adi}, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
    except Exception:
        pass

# ============================================================
# CEVIRILER (7 DIL)
# ============================================================
CEVIRILER = {
    "tr": {
        "app_title": "Multi Downloader",
        "url_label": "Video linki (YouTube, Instagram, TikTok, Twitter...):",
        "paste": "Yapistir",
        "clear": "Temizle",
        "browser_label": "Tarayici:",
        "save_label": "Kayit:",
        "get_resolutions": "1) Cozunurlukleri Getir",
        "select_resolution": "Cozunurluk sec (2):",
        "best_quality": "En iyi kalite (en yuksek)",
        "audio_only": "Sadece ses (MP3)",
        "download": "3)  I N D I R",
        "cancel": "Iptal",
        "status_ready": "Hazir",
        "status_analyzing": "Analiz ediliyor...",
        "status_downloading": "Indiriliyor...",
        "status_merging": "Birlesiyor...",
        "status_done": "Tamamlandi",
        "status_cancelled": "Iptal ediliyor...",
        "status_error": "Hata",
        "log_title": "Baslik:",
        "log_format": "Format:",
        "log_folder": "Klasor:",
        "log_saved": "Kaydedildi:",
        "log_merging": "Indirme tamam, birlestiriliyor...",
        "log_cancel": "Iptal istegi gonderildi.",
        "log_browser": "Tarayici:",
        "log_link": "Link:",
        "msg_no_url": "Link gerekli",
        "msg_no_url_detail": "Video linkini yapistirin.",
        "msg_no_selection": "Secim yok",
        "msg_no_selection_detail": "Once bir cozunurluk sec.",
        "msg_paste_empty": "Pano bos",
        "msg_paste_empty_detail": "Panoda metin yok.",
        "msg_complete": "Indirme tamamlandi",
        "msg_complete_detail": "Klasoru acilsin mi?",
        "msg_missing_deps": "Eksik bagimlilik",
        "msg_missing_deps_detail": "Eksik olan:\n{deps}\n\nOnce bunlari kurun.",
        "msg_folder_error": "Klasor hatasi",
        "options_found": "secenek bulundu. Birini sec, INDIR'e bas.",
        "no_browser": "Tarayici bulunamadi",
        "no_browser_detail": "Video indirmek icin bir tarayici gerekli.\n\nTarayici kurduktan sonra programi yeniden baslatin.",
        # Hata mesajlari
        "err_unavailable": "Video mevcut degil (silinmis veya gizli)",
        "err_no_video": "Bu linkte video bulunamadi",
        "err_private": "Video gizli",
        "err_signin": "Giris yaparak dogrulayin",
        "err_login": "Giris gerekli",
        "err_403": "Erisim engellendi (403)",
        "err_404": "Video bulunamadi (404)",
        "err_429": "Cok fazla istek (429) - biraz bekle",
        "err_download": "Indirilemedi",
        "err_geo": "Bolgesel engel",
        "err_blocked": "Istek engellendi",
        "err_extract": "Veri cikarilamadi",
        "err_unsupported": "Desteklenmeyen URL",
        "err_invalid_url": "Gecersiz URL",
        # Help menusu
        "menu_help": "Yardim",
        "menu_info": "Hakkinda",
        "menu_shortcuts": "Kisayollar",
        "menu_update": "Guncelleme Kontrolu",
        "menu_github": "GitHub Sayfasi",
        "info_title": "Hakkinda",
        "info_version": "Versiyon",
        "info_author": "Gelistirici",
        "info_license": "Lisans",
        "info_desc": "Coklu platform video indirme araci",
        "shortcuts_title": "Klavye Kisayollari",
        "shortcuts_paste": "Ctrl+V / Sag Tik",
        "shortcuts_paste_desc": "Panodan yapistir",
        "shortcuts_enter": "Enter",
        "shortcuts_enter_desc": "Cozunurlukleri getir",
        "shortcuts_double": "Cift Tik",
        "shortcuts_double_desc": "Indirmeyi baslat",
        "shortcuts_esc": "Escape",
        "shortcuts_esc_desc": "Iptal et",
        "update_title": "Guncelleme Kontrolu",
        "update_current": "Mevcut versiyon:",
        "update_latest": "Son versiyon:",
        "update_checking": "Kontrol ediliyor...",
        "update_ok": "Guncel",
        "update_new": "Yeni versiyon mevcut!",
        "update_error": "Guncelleme kontrolu yapilamadi",
        "lang_label": "Dil:",
        "menu_gorunum": "Gorunum",
        "tema_acik": "Acik Tema",
        "tema_koyu": "Koyu Tema",
    },
    "es": {
        "app_title": "Multi Downloader",
        "url_label": "Enlace de video (YouTube, Instagram, TikTok, Twitter...):",
        "paste": "Pegar",
        "clear": "Limpiar",
        "browser_label": "Navegador:",
        "save_label": "Guardar:",
        "get_resolutions": "1) Obtener Resoluciones",
        "select_resolution": "Seleccionar resolucion (2):",
        "best_quality": "Mejor calidad (mas alta)",
        "audio_only": "Solo audio (MP3)",
        "download": "3)  D E S C A R G A R",
        "cancel": "Cancelar",
        "status_ready": "Listo",
        "status_analyzing": "Analizando...",
        "status_downloading": "Descargando...",
        "status_merging": "Combinando...",
        "status_done": "Completado",
        "status_cancelled": "Cancelando...",
        "status_error": "Error",
        "log_title": "Titulo:",
        "log_format": "Formato:",
        "log_folder": "Carpeta:",
        "log_saved": "Guardado:",
        "log_merging": "Descarga completa, combinando...",
        "log_cancel": "Solicitud de cancelacion enviada.",
        "log_browser": "Navegador:",
        "log_link": "Enlace:",
        "msg_no_url": "Enlace requerido",
        "msg_no_url_detail": "Pega un enlace de video.",
        "msg_no_selection": "Sin seleccion",
        "msg_no_selection_detail": "Primero selecciona una resolucion.",
        "msg_paste_empty": "Portapapeles vacio",
        "msg_paste_empty_detail": "No hay texto en el portapapeles.",
        "msg_complete": "Descarga completada",
        "msg_complete_detail": "¿Abrir carpeta?",
        "msg_missing_deps": "Dependencias faltantes",
        "msg_missing_deps_detail": "Faltan:\n{deps}\n\nInstalalos primero.",
        "msg_folder_error": "Error de carpeta",
        "options_found": "opciones encontradas. Selecciona una y haz clic en DESCARGAR.",
        "no_browser": "Navegador no encontrado",
        "no_browser_detail": "Se necesita un navegador para descargar videos.\n\nReinicia el programa despues de instalar un navegador.",
        "err_unavailable": "Video no disponible (eliminado o privado)",
        "err_no_video": "No se encontro video en este enlace",
        "err_private": "Video privado",
        "err_signin": "Inicia sesion para confirmar",
        "err_login": "Inicio de sesion requerido",
        "err_403": "Acceso denegado (403)",
        "err_404": "Video no encontrado (404)",
        "err_429": "Demasiadas solicitudes (429)",
        "err_download": "No se pudo descargar",
        "err_geo": "Bloqueo geografico",
        "err_blocked": "Solicitud bloqueada",
        "err_extract": "No se pudieron extraer los datos",
        "err_unsupported": "URL no compatible",
        "err_invalid_url": "URL invalida",
        "menu_help": "Ayuda",
        "menu_info": "Acerca de",
        "menu_shortcuts": "Atajos de Teclado",
        "menu_update": "Buscar Actualizaciones",
        "menu_github": "Pagina de GitHub",
        "info_title": "Acerca de",
        "info_version": "Version",
        "info_author": "Desarrollador",
        "info_license": "Licencia",
        "info_desc": "Herramienta para descargar videos de multiples plataformas",
        "shortcuts_title": "Atajos de Teclado",
        "shortcuts_paste": "Ctrl+V / Clic Derecho",
        "shortcuts_paste_desc": "Pegar del portapapeles",
        "shortcuts_enter": "Enter",
        "shortcuts_enter_desc": "Obtener resoluciones",
        "shortcuts_double": "Doble Clic",
        "shortcuts_double_desc": "Iniciar descarga",
        "shortcuts_esc": "Escape",
        "shortcuts_esc_desc": "Cancelar",
        "update_title": "Buscar Actualizaciones",
        "update_current": "Version actual:",
        "update_latest": "Ultima version:",
        "update_checking": "Buscando...",
        "update_ok": "Actualizado",
        "update_new": "Nueva version disponible!",
        "update_error": "No se pudo buscar actualizaciones",
        "lang_label": "Idioma:",
        "menu_gorunum": "Apariencia",
        "tema_acik": "Tema Claro",
        "tema_koyu": "Tema Oscuro",
    },
    "pt": {
        "app_title": "Multi Downloader",
        "url_label": "Link do video (YouTube, Instagram, TikTok, Twitter...):",
        "paste": "Colar",
        "clear": "Limpar",
        "browser_label": "Navegador:",
        "save_label": "Salvar:",
        "get_resolutions": "1) Obter Resolucoes",
        "select_resolution": "Selecionar resolucao (2):",
        "best_quality": "Melhor qualidade (mais alta)",
        "audio_only": "Apenas audio (MP3)",
        "download": "3)  B A I X A R",
        "cancel": "Cancelar",
        "status_ready": "Pronto",
        "status_analyzing": "Analisando...",
        "status_downloading": "Baixando...",
        "status_merging": "Combinando...",
        "status_done": "Concluido",
        "status_cancelled": "Cancelando...",
        "status_error": "Erro",
        "log_title": "Titulo:",
        "log_format": "Formato:",
        "log_folder": "Pasta:",
        "log_saved": "Salvo:",
        "log_merging": "Download completo, combinando...",
        "log_cancel": "Solicitacao de cancelamento enviada.",
        "log_browser": "Navegador:",
        "log_link": "Link:",
        "msg_no_url": "Link necessario",
        "msg_no_url_detail": "Cole um link de video.",
        "msg_no_selection": "Sem selecao",
        "msg_no_selection_detail": "Primeiro selecione uma resolucao.",
        "msg_paste_empty": "Area de transferencia vazia",
        "msg_paste_empty_detail": "Nao ha texto na area de transferencia.",
        "msg_complete": "Download concluido",
        "msg_complete_detail": "Abrir pasta?",
        "msg_missing_deps": "Dependencias faltando",
        "msg_missing_deps_detail": "Faltam:\n{deps}\n\nInstale primeiro.",
        "msg_folder_error": "Erro de pasta",
        "options_found": "opcoes encontradas. Selecione uma e clique em BAIXAR.",
        "no_browser": "Navegador nao encontrado",
        "no_browser_detail": "Um navegador e necessario para baixar videos.\n\nReinicie o programa apos instalar um navegador.",
        "err_unavailable": "Video indisponivel (removido ou privado)",
        "err_no_video": "Nenhum video encontrado neste tweet",
        "err_private": "Video privado",
        "err_signin": "Faca login para confirmar",
        "err_login": "Login necessario",
        "err_403": "Acesso negado (403)",
        "err_404": "Video nao encontrado (404)",
        "err_429": "Muitas requisicoes (429)",
        "err_download": "Nao foi possivel baixar",
        "err_geo": "Bloqueio geografico",
        "err_blocked": "Requisicao bloqueada",
        "err_extract": "Nao foi possivel extrair dados",
        "err_unsupported": "URL nao suportada",
        "err_invalid_url": "URL invalida",
        "menu_help": "Ajuda",
        "menu_info": "Sobre",
        "menu_shortcuts": "Atalhos de Teclado",
        "menu_update": "Verificar Atualizacoes",
        "menu_github": "Pagina do GitHub",
        "info_title": "Sobre",
        "info_version": "Versao",
        "info_author": "Desenvolvedor",
        "info_license": "Licenca",
        "info_desc": "Ferramenta para baixar videos de multiplas plataformas",
        "shortcuts_title": "Atalhos de Teclado",
        "shortcuts_paste": "Ctrl+V / Clique Direito",
        "shortcuts_paste_desc": "Colar da area de transferencia",
        "shortcuts_enter": "Enter",
        "shortcuts_enter_desc": "Obter resolucoes",
        "shortcuts_double": "Duplo Clique",
        "shortcuts_double_desc": "Iniciar download",
        "shortcuts_esc": "Escape",
        "shortcuts_esc_desc": "Cancelar",
        "update_title": "Verificar Atualizacoes",
        "update_current": "Versao atual:",
        "update_latest": "Ultima versao:",
        "update_checking": "Verificando...",
        "update_ok": "Atualizado",
        "update_new": "Nova versao disponivel!",
        "update_error": "Nao foi possivel verificar atualizacoes",
        "lang_label": "Idioma:",
        "menu_gorunum": "Aparencia",
        "tema_acik": "Tema Claro",
        "tema_koyu": "Tema Escuro",
    },
    "it": {
        "app_title": "Multi Downloader",
        "url_label": "Link del video (YouTube, Instagram, TikTok, Twitter...):",
        "paste": "Incolla",
        "clear": "Pulisci",
        "browser_label": "Browser:",
        "save_label": "Salva:",
        "get_resolutions": "1) Ottieni Risoluzioni",
        "select_resolution": "Seleziona risoluzione (2):",
        "best_quality": "Migliore qualita (piu alta)",
        "audio_only": "Solo audio (MP3)",
        "download": "3)  S C A R I C A",
        "cancel": "Annulla",
        "status_ready": "Pronto",
        "status_analyzing": "Analisi in corso...",
        "status_downloading": "Download in corso...",
        "status_merging": "Unione in corso...",
        "status_done": "Completato",
        "status_cancelled": "Annullamento...",
        "status_error": "Errore",
        "log_title": "Titolo:",
        "log_format": "Formato:",
        "log_folder": "Cartella:",
        "log_saved": "Salvato:",
        "log_merging": "Download completato, unione in corso...",
        "log_cancel": "Richiesta di annullamento inviata.",
        "log_browser": "Browser:",
        "log_link": "Link:",
        "msg_no_url": "Link richiesto",
        "msg_no_url_detail": "Incolla un link del video.",
        "msg_no_selection": "Nessuna selezione",
        "msg_no_selection_detail": "Prima seleziona una risoluzione.",
        "msg_pane_empty": "Appunti vuoti",
        "msg_pane_empty_detail": "Nessun testo negli appunti.",
        "msg_complete": "Download completato",
        "msg_complete_detail": "Aprire la cartella?",
        "msg_missing_deps": "Dipendenze mancanti",
        "msg_missing_deps_detail": "Mancano:\n{deps}\n\nInstallali prima.",
        "msg_folder_error": "Errore cartella",
        "options_found": "opzioni trovate. Selezionane una e clicca SCARICA.",
        "no_browser": "Browser non trovato",
        "no_browser_detail": "Serve un browser per scaricare i video.\n\nRiavvia il programma dopo aver installato un browser.",
        "err_unavailable": "Video non disponibile (rimosso o privato)",
        "err_no_video": "Nessun video trovato in questo tweet",
        "err_private": "Video privato",
        "err_signin": "Accedi per confermare",
        "err_login": "Accesso richiesto",
        "err_403": "Accesso negato (403)",
        "err_404": "Video non trovato (404)",
        "err_429": "Troppe richieste (429)",
        "err_download": "Impossibile scaricare",
        "err_geo": "Blocco geografico",
        "err_blocked": "Richiesta bloccata",
        "err_extract": "Impossibile estrarre i dati",
        "err_unsupported": "URL non supportato",
        "err_invalid_url": "URL non valido",
        "menu_help": "Aiuto",
        "menu_info": "Informazioni",
        "menu_shortcuts": "Scorciatoie",
        "menu_update": "Controlla Aggiornamenti",
        "menu_github": "Pagina GitHub",
        "info_title": "Informazioni",
        "info_version": "Versione",
        "info_author": "Sviluppatore",
        "info_license": "Licenza",
        "info_desc": "Strumento per scaricare video da piattaforme multiple",
        "shortcuts_title": "Scorciatoie da Tastiera",
        "shortcuts_paste": "Ctrl+V / Tasto Destro",
        "shortcuts_paste_desc": "Incolla dagli appunti",
        "shortcuts_enter": "Invio",
        "shortcuts_enter_desc": "Ottieni risoluzioni",
        "shortcuts_double": "Doppio Clic",
        "shortcuts_double_desc": "Avvia download",
        "shortcuts_esc": "Escape",
        "shortcuts_esc_desc": "Annulla",
        "update_title": "Controlla Aggiornamenti",
        "update_current": "Versione attuale:",
        "update_latest": "Ultima versione:",
        "update_checking": "Controllo in corso...",
        "update_ok": "Aggiornato",
        "update_new": "Nuova versione disponibile!",
        "update_error": "Impossibile controllare gli aggiornamenti",
        "lang_label": "Lingua:",
        "menu_gorunum": "Aspetto",
        "tema_acik": "Tema Chiaro",
        "tema_koyu": "Tema Scuro",
    },
    "ja": {
        "app_title": "Multi Downloader",
        "url_label": "ビデオリンク (YouTube, Instagram, TikTok, Twitter...):",
        "paste": "貼り付け",
        "clear": "クリア",
        "browser_label": "ブラウザ:",
        "save_label": "保存先:",
        "get_resolutions": "1) 解像度を取得",
        "select_resolution": "解像度を選択 (2):",
        "best_quality": "最高品質",
        "audio_only": "音声のみ (MP3)",
        "download": "3)  ダ ー ン ロ ー ド",
        "cancel": "キャンセル",
        "status_ready": "準備完了",
        "status_analyzing": "分析中...",
        "status_downloading": "ダウンロード中...",
        "status_merging": "結合中...",
        "status_done": "完了",
        "status_cancelled": "キャンセル中...",
        "status_error": "エラー",
        "log_title": "タイトル:",
        "log_format": "フォーマット:",
        "log_folder": "フォルダ:",
        "log_saved": "保存先:",
        "log_merging": "ダウンロード完了、結合中...",
        "log_cancel": "キャンセルリクエストを送信しました。",
        "log_browser": "ブラウザ:",
        "log_link": "リンク:",
        "msg_no_url": "リンクが必要です",
        "msg_no_url_detail": "ビデオリンクを貼り付けてください。",
        "msg_no_selection": "未選択",
        "msg_no_selection_detail": "まず解像度を選択してください。",
        "msg_paste_empty": "クリップボードが空です",
        "msg_paste_empty_detail": "クリップボードにテキストがありません。",
        "msg_complete": "ダウンロード完了",
        "msg_complete_detail": "フォルダを開きますか？",
        "msg_missing_deps": "依存関係が不足しています",
        "msg_missing_deps_detail": "不足:\n{deps}\n\n先にインストールしてください。",
        "msg_folder_error": "フォルダエラー",
        "options_found": "件見つかりました。選択してダウンロードをクリック。",
        "no_browser": "ブラウザが見つかりません",
        "no_browser_detail": "ビデオをダウンロードするにはブラウザが必要です。\n\nブラウザインストール後にプログラムを再起動してください。",
        "err_unavailable": "ビデオは利用できません（削除または非公開）",
        "err_no_video": "このツイートにビデオが見つかりません",
        "err_private": "非公開ビデオ",
        "err_signin": "確認のためにログインしてください",
        "err_login": "ログインが必要です",
        "err_403": "アクセス拒否 (403)",
        "err_404": "ビデオが見つかりません (404)",
        "err_429": "リクエスト过多 (429)",
        "err_download": "ダウンロードできませんでした",
        "err_geo": "地理的ブロック",
        "err_blocked": "リクエストがブロックされました",
        "err_extract": "データを抽出できませんでした",
        "err_unsupported": "サポートされていないURL",
        "err_invalid_url": "無効なURL",
        "menu_help": "ヘルプ",
        "menu_info": "情報",
        "menu_shortcuts": "キーボードショートカット",
        "menu_update": "アップデート確認",
        "menu_github": "GitHubページ",
        "info_title": "情報",
        "info_version": "バージョン",
        "info_author": "開発者",
        "info_license": "ライセンス",
        "info_desc": "Twitter/Xからビデオをダウンロードするツール",
        "shortcuts_title": "キーボードショートカット",
        "shortcuts_paste": "Ctrl+V / 右クリック",
        "shortcuts_paste_desc": "クリップボードから貼り付け",
        "shortcuts_enter": "Enter",
        "shortcuts_enter_desc": "解像度を取得",
        "shortcuts_double": "ダブルクリック",
        "shortcuts_double_desc": "ダウンロード開始",
        "shortcuts_esc": "Escape",
        "shortcuts_esc_desc": "キャンセル",
        "update_title": "アップデート確認",
        "update_current": "現在のバージョン:",
        "update_latest": "最新バージョン:",
        "update_checking": "確認中...",
        "update_ok": "最新です",
        "update_new": "新しいバージョンがあります！",
        "update_error": "アップデートを確認できませんでした",
        "lang_label": "言語:",
        "menu_gorunum": "表示",
        "tema_acik": "ライトテーマ",
        "tema_koyu": "ダークテーマ",
    },
    "ko": {
        "app_title": "Multi Downloader",
        "url_label": "비디오 링크 (YouTube, Instagram, TikTok, Twitter...):",
        "paste": "붙여넣기",
        "clear": "지우기",
        "browser_label": "브라우저:",
        "save_label": "저장:",
        "get_resolutions": "1) 해상도 가져오기",
        "select_resolution": "해상도 선택 (2):",
        "best_quality": "최고 품질",
        "audio_only": "오디오만 (MP3)",
        "download": "3)  다  우  로  드",
        "cancel": "취소",
        "status_ready": "준비",
        "status_analyzing": "분석 중...",
        "status_downloading": "다운로드 중...",
        "status_merging": "병합 중...",
        "status_done": "완료",
        "status_cancelled": "취소 중...",
        "status_error": "오류",
        "log_title": "제목:",
        "log_format": "형식:",
        "log_folder": "폴더:",
        "log_saved": "저장됨:",
        "log_merging": "다운로드 완료, 병합 중...",
        "log_cancel": "취소 요청이 전송되었습니다.",
        "log_browser": "브라우저:",
        "log_link": "링크:",
        "msg_no_url": "링크 필요",
        "msg_no_url_detail": "비디오 링크를 붙여넣으세요.",
        "msg_no_selection": "선택 없음",
        "msg_no_selection_detail": "먼저 해상도를 선택하세요.",
        "msg_paste_empty": "클립보드가 비어있습니다",
        "msg_paste_empty_detail": "클립보드에 텍스트가 없습니다.",
        "msg_complete": "다운로드 완료",
        "msg_complete_detail": "폴더를 열까요?",
        "msg_missing_deps": "필수 항목 누락",
        "msg_missing_deps_detail": "누락:\n{deps}\n\n먼저 설치하세요.",
        "msg_folder_error": "폴더 오류",
        "options_found": "개를 찾았습니다. 선택 후 다운로드를 클릭하세요.",
        "no_browser": "브라우저를 찾을 수 없습니다",
        "no_browser_detail": "비디오 다운로드에 브라우저가 필요합니다.\n\n브라우저 설치 후 프로그램을 재시작하세요.",
        "err_unavailable": "비디오를 사용할 수 없습니다 (삭제 또는 비공개)",
        "err_no_video": "이 트윗에서 비디오를 찾을 수 없습니다",
        "err_private": "비공개 비디오",
        "err_signin": "확인을 위해 로그인하세요",
        "err_login": "로그인 필요",
        "err_403": "접속 거부 (403)",
        "err_404": "비디오를 찾을 수 없습니다 (404)",
        "err_429": "요청 과다 (429)",
        "err_download": "다운로드할 수 없습니다",
        "err_geo": "지역 차단",
        "err_blocked": "요청이 차단되었습니다",
        "err_extract": "데이터를 추출할 수 없습니다",
        "err_unsupported": "지원되지 않는 URL",
        "err_invalid_url": "잘못된 URL",
        "menu_help": "도움말",
        "menu_info": "정보",
        "menu_shortcuts": "키보드 단축키",
        "menu_update": "업데이트 확인",
        "menu_github": "GitHub 페이지",
        "info_title": "정보",
        "info_version": "버전",
        "info_author": "개발자",
        "info_license": "라이선스",
        "info_desc": "Twitter/X에서 비디오를 다운로드하는 도구",
        "shortcuts_title": "키보드 단축키",
        "shortcuts_paste": "Ctrl+V / 오른쪽 클릭",
        "shortcuts_paste_desc": "클립보드에서 붙여넣기",
        "shortcuts_enter": "Enter",
        "shortcuts_enter_desc": "해상도 가져오기",
        "shortcuts_double": "더블 클릭",
        "shortcuts_double_desc": "다운로드 시작",
        "shortcuts_esc": "Escape",
        "shortcuts_esc_desc": "취소",
        "update_title": "업데이트 확인",
        "update_current": "현재 버전:",
        "update_latest": "최신 버전:",
        "update_checking": "확인 중...",
        "update_ok": "최신입니다",
        "update_new": "새 버전이 있습니다!",
        "update_error": "업데이트를 확인할 수 없습니다",
        "lang_label": "언어:",
        "menu_gorunum": "보기",
        "tema_acik": "라이트 테마",
        "tema_koyu": "다크 테마",
    },
    "zh": {
        "app_title": "Multi Downloader",
        "url_label": "视频链接 (YouTube, Instagram, TikTok, Twitter...):",
        "paste": "粘贴",
        "clear": "清除",
        "browser_label": "浏览器:",
        "save_label": "保存:",
        "get_resolutions": "1) 获取分辨率",
        "select_resolution": "选择分辨率 (2):",
        "best_quality": "最高质量",
        "audio_only": "仅音频 (MP3)",
        "download": "3)  下  载",
        "cancel": "取消",
        "status_ready": "就绪",
        "status_analyzing": "分析中...",
        "status_downloading": "下载中...",
        "status_merging": "合并中...",
        "status_done": "完成",
        "status_cancelled": "取消中...",
        "status_error": "错误",
        "log_title": "标题:",
        "log_format": "格式:",
        "log_folder": "文件夹:",
        "log_saved": "已保存:",
        "log_merging": "下载完成，合并中...",
        "log_cancel": "取消请求已发送。",
        "log_browser": "浏览器:",
        "log_link": "链接:",
        "msg_no_url": "需要链接",
        "msg_no_url_detail": "请粘贴视频链接。",
        "msg_no_selection": "未选择",
        "msg_no_selection_detail": "请先选择分辨率。",
        "msg_paste_empty": "剪贴板为空",
        "msg_paste_empty_detail": "剪贴板中没有文本。",
        "msg_complete": "下载完成",
        "msg_complete_detail": "打开文件夹？",
        "msg_missing_deps": "缺少依赖",
        "msg_missing_deps_detail": "缺少:\n{deps}\n\n请先安装。",
        "msg_folder_error": "文件夹错误",
        "options_found": "个选项。选择后点击下载。",
        "no_browser": "未找到浏览器",
        "no_browser_detail": "下载视频需要浏览器。\n\n安装浏览器后请重启程序。",
        "err_unavailable": "视频不可用（已删除或私密）",
        "err_no_video": "此推文中未找到视频",
        "err_private": "私密视频",
        "err_signin": "请登录确认",
        "err_login": "需要登录",
        "err_403": "访问被拒绝 (403)",
        "err_404": "视频未找到 (404)",
        "err_429": "请求过多 (429)",
        "err_download": "无法下载",
        "err_geo": "地区限制",
        "err_blocked": "请求被阻止",
        "err_extract": "无法提取数据",
        "err_unsupported": "不支持的URL",
        "err_invalid_url": "无效URL",
        "menu_help": "帮助",
        "menu_info": "关于",
        "menu_shortcuts": "键盘快捷键",
        "menu_update": "检查更新",
        "menu_github": "GitHub 页面",
        "info_title": "关于",
        "info_version": "版本",
        "info_author": "开发者",
        "info_license": "许可证",
        "info_desc": "Twitter/X 视频下载工具",
        "shortcuts_title": "键盘快捷键",
        "shortcuts_paste": "Ctrl+V / 右键",
        "shortcuts_paste_desc": "从剪贴板粘贴",
        "shortcuts_enter": "Enter",
        "shortcuts_enter_desc": "获取分辨率",
        "shortcuts_double": "双击",
        "shortcuts_double_desc": "开始下载",
        "shortcuts_esc": "Escape",
        "shortcuts_esc_desc": "取消",
        "update_title": "检查更新",
        "update_current": "当前版本:",
        "update_latest": "最新版本:",
        "update_checking": "检查中...",
        "update_ok": "已是最新",
        "update_new": "有新版本！",
        "update_error": "无法检查更新",
        "lang_label": "语言:",
        "menu_gorunum": "外观",
        "tema_acik": "浅色主题",
        "tema_koyu": "深色主题",
    },
}

# ============================================================
# HATA CEVIRILERI
# ============================================================
HATA_CEVRIR = {
    "tr": {
        "Video unavailable": "Video mevcut degil (silinmis veya gizli)",
        "No video could be found in this tweet": "Bu tweet'te video bulunamadi",
        "Video #1 is unavailable": "Video #1 mevcut degil",
        "This content isn't available": "Bu icerik mevcut degil",
        "Private video": "Video gizli",
        "This video is private": "Bu video gizli",
        "Sign in to confirm": "Giris yaparak dogrulayin",
        "Login required": "Giris gerekli",
        "HTTP Error 403": "Erisim engellendi (403)",
        "HTTP Error 404": "Video bulunamadi (404)",
        "HTTP Error 429": "Cok fazla istek (429)",
        "Unable to download": "Indirilemedi",
        "GeoBlocked": "Bolgesel engel",
        "Request blocked": "Istek engellendi",
        "Could not extract": "Veri cikarilamadi",
        "Unsupported URL": "Desteklenmeyen URL",
        "Not a valid URL": "Gecersiz URL",
    },
    "es": {
        "Video unavailable": "Video no disponible",
        "No video could be found in this tweet": "No se encontro video en este tweet",
        "Video #1 is unavailable": "Video #1 no disponible",
        "Private video": "Video privado",
        "Sign in to confirm": "Inicia sesion para confirmar",
        "Login required": "Inicio de sesion requerido",
        "HTTP Error 403": "Acceso denegado (403)",
        "HTTP Error 404": "Video no encontrado (404)",
        "HTTP Error 429": "Demasiadas solicitudes (429)",
        "Unable to download": "No se pudo descargar",
        "GeoBlocked": "Bloqueo geografico",
        "Request blocked": "Solicitud bloqueada",
        "Could not extract": "No se pudieron extraer datos",
        "Unsupported URL": "URL no compatible",
        "Not a valid URL": "URL invalida",
    },
    "pt": {
        "Video unavailable": "Video indisponivel",
        "No video could be found in this tweet": "Nenhum video encontrado neste tweet",
        "Video #1 is unavailable": "Video #1 indisponivel",
        "Private video": "Video privado",
        "Sign in to confirm": "Faca login para confirmar",
        "Login required": "Login necessario",
        "HTTP Error 403": "Acesso negado (403)",
        "HTTP Error 404": "Video nao encontrado (404)",
        "HTTP Error 429": "Muitas requisicoes (429)",
        "Unable to download": "Nao foi possivel baixar",
        "GeoBlocked": "Bloqueio geografico",
        "Request blocked": "Requisicao bloqueada",
        "Could not extract": "Nao foi possivel extrair dados",
        "Unsupported URL": "URL nao suportada",
        "Not a valid URL": "URL invalida",
    },
    "it": {
        "Video unavailable": "Video non disponibile",
        "No video could be found in this tweet": "Nessun video trovato in questo tweet",
        "Video #1 is unavailable": "Video #1 non disponibile",
        "Private video": "Video privato",
        "Sign in to confirm": "Accedi per confermare",
        "Login required": "Accesso richiesto",
        "HTTP Error 403": "Accesso negato (403)",
        "HTTP Error 404": "Video non trovato (404)",
        "HTTP Error 429": "Troppe richieste (429)",
        "Unable to download": "Impossibile scaricare",
        "GeoBlocked": "Blocco geografico",
        "Request blocked": "Richiesta bloccata",
        "Could not extract": "Impossibile estrarre i dati",
        "Unsupported URL": "URL non supportato",
        "Not a valid URL": "URL non valido",
    },
    "ja": {
        "Video unavailable": "ビデオは利用できません",
        "No video could be found in this tweet": "このツイートにビデオが見つかりません",
        "Video #1 is unavailable": "ビデオ #1 は利用できません",
        "Private video": "非公開ビデオ",
        "Sign in to confirm": "確認のためにログインしてください",
        "Login required": "ログインが必要です",
        "HTTP Error 403": "アクセス拒否 (403)",
        "HTTP Error 404": "ビデオが見つかりません (404)",
        "HTTP Error 429": "リクエスト过多 (429)",
        "Unable to download": "ダウンロードできませんでした",
        "GeoBlocked": "地理的ブロック",
        "Request blocked": "リクエストがブロックされました",
        "Could not extract": "データを抽出できませんでした",
        "Unsupported URL": "サポートされていないURL",
        "Not a valid URL": "無効なURL",
    },
    "ko": {
        "Video unavailable": "비디오를 사용할 수 없습니다",
        "No video could be found in this tweet": "이 트윗에서 비디오를 찾을 수 없습니다",
        "Video #1 is unavailable": "비디오 #1을 사용할 수 없습니다",
        "Private video": "비공개 비디오",
        "Sign in to confirm": "확인을 위해 로그인하세요",
        "Login required": "로그인 필요",
        "HTTP Error 403": "접속 거부 (403)",
        "HTTP Error 404": "비디오를 찾을 수 없습니다 (404)",
        "HTTP Error 429": "요청 과다 (429)",
        "Unable to download": "다운로드할 수 없습니다",
        "GeoBlocked": "지역 차단",
        "Request blocked": "요청이 차단되었습니다",
        "Could not extract": "데이터를 추출할 수 없습니다",
        "Unsupported URL": "지원되지 않는 URL",
        "Not a valid URL": "잘못된 URL",
    },
    "zh": {
        "Video unavailable": "视频不可用",
        "No video could be found in this tweet": "此推文中未找到视频",
        "Video #1 is unavailable": "视频 #1 不可用",
        "Private video": "私密视频",
        "Sign in to confirm": "请登录确认",
        "Login required": "需要登录",
        "HTTP Error 403": "访问被拒绝 (403)",
        "HTTP Error 404": "视频未找到 (404)",
        "HTTP Error 429": "请求过多 (429)",
        "Unable to download": "无法下载",
        "GeoBlocked": "地区限制",
        "Request blocked": "请求被阻止",
        "Could not extract": "无法提取数据",
        "Unsupported URL": "不支持的URL",
        "Not a valid URL": "无效URL",
    },
}

TARAYICI_ISIMLERI = {
    "firefox": {"tr": "Firefox", "es": "Firefox", "pt": "Firefox", "it": "Firefox", "ja": "Firefox", "ko": "파이어폭스", "zh": "Firefox"},
    "chrome": {"tr": "Google Chrome", "es": "Google Chrome", "pt": "Google Chrome", "it": "Google Chrome", "ja": "Google Chrome", "ko": "구글 크롬", "zh": "Google Chrome"},
    "brave": {"tr": "Brave Browser", "es": "Brave Browser", "pt": "Brave Browser", "it": "Brave Browser", "ja": "Brave", "ko": "브레이브", "zh": "Brave"},
    "chromium": {"tr": "Chromium", "es": "Chromium", "pt": "Chromium", "it": "Chromium", "ja": "Chromium", "ko": "크로미움", "zh": "Chromium"},
    "edge": {"tr": "Microsoft Edge", "es": "Microsoft Edge", "pt": "Microsoft Edge", "it": "Microsoft Edge", "ja": "Microsoft Edge", "ko": "마이크로소프트 엣지", "zh": "Microsoft Edge"},
    "opera": {"tr": "Opera", "es": "Opera", "pt": "Opera", "it": "Opera", "ja": "Opera", "ko": "오페라", "zh": "Opera"},
    "vivaldi": {"tr": "Vivaldi", "es": "Vivaldi", "pt": "Vivaldi", "it": "Vivaldi", "ja": "Vivaldi", "ko": "리발디", "zh": "Vivaldi"},
}

def cevir_hata(hata_metni, dil="tr"):
    hata_ceviriler = HATA_CEVRIR.get(dil, HATA_CEVRIR["tr"])
    for en, tr in hata_ceviriler.items():
        if en.lower() in hata_metni.lower():
            return tr
    return hata_metni

def os_dil_algila():
    """Isletim sistemi dilini algila"""
    try:
        sistem_dili = locale.getdefaultlocale()[0]
        if sistem_dili:
            kod = sistem_dili.split("_")[0].lower()
            if kod in CEVIRILER:
                return kod
    except Exception:
        pass
    return "tr"

def tarayici_bul():
    bulunanlar = []
    
    if sys.platform == "win32":
        # Windows tarayici yollari
        windows_tarayicilar = {
            "chrome": [
                os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
                r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            ],
            "edge": [
                os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\Edge\Application\msedge.exe"),
                r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
                r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
            ],
            "firefox": [
                os.path.expandvars(r"%LOCALAPPDATA%\Mozilla Firefox\firefox.exe"),
                r"C:\Program Files\Mozilla Firefox\firefox.exe",
                r"C:\Program Files (x86)\Mozilla Firefox\firefox.exe",
            ],
            "brave": [
                os.path.expandvars(r"%LOCALAPPDATA%\BraveSoftware\Brave-Browser\Application\brave.exe"),
                r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",
            ],
            "opera": [
                os.path.expandvars(r"%LOCALAPPDATA%\Opera Software\Opera Stable\opera.exe"),
                r"C:\Program Files\Opera\opera.exe",
            ],
            "vivaldi": [
                os.path.expandvars(r"%LOCALAPPDATA%\Vivaldi\Application\vivaldi.exe"),
                r"C:\Program Files\Vivaldi\Application\vivaldi.exe",
            ],
        }
        for tarayici_adi, yollar in windows_tarayicilar.items():
            for yol in yollar:
                if os.path.isfile(yol):
                    bulunanlar.append(tarayici_adi)
                    break
    else:
        # Linux tarayici komutlari
        linux_tarayicilar = {
            "firefox": ["firefox", "firefox-esr"],
            "chrome": ["google-chrome", "google-chrome-stable"],
            "brave": ["brave-browser", "brave"],
            "chromium": ["chromium", "chromium-browser"],
            "edge": ["microsoft-edge", "microsoft-edge-stable"],
            "opera": ["opera", "opera-stable"],
            "vivaldi": ["vivaldi", "vivaldi-stable"],
        }
        for tarayici_adi, komutlar in linux_tarayicilar.items():
            for komut in komutlar:
                if shutil.which(komut):
                    bulunanlar.append(tarayici_adi)
                    break
    
    return bulunanlar

def _varsayilan_indirme_klasoru():
    if sys.platform == "win32":
        # Windows: Kullanici/Downloads
        return str(Path.home() / "Downloads")
    try:
        sonuc = subprocess.run(["xdg-user-dir", "DOWNLOAD"], capture_output=True,
                               text=True, timeout=5)
        yol = sonuc.stdout.strip()
        if yol and os.path.isdir(yol):
            return yol
    except Exception:
        pass
    return str(Path.home() / "Downloads")

INDIRME_KONUMU = _varsayilan_indirme_klasoru()


class TwitterIndirici(tk.Tk):
    def __init__(self, baslangic_dili=None):
        super().__init__()
        
        # Pencere ikonu
        self._icon_ref = None
        icon_dir = Path(__file__).parent
        icon_path = icon_dir / "download-icon-32.png"
        if icon_path.exists():
            self._icon_ref = tk.PhotoImage(file=str(icon_path))
            # Pencere haritaya gectikten sonra iconu ayarla
            self.after(100, lambda: self.iconphoto(True, self._icon_ref))
        
        if baslangic_dili:
            self.dil = baslangic_dili
        else:
            self.dil = os_dil_algila()
        self.celevriler = CEVIRILER[self.dil]
        self.tema = tema_tercihi_yukle()
        
        self.title(f"{self.celevriler['app_title']} v{VERSION}")
        self.geometry("720x750")
        self.minsize(660, 650)

        self.msg_queue = queue.Queue()
        self.isleniyor = False
        self.analiz_ediliyor = False
        self._ytdl = None
        self.cozunurlukler = []
        self.analiz_url = ""

        self.bulunan_tarayicilar = tarayici_bul()

        self._kontrol_yukleme()
        self._arayuz_kur()
        self.after(100, self._kuyruk_oku)

    def _t(self, anahtar):
        """Ceviri getir"""
        return self.celevriler.get(anahtar, anahtar)

    def tema_ayarla(self, tema_adi):
        """Temayi degistir, tercihi JSON'a kaydet ve tum widget'lara uygula"""
        if tema_adi not in TEMA_ISIMLERI:
            return
        self.tema = tema_adi
        if hasattr(self, "tema_var"):
            self.tema_var.set(tema_adi)
        tema_tercihi_kaydet(tema_adi)
        self._tema_uygula()

    def _tema_uygula(self):
        """Aktif temanin renklerini ttk.Style ve tum widget'lara uygula"""
        r = TEMA_ISIMLERI[self.tema]

        self.configure(bg=r["arka"])

        style = ttk.Style(self)
        try:
            if style.theme_use() != "clam":
                style.theme_use("clam")
        except Exception:
            pass
        style.configure(".", background=r["arka"], foreground=r["yazi"],
                        fieldbackground=r["giris_bg"], troughcolor=r["arka"],
                        bordercolor=r["kenarlik"], lightcolor=r["arka"],
                        darkcolor=r["buton_bg"],
                        selectbackground=r["secim_bg"],
                        selectforeground="#ffffff")
        style.configure("TFrame", background=r["arka"])
        style.configure("TLabel", background=r["arka"], foreground=r["yazi"])
        style.configure("TButton", background=r["buton_bg"], foreground=r["yazi"])
        style.map("TButton",
                  background=[("disabled", r["buton_pasif"]),
                              ("pressed", r["baslik"]),
                              ("active", r["buton_ustune"])],
                  foreground=[("disabled", r["pasif_yazi"])])
        style.configure("TEntry", fieldbackground=r["giris_bg"],
                        foreground=r["yazi"], insertcolor=r["yazi"])
        style.map("TEntry",
                  fieldbackground=[("readonly", r["giris_bg"])],
                  foreground=[("disabled", r["pasif_yazi"])])
        style.configure("TScrollbar", background=r["buton_bg"],
                        troughcolor=r["arka"], arrowcolor=r["yazi"])
        style.map("TScrollbar",
                  background=[("active", r["buton_ustune"])])
        style.configure("Horizontal.TProgressbar", background=r["baslik"],
                        troughcolor=r["arka"], lightcolor=r["baslik"],
                        darkcolor=r["baslik"], bordercolor=r["arka"])

        # tk tabanli widgetlar (Listbox + log)
        self.liste.config(bg=r["giris_bg"], fg=r["yazi"],
                          selectbackground=r["secim_bg"],
                          selectforeground="#ffffff",
                          highlightbackground=r["kenarlik"],
                          highlightcolor=r["baslik"],
                          disabledforeground=r["pasif_yazi"])
        self.log.config(bg=r["log_bg"], fg=r["yazi"],
                        insertbackground=r["yazi"],
                        highlightbackground=r["kenarlik"],
                        highlightcolor=r["baslik"])
        try:
            self.log.vbar.config(background=r["buton_bg"],
                                 troughcolor=r["arka"],
                                 activebackground=r["buton_ustune"])
        except Exception:
            pass

        # Menu cubugu ve alt menuler
        for menu in (self.menu_cubugu, self.yardim_menu,
                     self.dil_menu, self.gorunum_menu):
            try:
                menu.config(bg=r["arka"], fg=r["yazi"],
                            activebackground=r["baslik"],
                            activeforeground="#ffffff")
            except Exception:
                pass

    def _arayuz_kur(self):
        # Menu cubugu
        self.menu_cubugu = tk.Menu(self)
        self.config(menu=self.menu_cubugu)
        
        # Yardim menusu
        self.yardim_menu = tk.Menu(self.menu_cubugu, tearoff=0)
        self.menu_cubugu.add_cascade(label=self._t("menu_help"), menu=self.yardim_menu)
        self.yardim_menu.add_command(label=self._t("menu_info"), command=self._info_goster)
        self.yardim_menu.add_command(label=self._t("menu_shortcuts"), command=self._kisayollar_goster)
        
        # Dil alt menusu
        self.dil_menu = tk.Menu(self.yardim_menu, tearoff=0)
        self.yardim_menu.add_cascade(label=self._t("lang_label"), menu=self.dil_menu)
        
        DIL_ISIMLERI = {
            "tr": "Turkce",
            "es": "Espanol",
            "pt": "Portugues",
            "it": "Italiano",
            "ja": "Nihongo",
            "ko": "Korean",
            "zh": "Chinese",
        }
        
        for kod, bayrak in BAYRAKLAR.items():
            dil_adi = DIL_ISIMLERI.get(kod, kod)
            self.dil_menu.add_command(
                label=f"  [{bayrak}]  {dil_adi}",
                command=lambda k=kod: self._dil_ayarla(k)
            )
        
        self.yardim_menu.add_separator()
        self.yardim_menu.add_command(label=self._t("menu_update"), command=self._guncelleme_kontrol)
        self.yardim_menu.add_command(label=self._t("menu_github"), command=self._github_ac)

        # Gorunum menusu (tema secimi)
        self.tema_var = tk.StringVar(value=self.tema)
        self.gorunum_menu = tk.Menu(self.menu_cubugu, tearoff=0)
        self.menu_cubugu.add_cascade(label=self._t("menu_gorunum"), menu=self.gorunum_menu)
        self.gorunum_menu.add_radiobutton(
            label=self._t("tema_acik"),
            variable=self.tema_var, value="acik",
            command=lambda: self.tema_ayarla("acik"),
        )
        self.gorunum_menu.add_radiobutton(
            label=self._t("tema_koyu"),
            variable=self.tema_var, value="koyu",
            command=lambda: self.tema_ayarla("koyu"),
        )

        pad = {"padx": 12, "pady": 4}

        ust = ttk.Frame(self)
        ust.pack(fill="x", **pad)

        # URL
        ttk.Label(ust, text=self._t("url_label")).pack(anchor="w")
        self.url_var = tk.StringVar()
        url_satir = ttk.Frame(ust)
        url_satir.pack(fill="x", pady=(2, 6))
        self.url_entry = ttk.Entry(url_satir, textvariable=self.url_var, font=("Sans", 11))
        self.url_entry.pack(side="left", fill="x", expand=True)
        self.url_entry.bind("<Return>", lambda e: self._getir_baslat())
        self.url_entry.bind("<Button-3>", self._sag_tik_yapistir)
        ttk.Button(url_satir, text=self._t("paste"), width=7,
                   command=self._pano_yapistir).pack(side="left", padx=(6, 0))
        ttk.Button(url_satir, text=self._t("clear"), width=6,
                   command=self._pano_temizle).pack(side="left", padx=(4, 0))

        # Kayit yolu
        alt_satir = ttk.Frame(ust)
        alt_satir.pack(fill="x", pady=(2, 4))
        
        ttk.Label(alt_satir, text=self._t("save_label")).pack(side="left")
        self.klasor_var = tk.StringVar(value=INDIRME_KONUMU)
        self.klasor_entry = ttk.Entry(alt_satir, textvariable=self.klasor_var, width=30)
        self.klasor_entry.pack(side="left", fill="x", expand=True, padx=6)
        ttk.Button(alt_satir, text="...", width=3,
                   command=self._klasor_sec).pack(side="left")

        self.getir_btn = ttk.Button(ust, text=self._t("get_resolutions"),
                                    command=self._getir_baslat)
        self.getir_btn.pack(fill="x", pady=(8, 2))

        ttk.Label(self, text=self._t("select_resolution"), font=("Sans", 10)).pack(anchor="w", padx=14)
        liste_cerceve = ttk.Frame(self)
        liste_cerceve.pack(fill="both", expand=True, padx=12, pady=(2, 4))
        self.liste = tk.Listbox(liste_cerceve, font=("Sans", 10), height=7,
                                activestyle="dotbox")
        kaydir = ttk.Scrollbar(liste_cerceve, orient="vertical",
                               command=self.liste.yview)
        self.liste.config(yscrollcommand=kaydir.set)
        self.liste.pack(side="left", fill="both", expand=True)
        kaydir.pack(side="right", fill="y")
        self.liste.bind("<Double-Button-1>", lambda e: self._indir_baslat())

        buton = ttk.Frame(self)
        buton.pack(fill="x", padx=12, pady=(6, 2))
        self.iptal_btn = ttk.Button(buton, text=self._t("cancel"), state="disabled",
                                    command=self._iptal)
        self.iptal_btn.pack(side="right")
        self.indir_btn = ttk.Button(buton, text=self._t("download"),
                                    state="disabled",
                                    command=self._indir_baslat)
        self.indir_btn.pack(side="right", padx=8)

        self.durum_var = tk.StringVar(value=self._t("status_ready"))
        ttk.Label(self, textvariable=self.durum_var,
                  font=("Sans", 9)).pack(fill="x", padx=14)
        self.progress = ttk.Progressbar(self, mode="determinate")
        self.progress.pack(fill="x", padx=12, pady=(2, 4))

        self.log = ScrolledText(self, height=7,
                                font=("Consolas", 9), wrap="word")
        self.log.pack(fill="both", expand=True, padx=12, pady=(4, 10))

        # Kayitli temayi uygula
        self._tema_uygula()

    def _dil_ayarla(self, yeni_dil):
        """Dili degistir ve yeniden baslat"""
        if yeni_dil == self.dil:
            return
        # Mevcut ayarlari kaydet
        mevcut_url = self.url_var.get() if hasattr(self, 'url_var') else ""
        mevcut_klasor = self.klasor_var.get() if hasattr(self, 'klasor_var') else INDIRME_KONUMU
        
        self.destroy()
        
        # Yeni pencere ac - dili dogru aktar
        app = TwitterIndirici(baslangic_dili=yeni_dil)
        
        # Ayarlari geri yukle
        if mevcut_url:
            app.url_var.set(mevcut_url)
        app.klasor_var.set(mevcut_klasor)
        
        app.mainloop()

    def _secilen_tarayici(self, url=""):
        """URL'deki platform icin session olan tarayiciyi bul"""
        if not self.bulunan_tarayicilar:
            return None
        
        # Platformu URL'den algila
        platform = self._platform_algila(url)
        
        # Tum tarayicilari dene, hangisinde session varsa onu kullan
        for tarayici in self.bulunan_tarayicilar:
            try:
                cookies_klasoru = self._cookies_klasoru_bul(tarayici)
                if cookies_klasoru and self._session_var_mi(cookies_klasoru, platform):
                    return tarayici
            except Exception:
                continue
        
        # Hiçbirinde session yoksa ilk tarayiciyi dondur
        return self.bulunan_tarayicilar[0]
    
    def _platform_algila(self, url):
        """URL'den platformu algila"""
        url_lower = url.lower()
        if "twitter.com" in url_lower or "x.com" in url_lower:
            return "twitter"
        elif "instagram.com" in url_lower:
            return "instagram"
        elif "youtube.com" in url_lower or "youtu.be" in url_lower:
            return "youtube"
        elif "tiktok.com" in url_lower:
            return "tiktok"
        elif "facebook.com" in url_lower or "fb.com" in url_lower:
            return "facebook"
        elif "reddit.com" in url_lower:
            return "reddit"
        elif "twitch.tv" in url_lower:
            return "twitch"
        return "genel"
    
    def _session_var_mi(self, cookies_klasoru, platform):
        """Tarayicida platform session cookie'si var mi kontrol et"""
        import sqlite3
        import glob
        
        # Platform bazli domain arama
        domain_map = {
            "twitter": ["twitter.com", "x.com"],
            "instagram": ["instagram.com"],
            "youtube": ["youtube.com", "google.com"],
            "tiktok": ["tiktok.com"],
            "facebook": ["facebook.com", "fb.com"],
            "reddit": ["reddit.com"],
            "twitch": ["twitch.tv"],
            "genel": ["twitter.com", "x.com", "instagram.com", "youtube.com"],
        }
        
        domains = domain_map.get(platform, domain_map["genel"])
        
        # Chrome/Brave/Edge tarayicilari icin
        cookie_dosyalari = glob.glob(str(cookies_klasoru / "**/Cookies"), recursive=True)
        for cookie_dosyasi in cookie_dosyalari[:3]:
            try:
                conn = sqlite3.connect(cookie_dosyasi)
                cursor = conn.cursor()
                for domain in domains:
                    cursor.execute("SELECT name FROM cookies WHERE host_key LIKE ? LIMIT 1", (f"%{domain}%",))
                    if cursor.fetchone():
                        conn.close()
                        return True
                conn.close()
            except Exception:
                continue
        
        # Firefox icin
        if "firefox" in str(cookies_klasoru):
            sqlite_dosyalari = glob.glob(str(cookies_klasoru / "*/cookies.sqlite"))
            for sqlite_dosyasi in sqlite_dosyalari[:3]:
                try:
                    conn = sqlite3.connect(sqlite_dosyasi)
                    cursor = conn.cursor()
                    for domain in domains:
                        cursor.execute("SELECT name FROM moz_cookies WHERE baseDomain LIKE ? LIMIT 1", (f"%{domain}%",))
                        if cursor.fetchone():
                            conn.close()
                            return True
                    conn.close()
                except Exception:
                    continue
        
        return False
    
    def _cookies_klasoru_bul(self, tarayici):
        """Tarayici cookies klasorunu bul"""
        ev = Path.home()
        klasorler = {
            "firefox": [ev / ".mozilla" / "firefox"],
            "chrome": [ev / ".config" / "google-chrome"],
            "brave": [ev / ".config" / "BraveSoftware" / "Brave-Browser"],
            "chromium": [ev / ".config" / "chromium"],
            "edge": [ev / ".config" / "microsoft-edge"],
            "opera": [ev / ".config" / "opera"],
            "vivaldi": [ev / ".config" / "vivaldi"],
        }
        for k in klasorler.get(tarayici, []):
            if k.exists():
                return k
        return None
    
    def _twitter_session_var_mi(self, cookies_klasoru):
        """Tarayicida Twitter session cookie'si var mi kontrol et"""
        import sqlite3
        import glob
        
        # Chrome/Brave/Edge tarayicilari icin
        for root in [cookies_klasoru]:
            cookie_dosyalari = glob.glob(str(root / "**/Cookies"), recursive=True)
            for cookie_dosyasi in cookie_dosyalari[:3]:  # max 3 kontrol et
                try:
                    conn = sqlite3.connect(cookie_dosyasi)
                    cursor = conn.cursor()
                    cursor.execute("SELECT name FROM cookies WHERE host_key LIKE '%twitter.com%' OR host_key LIKE '%x.com%' LIMIT 1")
                    sonuc = cursor.fetchone()
                    conn.close()
                    if sonuc:
                        return True
                except Exception:
                    continue
        
        # Firefox icin
        if "firefox" in str(cookies_klasoru):
            sqlite_dosyalari = glob.glob(str(cookies_klasoru / "*/cookies.sqlite"))
            for sqlite_dosyasi in sqlite_dosyalari[:3]:
                try:
                    conn = sqlite3.connect(sqlite_dosyasi)
                    cursor = conn.cursor()
                    cursor.execute("SELECT name FROM moz_cookies WHERE baseDomain LIKE '%twitter.com%' OR baseDomain LIKE '%x.com%' LIMIT 1")
                    sonuc = cursor.fetchone()
                    conn.close()
                    if sonuc:
                        return True
                except Exception:
                    continue
        
        return False

    def _kontrol_yukleme(self):
        eksik = []
        # yt-dlp kontrolu: once Python modulu, sonra exe
        ytdlp_yolu = shutil.which("yt-dlp")
        if BUNDLE_DIR and (BUNDLE_DIR / "yt-dlp.exe").exists():
            ytdlp_yolu = ytdlp_yolu or str(BUNDLE_DIR / "yt-dlp.exe")
        if not HAS_YTDLP and not ytdlp_yolu:
            eksik.append("yt-dlp (pip install yt-dlp)")
        # ffmpeg kontrolu
        ffmpeg_yolu = shutil.which("ffmpeg") or (
            str(BUNDLE_DIR / "ffmpeg.exe") if BUNDLE_DIR and (BUNDLE_DIR / "ffmpeg.exe").exists() else None
        )
        if not ffmpeg_yolu:
            eksik.append("ffmpeg (sudo dnf/apt install ffmpeg)")
        if eksik:
            messagebox.showerror(
                self._t("msg_missing_deps"),
                self._t("msg_missing_deps_detail").format(deps="\n".join(f"- {e}" for e in eksik)),
            )
            self.destroy()
            sys.exit(1)
        
        if not self.bulunan_tarayicilar:
            messagebox.showwarning(
                self._t("no_browser"),
                self._t("no_browser_detail"),
            )

    def _klasor_sec(self):
        sec = filedialog.askdirectory(initialdir=self.klasor_var.get())
        if sec:
            self.klasor_var.set(sec)

    def _pano_yapistir(self):
        try:
            metin = self.clipboard_get()
            self.url_var.set(metin.strip())
            self.url_entry.icursor("end")
        except tk.TclError:
            messagebox.showinfo(self._t("msg_paste_empty"), self._t("msg_paste_empty_detail"))

    def _pano_temizle(self):
        self.url_var.set("")
        self.url_entry.focus_set()

    def _sag_tik_yapistir(self, event):
        self._pano_yapistir()

    def _log_yaz(self, metin):
        self.log.config(state="normal")
        self.log.insert("end", metin + "\n")
        self.log.see("end")

    def _log_temizle(self):
        self.log.config(state="normal")
        self.log.delete("1.0", "end")

    def _kuyruk_oku(self):
        try:
            while True:
                tip, veri = self.msg_queue.get_nowait()
                if tip == "log":
                    self._log_yaz(veri)
                elif tip == "durum":
                    self.durum_var.set(veri)
                elif tip == "progress":
                    self.progress.config(value=veri)
                elif tip == "listelendi":
                    self._liste_doldur(veri)
                elif tip == "bitti":
                    self._islem_bitti(veri)
                elif tip == "hata":
                    self._islem_hata(veri)
        except queue.Empty:
            pass
        self.after(100, self._kuyruk_oku)

    def _getir_baslat(self):
        if self.isleniyor or self.analiz_ediliyor:
            return
        url = self.url_var.get().strip()
        if not url:
            messagebox.showwarning(self._t("msg_no_url"), self._t("msg_no_url_detail"))
            return
        self.analiz_ediliyor = True
        self.getir_btn.config(state="disabled")
        self.indir_btn.config(state="disabled")
        self.liste.delete(0, "end")
        self.cozunurlukler = []
        self.analiz_url = url
        self._log_temizle()
        self.progress.config(value=0)
        self.durum_var.set(self._t("status_analyzing"))
        self._log_yaz(f"{self._t('log_link')} {url}")

        thread = threading.Thread(target=self._getir_thread, args=(url,), daemon=True)
        thread.start()

    def _getir_thread(self, url):
        try:
            tarayici = self._secilen_tarayici(url)
            if tarayici and tarayici != "YOK":
                isim = TARAYICI_ISIMLERI.get(tarayici, {}).get(self.dil, tarayici)
                self.msg_queue.put(("log", f"{self._t('log_browser')} {isim}"))
            
            # yt-dlp.exe yolunu bul
            ytdlp_yolu = shutil.which("yt-dlp")
            if BUNDLE_DIR and (BUNDLE_DIR / "yt-dlp.exe").exists():
                ytdlp_yolu = ytdlp_yolu or str(BUNDLE_DIR / "yt-dlp.exe")
            
            if HAS_YTDLP:
                # Python modulu ile
                opts = {
                    "quiet": True,
                    "no_warnings": True,
                    "noplaylist": True,
                }
                if tarayici and tarayici != "YOK":
                    opts["cookiesfrombrowser"] = (tarayici,)
                try:
                    with YoutubeDL(opts) as ydl:
                        self._ytdl = ydl
                        info = ydl.extract_info(url, download=False)
                except Exception as cookie_err:
                    if "cookie" in str(cookie_err).lower():
                        opts.pop("cookiesfrombrowser", None)
                        self.msg_queue.put(("log", f"Cookie hatasi, cookiesiz devam: {cookie_err}"))
                        with YoutubeDL(opts) as ydl:
                            self._ytdl = ydl
                            info = ydl.extract_info(url, download=False)
                    else:
                        raise
            elif ytdlp_yolu:
                # yt-dlp.exe subprocess ile
                cmd = [ytdlp_yolu, "--dump-json", "--no-playlist", "--quiet", url]
                if tarayici and tarayici != "YOK":
                    cmd = [ytdlp_yolu, "--dump-json", "--no-playlist", "--quiet",
                           "--cookies-from-browser", tarayici, url]
                sonuc = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
                if sonuc.returncode != 0:
                    hata = sonuc.stderr.strip()
                    if "cookie" in hata.lower():
                        self.msg_queue.put(("log", f"Cookie hatasi, cookiesiz devam: {hata[:100]}"))
                        cmd = [ytdlp_yolu, "--dump-json", "--no-playlist", "--quiet", url]
                        sonuc = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
                    if sonuc.returncode != 0:
                        raise Exception(sonuc.stderr.strip() or "yt-dlp calistirilamadi")
                import json
                info = json.loads(sonuc.stdout)
            else:
                raise Exception("yt-dlp bulunamadi")

            baslik = info.get("title") or info.get("id") or ""
            self.msg_queue.put(("log", f"{self._t('log_title')} {str(baslik)[:80]}"))

            gorulen = {}
            formatlar = info.get("formats") or []
            for f in formatlar:
                h = f.get("height")
                ext = f.get("ext", "")
                if h and f.get("vcodec") not in ("none", None):
                    if h not in gorulen or f.get("tbr", 0) > gorulen[h].get("tbr", 0):
                        gorulen[h] = f

            yukseklikler = sorted(gorulen.keys(), reverse=True)

            secenekler = []
            if yukseklikler:
                secenekler.append((self._t("best_quality"), "best", False))
                for h in yukseklikler:
                    etiket = f"{h}p"
                    secenekler.append((etiket, f"height<={h}", False))
            secenekler.append((self._t("audio_only"), "bestaudio", True))

            self.msg_queue.put(("listelendi", (secenekler, yukseklikler)))
        except Exception as e:
            self.msg_queue.put(("hata", str(e)))
        finally:
            self._ytdl = None

    def _liste_doldur(self, veri):
        secenekler, yukseklikler = veri
        self.cozunurlukler = secenekler
        self.analiz_ediliyor = False
        self.getir_btn.config(state="normal")

        for etiket, _, _ in secenekler:
            self.liste.insert("end", etiket)

        if yukseklikler:
            self.liste.selection_set(0)
            self.liste.activate(0)

        self.durum_var.set(
            f"{len(secenekler)} {self._t('options_found')}"
        )
        self.indir_btn.config(state="normal")

    def _indir_baslat(self):
        if self.isleniyor or self.analiz_ediliyor:
            return
        secim = self.liste.curselection()
        if not secim:
            messagebox.showwarning(self._t("msg_no_selection"), self._t("msg_no_selection_detail"))
            return

        etiket, format_secimi, ses_mi = self.cozunurlukler[secim[0]]
        url = self.analiz_url
        if not url:
            url = self.url_var.get().strip()
        klasor = self.klasor_var.get().strip()

        if not os.path.isdir(klasor):
            try:
                os.makedirs(klasor, exist_ok=True)
            except OSError as e:
                messagebox.showerror(self._t("msg_folder_error"), str(e))
                return

        if ses_mi:
            format_sec = "bestaudio/best"
        elif format_secimi == "best":
            format_sec = "bestvideo+bestaudio/best"
        else:
            format_sec = f"bestvideo[{format_secimi}]+bestaudio/best[{format_secimi}]"

        self.isleniyor = True
        self.indir_btn.config(state="disabled")
        self.getir_btn.config(state="disabled")
        self.iptal_btn.config(state="normal")
        self._log_yaz("-" * 50)
        self._log_yaz(f"{self._t('log_title')} {etiket}")
        self._log_yaz(f"{self._t('log_format')} {format_sec}")
        self._log_yaz(f"{self._t('log_folder')} {klasor}")

        thread = threading.Thread(
            target=self._indir_thread,
            args=(url, klasor, format_sec, ses_mi),
            daemon=True,
        )
        thread.start()

    def _indir_thread(self, url, klasor, format_sec, ses_mi):
        # yt-dlp.exe yolunu bul
        ytdlp_yolu = shutil.which("yt-dlp")
        if BUNDLE_DIR and (BUNDLE_DIR / "yt-dlp.exe").exists():
            ytdlp_yolu = ytdlp_yolu or str(BUNDLE_DIR / "yt-dlp.exe")
        
        tarayici = self._secilen_tarayici(url)

        if HAS_YTDLP:
            # Python modulu ile
            def progress_hook(d):
                if d.get("status") == "downloading":
                    total = d.get("total_bytes") or d.get("total_bytes_estimate") or 0
                    done = d.get("downloaded_bytes") or 0
                    if total:
                        yuzde = int(done * 100 / total)
                        hiz = d.get("_speed_str", "")
                        self.msg_queue.put(("progress", yuzde))
                        self.msg_queue.put(("durum", f"{self._t('status_downloading')} %{yuzde} ({hiz})"))
                elif d.get("status") == "finished":
                    self.msg_queue.put(("progress", 100))
                    self.msg_queue.put(("durum", self._t("status_merging")))
                    self.msg_queue.put(("log", self._t("log_merging")))

            opts = {
                "outtmpl": os.path.join(klasor, "%(title)s [%(id)s].%(ext)s"),
                "format": format_sec,
                "progress_hooks": [progress_hook],
                "noplaylist": True,
                "quiet": True,
                "no_warnings": True,
                "noprogress": True,
                "retries": 3,
                "fragment_retries": 3,
                "merge_output_format": "mp4",
            }
            if BUNDLE_DIR:
                ffmpeg_yolu = str(BUNDLE_DIR / "ffmpeg.exe") if (BUNDLE_DIR / "ffmpeg.exe").exists() else None
                if ffmpeg_yolu:
                    opts["ffmpeg_location"] = str(BUNDLE_DIR)
            if tarayici and tarayici != "YOK":
                opts["cookiesfrombrowser"] = (tarayici,)
            if ses_mi:
                opts["postprocessors"] = [{"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": "192"}]
            else:
                opts["postprocessors"] = [{"key": "FFmpegVideoConvertor", "preferedformat": "mp4"}]
            try:
                with YoutubeDL(opts) as ydl:
                    self._ytdl = ydl
                    info = ydl.extract_info(url, download=True)
                    dosya = ydl.prepare_filename(info)
                    if ses_mi:
                        dosya = os.path.splitext(dosya)[0] + ".mp3"
                    self.msg_queue.put(("bitti", dosya))
            except Exception as e:
                if "cookie" in str(e).lower():
                    opts.pop("cookiesfrombrowser", None)
                    self.msg_queue.put(("log", f"Cookie hatasi, cookiesiz devam"))
                    try:
                        with YoutubeDL(opts) as ydl:
                            self._ytdl = ydl
                            info = ydl.extract_info(url, download=True)
                            dosya = ydl.prepare_filename(info)
                            if ses_mi:
                                dosya = os.path.splitext(dosya)[0] + ".mp3"
                            self.msg_queue.put(("bitti", dosya))
                    except Exception as e2:
                        self.msg_queue.put(("hata", str(e2)))
                else:
                    self.msg_queue.put(("hata", str(e)))
            finally:
                self._ytdl = None

        elif ytdlp_yolu:
            # yt-dlp.exe subprocess ile
            cmd = [
                ytdlp_yolu,
                "-f", format_sec,
                "-o", os.path.join(klasor, "%(title)s [%(id)s].%(ext)s"),
                "--merge-output-format", "mp4",
                "--no-playlist",
                "--retries", "3",
                "--no-warnings",
            ]
            if tarayici and tarayici != "YOK":
                cmd += ["--cookies-from-browser", tarayici]
            if ses_mi:
                cmd += ["-x", "--audio-format", "mp3", "--audio-quality", "192"]
            cmd.append(url)
            
            self.msg_queue.put(("durum", self._t("status_downloading")))
            
            proc = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                text=True, bufsize=1
            )
            self._ytdl = proc
            
            for satir in proc.stdout:
                satir = satir.strip()
                if satir:
                    # Progress yuzdesi
                    if "%" in satir:
                        try:
                            import re
                            m = re.search(r'(\d+\.?\d*)%', satir)
                            if m:
                                yuzde = int(float(m.group(1)))
                                self.msg_queue.put(("progress", yuzde))
                                self.msg_queue.put(("durum", f"{self._t('status_downloading')} %{yuzde}"))
                        except Exception:
                            pass
                    self.msg_queue.put(("log", satir))
            
            proc.wait()
            self._ytdl = None
            
            if proc.returncode == 0:
                # Bulunan dosyayi tara
                import glob as glob_mod
                sablon = os.path.join(klasor, "*.*")
                dosyalar = sorted(glob_mod.glob(sablon), key=os.path.getmtime, reverse=True)
                dosya = dosyalar[0] if dosyalar else "Indirildi"
                self.msg_queue.put(("bitti", dosya))
            else:
                self.msg_queue.put(("hata", f"yt-dlp hatasi (kod: {proc.returncode})"))
        else:
            self.msg_queue.put(("hata", "yt-dlp bulunamadi"))

    def _iptal(self):
        self.durum_var.set(self._t("status_cancelled"))
        self._log_yaz(self._t("log_cancel"))
        if self._ytdl is not None:
            try:
                if hasattr(self._ytdl, '_progress_hooks'):
                    self._ytdl._progress_hooks = []
            except Exception:
                pass
            try:
                if hasattr(self._ytdl, 'kill'):
                    self._ytdl.kill()
                elif hasattr(self._ytdl, 'terminate'):
                    self._ytdl.terminate()
            except Exception:
                pass
        self.isleniyor = False
        self.indir_btn.config(state="normal")
        self.getir_btn.config(state="normal")
        self.iptal_btn.config(state="disabled")

    def _islem_bitti(self, dosya):
        self.isleniyor = False
        self.progress.config(value=100)
        self.durum_var.set(self._t("status_done"))
        self.indir_btn.config(state="normal")
        self.getir_btn.config(state="normal")
        self.iptal_btn.config(state="disabled")
        self._log_yaz("-" * 50)
        self._log_yaz(f"{self._t('log_saved')} {dosya}")
        sonuc = messagebox.askyesno(
            self._t("msg_complete"),
            f"{dosya}\n\n{self._t('msg_complete_detail')}",
        )
        if sonuc:
            subprocess.Popen(["xdg-open", os.path.dirname(dosya)])

    def _islem_hata(self, hata):
        self.isleniyor = False
        self.analiz_ediliyor = False
        self.progress.config(value=0)
        self.durum_var.set(self._t("status_error"))
        self.indir_btn.config(state="normal")
        self.getir_btn.config(state="normal")
        self.iptal_btn.config(state="disabled")
        hata_tr = cevir_hata(hata, self.dil)
        self._log_yaz("-" * 50)
        self._log_yaz(f"HATA: {hata_tr}")
        messagebox.showerror(self._t("status_error"), hata_tr)

    # ============================================================
    # HELP MENU Fonksiyonlari
    # ============================================================
    def _info_goster(self):
        mesaj = (
            f"{self._t('app_title')}\n"
            f"Versiyon: {VERSION}\n"
            f"{self._t('info_desc')}\n\n"
            f"Gelistirici: Berk8858\n"
            f"Lisans: MIT\n"
            f"GitHub: {GITHUB_URL}"
        )
        messagebox.showinfo(self._t("info_title"), mesaj)

    def _kisayollar_goster(self):
        mesaj = (
            "Klavye Kisayollari:\n\n"
            "Ctrl+V / Sag Tik  →  Panodan yapistir\n"
            "Enter  →  Cozunurlukleri getir\n"
            "Escape  →  Iptal et\n"
            "Cift Tik  →  Indirmeyi baslat"
        )
        messagebox.showinfo(self._t("shortcuts_title"), mesaj)

    @staticmethod
    def _versiyon_ayristir(versiyon_str):
        """Versiyon string'ini karsilastirilabilir tuple'a cevir.

        '1.6K' -> (1, 6, 0)
        '1.5.3' -> (1, 5, 3)
        '1.5'   -> (1, 5, 0)
        Gecersiz -> None
        """
        try:
            parts = []
            for x in versiyon_str.split("."):
                num = "".join(c for c in x if c.isdigit())
                parts.append(int(num) if num else 0)
            return tuple(parts) if parts else None
        except (ValueError, AttributeError):
            return None

    def _guncelleme_kontrol(self):
        import urllib.request
        import json

        self._log_yaz("Guncelleme kontrol ediliyor...")
        self.durum_var.set(self._t("update_checking"))

        try:
            url = "https://api.github.com/repos/Berk8858/Download/releases"
            req = urllib.request.Request(url, headers={
                "Accept": "application/vnd.github.v3+json",
                "User-Agent": "Multi-Downloader",
            })
            response = urllib.request.urlopen(req, timeout=15)
            data = json.loads(response.read())

            if not data:
                raise Exception("GitHub API bos yanit dondu")

            versiyonlar = []
            for r in data:
                tag = r.get("tag_name", "")
                if tag.startswith("v"):
                    ham = tag[1:]
                    parsed = self._versiyon_ayristir(ham)
                    if parsed is not None:
                        versiyonlar.append((parsed, ham, r))

            if not versiyonlar:
                raise Exception("Gecerli versiyon bulunamadi")

            en_yeni = max(versiyonlar, key=lambda x: x[0])
            parsed_yeni, ham_yeni, release = en_yeni

            self._son_release = release

            mevcut_parsed = self._versiyon_ayristir(VERSION)
            if mevcut_parsed is None:
                raise Exception(f"Mevcut versiyon gecersiz: {VERSION}")

            if parsed_yeni <= mevcut_parsed:
                self._log_yaz(f"Guncel versiyon: v{VERSION}")
                messagebox.showinfo(
                    self._t("update_title"),
                    f"Guncel versiyonu kullaniyorsunuz.\n\nMevcut: v{VERSION}"
                )
                return

            asset_satirlari = ""
            for asset in release.get("assets", []):
                name = asset.get("name", "")
                if name.lower().endswith(".exe") or "-linux-" in name or "-macos" in name:
                    boyut = asset.get("size", 0) // 1024 // 1024
                    asset_satirlari += f"\n  {name} ({boyut}MB)"

            changelog = release.get("body", "") or ""
            if changelog:
                changelog = f"\n\nDegisiklikler:\n{changelog[:500]}"

            mesaj = (
                f"Yeni versiyon mevcut!\n\n"
                f"Mevcut : v{VERSION}\n"
                f"Son    : v{ham_yeni}"
                f"{asset_satirlari}"
                f"{changelog}\n\n"
                f"Guncellemek ister misiniz?"
            )

            cevap = messagebox.askyesno(self._t("update_title"), mesaj)
            if cevap:
                self._guncelleme_indir(ham_yeni, release)

        except urllib.error.URLError as e:
            hata = f"Internet baglantisi hatasi:\n{e}"
            self._log_yaz(f"HATA: {hata}")
            messagebox.showwarning(self._t("update_title"), hata)
        except Exception as e:
            hata = f"Guncelleme kontrolu yapilamadi:\n{e}"
            self._log_yaz(f"HATA: {hata}")
            messagebox.showwarning(self._t("update_title"), self._t("update_error"))

    def _guncelleme_indir(self, versiyon, release_data):
        import urllib.request
        import hashlib
        import shutil
        import tempfile
        import subprocess

        self._log_yaz(f"v{versiyon} indiriliyor...")
        self.durum_var.set(f"v{versiyon} indiriliyor...")
        yeni_dosya = None

        try:
            frozen = getattr(sys, 'frozen', False)

            if frozen:
                exe_asset = None
                for asset in release_data.get("assets", []):
                    if asset.get("name", "").lower().endswith(".exe"):
                        exe_asset = asset
                        break

                if not exe_asset:
                    raise Exception("Indirilebilir EXE dosyasi bulunamadi")

                download_url = exe_asset["browser_download_url"]
                beklenen_boyut = exe_asset.get("size", 0)

                beklenen_hash = None
                digest = exe_asset.get("digest", "")
                if digest and ":" in digest:
                    beklenen_hash = digest.split(":", 1)[1]

                self._log_yaz(
                    f"Dosya: {exe_asset['name']} "
                    f"({beklenen_boyut // 1024 // 1024}MB)"
                )

                yeni_dosya = os.path.join(
                    tempfile.gettempdir(),
                    f"Multi-Downloader-v{versiyon}.exe"
                )

                self._log_yaz("Indiriliyor...")
                req = urllib.request.Request(
                    download_url,
                    headers={"User-Agent": "Multi-Downloader"},
                )
                try:
                    with urllib.request.urlopen(req, timeout=120) as resp:
                        toplam = int(resp.headers.get("Content-Length", 0))
                        indirilen = 0
                        sha256 = hashlib.sha256()
                        with open(yeni_dosya, "wb") as f:
                            while True:
                                chunk = resp.read(65536)
                                if not chunk:
                                    break
                                f.write(chunk)
                                sha256.update(chunk)
                                indirilen += len(chunk)
                                if toplam > 0:
                                    yuzde = indirilen * 100 // toplam
                                    self.durum_var.set(
                                        f"Indiriliyor... %{yuzde}"
                                    )
                except Exception:
                    urllib.request.urlretrieve(download_url, yeni_dosya)
                    sha256 = hashlib.sha256()
                    with open(yeni_dosya, "rb") as f:
                        for chunk in iter(lambda: f.read(65536), b""):
                            sha256.update(chunk)

                indirilen_boyut = os.path.getsize(yeni_dosya)
                if indirilen_boyut < 1_000_000:
                    os.remove(yeni_dosya)
                    raise Exception(
                        f"Indirilen dosya cok kucuk ({indirilen_boyut} byte)"
                    )
                self._log_yaz(
                    f"Indirme tamam ({indirilen_boyut // 1024 // 1024}MB)"
                )

                if beklenen_hash:
                    self._log_yaz("SHA256 dogrulamasi yapiliyor...")
                    gercek_hash = sha256.hexdigest()
                    if gercek_hash.lower() != beklenen_hash.lower():
                        os.remove(yeni_dosya)
                        raise Exception(
                            f"SHA256 dogrulamasi basarisiz!\n"
                            f"Beklenen : {beklenen_hash}\n"
                            f"Gercek   : {gercek_hash}"
                        )
                    self._log_yaz("SHA256 dogrulandi ✓")
                else:
                    self._log_yaz("Uyari: Hash dogrulamasi yok, atlaniyor")

                mevcut_dosya = os.path.abspath(sys.argv[0])

                cevap = messagebox.askyesno(
                    self._t("update_title"),
                    f"v{versiyon} indirildi ve dogrulandi!\n\n"
                    f"Simdi guncellensin mi?\n"
                    f"(Program yeniden baslatilacak)",
                )
                if not cevap:
                    if os.path.exists(yeni_dosya):
                        os.remove(yeni_dosya)
                    return

                if sys.platform == "win32":
                    batch_icerik = (
                        "@echo off\r\n"
                        "timeout /t 2 /nobreak >nul\r\n"
                        f'copy /Y "{yeni_dosya}" "{mevcut_dosya}"\r\n'
                        f'start "" "{mevcut_dosya}"\r\n'
                        'del "%~f0"\r\n'
                    )
                    batch_dosya = os.path.join(
                        tempfile.gettempdir(),
                        "update_multidownloader.bat",
                    )
                    with open(batch_dosya, "w", encoding="ascii") as bf:
                        bf.write(batch_icerik)

                    self._log_yaz("Guncelleme baslatiliyor...")
                    try:
                        subprocess.Popen(
                            [batch_dosya], shell=True,
                            creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0,
                        )
                    except Exception:
                        subprocess.Popen([batch_dosya], shell=True)
                    self.after(500, self.destroy)
                else:
                    mevcut_klasor = os.path.dirname(mevcut_dosya)
                    yedek_dosya = mevcut_dosya + ".yedek"
                    self._log_yaz(f"Yedekleniyor: {yedek_dosya}")
                    shutil.copy2(mevcut_dosya, yedek_dosya)

                    shutil.copy2(yeni_dosya, mevcut_dosya)
                    os.chmod(mevcut_dosya, 0o755)
                    self._log_yaz("Guncelleme tamam!")

                    messagebox.showinfo(
                        self._t("update_title"),
                        f"v{versiyon} guncellendi!\n\n"
                        f"Program yeniden baslatilacak.",
                    )
                    python_yolu = sys.executable
                    if "pythonw" in python_yolu.lower():
                        python_yolu = python_yolu.replace("pythonw", "python")
                    try:
                        subprocess.Popen(
                            [python_yolu, mevcut_dosya] + sys.argv[1:],
                            cwd=mevcut_klasor,
                            creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0,
                        )
                    except Exception:
                        subprocess.Popen(
                            [python_yolu, mevcut_dosya] + sys.argv[1:],
                            cwd=mevcut_klasor,
                        )
                    self.after(500, self.destroy)
            else:
                self._log_yaz("Python modu - .py guncelleniyor...")

                raw_url = (
                    "https://raw.githubusercontent.com/"
                    "Berk8858/Download/main/twitter-indirici.py"
                )
                data = None
                for url in [
                    raw_url,
                    raw_url.replace("raw.githubusercontent.com",
                                    "github.com/Berk8858/Download/raw"),
                ]:
                    try:
                        req = urllib.request.Request(
                            url,
                            headers={"User-Agent": "Multi-Downloader"},
                        )
                        data = urllib.request.urlopen(req, timeout=30).read()
                        break
                    except Exception:
                        continue

                if data is None or len(data) < 1000:
                    raise Exception(
                        f"Indirilen dosya cok kucuk "
                        f"({0 if data is None else len(data)} byte)"
                    )

                icerik = data.decode("utf-8", errors="ignore")
                if "VERSION" not in icerik:
                    raise Exception("Indirilen dosya gecerli gorunmuyor")

                yeni_v = self._versiyon_ayristir(
                    icerik.split('VERSION = "')[1].split('"')[0]
                    if 'VERSION = "' in icerik else ""
                )
                if yeni_v is None:
                    raise Exception("Yeni dosyada gecerli versiyon bulunamadi")

                mevcut_dosya = os.path.abspath(sys.argv[0])
                mevcut_klasor = os.path.dirname(mevcut_dosya)

                yedek_dosya = mevcut_dosya + ".yedek"
                self._log_yaz(f"Yedekleniyor: {yedek_dosya}")
                shutil.copy2(mevcut_dosya, yedek_dosya)

                with open(mevcut_dosya, "wb") as f:
                    f.write(data)

                self._log_yaz("Guncelleme tamam!")

                cevap = messagebox.askyesno(
                    self._t("update_title"),
                    f"v{versiyon} guncellendi!\n\n"
                    f"Program yeniden baslatilacak.\nDevam edilsin mi?",
                )
                if cevap:
                    python_yolu = sys.executable
                    if "pythonw" in python_yolu.lower():
                        python_yolu = python_yolu.replace("pythonw", "python")
                    try:
                        subprocess.Popen(
                            [python_yolu, mevcut_dosya] + sys.argv[1:],
                            cwd=mevcut_klasor,
                            creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0,
                        )
                    except Exception:
                        subprocess.Popen(
                            [python_yolu, mevcut_dosya] + sys.argv[1:],
                            cwd=mevcut_klasor,
                        )
                    self.after(500, self.destroy)

        except Exception as e:
            if yeni_dosya and os.path.exists(yeni_dosya):
                try:
                    os.remove(yeni_dosya)
                except OSError:
                    pass
            hata = f"Guncelleme hatasi:\n{e}"
            self._log_yaz(f"HATA: {hata}")
            messagebox.showerror(self._t("update_title"), hata)

    def _github_ac(self):
        try:
            import webbrowser
            webbrowser.open(GITHUB_URL)
        except Exception:
            pass


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Twitter/X Video Indirici")
    parser.add_argument("--lang", "-l", choices=["tr", "es", "pt", "it", "ja", "ko", "zh"],
                        help="Dil secimi (ornek: --lang en)")
    args = parser.parse_args()
    
    app = TwitterIndirici(baslangic_dili=args.lang)
    app.mainloop()
