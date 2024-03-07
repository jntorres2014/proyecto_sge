import random
from django.db import models
from django.core.validators import RegexValidator
from django.utils.timezone import now
from datetime import date, timezone
from django.core.exceptions import ValidationError
from faker import Faker
from django.db.models.signals import post_save
from django.dispatch import receiver
import pandas as pd
from django.db import IntegrityError


class Localidad (models.Model):

    REGEX_NUMEROPOSTAL = '^[0-9]{1,12}$'
    MAXNUMEROPOSTAL=4
    REGEX_NOMBRE = '^[0-9a-zA-Z-_ .]{3,100}$'
    MAXNOMBRELOCALIDAD=70

    codigoPostal = models.CharField(
        help_text="cp",
        max_length=MAXNUMEROPOSTAL,
        unique=False,
        null=False,
        blank=False,
        error_messages={
            'max_length': "El Codigo Postal puede tener a lo sumo {} caracteres".format(MAXNUMEROPOSTAL),
            'unique': "El Codigo Postal ingresado ya existe",
            'blank': "El Codigo Postal  es obligatorio"
        }
    )

    nombre= models.CharField(
        help_text= "Trelew ",
        max_length = MAXNOMBRELOCALIDAD,
        unique= False,
        null= False,
        blank= False,
        validators= [RegexValidator(regex=REGEX_NOMBRE)],
        error_messages= {
            'max_length': "El nombre puede tener a lo sumo {} caracteres".format(MAXNOMBRELOCALIDAD),
            'blank': "El nombre es obligatorio"
        }
    )

    def __str__(self):
        return "{1} - {0}".format( self.nombre,self.codigoPostal)
    
    
    def altaLocalidadExcel():
        print("entre")
         # Cargar datos desde el archivo Excel
        df = pd.read_excel("prueba.xls")
        for index, row in df.iterrows():
        # Iterar sobre filas y crear instancias de Localidad
            try:
                localidad = Localidad(
                    codigoPostal=row['Codigo Postal'],
                    nombre=row['Localidad'],
                )
                localidad.save()
            except IntegrityError:
                print(f"La localidad con Codigo Postal {row['Codigo Postal']} ya existe. Continuando con la siguiente.")


    @classmethod
    def seed_db(this,n):
        faker = Faker()
        for  n in range(0,n):
            Localidad.objects.create(
                codigoPostal = n,
                nombre = faker.name()
            )

class PlanDeEstudios(models.Model):
    MAXCODIGO=20
    MAXANIO=4
    MAXORIENTACION= 50
    MAXNIVEL= 50
    MAXDESCRIPCION=50
    #REGEX_CODIGO= 1


    codigo= models.CharField(
        help_text="Ej: 123456",
        unique=True,
        max_length=MAXCODIGO,
        null=False,
        blank=False,
       # validators= [RegexValidator(regex= REGEX_CODIGO) ],
        error_messages={
            'blank': "El nombre es obligatorio"
        }
    )
    anio = models.CharField(
        help_text="Ej: 2024",
        unique=False,
        max_length=MAXANIO,
        null=True,
        blank=False,
        default= 1,
        error_messages={
            'blank': "el anio es obligatorio"
        }
    )
    orientacion = models.CharField(
        help_text="Ej: Profesorado de educacion primaria",
        unique=False,
        max_length=MAXORIENTACION,
        null=False,
        blank=False,
        primary_key=False,
        error_messages={
            'blank': "la orientacion es obligatoria"
        }
    )
    nivel = models.CharField(
        help_text="Ej: Primario",
        unique=False,
        max_length= MAXORIENTACION,
        null=False,
        blank=False,
        error_messages={
            'blank': "El nivel es obligatorio"
        }
    )
    descripcion = models.CharField(
        help_text="Ej: descripcion del plan de estudios",
        unique=False,
        max_length= MAXDESCRIPCION,
        null=False,
        blank=True,
    )

    esActual = models.BooleanField(
        default= True
    )
    implementado = models.BooleanField(
        default= False
    )
    
    cantidadAnios = models.PositiveIntegerField()
    
    

    def __str__(self):
        return "Plan de estudios del año {0}, Orientacion {1}".format(self.anio, self.orientacion)

    @staticmethod
    def crear_anios_plan(self):
        anio= 1
        while anio <= self.cantidadAnios:
            Anio = AnioPlan.objects.create(codigo=anio, descripcion="anio", plan=self)
            Anio.save()
            anio= anio +1
        return Anio
   
    @classmethod
    def actualizar_actual(cls):
        # Establecer todos los planes como no actuales
        cls.objects.all().update(esActual=False)

    @classmethod
    def cambiar_actual(cls, request, id_plan):
        # Actualizar el estado de todos los planes
        cls.actualizar_actual()

        # Establecer el plan específico como actual
        plan = cls.objects.get(id=id_plan)
        plan.esActual = True
        plan.save()

        
