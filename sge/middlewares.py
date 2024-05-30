from django.utils import timezone
from Core.models import Ciclo, PlanDeEstudios

class AgregarPlanAlContextoMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        fecha_actual = timezone.now().date()
        ciclos_activos = Ciclo.objects.filter(fechaInicio__lte=fecha_actual, fechaFin__gte=fecha_actual)
        if ciclos_activos.exists():
            ciclo_activo = ciclos_activos.first()
            print("HAY CICLOOOOOOO1", ciclo_activo)
            request.hayCicloActivo = True
        else:
            ciclo_activo = None
            
        # Intentar obtener el plan actual
        try:
            plan = PlanDeEstudios.objects.get(esActual=True)
        except PlanDeEstudios.DoesNotExist:
            plan = None
        
        # Agregar el plan y ciclo al contexto de renderizado
        request.plan = plan
        request.ciclo = ciclo_activo

        response = self.get_response(request)
        return response
