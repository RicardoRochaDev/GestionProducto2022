from django.db import models
from .Proveedor import Proveedor

class Horario(models.Model):
    horaInicio = models.TimeField(help_text="Please use the following format: <em>YYYY-MM-DD</em>.")
    horaFinal = models.TimeField(help_text="Please use the following format: <em>YYYY-MM-DD</em>.")
    dia = models.CharField(max_length=15)
    proveedor = models.ForeignKey(
        Proveedor,
        on_delete=models.CASCADE)
    
    def __str__(self):
        return str(str(self.horaInicio) + " - " + str(self.horaFinal))