@receiver(post_save, sender=PlanDeEstudios)
def ajustar_actual(sender, instance, **kwargs):
   if instance.esActual:
        PlanDeEstudios.objects.exclude(pk=instance.pk).update(esActual=False)

class Rol(models.Model):
    nombre = models.CharField(max_length = 100, unique = True,default = 'Docente')
    

    def __str__(self):
        return self.nombre

class Persona(models.Model):
    MAXNOMBRE = 50
    MAXAPELLIDO = 50
    REGEX_NOMBRE = '^[0-9a-zA-Z-_ .]{3,100}$'
    REGEX_NUMERO = '^[0-9]{1,12}$'
    MAXDNI =11
    MAXDIRECCION = 100
    MAXTELEFONO = 10

    nombre = models.CharField(
        help_text="Ej: Juan",
        max_length = MAXNOMBRE,
        unique= False,
        null= False,
        blank= False,
        validators= [RegexValidator(regex=REGEX_NOMBRE)],
        error_messages= {
            'max_length': "El nombre puede tener a lo sumo {} caracteres".format(MAXNOMBRE),
            'blank': "El nombre es obligatorio"
        }
    )

    apellido = models.CharField(
        help_text="Ej: Perez",
        max_length=MAXAPELLIDO,
        unique=False,
        null=False,
        blank=False,
        validators=[RegexValidator(regex=REGEX_NOMBRE)],
        error_messages={
            'max_length': "El apellido puede tener a lo sumo {} caracteres".format(MAXNOMBRE),
            'blank': "El apéllido es obligatorio"
        }
    )

    dni= models.CharField(
        help_text="Ej: 12345678",
        max_length = MAXDNI,
        unique= True,
        null= False,
        blank= False,
        error_messages= {
            'max_length': "El dni puede tener a lo sumo {} caracteres".format(MAXDNI),
            'unique': "El dni ingresado ya existe",
            'blank': "El dni es obligatorio"
        }
    )
    localidad=models.ForeignKey(
        Localidad,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        help_text="Ej: Trelew",
        error_messages={
        }
    )

    direccion=models.CharField(
        help_text="Ej: Calle falsa 123",
        max_length = MAXDIRECCION,
        unique= False,
        null= False,
        blank= False,
        error_messages= {
            'blank': "La direccion es obligatoria"
        }
    )

    email = models.EmailField(
        help_text="Ej: asd@asd.com",
        unique=True,
        null=True,
        blank=True,
        primary_key=False,
        error_messages={
            'unique': "El email no esta disponible",
        }
    )

    telefono= models.CharField(
        help_text="Ej: 0123456789 ",
        max_length=MAXTELEFONO,
        unique=False,
        null=True,
        blank=True,
        primary_key=False,
        validators=[RegexValidator(regex=REGEX_NUMERO)],
        error_messages={
            'max_length': "El telefono puede tener a lo sumo {} caracteres".format(MAXTELEFONO),
        }
    )

    def __str__(self):
        return "{0}, {1}, {2}".format(self.dni, self.apellido, self.nombre)



class Estudiante(Persona):

    def dia_futuro(value):
        hoy = date.today()
        if hoy <  value:
            raise ValidationError('La fecha ingresada es mayor a la actual')
        return value

    legajo = models.CharField(
        help_text="Ej: asd123",
        max_length= 50,unique= True,
        )
    fechaInscripcion = models.DateField(default = now,validators=[dia_futuro])

    @classmethod
    def seed_db(this,n):
        fake = Faker()
        localidad = Localidad.objects.get_or_create(id=1)[0]
        for  n in range(0,n):
            Estudiante.objects.create(
                nombre= fake.first_name(),
                apellido= fake.last_name(),
                dni= fake.unique.random_number(digits=8),
                localidad = localidad,
                email = fake.email(),
                telefono = 123345,
                direccion = fake.address(),
                legajo=fake.unique.random_number(digits=5),
                fechaInscripcion=fake.date_between(start_date='-365d', end_date='today'),  # fecha aleatoria en el último año
            )
    aulas = models.ManyToManyField(
        'Aula',
        blank=True,
        related_name='estudiantes_en_aula'
        )
