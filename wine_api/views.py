from rest_framework import viewsets
from .models import Wine, Event
from .serializers import WineSerializer, EventSerializer


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
    queryset = Event.objects.all()
    serializer_class = EventSerializer

