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

    productos = models.ManyToManyField(Producto, through='PedidoProductos')

    estado = models.ForeignKey(
        EstadoPedido, 
        on_delete=models.CASCADE)
    
    calificacion = models.OneToOneField(Calificacion, on_delete=models.CASCADE, null=True)

    fecha_creacion= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Cliente: " + self.cliente.user.username + " - Proveedor: " + self.proveedor.user.username

class PedidoProductos(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    cantidad = models.IntegerField()