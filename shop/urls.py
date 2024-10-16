from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


app_name = 'shop'

urlpatterns = [
    path('cart/', views.cart, name='cart'),
    path('ayuda/', views.ayuda, name='ayuda'),
    path('quienes_somos/', views.quienes_somos, name='quienes_somos'),
    path('politica_privacidad/', views.politica_privacidad, name='politica_privacidad'),
    path('terminos_condiciones/', views.terminos_condiciones, name='terminos_condiciones'),
    path('tyc/', views.tyc, name='tyc'),
    path('blog/', views.blog, name='blog'),
    path('', views.product_list, name='product_list'),
    path('<slug:category_slug>/', views.product_list,name='product_list_by_category'),
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
    path('search/', views.search_products, name='search_products'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
   



   



