# Kullanım Kılavuzu — Bot Nasıl İşler?

Bu bot, `XAUUSD_GoldSignalsVIP` kanalına **kişisel hesabınız adına** her gün
otomatik içerik atar. Aşağıda günlük işleyiş, komutlar ve yönetim anlatılır.

---

## 1. Bot ne yapar? (tek cümle)

Belirlenen saatlerde → canlı altın fiyatını çeker → o güne/saate uygun içerik
tipini seçer → Claude ile İngilizce, SEO-uyumlu, disclaimer'lı metni üretir →
kanala gönderir → kaydını tutar.

---

## 2. İşleyiş akışı

```
Zamanlayıcı (cron)  →  python main.py --slot <slot>
        │
        1) config.py    → bugün + slot için hangi içerik tipi? (WEEKLY_PLAN)
        2) data_sources → canlı XAUUSD fiyatı (ücretsiz)
        3) content_engine → Claude ile metin + disclaimer + hashtag
        4) poster.py    → Telethon ile kanala gönderir
        5) posted_history.json + run.log → kayıt
```

Günde **4 slot** var — **6 saatte bir** post (saatler `config.py > SLOT_HOURS`'ta, VPS saatine göre):

| Slot | Saat | Amaç |
|------|------|------|
| `night`   | 00:00 | Asya seansı / eğitim |
| `morning` | 06:00 | Londra öncesi piyasa brifingi |
| `midday`  | 12:00 | Londra/ABD kesişimi: seviyeler / ekonomik olay |
| `evening` | 18:00 | ABD seansı özeti / haftalık özet / VIP CTA |

Haftalık plan (hangi gün-slot hangi içerik) `config.py > WEEKLY_PLAN`'da.
Hafta içi canlı piyasa içeriği; hafta sonu (piyasa kapalı) eğitim + haftaya
bakış + CTA gibi "evergreen" içerik atılır. Örn. Cuma akşamı "haftalık özet",
Pazar öğlen "haftaya bakış".

**Bot akıllıdır:** o gün/slot için plan yoksa hiçbir şey yapmadan çıkar; aynı
slotu günde iki kez atmaz (posted_history.json kontrolü).

---

## 3. Elle çalıştırma (test / manuel gönderim)

Her komut `C:\spacefxtelegramyönetim` klasöründen çalışır.

| Komut | Ne yapar |
|-------|----------|
| `python main.py --type educational --dry` | Eğitim içeriği üretir, **atmadan** ekrana yazar |
| `python main.py --type educational` | Aynısını üretir ve **gerçekten atar** |
| `python main.py --slot morning` | Bugünün sabah içeriğini üretir + atar |
| `python main.py auto` | Şu anki saate en yakın slotu seçer |
| `python data_sources.py` | Sadece canlı fiyatı test eder |

**Kullanılabilir içerik tipleri** (`--type` ile):
`market_open_brief`, `key_levels`, `economic_event_watch`, `educational`,
`midday_update`, `weekly_recap`, `weekend_outlook`, `vip_soft_cta`.

> İpucu: Bir şeyi denemeden önce `--dry` ekleyin; beğenirseniz `--dry`'siz atın.

---

## 4. 7/24 otonom çalıştırma (asıl kullanım — VPS)

Otonomluk için bot bir **VPS'te (7/24 açık sunucu)** cron ile çalışır. Bilgisayarınız
kapalıyken de post atılmaya devam eder.

1. Projeyi + `.env`'i VPS'e taşıyın, `pip install -r requirements.txt` çalıştırın.
2. `crontab -e` ile 4 satır ekleyin (6 saatte bir):
   ```
   0  0  * * *  cd /yol/spacefx && python3 main.py --slot night   >> run.log 2>&1
   0  6  * * *  cd /yol/spacefx && python3 main.py --slot morning >> run.log 2>&1
   0  12 * * *  cd /yol/spacefx && python3 main.py --slot midday  >> run.log 2>&1
   0  18 * * *  cd /yol/spacefx && python3 main.py --slot evening >> run.log 2>&1
   ```
Bu dört satır tüm haftalık planı otomatik yürütür. Başka hiçbir şey gerekmez.

> VPS yoksa: Windows Görev Zamanlayıcı ile aynı komutları planlayabilirsiniz,
> ama bilgisayar kapalıyken post atılmaz.

---

## 5. Kontrol ve izleme

- **Ne atıldı?** → `posted_history.json` (tarih, saat, slot, tip, önizleme).
- **Çalışma günlüğü / hatalar?** → `run.log`.
- **Kanalı kontrol edin** — mesajlar sizin adınıza görünür.

---

## 6. İçeriği/planı özelleştirme

| İstek | Nereden |
|------|---------|
| Gün/slot planı | `config.py > WEEKLY_PLAN` |
| Yayın saatleri | `config.py > SLOT_HOURS` + crontab |
| Metin talimatları (uzunluk, ton) | `content_engine.py > POST_TYPES` |
| Marka tanımı | `content_engine.py > BRAND_CONTEXT` |
| Uyumluluk kuralları | `content_engine.py > COMPLIANCE` |
| Anahtar kelime / hashtag | `keywords.py` |
| Dil (en/tr) | `.env > CONTENT_LANG` |
| Model / maliyet | `.env > CLAUDE_MODEL` |

---

## 7. Maliyet

- **Telegram / veri:** ücretsiz.
- **Claude API:** günde ~2–3 kısa metin. Her metin küçük (~birkaç bin token).
  `claude-opus-4-8` en yeteneklisi; ucuzlatmak için `.env`'de
  `CLAUDE_MODEL=claude-sonnet-5` yapın.

---

## 8. Sık sorunlar

| Belirti | Çözüm |
|--------|-------|
| `SESSION_STRING boş` | `python generate_session.py` (gerçek terminalde) |
| `EOF when reading a line` | Etkileşimli giriş; ayrı PowerShell penceresinde çalıştırın |
| Emoji yazdırma hatası (Windows) | Düzeltildi (UTF-8). Gerekirse `set PYTHONIOENCODING=utf-8` |
| Canlı fiyat gelmiyor | Bot yine de fiyatsız genel içerik üretir; `run.log`'a bakın |
| Yanlış saatte atıyor | VPS saat dilimini kontrol edin (`timedatectl`) |

---

## 9. Güvenlik

- `.env`, `*.session`, `posted_history.json` paylaşılmaz (`.gitignore`).
- Session string = hesap erişimi; sızdırmayın.
- Bot garantili kazanç iddiası üretmez; her post disclaimer ile çıkar.
