"""Claude ile günlük içerik üretimi.

Her içerik tipi (POST_TYPES) bir talimat + hedef anahtar kelime seti +
hashtag türü tanımlar. Canlı altın verisi ve marka bilgisi prompt'a eklenir.
"""
import anthropic

import config
import keywords
from data_sources import format_market_snapshot

# ------------------------------------------------------------------
# Marka / sektör bağlamı — her prompt'un başına eklenir.
# ------------------------------------------------------------------
BRAND_CONTEXT = """\
BRAND: SpaceFX Pro (spacefxpro.com)
SECTOR: Forex & Gold (XAUUSD) trading signals + market education.
CHANNEL: A public Telegram channel that posts gold market analysis and
promotes the VIP signal group. Audience: retail traders following XAUUSD.
POSITIONING: Transparent, disciplined, education-first. We stand out through
clear key levels, reasoning, and honest risk talk — NOT hype.
"""

# ------------------------------------------------------------------
# Uyumluluk kuralları — yanıltıcı finansal vaatler yasak.
# ------------------------------------------------------------------
COMPLIANCE = """\
STRICT RULES (never break):
- This is educational market commentary, NOT financial advice.
- NEVER promise guaranteed profit, fixed win-rates, or "risk-free" returns.
- NEVER invent specific fake signals, fabricated results, or fake testimonials.
- Support/resistance levels must be framed as scenarios/zones to watch, not certainties.
- Always keep a professional, calm, credible tone. Hype words are fine sparingly (🚀) but no scam language.
- End market/analysis posts with a short risk reminder.
"""

_LANG_INSTR = {
    "en": "Write in clear, professional English.",
    "tr": "Metni akıcı, profesyonel Türkçe yaz.",
}

# ------------------------------------------------------------------
# Etkileşim (engagement) direktifi — ilgi çekmek için, uyumluluğu bozmadan.
# ------------------------------------------------------------------
ENGAGEMENT = """\
ENGAGEMENT (make it stop the scroll — without hype or false promises):
- Open with a SHORT punchy hook line (a bold observation, a sharp question, or
  a tension) tied to the live data — not a generic greeting.
- Give ONE clear, memorable takeaway readers can act on or remember.
- Reference the REAL numbers from the live data (price, today's range, moving
  averages, RSI) so it reads like fresh, current analysis — not evergreen filler.
- Where natural, end with a light engagement nudge (a question to comment on, or
  "which side are you watching?") to invite replies. Keep it classy, never spammy.
- Use emojis with intent (3-6), not decoration.
"""

# ------------------------------------------------------------------
# İçerik tipleri
# ------------------------------------------------------------------
POST_TYPES = {
    "market_open_brief": {
        "hashtag_kind": "analysis",
        "keywords": ["XAUUSD analysis", "gold price today", "gold signals"],
        "instruction": (
            "Write a concise PRE-MARKET gold (XAUUSD) brief for today. "
            "Cover: current bias (bullish/bearish/neutral) with reasoning, one key "
            "support zone and one key resistance zone to watch, and what could move "
            "price during the London/US sessions. 90-140 words. Use 3-5 relevant emojis."
        ),
    },
    "key_levels": {
        "hashtag_kind": "analysis",
        "keywords": ["gold support and resistance levels", "XAUUSD signals", "buy sell gold signal"],
        "instruction": (
            "Write a KEY LEVELS update for XAUUSD. Present 2 support zones and 2 "
            "resistance zones as scenarios (e.g. 'a break above X opens the door to Y'). "
            "Explain the intraday bias briefly. 80-130 words. Structure with line breaks."
        ),
    },
    "economic_event_watch": {
        "hashtag_kind": "event",
        "keywords": keywords.EVENT_KEYWORDS[:3],
        "instruction": (
            "Write an ECONOMIC EVENT WATCH post for gold traders. Pick a relevant "
            "recurring high-impact driver (CPI, NFP, FOMC/Fed, PPI, jobless claims) and "
            "explain how it typically affects XAUUSD and what traders should watch. "
            "If no live event today, frame it as general preparation. 90-140 words."
        ),
    },
    "educational": {
        "hashtag_kind": "education",
        "keywords": None,  # rotasyonla longtail'den seçilir (main tarafında)
        "instruction": (
            "Write a short EDUCATIONAL post that teaches ONE concrete gold-trading "
            "concept for beginners-to-intermediate traders. Make it genuinely useful "
            "and skimmable. 100-150 words. End with a light nudge to follow for more."
        ),
    },
    "midday_update": {
        "hashtag_kind": "analysis",
        "keywords": ["live gold signals", "XAUUSD analysis"],
        "instruction": (
            "Write a MID-SESSION XAUUSD update: how price has behaved so far vs the "
            "morning bias, and what to watch into the close. 70-110 words."
        ),
    },
    "weekly_recap": {
        "hashtag_kind": "analysis",
        "keywords": ["gold trading signals", "XAUUSD analysis"],
        "instruction": (
            "Write a WEEKLY RECAP for XAUUSD: the week's dominant theme/direction, key "
            "levels that mattered, and a forward look at next week's focus. 110-160 words."
        ),
    },
    "weekend_outlook": {
        "hashtag_kind": "analysis",
        "keywords": ["XAUUSD analysis", "gold price today"],
        "instruction": (
            "Write a WEEKEND OUTLOOK for gold: the macro picture, key zones for the week "
            "ahead, and the main risk events on the calendar. Calm, strategic tone. 110-160 words."
        ),
    },
    "vip_soft_cta": {
        "hashtag_kind": "cta",
        "keywords": ["gold signals telegram", "free gold signals"],
        "instruction": (
            "Write a SOFT promotional post inviting followers to the VIP signal group. "
            "Lead with value (what members get: detailed entries, key levels, market "
            "context, risk guidance) — NOT hype or profit promises. 70-110 words. "
            "End by inviting them to tap the VIP link below to join (the link is added "
            "automatically after your text — do NOT write any URL yourself)."
        ),
    },
}


