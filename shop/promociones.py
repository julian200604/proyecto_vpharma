from django.db import models
from django.utils import timezone

class Promocion(models.Model):
    nombre = models.CharField(max_length=100)
    descuento = models.DecimalField(max_digits=5, decimal_places=2)  # Porcentaje de descuento
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()

    def __str__(self):
        return self.nombre

    def is_active(self):
        today = timezone.now().date()
        return self.fecha_inicio <= today <= self.fecha_fin
