"""SEO anahtar kelime bankası ve hashtag setleri.

STRATEJİ (2026-07-17 güncellendi): Bu bir SEO çalışması — insanlar altın/forex
araması yaptığında kanalın Telegram/Google aramalarında öne çıkması hedeflenir.
- HABER odaklı, yüksek aramalı terimler önceliklidir (gold news, gold price today...).
- "VIP" kelimesinden KAÇINILIR: aşırı "VIP" kullanımı kanalın arama sıralamasını
  düşürüyor. Promosyon dilinde "premium/full signals" tercih edilir, hashtag'lerde
  VIP hiç kullanılmaz.
"""

# Yüksek hacimli / ana anahtar kelimeler (haber + fiyat odaklı, VIP yok)
PRIMARY_KEYWORDS = [
    "gold news",
    "gold price today",
    "gold price forecast",   # sadece "piyasanın sorusu" olarak; kendi tahminimiz değil
    "XAUUSD analysis",
    "gold market news",
    "gold signals",
    "XAUUSD signals",
    "live gold price",
    "gold market today",
    "gold price update",
    "gold price live",
    "gold trading signals",
]

# Haber içerikleri için (haber analizi postlarında öne çıkar)
NEWS_KEYWORDS = [
    "gold news today",
    "gold market update",
    "XAUUSD news",
    "gold price analysis",
    "gold price live",
    "why is gold falling",
    "what is moving gold price",
    "gold market analysis today",
]

# Uzun kuyruk (long-tail) - eğitim/haber içerikleri için, rekabeti düşük
LONGTAIL_KEYWORDS = [
    "why is gold falling today",
    "what is moving the gold price",
    "will gold break 4000",
    "gold price after Fed decision",
    "how CPI affects gold price",
    "gold safe haven demand",
    "gold vs dollar today",
    "how to read gold news",
    "gold support and resistance levels",
    "best XAUUSD trading strategy",
    "gold trading for beginners",
    "risk management in gold trading",
]

# Ekonomik olay odaklı kelimeler
EVENT_KEYWORDS = [
    "gold NFP reaction",
    "gold CPI reaction",
    "Fed decision gold impact",
    "gold FOMC analysis",
    "XAUUSD news trading",
]

# Post tipine göre hashtag setleri — SEO odaklı, aranabilir terimler; VIP YOK.
HASHTAGS = {
    "core": ["#XAUUSD", "#Gold", "#GoldSignals", "#GoldNews"],
    "analysis": ["#XAUUSD", "#GoldPrice", "#GoldAnalysis", "#GoldForecast", "#GoldNews"],
    "education": ["#GoldTrading", "#XAUUSD", "#GoldMarket", "#TradingTips"],
    "event": ["#XAUUSD", "#GoldNews", "#CPI", "#FOMC", "#Gold"],
    "news": ["#XAUUSD", "#GoldNews", "#GoldPrice", "#GoldForecast", "#Gold"],
    "cta": ["#GoldSignals", "#XAUUSD", "#GoldNews", "#GoldPrice", "#GoldTrading"],
}


def hashtags_for(kind: str) -> str:
    tags = HASHTAGS.get(kind, HASHTAGS["core"])
    return " ".join(tags)
