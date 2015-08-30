#-*- coding: utf-8 -*-
from datetime import date
from django.core.urlresolvers import reverse
from rest_framework import serializers
from blogs.models import Blog, Post

class BlogSerializer(serializers.ModelSerializer):
    """
    Clase serializador para el api de detalle de un blog
    """
    # Añadimos parámetros al return
    blog_url = serializers.SerializerMethodField('blogUrl')
    published_posts_count = serializers.SerializerMethodField('publishedPostsCount')

    class Meta:
        """
        Serializer basado en modelo Blog
        """
        model = Blog
        read_only_fields = ('owner',)
        fields = ('owner', 'blog_url', 'published_posts_count')

    def blogUrl(self, obj):
        """
        Método con el que obtenemos la url del blog, en este caso, a partir de la url nombrada blog_detail
        :param obj:
        :return:
        """
        return reverse('blog_detail', kwargs={'username': obj.owner.username})


    def publishedPostsCount(self, obj):
        """
        Con este método obtenemos el número de posts del usuario que han sido publicados
        :param obj:
        :return:
        """
        return len(Post.objects.filter(blog=obj, published_at__lte=date.today))



class PostSerializer(serializers.ModelSerializer):
    """
    Clase serializador para el api de detalle de un post
    """
    class Meta:
        """
        Serializer basado en modelo Post
        """
        model = Post
        read_only_fields = ('blog',)


class PostListSerializer(serializers.ModelSerializer):
    """
    Clase serializador para el api de listado de posts
    """
    class Meta:
        """
        # Definimos campos que se mostrarán en el resultado del API rest devuelto
        """
        model = Post
        fields = ('id', 'title', 'summary', 'image_url', 'published_at')




