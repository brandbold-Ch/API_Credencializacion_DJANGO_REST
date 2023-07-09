from django.urls import path
from . import views

urlpatterns = [

    path('carreras/', views.ProfessionView.as_view(), name='carrera'),
    path('grado_estudio/', views.GradoEstudioView.as_view(), name='grado_estudio'),
    path('cuatrimestres/', views.CuatrimestreView.as_view(), name='cuatrimestre'),

    path('administradores/', views.AdminView.as_view(), name='administradores'),
    path('administrador/<int:unique>', views.AdminDetailView.as_view(), name='administrador'),
    path('administrador/<int:unique>/changeauth', views.ChangePasswordAdminView.as_view(), name='administrador'),
    path('administrador/<int:unique>/contactos', views.AdminContactEmergencyView.as_view(), name='administrador'),
    path('administrador/<int:unique>/ficha_medica', views.AdminMedicalRecordView.as_view(), name='administrador'),
    path('administrador/<int:unique>/credencial/<str:user>/<int:other>/<str:option>', views.ActivateCredentialView.as_view(), name='administrador'),
    path('administrador/<int:unique>/solicitud/<str:user>/<int:other>/<str:option>', views.ValidateRequestView.as_view(), name='administrador'),
    path('administrador/<int:unique>/solicitudes/<str:user>/<str:status>', views.ListadoSolicitudesView.as_view(), name='administrador'),

    path('administrador/<int:unique>/alumnos', views.ListadoAlumnos.as_view(), name='administrador'),
    path('administrador/<int:unique>/alumno/<int:other>', views.ListadoDetailAlumno.as_view(), name='administrador'),


    path('administrador/<int:unique>/directivos', views.ListadoDirectivos.as_view(), name='administrador'),
    path('administrador/<int:unique>/directivo/<int:other>', views.ListadoDetailDirectivo.as_view(), name='administrador'),

    path('administrador/<int:unique>/maestros', views.ListadoMaestros.as_view(), name='administrador'),
    path('administrador/<int:unique>/maestro/<int:other>', views.ListadoDetailMaestro.as_view(), name='administrador'),
]
