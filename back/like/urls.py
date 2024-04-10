from django.urls import path
from .views import LikeViewSet

urlpatterns = [
  path('likes/', LikeViewSet.as_view({'get': 'list', 'post': 'create'})),
  path('likes/<int:pk>/', LikeViewSet.as_view({'get': 'retrieve', 'delete': 'destroy'})),
]