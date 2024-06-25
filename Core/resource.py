from import_export import resources  
from .models import Localidad , EspacioCurricular


class LocalidadResource(resources.ModelResource):  
    class Meta:  
        model = Localidad  


class EspacioCurricularResource(resources.ModelResource):
    class Meta:
        model = EspacioCurricular
        fields = ('id', 'anio__id', 'codigo', 'cantidadModulos', 'nombre', 'contenido', 'plan__id')
        export_order = ('id', 'anio__id', 'codigo', 'cantidadModulos', 'nombre', 'contenido', 'plan__id')
        # Incluye los campos de las claves foráneas para asegurar que se manejen correctamente
        import_id_fields = ('anio__id', 'plan__id')  # Claves primarias de AnioPlan y PlanDeEstudios

    def before_import_row(self, row, **kwargs):
        # Convertir valores de anio_id y plan_id a enteros si es necesario
        if 'anio__id' in row:
            row['anio__id'] = int(row['anio__id']) if row['anio__id'] else None
        if 'plan__id' in row:
            row['plan__id'] = int(row['plan__id']) if row['plan__id'] else None