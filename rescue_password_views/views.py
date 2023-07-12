from rest_framework.views import APIView
from password_reset_application.MailService import Reset
from rest_framework.request import Request
from rest_framework.response import Response
from core.models import Alumno, Administrador, Directivo, Maestro
from rest_framework.status import *
from api_auth.views import get_character


def filter_user(user: str, unique: int):

    match user:
        case "alumno":
            model: Alumno = get_character(unique, "alumno")
            if model is not None:
                return model
            else:
                return Response({
                    "message": "El alumno no existe"
                }, status=HTTP_404_NOT_FOUND)
        case "directivo":
            model: Directivo = get_character(unique, "directivo")
            if model is not None:
                return model
            else:
                return Response({
                    "message": "El directivo no existe"
                }, status=HTTP_404_NOT_FOUND)
        case "maestro":
            model: Maestro = get_character(unique, "maestro")
            if model is not None:
                return model
            else:
                return Response({
                    "message": "El maestro no existe"
                }, status=HTTP_404_NOT_FOUND)
        case "administrador":
            model: Administrador = get_character(unique, "administrador")
            if model is not None:
                return model
            else:
                return Response({
                    "message": "El administrador no existe"
                }, status=HTTP_404_NOT_FOUND)
        case _:
            return Response({
                "message": "Hubo un error en la consulta"
            }, status=HTTP_404_NOT_FOUND)


class ResetPasswordClient(APIView):

    def post(self, request: Request, user: str):
        print(request.data["username"])
        model = filter_user(user, request.data["username"])
        reset_password = Reset()

        if type(model).__name__ != "Response":
            if str(model.fecha_nacimiento) == request.data["birthdate"]:
                model.set_password(reset_password.send(model.email, f"{model.nombre} {model.apellidos}"))
                model.save()
                return Response({
                    "message": "La contraseña fue cambiada con éxito"
                }, status=HTTP_202_ACCEPTED)
            else:
                return Response({
                    "message": "Las fechas de nacimiento no coinciden"
                }, status=HTTP_400_BAD_REQUEST)
        else:
            return model