'''calificacion = models.ForeignKey(Calificacion, on_delete= models.CASCADE, related_name= "estudiante")
'''

class Docente(Persona):
    tituloHabilitante = models.CharField(max_length= 50)
    rol = models.ForeignKey(Rol, on_delete = models.CASCADE, default = 'Docente')

class Preceptor(Persona):
    pass

class AnioPlan(models.Model):
    MAXCODIGO= 50
    CANTMAXPORANIO= 50
    MAXDESCRIPCION = 50

    codigo = models.CharField(
        help_text="Ej: ",
        max_length= MAXCODIGO,
        null=False,
        blank=False,
        error_messages={
            'blank': "El codigo es obligatorio"
        })


    descripcion = models.CharField(help_text="nivel",
        unique=False,
        max_length= MAXDESCRIPCION,
        null=False,
        blank=False,
        primary_key=False,
        )

    plan = models.ForeignKey(PlanDeEstudios, models.CASCADE, related_name="anios")

    inscripciones = models.ManyToManyField(Estudiante)

    class Meta:
        unique_together = [['codigo', 'plan']]


    def __str__(self):
        return "{0}{1}".format(self.codigo, '°')


class EspacioCurricular(models.Model):
    class Meta:
        unique_together = [['anio', 'codigo']]

    anio = models.ForeignKey(
        AnioPlan, on_delete= models.CASCADE,
        help_text="Ej: Elija un año del plan",)

    codigo = models.CharField(
        help_text="Ej: MAT-035",
        max_length= 50,
        unique= True)

    cantidadModulos = models.PositiveIntegerField(
        help_text="Ej: 5",)

    nombre = models.CharField(help_text="Ej: Matematica"
                              ,max_length= 50)

    contenido = models.CharField(help_text="Ej: Sumas y restas basicas"
                                 ,max_length=50)
    
    plan = models.ForeignKey(PlanDeEstudios, on_delete=models.CASCADE)

    '''estudiantes = models.ManyToManyField(Estudiante, through="Calificacion")
    '''

    def __str__(self):
        return "{0}, {1}".format(self.codigo, self.nombre)


class Calificacion(models.Model):
    FINAL = 1
    PARCIAL = 2
    CHOICES_TIPO = (
        (FINAL, 'final'),
        (PARCIAL, 'parcial'))

    tipo= models.PositiveIntegerField(choices = CHOICES_TIPO)

    nota = models.PositiveSmallIntegerField()

    docente = models.ForeignKey(
        Docente,
        null=True,
        blank=False,
        on_delete=models.CASCADE,
        related_name="docente")

    espacioCurricular = models.ForeignKey(
        EspacioCurricular,
        null=True,
        blank=False,
        on_delete=models.CASCADE,
        related_name="espacioCurricular")

    estudiante= models.ForeignKey(
        Estudiante,
        null= True,
        blank= False,
        on_delete= models.CASCADE
    )
    
#__________________-------------------------________________________-----------------------__________

