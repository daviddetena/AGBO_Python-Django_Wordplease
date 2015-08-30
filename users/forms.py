#-*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class LoginForm(forms.Form):
    """
    Definimos nuestra clase LoginForm para crear un formulario de Django con los campos que le indicamos
    """
    # campos, siempre tienen que heredar de XXXField
    # Con widget indicamos de qué tipo queremos que pinte el campo
    usr = forms.CharField(label="Nombre de usuario", max_length=20)
    pwd = forms.CharField(label="Contraseña", max_length=15, widget=forms.PasswordInput())

"""
class SignupForm(forms.Form):

    first_name = forms.CharField(label="Nombre", max_length=20)
    last_name = forms.CharField(label="Apellidos", max_length=40)
    username = forms.CharField(label="Nombre de usuario", max_length=20)
    email = forms.EmailField(max_length=40)
    password = forms.CharField(label="Contraseña", max_length=15, widget=forms.PasswordInput())
    """

class SignupForm(forms.ModelForm):
    """
    Heredamos de ModelForm para que genere un formulario automágicamente a partir del modelo User
    """

    class Meta:
        """
        Definimos modelo base para crear el formulario. Incluimos sólo los campos que queremos
        """
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']
        widgets = {'password': forms.PasswordInput}


    def clean(self):
        """
        Valida y limpia los datos del formulario
        :return:
        """
        cleaned_data = super(SignupForm, self).clean()

        # Comprobamos que no exista el usuario introducido
        username = cleaned_data.get('username')

        users = User.objects.filter(username=username)
        if len(users) != 0:
            raise ValidationError(u'Ya existe un usuario con ese nombre de usuario')
        else:
            return cleaned_data

