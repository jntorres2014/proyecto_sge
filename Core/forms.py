from django import forms
from django.utils import timezone
from Core.models import PlanDeEstudios, EspacioCurricular,AnioPlan,Localidad
from Core.models import Persona,Docente,Estudiante,Ciclo,Division, Inscripcion
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

class PlanDeEstudiosEditForm(forms.ModelForm):
    class Meta:
        model = PlanDeEstudios

        fields = [
            'codigo',
            'anio',
            'orientacion',
            'nivel',
            'descripcion',
        ]
        placeholder ={
            'codigo': 'Ej. 687197716',
            'anio' : 'Ej. 2024',
            'orientacion': 'Ej. Programacion Orientada a objetos',
            'nivel': 'Ej Primario',
            'descripcion' : '',
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
        labels = {
            'codigo': 'Codigo',
            'anio' : 'Año',
            'orientacion':'Orientacion',
            'nivel': 'Nivel',
            'cantidadAnios': 'Cantidad de años',
            'descripcion': 'Descripcion',
        }

    def clean_cantidadAnios(self):
        anios = self.cleaned_data.get("cantidadAnios")
        if anios < 1:
            raise forms.ValidationError("La cantidad de años ingresadas debe ser mayor a cero")
        return anios
class LocalidadForm(forms.ModelForm):

    class Meta:
        model = Localidad

        fields= [
            'codigoPostal',
            'nombre',
        ]



class PersonaForm(forms.ModelForm):
    class Meta:
        model = Persona
        fields= [
            'dni',
            'nombre',
            'apellido',
            'direccion',
            'localidad',
            'email',
            'telefono'
        ]


class DocenteForm(forms.ModelForm):
    class Meta():
        model = Docente
        fields = [
            'dni',
            'nombre',
            'apellido',
            'direccion',
            'localidad',
            'email',
            'telefono',
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
        fields = ['nombre',
                  'apellido',
                  'dni',
                  'legajo',
                  'localidad',
                  'direccion',
                  'email',
                  'telefono',
                  ]

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
        labels = {
            'codigo': 'Codigo',
            'cantidadModulos': 'Cantidad de modulos',
            'nombre' : 'nombre',
            'contenido': 'Contenido',
        }
        widgets = { 
            'plan': forms.Select(attrs={'class': 'input-group mb-3'}),
            'anio': forms.Select(attrs={'class': 'input-group mb-3'}),
            'codigo': forms.TextInput(attrs={'class': 'input-group mb-3'}),
            'cantidadModulos': forms.TextInput(attrs={'class': 'input-group mb-3', 'type': 'number', 'min':'1'}),
            'nombre': forms.TextInput(attrs={'class': 'input-group mb-3'}),
            'contenido': forms.TextInput(attrs={'class': 'input-group mb-3'}),
            
        }

class EspacioCurricularForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        plan_estudio_id = kwargs.pop('id_plan', None)
        print('Plan de estudioooo', plan_estudio_id)
        super(EspacioCurricularForm, self).__init__(*args, **kwargs)
        if plan_estudio_id:
            self.fields['plan'].queryset = PlanDeEstudios.objects.filter(id=plan_estudio_id)

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
        labels={
            'plan': 'Plan de estudio',
            'anio': 'Año',
            'codigo': 'Codigo de Espacio Curricular',
            'cantidadModulos': 'Cantidad de modulos',
            'nombre': 'nombre',
            'contenido': 'Contenido',
        }
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
        print('Plan de estudioooo',id_plan)
        super(EspacioCurricularForm, self).__init__(*args, **kwargs)
        # Obtener la fecha del sistema
        # Establecer la fecha del sistema en el campo de fecha del formulario
        #self.fields['fecha'].initial = current_date
        self.fields['plan'].queryset = PlanDeEstudios.objects.filter(id=id_plan)

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

        ]
        labels = {
            'anioCalendario': 'Año calendario',
            'fechaInicio': 'Fecha de inicio',
            'fechaFin': 'Fecha de fin',

        }
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

#plan_actual = PlanDeEstudios.objects.get(esActual='True')
class CicloForm(forms.ModelForm):

    class Meta:
        model = Ciclo
        fields = [
            'anioCalendario',
            'fechaInicio',
            'fechaFin',
            'plan',
        ]
        labels = {
            'anioCalendario': 'Año Calendario',
            'fechaInicio': 'Fecha de Inicio de ciclo',
            'fechaFin': 'Fecha de fin de ciclo',
            'plan': 'Plan de Estudios',
        }
        widgets = {
            'fechaInicio': forms.DateInput(attrs={'type': 'date'}),
            'fechaFin': forms.DateInput(attrs={'type': 'date'}),
            'plan': forms.HiddenInput(),
        }

    def clean_fechaFin(self):
        inicio = self.cleaned_data.get("fechaInicio")
        fin = self.cleaned_data.get("fechaFin")
        if inicio >= fin:
            raise forms.ValidationError("La fecha de fin debe ser posterior a la fecha de inicio.")
        # Verificar si hay ciclos activos para las fechas proporcionadas
        ciclos_activos = Ciclo.objects.filter(fechaInicio__lte=fin, fechaFin__gte=inicio).exclude(id=self.instance.id)
        if ciclos_activos.exists():
            raise forms.ValidationError("Hay un ciclo activo para las fechas proporcionadas.")
        return fin
    
    def clean_plan(self):
        plan = self.cleaned_data.get("plan")
        if not plan:
            # Si el plan no se proporciona, obtener el plan actual
            plan = PlanDeEstudios.objects.get(esActual=True)
        return plan
    
    def __init__(self, *args, **kwargs):
        super(CicloForm, self).__init__(*args, **kwargs)
        # Obtener el plan de estudios actual y establecerlo como valor inicial para el campo 'plan'
        plan_actual = PlanDeEstudios.objects.get(esActual=True)
        self.fields['plan'].initial = plan_actual.id
        self.fields['plan'].widget.attrs['readonly'] = True

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

    class Meta:
        model = Inscripcion
        fields= '__all__'
        labels = {
            'anio': 'Año'
        }
        widgets_estudiante = autocomplete.ModelSelect2(url='core:estudiante-autocomplete',attrs={'type':'text','class': 'form-label' })
        fecha = datetime.strftime(datetime.today(), "%Y-%M-%d")
        #ciclo = Ciclo.objects.get(esActual = 'True')
     
        widgets = {
            'estudiante': widgets_estudiante,
            'fecha': forms.TextInput(attrs={'class': ' form-label datepicker input-group mb-3', 'type': 'date', 'value': fecha}),
            'anio': forms.Select(attrs={'class': 'form-control input-group mb-3 '}),
            'ciclo': forms.TextInput(attrs={'type': 'hidden', 'readonly':'True', 'Value': 2}),
            
        }
    def clean_fecha(self):
        fecha = self.cleaned_data.get("fecha")
        if fecha > timezone.now():
            raise forms.ValidationError("La fecha ingresada es mayor al día de hoy")
        return fecha

    def __init__(self, *args, **kwargs):
        super(inscripcionAlumnoForm, self).__init__(*args, **kwargs)
        # Obtener la fecha del sistema
        current_date = datetime.now().strftime("%d de %B del %Y")
        # Establecer la fecha del sistema en el campo de fecha del formulario
        #self.fields['fecha'].initial = current_date
        anios_plan_estudio = AnioPlan.objects.filter(plan=PlanDeEstudios.objects.get(esActual= 'True'))
        self.fields['ciclo'].queryset = Ciclo.objects.filter(esActual = 'True')
        self.fields['anio'].queryset = anios_plan_estudio
        

   