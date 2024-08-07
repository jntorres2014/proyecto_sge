from datetime import datetime
from django import forms
from Core.models import Calificacion, Ciclo, Detalle_Horario, EspacioCurricular, Estudiante, Horario, InscripcionDocente, Instancia, PlanDeEstudios
from dal import autocomplete
from Clases.models import Inasistencias
from django.utils import timezone

class CalificacionForm(forms.ModelForm):

    class Meta:
        model = Calificacion
        fields = ['espacioCurricular', 'estudiante', 'nota', 'instancia']
        labels={
            'espacioCurricular': 'Espacio Curricular',
            'estudiante': 'Estudiante',
            'nota': 'Calificacion',            
        }
        widgets = {
            'espacioCurricular': forms.Select(attrs={'class': 'form-control input-group mb-3'}),
            # 'tipo': forms.Select(attrs={'class': 'form-control input-group mb-3'}),
            'instancia': forms.Select(attrs={'class': 'form-control input-group mb-3'}),
             'estudiante': autocomplete.ModelSelect2(url='core:estudiantes-autocomplete-aula', forward=['estudiantes'], attrs={'class': 'form-control input-group mb-3'}),
            'estudiante': forms.Select(attrs={'class': 'form-control input-group mb-3' }),

            'nota': forms.TextInput(attrs={'type':'number', 'class': 'form-control input-group mb-3','max':'10','min':'1'})
        }

    def __init__(self, *args, **kwargs):
        espacios = kwargs.pop('espacios', None)
        estudiantes = kwargs.pop('estudiantes', None)
        super(CalificacionForm, self).__init__(*args, **kwargs)
        self.fields['instancia'].queryset = Instancia.objects.filter(disponible=True)
        
        if espacios:
            unique_espacios = []
            for espacio in espacios:
                first_instance = Detalle_Horario.objects.filter(espacioCurricular=espacio['espacioCurricular']).first()
                if first_instance:  # Asegúrate de que hay al menos una instancia
                    unique_espacios.append((first_instance.espacioCurricular.id, first_instance.espacioCurricular))
            self.fields['espacioCurricular'].choices = unique_espacios
        
        if estudiantes:
            choices = [(estudiante.id, estudiante.nombre + ' ' + estudiante.apellido) for estudiante in estudiantes]
            self.fields['estudiante'].choices = choices
        else:
            self.fields['estudiante'].choices = []

class HabilitarInstanciaForm(forms.ModelForm):
    fecha_fin = forms.DateField(label='Fecha Fin', widget=forms.TextInput(attrs={'type': 'date'}))

    class Meta:
        model = Instancia
        fields = ['fecha_fin']        
    
    def clean_fecha_fin(self):
        fecha = datetime.strftime(datetime.today(), "%Y-%M-%d")
        fin = self.cleaned_data.get("fecha_fin")
        print("Estoy acaaaaa")
        print('fin',fin, type(fin))

        print('hoy',fecha, type(fecha))
        if   fin >= fecha:
            raise forms.ValidationError("fecha ingresada es menor a la fecha actual")
    
        return fin
class InasistenciasForm(forms.ModelForm):
    class Meta:
        model= Inasistencias
        fields=[
            'estudiante',
            'dia',
            'falta',
            'justificacion',]
        
class InstanciaForm(forms.ModelForm):
    fecha = datetime.today().date()
    fecha_inicio = forms.DateField(label='Fecha Inicio', widget=forms.TextInput(attrs={'type': 'date','value': fecha}))
    fecha_fin = forms.DateField(label='Fecha Fin', widget=forms.TextInput(attrs={'type': 'date','value': fecha}))
    class Meta:
        model= Instancia
        fields=[
        'nombre',
        'fecha_inicio',
        'fecha_fin',
        'ciclo',
        'disponible'        
        ]
        labels={
            'nombre': 'Nombre',
            'ciclo': 'Ciclo actual',
            'disponible': 'Disponible',            
        }
            
    def clean_fecha_fin(self):
        inicio = self.cleaned_data.get("fecha_inicio")
        inicio = datetime.today().date()
        fin = self.cleaned_data.get("fecha_fin")
        #import pdb; pdb.set_trace()
        
        print('inicio', inicio)
        print("tipossss",type(inicio),type(fin))
        print('fin',fin)
        if inicio >= fin:
            raise forms.ValidationError("fecha ingresada es menor a la de inicio")
    
        return fin
 

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
        espacio_curricular = cleaned_data.get('espacioCurricular')
        docente = cleaned_data.get("docente")
        horario = cleaned_data.get("horario")
        ciclo= Ciclo.objects.filter(fechaInicio__lte=timezone.now(), fechaFin__gte=timezone.now()).first()
        inscripciones = InscripcionDocente.objects.filter(docente= docente,ciclo=ciclo)
        anios_inscritos = inscripciones.values_list('anio_id', flat=True)
        Detalle_Horario.objects.filter(docente=docente, horario__division__anio__in=anios_inscritos)
        # Verificar si el docente ya está asignado en otro horario en el mismo día y módulo
        if Detalle_Horario.objects.filter(horario = horario,docente=docente, dia=dia, hora=hora).exists():
            raise forms.ValidationError("El docente ya está asignado en otro horario en el mismo día y módulo.")
        if espacio_curricular and dia and horario:
            # Obtener la cantidad de módulos permitidos para el espacio curricular
            cantidad_modulos_permitidos = espacio_curricular.cantidadModulos

            # Calcular cuántos módulos están asignados para este espacio en este horario
            cant = Detalle_Horario.objects.filter(
                horario = horario,
                espacioCurricular=espacio_curricular,
            ).count()
            
            print("cantidad", cant, cantidad_modulos_permitidos)
            # Comparar con la cantidad máxima permitida
            if  cant > cantidad_modulos_permitidos:
                raise forms.ValidationError(f"El espacio curricular '{espacio_curricular}' ya tiene asignados todos los módulos permitidos ({cantidad_modulos_permitidos}) para este horario y día.")
        return cleaned_data
    def __init__(self, *args, **kwargs):
        division = kwargs.pop('division', None)
        super(Detalle_HorarioForm, self).__init__(*args, **kwargs)
        

        # # Personaliza el widget para el campo 'dia'
        self.fields['dia'].widget = forms.Select(choices=Horario.CHOICES_DIA)
        print("en teoria es el id del año",division.anio.id)
        self.fields['espacioCurricular'].queryset = EspacioCurricular.objects.filter(anio_id= division.anio.id)
        horario = Horario.objects.get(division = division)
        print("Esta es la division", division.id,"Año", horario)
        self.fields['horario'] = forms.ModelChoiceField(queryset=Horario.objects.filter(division= division), initial=horario.id, widget=forms.HiddenInput())
        #self.fields['horario'].queryset = Horario.objects.filter(division_id= division.id)

        # # Personaliza el widget para el campo 'hora'
        self.fields['hora'].widget = forms.Select(choices=Horario.CHOICES_HORA)

class ReporteForm(forms.Form):
    plan = forms.ModelChoiceField(queryset=PlanDeEstudios.objects.all(), required=True,widget=forms.Select(attrs={'class': 'form-control'}))
    ciclo = forms.ModelChoiceField(queryset=Ciclo.objects.none(), required=False,widget=forms.Select(attrs={'class': 'form-control'}))
    instancia = forms.ModelChoiceField(queryset=Instancia.objects.none(), required=False,widget=forms.Select(attrs={'class': 'form-control'}))

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
