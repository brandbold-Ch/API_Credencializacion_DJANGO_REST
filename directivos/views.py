from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import make_password
from rest_framework.views import APIView
from alumnos.serializers import *
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.status import *
from directivos.serializers import SerializerDirectivo
from core.models import Directivo


def get_character(unique: int):
    try:
        return Directivo.objects.get(pk=unique)
    except Directivo.DoesNotExist:
        return None


class DirectivoView(APIView):

    def post(self, request: Request):
        request.data["password"] = make_password(request.data["password"])
        serializer = SerializerDirectivo(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=HTTP_204_NO_CONTENT)


class DirectivoDetail(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, unique: int):
        directivo: Directivo = get_character(unique)

        if directivo is not None:
            serializer = SerializerDirectivo(directivo)
            return Response(serializer.data, status=HTTP_200_OK)
        else:
            return Response({
                "message": "El usuario no existe"
            }, status=HTTP_404_NOT_FOUND)

    def patch(self, request: Request, unique: int):
        directivo: Directivo = get_character(unique)

        if directivo is not None:
            serializer = SerializerDirectivo(directivo, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=HTTP_202_ACCEPTED)
            else:
                return Response(serializer.errors, status=HTTP_204_NO_CONTENT)
        else:
            return Response({
                "message": "El directivo no existe"
            }, status=HTTP_404_NOT_FOUND)


class CambiarPasswordDirectivo(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def patch(self, request: Request, unique: int):
        directivo: Directivo = get_character(unique)

        if directivo is not None:
            if directivo.check_password(request.data["old_password"]):
                directivo.set_password(request.data["new_password"])
                directivo.save()

                return Response({
                    "message": "La contraseña fue cambiada con éxito"
                }, status=HTTP_202_ACCEPTED)

            else:
                return Response({
                    "message": "La contraseña no coincide con la actual"
                }, status=HTTP_204_NO_CONTENT)

        else:
            return Response({
                "message": "El directivo no existe"
            }, status=HTTP_404_NOT_FOUND)


class DirectivoFichaMedicaView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, unique: int):
        directivo: Directivo = get_character(unique)

        if directivo is not None:
            return Response({
                "tipo_sangre": directivo.get_tipo_sangre(),
                "alergias": directivo.get_alergias(),
                "enfermedades_cronicas": directivo.get_enfermedades_cronicas()
            }, status=HTTP_302_FOUND)
        else:
            return Response({
                "message": "El directivo no existe"
            }, status=HTTP_404_NOT_FOUND)

    def post(self, request: Request, unique: int):
        directivo: Directivo = get_character(unique)

        if directivo is not None:
            serializer = SerializerFichaMedica(data=request.data)

            if serializer.is_valid():
                directivo.crearFichaMedica(request.data["tipo_sangre"], request.data["alergias"],
                                         request.data["enfermedades_cronicas"])
                return Response(serializer.data, status=HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=HTTP_204_NO_CONTENT)
        else:
            return Response({
                "message": "El directivo no existe"
            }, status=HTTP_404_NOT_FOUND)

    def put(self, request: Request, unique: int):
        directivo: Directivo = get_character(unique)

        if directivo is not None:
            serializer = SerializerFichaMedica(data=request.data)

            if serializer.is_valid():
                directivo.ficha_medica.tipo_sangre = request.data["tipo_sangre"]
                directivo.ficha_medica.alergias = request.data["alergias"]
                directivo.ficha_medica.enfermedades_cronicas = request.data["enfermedades_cronicas"]
                directivo.ficha_medica.save()
                return Response(serializer.data, status=HTTP_202_ACCEPTED)
            else:
                return Response(serializer.errors, status=HTTP_204_NO_CONTENT)
        else:
            return Response({
                "message": "El directivo no existe"
            }, status=HTTP_404_NOT_FOUND)


class DirectivoContactoEmergencia(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, unique: int):
        directivo: Directivo = get_character(unique)

        if directivo is not None:
            return Response({
                "nombre_contacto_emergencia": directivo.get_nombre_contacto_emergencia(),
                "numero_contacto_emergencia": directivo.get_numero_contacto_emergencia()
            }, status=HTTP_302_FOUND)
        else:
            return Response({
                "message": "El directivo no existe"
            }, status=HTTP_404_NOT_FOUND)

    def post(self, request: Request, unique: int):
        directivo: Directivo = get_character(unique)

        if directivo is not None:
            serializer = SerializerContactoEmergencia(data=request.data)

            if serializer.is_valid():
                directivo.crearContactoEmergencia(request.data["nombre_contacto_emergencia"], request.data["numero_contacto_emergencia"])
                return Response(serializer.data, status=HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=HTTP_204_NO_CONTENT)
        else:
            return Response({
                "message": "El directivo no existe"
            }, status=HTTP_404_NOT_FOUND)

    def put(self, request: Request, unique: int):
        directivo: Directivo = get_character(unique)

        if directivo is not None:
            serializer = SerializerContactoEmergencia(data=request.data)

            if serializer.is_valid():
                directivo.contacto_emergencia.nombre_contacto_emergencia = request.data["nombre_contacto_emergencia"]
                directivo.contacto_emergencia.numero_contacto_emergencia = request.data["numero_contacto_emergencia"]
                directivo.contacto_emergencia.save()
                return Response(serializer.data, status=HTTP_202_ACCEPTED)
            else:
                return Response(serializer.errors, status=HTTP_204_NO_CONTENT)
        else:
            return Response({
                "message": "El directivo no existe"
            }, status=HTTP_404_NOT_FOUND)


class DirectivoSolicitudCredencialView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, unique: int):
        directivo: Directivo = get_character(unique)
        if directivo is not None:
            solicitudes = directivo.lista_solicitudes()
            serializer = SerializerSolicitud(solicitudes, many=True)
            return Response(serializer.data, status=HTTP_200_OK)
        else:
            return Response({
                "message": "El directivo no existe"
            }, status=HTTP_404_NOT_FOUND)


class DirectivoGenerarSolicitud(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, unique: int):
        directivo: Directivo = get_character(unique)

        if directivo is not None:
            if directivo.solicitudes.exists() is False:
                if directivo.ficha_medica_existe():
                    if directivo.contacto_emergencia_existe():
                        directivo.generar_solicitud()

                        return Response({
                            "message": "Solicitud generada con éxito"
                        }, status=HTTP_200_OK)
                    else:
                        return Response({
                            "message": "Falta crear contacto emergencia"
                        }, status=HTTP_404_NOT_FOUND)
                else:
                    return Response({
                        "message": "Falta crear ficha médica"
                    }, status=HTTP_404_NOT_FOUND)
            elif directivo.get_estado_solicitud() == "aprobada":
                return Response({
                    "message": "Tu solicitud ya fué aprobada"
                }, status=HTTP_200_OK)
            else:
                return Response({
                    "message": "Ya tienes una solicitud pendiente"
                }, status=HTTP_200_OK)
        else:
            return Response({
                "message": "El directivo no existe"
            }, status=HTTP_404_NOT_FOUND)


class MyCredencial(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, unique: int):
        directivo: Directivo = get_character(unique)

        if directivo is not None:
            return Response({
                "estado_credencial": directivo.get_estado_credencial(),
                "clave_credencial": directivo.get_clave_credencial()
            }, status=HTTP_200_OK)
        else:
            return Response({
                "message": "El directivo no existe"
            }, status=HTTP_404_NOT_FOUND)
