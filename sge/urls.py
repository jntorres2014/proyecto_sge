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
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login', views.signin, name= 'login' ),
    path('', views.home2, name= '' ),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='password_change_form.html'), name='password_change'),
    path('reset_password/', views.CustomPasswordChangeView.as_view(),  name='reset_password'),
        path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'), name='password_change_done'),
    path('reset_password_done/', views.PasswordResetDoneView.as_view(), name='reset_password_done'),
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_pass_complete/',views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('signup/', views.signup, name= 'signup' ),
    path('principal/', views.principal, name= 'principal'),
    path('principal/<int:id>', views.principal_detail, name= 'principal_detail'),
    path('principal/<int:id>/complete', views.complete, name= 'complete'),
    path('principal/<int:id>/delete', views.delete, name= 'delete'),
    path('cambiar-contrasena/', views.CustomPasswordChangeView.as_view(), name='cambiar-contrasena'),    
    path('logout/', views.signout, name= 'logout'),
    path('signin/', views.signin, name= 'login'),
    path('task/create', views.create_task, name= 'create_task'),
    re_path(r'^Core/', include('Core.urls', namespace="core")),
    re_path(r'^Clases/', include('Clases.urls', namespace="clases")),

    
]