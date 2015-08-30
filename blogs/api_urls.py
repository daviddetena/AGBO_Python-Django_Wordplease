#-*- coding: utf-8 -*-
__author__ = 'daviddetena'

from django.conf.urls import include, url
from blogs.api import BlogsViewSet, PostsViewSet
from rest_framework.routers import DefaultRouter


# APIRouter
router = DefaultRouter()
router.register(r'blogs', BlogsViewSet)
router.register(r'posts', PostsViewSet)

"""
router.register(r'blogs/(?P<username>[a-z]+)', PostViewSet)
#router.register(r'blogs/new-post/', CreatePostViewSet)
"""


urlpatterns = [
    # API URLs
    url(r'^1.0/', include(router.urls)),  # incluyo las URLS de API
]