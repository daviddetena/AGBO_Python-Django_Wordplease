#-*- coding: utf-8 -*-
from blogs.models import Blog
from django.contrib.auth.models import User
from rest_framework.generics import GenericAPIView
from rest_framework.pagination import PageNumberPagination
from users.permissions import UserPermissions
from users.serializers import UserSerializer
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status

class UserListAPI(GenericAPIView):
    """
    Vista basada en clase para el listado de Users de la API Rest. En este caso, sólo se accede por GET.
    Las APIView nos proporciona un API rest navegable.
    """
    # Clase de paginación
    pagination_class = PageNumberPagination

    # Tupla de permisos
    permission_classes = (UserPermissions,)

    # Clase de serializador
    serializer_class = UserSerializer

    def get(self, request):
        """
        Endpoint de listado de usuarios. Devuelve en formato JSON una lista de diccionarios con los datos de cada usuario.
        :param request:
        :return:
        """
        users = User.objects.all()      # Obtenemos todos los usuarios

        self.paginate_queryset(users)   # Paginamos el resultado del queryset de users de forma manual

        # El serializador por defecto serializa un objeto. Tenemos que indicarle que serialice
        # todos los usuarios recibidos, poniendo many=True.
        # El serializador se guarda los datos en data
        serializer = UserSerializer(users, many=True)

        # Devolvemos respuesta paginada
        return self.get_paginated_response(serializer.data)

    def post(self, request):
        """
        Endpoint de creación de usuario. Por convención, se utiliza la url de listado con una petición POST para la creación de un objeto de ese listado. En el serializer.save() comprueba automáticamente si tiene instancia del User; si no la tiene, llama al método create del serializer.
        """

        # Creamos serializador a partir de los datos de la petición. En rest framwork, para evitar request.POST, request.GET, etc., se utiliza simplemente data
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            # Guardamos el usuario a través del serializer y devolvemos los datos del objeto creado
            new_user = serializer.save()

            # Guardamos blog para el nuevo usuario
            user_blog = Blog()
            user_blog.owner = new_user
            user_blog.save()

            # Respondemos código 201 (creado) y los datos del objeto creado
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            # Devolvemos diccionario con errores y el código 400 (petición errónea) si algo fue mal
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailAPI(GenericAPIView):
    """
    Vista basada en clase para el detalle de User.
    """
    # Clase de serializador
    serializer_class = UserSerializer

    permission_classes = (UserPermissions,)

    def get(self, request, pk):
        """
        Endpoint detalle de usuario
        :param request:
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

    def put(self, request, pk):
        """
        Endpoint de modificación de usuario. Por convención, se utiliza la url de listado con una petición PUT para la modificación de un objeto de ese listado. En el serializer.save() comprueba automáticamente si tiene instancia del User; si la tiene, coge esa instancia y llama al update() del serializer; si no la tiene, llama al método create() del serializer, como en el caso del POST del UserListAPI
        """
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

    def delete(self, request, pk):
        """
        Endpoint de modificación de usuario. Por convención, se utiliza la url de listado con una petición DELETE para la eliminación de un objeto de ese listado.
        """
        # Obtenemos usuario a eliminar, y devolvemos error si no existe
        user = get_object_or_404(User, pk=pk)

        # compruebo manualmente si el usuario autenticado puede hacer PUT en este user
        self.check_object_permissions(request, user)

        # Eliminamos usuario de la DB
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)