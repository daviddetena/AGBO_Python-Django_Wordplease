# -*- coding: utf-8 -*-
from blogs.models import Blog, Post, Category
from django.contrib import admin

class BlogAdmin(admin.ModelAdmin):
    """
    Personalizamos cómo se muestra el modelo Blog en nuestro admin de Django
    """
    # Lista de columnas que se verán en el admin. Para el blog llamamos a método que me devuelve el nombre y apellidos del usuario propietario del blog
    list_display = ('owner', 'blog_owner_name', 'created_at', 'modified_at')


    def blog_owner_name(self, obj):
        """
        Método que altera el campo list_display blog para poner el nombre y apellidos del propietario del blog
        :param obj:
        :return:
        """
        return obj.owner.first_name + u' ' + obj.owner.last_name

    # Atributos a métodos de función blog_owner_name, para poder indicar el header de columna y el campo correspondiente por el que ordena
    blog_owner_name.short_description = u'Owner name'
    blog_owner_name.admin_order_field = 'owner'



class PostAdmin(admin.ModelAdmin):
    """
    Personalizamos cómo se muestra el modelo Post en nuestro admin de Django
    """
    # Lista de columnas que se verán en el admin. Para el blog llamamos a método que me devuelve el nombre y apellidos del usuario propietario del blog
    list_display = ('title', 'summary', 'blog', 'blog_owner_name', 'created_at', 'published_at')

    # Lista de filtros que aparecerán a la derecha
    list_filter = ('blog', 'categories')

    # Lista de parámetros por los que se podrá buscar
    search_fields = ('title', 'summary', 'body')


    def blog_owner_name(self, obj):
        """
        Método que altera el campo list_display blog para poner el nombre y apellidos del propietario del blog del post
        :param obj:
        :return:
        """
        return obj.blog.owner.first_name + u' ' + obj.blog.owner.last_name

    # Atributos a métodos de función blog_owner_name, para poder indicar el header de columna y el campo correspondiente por el que ordena
    blog_owner_name.short_description = u'Blog owner'
    blog_owner_name.admin_order_field = 'blog'


    # Definimos campos que aparecen en la vista detalle del Post en el admin
    fieldsets = (
        ('General', {
            'fields': ('title', 'summary', 'body'),
            'classes': ('wide',)
        }),
        ('Addional info',{
            'fields': ('image_url', 'blog', 'categories', 'published_at'),
            'classes': ('wide',)
        })
    )

# Registramos modelo Blog
admin.site.register(Blog, BlogAdmin)

# Registramos modelo Post, cuyo admin personalizado es gestionado por nuestra clase PostAdmin
admin.site.register(Post, PostAdmin)
admin.site.register(Category)
