from django.urls import path
from . import views

urlpatterns = [
    path('login/administrador/', views.LoginAdministrador.as_view(), name='login_admin'),
    path('login/alumno/', views.LoginAlumno.as_view(), name='login_alumno'),
    path('login/directivo/', views.LoginDirectivo.as_view(), name='login_directivo'),
    path('login/maestro/', views.LoginMaestro.as_view(), name='login_maestro')
]
