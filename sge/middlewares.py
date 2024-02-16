


from Core.models import Ciclo, PlanDeEstudios


class AgregarPlanAlContextoMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Obtener el plan desde donde sea que lo tengas almacenado
        plan = PlanDeEstudios.objects.get(esActual='True')  # Aquí debes colocar tu lógica para obtener el plan
        ciclo = Ciclo.objects.get(esActual='True')
        # print("ciclo",ciclo, plan)
        # Agregar el plan al contexto de renderizado
        request.plan = plan
        request.ciclo = ciclo

        response = self.get_response(request)
        return response
