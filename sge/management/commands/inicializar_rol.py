from django.core.management.base import BaseCommand
from Core.models import Rol  

class Command(BaseCommand):
    help = 'Inicializar la base de datos con un Rol Docente'

    def handle(self, *args, **kwargs):
        rol, created = Rol.objects.get_or_create(name='Docente')
        if created:
            self.stdout.write(self.style.SUCCESS('Rol Docente creado correctamente'))
        else:
            self.stdout.write(self.style.WARNING('El rol Docente ya existe'))
