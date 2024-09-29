from django.shortcuts import get_object_or_404, render
from django.db.models import Q
from cart.forms import CartAddProductForm
from .models import Category, Product
from django.http import HttpResponse
from django.utils import timezone

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    cart_product_form = CartAddProductForm()
    search_query = request.GET.get('q', '') # Busqueda 

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    if search_query:# Busqueda
        products = products.filter(
            Q(name__icontains=search_query) | Q(description__icontains=search_query)
        )

    no_products = not products and search_query # Busqueda

    return render(
        request,
        'shop/product/list.html',
        {
            'category': category,
            'categories': categories,
            'products': products,
            'cart_product_form': cart_product_form,  
        },
    )

def cart(request):
    return render(request, 'cart/detail.html')

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

# Vista para buscar productos
def search_products(request):
    query = request.GET.get('q', '')  # Obtener la consulta de búsqueda del usuario
    results = Product.objects.filter(name__icontains=query, available=True)  # Filtrar productos disponibles por nombre
    return render(request, 'shop/search_results.html', {'products': results, 'query': query})

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



   