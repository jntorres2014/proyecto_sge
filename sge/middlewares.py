from django.utils import timezone
from Core.models import Ciclo, PlanDeEstudios


class AgregarPlanAlContextoMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        hay_ciclo = Ciclo.objects.exists()
        if hay_ciclo:
            try:
                ciclo_activo =  Ciclo.objects.get(esActual='True')
                print("HAY CICLOOOOOOO1",ciclo_activo)
            except Ciclo.DoesNotExist:
                pass
        else:
            ciclo_activo = 'No hay ciclos activos'
        print('ciclo')
        # Obtener el plan desde donde sea que lo tengas almacenado
        hay_ciclo = PlanDeEstudios.objects.exists()
        plan = PlanDeEstudios.objects.get(esActual='True')  # Aquí debes colocar tu lógica para obtener el plan
        #ciclo = Ciclo.objects.get(esActual='True')
        # print("ciclo",ciclo, plan)
        # Agregar el plan al contexto de renderizado
        request.plan = plan
        request.ciclo = ciclo_activo

        response = self.get_response(request)
        return response
