# -*- coding: utf-8 -*-
from blogs.models import Blog, Post
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def home(request):
    """
    Esta función devuelve el home de mi página
    :param request:
    :return:
    """
    posts = Post.objects.all().order_by('-published_at')
    context = {
        'post_list': posts[:6]
    }
    return render(request, 'blogs/home.html', context)