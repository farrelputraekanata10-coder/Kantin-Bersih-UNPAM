KANTIN BERSIH UNPAM — VERSI DEMO GITHUB PAGES

CARA MEMASANG DI REPOSITORY YANG SUDAH ADA
1. Ekstrak ZIP ini di komputer.
2. Buka repository GitHub Kantin-Bersih-UNPAM.
3. Klik Add file > Upload files.
4. Upload file index.html, style.css, script.js, dan README_GITHUB_PAGES.txt (serta .nojekyll bila terlihat).
5. Klik Commit changes.
6. Buka repository Settings > Pages.
7. Pada Build and deployment, pilih Deploy from a branch.
8. Branch: main; folder: /(root). Klik Save.
9. Tunggu beberapa menit, lalu lihat bagian Pages untuk URL publik.

PENTING
- Ini versi website statis untuk GitHub Pages.
- Form laporan hanya menyimpan data di localStorage browser yang digunakan. Laporan tidak dikirim ke server, tidak terlihat oleh pengguna lain, dan tidak masuk ke admin.
- Fitur login admin, database, upload foto, dan daftar laporan bersama dari versi Flask tidak tersedia di versi statis ini.
- Untuk sistem laporan publik yang benar-benar menyimpan laporan untuk pengelola, perlu backend/database online terpisah.
- Jangan unggah password atau SECRET_KEY ke repository publik.
