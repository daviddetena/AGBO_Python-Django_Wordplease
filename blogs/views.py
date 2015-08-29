# -*- coding: utf-8 -*-
from blogs.models import Blog
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def home(request):
    """
    Esta función devuelve el home de mi página
    :param request:
    :return:
    """
    blogs = Blog.objects.all()
    html = '<ul>'
    for blog in blogs:
        html+='<li>' + blog.owner.username + '</li>'
    html+= '</ul>'

    return HttpResponse(html)