"""Telethon ile kişisel hesap üzerinden kanala mesaj gönderimi."""
from telethon.sync import TelegramClient
from telethon.sessions import StringSession

import config


def send(text: str):
    if not config.TELEGRAM_SESSION_STRING:
        raise RuntimeError(
            "TELEGRAM_SESSION_STRING boş. Önce 'python generate_session.py' çalıştırın."
        )
    with TelegramClient(
        StringSession(config.TELEGRAM_SESSION_STRING),
        config.TELEGRAM_API_ID,
        config.TELEGRAM_API_HASH,
    ) as client:
        # parse_mode=None -> düz metin, özel karakter kaçış sorunu yaşanmaz
        client.send_message(config.TELEGRAM_CHANNEL, text,
                            parse_mode=None, link_preview=False)
    return True
