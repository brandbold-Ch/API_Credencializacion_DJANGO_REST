from django.urls import path
from . import views

urlpatterns = [
    path('maestros/', views.MaestroView.as_view(), name='maestros'),
    path('maestro/<int:pk>/changeauth', views.CambiarPasswordMaestro.as_view(), name='maestro'),
    path('maestro/<int:pk>', views.MaestroDetail.as_view(), name='maestro'),
    path('maestro/<int:pk>/ficha_medica', views.MaestroFichaMedicaView.as_view(), name='maestro'),
    path('maestro/<int:pk>/contactos', views.MaestroContactoEmergencia.as_view(), name='maestro'),
    path('maestro/<int:pk>/solicitudes', views.MaestroSolicitudCredencialView.as_view(), name='maestro'),
    path('maestro/<int:pk>/solicitudes/generar', views.MaestroGenerarSolicitud.as_view(), name='maestro'),
    path('maestro/<int:pk>/micredencial/', views.MyCredencial.as_view(), name='maestro'),
]
