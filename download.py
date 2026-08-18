#!/usr/bin/env python3
# Twitter/X Video Indirici - GUI
# yt-dlp tabanli cozunurluk sec + indir

import os
import re
import threading
import subprocess
import shutil
import queue
import sys
from pathlib import Path

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinter.scrolledtext import ScrolledText

try:
    from yt_dlp import YoutubeDL
    HAS_YTDLP = True
except ImportError:
    HAS_YTDLP = False

def _varsayilan_indirme_klasoru():
    """XDG kullanici indirme klasorunu bul (ornek: ~/Indirilenler)."""
    try:
        import subprocess
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
    def __init__(self):
        super().__init__()
        self.title("Twitter/X Video Indirici")
        self.geometry("680x680")
        self.minsize(620, 580)

        self.msg_queue = queue.Queue()
        self.isleniyor = False
        self.analiz_ediliyor = False
        self._ytdl = None
        self.cozunurlukler = []
        self.analiz_url = ""

        self._kontrol_yukleme()
        self._arayuz_kur()
        self.after(100, self._kuyruk_oku)

    def _arayuz_kur(self):
        pad = {"padx": 12, "pady": 4}

        ust = ttk.Frame(self)
        ust.pack(fill="x", **pad)

        ttk.Label(ust, text="Tweet / X linki:").pack(anchor="w")
        self.url_var = tk.StringVar()
        url_satir = ttk.Frame(ust)
        url_satir.pack(fill="x", pady=(2, 6))
        self.url_entry = ttk.Entry(url_satir, textvariable=self.url_var, font=("Sans", 11))
        self.url_entry.pack(side="left", fill="x", expand=True)
        self.url_entry.bind("<Return>", lambda e: self._getir_baslat())
        self.url_entry.bind("<Button-3>", self._sag_tik_yapistir)
        ttk.Button(url_satir, text="Paste", width=7,
                   command=self._pano_yapistir).pack(side="left", padx=(6, 0))
        ttk.Button(url_satir, text="Clear", width=6,
                   command=self._pano_temizle).pack(side="left", padx=(4, 0))

        buton_satir = ttk.Frame(ust)
        buton_satir.pack(fill="x")

        ttk.Label(buton_satir, text="Kayit:").pack(side="left")
        self.klasor_var = tk.StringVar(value=INDIRME_KONUMU)
        self.klasor_entry = ttk.Entry(buton_satir, textvariable=self.klasor_var, width=24)
        self.klasor_entry.pack(side="left", fill="x", expand=True, padx=6)
        ttk.Button(buton_satir, text="...", width=3,
                   command=self._klasor_sec).pack(side="left")

        self.getir_btn = ttk.Button(ust, text="1) Cozunurlukleri Getir",
                                    command=self._getir_baslat)
        self.getir_btn.pack(fill="x", pady=(8, 2))

        ttk.Label(self, text="Cozunurluk sec (2):").pack(anchor="w", padx=14)
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
        self.iptal_btn = ttk.Button(buton, text="Iptal", state="disabled",
                                    command=self._iptal)
        self.iptal_btn.pack(side="right")
        self.indir_btn = ttk.Button(buton, text="3)  I N D I R",
                                    state="disabled", command=self._indir_baslat)
        self.indir_btn.pack(side="right", padx=8)

        self.durum_var = tk.StringVar(value="Hazir")
        ttk.Label(self, textvariable=self.durum_var,
                  font=("Sans", 9)).pack(fill="x", padx=14)
        self.progress = ttk.Progressbar(self, mode="determinate")
        self.progress.pack(fill="x", padx=12, pady=(2, 4))

        self.log = ScrolledText(self, height=7, state="disabled",
                                font=("Consolas", 9), wrap="word")
        self.log.pack(fill="both", expand=True, padx=12, pady=(4, 10))

    def _kontrol_yukleme(self):
        eksik = []
        if not HAS_YTDLP:
            eksik.append("yt-dlp (pip install yt-dlp)")
        if not shutil.which("ffmpeg"):
            eksik.append("ffmpeg (sudo dnf install ffmpeg)")
        if eksik:
            messagebox.showerror(
                "Eksik bagimlilik",
                "Eksik olan:\n" + "\n".join(f"- {e}" for e in eksik) +
                "\n\nOnce bunlari kurun.",
            )
            self.destroy()
            sys.exit(1)

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
            messagebox.showinfo("Pano bos", "Panoda metin yok.")

    def _pano_temizle(self):
        self.url_var.set("")
        self.url_entry.focus_set()

    def _sag_tik_yapistir(self, event):
        self._pano_yapistir()

    def _log_yaz(self, metin):
        self.log.config(state="normal")
        self.log.insert("end", metin + "\n")
        self.log.see("end")
        self.log.config(state="disabled")

    def _log_temizle(self):
        self.log.config(state="normal")
        self.log.delete("1.0", "end")
        self.log.config(state="disabled")

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
            messagebox.showwarning("Link gerekli", "Tweet / X linki yapistir.")
            return
        self.analiz_ediliyor = True
        self.getir_btn.config(state="disabled")
        self.indir_btn.config(state="disabled")
        self.liste.delete(0, "end")
        self.cozunurlukler = []
        self.analiz_url = url
        self._log_temizle()
        self.progress.config(value=0)
        self.durum_var.set("Analiz ediliyor...")
        self._log_yaz("Link: " + url)

        thread = threading.Thread(target=self._getir_thread, args=(url,), daemon=True)
        thread.start()

    def _getir_thread(self, url):
        try:
            opts = {
                "quiet": True,
                "no_warnings": True,
                "noplaylist": True,
            }
            with YoutubeDL(opts) as ydl:
                self._ytdl = ydl
                info = ydl.extract_info(url, download=False)

            baslik = info.get("title") or info.get("id") or ""
            self.msg_queue.put(("log", "Baslik: " + str(baslik)[:80]))

            gorulen = {}
            formatlar = info.get("formats") or []
            for f in formatlar:
                h = f.get("height")
                if h and f.get("vcodec") not in ("none", None):
                    if h not in gorulen or f.get("tbr", 0) > gorulen[h].get("tbr", 0):
                        gorulen[h] = f

            yukseklikler = sorted(gorulen.keys(), reverse=True)

            secenekler = []
            if yukseklikler:
                secenekler.append(("En iyi kalite (en yuksek)", "best", False))
                for h in yukseklikler:
                    etiket = f"{h}p"
                    secenekler.append((etiket, f"height<={h}", False))
            secenekler.append(("Sadece ses (MP3)", "bestaudio", True))

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
            f"{len(secenekler)} secenek bulundu. Birini sec, INDIR'e bas."
        )
        self.indir_btn.config(state="normal")

    def _indir_baslat(self):
        if self.isleniyor or self.analiz_ediliyor:
            return
        secim = self.liste.curselection()
        if not secim:
            messagebox.showwarning("Secim yok", "Once bir cozunurluk sec.")
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
                messagebox.showerror("Klasor hatasi", str(e))
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
        self._log_yaz(f"Secim: {etiket}")
        self._log_yaz(f"Format: {format_sec}")
        self._log_yaz(f"Klasor: {klasor}")

        thread = threading.Thread(
            target=self._indir_thread,
            args=(url, klasor, format_sec, ses_mi),
            daemon=True,
        )
        thread.start()

    def _indir_thread(self, url, klasor, format_sec, ses_mi):
        def progress_hook(d):
            if d.get("status") == "downloading":
                total = d.get("total_bytes") or d.get("total_bytes_estimate") or 0
                done = d.get("downloaded_bytes") or 0
                if total:
                    yuzde = int(done * 100 / total)
                    hiz = d.get("_speed_str", "")
                    self.msg_queue.put(("progress", yuzde))
                    self.msg_queue.put(("durum", f"Indiriliyor... %{yuzde} ({hiz})"))
            elif d.get("status") == "finished":
                self.msg_queue.put(("progress", 100))
                self.msg_queue.put(("durum", "Birlesiyor..."))
                self.msg_queue.put(("log", "Indirme tamam, birlestiriliyor..."))

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
        }

        if ses_mi:
            opts["postprocessors"] = [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }]

        try:
            with YoutubeDL(opts) as ydl:
                self._ytdl = ydl
                info = ydl.extract_info(url, download=True)
                dosya = ydl.prepare_filename(info)
                if ses_mi:
                    dosya = os.path.splitext(dosya)[0] + ".mp3"
                self.msg_queue.put(("bitti", dosya))
        except Exception as e:
            self.msg_queue.put(("hata", str(e)))
        finally:
            self._ytdl = None

    def _iptal(self):
        self.durum_var.set("Iptal ediliyor...")
        self._log_yaz("Iptal istegi gonderildi.")
        if self._ytdl is not None:
            try:
                self._ytdl._progress_hooks = []
            except Exception:
                pass

    def _islem_bitti(self, dosya):
        self.isleniyor = False
        self.progress.config(value=100)
        self.durum_var.set("Tamamlandi")
        self.indir_btn.config(state="normal")
        self.getir_btn.config(state="normal")
        self.iptal_btn.config(state="disabled")
        self._log_yaz("-" * 50)
        self._log_yaz("Kaydedildi: " + dosya)
        sonuc = messagebox.askyesno(
            "Indirme tamamlandi",
            f"Dosya kaydedildi:\n{dosya}\n\nKlasoru acilsin mi?",
        )
        if sonuc:
            subprocess.Popen(["xdg-open", os.path.dirname(dosya)])

    def _islem_hata(self, hata):
        self.isleniyor = False
        self.analiz_ediliyor = False
        self.progress.config(value=0)
        self.durum_var.set("Hata")
        self.indir_btn.config(state="normal")
        self.getir_btn.config(state="normal")
        self.iptal_btn.config(state="disabled")
        self._log_yaz("-" * 50)
        self._log_yaz("HATA: " + hata)
        messagebox.showerror("Hata", hata)


if __name__ == "__main__":
    app = TwitterIndirici()
    app.mainloop()
