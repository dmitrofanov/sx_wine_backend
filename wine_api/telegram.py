import os
import logging
import asyncio
from telegram import Bot
from telegram.error import TelegramError

logger = logging.getLogger(__name__)


class BotTokenIsNotSetError(Exception):
    pass

def send_message(message):
    # Получаем токен бота из настроек
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not bot_token:
        logger.error('TELEGRAM_BOT_TOKEN не установлен в переменных окружения')
        raise BotTokenIsNotSetError('Токен Telegram бота не настроен')

    try:
        # Отправляем сообщение через бота
        bot = Bot(token=bot_token)
        asyncio.run(bot.send_message(
            chat_id=os.getenv('TELEGRAM_ADMIN_CHAT_ID'),
            text=message
        ))
    
    except TelegramError as e:
        logger.error(f'Ошибка при отправке сообщения в Telegram: {e}')
        raise e
    
    except Exception as e:
        logger.error(f'Неожиданная ошибка: {e}')
        raise e