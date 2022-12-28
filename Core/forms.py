from django import forms
from Core.models import PlanDeEstudios, EspacioCurricular
from Core.models import AnioPlan
from Core.models import Localidad
from Core.models import Persona,Docente,Estudiante

from datetime import datetime

#   from Cursada.forms import plan

ciclo = forms.DateField(
    required=True,
    label='ciclo',
    widget=forms.CharField,
    help_text='ciclo lectivo',
    error_messages={
        'invalid_choice': "La opcion no es valida",
        'required': "El ciclo lectivo es obligatorio"
    })

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
        ]

    def __init__(self, *args, **kwargs):
        id_plan = kwargs.pop('id_plan', None)
        super(EspacioCurricularForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)

        if instance and instance.id:
             self.fields['contenido'].required = False
             self.fields['contenido'].widget.attrs['disabled'] = True

        self.fields['anio'].queryset = AnioPlan.objects.filter(plan__id=id_plan)
