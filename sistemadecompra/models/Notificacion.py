from django.db import models
from .Pedido import Pedido
from django.contrib.auth.models import User

class Notificacion(models.Model):
    user= models.ForeignKey(User, on_delete=models.PROTECT, null=True)
    leido= models.BooleanField(default= False)
    mensaje= models.CharField(max_length=200, null=True)
    