def _client():
    return anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)


def _cta_footer(post_type: str) -> str:
    """Mesaj sonuna eklenen estetik CTA + link bloğu (dile duyarlı).

    VIP CTA postlarında VIP linki öne çıkar; diğerlerinde büyütmek istediğimiz
    free kanalı öne çıkarır, VIP'i ikincil sunar.
    """
    vip = config.VIP_LINK
    free = config.FREE_CHANNEL_LINK
    tr = config.CONTENT_LANG == "tr"

    if post_type == "vip_soft_cta":
        if tr:
            lines = [f"💎 VIP'e katıl → {vip}",
                     f"📲 Hazır değil misin? Ücretsiz kanal → {free}"]
        else:
            lines = [f"💎 Join VIP now → {vip}",
                     f"📲 Not ready yet? Free channel → {free}"]
    else:
        if tr:
            lines = [f"📲 Günlük ücretsiz altın analizi → {free}",
                     f"💎 VIP sinyaller & net girişler → {vip}"]
        else:
            lines = [f"📲 Free daily gold analysis → {free}",
                     f"💎 VIP signals & live entries → {vip}"]
    return "➖➖➖➖➖➖➖➖\n" + "\n".join(lines)


def generate(post_type: str, gold_data=None, extra_keywords=None) -> str:
    """Belirtilen içerik tipini üretir ve düz metin döndürür."""
    spec = POST_TYPES[post_type]
    kws = list(spec.get("keywords") or [])
    if extra_keywords:
        kws += list(extra_keywords)
    hashtags = keywords.hashtags_for(spec["hashtag_kind"])
    lang_instr = _LANG_INSTR.get(config.CONTENT_LANG, _LANG_INSTR["en"])

    prompt = f"""{BRAND_CONTEXT}
{COMPLIANCE}
{ENGAGEMENT}

LANGUAGE: {lang_instr}

LIVE MARKET DATA:
{format_market_snapshot(gold_data)}

TASK:
{spec['instruction']}

SEO: Naturally weave in some of these search terms (do NOT keyword-stuff, keep it
readable): {', '.join(kws) if kws else '(general gold trading terms)'}

FORMAT RULES:
- Plain text suitable for a Telegram message (NO markdown symbols like * or _).
- Start with a short bold-feeling headline line (use CAPS or an emoji, not markdown).
- Use short lines / line breaks for readability, with emojis placed intentionally
  (lead a section or a key line — not clustered or random) for a clean, aesthetic look.
- Do NOT include any links, URLs, @handles, disclaimer, or hashtags yourself —
  the CTA links, disclaimer and hashtags are all appended automatically.
- Output ONLY the post text, nothing else."""

    resp = _client().messages.create(
        model=config.CLAUDE_MODEL,
        max_tokens=2000,
        thinking={"type": "adaptive"},
        output_config={"effort": config.CLAUDE_EFFORT},
        messages=[{"role": "user", "content": prompt}],
    )
    body = "".join(b.text for b in resp.content if b.type == "text").strip()

    disclaimer = ("⚠️ Educational content only — not financial advice. Trade safely."
                  if config.CONTENT_LANG == "en"
                  else "⚠️ Yalnızca eğitim amaçlıdır — yatırım tavsiyesi değildir. Güvenli işlem yapın.")

    footer = _cta_footer(post_type)

    return f"{body}\n\n{footer}\n\n{disclaimer}\n\n{hashtags}"
