from django.db import models
from django.urls import reverse
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name='Nombre')  
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
        ]
        verbose_name = 'categoría'  
        verbose_name_plural = 'categorías' 

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.slug])

class Promocion(models.Model):
    nombre = models.CharField(max_length=200, verbose_name='Nombre')  
    descuento = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Descuento')  
    fecha_inicio = models.DateField(verbose_name='Fecha de inicio')  
    fecha_fin = models.DateField(verbose_name='Fecha de fin') 

    class Meta:
        verbose_name = 'promoción'  
        verbose_name_plural = 'promociones' 

    def __str__(self):
        return self.nombre

    @property
    def is_active(self):
        today = timezone.now().date()
        return self.fecha_inicio <= today <= self.fecha_fin

class Product(models.Model):
    category = models.ForeignKey(
        Category,
        related_name='products',
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=200, verbose_name='Nombre') 
    slug = models.SlugField(max_length=200)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True, verbose_name='Imagen')  
    description = models.TextField(blank=True, verbose_name='Descripción')  
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Precio')  
    cantidad = models.PositiveIntegerField(default=0, verbose_name='Cantidad')  
    available = models.BooleanField(default=True, verbose_name='Disponible')  
    promocion = models.ForeignKey(Promocion, related_name='productos', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Promoción')  # Cambié a español

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['name']),
        ]
        verbose_name = 'producto'  
        verbose_name_plural = 'productos'

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])

    @property
    def precio_con_descuento(self):
        if self.promocion and self.promocion.is_active:
            return self.price * (1 - (self.promocion.descuento / 100))
        return self.price

    @property
    def precio_en_pesos(self):
        return f"${self.price:,.0f} COP"  # Formato en pesos colombianos

