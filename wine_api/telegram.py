import os
import logging
import asyncio
from telegram import Bot
from telegram.error import TelegramError
from rest_framework import status as rest_status

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

def handle_message(message):
    try:
        send_message(message)
        return {'success': True, 'message': 'Уведомление успешно отправлено',}, rest_status.HTTP_200_OK
    except BotTokenIsNotSetError as e:
            return {'error': str(e)}, rest_status.HTTP_500_INTERNAL_SERVER_ERROR
    except TelegramError as e:
            return {'error': f'Ошибка при отправке сообщения в Telegram: {str(e)}'}, rest_status.HTTP_500_INTERNAL_SERVER_ERROR
    except Exception as e:
            return {'error': f'Внутренняя ошибка сервера: {str(e)}'}, rest_status.HTTP_500_INTERNAL_SERVER_ERROR