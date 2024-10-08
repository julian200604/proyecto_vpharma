from django.db import models

class Order(models.Model):
    first_name = models.CharField(max_length=50, verbose_name='Nombres')
    last_name = models.CharField(max_length=50, verbose_name='Apellidos')
    email = models.EmailField(verbose_name='Correo electrónico')
    address = models.CharField(max_length=250, verbose_name='Dirección', null=True, blank=True)
    city = models.CharField(max_length=100, verbose_name='Ciudad - Municipio')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    paid = models.BooleanField(default=False, verbose_name='Pagado')

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created']),
        ]
        verbose_name = 'orden'  
        verbose_name_plural = 'ordenes'

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
