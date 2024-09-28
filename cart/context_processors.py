from .cart import Cart

def cart(request):
    """
    Este context processor devuelve el carrito y además si está vacío 
    y la cantidad total de productos en el carrito.
    """
    cart = Cart(request)
    
    # Verificar si el carrito está vacío
    carrito_vacio = len(cart) == 0
    
    # Devolver el carrito, si está vacío y el total de productos en el carrito
    return {
        'cart': cart,
        'carrito_vacio': carrito_vacio,  # Si el carrito está vacío o no
        'total_items': len(cart),  # Cantidad de productos en el carrito
    }

