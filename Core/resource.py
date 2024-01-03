from import_export import resources  
from .models import Localidad  


class LocalidadResource(resources.ModelResource):  
    class Meta:  
        model = Localidad  