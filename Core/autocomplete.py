# En un archivo llamado autocomplete.py dentro de la app donde está tu modelo

import autocomplete_light as al

from .models import Estudiante

class MiModeloAutocomplete(al.AutocompleteModelBase):
    search_fields = ['Localidad']

al.register(Estudiante, MiModeloAutocomplete)
