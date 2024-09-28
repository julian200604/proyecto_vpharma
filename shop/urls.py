from django.urls import path
from . import views


app_name = 'shop'

urlpatterns = [

    path('ayuda/', views.ayuda, name='ayuda'),

    path('quienes_somos/', views.quienes_somos, name='quienes_somos'),

    path('politica_privacidad/', views.politica_privacidad, name='politica_privacidad'),

    path('tyc/', views.tyc, name='tyc'),
    
    path('blog/', views.blog, name='blog'),


    path('', views.product_list, name='product_list'),
    path(
        '<slug:category_slug>/',
        views.product_list,
        name='product_list_by_category'
    ),
    path(
        '<int:id>/<slug:slug>/',
        views.product_detail,
        name='product_detail'
    ),
]

