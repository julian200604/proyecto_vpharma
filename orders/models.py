from django.db import models
from django.contrib.auth.models import User

class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('delivered', 'Entregado'),
        ('canceled', 'Cancelado'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=50, verbose_name='Nombres')
    last_name = models.CharField(max_length=50, verbose_name='Apellidos')
    address = models.CharField(max_length=250, verbose_name='Dirección', null=True, blank=True)
    neighborhood = models.CharField(max_length=100, verbose_name='Barrio', null=True, blank=True)
    phone_number = models.CharField(max_length=20, verbose_name='Número de teléfono', null=True, blank=True)
    instructions = models.TextField(verbose_name='Instrucciones', null=True, blank=True)
    payment_method = models.CharField(max_length=20, verbose_name='Forma de pago')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    paid = models.BooleanField(default=False, verbose_name='Pagado')
    status = models.CharField(max_length=10, choices=ORDER_STATUS_CHOICES, default='pending', verbose_name='Estado del pedido')

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created']),
        ]
        verbose_name = 'orden'  
        verbose_name_plural = 'órdenes'

    def __str__(self):
        return f'Order {self.id}'

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        related_name='items',
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        'shop.Product',
        related_name='order_items',
        on_delete=models.CASCADE
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity

class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name='nombre')
    category = models.CharField(max_length=100, verbose_name='categoría')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='precio')
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True, verbose_name='imagen')

    