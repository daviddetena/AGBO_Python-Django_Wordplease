#-*- coding: utf-8 -*-
from django.contrib.auth.models import User
from rest_framework import serializers

class UserSerializer(serializers.Serializer):
    """
    Clase serializador para los usuarios. Actúa de forma similiar a los Django Forms.
    Debemos definir los campos que quiero mandar/recibir del cliente.
    """
    id = serializers.ReadOnlyField()    # campo id es de sólo lectura (no se muestra hacia fuera)
    first_name = serializers.CharField(max_length=20)
    last_name = serializers.CharField(max_length=40)
    username = serializers.CharField(max_length=20)
    email = serializers.EmailField(max_length=40)
    password = serializers.CharField(max_length=15)

    def create(self, validated_data):
        """
        Crea una instancia de user a partir de los datos de validated_data, que contiene
        valores deserializados
        :param validated_data: Diccionario de datos de usuario
        :return: objeto User creado
        """
        instance = User()
        return self.update(instance, validated_data)

    def update(self, instance, validated_data):
        """
        Actualiza instancia de User a partir de los datos del diccionario validated_data, que
        contiene valores deserializados.
        :param instance: objeto User a actualizar
        :param validated_data: diccionario con nuevos valores para el User
        :return: objeto User actualizado
        """
        instance.first_name = validated_data.get("first_name")
        instance.last_name = validated_data.get("last_name")
        instance.username = validated_data.get("username")
        instance.email = validated_data.get("email")
        instance.set_password(validated_data.get("password"))   # encripta password introducido

        # Guardamos en db
        instance.save()

        # Devolvemos por json el nuevo objeto creado
        return instance

    def validate_username(self, data):
        """
        Valida si existe un usuario con ese username. Lanzamos excepción si ya existe. Actúa automágicamente como
        validador del campo username
        :param data: nombre de usuario a validar
        :return: nombre de usuario
        """
        users = User.objects.filter(username=data)

        # Si estoy creando (no instancia), comprobar si hay usuarios con ese username
        if not self.instance and len(users) > 0:
            raise serializers.ValidationError("Ya existe un usuario con ese nombre de usuario")
        # Si estoy actualizando, el nuevo username es diferente al de la instancia (cambia el username) y
        # existen usuarios ya registrados con el nuevo username
        elif self.instance and self.instance.username != data and len(users) > 0:
            raise serializers.ValidationError("Ya existe un usuario con ese nombre de usuario")
        else:
            # Actualiza manteniendo username o cambia a un username que no existe
            return data
