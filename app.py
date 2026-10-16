import os
import sqlite3
from datetime import datetime
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, flash, session, abort
from werkzeug.utils import secure_filename

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "kantin_bersih.db")
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}
MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5 MB

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "ganti-secret-key-ini-sebelum-deploy")
app.config["UPLOAD_FOLDER"] = UPLOAD_DIR
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH

# Ganti nilai ini sebelum aplikasi dipakai secara publik.
ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "unpam123")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                location TEXT NOT NULL,
                category TEXT NOT NULL,
                description TEXT NOT NULL,
                photo TEXT,
                status TEXT NOT NULL DEFAULT 'Menunggu',
                created_at TEXT NOT NULL
            )
        """)
        conn.commit()


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def admin_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("is_admin"):
            return redirect(url_for("admin_login"))
        return view(*args, **kwargs)
    return wrapped


@app.route("/")
def index():
    conn = get_db()
    total = conn.execute("SELECT COUNT(*) FROM reports").fetchone()[0]
    pending = conn.execute("SELECT COUNT(*) FROM reports WHERE status = 'Menunggu'").fetchone()[0]
    handled = conn.execute("SELECT COUNT(*) FROM reports WHERE status = 'Selesai'").fetchone()[0]
    recent = conn.execute(
        "SELECT * FROM reports ORDER BY id DESC LIMIT 5"
    ).fetchall()
    conn.close()
    return render_template("index.html", total=total, pending=pending, handled=handled, recent=recent)


@app.route("/lapor", methods=["GET", "POST"])
def report():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        location = request.form.get("location", "").strip()
        category = request.form.get("category", "").strip()
        description = request.form.get("description", "").strip()
        photo_name = None

        if not all([name, location, category, description]):
            flash("Semua kolom wajib diisi kecuali foto.", "error")
            return render_template("report.html", form=request.form)

        if len(name) > 80 or len(description) > 1000:
            flash("Nama maksimal 80 karakter dan deskripsi maksimal 1.000 karakter.", "error")
            return render_template("report.html", form=request.form)

        photo = request.files.get("photo")
        if photo and photo.filename:
            if not allowed_file(photo.filename):
                flash("Format foto harus PNG, JPG, JPEG, atau WEBP.", "error")
                return render_template("report.html", form=request.form)
            safe_name = secure_filename(photo.filename)
            stamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
            photo_name = f"{stamp}_{safe_name}"
            photo.save(os.path.join(UPLOAD_DIR, photo_name))

        conn = get_db()
        conn.execute("""
            INSERT INTO reports (name, location, category, description, photo, status, created_at)
            VALUES (?, ?, ?, ?, ?, 'Menunggu', ?)
        """, (name, location, category, description, photo_name,
              datetime.now().strftime("%d-%m-%Y %H:%M")))
        conn.commit()
        conn.close()
        flash("Laporan berhasil dikirim. Terima kasih sudah menjaga kebersihan kantin!", "success")
        return redirect(url_for("index"))

    return render_template("report.html", form={})


@app.route("/laporan")
def reports():
    status = request.args.get("status", "").strip()
    conn = get_db()
    if status in ("Menunggu", "Diproses", "Selesai"):
        rows = conn.execute(
            "SELECT * FROM reports WHERE status = ? ORDER BY id DESC", (status,)
        ).fetchall()
    else:
        rows = conn.execute("SELECT * FROM reports ORDER BY id DESC").fetchall()
    conn.close()
    return render_template("reports.html", reports=rows, selected_status=status)


@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if session.get("is_admin"):
        return redirect(url_for("admin_dashboard"))
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["is_admin"] = True
            flash("Berhasil masuk ke dashboard admin.", "success")
            return redirect(url_for("admin_dashboard"))
        flash("Username atau password salah.", "error")
    return render_template("admin_login.html")


@app.route("/admin")
@admin_required
def admin_dashboard():
    conn = get_db()
    rows = conn.execute("SELECT * FROM reports ORDER BY id DESC").fetchall()
    conn.close()
    return render_template("admin.html", reports=rows)


@app.route("/admin/status/<int:report_id>", methods=["POST"])
@admin_required
def update_status(report_id):
    status = request.form.get("status", "")
    if status not in ("Menunggu", "Diproses", "Selesai"):
        abort(400)
    conn = get_db()
    conn.execute("UPDATE reports SET status = ? WHERE id = ?", (status, report_id))
    conn.commit()
    conn.close()
    flash(f"Status laporan #{report_id} diperbarui.", "success")
    return redirect(url_for("admin_dashboard"))


@app.route("/admin/hapus/<int:report_id>", methods=["POST"])
@admin_required
def delete_report(report_id):
    conn = get_db()
    row = conn.execute("SELECT photo FROM reports WHERE id = ?", (report_id,)).fetchone()
    if row:
        if row["photo"]:
            path = os.path.join(UPLOAD_DIR, row["photo"])
            if os.path.isfile(path):
                os.remove(path)
        conn.execute("DELETE FROM reports WHERE id = ?", (report_id,))
        conn.commit()
    conn.close()
    flash(f"Laporan #{report_id} dihapus.", "success")
    return redirect(url_for("admin_dashboard"))


@app.route("/uploads/<path:filename>")
def uploaded_file(filename):
    # Only serve files stored in the upload folder.
    from flask import send_from_directory
    return send_from_directory(UPLOAD_DIR, filename)


@app.route("/admin/logout")
def admin_logout():
    session.clear()
    flash("Anda sudah keluar dari dashboard admin.", "success")
    return redirect(url_for("index"))


@app.errorhandler(413)
def too_large(_error):
    flash("Ukuran foto terlalu besar. Maksimal 5 MB.", "error")
    return redirect(url_for("report"))


init_db()

if __name__ == "__main__":
    app.run(debug=True)
