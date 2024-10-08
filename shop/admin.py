from django.contrib import admin
from .models import Category, Product, Promocion

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']  
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'available', 'cantidad']  
    list_filter = ['available']
    list_editable = ['price', 'available', 'cantidad'] 
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Promocion)
class PromocionAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'descuento', 'fecha_inicio', 'fecha_fin']  
    list_filter = ['fecha_inicio', 'fecha_fin']
    search_fields = ['nombre']