from django.urls import re_path
from django.urls import path

from . import views


urlpatterns = [
    re_path(r'^altaLocalidad$', views.localidad_view, name='altaLocalidad'),
    re_path(r'^verLocalidad$', views.localidad_list.as_view(), name='verLocalidad'),
    re_path(r'^modificarLocalidad/(?P<id_localidad>\d+)/$', views.localidad_edit, name='modificarLocalidad'),

    re_path(r'^altaDocente$', views.docente_view, name='altaDocente'),
    re_path(r'^verDocentes$', views.docente_list.as_view(), name='verDocentes'),
    re_path(r'^modificarDocente/(?P<id_docente>\d+)/$', views.docente_edit, name='modificarDocente'),

    re_path(r'^altaEstudiante$', views.Estudiante_view, name='altaEstudiante'),
    re_path(r'^verEstudiantes$', views.estudiante_list.as_view(),name='verEstudiantes'),
    re_path(r'^modificarEstudiante/(?P<id_estudiante>\d+)/$', views.estudiante_edit, name='modificarEstudiante'),

    re_path(r'^altaPlan$', views.plan_de_estudios_view,name='altaPlan'),
    re_path(r'^verPlan$', views.plan_list.as_view(), name= 'verPlan'),
    re_path(r'^modificarPlan/(?P<id_plan>\d+)/$', views.plan_edit, name='modificarPlan'),

    re_path(r'agregarEspacio/(?P<id_plan>\d+)/$', views.Espacio_view,name= 'agregarEspacio'),

    re_path(r'^altaEspacio$', views.Espacio_view,name='altaEspacio'),

    re_path(r'^verEspacios$', views.Espacio_list.as_view(), name='verEspacios'),
    re_path(r'^modificarEspacio/(?P<id_espacio>\d+)/$', views.espacio_edit, name='modificarEspacio'),
    path('ajax/cargar-espacios/', views.cargar_espacios, name='ajax_cargar_espacios'),

]