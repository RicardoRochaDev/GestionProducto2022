from django.db import models
from .TipoProducto import TipoProducto
from .Proveedor import Proveedor

class Producto(models.Model):
    nombre = models.CharField(max_length=50)
    marca = models.CharField(max_length=100)
    tipo = models.ForeignKey(
        TipoProducto,
        on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=200)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    proveedor = models.ForeignKey(
        Proveedor,
        on_delete = models.CASCADE)

    creado= models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.nombre