from django.urls import path
from . import views

urlpatterns = [
    path('directivos/', views.DirectivoView.as_view(), name='directivos'),
    path('directivo/<int:unique>/changeauth', views.CambiarPasswordDirectivo.as_view(), name='directivo'),
    path('directivo/<int:unique>', views.DirectivoDetail.as_view(), name='directivo'),
    path('directivo/<int:unique>/ficha_medica', views.DirectivoFichaMedicaView.as_view(), name='directivo'),
    path('directivo/<int:unique>/contactos', views.DirectivoContactoEmergencia.as_view(), name='directivo'),
    path('directivo/<int:unique>/solicitudes', views.DirectivoSolicitudCredencialView.as_view(), name='directivo'),
    path('directivo/<int:unique>/solicitudes/generar', views.DirectivoGenerarSolicitud.as_view(), name='directivo'),
    path('directivo/<int:unique>/micredencial/', views.MyCredencial.as_view(), name='directivo'),
]
