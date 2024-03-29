from django.db import models
from django.contrib.auth.models import User

class Cliente(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name = 'cliente', null=True, blank=True)
    calle= models.CharField(max_length=100)
    numero= models.IntegerField()
    latitud = models.DecimalField(max_digits=20, decimal_places=10)
    longitud = models.DecimalField(max_digits=20, decimal_places=10)
    telefono = models.BigIntegerField() 

    def __str__(self):
        return self.user.username  