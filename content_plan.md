# SpaceFX Pro — Telegram İçerik & SEO Stratejisi

Kanal: `t.me/XAUUSD_GoldSignalsVIP` · Sektör: Forex & Altın (XAUUSD) sinyalleri
Dil: İngilizce (uluslararası trader kitlesi + global arama hacmi)

---

## 1. Amaç ve gerçekçi SEO beklentisi

**Hedef:** Google'da altın sinyali aramalarında öne çıkmak + Telegram kanalını
büyütmek.

**Dürüst mekanik:** Telegram mesajları Google'da doğrudan güçlü sıralanmaz.
Değerin oluştuğu iki yer:
1. **`t.me/s/XAUUSD_GoldSignalsVIP`** genel önizleme sayfası — düzenli, anahtar
   kelime içeren, hashtag'li içerik burada kısmen indexlenir.
2. **Asıl SEO motoru = web sitesi.** En etkili büyüme için bu sistemle üretilen
   günlük analizi **aynı zamanda sitenizde bir blog/analiz yazısına** çevirmek
   gerekir (bkz. Bölüm 6 — Genişleme). Telegram etkileşimi, site sıralamayı taşır.

Bu yüzden içerikler hem "Telegram-doğal" (emoji, kısa satır, hashtag) hem de
**anahtar kelime bakımından SEO-uyumlu** üretilir.

---

## 2. Hedef anahtar kelimeler

Ayrıntılı liste `keywords.py` içinde. Özet:

**Ana (yüksek hacim, yüksek rekabet):**
`gold signals`, `XAUUSD signals`, `forex gold signals`, `gold trading signals`,
`free gold signals`, `gold price today`, `XAUUSD analysis`.

**Uzun kuyruk (düşük rekabet, dönüşüm yüksek) — eğitim içerikleri için:**
`how to trade gold with signals`, `what is XAUUSD`, `gold support and resistance
levels`, `how CPI affects gold price`, `NFP gold trading`, `risk management in
gold trading`.

**Olay odaklı:** `gold NFP forecast`, `gold CPI reaction`, `Fed decision gold impact`.

Strateji: **ana kelimeler** analiz postlarında, **uzun kuyruk** eğitim
postlarında hedeflenir. Uzun kuyruk, hızlı sıralama kazanmanın en gerçekçi yolu.

---

## 3. Haftalık yayın takvimi

Günde ~2–3 post. Slotlar (VPS saatine göre `config.py`):
`morning` (08:00 — piyasa öncesi), `midday` (13:00), `evening` (20:00).

| Gün | Sabah | Öğle | Akşam |
|-----|-------|------|-------|
| Pzt | Piyasa açılış brifingi | Kilit seviyeler | Eğitim |
| Sal | Piyasa açılış brifingi | Ekonomik olay izleme | VIP yumuşak CTA |
| Çar | Piyasa açılış brifingi | Kilit seviyeler | Eğitim |
| Per | Piyasa açılış brifingi | Ekonomik olay izleme | Gün içi güncelleme |
| Cum | Piyasa açılış brifingi | Kilit seviyeler | Haftalık özet |
| Cmt | — | Eğitim | — |
| Paz | — | — | Haftaya bakış |

Planı değiştirmek: `config.py > WEEKLY_PLAN`.

---

## 4. İçerik tipleri (ne, neden)

`content_engine.py > POST_TYPES` içinde tanımlı. Her biri farklı bir SEO/etkileşim amacına hizmet eder:

- **market_open_brief** — günlük düzenlilik + `XAUUSD analysis`, `gold price today`.
- **key_levels** — trader'ların en çok aradığı içerik; destek/direnç *senaryo* olarak.
- **economic_event_watch** — CPI/NFP/Fed; olay kelimelerini yakalar, otorite kurar.
- **educational** — uzun kuyruk SEO'nun ana aracı; her gün farklı konu (rotasyon).
- **weekly_recap / weekend_outlook** — düzenli takip alışkanlığı.
- **vip_soft_cta** — değer-önce satış; kanaldan VIP'e dönüşüm.

---

## 5. Uyumluluk / marka güvenliği

`content_engine.py > COMPLIANCE` her prompt'a gömülür:
- "Yatırım tavsiyesi değildir" disclaimer'ı her postun sonunda otomatik.
- **Garantili kazanç / sabit win-rate / risksiz getiri iddiası YASAK.**
- Sahte sinyal/sonuç/yorum uydurmak yasak.
- Seviyeler kesinlik değil, "izlenecek senaryo" olarak sunulur.

Bu, hem itibar hem de reklam/platform politikaları açısından kritik.

---

## 6. Genişleme (öneri — sonraki adım)

En yüksek SEO getirisi için, üretilen günlük analizin **aynı anda web sitesine
SEO-optimize blog yazısı** olarak da yayınlanması. Sistem buna hazır tasarlandı:
`content_engine.generate()` çıktısı bir web-CMS API'sine (WordPress REST, Ghost,
Next.js) beslenebilir. İstenirse ikinci faz olarak eklenir.

Ek fikirler: haftalık en iyi analizin görselleştirilmesi (grafik), YouTube Shorts
için metin→seslendirme, e-posta bülteni.
