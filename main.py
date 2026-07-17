"""Otonom içerik orkestratörü.

Kullanım:
  python main.py --slot morning        # o günün 'morning' içeriğini üret+at
  python main.py --slot midday
  python main.py --slot evening
  python main.py auto                   # şu anki saate en yakın slotu seç
  python main.py --type educational     # belirli tipi zorla (test)
  python main.py --slot morning --dry   # atmadan sadece göster

VPS'te cron her slot için ilgili saatte 'python main.py --slot <slot>' çağırır.
"""
import argparse
import datetime as dt
import json
import os
import random
import sys

# Windows konsolunda emoji/Türkçe karakter yazdırabilmek için UTF-8'e geç
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8")
    except Exception:  # noqa: BLE001
        pass

import config
import content_engine
import keywords
from data_sources import get_gold_data

HISTORY_FILE = os.path.join(os.path.dirname(__file__), "posted_history.json")
LOG_FILE = os.path.join(os.path.dirname(__file__), "run.log")


def _log(msg: str):
    line = f"{dt.datetime.now().isoformat(timespec='seconds')} | {msg}"
    print(line)
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:  # noqa: BLE001
        pass


def _load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, encoding="utf-8") as f:
                return json.load(f)
        except Exception:  # noqa: BLE001
            return []
    return []


def _save_history(entries):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(entries[-500:], f, ensure_ascii=False, indent=2)


def _already_posted_today(slot: str, post_type: str) -> bool:
    today = dt.date.today().isoformat()
    for e in _load_history():
        if e.get("date") == today and e.get("slot") == slot and e.get("type") == post_type:
            return True
    return False


def _auto_slot() -> str:
    """Şu anki saate en yakın slotu döndürür."""
    hour = dt.datetime.now().hour
    best, best_diff = "morning", 99
    for slot, h in config.SLOT_HOURS.items():
        diff = abs(hour - h)
        if diff < best_diff:
            best, best_diff = slot, diff
    return best


def run(slot=None, forced_type=None, dry=False):
    weekday = dt.datetime.now().weekday()

    if forced_type:
        post_type = forced_type
        slot = slot or "manual"
    else:
        if slot in (None, "auto"):
            slot = _auto_slot()
        post_type = config.resolve_post_type(weekday, slot)
        if not post_type:
            _log(f"Bugün ({weekday}) '{slot}' slotu için planlanmış içerik yok. Çıkılıyor.")
            return

    if not forced_type and _already_posted_today(slot, post_type):
        _log(f"Bugün '{slot}/{post_type}' zaten atılmış. Tekrar atılmıyor.")
        return

    _log(f"İçerik üretiliyor: slot={slot} type={post_type} lang={config.CONTENT_LANG}")

    # Eğitim içerikleri için longtail anahtar kelimeyi rotasyonla seç (çeşitlilik)
    extra_kw = None
    if post_type == "educational":
        extra_kw = random.sample(keywords.LONGTAIL_KEYWORDS,
                                 k=min(2, len(keywords.LONGTAIL_KEYWORDS)))

    gold = get_gold_data()
    text = content_engine.generate(post_type, gold_data=gold, extra_keywords=extra_kw)

    print("\n" + "=" * 60 + "\n" + text + "\n" + "=" * 60 + "\n")

    if dry or config.DRY_RUN:
        _log("DRY_RUN aktif — mesaj atılmadı.")
        return

    import poster
    poster.send(text)
    _log(f"✅ Gönderildi: {slot}/{post_type}")

    hist = _load_history()
    hist.append({
        "date": dt.date.today().isoformat(),
        "time": dt.datetime.now().strftime("%H:%M"),
        "slot": slot,
        "type": post_type,
        "preview": text[:120],
    })
    _save_history(hist)


def parse_args():
    p = argparse.ArgumentParser(description="SpaceFX Telegram otonom içerik sistemi")
    p.add_argument("mode", nargs="?", default=None, help="'auto' veya boş bırakın")
    p.add_argument("--slot", choices=["night", "morning", "midday", "evening", "auto"],
                   help="Yayın slotu")
    p.add_argument("--type", dest="forced_type", help="Belirli içerik tipini zorla")
    p.add_argument("--dry", action="store_true", help="Atmadan sadece göster")
    return p.parse_args()


if __name__ == "__main__":
    args = parse_args()
    slot = args.slot or (args.mode if args.mode in ("auto",) else None)
    run(slot=slot, forced_type=args.forced_type, dry=args.dry)
