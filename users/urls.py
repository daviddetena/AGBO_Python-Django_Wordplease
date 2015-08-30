#-*- coding: utf-8 -*-
__author__ = 'daviddetena'

from django.conf.urls import url
from users.views import LoginView, LogoutView, SignupView

urlpatterns = [
    # Users' URLs
    url(r'^signup/$', SignupView.as_view(), name='user_signup'),
    url(r'^login$', LoginView.as_view(), name='user_login'),
    url(r'^logout$', LogoutView.as_view(), name='user_logout'),
]