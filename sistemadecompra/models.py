from django.db import models

class Producto(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=200)
    valor = models.DecimalField(default=0, max_digits=8, decimal_places=2)