# favorite/urls.py
from django.urls import path
from . import views

app_name = 'favorite'

urlpatterns = [
    path('product/<int:product_id>/add/', views.add_to_favorites, name='add_to_favorites'),
    path('product/<int:product_id>/remove/', views.remove_from_favorites, name='remove_from_favorites'),
    path('favorites/', views.favorite_list, name='favorite_list'),
]
