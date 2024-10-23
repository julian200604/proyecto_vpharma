from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'first_name',
        'last_name',
        'address',
        'neighborhood',
        'phone_number',
        'payment_method',
        'is_paid',  
        'status',  # Agregar el estado del pedido aquí
        'created',
        'paid'
    ]
    list_filter = ['paid', 'created', 'status', 'payment_method']  # Agregar filtro por estado
    inlines = [OrderItemInline]

    # Método para mostrar "Sí" o "No" en la columna de "Pagado"
    def is_paid(self, obj):
        return "Sí pago" if obj.paid else "No ha pagado"

    is_paid.short_description = 'Estado de pago'  
    is_paid.admin_order_field = 'paid'  
    
    # Hacer el campo 'paid' editable directamente
    list_editable = ['paid', 'status']  # Hacer el estado editable