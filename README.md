# SpaceFX Pro — Telegram Otonom İçerik Sistemi

`t.me/XAUUSD_GoldSignalsVIP` kanalına her gün, **kişisel hesabınız adına**,
canlı altın verisi + Claude AI ile üretilmiş, SEO-uyumlu içerikleri otomatik
gönderir.

İçerik/SEO stratejisi için: **[content_plan.md](content_plan.md)**

---

## Nasıl çalışır?

```
cron (VPS)  ->  main.py --slot <slot>
                     │
                     ├─ data_sources.py   canlı XAUUSD fiyatı (ücretsiz API)
                     ├─ content_engine.py Claude ile metin üretimi (+ uyumluluk)
                     └─ poster.py         Telethon ile kişisel hesaptan gönderim
```

Haftalık plan `config.py > WEEKLY_PLAN`, içerik tipleri
`content_engine.py > POST_TYPES` içindedir.

---

## Kurulum (adım adım)

### 1) Gereksinimler
- Python 3.10+
- Anthropic API anahtarı — https://console.anthropic.com
- Telegram API kimliği — https://my.telegram.org → *API development tools*
  (küçük bir uygulama oluşturun; `api_id` ve `api_hash` alın)

### 2) Bağımlılıklar
```bash
pip install -r requirements.txt
```

### 3) Ayar dosyası
```bash
cp .env.example .env      # Windows: copy .env.example .env
```
`.env` içini doldurun: `ANTHROPIC_API_KEY`, `TELEGRAM_API_ID`, `TELEGRAM_API_HASH`.

### 4) Telegram oturumu (TEK SEFER, kendi bilgisayarınızda)
```bash
python generate_session.py
```
Telefon numaranızı `+90...` biçiminde girin, gelen kodu (varsa 2FA şifresini)
yazın. Ekrandaki uzun dizeyi `.env > TELEGRAM_SESSION_STRING` alanına yapıştırın.

> Bu dize, VPS'te tekrar giriş yapmadan hesabınız adına mesaj atmayı sağlar.
> Kanalın admini olduğunuz için ek yetki gerekmez.

### 5) Test (mesaj atmadan)
```bash
python data_sources.py                 # canlı fiyat geliyor mu?
python main.py --type educational --dry # örnek içerik üret, ekrana yaz
```
Beğenirseniz gerçek gönderim:
```bash
python main.py --type educational
```

---

## VPS'te 7/24 otonom çalıştırma (cron)

1. Projeyi VPS'e kopyalayın, `pip install -r requirements.txt` çalıştırın,
   `.env` dosyasını (session string dahil) VPS'e taşıyın.
2. VPS saat dilimini kontrol edin: `timedatectl` (gerekirse
   `sudo timedatectl set-timezone Europe/Istanbul`).
3. `crontab -e` ile şunları ekleyin (saatler `config.py > SLOT_HOURS` ile uyumlu):

```cron
# dizini kendi yolunuzla değiştirin — 6 saatte bir (günde 4 post)
0  0  * * *  cd /home/user/spacefx && /usr/bin/python3 main.py --slot night   >> run.log 2>&1
0  6  * * *  cd /home/user/spacefx && /usr/bin/python3 main.py --slot morning >> run.log 2>&1
0  12 * * *  cd /home/user/spacefx && /usr/bin/python3 main.py --slot midday  >> run.log 2>&1
0  18 * * *  cd /home/user/spacefx && /usr/bin/python3 main.py --slot evening >> run.log 2>&1
```

`main.py`, o gün/slot için plan yoksa hiçbir şey yapmadan çıkar; aynı slotu
günde iki kez atmaz. Yani üç cron satırı tüm haftalık planı yürütür.

> Alternatif: sürekli çalışan bir servis istemiyorsanız cron en basitidir.
> `systemd timer` tercih ederseniz aynı komutları timer'a bağlayabilirsiniz.

---

## Sık ayarlar

| İstek | Yer |
|------|-----|
| Gün/slot planını değiştir | `config.py > WEEKLY_PLAN` |
| Yayın saatleri | `config.py > SLOT_HOURS` + crontab |
| İçerik tipleri / talimatlar | `content_engine.py > POST_TYPES` |
| Anahtar kelimeler / hashtag | `keywords.py` |
| Dil (en/tr) | `.env > CONTENT_LANG` |
| Model / maliyet | `.env > CLAUDE_MODEL` (ör. `claude-sonnet-5`) |
| Uyumluluk kuralları | `content_engine.py > COMPLIANCE` |

---

## Güvenlik notları
- `.env`, `*.session`, `posted_history.json` **paylaşılmaz** (`.gitignore`'da).
- Session string'i sızdırmayın — hesabınıza erişim demektir.
- İçerikler "yatırım tavsiyesi değildir" disclaimer'ı ile çıkar; garantili
  kazanç iddiası üretmemesi için model kısıtlanmıştır.
```
