from rest_framework.request import Request
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from core.models import Administrador, Alumno, Maestro, Directivo


def get_character(unique: str, person: str):
    match person:
        case "alumno":
            try:
                return Alumno.objects.get(email=unique)
            except Alumno.DoesNotExist:
                return None

        case "administrador":
            try:
                return Administrador.objects.get(email=unique)
            except Administrador.DoesNotExist:
                return None

        case "directivo":
            try:
                return Directivo.objects.get(email=unique)
            except Directivo.DoesNotExist:
                return None

        case "maestro":
            try:
                return Maestro.objects.get(email=unique)
            except Maestro.DoesNotExist:
                return None


def get_or_create_token(admin):
    return Response({
        "id_admin": admin.id,
        "token": str(Token.objects.get_or_create(admin)[0])
    }, status=HTTP_200_OK)


class LoginAdministrador(APIView):

    def post(self, request: Request):
        admin: Administrador = get_character(request.data["username"], "administrador")

        if admin is not None:
            if admin.check_password(request.data["password"]):
                return get_or_create_token(admin)

            else:
                return Response({
                    "message": "Contraseña incorrecta",
                }, status=HTTP_401_UNAUTHORIZED)
        else:
            return Response({
                "message": "El administrador no existe"
            }, status=HTTP_404_NOT_FOUND)


class LoginAlumno(APIView):

    def post(self, request: Request):
        alumno: Alumno = get_character(request.data["username"], "alumno")

        if alumno is not None:
            if alumno.check_password(request.data["password"]):
                return get_or_create_token(alumno)

            else:
                return Response({
                    "message": "Contraseña incorrecta",
                }, status=HTTP_401_UNAUTHORIZED)
        else:
            return Response({
                "message": "El alumno no existe"
            }, status=HTTP_404_NOT_FOUND)


class LoginDirectivo(APIView):

    def post(self, request: Request):
        dircetivo: Directivo = get_character(request.data["username"], "directivo")

        if dircetivo is not None:
            if dircetivo.check_password(request.data["password"]):
                return get_or_create_token(dircetivo)

            else:
                return Response({
                    "message": "Contraseña incorrecta",
                }, status=HTTP_401_UNAUTHORIZED)
        else:
            return Response({
                "message": "El directivo no existe"
            }, status=HTTP_404_NOT_FOUND)


class LoginMaestro(APIView):

    def post(self, request: Request):
        maestro: Maestro = get_character(request.data["username"], "maestro")

        if maestro is not None:
            if maestro.check_password(request.data["password"]):
                return get_or_create_token(maestro)

            else:
                return Response({
                    "message": "Contraseña incorrecta",
                }, status=HTTP_401_UNAUTHORIZED)
        else:
            return Response({
                "message": "El maestro no existe"
            }, status=HTTP_404_NOT_FOUND)
