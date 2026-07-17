"""Canlı altın (XAUUSD) fiyat + teknik gösterge verisi.

Yahoo Finance'ten günlük geçmişi çeker ve GERÇEK teknik göstergeleri hesaplar
(20 günlük yüksek/düşük, MA50, MA200, RSI-14, günlük yüksek/düşük). Bu sayede
içerik motoru destek/direnç seviyelerini uydurmadan, gerçek veriye dayandırır.
Kaynak çalışmazsa spot fiyata (gold-api.com) düşer; o da olmazsa None döner.
"""
import datetime as dt
import xml.etree.ElementTree as ET

import requests

_HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; SpaceFXBot/1.0)"}
_TIMEOUT = 12


# ------------------------------------------------------------------
# Teknik gösterge hesapları (saf Python — ek bağımlılık yok)
# ------------------------------------------------------------------
def _sma(values, period):
    if len(values) < period:
        return None
    return round(sum(values[-period:]) / period, 2)


def _rsi(closes, period=14):
    """Wilder RSI-14. Yeterli veri yoksa None."""
    if len(closes) < period + 1:
        return None
    gains, losses = [], []
    for i in range(1, len(closes)):
        diff = closes[i] - closes[i - 1]
        gains.append(max(diff, 0.0))
        losses.append(max(-diff, 0.0))
    avg_gain = sum(gains[:period]) / period
    avg_loss = sum(losses[:period]) / period
    for i in range(period, len(gains)):
        avg_gain = (avg_gain * (period - 1) + gains[i]) / period
        avg_loss = (avg_loss * (period - 1) + losses[i]) / period
    if avg_loss == 0:
        return 100.0
    rs = avg_gain / avg_loss
    return round(100 - (100 / (1 + rs)), 1)


def _from_yahoo():
    """Yahoo Finance chart endpoint — fiyat + günlük geçmiş + teknikler."""
    url = "https://query1.finance.yahoo.com/v8/finance/chart/GC=F"
    r = requests.get(url, params={"interval": "1d", "range": "1y"},
                     headers=_HEADERS, timeout=_TIMEOUT)
    r.raise_for_status()
    result = r.json()["chart"]["result"][0]
    meta = result["meta"]
    price = meta.get("regularMarketPrice")
    if not price:
        return None

    quote = result.get("indicators", {}).get("quote", [{}])[0]
    timestamps = result.get("timestamp") or []
    # None mumları at (tarih hizasını koruyarak)
    rows = [(t, c, h, l) for t, c, h, l in zip(
                timestamps, quote.get("close") or [], quote.get("high") or [],
                quote.get("low") or [])
            if c is not None]
    closes = [c for _, c, _, _ in rows]
    highs = [h for _, _, h, _ in rows if h is not None]
    lows = [l for _, _, _, l in rows if l is not None]

    # Günlük değişim için ÖNCEKİ GÜN kapanışı gerekir. range=1y iken meta'nın
    # chartPreviousClose'u 1 yıl öncesini verir. Son mum BUGÜN oluşan mumsa
    # (canlı), önceki gün = closes[-2]; değilse son tamamlanan = closes[-1].
    prev = None
    if len(closes) >= 2:
        last_date = dt.datetime.fromtimestamp(rows[-1][0], dt.timezone.utc).date()
        prev = closes[-2] if last_date == dt.datetime.now(dt.timezone.utc).date() else closes[-1]
    if prev is None:
        prev = meta.get("previousClose") or meta.get("chartPreviousClose")

    change = round(price - prev, 2) if prev else None
    change_pct = round((change / prev) * 100, 2) if (prev and change is not None) else None

    day_high = meta.get("regularMarketDayHigh") or (highs[-1] if highs else None)
    day_low = meta.get("regularMarketDayLow") or (lows[-1] if lows else None)

    tech = {
        "day_high": round(day_high, 2) if day_high else None,
        "day_low": round(day_low, 2) if day_low else None,
        "high_20d": round(max(highs[-20:]), 2) if len(highs) >= 5 else None,
        "low_20d": round(min(lows[-20:]), 2) if len(lows) >= 5 else None,
        "ma50": _sma(closes, 50),
        "ma200": _sma(closes, 200),
        "rsi14": _rsi(closes, 14),
    }
    return {"price": round(price, 2), "prev_close": prev,
            "change": change, "change_pct": change_pct,
            "tech": tech,
            "source": "Yahoo Finance (GC=F futures)"}


def _from_goldapi():
    """gold-api.com — anahtarsız spot altın fiyatı (teknik vermez, yedek)."""
    r = requests.get("https://api.gold-api.com/price/XAU",
                     headers=_HEADERS, timeout=_TIMEOUT)
    r.raise_for_status()
    data = r.json()
    price = data.get("price")
    if not price:
        return None
    return {"price": round(price, 2), "prev_close": None,
            "change": None, "change_pct": None, "tech": {},
            "source": "gold-api.com (spot XAU/USD)"}


