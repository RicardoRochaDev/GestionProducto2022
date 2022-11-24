from django.db import models
from .Cliente import Cliente
from .Proveedor import Proveedor
from .Producto import Producto 
from .EstadoPedido import EstadoPedido
from .Calificacion import Calificacion


class Pedido(models.Model):
    #tiene una lista de productos
    
    #cuando confirmado = true, el pedido pasa a la lista de pedidos para entregar
    
    cliente = models.ForeignKey(
        Cliente,
        on_delete = models.CASCADE)
    fecha = models.DateField()
    hora = models.TimeField()
    proveedor = models.ForeignKey(
        Proveedor, 
        on_delete=models.CASCADE)

    calle= models.CharField(max_length=100)
    numero= models.IntegerField()
    latitud = models.DecimalField(max_digits=20, decimal_places=10)
    longitud = models.DecimalField(max_digits=20, decimal_places=10)

    productos = models.ManyToManyField(
        Producto)

    estado = models.ForeignKey(
        EstadoPedido, 
        on_delete=models.CASCADE)
    
    calificacion = models.OneToOneField(Calificacion, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.cliente.user.username
