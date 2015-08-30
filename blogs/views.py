# -*- coding: utf-8 -*-
from datetime import date
from blogs.models import Blog, Post
from django.db.models import Q
from django.views.generic import View
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render


class PostsQuerySet(object):

    def get_home_posts_queryset(self):
        """
        Obtenemos todos los artículos publicados
        :param request:
        :return:
        """
        posts = Post.objects.filter(published_at__lte=date.today).order_by('-published_at')
        return posts


    def get_posts_queryset(self, request):
        """
        Recuperamos listado de posts según el siguiente criterio:
        :param request: HttpRequest
        :return:
        """

        if not request.user.is_authenticated():
            # Si no está autenticado => TODOS los PUBLICADOS
            posts = Post.objects.filter(published_at__lte=date.today)
        elif request.user.is_superuser:
            # Admin => TODOS los posts
            posts = Post.objects.all()
        else:
            # No es admin y está autenticado => TODOS los de ese usuario, publicados o no, y los PUBLICOS del resto
            posts = Post.objects.filter(Q(blog__owner__username=request.user.username) | Q(published_at__lte=date.today))

        # Ordenamos resultados por fecha de publicación, o de creación
        return posts.order_by('-published_at', '-created_at')


    def get_posts_blog_queryset(self, request, username):
        """
        Recuperamos los posts de un blog concreto:
        - Si el usuario autenticado es el dueño del blog, o es administrador, verá todos los posts de ese usuario,
        publicados o no.
        - Si el usuario no está autenticado, o no es el dueño, sólo verá los públicos de ese usuario
        :param request:
        :param username:
        :return:
        """
        queryset = Post.objects.filter(blog__owner__username=username)

        if request.user.is_superuser or (request.user.is_authenticated and request.user.username == username):
            posts = queryset
        else:
            posts = queryset.filter(published_at__lte=date.today)

        return posts


    def get_post_detail_queryset(self, request, username, pk):
        """
        Definimos queryset para el detalle de post. Llamamos al método anterior, para que filtre por pk.
        """
        posts = self.get_posts_queryset(request).filter(pk=pk).select_related('blog')

        if len(posts) == 1:
            return posts[0]
        else:
            return None


class HomeView(View, PostsQuerySet):

    def get(self, request):
        """
        Vista home de la plataforma. Muestra los últimos 5 posts publicados.
        :param request: HttpRequest
        :return: render con HttpResponse
        """
        posts = self.get_home_posts_queryset()
        context = {
            #'post_list': posts[:5]
            'post_list': posts
        }
        return render(request, 'blogs/home.html', context)



class BlogListView(View):

    def get(self, request):
        """
        Muestra el listado de blogs de la plataforma
        :param request: HttpRequest
        :return: HttpResponse
        """
        blogs = Blog.objects.order_by('-created_at')
        if len(blogs) > 0:
            context = {
                'blog_list': blogs,
            }
        else:
            context = {
                'blog_list': None,
            }

        return render(request, 'blogs/blog_list.html', context)


class BlogDetailView(View, PostsQuerySet):

    def get(self, request, username):
        """
        Muestra los posts de un blog, es decir, la vista de detalle de un blog a partir de la url blogs/<nombre_usuario>, según el siguiente criterio:
        - Si no está autenticado => TODOS los PUBLICADOS
        - Admin => TODOS los posts
        - No es admin y está autenticado => TODOS los de ese usuario, publicados o no, y los PUBLICOS del resto
        :param request: HttpRequest
        :param username: nombre del blog cuyos posts se quieren ver
        :return: HttpResponse
        """
        possible_posts = self.get_posts_blog_queryset(request, username)
        if len(possible_posts) > 0:
            context = {
                "post_list": possible_posts
            }
            return render(request, 'blogs/blog_detail.html', context)
        else:
            # 404 - blog no encontrado
            return HttpResponseNotFound('No existe el blog')



class PostDetailView(View, PostsQuerySet):
    """
    Vista basada en clase para el detalle de post. Tendremos que definir los métodos del HTTP get y post.
    En este caso, es sólo por GET
    """
    def get(self, request, username, pk):
        """
        Método para manejar la vista detalle de un post.
        :param request: Objeto request con la petición
        :param pk: Parámetro pk con el identificador del blog cuyo detalle se mostrará
        :return: render que cargará la vista de detalle del post (por debajo, crea un HttpResponse)
        """

        # Obtenemos queryset del detalle de post
        possible_post = self.get_post_detail_queryset(self.request, username, pk)
        if possible_post is not None:
            context = {
                "post": possible_post
            }
            # cargamos template con los datos del contexto, que incluye el post a mostrar
            return render(request, 'blogs/post_detail.html', context)

        else:
            # error 404 - post no encontrado
            return HttpResponseNotFound('No existe el post')
