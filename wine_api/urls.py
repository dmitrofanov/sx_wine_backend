from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    WineViewSet,
    EventViewSet,
    PersonViewSet,
    send_wine_interest_notification,
    send_event_interest_notification,
    bind_telegram_id,
)

router = DefaultRouter()
router.register(r'wines', WineViewSet, basename='wine')
router.register(r'events', EventViewSet, basename='event')
router.register(r'persons', PersonViewSet, basename='person')

urlpatterns = [
    path('', include(router.urls)),
    path('notifications/wine-interest/', send_wine_interest_notification, name='wine-interest-notification'),
    path('notifications/event-interest/', send_event_interest_notification, name='event-interest-notification'),
    path('auth/bind-telegram/', bind_telegram_id, name='bind-telegram-id'),
]

