#-*- coding: utf-8 -*-
from blogs.models import Blog
from django.contrib.auth.models import User
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import GenericViewSet
from users.permissions import UserPermissions
from users.serializers import UserSerializer
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status

class UserViewSet (GenericViewSet):

    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
    permission_classes = (UserPermissions,)

    # LIST => listado de usuarios.
    def list(self, request):
        """
        Endpoint de listado de usuarios. Los mostramos de forma paginada
        :param request:
        :return:
        """
        users = User.objects.all()
        self.paginate_queryset(users)
        serializer = UserSerializer(users, many=True)

        return self.get_paginated_response(serializer.data)


    # POST => Creación de nuevo usuario
    def create(self, request):
        """
        Endpoint de creación de usuario. Guardamos automáticamente también el blog con su nombre de usuario
        :param request:
        :return:
        """
        # Creamos serializador a partir de los datos de la petición. En rest framwork, para evitar request.POST,
        # request.GET, etc., se utiliza simplemente data
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            new_user = serializer.save()

            # Guardamos blog para el nuevo usuario
            user_blog = Blog()
            user_blog.owner = new_user
            user_blog.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    # GET => Obtenemos vista detalle de usuario
    def retrieve(self, request, pk):
        """
        Endpoint detalle de usuario
        :param request:
        :param pk:
        :return:
        """
        # Si existe el usuario cuya PK=pk existe lo devuelve, y si no se captura una excepción y se manda
        # un código 404
        # La función get_object_or_404 recibe el modelo como primer parámetro y a continuación los campos
        # de búsqueda
        user = get_object_or_404(User, pk=pk)

        # compruebo manualmente si el usuario autenticado puede hacer GET en este user
        self.check_object_permissions(request, user)

        # Convertimos objeto user en diccionario, que es guardado en 'data'
        serializer = UserSerializer(user)

        return Response(serializer.data)


    # PUT => Actualización de datos del usuario
    def update(self, request, pk):
        """
        Endpoint actualización usuario. Por convención, se utiliza la url de listado con una petición PUT para la
        modificación de un objeto de ese listado. En el serializer.save() comprueba automáticamente si tiene instancia
        del User; si la tiene, coge esa instancia y llama al update() del serializer; si no la tiene, llama al método
        create() del serializer, como en el caso del POST del UserListAPI
        :param request:
        :param pk:
        :return:
        """
        # Comprobamos si existe el usuario solicitado, o devolvemos un 404
        user = get_object_or_404(User, pk=pk)

        # compruebo manualmente si el usuario autenticado puede hacer PUT en este user
        self.check_object_permissions(request, user)

        # Actualiza los datos de la instancia recuperada con los datos que me pasan por la API
        serializer = UserSerializer(instance=user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    # DELETE => Eliminación del usuario
    def destroy(self, request, pk):
        """
        Endpoint de eliminación de usuario.  Por convención, se utiliza la url de listado con una petición DELETE para
        la eliminación de un objeto de ese listado.
        :param request:
        :param pk:
        :return:
        """
        # Obtenemos usuario a eliminar, y devolvemos error si no existe
        user = get_object_or_404(User, pk=pk)

        # compruebo manualmente si el usuario autenticado puede hacer PUT en este user
        self.check_object_permissions(request, user)

        # Eliminamos usuario de la DB
        user.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)