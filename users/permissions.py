#-*- coding: utf-8 -*-
from rest_framework.permissions import BasePermission

class UserPermissions(BasePermission):

    def has_permission(self, request, view):
        """
        Define si el usuario autenticado en request.user tiene permiso para realizar la acción
        (GET, POST, PUT o DELETE)
        :param request:
        :param view:
        :return:
        """

        # POST => se puede crear un usuario siempre
        if view.action == "create":
            return True
        # Superadmin => puede hacer todas las operaciones
        elif request.user.is_superuser:
            return True
        # si es un GET, PUT o DELETE se decide en has_object_permissions
        elif view.action in ['retrieve', 'update', 'destroy']:
            return True
        # por defecto no damos permiso
        else:
            # GET a /api/1.0/users/
            return False


    def has_object_permission(self, request, view, obj):
        """
        Define si el usuario autenticado en request.user tiene permiso para realizar la acción
        (GET, PUT o DELETE)sobre el object obj
        :param request:
        :param view:
        :param obj:
        :return:
        """

        # Sólo damos permiso si es superadmin o si es el usuario autenticado el que intenta hacer
        # GET, PUT o DELETE sobre su mismo perfil
        return request.user.is_superuser or request.user == obj