"""TEK SEFERLİK: Telethon oturum dizesi (session string) üretir.

Kendi bilgisayarınızda çalıştırın. Telefonunuza gelen kodu (ve varsa 2FA
şifrenizi) girin. Ekrana basılan uzun dizeyi .env içindeki
TELEGRAM_SESSION_STRING alanına yapıştırın. Bu dize, VPS'te tekrar giriş
yapmadan hesabınız adına mesaj atmayı sağlar.

Önce .env içine TELEGRAM_API_ID ve TELEGRAM_API_HASH değerlerini girin.
"""
from telethon.sync import TelegramClient
from telethon.sessions import StringSession

import config


def main():
    if not config.TELEGRAM_API_ID or not config.TELEGRAM_API_HASH:
        print("HATA: Önce .env içine TELEGRAM_API_ID ve TELEGRAM_API_HASH girin.")
        return
    print("Telegram'a giriş yapılıyor... Telefon numaranızı +90... biçiminde girin.")
    with TelegramClient(StringSession(), config.TELEGRAM_API_ID,
                        config.TELEGRAM_API_HASH) as client:
        session_string = client.session.save()
        me = client.get_me()
        print("\n✅ Giriş başarılı:", me.first_name, f"(@{me.username})")
        print("\n--- Aşağıdaki dizeyi .env içindeki TELEGRAM_SESSION_STRING'e yapıştırın ---\n")
        print(session_string)
        print("\n----------------------------------------------------------------------\n")


if __name__ == "__main__":
    main()
