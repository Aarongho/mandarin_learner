"""
extend_words.py — pipeline untuk memperbesar daily_words.json sampai 365 kata.

Alur kerja (gratis, tanpa API key):
  1. python extend_words.py prompt      -> cetak prompt generasi batch berikutnya
     Paste prompt itu ke LLM mana pun (Claude / Gemini / ChatGPT),
     simpan output JSON-nya ke file, misal: batch2.json
  2. python extend_words.py merge batch2.json
     -> validasi (field lengkap, hanzi tidak duplikat, pinyin bertanda nada),
        gabungkan ke daily_words.json, dan renumber id.
  Ulangi sampai total 365 kata.

Kalau nanti mau full otomatis, tinggal ganti langkah 1-2 dengan call API LLM
memakai PROMPT_TEMPLATE yang sama.
"""

import json
import sys
import unicodedata
from pathlib import Path

MAIN_FILE = Path(__file__).parent / "daily_words.json"
TARGET_TOTAL = 365
BATCH_SIZE = 40

REQUIRED_FIELDS = ["hanzi", "pinyin", "arti", "contoh", "contoh_pinyin", "contoh_arti", "hsk"]

PROMPT_TEMPLATE = """Kamu adalah penyusun materi belajar bahasa Mandarin untuk pemula Indonesia.
Buat {n} kata Mandarin BARU yang paling berguna untuk percakapan sehari-hari,
level HSK 1-3, diurutkan dari yang paling sering dipakai.

JANGAN gunakan kata yang sudah ada di daftar ini: {existing}

Format output: HANYA array JSON valid (tanpa teks lain), setiap item:
{{"hanzi": "...", "pinyin": "... (dengan tanda nada, mis. nǐ hǎo)",
  "arti": "arti dalam Bahasa Indonesia",
  "contoh": "kalimat contoh pendek memakai kata itu (hanzi)",
  "contoh_pinyin": "pinyin kalimat contoh",
  "contoh_arti": "arti kalimat contoh dalam Bahasa Indonesia",
  "hsk": 1}}

Aturan: kalimat contoh maksimal 8 karakter hanzi, pakai kosakata sederhana,
arti singkat (1-4 kata), pinyin wajib memakai tanda nada (ā á ǎ à)."""


def load_main() -> dict:
    return json.loads(MAIN_FILE.read_text(encoding="utf-8"))


def has_tone_marks(pinyin: str) -> bool:
    """Pinyin valid harus mengandung huruf bertanda nada ATAU nada netral murni."""
    toned = "āáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜ"
    # kata seperti 'xièxie' punya nada; partikel netral murni (mis. 'ma') jarang jadi entri sendiri
    return any(c in toned for c in unicodedata.normalize("NFC", pinyin))


def cmd_prompt() -> None:
    data = load_main()
    existing = "、".join(w["hanzi"] for w in data["words"])
    n = min(BATCH_SIZE, TARGET_TOTAL - len(data["words"]))
    if n <= 0:
        print(f"Sudah {len(data['words'])} kata — target {TARGET_TOTAL} tercapai 🎉")
        return
    print(PROMPT_TEMPLATE.format(n=n, existing=existing))
    print(f"\n--- (progress: {len(data['words'])}/{TARGET_TOTAL} kata) ---")


def cmd_merge(batch_path: str) -> None:
    data = load_main()
    existing_hanzi = {w["hanzi"] for w in data["words"]}
    raw = Path(batch_path).read_text(encoding="utf-8").strip()
    # toleransi kalau LLM membungkus dengan ```json ... ```
    if raw.startswith("```"):
        raw = raw.split("```")[1].removeprefix("json").strip()
    batch = json.loads(raw)

    added, skipped, errors = 0, [], []
    for item in batch:
        missing = [f for f in REQUIRED_FIELDS if f not in item or item[f] in ("", None)]
        if missing:
            errors.append(f"{item.get('hanzi', '???')}: field kurang {missing}")
            continue
        if item["hanzi"] in existing_hanzi:
            skipped.append(item["hanzi"])
            continue
        if not has_tone_marks(item["pinyin"]):
            errors.append(f"{item['hanzi']}: pinyin tanpa tanda nada -> '{item['pinyin']}'")
            continue
        item["id"] = len(data["words"]) + 1
        # pastikan urutan field konsisten
        data["words"].append({k: item[k] for k in ["id"] + REQUIRED_FIELDS})
        existing_hanzi.add(item["hanzi"])
        added += 1

    MAIN_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"✅ Ditambahkan : {added} kata")
    print(f"⏭️  Duplikat    : {len(skipped)} {skipped if skipped else ''}")
    for e in errors:
        print(f"⚠️  Ditolak     : {e}")
    print(f"📊 Total sekarang: {len(data['words'])}/{TARGET_TOTAL} kata")


if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] == "prompt":
        cmd_prompt()
    elif len(sys.argv) >= 3 and sys.argv[1] == "merge":
        cmd_merge(sys.argv[2])
    else:
        print("Pakai:  python extend_words.py prompt")
        print("        python extend_words.py merge <file_batch.json>")
