from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import make_password
from rest_framework.views import APIView
from alumnos.serializers import *
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.status import *
from maestros.serializers import SerializerMaestro
from core.models import Maestro


def get_character(unique: str):
    try:
        return Maestro.objects.get(pk=unique)
    except Maestro.DoesNotExist:
        return None


class MaestroView(APIView):

    def post(self, request: Request):
        request.data["password"] = make_password(request.data["password"])
        serializer = SerializerMaestro(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=HTTP_204_NO_CONTENT)


class MaestroDetail(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, pk):
        maestro: Maestro = get_character(pk)

        if maestro is not None:
            serializer = SerializerMaestro(maestro)
            return Response(serializer.data)
        else:
            return Response({
                "message": "El maestro no existe"
            }, status=HTTP_404_NOT_FOUND)

    def patch(self, request: Request, pk):
        maestro: Maestro = get_character(pk)

        if maestro is not None:
            serializer = SerializerMaestro(maestro, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=HTTP_202_ACCEPTED)
            else:
                return Response(serializer.errors, status=HTTP_204_NO_CONTENT)
        else:
            return Response({
                "message": "El maestro no existe"
            }, status=HTTP_404_NOT_FOUND)


class CambiarPasswordMaestro(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def patch(self, request: Request, pk):
        maestro: Maestro = get_character(pk)

        if maestro is not None:
            if maestro.check_password(request.data["old_password"]):
                maestro.set_password(request.data["new_password"])
                maestro.save()

                return Response({
                    "message": "La contraseña fue cambiada con éxito"
                }, status=HTTP_202_ACCEPTED)

            else:
                return Response({
                    "message": "La contraseña no coincide con la actual"
                }, status=HTTP_204_NO_CONTENT)

        else:
            return Response({
                "message": "El maestro no existe"
            }, status=HTTP_404_NOT_FOUND)


class MaestroFichaMedicaView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, pk):
        maestro: Maestro = get_character(pk)

        if maestro is not None:
            return Response({
                "tipo_sangre": maestro.get_tipo_sangre(),
                "alergias": maestro.get_alergias(),
                "enfermedades_cronicas": maestro.get_enfermedades_cronicas()
            }, status=HTTP_302_FOUND)
        else:
            return Response({
                "message": "El maestro no existe"
            }, status=HTTP_404_NOT_FOUND)

    def post(self, request: Request, pk):
        maestro: Maestro = get_character(pk)

        if maestro is not None:
            serializer = SerializerFichaMedica(data=request.data)

            if serializer.is_valid():
                maestro.crearFichaMedica(request.data["tipo_sangre"], request.data["alergias"],
                                         request.data["enfermedades_cronicas"])
                return Response(serializer.data, status=HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=HTTP_204_NO_CONTENT)
        else:
            return Response({
                "message": "El maestro no existe"
            }, status=HTTP_404_NOT_FOUND)

    def put(self, request: Request, pk):
        maestro: Maestro = get_character(pk)

        if maestro is not None:
            serializer = SerializerFichaMedica(data=request.data)

            if serializer.is_valid():
                maestro.ficha_medica.tipo_sangre = request.data["tipo_sangre"]
                maestro.ficha_medica.alergias = request.data["alergias"]
                maestro.ficha_medica.enfermedades_cronicas = request.data["enfermedades_cronicas"]
                maestro.ficha_medica.save()
                return Response(serializer.data, status=HTTP_202_ACCEPTED)
            else:
                return Response(serializer.errors, status=HTTP_204_NO_CONTENT)
        else:
            return Response({
                "message": "El maestro no existe"
            }, status=HTTP_404_NOT_FOUND)


class MaestroContactoEmergencia(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, pk):
        maestro: Maestro = get_character(pk)

        if maestro is not None:
            return Response({
                "nombre_contacto_emergencia": maestro.get_nombre_contacto_emergencia(),
                "numero_contacto_emergencia": maestro.get_numero_contacto_emergencia()
            }, status=HTTP_302_FOUND)
        else:
            return Response({
                "message": "El maestro no existe"
            }, status=HTTP_404_NOT_FOUND)

    def post(self, request: Request, pk):
        maestro: Maestro = get_character(pk)

        if maestro is not None:
            serializer = SerializerContactoEmergencia(data=request.data)

            if serializer.is_valid():
                maestro.crearContactoEmergencia(request.data["nombre_contacto_emergencia"], request.data["numero_contacto_emergencia"])
                return Response(serializer.data, status=HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=HTTP_204_NO_CONTENT)
        else:
            return Response({
                "message": "El maestro no existe"
            }, status=HTTP_404_NOT_FOUND)

    def put(self, request: Request, pk):
        maestro: Maestro = get_character(pk)

        if maestro is  not None:
            serializer = SerializerContactoEmergencia(data=request.data, partial=True)

            if serializer.is_valid():
                maestro.contacto_emergencia.nombre_contacto_emergencia = request.data["nombre_contacto_emergencia"]
                maestro.contacto_emergencia.numero_contacto_emergencia = request.data["numero_contacto_emergencia"]
                maestro.contacto_emergencia.save()
                return Response(serializer.data, status=HTTP_202_ACCEPTED)
            else:
                return Response(serializer.errors, status=HTTP_204_NO_CONTENT)
        else:
            return Response({
                "message": "El maestro no existe"
            }, status=HTTP_404_NOT_FOUND)


class MaestroSolicitudCredencialView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, pk):
        maestro: Maestro = get_character(pk)

        if maestro is not None:
            solicitudes = maestro.lista_solicitudes()
            serializer = SerializerSolicitud(solicitudes, many=True)
            return Response(serializer.data, status=HTTP_200_OK)
        else:
            return Response({
                "message": "El maestro no existe"
            }, status=HTTP_404_NOT_FOUND)


class MaestroGenerarSolicitud(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, pk):
        maestro: Maestro = get_character(pk)

        if maestro is not None:
            if maestro.solicitudes.exists() is False:
                if maestro.ficha_medica_existe():
                    if maestro.contacto_emergencia_existe():
                        maestro.generar_solicitud()

                        return Response({
                            "message": "Solicitud generada con éxito"
                        }, status=HTTP_200_OK)
                    else:
                        return Response({
                            "m|essage": "Falta crear contacto emergencia"
                        }, status=HTTP_404_NOT_FOUND)
                else:
                    return Response({
                        "message": "Falta crear ficha médica"
                    }, status=HTTP_404_NOT_FOUND)
            elif maestro.get_estado_solicitud() == "aprobada":
                return Response({
                    "message": "Tu solicitud ya fué aprobada"
                }, status=HTTP_200_OK)
            else:
                return Response({
                    "message": "Ya tienes una solicitud pendiente"
                }, status=HTTP_200_OK)
        else:
            return Response({
                "message": "El maestro no existe"
            }, status=HTTP_404_NOT_FOUND)


class MyCredencial(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, pk):
        maestro: Maestro = get_character(pk)

        if maestro is not None:
            return Response({
                "estado_credencial": maestro.get_estado_credencial(),
                "clave_credencial": maestro.get_clave_credencial()
            }, status=HTTP_200_OK)
        else:
            return Response({
                "message": "El maestro no existe"
            }, status=HTTP_404_NOT_FOUND)
