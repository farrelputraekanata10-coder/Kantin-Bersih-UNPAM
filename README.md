# Kantin Bersih UNPAM

Website responsif untuk pelaporan sampah di area kantin dekat Gedung Teknik Elektro Universitas Pamulang.

## Fitur
- Form laporan dengan nama, lokasi, jenis masalah, deskripsi, dan foto opsional.
- Penyimpanan laporan menggunakan SQLite (data tetap tersimpan setelah server dimatikan).
- Daftar laporan publik dan filter status.
- Dashboard admin untuk mengubah status menjadi Menunggu, Diproses, atau Selesai, serta menghapus laporan.
- Tampilan responsif untuk laptop dan ponsel.
- Upload foto maksimal 5 MB dengan format PNG, JPG, JPEG, WEBP.

## Cara menjalankan di Windows
1. Pastikan Python 3.10 atau lebih baru sudah terpasang. Saat instalasi Python, centang **Add Python to PATH**.
2. Ekstrak file ZIP ini.
3. Buka folder `kantin_bersih_unpam`.
4. Buka CMD/Terminal di folder tersebut.
5. Jalankan:
   ```bash
   py -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   py app.py
   ```
6. Buka browser ke `http://127.0.0.1:5000`.

Jika perintah `py` tidak dikenali, coba `python` sebagai pengganti `py`.

## Login admin awal
- Username: `admin`
- Password: `unpam123`

Login ini hanya untuk demo lokal. Ganti password sebelum dipakai pada jaringan publik.

## Mengubah password admin
Atur environment variable sebelum menjalankan aplikasi di Windows CMD:
```bat
set ADMIN_USERNAME=adminbaru
set ADMIN_PASSWORD=password-yang-kuat
set FLASK_SECRET_KEY=isi-dengan-random-string-panjang
py app.py
```
Variabel tersebut berlaku untuk jendela CMD yang sedang digunakan.

## Catatan penting
- Website ini berjalan lokal di laptop. Agar dapat diakses mahasiswa lain melalui internet, aplikasi perlu di-deploy ke layanan hosting dan konfigurasi keamanan perlu diperkuat.
- Jangan gunakan server debug Flask untuk deployment publik.
- Database `kantin_bersih.db` dan foto di folder `uploads` akan dibuat otomatis.
- Ini adalah prototipe fungsional untuk tugas/proyek kampus, bukan layanan resmi Universitas Pamulang.
