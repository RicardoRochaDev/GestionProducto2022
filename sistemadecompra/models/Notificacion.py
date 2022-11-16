from django.db import models
from django.contrib.auth.models import User

class Notificacion(models.Model):
    #user: Para quien va dirijo la notificacion
    user= models.ForeignKey(User, on_delete=models.PROTECT, null=True) 
    leido= models.BooleanField(default= False)
    mensaje= models.CharField(max_length=200, null=True)
    

