from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'image','author', 'publish', 'status']  # Agrega 'image' aquí
    list_filter = ['status', 'created', 'publish', 'author']
    search_fields = ['title', 'body']
    raw_id_fields = ['author']
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']
    show_facets = admin.ShowFacets.ALWAYS
    fields = ['title', 'author', 'image', 'body', 'publish', 'status']  # Asegúrate de incluir 'image' en los campos editables