def get_gold_news(query="gold price XAUUSD", limit=5):
    """Güncel altın haber başlıklarını Google News RSS'ten çeker (anahtarsız, ücretsiz).

    Gerçek, tarihli, kaynaklı başlıklar döndürür; hata olursa boş liste.
    """
    try:
        r = requests.get(
            "https://news.google.com/rss/search",
            params={"q": query, "hl": "en-US", "gl": "US", "ceid": "US:en"},
            headers=_HEADERS, timeout=_TIMEOUT)
        r.raise_for_status()
        root = ET.fromstring(r.content)
        news = []
        for item in root.findall(".//item")[: limit * 2]:
            title = (item.findtext("title") or "").strip()
            source = (item.findtext("source") or "").strip()
            # Google News başlığı "Manşet - Kaynak" biçiminde; kaynağı manşetten ayıkla
            if source and title.endswith(f" - {source}"):
                title = title[: -(len(source) + 3)].strip()
            pub = (item.findtext("pubDate") or "").strip()
            if title:
                news.append({"title": title, "source": source, "published": pub})
            if len(news) >= limit:
                break
        return news
    except Exception as e:  # noqa: BLE001
        print(f"[news] Haber alınamadı: {e}")
        return []


def get_driver_news(limit=6):
    """Altını hareket ettiren ANA sürücüleri yakalamak için birden çok sorguyu
    birleştirir (fiyat + Fed/enflasyon + jeopolitik). Tekrarları eler.
    """
    seen, out = set(), []
    for q in ("gold price XAUUSD",
              "gold Fed rate inflation",
              "gold safe haven geopolitical"):
        for n in get_gold_news(q, 4):
            key = n["title"].lower()[:60]
            if key in seen:
                continue
            seen.add(key)
            out.append(n)
            if len(out) >= limit:
                return out
    return out


# Altını güçlü etkileyen yüksek-etkili haber anahtarları (breaking tespiti için)
_HIGH_IMPACT = (
    "fed", "rate cut", "rate hike", "fomc", "cpi", "inflation", "nfp",
    "payroll", "war", "middle east", "geopolit", "record high", "record-high",
    "all-time high", "crash", "plunge", "surge", "soars", "tumbles",
    "biggest weekly", "safe haven", "recession", "tariff", "yields",
)


def high_impact_headline(news):
    """Haber listesinde yüksek-etkili bir manşet varsa onu döndürür, yoksa None.
    breaking_news tipini otomatik tetiklemek için kullanılır.
    """
    for n in news or []:
        t = n.get("title", "").lower()
        if any(k in t for k in _HIGH_IMPACT):
            return n
    return None


def format_news_snapshot(news) -> str:
    """Haber başlıklarını prompt'a gömmek için biçimlendirir."""
    if not news:
        return "No recent headlines available — do not reference specific news."
    lines = ["Recent REAL gold-market headlines (context — reference the current "
             "narrative but do NOT invent facts beyond these):"]
    for n in news:
        src = f" ({n['source']})" if n.get("source") else ""
        lines.append(f"- {n['title']}{src}")
    return "\n".join(lines)


def get_gold_data():
    """Altın verisini döndürür; hepsi başarısızsa None."""
    for fetcher in (_from_yahoo, _from_goldapi):
        try:
            data = fetcher()
            if data and data.get("price"):
                return data
        except Exception as e:  # noqa: BLE001
            print(f"[data] {fetcher.__name__} başarısız: {e}")
    print("[data] Canlı fiyat alınamadı; fiyatsız içerik üretilecek.")
    return None


def format_market_snapshot(data) -> str:
    """Prompt'a gömmek için insan-okunur özet (gerçek teknik seviyelerle)."""
    if not data:
        return "Live price unavailable — write a general, non-numeric outlook."
    lines = [f"Current XAU/USD price: ${data['price']}"]
    if data.get("change") is not None:
        arrow = "up" if data["change"] >= 0 else "down"
        lines.append(f"Daily change: {arrow} {abs(data['change'])} USD "
                     f"({data['change_pct']:+.2f}%)")

    t = data.get("tech") or {}
    if t.get("day_high") and t.get("day_low"):
        lines.append(f"Today's range: {t['day_low']} - {t['day_high']}")
    if t.get("low_20d") and t.get("high_20d"):
        lines.append(f"20-day range (real support/resistance anchors): "
                     f"{t['low_20d']} (support) - {t['high_20d']} (resistance)")
    if t.get("ma50"):
        rel = "above" if data["price"] >= t["ma50"] else "below"
        lines.append(f"50-day moving average: {t['ma50']} (price is {rel} it)")
    if t.get("ma200"):
        rel = "above" if data["price"] >= t["ma200"] else "below"
        lines.append(f"200-day moving average: {t['ma200']} (price is {rel} it)")
    if t.get("rsi14") is not None:
        r = t["rsi14"]
        state = "overbought" if r >= 70 else "oversold" if r <= 30 else "neutral"
        lines.append(f"RSI(14): {r} ({state})")

    lines.append(f"Data source: {data['source']}")
    lines.append("NOTE: Build your support/resistance zones around these REAL "
                 "numbers (20-day range, moving averages, today's range) — do not "
                 "invent unrelated levels.")
    return "\n".join(lines)


if __name__ == "__main__":
    d = get_gold_data()
    print(format_market_snapshot(d))
