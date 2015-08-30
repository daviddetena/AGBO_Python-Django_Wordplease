# -*- coding: utf-8 -*-
from datetime import date
from blogs.forms import PostForm
from blogs.models import Blog, Post
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from django.utils.decorators import method_decorator



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

        posts = queryset
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
            #'post_list': posts[:5],
            'unpublished_posts': None,
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

        possible_blogs = Blog.objects.filter(owner__username__exact=username)
        if len(possible_blogs) == 1:
            # Existe el blogs. Vemos si tiene posts
            possible_posts = self.get_posts_blog_queryset(request, username)

            if len(possible_posts) > 0:

                # Comprobamos publicados y no publicados
                if request.user.is_authenticated and (request.user.is_superuser or request.user.username == username):
                    published_posts = possible_posts.filter(published_at__lte=date.today).order_by('-published_at')
                    unpublished_posts = possible_posts.filter(published_at__gt=date.today).order_by('-created_at')
                else:
                    published_posts = possible_posts.filter(published_at__lte=date.today).order_by('-published_at')
                    unpublished_posts = None

                context = {
                    "post_list": published_posts,
                    "unpublished_posts": unpublished_posts
                }
                return render(request, 'blogs/blog_detail.html', context)
            else:
                # Sin posts
                context = {
                   "post_list": None
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


# url /new_post/
class CreateView(View):
    """
    Vista basada en clase para el la creación de post. Tendremos que definir los métodos del HTTP get y post.
    """
    @method_decorator(login_required())
    def get(self, request):
        """
        Muestra un formulario para crear un post. Este formulario no se manda nunca por get, por lo que no es
        necesario incluir mensajes de error.
        :param request: Objeto HttpRequest con la petición
        :return: HttpResponse
        """
        # Formulario vacío si viene por GET
        form = PostForm()

        context = {
            'form': form,
            'success_message': ''
        }

        return self.renderize(request, context)


    @method_decorator(login_required())
    def post(self, request):
        """
        Crea un post en base a la información POST. Con el decorador @login_required() nos va a ejecutar esta función
        solamente en el caso de que el usuario esté autenticado. En caso contrario, redirigirá a una url del paquete
        django.contrib.auth que redefinimos en el settings.py LOGIN_URL. Esta es la magia que hace Django para
        redireccionar al usuario a una url en el caso de que intente acceder a una url protegida sólo accesible si
        está autenticado.
        :param request: Objeto HttpRequest con la petición
        :return: HttpResponse
        """
        success_message = ''

        # Creo un post vacío y le asigno el blog actual.
        post_with_blog = Post()
        post_with_blog.blog = request.user.blog

        # Le pedimos al formulario que en vez de usar la instancia que él crea, utilice la que le
        # indicamos con el post_with_blog. Con esto, guarda la instancia con todos los campos del
        # formulario, excepto del blog, que coge el que le indicamos nosotros que ha sido creado.
        form = PostForm(request.POST, instance=post_with_blog)

        if form.is_valid():
            # Si se valida correctamente creamos objeto post, lo guardamos en DB y lo devolvemos
            # Obtenemos el blog del usuario autenticado para guardarlo automáticamente.
            new_post = form.save()

            # Reiniciamos formulario y componemos mensaje con enlace al nuevo post creado. Para acceder a una url
            # nombrada en un controlador utilizamos la función reverse, con los argumentos de la url nombrada, en este
            # caso, el nombre del blog, y la pk del post.
            # Como por defecto Django escapa el HTML, necesitamos indicar que el enlace al nuevo post no escape HTML.
            # Lo indicamos en la plantilla con el |safe en el mensaje. Lo normal es que este trabajo se haga en el
            # template
            form = PostForm()
            success_message = '¡Post creado con éxito!  '
            success_message += '<a href="{0}">'.format(reverse('post_detail', args=[new_post.blog, new_post.pk]))
            success_message += 'Ver post'
            success_message += '</a>'

        context = {
            'form': form,
            'success_message': success_message
        }

        return self.renderize(request, context)


    def renderize(self, request, context):
        """
        Cargamos template con los datos del contexto, que incluye el formulario basado en modelo
        En el template podemos incluir cada campo como <p>, <tr> de table o <li> de <ul>
        :param request: HttpRequest
        :param context: Contexto con los datos a los que el template tendrá acceso
        :return: render que genera el HttpResponse con el context y el template indicados
        """
        return render(request, 'blogs/post_create.html', context)