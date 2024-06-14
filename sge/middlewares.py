from django.db import OperationalError
from django.utils import timezone
from Core.models import Ciclo, PlanDeEstudios

class AgregarPlanAlContextoMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        fecha_actual = timezone.now().date()
        ciclo_activo = None
        plan = None
        
        # Intentar obtener el ciclo activo
        try:
            ciclos_activos = Ciclo.objects.filter(fechaInicio__lte=fecha_actual, fechaFin__gte=fecha_actual)
            if ciclos_activos.exists():
                ciclo_activo = ciclos_activos.first()
                request.hayCicloActivo = True
            else:
                request.hayCicloActivo = False
        except OperationalError as e:
            print(f"Error al obtener el ciclo activo: {e}")
            request.hayCicloActivo = False

        # Intentar obtener el plan actual
        try:
            plan = PlanDeEstudios.objects.get(esActual=True)
            request.hayPlan = True
        except PlanDeEstudios.DoesNotExist:
            plan = None
            request.hayPlan = False
        except OperationalError as e:
            print(f"Error al obtener el plan de estudios: {e}")
            plan = None
            request.hayPlan = False

        # Agregar el plan y ciclo al contexto de renderizado
        request.plan = plan
        request.ciclo = ciclo_activo

        response = self.get_response(request)
        return response
