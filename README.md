# Sistem Donanım ve Kaynak Takip Monitörü

Python ve `tkinter` kullanılarak geliştirilmiş; işlemci, bellek, depolama ve ağ veri akışını dinamik görsel göstergelerle anlık takip eden hafif bir masaüstü izleme uygulaması.

## Özellikler
- **İşlemci (CPU):** Kullanım yüzdesi ve anlık frekans (MHz) takibi.
- **Bellek (RAM):** Toplam, kullanılan miktar (GB) ve yüzde göstergesi.
- **Depolama (Disk):** C: sürücüsü doluluk oranı ve kalan boş alan analizi.
- **Ağ (Network):** Canlı gönderilen (TX) ve alınan (RX) veri akışı.
- **Dinamik Uyarı Mekanizması:** Kritik kaynak tüketiminde (%85+ CPU/RAM veya %90+ Disk) otomatik renk değişimi ve durum uyarısı.
- **Arka Plan Threading:** Arayüzün donmasını engelleyen çoklu iş parçacığı mimarisi.

## Kullanılan Teknolojiler
- Python 3
- Tkinter (Custom TTK Themes)
- psutil
- PyInstaller

## Çalıştırma

### 1. Hazır Sürüm (.exe)
Herhangi bir Python kurulumu gerekmeden, repo içindeki `sistem.exe` dosyasına çift tıklayarak doğrudan çalıştırabilirsiniz.

### 2. Kaynak Koddan Çalıştırma
```bash
pip install psutil
python sistem_monitor_gui.py
