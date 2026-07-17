"""Tüm içerik tiplerinden birer örnek üretir (atmadan). Test/önizleme için."""
import sys
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:  # noqa: BLE001
        pass

import random
import content_engine
import keywords
from data_sources import get_gold_data

gold = get_gold_data()
order = [
    "market_open_brief", "key_levels", "economic_event_watch",
    "educational", "midday_update", "weekly_recap",
    "weekend_outlook", "vip_soft_cta",
]
for pt in order:
    extra = None
    if pt == "educational":
        extra = random.sample(keywords.LONGTAIL_KEYWORDS, 2)
    text = content_engine.generate(pt, gold_data=gold, extra_keywords=extra)
    print("\n" + "#" * 64)
    print(f"# ORNEK ICERIK TIPI:  {pt}")
    print("#" * 64 + "\n")
    print(text)
