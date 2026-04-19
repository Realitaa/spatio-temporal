# Spatio-Temporal Data Analysis System

Sistem analisis aktivitas manusia berbasis video menggunakan pendekatan numerik dan kalkulus integral (integral ganda) untuk menghitung kepadatan aktivitas secara spatio-temporal.

## Deskripsi Proyek
Proyek ini dirancang untuk menganalisis rekaman video dan mengekstrak data aktivitas manusia dengan membagi area video menjadi grid dan menghitung perubahan intensitas piksel antar frame. Hasil analisis disajikan dalam bentuk grafik deret waktu (time-series), statistik ringkasan, dan heatmap aktivitas.

## Teknologi Utama
- **Backend:** Django 5.1 (Python 3.12)
- **Frontend:** Vue 3, Inertia.js, Vite
- **UI Framework:** Nuxt UI (Vite version), Tailwind CSS
- **Analisis Gambar:** OpenCV (cv2), NumPy
- **Visualisasi:** Chart.js, KaTeX (untuk rumus matematika)
- **Database:** SQLite

## Fitur Utama
1. **Upload Video:** Mendukung pengunggahan file video untuk dianalisis.
2. **ROI (Region of Interest) Selection:** Pengguna dapat memilih area spesifik dalam video yang ingin dianalisis.
3. **Analisis Numerik:**
   - Deteksi gerakan menggunakan perbedaan frame (frame differencing).
   - Perhitungan kepadatan aktivitas menggunakan grid (spatio).
   - Akumulasi aktivitas sepanjang waktu (temporal).
4. **Dashboard Hasil:**
   - Grafik aktivitas sepanjang durasi video.
   - Heatmap untuk melihat lokasi dengan aktivitas tertinggi.
   - Statistik ringkasan (rata-rata, puncak aktivitas, durasi, dll).

## Instalasi

### Prasyarat
- Python 3.12+
- Node.js & npm/pnpm

### Langkah-langkah
1. **Clone repositori:**
   ```bash
   git clone https://github.com/Realitaa/spatio-temporal.git
   cd spatio-temporal
   ```

2. **Setup Backend:**
   ```bash
   # Buat virtual environment
   python -m venv .venv
   source .venv/bin/activate  # Untuk Linux/macOS

   # Install dependensi
   pip install -r requirements.txt

   # Jalankan migrasi database
   python manage.py migrate
   ```

3. **Setup Frontend:**
   ```bash
   # Install dependensi node
   npm install

   # Jalankan server pengembangan Vite
   npm run dev
   ```

4. **Jalankan Server Django:**
   Buka terminal baru (dengan virtual environment aktif):
   ```bash
   python manage.py runserver
   ```

Aplikasi dapat diakses melalui browser (biasanya di `http://localhost:8000`).

## Struktur Direktori Utama
- `/canvas`: Aplikasi Django utama yang menangani logika analisis video dan penyimpanan data.
- `/frontend`: Berisi kode sumber Vue 3, komponen UI, dan aset frontend.
- `/spatio-temporal`: Konfigurasi proyek Django (settings, urls, dll).
- `/public`: Aset statis publik.
- `/uploads`: Direktori penyimpanan video yang diunggah dan thumbnail.

---
Dikembangkan untuk keperluan analisis data aktivitas berbasis kalkulus numerik untuk mata kuliah kalkulus integral.
