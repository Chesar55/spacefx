# SpaceFX — Otonom Altın (XAUUSD) İçerik & SEO Sistemi
### Ekip Sunumu · 17 Temmuz 2026

---

## 1. Tek Cümlede Ne Yaptık?

**Altın (XAUUSD) piyasasını canlı takip edip, günde 4 kez (6 saatte bir), gerçek
haber ve verilerle, SEO uyumlu, İngilizce içerik üreten ve Telegram kanalına
otomatik gönderen otonom bir sistem kurduk.**

Kimse başında beklemez. Sunucu 7/24 çalışır, içerik kendiliğinden akar.

---

## 2. Neden Yapıyoruz? (Amaç)

- 🎯 **SEO / Keşfedilebilirlik:** İnsanlar "gold news", "gold price today",
  "XAUUSD analysis" gibi terimler arattığında **kanalımız öne çıksın.**
- 📈 **Kanal büyütme:** Asıl büyütmek istediğimiz **ücretsiz kanal**
  (t.me/FxSpaceGlobal — "Forex Gold Analysis") her postta öne çıkarılır.
- 💎 **Dönüşüm:** İlgi duyanlar premium sinyal grubuna yönlendirilir.
- ⏱️ **Süreklilik:** Elle içerik üretme yükü sıfıra iner; kanal her gün canlı kalır.

---

## 3. Sistem Nasıl Çalışıyor? (Akış)

```
Zamanlayıcı (6 saatte bir)
        │
        ▼
1) PLAN      → O gün + saat için hangi içerik tipi? (haftalık plan)
2) VERİ      → Canlı altın fiyatı + teknik göstergeler (Yahoo Finance)
3) HABER     → O ana ait gerçek manşetler (Google News)
4) BÜYÜK HABER? → Altını çok ilgilendiren olay varsa "breaking" moduna geç
5) ÜRETİM    → Claude ile İngilizce, SEO'lu, kurallara uygun metin
6) GÖNDERİM  → Telegram kanalına otomatik atılır
7) KAYIT     → Ne, ne zaman atıldı loglanır
```

---

## 4. Günlük Yayın Planı (6 saatte bir · 4 slot)

| Saat  | Slot     | Odak |
|-------|----------|------|
| 00:00 | Gece     | Eğitim / genel içerik |
| 06:00 | Sabah    | Günün haber brifingi |
| 12:00 | Öğle     | Piyasa haber nabzı |
| 18:00 | Akşam    | Gün/hafta haber özeti |

> Hafta içi canlı piyasa haberleri; hafta sonu (piyasa kapalı) eğitim + haftaya
> bakış içeriği. Cuma akşamı otomatik **haftalık özet.**

---

## 5. İçerik Stratejisi — 4 Temel İlke

### 🔑 İlke 1: Haber odaklı (teknik değil)
İçeriğin büyük çoğunluğu **güncel gerçek haberlerden** beslenir. Ağır teknik
analiz haftada sadece 1 kez. Sebep: insanlar haber arar, teknik jargon aramaz.

### 🔑 İlke 2: SEO kelimeleri öne
Hedef arama terimleri (gold news, gold price today, XAUUSD analysis...)
**manşete ve ilk iki satıra** doğal biçimde yerleştirilir.

### 🔑 İlke 3: "VIP" kelimesinden kaçın
Aşırı "VIP" kullanımı kanalı aramalarda **aşağı düşürüyor.** Bu yüzden içerikte
ve hashtag'lerde "VIP" geçmez; onun yerine "premium / full signals" denir.

### 🔑 İlke 4: ASLA öngörü/tahmin yok
"Altın yükselecek/düşecek", fiyat hedefi, "gelecek hafta şu olur" **yasak.**
Sadece **şu an ne oluyor** anlatılır; seviyeler tarafsız "izlenecek bölge"
olarak, iki yönlü verilir. (Uyumluluk + güvenilirlik.)

---

## 6. Canlı Veri Kaynakları (Hepsi Ücretsiz)

| Veri | Kaynak | Kullanım |
|------|--------|----------|
| Fiyat + günlük değişim | Yahoo Finance (GC=F) | Her postta anlık |
| Günlük / 20-günlük yüksek-düşük | Yahoo Finance | Gerçek destek/direnç |
| MA50, MA200, RSI-14 | Yerinde hesaplanır | Piyasa durumu |
| Yedek fiyat | gold-api.com | Yahoo çökerse |
| Güncel haberler | Google News RSS | Gerçek manşetler |

