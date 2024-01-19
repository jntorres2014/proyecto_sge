from django import forms
from django.urls import reverse
from Core.models import PlanDeEstudios, EspacioCurricular
from Core.models import AnioPlan
from Core.models import Localidad
from Core.models import Persona,Docente,Estudiante,Ciclo,Division, inscripcionEstudianteCiclo

from dal import autocomplete

from datetime import datetime


class AnioForm(forms.ModelForm):

    class Meta:
        model = AnioPlan

        fields= [
            'codigo',
            'descripcion',
            'plan',
        ]

        labels = {
            'codigo': 'Codigo',
            'descripcion': 'Descripcion',
            #'ciclo': 'Ciclo'
                }
        widgets={

            'codigo': forms.TextInput(attrs={'class':'form-control'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
            #'ciclo' : forms.TextInput(attrs={'class': 'ciclo.codigo'}),
        }



class PlanDeEstudiosForm(forms.ModelForm):

    class Meta:
        model = PlanDeEstudios

        fields = [
            'codigo',
            'anio',
            'orientacion',
            'nivel',
            'cantidadAnios',
            'descripcion',
        ]

class LocalidadForm(forms.ModelForm):

    class Meta:
        model = Localidad

        fields= [
            'CodigoPosta',
            'NombreLocalidad',
        ]


# Localidad = forms.DateField(
#     required=True,
#     label='Localidad',
#     widget=forms.CharField,
#     help_text='Localidad',
#     error_messages={
#         'invalid_choice': "La opcion no es valida",
#         'required': "La localidad es obligatorio"
#     })


class PersonaForm(forms.ModelForm):
    class Meta:
        model = Persona
        fields= [
            'Dni',
            'Nombre',
            'Apellido',
            'Direccion',
            'Localidad',
            'Email',
            'Telefono'
        ]


class DocenteForm(forms.ModelForm):
    class Meta():
        model = Docente
        fields = [
            'Dni',
            'Nombre',
            'Apellido',
            'Direccion',
            'Localidad',
            'Email',
            'Telefono',
            'tituloHabilitante',
        ]


class EstudianteForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        print("acaaaaaaaaaaaaaa")
        # Obtener el plan de estudios y los ciclos desde los kwargs
        #plan_estudio = kwargs.pop('plan_estudio', None)
        
        super(EstudianteForm, self).__init__(*args, **kwargs)
    
    class Meta:
        model = Estudiante
        fields = '__all__'
        print("acaaaaaaaaaaaaaaasdasdas")
        widgets_localidad = autocomplete.ModelSelect2(url='core:localidad-autocomplete',attrs={'class': 'input-group'})
        print(widgets_localidad)
        fecha = datetime.strftime(datetime.today(), "%Y-%M-%d")
        
        widgets = {
            'Localidad': widgets_localidad,
            'fechaInscripcion': forms.TextInput(attrs={'type': 'date', 'value': fecha})
        }
    
    def __init__(self, *args, **kwargs):
        print("acaaaaaaaaaaaaaa")
        # Obtener el plan de estudios y los ciclos desde los kwargs
        #plan_estudio = kwargs.pop('plan_estudio', None)
        
        super(EstudianteForm, self).__init__(*args, **kwargs)


class EspacioCurricularEditForm(forms.ModelForm):
    
    class Meta:
        model= EspacioCurricular
        fields= [
            'codigo',
            'cantidadModulos',
            'nombre',
            'contenido',
        ]

class EspacioCurricularForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        print("acaaaaaaaaaaaaaa")
        # Obtener el plan de estudios y los ciclos desde los kwargs
        #plan_estudio = kwargs.pop('plan_estudio', None)
        
        super(EspacioCurricularForm, self).__init__(*args, **kwargs)

    class Meta:
        model= EspacioCurricular
        fields= [
            'plan',
            'anio',
            'codigo',
            'cantidadModulos',
            'nombre',
            'contenido',

        ]
        widgets = { 
            'plan': forms.Select(attrs={'class': 'input-group mb-3'}),
            'anio': forms.Select(attrs={'class': 'input-group mb-3'}),
            'codigo': forms.TextInput(attrs={'class': 'input-group mb-3'}),
            'cantidadModulos': forms.TextInput(attrs={'class': 'input-group mb-3', 'type': 'number', 'min':'1'}),
            'nombre': forms.TextInput(attrs={'class': 'input-group mb-3'}),
            'contenido': forms.TextInput(attrs={'class': 'input-group mb-3'}),
            
        }
        cantidadModulos = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        id_plan = kwargs.pop('id_plan', None)
        super(EspacioCurricularForm, self).__init__(*args, **kwargs)
        # Obtener la fecha del sistema
        # Establecer la fecha del sistema en el campo de fecha del formulario
        #self.fields['fecha'].initial = current_date

        anios_plan_estudio = AnioPlan.objects.filter(plan=PlanDeEstudios.objects.get(esActual= 'True'))
        
        
        self.fields['anio'].queryset = anios_plan_estudio

   


class CicloEditForm(forms.ModelForm):

    class Meta:
        model = Ciclo
        plan = forms.TextInput(attrs={'value': PlanDeEstudios})
        fields = [
            'anioCalendario',
            'fechaInicio',
            'fechaFin',
            'plan',
        ]
        #self.fields['plan'].queryset = PlanDeEstudios.objects.filter(esActual= 'True')

        fecha = datetime.strftime(datetime.today(), "%Y-%M-%d")
        widgets = {
        'fechaInicio': forms.TextInput(attrs={'type': 'date', 'value': fecha,'readonly': True}),
        'fechaFin': forms.TextInput(attrs={'type': 'date', 'value': fecha}),
    }
    def clean_fechaFin(self):
        inicio = self.cleaned_data.get("fechaInicio")
        fin = self.cleaned_data.get("fechaFin")
        if inicio >= fin:
            raise forms.ValidationError("fecha ingresada es menor a la de inicio")
        return fin

class CicloForm(forms.ModelForm):

    class Meta:
        model = Ciclo
        plan = forms.TextInput(attrs={'value': PlanDeEstudios})
        fields = [
            'anioCalendario',
            'fechaInicio',
            'fechaFin',
            'plan',
        ]

        fecha = datetime.strftime(datetime.today(), "%Y-%M-%d")
        anios_plan_estudio = PlanDeEstudios.objects.filter(esActual='True')
        widgets = {
        'fechaInicio': forms.TextInput(attrs={'type': 'date', 'value': fecha}),
        'fechaFin': forms.TextInput(attrs={'type': 'date', 'value': fecha}),
    }
    def clean_fechaFin(self):
        inicio = self.cleaned_data.get("fechaInicio")
        fin = self.cleaned_data.get("fechaFin")
        if inicio >= fin:
            raise forms.ValidationError("fecha ingresada es menor a la de inicio")
        return fin
    
    
    def __init__(self, *args, **kwargs):
        super(CicloForm, self).__init__(*args, **kwargs)
        anios_plan_estudio = PlanDeEstudios.objects.filter(esActual='True')
        self.fields['plan'].queryset = anios_plan_estudio

PRIMERA = '1ra'
SEGUNDA = '2da'
TERCERA = '3ra'
CUARTA = '4ta'
CHOICES_DIV = (
    (PRIMERA, 'Primera'),
    (SEGUNDA, 'Segunda'),
    (TERCERA, 'Tercera'),
    (CUARTA, 'Cuarta'),)


anio = forms.DateField(
    required=True,
    label='anio',
    widget=forms.CharField,
    help_text='Anio',
    error_messages={
        'invalid_choice': "La opcion no es valida",
        'required': "el cliente es obligatorio"
    },
    validators=[],

)
class DivisionForm(forms.ModelForm):
    class Meta:
        model = Division
        fields = ['ciclo', 'codigo', 'anio', 'descripcion', 'alumnos']
        widgets = {
            'ciclo': forms.Select(attrs={'class': 'custom-select'}),
            'anio': forms.Select(attrs={'class': 'custom-select'}),
            'estudiante': forms.SelectMultiple(attrs={'class': 'custom-select'}),
        }
        labels = {
            'ciclo': 'Ciclo Lectivo',
            'anio': 'Año',
            'estudiante': 'Estudiantes',
        }
        help_texts = {
            'ciclo': 'Seleccione el ciclo lectivo',
            'anio': 'Seleccione el año académico',
            'estudiante': 'Seleccione los estudiantes',
        }



estudiante = forms.DateField(
    required=True,
    label='estudiante',
    widget=forms.CharField,
    help_text='estudiate',
    error_messages={
        'invalid_choice': "La opcion no es valida",
        'required': "el estudiante es obligatorio"
    },
    validators=[],
)
class inscripcionAlumnoForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        print("acaaaaaaaaaaaaaa")
        # Obtener el plan de estudios y los ciclos desde los kwargs
        #plan_estudio = kwargs.pop('plan_estudio', None)
        
        super(inscripcionAlumnoForm, self).__init__(*args, **kwargs)



    class Meta:
        model = inscripcionEstudianteCiclo
        fields= '__all__'
        widgets_estudiante = autocomplete.ModelSelect2(url='core:estudiante-autocomplete',attrs={'class': 'input-group mb-3'})
        #import ipdb; ipdb.set_trace() 
        # print(widgets_estudiante)
        fecha = datetime.strftime(datetime.today(), "%Y-%M-%d")
        
     
        widgets = {
            'estudiante': widgets_estudiante,
            'fecha': forms.TextInput(attrs={'class': 'datepicker input-group mb-3', 'type': 'date', 'value': fecha}),
            'ciclo': forms.Select(attrs={'class': 'input-group mb-3'}),
            'anio': forms.Select(attrs={'class': 'form-label input-group mb-3 '}),
            
        }

    def __init__(self, *args, **kwargs):
        super(inscripcionAlumnoForm, self).__init__(*args, **kwargs)
        # Obtener la fecha del sistema
        current_date = datetime.now().strftime("%d de %B del %Y")
        # Establecer la fecha del sistema en el campo de fecha del formulario
        #self.fields['fecha'].initial = current_date
        anios_plan_estudio = AnioPlan.objects.filter(plan=PlanDeEstudios.objects.get(esActual= 'True'))
        self.fields['ciclo'].queryset = Ciclo.objects.filter(esActual = 'True')
        self.fields['anio'].queryset = anios_plan_estudio
        

   