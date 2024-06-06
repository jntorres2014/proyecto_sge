from datetime import datetime
from django import forms
from Core.models import Calificacion, Ciclo, Detalle_Horario, EspacioCurricular, Estudiante, Horario, Instancia, PlanDeEstudios
from dal import autocomplete
from Clases.models import Inasistencias
from django.utils import timezone


class CalificacionForm(forms.ModelForm):

    class Meta:
        model = Calificacion
        fields= {
            'espacioCurricular',
            'estudiante',
            'nota',
            'tipo',
            'instancia',
        }
        
    def __init__(self, *args, **kwargs):
        espacios = kwargs.pop('espacios', None)
        estudiantes = kwargs.pop('estudiantes', None)
        super(CalificacionForm, self).__init__(*args, **kwargs)
        print('Espacioooos',espacios)
        if espacios:
            choices = [(espacio.id, espacio.espacioCurricular) for espacio in espacios]
            self.fields['espacioCurricular'].widget.choices = choices
        if estudiantes:
            choices = [(estudiante.id, estudiante.nombre) for estudiante in estudiantes]
            self.fields['estudiante'].widget.choices = choices

class HabilitarInstanciaForm(forms.ModelForm):
    fecha_fin = forms.DateField(label='Fecha Fin', widget=forms.TextInput(attrs={'type': 'date'}))

    class Meta:
        model = Instancia
        fields = ['fecha_fin']        

class InasistenciasForm(forms.ModelForm):
    class Meta:
        model= Inasistencias
        fields={
            'estudiante',
            'dia',
            'falta',
            'justificacion',

        }
class InstanciaForm(forms.ModelForm):
    class Meta:
        model= Instancia
        fields={
        'nombre',
        'fecha_inicio',
        'fecha_fin',
        'disponible',        
        'ciclo'
        }
        labels={
            'nombre': 'Nombre',
            'fecha_inicio': 'Fecha de inicio',
            'fecha_fin': 'Fecha de finalizacion',
            'disponible': 'Disponible',            
            'ciclo': 'Ciclo actual'
        }
        fecha = datetime.strftime(datetime.today(), "%Y-%M-%d")
        widgets = {
            'fecha_inicio': forms.TextInput(attrs={'class': 'datepicker input-group mb-3', 'type': 'date', 'value': fecha}),
            'fecha_fin': forms.TextInput(attrs={'class': 'datepicker input-group mb-3', 'type': 'date', 'value': fecha}),  
        }
        
 

class Detalle_HorarioForm(forms.ModelForm):
    class Meta:
        model= Detalle_Horario
        fields=[
            'horario',
            'espacioCurricular',
            'dia',
            'hora',
            'docente'
            
        ]
        
        labels={
            'espacioCurricular': 'Espacio Curricular',
            'hora': 'Modulo'
        }
        widgets_docente = autocomplete.ModelSelect2(url='core:docenteHora-autocomplete',forward=['horario'],attrs={'class': 'form-select'})
        widgets_espacio = autocomplete.ModelSelect2(url='core:espacio-autocomplete',forward=['horario'],attrs={'class': 'form-select'})
        fecha = datetime.strftime(datetime.today(), "%Y-%M-%d")
        
     
        widgets = {
            
            #'horario': forms.TextInput(attrs={'type':'hidden', 'class': 'input-group con-mv-4', 'id':'id_division','onchange':'cargarDatosHorario()'}),
            'hora': forms.Select(attrs={'class': 'input-group con-mv-4'}),
            'espacioCurricular': widgets_espacio,
            'docente': widgets_docente,
            'dia': forms.TextInput(attrs={'class': 'input-group mb-3'}),   

        }

    def clean(self):
        cleaned_data = super().clean()
        dia = cleaned_data.get("dia")
        hora = cleaned_data.get("hora")
        docente = cleaned_data.get("docente")
        
        # Verificar si el docente ya está asignado en otro horario en el mismo día y módulo
        if Detalle_Horario.objects.filter(docente=docente, dia=dia, hora=hora).exists():
            raise forms.ValidationError("El docente ya está asignado en otro horario en el mismo día y módulo.")
        
        return cleaned_data
    def __init__(self, *args, **kwargs):
        division = kwargs.pop('division', None)
        super(Detalle_HorarioForm, self).__init__(*args, **kwargs)
        

        # # Personaliza el widget para el campo 'dia'
        self.fields['dia'].widget = forms.Select(choices=Horario.CHOICES_DIA)
        self.fields['espacioCurricular'].queryset = EspacioCurricular.objects.filter(anio_id= division.anio_id)
        horario = Horario.objects.get(division_id= division.id)
        self.fields['horario'] = forms.ModelChoiceField(queryset=Horario.objects.filter(division_id= division.id), initial=horario, widget=forms.HiddenInput())
        #self.fields['horario'].queryset = Horario.objects.filter(division_id= division.id)

        # # Personaliza el widget para el campo 'hora'
        self.fields['hora'].widget = forms.Select(choices=Horario.CHOICES_HORA)

class ReporteForm(forms.Form):
    plan = forms.ModelChoiceField(queryset=PlanDeEstudios.objects.all(), required=True)
    ciclo = forms.ModelChoiceField(queryset=Ciclo.objects.none(), required=False)
    instancia = forms.ModelChoiceField(queryset=Instancia.objects.none(), required=False)

    def __init__(self, *args, **kwargs):
        super(ReporteForm, self).__init__(*args, **kwargs)
        if 'plan' in self.data:
            try:
                plan_id = int(self.data.get('plan'))
                self.fields['ciclo'].queryset = Ciclo.objects.filter(plan_id=plan_id).order_by('anioCalendario')
                if 'ciclo' in self.data:
                    ciclo_id = int(self.data.get('ciclo'))
                    self.fields['instancia'].queryset = Instancia.objects.filter(ciclo_id=ciclo_id).order_by('nombre')
            except (ValueError, TypeError):
                pass
        else:
            self.fields['ciclo'].queryset = Ciclo.objects.none()
            self.fields['instancia'].queryset = Instancia.objects.none()

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
