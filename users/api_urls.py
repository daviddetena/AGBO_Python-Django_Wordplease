#-*- coding: utf-8 -*-
__author__ = 'daviddetena'

from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter
from users.api import UserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, base_name='user')

urlpatterns = [
    # Incluimos las URLs de la API
    url(r'1.0/', include(router.urls)),
]
