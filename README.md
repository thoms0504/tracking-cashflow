# 💰 Cashflow Tracker Pro

Cashflow Tracker Pro adalah aplikasi manajemen keuangan pribadi berbasis Python yang dibangun menggunakan framework Streamlit. Aplikasi ini membantu Anda mencatat dan memantau arus kas (pemasukan, pengeluaran, dan investasi) dengan visualisasi data yang interaktif dan antarmuka yang modern.

## ✨ Fitur Utama

*   **📊 Dashboard Interaktif**: Ringkasan keuangan real-time dengan kartu ringkasan, diagram lingkaran (Pie Chart) per kategori, dan grafik tren pengeluaran harian.
*   **📈 Pencatatan Pemasukan**: Form input intuitif untuk mencatat berbagai sumber pendapatan.
*   **📉 Pelacakan Pengeluaran**: Monitor pengeluaran harian Anda untuk menjaga kesehatan finansial.
*   **💎 Manajemen Investasi**: Catat instrumen investasi untuk memantau pertumbuhan aset.
*   **📝 Kategori Kustom**: Kemampuan untuk menambahkan kategori baru untuk pemasukan, pengeluaran, dan investasi (disimpan dalam sesi aktif).
*   **💾 Penyimpanan Lokal**: Data tersimpan aman secara lokal dalam format CSV (`pemasukan.csv`, `pengeluaran.csv`, `investasi.csv`), sehingga mudah diakses dan dibackup.
*   **📥 Ekspor Data**: Fitur untuk mengunduh laporan keuangan (per kategori atau gabungan) dalam format CSV.
*   **🎨 UI Modern**: Tampilan antarmuka yang bersih dengan gradien warna dan desain responsif.

## 🛠️ Prasyarat

Pastikan Anda telah menginstal Python (versi 3.7 atau lebih baru). Aplikasi ini bergantung pada library Python berikut:

*   `streamlit`
*   `pandas`
*   `plotly`

## 🚀 Cara Instalasi dan Menjalankan

1.  **Siapkan Folder Proyek**
    Pastikan file `cashflow-app.py` berada di dalam folder proyek Anda.

2.  **Instal Library**
    Buka terminal atau command prompt, arahkan ke folder proyek, dan jalankan perintah berikut untuk menginstal dependensi:

    ```bash
    pip install streamlit pandas plotly
    ```

3.  **Jalankan Aplikasi**
    Jalankan aplikasi menggunakan perintah streamlit:

    ```bash
    streamlit run cashflow-app.py
    ```

4.  **Akses Aplikasi**
    Aplikasi akan otomatis terbuka di browser default Anda pada alamat `http://localhost:8501`.

## 📂 Struktur Data

Aplikasi akan secara otomatis membuat file CSV berikut saat pertama kali dijalankan atau saat data disimpan:
*   `pemasukan.csv`: Menyimpan data tanggal, kategori, jumlah, dan keterangan pemasukan.
*   `pengeluaran.csv`: Menyimpan data pengeluaran.
*   `investasi.csv`: Menyimpan data investasi.

## 💡 Catatan

*   Data kategori kustom yang ditambahkan melalui aplikasi bersifat sementara (session state) dan akan kembali ke default jika aplikasi di-restart, namun data transaksi di CSV tetap aman.
*   Untuk membackup data, cukup salin file `.csv` yang ada di folder aplikasi.
