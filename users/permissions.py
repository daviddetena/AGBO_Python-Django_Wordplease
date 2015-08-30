#-*- coding: utf-8 -*-
from rest_framework.permissions import BasePermission

class UserPermissions(BasePermission):

    def has_permission(self, request, view):
        """
        Define si el usuario autenticado en request.user tiene permiso para realizar la acción
        GET, PUT, POST, DELETE
        :param request:
        :param view:
        :return:
        """
        from users.api import UserDetailAPI

        # si se quiere crear un nuevo usuario, sea quien sea puede
        if request.method == "POST":
            return True
        # si no es POST,super admin siempre puede
        elif request.user.is_superuser:
            return True
        # si es un GET a la vista de detalle, tomo la decisión en has_object_permissions
        elif isinstance(view, UserDetailAPI):
            return True
        else:
            # GET a /api/1.0/users/
            return False


    def has_object_permission(self, request, view, obj):
        """
        Define si el usuario autenticado en request.user tiene permiso para realizar la acción
        GET, PUT, POST, DELETE sobre el objeto obj
        :param request:
        :param view:
        :param obj:
        :return:
        """
        # Si es superadmin, o el usuario autenticado intenta hacer GET, PUT o DELETE sobre su mismo perfil
        return request.user.is_superuser or request.user == obj