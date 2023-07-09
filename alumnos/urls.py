from django.urls import path
from . import views

urlpatterns = [
    path('alumnos/', views.StudentView.as_view(), name='alumnos'),
    path('alumno/<int:unique>/changeauth', views.CambiarPasswordAlumno.as_view(), name='alumno'),
    path('alumno/<int:unique>', views.StudentDetail.as_view(), name='alumno'),
    path('alumno/<int:unique>/ficha_medica', views.StudentFichaMedicaView.as_view(), name='alumno'),
    path('alumno/<int:unique>/contactos', views.StudentContactoEmergencia.as_view(), name='alumno'),
    path('alumno/<int:unique>/solicitudes', views.StudentSolicitudCredencialView.as_view(), name='alumno'),
    path('alumno/<int:unique>/solicitudes/generar', views.StudentGenerarSolicitud.as_view(), name='alumno'),
    path('alumno/<int:unique>/micredencial/', views.MyCredencial.as_view(), name='alumno')
]
