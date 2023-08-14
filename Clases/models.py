from django.db import models
from django.utils import  timezone
from Core.models import Estudiante


class Inasistencias(models.Model):
    class Meta:
        unique_together = [['dia', 'estudiante']]

    estudiante = models.ForeignKey(
        Estudiante,
        null=False,
        blank=False,
        on_delete=models.CASCADE)
    dia= models.DateField(default=timezone.now)

    falta= models.BooleanField(default=True)

    justificacion= models.CharField(max_length=50)