class Ciclo (models.Model):


    # def tope(inicio):

    #     if inicio >= inicio:
    #         raise ValidationError('La fecha ingresada es mayor a la actual')
    #     return
    
    anioCalendario = models.CharField(
        help_text="Ej: 2024",
        max_length=4,
        unique= True)

    fechaInicio = models.DateField(help_text="Ej: 16/02/2024",
                                   default=now)

    plan = models.ForeignKey(PlanDeEstudios, blank=False, on_delete=models.CASCADE)

    fechaFin = models.DateField(help_text="Ej: 28/11/2024",)
    
    esActual = models.BooleanField(
        default= True
    )
    @property
    def esta_vigente(self):
        """
        Método que verifica si el ciclo está vigente en función de la fecha actual.
        """
        fecha_actual = timezone.now().date()
        return self.fechaInicio <= fecha_actual <= self.fechaFin

    
    def __str__(self):
        return "{0} Vigente desde {1} hasta {2}".format(self.anioCalendario,self.fechaInicio.strftime("%d-%m-%Y"), self.fechaFin.strftime("%d-%m-%Y"))
    
    @staticmethod
    def crear_division_para_anio_ciclo(self,anios):
        for a in anios.all():
            division=Division.objects.create(ciclo=self,
                                             codigo='A',
                                             descripcion="{} {}".format(a, 'Division A'),
                                             anio=a)
            division.crear_Horario_Division()
        return division
    @classmethod
    def actualizar_actual(cls):
        # Establecer todos los planes como no actuales
        cls.objects.all().update(esActual=False)

    @classmethod
    def cambiar_actual(cls, request, id_ciclo):
        # Actualizar el estado de todos los ciclos
        cls.actualizar_actual()

        # Establecer el ciclo específico como actual
        ciclo = cls.objects.get(id=id_ciclo)
        ciclo.esActual = True
        ciclo.save()

    @staticmethod
    def crear_division_para_plan(ciclo,plan):
        for a in plan.anios.all():
            print('entro')
            division=Division.objects.create(ciclo=ciclo,
                                             codigo=Division.PRIMERA,
                                             descripcion="{} {}".format(a, Division.PRIMERA),
                                             anio=a)
            division.crear_Horario_Division(division)
        return division
@receiver(post_save, sender=Ciclo)
def ajustarCicloactual(sender, instance, **kwargs):
   if instance.esActual:
        Ciclo.objects.exclude(pk=instance.pk).update(esActual=False)
    
    
#--------------------------------------------------------------------------

class Division(models.Model):
    PRIMERA = '1ra'
    SEGUNDA = '2da'
    TERCERA = '3ra'
    CUARTA = '4ta'
    QUINTA = '5ta'
    CHOICES_DIV = (
        (PRIMERA, 'Primera'),
        (SEGUNDA, 'Segunda'),
        (TERCERA, 'Tercera'),
        (CUARTA, 'Cuarta'),
        (QUINTA, 'Quinta'))

    #class Meta:
    #   unique_together = (('codigo', 'anio', 'ciclo'))

    ciclo = models.ForeignKey(Ciclo, on_delete=models.CASCADE, related_name="divisiones")
    
    codigo = models.CharField(max_length=50, choices=CHOICES_DIV, default=PRIMERA)
    
    descripcion = models.CharField(max_length=50)
    
    anio = models.ForeignKey(AnioPlan, on_delete=models.CASCADE)
    
    alumnos = models.ManyToManyField(Estudiante)


    def __str__(self):
        return "{0},{1}".format(self.anio.codigo, self.codigo)

    def generarCodigoDiv(self):
        print(Division.objects.filter(anio=self.anio).count)

        self.codigo= Division.objects.filter().count

    def crear_Horario_Division(self):
        print("entre a crear horario divisioon")
        Horario.objects.create(division= self)    

    def agregar_materia(self, materia, dia, hora, modulos):
        return Horario.objects.create(division=self,
            espacioCurricular=materia,
            dia=dia,
            hora=hora,
            cantidad_modulo=modulos)


    def asigar_estudiante_a_division(self):
        pass

class Horario(models.Model):
    LUNES= 1
    MARTES= 2
    MIERCOLES= 3
    JUEVES = 4
    VIERNES = 5
    SABADO = 6
    DOMINGO = 7
    CHOICES_DIA = (
        (LUNES, 'Lunes'),
        (MARTES, 'Martes'),
        (MIERCOLES, 'Miercoles'),
        (JUEVES, 'Jueves'),
        (VIERNES, 'Viernes'),
        (SABADO, 'Sabado'),
        (DOMINGO, 'Domingo'))


    MODUNO= 1
    MODDOS= 2
    MODTRES= 3
    MODCUATRO = 4
    MODCINCO = 5
    MODSEIS= 6
    MODSIETE = 7
    MODOCHO = 8
    CHOICES_HORA = (
        (MODUNO, '1'),
        (MODDOS, '2'),
        (MODTRES, '3'),
        (MODCUATRO, '4'),
        (MODCINCO, '5'),
        (MODSEIS,'6'),
        (MODOCHO, '7'))

    class Meta:
        unique_together = (('division'),)

    division = models.ForeignKey(Division, on_delete=models.CASCADE, related_name='horarios',blank=False)

    cantidad_modulo = models.PositiveSmallIntegerField(null=False, blank=False, default=1)

    docente = models.ForeignKey(
        Docente,
        null = True,
        blank = True,
        on_delete = models.CASCADE
        )


    def control_modulos(self,modulo):
        self.cantidad_modulo= self.cantidad_modulo - modulo
        return self

    def asignar_a_modulos(self,cant):
        print(cant)
        i=1
        while cant > 1:
            cant = cant -1
            Horario.objects.create(division=self.division, espacioCurricular=self.espacioCurricular,cantidad_modulo= cant[1], dia= self.dia,hora= self.hora+i)
            i=i+1
    def __str__(self):
        return "{0}, ".format(self.division)


