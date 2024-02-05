# Generated by Django 4.2.8 on 2024-02-04 20:38

import Core.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AnioPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(error_messages={'blank': 'El codigo es obligatorio'}, help_text='codigo', max_length=50)),
                ('descripcion', models.CharField(help_text='nivel', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Ciclo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('anioCalendario', models.CharField(max_length=4, unique=True)),
                ('fechaInicio', models.DateField(default=django.utils.timezone.now)),
                ('fechaFin', models.DateField()),
                ('esActual', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Division',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(choices=[('1ra', 'Primera'), ('2da', 'Segunda'), ('3ra', 'Tercera'), ('4ta', 'Cuarta'), ('5ta', 'Quinta')], default='1ra', max_length=50)),
                ('descripcion', models.CharField(max_length=50)),
                ('anio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Core.anioplan')),
                ('ciclo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='divisiones', to='Core.ciclo')),
            ],
        ),
        migrations.CreateModel(
            name='Localidad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CodigoPosta', models.CharField(error_messages={'blank': 'El Codigo Postal  es obligatorio', 'max_length': 'El Codigo Postal puede tener a lo sumo 4 caracteres', 'unique': 'El Codigo Postal ingresado ya existe'}, help_text='cp', max_length=4)),
                ('NombreLocalidad', models.CharField(error_messages={'blank': 'El nombre es obligatorio', 'max_length': 'El nombre puede tener a lo sumo 70 caracteres'}, help_text='Nombre Localidad ', max_length=70, validators=[django.core.validators.RegexValidator(regex='^[0-9a-zA-Z-_ .]{3,100}$')])),
            ],
        ),
        migrations.CreateModel(
            name='Persona',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Nombre', models.CharField(error_messages={'blank': 'El nombre es obligatorio', 'max_length': 'El nombre puede tener a lo sumo 50 caracteres'}, help_text='Nombre', max_length=50, validators=[django.core.validators.RegexValidator(regex='^[0-9a-zA-Z-_ .]{3,100}$')])),
                ('Apellido', models.CharField(error_messages={'blank': 'El apéllido es obligatorio', 'max_length': 'El apellido puede tener a lo sumo 50 caracteres'}, help_text='Apellido', max_length=50, validators=[django.core.validators.RegexValidator(regex='^[0-9a-zA-Z-_ .]{3,100}$')])),
                ('Dni', models.CharField(error_messages={'blank': 'El dni es obligatorio', 'max_length': 'El dni puede tener a lo sumo 11 caracteres', 'unique': 'El dni ingresado ya existe'}, help_text='ingrese DNI', max_length=11, unique=True)),
                ('Direccion', models.CharField(error_messages={'blank': 'El dni es obligatorio', 'max_length': 'El dni puede tener a lo sumo 11 caracteres', 'unique': 'El dni ingresado ya existe'}, help_text='Direccion', max_length=11)),
                ('Email', models.EmailField(blank=True, error_messages={'unique': 'Otra persona tiene ese email'}, help_text='Ingrese email valido', max_length=254, null=True, unique=True)),
                ('Telefono', models.CharField(blank=True, error_messages={'max_length': 'El telefono puede tener a lo sumo 7 caracteres'}, help_text='Telefono ', max_length=7, null=True, validators=[django.core.validators.RegexValidator(regex='^[0-9]{1,12}$')])),
                ('Localidad', models.ForeignKey(error_messages={}, help_text='Ingrese Localidad', on_delete=django.db.models.deletion.CASCADE, to='Core.localidad')),
            ],
        ),
        migrations.CreateModel(
            name='PlanDeEstudios',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(error_messages={'blank': 'El nombre es obligatorio'}, help_text='codigo plan estudio', max_length=20, unique=True)),
                ('anio', models.CharField(default=1, error_messages={'blank': 'el anio es obligatorio'}, help_text='año actual del plan de estudio', max_length=4, null=True)),
                ('orientacion', models.CharField(error_messages={'blank': 'la orientacion es obligatoria'}, help_text='orientacion del plan de estudio', max_length=50)),
                ('nivel', models.CharField(error_messages={'blank': 'El nivel es obligatorio'}, help_text='nivel ', max_length=50)),
                ('descripcion', models.CharField(blank=True, help_text='descripcion', max_length=50)),
                ('esActual', models.BooleanField(default=True)),
                ('implementado', models.BooleanField(default=False)),
                ('cantidadAnios', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Docente',
            fields=[
                ('persona_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='Core.persona')),
                ('tituloHabilitante', models.CharField(max_length=50)),
            ],
            bases=('Core.persona',),
        ),
        migrations.CreateModel(
            name='Estudiante',
            fields=[
                ('persona_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='Core.persona')),
                ('legajo', models.CharField(max_length=50, unique=True)),
                ('fechaInscripcion', models.DateField(default=django.utils.timezone.now, validators=[Core.models.Estudiante.dia_futuro])),
            ],
            bases=('Core.persona',),
        ),
        migrations.CreateModel(
            name='Preceptor',
            fields=[
                ('persona_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='Core.persona')),
            ],
            bases=('Core.persona',),
        ),
        migrations.CreateModel(
            name='Horario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad_modulo', models.PositiveSmallIntegerField(default=1)),
                ('division', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='horarios', to='Core.division')),
                ('docente', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Core.docente')),
            ],
            options={
                'unique_together': {('division',)},
            },
        ),
        migrations.CreateModel(
            name='EspacioCurricular',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=50)),
                ('cantidadModulos', models.PositiveIntegerField()),
                ('nombre', models.CharField(max_length=50)),
                ('contenido', models.CharField(max_length=50)),
                ('anio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Core.anioplan')),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Core.plandeestudios')),
            ],
            options={
                'unique_together': {('anio', 'codigo')},
            },
        ),
        migrations.CreateModel(
            name='Detalle_Horario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dia', models.CharField(max_length=10)),
                ('hora', models.CharField(max_length=10)),
                ('espacioCurricular', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='horarios', to='Core.espaciocurricular')),
                ('horario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Core.horario')),
            ],
        ),
        migrations.AddField(
            model_name='ciclo',
            name='plan',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Core.plandeestudios'),
        ),
        migrations.CreateModel(
            name='Aula',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('division', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='aulas', to='Core.division')),
            ],
            options={
                'db_table': 'Aula',
            },
        ),
        migrations.AddField(
            model_name='anioplan',
            name='plan',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='anios', to='Core.plandeestudios'),
        ),
        migrations.CreateModel(
            name='inscripcionEstudianteCiclo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(default=django.utils.timezone.now)),
                ('anio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Core.anioplan')),
                ('ciclo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Core.ciclo')),
                ('estudiante', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='Core.estudiante')),
            ],
        ),
        migrations.AddField(
            model_name='estudiante',
            name='aulas',
            field=models.ManyToManyField(blank=True, related_name='estudiantes_en_aula', to='Core.aula'),
        ),
        migrations.AddField(
            model_name='division',
            name='alumnos',
            field=models.ManyToManyField(to='Core.estudiante'),
        ),
        migrations.CreateModel(
            name='Calificacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.PositiveIntegerField(choices=[(1, 'final'), (2, 'parcial')])),
                ('nota', models.PositiveSmallIntegerField()),
                ('espacioCurricular', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='espacioCurricular', to='Core.espaciocurricular')),
                ('docente', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='docente', to='Core.docente')),
                ('estudiante', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Core.estudiante')),
            ],
        ),
        migrations.AddField(
            model_name='aula',
            name='estudiantes',
            field=models.ManyToManyField(blank=True, related_name='aulas_del_estudiante', to='Core.estudiante'),
        ),
        migrations.AddField(
            model_name='anioplan',
            name='inscripciones',
            field=models.ManyToManyField(to='Core.estudiante'),
        ),
        migrations.AlterUniqueTogether(
            name='anioplan',
            unique_together={('codigo', 'plan')},
        ),
    ]
