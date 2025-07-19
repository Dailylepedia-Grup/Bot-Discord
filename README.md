# 🤖 BotDS - Discord Music Bot with yt-dlp & Cookies Support

**BotDS** adalah bot Discord sederhana berbasis `discord.py` yang dapat memutar musik dari YouTube menggunakan `yt-dlp`, dengan dukungan cookies browser agar bisa melewati pembatasan YouTube.

---

# 🧰 Fitur

- Join voice channel dan memutar audio dari YouTube
- Antrian lagu (queue)
- Loop lagu
- Efek audio FFMPEG per server (opsional)
- Otomatis ambil cookies dari browser (Chrome/Firefox) agar video tidak diblokir

---

# 🚀 Instalasi

# 1. Clone repositori
```
git clone https://github.com/username/BotDS.git
cd BotDS
```
# 2. Buat virtual environment (opsional tapi disarankan)
```
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

# 3. Install dependencies
```
pip install -r requirements.txt
```
# ⚙️ Konfigurasi .env
Buat file .env di direktori utama dan isi seperti ini:
```
DISCORD_TOKEN=token_discord_kamu
```
Ganti token_discord_kamu dengan token dari Discord Developer Portal.

# ▶️ Menjalankan Bot
```
python bot-ds.py
```
Bot akan login dan siap menerima perintah di server Discord kamu.

# 🧪 Contoh Perintah
!play <url> – Memutar musik dari YouTube

!skip – Melewati lagu saat ini

!stop – Menghentikan musik dan keluar dari voice

!loop – Toggle loop

!effect bass – Menambahkan efek bassboost (jika tersedia)

# 🍪 Dukungan YouTube Cookie
Jika YouTube memblokir permintaan bot (verifikasi bot/usia):

Install browser extension seperti Get cookies.txt

Ekspor cookies dari https://youtube.com

Simpan sebagai youtube_cookies.txt di direktori bot

Edit bot-ds.py:
```
YTDL_OPTIONS = {
    "cookiefile": "youtube_cookies.txt",
    ...
}
```
#🧩 Dependency

discord.py
yt-dlp
python-dotenv
browser-cookie3
PyNaCl
aiohttp
requests

# 📄 Lisensi
Proyek ini open source dan menggunakan lisensi MIT.

# ✨ Kontribusi
Pull Request dan issue sangat diterima! Jangan ragu untuk fork dan kembangkan bot ini.

---

Kalau kamu ingin aku tambahkan badge GitHub (Stars, Forks, License, dll) atau contoh gambar botnya, tinggal beri tahu. Bisa juga dibuatkan auto-deploy via Docker atau sistem service `.service` (jika ingin bot otomatis jalan di VPS).
