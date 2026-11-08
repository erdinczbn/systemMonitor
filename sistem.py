import tkinter as tk
from tkinter import ttk
import threading
import time
import os
import psutil

class SistemMonitorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistem Donanım ve Kaynak Takip")
        self.root.geometry("480x560")
        self.root.resizable(False, False)
        self.root.configure(bg="#0f172a")
        self.calisiyor = True
        self.stil = ttk.Style()
        self.stil.theme_use("clam")
        self.stil.configure("Mavi.Horizontal.TProgressbar", troughcolor="#1e293b", background="#0284c7", thickness=14)
        self.stil.configure("Turuncu.Horizontal.TProgressbar", troughcolor="#1e293b", background="#f59e0b", thickness=14)
        self.stil.configure("Kirmizi.Horizontal.TProgressbar", troughcolor="#1e293b", background="#ef4444", thickness=14)
        self.arayuz_olustur()
        self.thread = threading.Thread(target=self.veri_guncelle_dongusu, daemon=True)
        self.thread.start(
        self.root.protocol("WM_DELETE_WINDOW", self.kapat)

    def bayt_donustur(self, bayt):
        for birim in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bayt < 1024:
                return f"{bayt:.2f} {birim}"
            bayt /= 1024
        return f"{bayt:.2f} PB"

    def kart_olustur(self, baslik):
        cerceve = tk.Frame(self.root, bg="#1e293b", bd=0, highlightthickness=1, highlightbackground="#334155")
        cerceve.pack(fill="x", padx=16, pady=6)
        
        lbl_baslik = tk.Label(cerceve, text=baslik, font=("Segoe UI", 10, "bold"), fg="#38bdf8", bg="#1e293b")
        lbl_baslik.pack(anchor="w", padx=12, pady=(8, 2))
        return cerceve

    def arayuz_olustur(self):
        lbl_ana_baslik = tk.Label(
            self.root, 
            text="SİSTEM PERFORMANS MONİTÖRÜ", 
            font=("Segoe UI", 12, "bold"), 
            fg="#f8fafc", 
            bg="#0f172a"
        )
        lbl_ana_baslik.pack(pady=(14, 6))

        # 1. CPU
        kart_cpu = self.kart_olustur("İŞLEMCİ (CPU)")
        self.lbl_cpu_detay = tk.Label(kart_cpu, text="Yükleniyor...", font=("Segoe UI", 9), fg="#94a3b8", bg="#1e293b")
        self.lbl_cpu_detay.pack(anchor="w", padx=12)
        self.bar_cpu = ttk.Progressbar(kart_cpu, style="Mavi.Horizontal.TProgressbar", length=440)
        self.bar_cpu.pack(padx=12, pady=(4, 10))

        # 2. RAM
        kart_ram = self.kart_olustur("BELLEK (RAM)")
        self.lbl_ram_detay = tk.Label(kart_ram, text="Yükleniyor...", font=("Segoe UI", 9), fg="#94a3b8", bg="#1e293b")
        self.lbl_ram_detay.pack(anchor="w", padx=12)
        self.bar_ram = ttk.Progressbar(kart_ram, style="Mavi.Horizontal.TProgressbar", length=440)
        self.bar_ram.pack(padx=12, pady=(4, 10))

        # 3. Disk
        kart_disk = self.kart_olustur("DEPOLAMA (C: SÜRÜCÜSÜ)")
        self.lbl_disk_detay = tk.Label(kart_disk, text="Yükleniyor...", font=("Segoe UI", 9), fg="#94a3b8", bg="#1e293b")
        self.lbl_disk_detay.pack(anchor="w", padx=12)
        self.bar_disk = ttk.Progressbar(kart_disk, style="Mavi.Horizontal.TProgressbar", length=440)
        self.bar_disk.pack(padx=12, pady=(4, 10))

        # 4. Ağ
        kart_alt = tk.Frame(self.root, bg="#1e293b", highlightthickness=1, highlightbackground="#334155")
        kart_alt.pack(fill="x", padx=16, pady=6)
        lbl_ag_baslik = tk.Label(kart_alt, text="AĞ VERİ AKIŞI", font=("Segoe UI", 10, "bold"), fg="#38bdf8", bg="#1e293b")
        lbl_ag_baslik.pack(anchor="w", padx=12, pady=(8, 2))
        self.lbl_ag_detay = tk.Label(kart_alt, text="TX: 0 MB | RX: 0 MB", font=("Segoe UI", 9), fg="#cbd5e1", bg="#1e293b")
        self.lbl_ag_detay.pack(anchor="w", padx=12, pady=(0, 8))

        # Durum Mesajı
        self.lbl_durum = tk.Label(
            self.root, 
            text="● Sistem Durumu: Kontrol ediliyor...", 
            font=("Segoe UI", 9, "bold"), 
            fg="#10b981", 
            bg="#0f172a"
        )
        self.lbl_durum.pack(pady=(10, 4))

    def stil_sec(self, yuzde):
        if yuzde > 85:
            return "Kirmizi.Horizontal.TProgressbar"
        elif yuzde > 65:
            return "Turuncu.Horizontal.TProgressbar"
        return "Mavi.Horizontal.TProgressbar"

    def veri_guncelle_dongusu(self):
        while self.calisiyor:
            try:
                cpu = psutil.cpu_percent(interval=0.6)
                frekans = psutil.cpu_freq()
                mhz = f"{frekans.current:.0f} MHz" if frekans else "N/A"
                ram = psutil.virtual_memory()
                disk = psutil.disk_usage('C:\\' if os.name == 'nt' else '/')
                ag = psutil.net_io_counters()

                self.root.after(0, self.arayuzu_guncelle, cpu, mhz, ram, disk, ag)
            except Exception:
                pass
            time.sleep(0.5)

    def arayuzu_guncelle(self, cpu, mhz, ram, disk, ag):
        # CPU
        self.lbl_cpu_detay.config(text=f"Kullanım: %{cpu:.1f}  |  Çalışma Hızı: {mhz}")
        self.bar_cpu["value"] = cpu
        self.bar_cpu.config(style=self.stil_sec(cpu))

        # RAM
        self.lbl_ram_detay.config(text=f"Kullanım: %{ram.percent:.1f}  |  {self.bayt_donustur(ram.used)} / {self.bayt_donustur(ram.total)}")
        self.bar_ram["value"] = ram.percent
        self.bar_ram.config(style=self.stil_sec(ram.percent))

        # Disk
        self.lbl_disk_detay.config(text=f"Doluluk: %{disk.percent:.1f}  |  Kalan Boş Alan: {self.bayt_donustur(disk.free)}")
        self.bar_disk["value"] = disk.percent
        self.bar_disk.config(style=self.stil_sec(disk.percent))

        # Ağ
        self.lbl_ag_detay.config(text=f"Gönderilen (TX): {self.bayt_donustur(ag.bytes_sent)}   |   Alınan (RX): {self.bayt_donustur(ag.bytes_recv)}")

        # Uyarı Durumu
        if disk.percent > 90:
            self.lbl_durum.config(text="⚠ DİKKAT: C: Sürücüsü dolmak üzere!", fg="#ef4444")
        elif cpu > 85 or ram.percent > 85:
            self.lbl_durum.config(text="⚠ DİKKAT: Yüksek kaynak tüketimi!", fg="#f59e0b")
        else:
            self.lbl_durum.config(text="● Sistem stabil ve normal çalışıyor.", fg="#10b981")

    def kapat(self):
        self.calisiyor = False
        self.root.destroy()

if __name__ == "__main__":
    pencere = tk.Tk()
    uygulama = SistemMonitorGUI(pencere)
    pencere.mainloop()
