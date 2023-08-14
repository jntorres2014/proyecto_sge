from django import forms
from Core.models import PlanDeEstudios, EspacioCurricular
from Core.models import AnioPlan
from Core.models import Localidad
from Core.models import Persona,Docente,Estudiante,Ciclo,Division, inscripcionEstudianteCiclo

from dal import autocomplete

from datetime import datetime

#   from Cursada.forms import plan

# ciclo = forms.DateField(
#     required=True,
#     label='ciclo',
#     widget=forms.CharField,
#     help_text='ciclo lectivo',
#     error_messages={
#         'invalid_choice': "La opcion no es valida",
#         'required': "El ciclo lectivo es obligatorio"
#     })

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


Localidad = forms.DateField(
    required=True,
    label='Localidad',
    widget=forms.CharField,
    help_text='Localidad',
    error_messages={
        'invalid_choice': "La opcion no es valida",
        'required': "La localidad es obligatorio"
    })


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
    #os = autocomplete_light.ChoiceField('OsAutocomplete')    
    class Meta:
        model = Estudiante
        fields = [
            'Dni',
            'Nombre',
            'Apellido',
            'Direccion',
            'Localidad',
            'Email',
            'Telefono',
            'legajo',
            'fechaInscripcion',
        ]
        fecha = datetime.strftime(datetime.today(), "%Y-%M-%d")
        widgets = {
            'fechaInscripcion': forms.TextInput(attrs={'type': 'date', 'value': fecha})
        }

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
    class Meta:
        model= EspacioCurricular
        fields= [
            'anio',
            'codigo',
            'cantidadModulos',
            'nombre',
            'contenido',
            'plan'
        ]
        widgets = {
           # 'estudiante': widgets_estudiante
        }

        

    def __init__(self, *args, **kwargs):
        id_plan = kwargs.pop('id_plan', None)
        super(EspacioCurricularForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)

        if instance and instance.id:
             self.fields['contenido'].required = False
             self.fields['contenido'].widget.attrs['disabled'] = True

        self.fields['anio'].queryset = AnioPlan.objects.filter(plan__id=id_plan)


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
        fields= [
            'ciclo',
            'codigo',
            'anio',
            'descripcion',
        ]

ciclo = forms.DateField(
    required=True,
    label='ciclo',
    widget=forms.CharField,
    help_text='ciclo lectivo',
    error_messages={
        'invalid_choice': "La opcion no es valida",
        'required': "El ciclo lectivo es obligatorio"
    })


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
    class Meta:
        model = inscripcionEstudianteCiclo
        fields= '__all__'
        widgets_estudiante = autocomplete.ModelSelect2(url='estudiante-autocomplete')
        widgets = {
            'fecha': forms.DateInput(attrs={'disabled': True}),
           # 'estudiante': widgets_estudiante
        }

    if estudiante:
        #widget_cliente = forms.TextInput(attrs={'value': cliente})
        widget_estudiante = autocomplete.ModelSelect2(url='/estudiante-autocomplete/?q={}')
