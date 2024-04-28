from django.db import models
from django.utils import  timezone
from Core.models import Estudiante,Ciclo
import random
from faker import Faker


class Inasistencias(models.Model):
    class Meta:
        unique_together = [['dia', 'estudiante']]
    ciclo = models.ForeignKey(
        Ciclo,
        null=False,
        blank=False,
        on_delete=models.CASCADE)
    
    estudiante = models.ForeignKey(
        Estudiante,
        null=False,
        blank=False,
        on_delete=models.CASCADE)
    dia= models.DateField(default=timezone.now)

    falta= models.BooleanField(default=True)

    justificacion= models.CharField(max_length=50)




    def generate_inasistencias(quantity):
        fake = Faker('es_ES')
        ciclos = Ciclo.objects.all()
        estudiantes = Estudiante.objects.all()
        for _ in range(quantity):
            inasistencia = Inasistencias.objects.create(
                ciclo=random.choice(ciclos),
                estudiante=random.choice(estudiantes),
                dia=fake.date_between(start_date="-10y", end_date="today"),
                falta=random.choice([True, False]),
                justificacion=fake.sentence(nb_words=6, variable_nb_words=True)
            )
            inasistencia.save()
