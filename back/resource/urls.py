from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import VideoViewSet

router = DefaultRouter()
router.register('videos', VideoViewSet, basename='skills')

urlpatterns = [
  path('', include(router.urls)),
]