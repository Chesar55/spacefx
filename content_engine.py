"""Claude ile günlük içerik üretimi.

Her içerik tipi (POST_TYPES) bir talimat + hedef anahtar kelime seti +
hashtag türü tanımlar. Canlı altın verisi ve marka bilgisi prompt'a eklenir.
"""
import anthropic

import config
import keywords
from data_sources import format_market_snapshot, format_news_snapshot, get_gold_news

# ------------------------------------------------------------------
# Marka / sektör bağlamı — her prompt'un başına eklenir.
# ------------------------------------------------------------------
BRAND_CONTEXT = """\
BRAND: SpaceFX Pro (spacefxpro.com)
SECTOR: Forex & Gold (XAUUSD) market NEWS and analysis.
CHANNEL: A public Telegram channel focused on daily gold market NEWS and analysis.
Audience: retail traders searching for gold news, gold price updates and XAUUSD
analysis. This is primarily an SEO play — content must help the channel surface
when people search gold/forex terms.
POSITIONING: Transparent, timely, news-first. We explain what is moving gold RIGHT
NOW and what it means — clear, credible, no hype.
"""

# ------------------------------------------------------------------
# Uyumluluk + SEO kuralları — yanıltıcı finansal vaatler yasak, VIP minimum.
# ------------------------------------------------------------------
COMPLIANCE = """\
STRICT RULES (never break):
- This is educational market commentary, NOT financial advice.
- NEVER promise guaranteed profit, fixed win-rates, or "risk-free" returns.
- NEVER invent specific fake signals, fabricated results, or fake testimonials.
- Levels must be framed as scenarios/zones to watch, not certainties.
- Professional, calm, credible tone. No scam language.
- End market/news posts with a short risk reminder.
SEO / RANKING RULES (critical):
- This channel must rank for gold search terms. Weave the target keywords in
  naturally and early (ideally in the first two lines) — but keep it readable.
- AVOID the word "VIP". Overusing "VIP" pushes the channel DOWN in search. Use
  "premium" or "full signals" AT MOST once, and only in promo posts.
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
- Where relevant (briefs, event watch, recaps, outlooks), weave in the CURRENT
  news narrative from the real headlines provided — mention the theme/driver, not
  a fake quote. Never invent news, numbers, or events beyond what's given.
- Where natural, end with a light engagement nudge (a question to comment on, or
  "which side are you watching?") to invite replies. Keep it classy, never spammy.
- Use emojis with intent (3-6), not decoration.
"""

