from django.db import models
#from .Pedido import Pedido 

class Calificacion(models.Model):
    #cliente= models.ForeignKey(User, on_delete=models.PROTECT, null=True) 
    #proveedor= models.BooleanField(default= False)
    #pedido= models.OneToOneField(Pedido, on_delete=models.CASCADE)
    puntaje= models.CharField(max_length=200, null=True)
    comentario= models.CharField(max_length=500) 
    fecha= models.DateField()

    def __str__(self):
        return self.puntaje
