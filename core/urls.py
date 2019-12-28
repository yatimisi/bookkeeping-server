"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from app.users.views import UserViewSet

from core.settings import MEDIA_ROOT, MEDIA_URL

from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from rest_framework import routers

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


router = routers.DefaultRouter()
router.trailing_slash = ''
router.register('users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('token', TokenObtainPairView.as_view(), name='token-create'),
    path('token/refresh', TokenRefreshView.as_view(), name='token-refresh'),

    path('admin/', admin.site.urls),
    *static(MEDIA_URL, document_root=MEDIA_ROOT),
]
