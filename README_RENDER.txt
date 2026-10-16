DEPLOY KE RENDER (RINGKAS)

1. Ekstrak ZIP.
2. Buat repository baru di GitHub, misalnya kantin-bersih-unpam.
3. Upload semua ISI folder kantin_bersih_unpam ke repository (app.py, requirements.txt, render.yaml, folder static, templates, uploads, dll). Jangan upload file ZIP-nya saja.
4. Di Render pilih New + > Web Service, hubungkan GitHub dan pilih repository tadi.
5. Jika konfigurasi render.yaml terbaca, cek runtime Python, Build Command: pip install -r requirements.txt, Start Command: gunicorn app:app, plan Free.
6. Tambahkan Environment Variables: FLASK_SECRET_KEY = string acak panjang; ADMIN_USERNAME = nama admin pilihan; ADMIN_PASSWORD = password admin yang kuat dan unik. Jangan pakai kredensial contoh.
7. Klik Deploy Web Service. Setelah status Live, buka URL .onrender.com.

PENTING: Ini konfigurasi demo. Render free memakai filesystem sementara; database SQLite dan foto yang diunggah dapat hilang saat restart/redeploy. Jangan gunakan untuk laporan penting sebelum database/file upload dipindahkan ke penyimpanan persisten. File .db dan uploads tidak boleh dianggap persisten pada paket gratis.
