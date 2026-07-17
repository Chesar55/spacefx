"""SEO anahtar kelime bankası ve hashtag setleri.

Bu kelimeler, altın (XAUUSD) sinyal sektöründe Google'da öne çıkmak için
hedeflediğimiz aramalardır. İçerik motoru her post için ilgili kelimeleri
metne ve hashtag'lere doğal biçimde yerleştirir.
"""

# Yüksek hacimli / ana anahtar kelimeler
PRIMARY_KEYWORDS = [
    "gold signals",
    "XAUUSD signals",
    "forex gold signals",
    "gold trading signals",
    "free gold signals",
    "XAUUSD analysis",
    "gold price today",
    "buy sell gold signal",
    "gold signals telegram",
    "live gold signals",
]

# Uzun kuyruk (long-tail) - eğitim içerikleri için, rekabeti düşük
LONGTAIL_KEYWORDS = [
    "how to trade gold with signals",
    "best XAUUSD trading strategy",
    "what is XAUUSD",
    "gold support and resistance levels",
    "how to read gold signals",
    "gold trading for beginners",
    "XAUUSD scalping strategy",
    "how CPI affects gold price",
    "NFP gold trading",
    "gold vs dollar correlation",
    "risk management in gold trading",
    "gold trading session times",
]

# Ekonomik olay odaklı kelimeler
EVENT_KEYWORDS = [
    "gold NFP forecast",
    "gold CPI reaction",
    "Fed decision gold impact",
    "gold FOMC analysis",
    "XAUUSD news trading",
]

# Post tipine göre hashtag setleri (Telegram + t.me/s indexlemesi için)
HASHTAGS = {
    "core": ["#XAUUSD", "#Gold", "#GoldSignals", "#ForexSignals"],
    "analysis": ["#XAUUSD", "#GoldAnalysis", "#GoldTrading", "#Forex", "#TradingSignals"],
    "education": ["#GoldTrading", "#ForexEducation", "#TradingTips", "#XAUUSD", "#LearnForex"],
    "event": ["#XAUUSD", "#Gold", "#NFP", "#CPI", "#FOMC", "#ForexNews"],
    "cta": ["#GoldSignals", "#VIPSignals", "#XAUUSD", "#ForexSignals", "#SpaceFX"],
}


def hashtags_for(kind: str) -> str:
    tags = HASHTAGS.get(kind, HASHTAGS["core"])
    return " ".join(tags)
