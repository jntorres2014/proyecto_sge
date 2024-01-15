from django import forms
from Core.models import Calificacion, Horario
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

class HorarioForm(forms.ModelForm):
    class Meta:
        model= Horario
        fields={
            'espacioCurricular',
            'division',
            'hora',
            'dia',

        }
    def __init__(self, *args, **kwargs):
        super(HorarioForm, self).__init__(*args, **kwargs)

        # Personaliza el widget para el campo 'dia'
        self.fields['dia'].widget = forms.Select(choices=Horario.CHOICES_DIA)

        # Personaliza el widget para el campo 'hora'
        horas_choices = [(1, '7:00 a 7:45'), (2, '7:45 a 8:20')]
        self.fields['hora'].widget = forms.Select(choices=horas_choices)