// Variables used by Scriptable.
// These must be at the very top of the file. Do not edit.
// icon-color: red; icon-glyph: language;

// ====== Kata Harian Mandarin — Scriptable Widget ======
// 1. Install app "Scriptable" (gratis) dari App Store
// 2. Buat script baru, paste kode ini
// 3. GANTI DATA_URL di bawah dengan URL JSON kamu (GitHub Pages / HF)
// 4. Long-press home screen → tambah widget Scriptable → pilih script ini
//    (ukuran Small atau Medium dua-duanya didukung)

const DATA_URL = "https://aarongho.github.io/mandarin_learner/daily_words.json";

// ---------- Ambil data (dengan cache offline) ----------
const fm = FileManager.local();
const cachePath = fm.joinPath(fm.cacheDirectory(), "daily_words_cache.json");

async function loadData() {
  try {
    const req = new Request(DATA_URL);
    req.timeoutInterval = 10;
    const data = await req.loadJSON();
    fm.writeString(cachePath, JSON.stringify(data)); // simpan cache
    return data;
  } catch (e) {
    // offline → pakai cache terakhir
    if (fm.fileExists(cachePath)) {
      return JSON.parse(fm.readString(cachePath));
    }
    throw e;
  }
}

// ---------- Pilih kata berdasarkan tanggal ----------
function todayWord(data) {
  const start = new Date(data.start_date + "T00:00:00");
  const now = new Date();
  const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
  const dayIndex = Math.max(0, Math.round((today - start) / 86400000));
  const words = data.words;
  return { word: words[dayIndex % words.length], dayNumber: dayIndex + 1 };
}

// ---------- Bangun tampilan widget ----------
function buildWidget(word, dayNumber, appUrl) {
  const w = new ListWidget();
  w.backgroundGradient = makeGradient();
  w.url = appUrl; // tap widget → buka web app kamu
  const isSmall = config.widgetFamily === "small";
  w.setPadding(14, 14, 14, 14);

  // Header
  const header = w.addText("📅 Kata Hari ke-" + dayNumber);
  header.font = Font.mediumSystemFont(isSmall ? 9 : 11);
  header.textColor = new Color("#ffffff", 0.75);
  w.addSpacer(isSmall ? 4 : 6);

  // Hanzi besar
  const hanzi = w.addText(word.hanzi);
  hanzi.font = Font.boldSystemFont(isSmall ? 34 : 42);
  hanzi.textColor = Color.white();
  hanzi.minimumScaleFactor = 0.5;
  hanzi.lineLimit = 1;
  w.addSpacer(2);

  // Pinyin + arti
  const pinyin = w.addText(word.pinyin);
  pinyin.font = Font.mediumSystemFont(isSmall ? 13 : 16);
  pinyin.textColor = new Color("#FFD166");
  const arti = w.addText(word.arti);
  arti.font = Font.regularSystemFont(isSmall ? 11 : 13);
  arti.textColor = new Color("#ffffff", 0.9);
  arti.lineLimit = 1;
  arti.minimumScaleFactor = 0.7;

  // Contoh kalimat (hanya di widget Medium ke atas)
  if (!isSmall && word.contoh) {
    w.addSpacer(6);
    const contoh = w.addText(word.contoh + "  ·  " + word.contoh_arti);
    contoh.font = Font.regularSystemFont(10);
    contoh.textColor = new Color("#ffffff", 0.65);
    contoh.lineLimit = 2;
    contoh.minimumScaleFactor = 0.8;
  }

  // Minta iOS refresh widget setelah lewat tengah malam
  const midnight = new Date();
  midnight.setHours(24, 0, 5, 0);
  w.refreshAfterDate = midnight;
  return w;
}

function makeGradient() {
  const g = new LinearGradient();
  g.colors = [new Color("#B3001B"), new Color("#6A040F")]; // merah khas Tiongkok
  g.locations = [0, 1];
  return g;
}

// ---------- Main ----------
let widget;
try {
  const data = await loadData();
  const { word, dayNumber } = todayWord(data);
  widget = buildWidget(word, dayNumber, data.app_url);
} catch (e) {
  widget = new ListWidget();
  const t = widget.addText("⚠️ Gagal memuat data.\nCek DATA_URL & koneksi.");
  t.font = Font.systemFont(12);
}

if (config.runsInWidget) {
  Script.setWidget(widget);
} else {
  await widget.presentMedium(); // preview saat dijalankan manual di app
}
Script.complete();
