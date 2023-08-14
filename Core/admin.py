from django.contrib import admin

# Register your models here.
from .models import Estudiante,inscripcionEstudianteCiclo

class EstudianteAdmin(admin.ModelAdmin):
    #readonly_fields = ("created",)
    readonly_fields = []
class inscripcionAdmin(admin.ModelAdmin):
    #readonly_fields = ("created")
    readonly_fields  = []

admin.site.register(Estudiante,EstudianteAdmin)

admin.site.register(inscripcionEstudianteCiclo,inscripcionAdmin)

# Register your models here.
