# Generated by Django 4.2.8 on 2024-06-10 17:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Core', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='calificacion',
            unique_together={('instancia', 'ciclo', 'estudiante')},
        ),
    ]
