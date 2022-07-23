from django.db import models
from .Proveedor import Proveedor

class Horario(models.Model):
    horaInicio = models.TimeField()
    horaFinal = models.TimeField()
    dia = models.CharField(max_length=15)
    proveedor = models.ForeignKey(
        Proveedor,
        on_delete=models.CASCADE)

    def __str__(self):
        return self.horaInicio