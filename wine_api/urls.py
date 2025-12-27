from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WineViewSet, EventViewSet, PersonViewSet

router = DefaultRouter()
router.register(r'wines', WineViewSet, basename='wine')
router.register(r'events', EventViewSet, basename='event')
router.register(r'persons', PersonViewSet, basename='person')

urlpatterns = [
    path('', include(router.urls)),
]

