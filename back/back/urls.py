"""
URL configuration for back project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from account.views import UserAPIView, CurrentUserView
from skill.views import get_skills_for_profession
from resource.views import load_videos_by_skill 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/users/', UserAPIView.as_view(), name='user-list'),
    path('api/user/current/', CurrentUserView.as_view(), name='current-user'),
    path('api/skill/<str:search>', get_skills_for_profession, name='skills'),
    path('api/videos/<str:skill_name>', load_videos_by_skill, name='load_videos'),
    path('api/', include('like.urls')),
]
