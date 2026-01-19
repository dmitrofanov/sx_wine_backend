from datetime import date
import os
import logging
import asyncio

from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
from telegram import Bot
from telegram.error import TelegramError

from .models import Wine, Event, Person
from .serializers import WineSerializer, EventSerializer, PersonSerializer

logger = logging.getLogger(__name__)


class WineViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet для чтения данных о винах.
    Предоставляет только GET endpoints.
    """
    queryset = Wine.objects.all()
    serializer_class = WineSerializer


class EventViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet для чтения данных о событиях.
    Предоставляет только GET endpoints.
    """
    serializer_class = EventSerializer

    def get_queryset(self):
        """
        Фильтрация событий по дате:
        - date_before: события с датой <= указанной
        - date_after: события с датой >= указанной
        Формат даты: YYYY-MM-DD.
        """
        qs = Event.objects.all()
        date_before = self.request.query_params.get("date_before")
        date_after = self.request.query_params.get("date_after")

        if date_before:
            try:
                parsed = date.fromisoformat(date_before)
                qs = qs.filter(date__lte=parsed)
            except ValueError:
                pass  # некорректный формат — игнорируем фильтр

        if date_after:
            try:
                parsed = date.fromisoformat(date_after)
                qs = qs.filter(date__gte=parsed)
            except ValueError:
                pass  # некорректный формат — игнорируем фильтр

        return qs


class PersonViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с персонами.
    Предоставляет GET, POST, PUT, PATCH, DELETE endpoints.
    """
    queryset = Person.objects.all()
    serializer_class = PersonSerializer


@api_view(['POST'])
def send_wine_interest_notification(request):
    """
    Endpoint для отправки уведомления о заинтересованности вином в Telegram.
    
    Принимает:
    - nickname: никнейм пользователя (Person)
    - wine_id: Primary Key вина (Wine)
    
    Отправляет сообщение в Telegram пользователю с указанным nickname.
    """
    nickname = request.data.get('nickname')
    wine_id = request.data.get('wine_id')
    
    # Валидация входных данных
    if not nickname:
        return Response(
            {'error': 'Параметр nickname обязателен'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if not wine_id:
        return Response(
            {'error': 'Параметр wine_id обязателен'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        # Получаем пользователя по nickname
        person = Person.objects.get(nickname=nickname)
    except Person.DoesNotExist:
        return Response(
            {'error': f'Пользователь с nickname "{nickname}" не найден'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    try:
        # Получаем вино по ID
        wine = Wine.objects.get(pk=wine_id)
    except Wine.DoesNotExist:
        return Response(
            {'error': f'Вино с ID {wine_id} не найдено'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Получаем токен бота из настроек
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not bot_token:
        logger.error('TELEGRAM_BOT_TOKEN не установлен в переменных окружения')
        return Response(
            {'error': 'Токен Telegram бота не настроен'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    # Формируем сообщение
    message = f"Пользователь {person.nickname} интересуется вином {wine.full_name}"
    
    try:
        # Отправляем сообщение через бота
        bot = Bot(token=bot_token)
        asyncio.run(bot.send_message(
            chat_id=os.getenv('TELEGRAM_ADMIN_CHAT_ID'),
            text=message
        ))
        print('Bot token: ', bot_token)
        return Response(
            {
                'success': True,
                'message': 'Уведомление успешно отправлено',
                'wine': wine.full_name
            },
            status=status.HTTP_200_OK
        )
    
    except TelegramError as e:
        logger.error(f'Ошибка при отправке сообщения в Telegram: {e}')
        return Response(
            {'error': f'Ошибка при отправке сообщения в Telegram: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    except Exception as e:
        logger.error(f'Неожиданная ошибка: {e}')
        return Response(
            {'error': f'Внутренняя ошибка сервера: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

