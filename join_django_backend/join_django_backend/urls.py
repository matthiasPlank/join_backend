"""
URL configuration for join_django_backend project.

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
from login.views import CustomAuthToken, register_view , check_token_view 
from tasks import views as tasks_views
from login import views as login_views

from django.contrib import admin
from django.urls import include, path

from rest_framework import routers
from django.views.decorators.csrf import csrf_exempt, csrf_protect

from django.contrib.auth import views as auth_views
from django.urls import path, include


router = routers.DefaultRouter()
router.register(r'api/tasks', tasks_views.TaskViewSet)
router.register(r'api/contacts', tasks_views.ContactViewSet)
router.register(r'api/users', login_views.UserViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api/api-token-auth/', CustomAuthToken.as_view()),
    path('api/register/', csrf_exempt(register_view)),
    path('api/checkToken/', csrf_exempt(check_token_view)),
]
