from django import forms
from Core.models import Calificacion, Detalle_Horario, EspacioCurricular, Horario,Division
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

class Detalle_HorarioForm(forms.ModelForm):
    class Meta:
        model= Detalle_Horario
        fields='__all__'
        widgets = {
            'horario': forms.Select(attrs={'class': 'input-group con-mv-4', 'id':'id_division','onchange':'cargarDatosHorario()'}),
            'hora': forms.Select(attrs={'class': 'input-group con-mv-4'}),
            'espacioCurricular': forms.Select(attrs={'class': 'input-group con-mv-4'}),
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