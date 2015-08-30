#-*- coding: utf-8 -*-
from rest_framework.pagination import PageNumberPagination
from blogs.models import Blog, Post
from blogs.permissions import PostPermission
from blogs.serializers import BlogSerializer, PostListSerializer, PostSerializer
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from blogs.views import PostsQuerySet


class BlogsViewSet(ReadOnlyModelViewSet):
    """
    Definimos el ViewSet para el API de blog
    """
    queryset = Blog.objects.all()

    def get_serializer_class(self):
        return BlogSerializer



class PostsViewSet(PostsQuerySet, ModelViewSet):
    """
    Definimos el ViewSet para el API de Post.
    """
    queryset = Post.objects.all()
    pagination_class = PageNumberPagination
    permission_classes = (PostPermission,)

    def get_queryset(self):
        return self.get_posts_queryset(self.request)

    def get_serializer_class(self):
        if self.action == 'list':
            return PostListSerializer
        else:
            return PostSerializer


    def perform_create(self, serializer):
        """
        Este método se ejecuta automáticamente tras crearse la nueva instancia del objeto.
        En nuestro caso, queremos que se guarde automáticamente en el nuevo post el blog al que pertenece, que será el del usuario autenticado
        :param serializer:
        :return:
        """
        #obtener blog del usuario y asignarlo
        user_blog = Blog.objects.get(owner=self.request.user)
        serializer.save(blog=user_blog)