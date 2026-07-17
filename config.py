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
# Hafta içi: canlı piyasa içeriği. Hafta sonu (piyasa kapalı): evergreen içerik.
WEEKLY_PLAN = {
    # Pazartesi
    (0, "night"): "educational",
    (0, "morning"): "market_open_brief",
    (0, "midday"): "key_levels",
    (0, "evening"): "midday_update",
    # Salı
    (1, "night"): "vip_soft_cta",
    (1, "morning"): "market_open_brief",
    (1, "midday"): "economic_event_watch",
    (1, "evening"): "key_levels",
    # Çarşamba
    (2, "night"): "educational",
    (2, "morning"): "market_open_brief",
    (2, "midday"): "key_levels",
    (2, "evening"): "midday_update",
    # Perşembe
    (3, "night"): "educational",
    (3, "morning"): "market_open_brief",
    (3, "midday"): "economic_event_watch",
    (3, "evening"): "key_levels",
    # Cuma
    (4, "night"): "vip_soft_cta",
    (4, "morning"): "market_open_brief",
    (4, "midday"): "key_levels",
    (4, "evening"): "weekly_recap",
    # Cumartesi (piyasa kapalı — evergreen)
    (5, "night"): "educational",
    (5, "morning"): "educational",
    (5, "midday"): "vip_soft_cta",
    (5, "evening"): "educational",
    # Pazar (piyasa kapalı — evergreen + haftaya bakış)
    (6, "night"): "educational",
    (6, "morning"): "educational",
    (6, "midday"): "weekend_outlook",
    (6, "evening"): "vip_soft_cta",
}


def resolve_post_type(weekday: int, slot: str):
    """Verilen gün+slot için içerik tipini döndürür (yoksa None)."""
    return WEEKLY_PLAN.get((weekday, slot))
