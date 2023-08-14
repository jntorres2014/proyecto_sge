from django import forms
from Core.models import Calificacion
from Clases.models import Inasistencias


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