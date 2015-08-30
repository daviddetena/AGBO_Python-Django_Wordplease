#-*- coding: utf-8 -*-
from rest_framework.permissions import BasePermission
from datetime import date


class PostPermission(BasePermission):
    """
    Clase de permisos para el modelo Post
    """
    def has_permission(self, request, view):
        """
        Define si el usuario autenticado en request.user tiene
        permiso para realizar la acción (GET, POST, PUT o DELETE)
        """
        # Admin puede hacer lo que quiera
        if request.user.is_superuser:
            return True
        # cualquiera puede hacer un GET, el contenido recibido se decidirá en has_object_permission
        elif view.action in ['retrieve', 'list']:
            return True
        # sólo usuarios autenticados podrán, pero has_object_permissions decidirá sobre el permiso final
        elif view.action in ['create', 'update', 'destroy']:
            return request.user.is_authenticated()
        # por defecto no se da permiso
        else:
            # GET a /api/1.0/users/
            return False

    def has_object_permission(self, request, view, obj):
        """
        Define si el usuario autenticado en request.user tiene
        permiso para realizar la acción (GET, PUT o DELETE)
        sobre el object obj
        """
        # Superadmin => puede hacer lo que quiera
        if request.user.is_superuser:
            return True
        # Si soy el dueño del post, podré operar con él
        elif view.action in ['create', 'update', 'destroy']:
            return request.user == obj.blog.owner
        # Se podrá leer un post (o listado de ellos) si es público o el usuario autenticado es el dueño
        elif view.action in ['retrieve', 'list']:
            return obj.published_at <= date.today() or request.user == obj.blog.owner
        # si no cumple nada de lo anterior
        else:
            False
