from django.urls import path
from . import views

urlpatterns = [
    path('<str:user>/restaurar_password', views.ResetPasswordClient.as_view(), name='restaurar')
]
