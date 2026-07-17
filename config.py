"""Merkezi yapılandırma: .env okunur, yayın takvimi ve slot planı tanımlanır."""
import os
from dotenv import load_dotenv

load_dotenv()

# --- Anthropic ---
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
CLAUDE_MODEL = os.getenv("CLAUDE_MODEL", "claude-opus-4-8")
CLAUDE_EFFORT = os.getenv("CLAUDE_EFFORT", "medium")

# --- Telegram ---
TELEGRAM_API_ID = int(os.getenv("TELEGRAM_API_ID", "0") or 0)
TELEGRAM_API_HASH = os.getenv("TELEGRAM_API_HASH", "")
TELEGRAM_SESSION_STRING = os.getenv("TELEGRAM_SESSION_STRING", "")
TELEGRAM_CHANNEL = os.getenv("TELEGRAM_CHANNEL", "XAUUSD_GoldSignalsVIP")

# --- Tanıtım linkleri (mesaj sonundaki CTA footer'da kullanılır) ---
# VIP_LINK: VIP alım/başvuru botu.  FREE_CHANNEL_LINK: büyütülmek istenen free kanal.
VIP_LINK = os.getenv("VIP_LINK", "https://t.me/m/2D9IxBhyZGNk")
FREE_CHANNEL_LINK = os.getenv("FREE_CHANNEL_LINK", "https://t.me/FxSpaceGlobal")

# --- Genel ---
CONTENT_LANG = os.getenv("CONTENT_LANG", "en").lower()
DRY_RUN = os.getenv("DRY_RUN", "false").lower() in ("1", "true", "yes")

# Büyük/yüksek-etkili bir altın haberi tespit edilirse o günün bir haber slotunu
# otomatik olarak 'breaking_news' (haber + kanala davet CTA) tipine yükseltir.
# Günde en fazla 1 kez (spam önleme). Kapatmak için .env'de BREAKING_NEWS_AUTO=false.
BREAKING_NEWS_AUTO = os.getenv("BREAKING_NEWS_AUTO", "true").lower() in ("1", "true", "yes")

# --- Yayın slotları (6 saatte bir = günde 4 post) ---
# Slot adı -> saat (VPS saat dilimine göre; cron bu saatlere kurulur)
SLOT_HOURS = {
    "night": 0,     # 00:00 — Asya seansı / eğitim
    "morning": 6,   # 06:00 — Londra öncesi piyasa brifingi
    "midday": 12,   # 12:00 — Londra/ABD kesişimi: seviyeler / olay
    "evening": 18,  # 18:00 — ABD seansı özeti / CTA
}

# Haftalık içerik planı: (haftanın günü 0=Pzt ... 6=Paz, slot) -> içerik tipi
# İçerik tipleri content_engine.POST_TYPES içinde tanımlıdır.
# STRATEJİ: HABER ağırlıklı (SEO). Teknik (key_levels) haftada 1, promo
# (signals_invite) haftada 2 — "VIP" izlenimini ve promo yorgunluğunu azaltmak için.
WEEKLY_PLAN = {
    # Pazartesi
    (0, "night"): "educational",
    (0, "morning"): "news_brief",
    (0, "midday"): "news_pulse",
    (0, "evening"): "news_recap",
    # Salı
    (1, "night"): "educational",
    (1, "morning"): "news_brief",
    (1, "midday"): "economic_event_watch",
    (1, "evening"): "news_recap",
    # Çarşamba
    (2, "night"): "educational",
    (2, "morning"): "news_brief",
    (2, "midday"): "key_levels",          # haftanın tek teknik postu
    (2, "evening"): "news_recap",
    # Perşembe
    (3, "night"): "signals_invite",       # promo 1/2
    (3, "morning"): "news_brief",
    (3, "midday"): "economic_event_watch",
    (3, "evening"): "news_recap",
    # Cuma
    (4, "night"): "educational",
    (4, "morning"): "news_brief",
    (4, "midday"): "news_pulse",
    (4, "evening"): "weekly_recap",
    # Cumartesi (piyasa kapalı — haber + eğitim)
    (5, "night"): "educational",
    (5, "morning"): "news_recap",
    (5, "midday"): "educational",
    (5, "evening"): "signals_invite",     # promo 2/2
    # Pazar (piyasa kapalı — haftaya bakış)
    (6, "night"): "educational",
    (6, "morning"): "educational",
    (6, "midday"): "weekend_outlook",
    (6, "evening"): "news_brief",
}


def resolve_post_type(weekday: int, slot: str):
    """Verilen gün+slot için içerik tipini döndürür (yoksa None)."""
    return WEEKLY_PLAN.get((weekday, slot))
