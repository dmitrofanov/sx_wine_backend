from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WineViewSet, EventViewSet

router = DefaultRouter()
router.register(r'wines', WineViewSet, basename='wine')
router.register(r'events', EventViewSet, basename='event')

urlpatterns = [
    path('', include(router.urls)),
]