class Detalle_Horario(models.Model):
    horario= models.ForeignKey(Horario,on_delete = models.CASCADE)
    espacioCurricular = models.ForeignKey(EspacioCurricular, on_delete=models.CASCADE, related_name='horarios')
    dia= models.CharField(help_text="Lunes",max_length=10)
    hora = models.CharField(help_text="Ej: Modulo 1",max_length=10)
    docente = models.ForeignKey(Docente, on_delete = models.CASCADE, null = True)
    
    
    class Meta:
        unique_together = ('horario','espacioCurricular','dia','hora')
    
    def __str__(self):
        return "{0}".format(self.horario.division)

class InscripcionDocente(models.Model):
    docente = models.ForeignKey(
        Docente,
        null=True,
        help_text="Ej: Juan Perez",
        on_delete=models.CASCADE,
    )
    
    ciclo = models.ForeignKey(
        Ciclo,
        null=True,
        on_delete=models.CASCADE,
        help_text="Ej: Actual",
    )

    anio = models.ForeignKey(
        AnioPlan,
        on_delete=models.CASCADE,
        help_text="Ej: 1,año",
    )
    fecha = models.DateTimeField(default=now,help_text="Ej: 16/02/2024",)

    class Meta:
        unique_together = ['docente', 'ciclo']

class Inscripcion(models.Model):
    estudiante = models.ForeignKey(
        Estudiante,
        null=True,
        help_text="Ej: Juan Perez",
        on_delete=models.CASCADE,
    )
    
    ciclo = models.ForeignKey(
        Ciclo,
        null=True,
        on_delete=models.CASCADE,
        help_text="Ej: Actual",
    )

    anio = models.ForeignKey(
        AnioPlan,
        on_delete=models.CASCADE,
        help_text="Ej: 1,año",
    )
    fecha = models.DateTimeField(default=now,help_text="Ej: 16/02/2024",)

    class Meta:
        unique_together = ['estudiante', 'ciclo', 'anio']

    @classmethod
    def seed_db(this, n):
        fake = Faker()
        ciclo_actual = Ciclo.objects.get(esActual='True')
        
        # Obtener todos los estudiantes que no están inscritos en el ciclo actual
        estudiantes_sin_inscripcion = Estudiante.objects.exclude(Inscripcion__ciclo=ciclo_actual)
        
        # Verificar si hay suficientes estudiantes disponibles para seleccionar aleatoriamente
        if estudiantes_sin_inscripcion.count() < n:
            print("No hay suficientes estudiantes disponibles.")
            return
        
        # Seleccionar n estudiantes al azar sin repetición de la lista de estudiantes sin inscripción
        estudiantes_aleatorios = random.sample(list(estudiantes_sin_inscripcion), n)
        
        # Crear inscripciones para los estudiantes seleccionados
        for estudiante in estudiantes_aleatorios:
            Inscripcion.objects.create(
                estudiante=estudiante,
                ciclo=ciclo_actual,
                anio=random.choice(list(AnioPlan.objects.filter(plan=PlanDeEstudios.objects.get(esActual='True')))),
                fecha=fake.date_between(start_date='-365d', end_date='today'),  # fecha aleatoria en el último año
            )

class Aula(models.Model):
    estudiantes = models.ManyToManyField(
        'Estudiante',
        blank=True,
        related_name="estudiantes",
    )   
    
    division = models.ForeignKey(
        'Division',
        unique=False,
        null=False,  # Asegura que cada aula tenga una división asociada
        blank=False,
        on_delete=models.CASCADE,
        related_name="aulas"  # Hace que el acceso a las aulas asociadas con una división sea más claro
    )
    
    class Meta:
        db_table = 'Aula'
    
