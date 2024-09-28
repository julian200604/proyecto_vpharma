# favorite/models.py
from django.db import models
from django.contrib.auth.models import User
from shop.models import Product  # Asegúrate de que el modelo Product esté correctamente importado desde la app correspondiente

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user} - {self.product}"

