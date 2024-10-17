from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    cart.add(product=product, quantity=quantity)
    
    return JsonResponse({'success': True, 'message': 'Producto añadido al carrito'})

@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')

def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'], 'override': True})
    return render(request, 'cart/detail.html', {'cart': cart, 'is_cart_detail': True})

@require_POST
def cart_update(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)

    if request.content_type == 'application/json':
        import json
        data = json.loads(request.body)
        quantity = int(data.get('quantity', 1))
    else:
        quantity = int(request.POST.get('quantity', 1))

    cart.add(product=product, quantity=quantity, override_quantity=True)
    
    # Calcular el nuevo total del carrito
    total = cart.get_total_price()  # Asegúrate de que este método esté definido

    return JsonResponse({'success': True, 'total': total})