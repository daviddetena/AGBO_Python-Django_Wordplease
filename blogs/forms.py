#-*- coding: utf-8 -*-
from django import forms
from blogs.models import Post


class PostForm(forms.ModelForm):
    """
    Heredamos de ModelForm para que genere un formulario automágicamente a partir de nuestro modelo Post
    """

    class Meta:
        """
        En la clase meta definimos el modelo base para crear el formulario. Podemos indicarle también los
        campos que queremos que aparezcan en el formulario (fields), y los que no (exclude)
        """
        # Formulario para el modelo Post, excluyendo campo "blog" para que coja el del usuario autenticado automáticamente
        model = Post
        exclude = ['blog']