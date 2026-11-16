# 一天一词 · Kata Harian Mandarin

Aplikasi belajar bahasa Mandarin untuk pemula Indonesia — satu kata baru setiap hari di home screen iPhone, lengkap dengan flashcards dan kuis.

**Live app:** https://aarongho.github.io/mandarin_learner/

## Fitur

- 📅 **Kata harian** — 5.000 kata HSK 1–6 (pinyin + arti Bahasa Indonesia), diurutkan dari yang paling berguna; cukup untuk ±13 tahun tanpa pengulangan
- 📱 **Widget iPhone** — via [Scriptable](https://scriptable.app), menampilkan kata hari ini dan auto-refresh tiap tengah malam; tap widget → buka app
- 🎴 **Flashcards** — belajar per batch 10 kata dengan kartu flip (hanzi → pinyin + arti) dan audio pelafalan (TTS zh-CN)
- ✍️ **Kuis pilihan ganda** — otomatis setiap 10 kata, campuran soal hanzi→arti dan arti→hanzi dengan pengecoh dari level HSK berdekatan
- 🔁 **Review** — kata yang salah di kuis masuk daftar review sampai dijawab benar
- 📊 **Progres** — streak harian, akurasi kuis, dan progress bar per level HSK, tersimpan di localStorage

## Cara Pakai

### App (PWA)
1. Buka https://aarongho.github.io/mandarin_learner/ di Safari iPhone
2. Share → **Add to Home Screen** → app tampil fullscreen seperti app native

### Widget
1. Install app **Scriptable** (gratis) dari App Store
2. Buat script baru, paste isi [`kata-harian-widget.js`](kata-harian-widget.js)
3. Long-press home screen → tambah widget **Scriptable** (Small/Medium) → pilih script-nya

## Data & Pipeline

- Wordlist: [clem109/hsk-vocabulary](https://github.com/clem109/hsk-vocabulary) (HSK 1–6), diterjemahkan ke Bahasa Indonesia dengan bantuan LLM lalu divalidasi (dedupe, tanda nada pinyin, polifon seperti 长 *cháng/zhǎng* dipertahankan terpisah)
- [`daily_words.json`](daily_words.json) — satu sumber data untuk widget **dan** app
- [`extend_words.py`](extend_words.py) — pipeline untuk menambah kata / contoh kalimat per batch dengan validasi otomatis

## Tech

Vanilla HTML/CSS/JS (tanpa framework, tanpa build step) · Scriptable (JavaScript widget iOS) · Python (data pipeline) · GitHub Pages

---
Dibuat oleh [Aaron Winston Gho](https://aarongho.github.io/Portofolio/page3.html)
