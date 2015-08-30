# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models
from datetime import date


class Category(models.Model):
    """
    Definimos modelo Category. Varios posts pueden estar en una misma categoría, y un mismo post tener varias
    categorías.
    """
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return u'%s' % self.name

class Blog(models.Model):
    """
    Definimos modelo Blog. Un blog por usuario. Cada blog de usuario tendrá n posts
    """
    # Un blog por usuario
    owner = models.OneToOneField(User)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return u'%s' % self.owner.username


class Post(models.Model):
    """
    Definimos el modelo Post. Como cada usuario tendrá un único blog en principio, hacemos que el usuario del post sea
    el usuario autenticado.
    """
    blog = models.ForeignKey(Blog)                                      # El blog es FK. Es un 1-n (1 blog - n posts)
    title = models.CharField(max_length=100)
    summary = models.CharField(max_length=300)
    body = models.TextField()
    image_url = models.URLField(blank=True, null=True, default="")      # Imagen url opcional
    created_at = models.DateTimeField(auto_now_add=True)                # Se guarda la fecha al crearse
    modified_at = models.DateTimeField(auto_now=True)                   # Se actualiza cada vez que se guarde
    published_at = models.DateField(default=date.today)                 # Por defecto se publica con la fecha del día
    categories = models.ManyToManyField(Category, blank=True, null=True)

    def __unicode__(self):
        return u'%s' % self.title