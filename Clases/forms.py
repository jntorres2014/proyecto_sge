from datetime import datetime
from django import forms
from Core.models import Calificacion, Detalle_Horario, EspacioCurricular, Estudiante, Horario,Division
from dal import autocomplete
from Clases.models import Inasistencias
from django.utils import timezone


class CalificacionForm(forms.ModelForm):

    class Meta:
        model = Calificacion

        fields= [
            'tipo',
            'espacioCurricular',
            'docente',
            'estudiante',
            'nota',

        ]


class InasistenciasForm(forms.ModelForm):
    class Meta:
        model= Inasistencias
        fields={
            'estudiante',
            'dia',
            'falta',
            'justificacion',

        }

class Detalle_HorarioForm(forms.ModelForm):
    class Meta:
        model= Detalle_Horario
        fields=[
            'horario',
            'espacioCurricular',
            'dia',
            'hora',
            
        ]
        
        labels={
            'espacioCurricular': 'Espacio Curricular',
            'hora': 'Modulo'
        }

        widgets_espacio = autocomplete.ModelSelect2(url='core:espacio-autocomplete',attrs={'class': 'input-group mb-3'})
        fecha = datetime.strftime(datetime.today(), "%Y-%M-%d")
        
     
        widgets = {
            
            #'horario': forms.TextInput(attrs={'type':'hidden', 'class': 'input-group con-mv-4', 'id':'id_division','onchange':'cargarDatosHorario()'}),
            'hora': forms.Select(attrs={'class': 'input-group con-mv-4'}),
            #'espacioCurricular': widgets_espacio,
          
            'dia': forms.TextInput(attrs={'class': 'input-group mb-3'}),   

        }

    def __init__(self, *args, **kwargs):
        division = kwargs.pop('division', None)
        super(Detalle_HorarioForm, self).__init__(*args, **kwargs)
        

        # # Personaliza el widget para el campo 'dia'
        self.fields['dia'].widget = forms.Select(choices=Horario.CHOICES_DIA)
        self.fields['espacioCurricular'].queryset = EspacioCurricular.objects.filter(anio_id= division.anio_id)
        self.fields['horario'].queryset = Horario.objects.filter(division_id= division.id)

        # # Personaliza el widget para el campo 'hora'
        self.fields['hora'].widget = forms.Select(choices=Horario.CHOICES_HORA)


class ConsultaForm(forms.Form):

    fields = [
        'fecha_inicio',
        'fecha_fin',
        'estudiante'
    ]
    labels={
            'estudiante': 'Estudiante'
        }

    fecha_inicio= forms.CharField(label='Fecha de Inicio', max_length=100)
    fecha_fin= forms.CharField(label='Fecha fin', max_length=100)
    widgets_estudiante=autocomplete.ModelSelect2(url='core:estudiante-autocomplete', attrs={'class': 'input-group mb-3'})
    #estudiante = autocomplete.ModelSelect2(url='core:estudiante-autocomplete',attrs={'class': 'input-group mb-3'})
    fecha = datetime.strftime(datetime.today(), "%Y-%M-%d")
    estudiante = forms.ModelChoiceField(
        queryset=Estudiante.objects.all(),
        widget=forms.Select(attrs={'class': 'input-group mb-3'})
    )
        
     
    widgets = {
            #'estudiante': widgets_estudiante,
            'fecha_inicio': forms.TextInput(attrs={'class': 'datepicker input-group mb-3', 'type': 'date', 'value': fecha}),
            'fecha_fin': forms.TextInput(attrs={'class': 'datepicker input-group mb-3', 'type': 'date', 'value': fecha}),  
        }
    def clean_fecha_fin(self):
        fecha = self.cleaned_data.get("fecha_fin")
        if fecha > timezone.now():
            raise forms.ValidationError("La fecha ingresada es mayor al día de hoy")
        return fecha
