# Generated by Django 4.1.4 on 2023-01-25 22:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='inscripcionEstudianteCiclo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alumno', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Core.estudiante')),
            ],
        ),
    ]
