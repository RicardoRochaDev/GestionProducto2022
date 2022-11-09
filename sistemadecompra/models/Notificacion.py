from django.db import models
from .Pedido import Pedido
#from django.contrib.auth.models import User

class Notificacion(models.Model):
    pedido= models.OneToOneField(Pedido, on_delete=models.PROTECT)
    leido= models.BooleanField(default= False)

