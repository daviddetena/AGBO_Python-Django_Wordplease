#-*- coding: utf-8 -*-
__author__ = 'daviddetena'

# -*- coding: utf-8 -*-
from django.conf.urls import url
from blogs.views import HomeView, BlogListView, BlogDetailView, PostDetailView, CreateView

urlpatterns = [
    # Blogs URLs
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^blogs/$', BlogListView.as_view(), name='blog_list'),
    url(r'^blogs/(?P<username>[a-z]+)$', BlogDetailView.as_view(), name='blog_detail'),
    url(r'^blogs/(?P<username>[a-z]+)/(?P<pk>[0-9]+)', PostDetailView.as_view(), name='post_detail'),
    url(r'^new-post/$', CreateView.as_view(), name='post_create'),
]
