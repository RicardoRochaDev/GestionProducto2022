from django.db import models
#from .Pedido import Pedido 

class Calificacion(models.Model):
    puntaje= models.IntegerField(default=0)
    comentario= models.CharField(max_length=500) 
    #fecha= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.puntaje