# ------------------------------------------------------------------
# İçerik tipleri
# ------------------------------------------------------------------
POST_TYPES = {
    "news_brief": {
        "hashtag_kind": "news",
        "keywords": ["gold news", "gold price today", "XAUUSD analysis", "gold price forecast"],
        "instruction": (
            "Write a MORNING GOLD NEWS BRIEF. Lead with the single biggest driver "
            "moving gold RIGHT NOW, taken from the real headlines provided. Explain in "
            "plain terms what's happening and what it means for the gold price today, "
            "tying in the live price. Keep one short line on the level/zone to watch. "
            "90-140 words. Reference the real news theme; never invent facts."
        ),
    },
    "news_pulse": {
        "hashtag_kind": "news",
        "keywords": ["gold market news", "gold price analysis", "XAUUSD news", "live gold price"],
        "instruction": (
            "Write a MIDDAY GOLD NEWS PULSE: what is the market reacting to right now "
            "(from the real headlines) and how the gold price is responding live. Punchy "
            "and current. 70-110 words."
        ),
    },
    "news_recap": {
        "hashtag_kind": "news",
        "keywords": ["gold news today", "gold market update", "gold price forecast"],
        "instruction": (
            "Write an END-OF-DAY GOLD NEWS RECAP: the day's main gold story from the real "
            "headlines, how the price moved, and the key thing to watch next. 100-150 words."
        ),
    },
    "economic_event_watch": {
        "hashtag_kind": "event",
        "keywords": keywords.EVENT_KEYWORDS[:3],
        "instruction": (
            "Write an ECONOMIC EVENT WATCH for gold traders. If the real headlines point "
            "to an upcoming or recent high-impact driver (CPI, NFP, FOMC/Fed, PPI, jobless "
            "claims), center on it; otherwise pick the most relevant recurring one. Explain "
            "how it moves XAUUSD and what to watch. 90-140 words."
        ),
    },
    "educational": {
        "hashtag_kind": "education",
        "keywords": None,  # rotasyonla longtail'den seçilir (main tarafında)
        "instruction": (
            "Write a short EDUCATIONAL post that teaches ONE concrete gold-trading or "
            "gold-news-reading concept for beginner-to-intermediate traders. Genuinely "
            "useful and skimmable. 100-150 words. End with a light nudge to follow for more."
        ),
    },
    "key_levels": {
        "hashtag_kind": "analysis",
        "keywords": ["gold price forecast", "XAUUSD analysis", "gold support and resistance levels"],
        "instruction": (
            "Write a KEY LEVELS update for XAUUSD. Present 2 support zones and 2 "
            "resistance zones as scenarios (e.g. 'a break above X opens the door to Y'), "
            "briefly tying them to the current news backdrop. 80-130 words."
        ),
    },
    "weekly_recap": {
        "hashtag_kind": "news",
        "keywords": ["gold news today", "gold price forecast", "XAUUSD analysis"],
        "instruction": (
            "Write a WEEKLY GOLD RECAP: the week's dominant news theme/direction (from the "
            "real headlines), how the price behaved, and a forward look at next week's news "
            "focus and risk events. 110-160 words."
        ),
    },
    "weekend_outlook": {
        "hashtag_kind": "news",
        "keywords": ["gold price forecast", "gold news", "XAUUSD forecast"],
        "instruction": (
            "Write a WEEKEND GOLD OUTLOOK: the macro/news picture, what to watch for the "
            "week ahead, and the main risk events on the calendar. Calm, strategic tone. "
            "110-160 words."
        ),
    },
    "signals_invite": {
        "hashtag_kind": "cta",
        "keywords": ["gold signals", "gold price analysis", "free gold signals"],
        "instruction": (
            "Write a SOFT invite to the premium gold signals room. Lead with value "
            "(detailed entries, key levels, live market context, risk guidance) — NOT hype "
            "or profit promises. Use the word 'VIP' zero times; say 'premium' or 'full "
            "signals' at most once. 70-110 words. End by inviting them to tap the link "
            "below (the link is added automatically — do NOT write any URL yourself)."
        ),
    },
}


def _client():
    return anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)


def _cta_footer(post_type: str) -> str:
    """Mesaj sonuna eklenen estetik CTA + link bloğu (dile duyarlı).

    SEO gereği "VIP" kelimesi footer'da HİÇ geçmez ("premium/full signals" denir).
    Promo postunda premium link öne çıkar; diğerlerinde büyütülmek istenen free
    kanalı öne çıkarır, premium ikincildir.
    """
    prem = config.VIP_LINK
    free = config.FREE_CHANNEL_LINK
    tr = config.CONTENT_LANG == "tr"

    if post_type == "signals_invite":
        if tr:
            lines = [f"💎 Premium altın sinyalleri → {prem}",
                     f"📲 Günlük ücretsiz altın haber & analiz → {free}"]
        else:
            lines = [f"💎 Get premium gold signals → {prem}",
                     f"📲 Free daily gold news & analysis → {free}"]
    else:
        if tr:
            lines = [f"📲 Günlük ücretsiz altın haber & analiz → {free}",
                     f"💎 Premium gold signals → {prem}"]
        else:
            lines = [f"📲 Free daily gold news & analysis → {free}",
                     f"💎 Premium gold signals → {prem}"]
    return "➖➖➖➖➖➖➖➖\n" + "\n".join(lines)


def generate(post_type: str, gold_data=None, extra_keywords=None, news=None) -> str:
    """Belirtilen içerik tipini üretir ve düz metin döndürür."""
    spec = POST_TYPES[post_type]
    kws = list(spec.get("keywords") or [])
    if extra_keywords:
        kws += list(extra_keywords)
    hashtags = keywords.hashtags_for(spec["hashtag_kind"])
    lang_instr = _LANG_INSTR.get(config.CONTENT_LANG, _LANG_INSTR["en"])
    if news is None:
        news = get_gold_news()

    prompt = f"""{BRAND_CONTEXT}
{COMPLIANCE}
{ENGAGEMENT}

LANGUAGE: {lang_instr}

LIVE MARKET DATA:
{format_market_snapshot(gold_data)}

{format_news_snapshot(news)}

TASK:
{spec['instruction']}

SEO (important — this is a search-ranking play): Weave these target search terms in
naturally and early, especially the headline and first two lines (do NOT keyword-stuff,
keep it readable): {', '.join(kws) if kws else '(general gold news terms)'}
Reminder: do NOT use the word "VIP" anywhere.

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
