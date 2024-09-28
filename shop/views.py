from django.shortcuts import get_object_or_404, render

from cart.forms import CartAddProductForm
from .models import Category, Product
from django.http import HttpResponse



def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    cart_product_form = CartAddProductForm()  # Agregar el formulario aquí
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(
        request,
        'shop/product/list.html',
        {
            'category': category,
            'categories': categories,
            'products': products,
            'cart_product_form': cart_product_form,  # Pasar el formulario al contexto
        },
    )


def product_detail(request, id, slug):
    product = get_object_or_404(
        Product, id=id, slug=slug, available=True
    )
    cart_product_form = CartAddProductForm()
    return render(
        request,
        'shop/product/detail.html',
        {'product': product, 'cart_product_form': cart_product_form},
    )

def ayuda(request):
    return render(request, 'info/ayuda.html')

def quienes_somos(request):
    return render(request, 'info/quienes_somos.html')

def politica_privacidad(request):
    return render(request, 'info/politica_privacidad.html')

def tyc(request):
    return render(request, 'info/terminos_condiciones.html')

def blog(request):
    return render(request, 'info/blog.html')



   