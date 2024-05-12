from django.utils import timezone
from Core.models import Ciclo, PlanDeEstudios

class AgregarPlanAlContextoMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        hay_ciclo = Ciclo.objects.exists()
        if hay_ciclo:
            try:
                ciclo_activo = Ciclo.objects.get(esActual=True)
                print("HAY CICLOOOOOOO1", ciclo_activo)
            except Ciclo.DoesNotExist:
                ciclo_activo = 'No hay ciclos activos'
        else:
            ciclo_activo = 'No hay ciclos activos'
            
        # Intentar obtener el plan actual
        try:
            plan = PlanDeEstudios.objects.get(esActual=True)
        except PlanDeEstudios.DoesNotExist:
            plan = "No hay plan actual"
        
        # Agregar el plan y ciclo al contexto de renderizado
        request.plan = plan
        request.ciclo = ciclo_activo

        response = self.get_response(request)
        return response
