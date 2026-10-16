@echo off
chcp 65001 >nul
cd /d "%~dp0"
title Kantin Bersih UNPAM

echo ==========================================
echo       KANTIN BERSIH UNPAM
echo ==========================================
echo.

where py >nul 2>nul
if errorlevel 1 (
  echo Python belum terdeteksi di laptop ini.
  echo Install Python dari https://www.python.org/downloads/
  echo Saat instalasi, centang pilihan "Add Python to PATH".
  echo Setelah selesai, buka file ini lagi.
  echo.
  pause
  exit /b 1
)

if not exist ".venv\Scripts\python.exe" (
  echo [1/3] Menyiapkan Python environment...
  py -m venv .venv
  if errorlevel 1 goto error
)

echo [2/3] Memasang kebutuhan website (pertama kali mungkin perlu internet)...
".venv\Scripts\python.exe" -m pip install --disable-pip-version-check -r requirements.txt
if errorlevel 1 goto error

echo.
echo [3/3] Menjalankan website...
echo Biarkan jendela hitam ini tetap terbuka selama website digunakan.
start "" http://127.0.0.1:5000
".venv\Scripts\python.exe" app.py
if errorlevel 1 goto error
pause
exit /b 0

:error
echo.
echo Ada error. Foto/salin tulisan di jendela ini lalu kirim ke ChatGPT.
echo.
pause
exit /b 1
