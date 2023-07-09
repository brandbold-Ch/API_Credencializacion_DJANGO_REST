from django.contrib import admin
from django.urls import path, include
from rest_framework.documentation import include_docs_urls


urlpatterns = [
    path('', include('api_auth.urls')),
    path('', include('alumnos.urls')),
    path('', include('administradores.urls')),
    path('', include('directivos.urls')),
    path('', include('maestros.urls')),
    path('', include('rescue_password_views.urls')),
    path('docs/', include_docs_urls(title='Api Documentation UPTAP Credencialización'))
]

handler404 = 'core.views.error_404'
