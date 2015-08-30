# -*- coding: utf-8 -*-
"""wordplease URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from blogs.views import HomeView, BlogListView, BlogDetailView, PostDetailView
from django.conf.urls import include, url
from django.contrib import admin
from users.views import LoginView, LogoutView, SignupView

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),


    # Users' URLs
    url(r'^signup/$', SignupView.as_view(), name='user_signup'), # signup o creación de cuenta de usuario, con vista basada en clase SignupView
    url(r'^login$', LoginView.as_view(), name='user_login'),    # login, con vista basada en clase LoginView
    url(r'^logout$', LogoutView.as_view(), name='user_logout'), # logout, con vista basada en clase LogoutView


    # Blogs URLs
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^blogs/$', BlogListView.as_view(), name='blog_list'),
    url(r'^blogs/(?P<username>[a-z]+)$', BlogDetailView.as_view(), name='blog_detail'),
    url(r'^blogs/(?P<username>[a-z]+)/(?P<pk>[0-9]+)', PostDetailView.as_view(), name='post_detail'),
]
