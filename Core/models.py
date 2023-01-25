from django.db import models
from django.core.validators import RegexValidator
from django.utils.timezone import now
from datetime import date
from django.core.exceptions import ValidationError


class Localidad (models.Model):

    REGEX_NUMEROPOSTAL = '^[0-9]{1,12}$'
    MAXNUMEROPOSTAL=4
    REGEX_NOMBRE = '^[0-9a-zA-Z-_ .]{3,100}$'
    MAXNOMBRELOCALIDAD=70

    CodigoPosta = models.CharField(
        help_text="cp",
        max_length=MAXNUMEROPOSTAL,
        unique=True,
        null=False,
        blank=False,
        error_messages={
            'max_length': "El Codigo Postal puede tener a lo sumo {} caracteres".format(MAXNUMEROPOSTAL),
            'unique': "El Codigo Postal ingresado ya existe",
            'blank': "El Codigo Postal  es obligatorio"
        }
    )

    NombreLocalidad= models.CharField(
        help_text= "Nombre Localidad ",
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
        return "{0}".format( self.NombreLocalidad)

class PlanDeEstudios(models.Model):
    MAXCODIGO=7
    MAXANIO=4
    MAXORIENTACION= 20
    MAXNIVEL= 20
    MAXDESCRIPCION=50
    #REGEX_CODIGO= 1


    codigo= models.CharField(
        help_text="codigo plan estudio",
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
        help_text="año actual del plan de estudio",
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
        help_text="orientacion del plan de estudio",
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
        help_text="nivel ",
        unique=False,
        max_length= MAXORIENTACION,
        null=False,
        blank=False,
        error_messages={
            'blank': "El nivel es obligatorio"
        }
    )
    descripcion = models.CharField(
        help_text="descripcion",
        unique=False,
        max_length= MAXDESCRIPCION,
        null=False,
        blank=True,
    )

    cantidadAnios = models.PositiveIntegerField()

    def __str__(self):
        return "{0}, {1}".format(self.anio, self.orientacion)

    @staticmethod
    def crear_anios_plan(self):
        anio= 1
        while anio <= self.cantidadAnios:
            Anio=AnioPlan.objects.create(codigo=anio, descripcion="anio", plan=self)
            Anio.save()
            anio= anio +1
        return Anio

class Persona(models.Model):
    MAXNOMBRE = 50
    MAXAPELLIDO = 50
    REGEX_NOMBRE = '^[0-9a-zA-Z-_ .]{3,100}$'
    REGEX_NUMERO = '^[0-9]{1,12}$'
    MAXDNI =11
    MAXDIRECCION = 100
    MAXTELEFONO = 7

    Nombre = models.CharField(
        help_text= "Nombre",
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

    Apellido = models.CharField(
        help_text="Apellido",
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

    Dni= models.CharField(
        help_text= "ingrese DNI",
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
    Localidad=models.ForeignKey(
        Localidad,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        help_text="Ingrese Localidad",
        error_messages={
        }
    )

    Direccion=models.CharField(
        help_text= "Direccion",
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

    Email = models.EmailField(
        help_text="Ingrese email valido",
        unique=True,
        null=True,
        blank=True,
        primary_key=False,
        error_messages={
            'unique': "Otra persona tiene ese email",
        }
    )

    Telefono= models.CharField(
        help_text="Telefono ",
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
        return "{0}, {1}, {2}".format(self.Dni, self.Apellido, self.Nombre)



class Estudiante(Persona):

    def dia_futuro(value):
        hoy = date.today()
        if hoy <= value:
            raise ValidationError('La fecha ingresada es mayor a la actual')
        return value

    legajo = models.CharField(max_length= 50,unique= True)
    fechaInscripcion = models.DateField(validators=[dia_futuro])



'''calificacion = models.ForeignKey(Calificacion, on_delete= models.CASCADE, related_name= "estudiante")
'''

class Docente(Persona):
    tituloHabilitante = models.CharField(max_length= 50)

class Preceptor(Persona):
    pass

class AnioPlan(models.Model):
    MAXCODIGO= 20
    CANTMAXPORANIO= 50
    MAXDESCRIPCION = 50

    codigo = models.CharField(help_text="codigo",
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


    def crear_inscripcion_alumno(self):

        pass


    def __str__(self):
        return "{0}, {1}".format(self.codigo, self.descripcion)


class EspacioCurricular(models.Model):
    class Meta:
        unique_together = [['anio', 'codigo']]

    anio = models.ForeignKey(AnioPlan, on_delete= models.CASCADE)

    codigo = models.CharField(max_length= 50)

    cantidadModulos = models.PositiveIntegerField()

    nombre = models.CharField(max_length= 50)

    contenido = models.CharField(max_length=50)

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
class inscripcionEstudianteCiclo(models.Model):
    alumno = models.ForeignKey(
        Estudiante,
        null= True,
        on_delete=models.CASCADE,
    )

    # ciclo = models.models.ForeignKey(
    #     Ciclo,
    #     on_delete=models.CASCADE)
