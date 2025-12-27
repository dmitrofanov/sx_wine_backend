from datetime import date

from rest_framework import viewsets

from .models import Wine, Event, Person
from .serializers import WineSerializer, EventSerializer, PersonSerializer


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

