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
        'directions',
        'phone_number',
        'payment_method',
        'city',
        'is_paid',
        'status',
        'created',
        'paid'
    ]
    list_filter = ['paid', 'created', 'status', 'payment_method']
    inlines = [OrderItemInline]
    list_editable = ['paid', 'status']

    def is_paid(self, obj):
        return "Sí pago" if obj.paid else "No ha pagado"

    is_paid.short_description = 'Estado de pago'
    is_paid.admin_order_field = 'paid'
