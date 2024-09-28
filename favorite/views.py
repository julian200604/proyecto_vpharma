# favorite/views.py
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from .models import Favorite
from shop.models import Product  # Asegúrate de que Product esté correctamente importado desde la app correspondiente

# Vista de detalle del producto, incluyendo si está en favoritos
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(user=request.user, product=product).exists()
    
    # Asegúrate de definir `cart_product_form` si se usa en la plantilla
    # Por ejemplo, podrías crear un formulario aquí o pasar `None` si no es necesario
    cart_product_form = None  # Ajusta esto según sea necesario

    return render(request, 'shop/product/detail.html', {
        'product': product,
        'cart_product_form': cart_product_form,
        'is_favorite': is_favorite
    })

# Añadir producto a favoritos
@login_required
def add_to_favorites(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, product=product)
    
    if created:
        messages.success(request, f'El producto "{product.name}" ha sido añadido a tus favoritos.')
    else:
        messages.info(request, f'El producto "{product.name}" ya está en tus favoritos.')
        
    return redirect(request.META.get('HTTP_REFERER', 'home'))

# Eliminar producto de favoritos
@login_required
def remove_from_favorites(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Favorite.objects.filter(user=request.user, product=product).delete()
    return redirect(request.META.get('HTTP_REFERER', 'home'))

# lista producto de favoritos
@login_required
def favorite_list(request):
    favorites = Favorite.objects.filter(user=request.user)
    return render(request, 'favorite/favorite_list.html', {'favorites': favorites})