> Önemli: Fiyat ve göstergeler **gerçek ve canlı.** Destek/direnç seviyeleri bu
> gerçek verilerden türetilir — uydurma değil.

---

## 7. İçerik Tipleri

- **news_brief** — Sabah haber brifingi
- **news_pulse** — Öğle haber nabzı
- **news_recap** — Gün sonu haber özeti
- **breaking_news** — Büyük haber özel postu (bkz. slide 8)
- **economic_event_watch** — Fed / CPI / NFP takibi
- **weekly_recap** — Cuma haftalık özet
- **weekend_outlook** — Pazar haftaya bakış
- **educational** — Eğitim içeriği
- **key_levels** — Teknik seviyeler (haftada 1)
- **signals_invite** — Premium davet (haftada 2, "VIP" kelimesi yok)

---

## 8. Öne Çıkan Özellik: Otomatik "Büyük Haber" Modu

Altını çok ilgilendiren bir olay çıktığında (Fed kararı, enflasyon,
savaş/jeopolitik, rekor seviye, sert düşüş...) sistem bunu **kendi tespit eder** ve
o slotu özel bir posta yükseltir:

1. Haberi anlatır 📰
2. Altına etkisini açıklar 📊
3. **"Bu tür hızlı haber akışında gerçek zamanlı analiz için kanala katıl"**
   diyerek kanala davet eder (CTA) 📩

> Günde en fazla 1 kez tetiklenir (spam olmaz). İstenirse kapatılabilir.

**Örnek (gerçek üretim):**
> 🔴 GOLD NEWS TODAY: MIDDLE EAST TENSIONS DRIVE THE TAPE
> Escalating Middle East tensions are reinforcing US rate-hike bets... For
> real-time gold news and analysis as this story develops, follow the channel below.

---

## 9. Link / CTA Stratejisi

Her postun altında, temiz ve estetik bir bölüm:

```
➖➖➖➖➖➖➖➖
📲 Free daily gold news & analysis → (ücretsiz kanal)
💎 Premium gold signals → (premium alım linki)
```

- Normal postlarda **ücretsiz kanal başta** (büyütmek istediğimiz kanal).
- Premium davet postunda premium link başta.
- Linkleri **sistem yazar** (Claude değil) → asla bozulmaz.

---

## 10. Uyumluluk & Güvenlik Kuralları

- ✅ Her postta: *"Yatırım tavsiyesi değildir — Trade safely"* uyarısı.
- 🚫 Garantili kazanç / sabit başarı oranı / "risksiz" iddiası **yok.**
- 🚫 Sahte sinyal, uydurma sonuç, sahte yorum **yok.**
- 🚫 Yön tahmini / fiyat hedefi **yok** (slide 5, İlke 4).
- 🔒 Gizli anahtarlar (`.env`, session) repoya/paylaşıma **girmez.**

---

## 11. Teknik Altyapı

- **Dil:** Python
- **İçerik üretimi:** Claude API (model: claude-opus-4-8)
- **Gönderim:** Telethon (kişisel hesap üzerinden — bot değil)
- **Barındırma:** VPS (7/24 açık sunucu)
- **Zamanlama:** 6 saatte bir otomatik çalışma
- **Kod deposu:** GitHub → güncelleme `git pull` ile saniyeler içinde

**Maliyet:** Telegram + veri kaynakları ücretsiz. Tek gider Claude API — günde
~4 kısa metin, çok düşük.

---

## 12. Durum & Yol Haritası

**✅ Tamamlanan**
- Otonom içerik motoru (haber + canlı veri + SEO)
- Büyük haber otomatik tespiti + CTA
- "VIP minimum" ve "tahmin yok" kuralları
- GitHub'a taşındı

**🔜 Sıradaki**
- VPS'e kurulum + otomatik zamanlama (devam ediyor)
- Genişleme: aynı içeriği web sitesine blog olarak besleme (asıl SEO gücü sitede)
- Türkçe içerik seçeneği (altyapı hazır)

---

## Özet

> Gerçek verilerle beslenen, haber odaklı, SEO uyumlu, tahminde bulunmayan,
> kendini yöneten bir içerik makinesi kurduk. Amaç: altın araması yapan
> herkesin karşısına çıkmak ve kanalı organik olarak büyütmek.

**Sorular?**
