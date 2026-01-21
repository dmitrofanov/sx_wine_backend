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
from .telegram import send_message, BotTokenIsNotSetError

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
    
    Отправляет администратору сообщение в Telegram.
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
    
    # Формируем сообщение
    message = f"Пользователь {person.nickname} интересуется вином {wine.full_name}"

    try:
        send_message(message)
        return Response(
            {
                'success': True,
                'message': 'Уведомление успешно отправлено',
                'wine': wine.full_name
            },
            status=status.HTTP_200_OK
        )
    except BotTokenIsNotSetError as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    except TelegramError as e:
        return Response(
            {'error': f'Ошибка при отправке сообщения в Telegram: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    except Exception as e:
        return Response(
            {'error': f'Внутренняя ошибка сервера: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
def send_event_interest_notification(request):
    """
    Endpoint для отправки уведомления о заинтересованности событием в Telegram.
    
    Принимает:
    - nickname: никнейм пользователя (Person)
    - event_id: Primary Key события (Event)
    
    Отправляет администратору сообщение в Telegram.
    """
    nickname = request.data.get('nickname')
    event_id = request.data.get('event_id')
    
    # Валидация входных данных
    if not nickname:
        return Response(
            {'error': 'Параметр nickname обязателен'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if not event_id:
        return Response(
            {'error': 'Параметр event_id обязателен'},
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
        event = Event.objects.get(pk=event_id)
    except Event.DoesNotExist:
        return Response(
            {'error': f'Событие с ID {event_id} не найдено'},
            status=status.HTTP_404_NOT_FOUND
        )

    message = f"Пользователь {person.nickname} интересуется событием {event.name}"
    
    try:
        send_message(message)
        return Response(
            {
                'success': True,
                'message': 'Уведомление успешно отправлено',
                'event': event.name
            },
            status=status.HTTP_200_OK
        )
    except BotTokenIsNotSetError as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    except TelegramError as e:
        return Response(
            {'error': f'Ошибка при отправке сообщения в Telegram: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    except Exception as e:
        return Response(
            {'error': f'Внутренняя ошибка сервера: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
