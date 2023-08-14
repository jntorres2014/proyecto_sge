"""sge URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include, re_path
from principal import views

from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.signin, name= 'login' ),
    path('home2', views.home2, name= 'home2' ),
    
    path('signup/', views.signup, name= 'signup' ),
    path('principal/', views.principal, name= 'principal'),
    path('principal/<int:id>', views.principal_detail, name= 'principal_detail'),
    path('principal/<int:id>/complete', views.complete, name= 'complete'),
    path('principal/<int:id>/delete', views.delete, name= 'delete'),
    path('inscripciones/', views.inscripciones, name= "inscripciones"),

    path('logout/', views.signout, name= 'logout'),
    path('signin/', views.signin, name= 'login'),
    path('task/create', views.create_task, name= 'create_task'),
    re_path(r'^Core/', include('Core.urls')),
    re_path(r'^Clases/', include('Clases.urls')),
    # path('autocomplete/', views.inscripciones.as_view(), name='my_autocomplete'),
    
    # path('altaLocalidad/', views.localidad_view, name='altaLocalidad'),
    # path(r'^verLocalidad$', views.localidad_list.as_view(), name='verLocalidad'),
    # path(r'^modificarLocalidad/(?P<id_localidad>\d+)/$', views.localidad_edit, name='modificarLocalidad'),

    # path(r'^altaDocente$', views.docente_view, name='altaDocente'),
    # path(r'^verDocentes$', views.docente_list.as_view(), name='verDocentes'),
    # path(r'^modificarDocente/(?P<id_docente>\d+)/$', views.docente_edit, name='modificarDocente'),

    # path(r'^altaEstudiante$', views.Estudiante_view, name='altaEstudiante'),
    # path(r'^verEstudiantes$', views.estudiante_list.as_view(),name='verEstudiantes'),
    # path(r'^modificarEstudiante/(?P<id_estudiante>\d+)/$', views.estudiante_edit, name='modificarEstudiante'),

    # path(r'^altaPlan$', views.plan_de_estudios_view,name='altaPlan'),
    # path(r'^verPlan$', views.plan_list.as_view(), name= 'verPlan'),
    # path(r'^modificarPlan/(?P<id_plan>\d+)/$', views.plan_edit, name='modificarPlan'),

    # path(r'agregarEspacio/(?P<id_plan>\d+)/$', views.Espacio_view,name= 'agregarEspacio'),

    # path(r'^altaEspacio$', views.Espacio_view,name='altaEspacio'),

    # path(r'^verEspacios$', views.Espacio_list.as_view(), name='verEspacios'),
    # path(r'^modificarEspacio/(?P<id_espacio>\d+)/$', views.espacio_edit, name='modificarEspacio'),
    # path('ajax/cargar-espacios/', views.cargar_espacios, name='ajax_cargar_espacios'),

    
]
