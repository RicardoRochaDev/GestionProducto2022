from django.db import models
#from .Pedido import Pedido 

class Calificacion(models.Model):
    puntaje= models.DecimalField(max_digits=10, decimal_places=2)
    comentario= models.CharField(max_length=1000) 
    fecha= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.puntaje)
