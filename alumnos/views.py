from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.hashers import make_password
from rest_framework.views import APIView
from alumnos.serializers import *
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.status import *
from core.models import Alumno


def get_character(unique: str):
    try:
        return Alumno.objects.get(pk=unique)
    except Alumno.DoesNotExist:
        return None


class StudentView(APIView):

    def post(self, request: Request):
        request.data["password"] = make_password(request.data["password"])
        serializer = SerializerStudent(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class StudentDetail(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, unique: int):
        alumno: Alumno = get_character(unique)

        if alumno is not None:
            serializer = SerializerStudent(alumno)
            return Response(serializer.data)
        else:
            return Response({
                "message": "El alumno no existe"
            }, status=HTTP_404_NOT_FOUND)

    def patch(self, request: Request, unique: int):
        alumno: Alumno = get_character(unique)

        if alumno is not None:
            serializer = SerializerStudent(alumno, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=HTTP_202_ACCEPTED)
            else:
                return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        else:
            return Response({
                "message": "El alumno no existe"
            }, status=HTTP_404_NOT_FOUND)


class CambiarPasswordAlumno(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def patch(self, request: Request, unique: int):
        alumno: Alumno = get_character(unique)

        if alumno is not None:
            if alumno.check_password(request.data["old_password"]):
                alumno.set_password(request.data["new_password"])
                alumno.save()

                return Response({
                    "message": "La contraseña fue cambiada con éxito"
                }, status=HTTP_202_ACCEPTED)

            else:
                return Response({
                    "message": "La contraseña no coincide con la actual"
                }, status=HTTP_204_NO_CONTENT)

        else:
            return Response({
                "message": "El alumno no existe"
            }, status=HTTP_404_NOT_FOUND)


class StudentFichaMedicaView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, unique: int):
        alumno: Alumno = get_character(unique)

        if alumno is not None:
            return Response({
                "tipo_sangre": alumno.get_tipo_sangre(),
                "alergias": alumno.get_alergias(),
                "enfermedades_cronicas": alumno.get_enfermedades_cronicas()
            }, status=HTTP_302_FOUND)
        else:
            return Response({
                "message": "El alumno no existe"
            }, status=HTTP_404_NOT_FOUND)

    def post(self, request: Request, unique: int):
        alumno: Alumno = get_character(unique)

        if alumno is not None:
            serializer = SerializerFichaMedica(data=request.data)

            if serializer.is_valid():
                alumno.crearFichaMedica(request.data["tipo_sangre"], request.data["alergias"],
                                         request.data["enfermedades_cronicas"])
                return Response(serializer.data, status=HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        else:
            return Response({
                "message": "El alumno no existe"
            }, status=HTTP_404_NOT_FOUND)

    def put(self, request: Request, unique: int):
        alumno: Alumno = get_character(unique)

        if alumno is not None:
            serializer = SerializerFichaMedica(data=request.data)

            if serializer.is_valid():
                alumno.ficha_medica.tipo_sangre = request.data["tipo_sangre"]
                alumno.ficha_medica.alergias = request.data["alergias"]
                alumno.ficha_medica.enfermedades_cronicas = request.data["enfermedades_cronicas"]
                alumno.ficha_medica.save()
                return Response(serializer.data, status=HTTP_202_ACCEPTED)
            else:
                return Response(serializer.errors, status=HTTP_204_NO_CONTENT)
        else:
            return Response({
                "message": "El alumno no existe"
            }, status=HTTP_404_NOT_FOUND)


class StudentContactoEmergencia(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, unique: int):
        alumno: Alumno = get_character(unique)

        if alumno is not None:
            return Response({
                "nombre_contacto_emergencia": alumno.get_nombre_contacto_emergencia(),
                "numero_contacto_emergencia": alumno.get_numero_contacto_emergencia()
            }, status=HTTP_302_FOUND)
        else:
            return Response({
                "message": "El alumno no existe"
            }, status=HTTP_404_NOT_FOUND)

    def post(self, request: Request, unique: int):
        alumno: Alumno = get_character(unique)

        if alumno is not None:
            serializer = SerializerContactoEmergencia(data=request.data)

            if serializer.is_valid():
                alumno.crearContactoEmergencia(request.data["nombre_contacto_emergencia"], request.data["numero_contacto_emergencia"])
                return Response(serializer.data, status=HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        else:
            return Response({
                "message": "El alumno no existe"
            }, status=HTTP_404_NOT_FOUND)

    def put(self, request: Request, unique: int):
        alumno: Alumno = get_character(unique)

        if alumno is not None:
            serializer = SerializerContactoEmergencia(data=request.data)

            if serializer.is_valid():
                alumno.contacto_emergencia.nombre_contacto_emergencia = request.data["nombre_contacto_emergencia"]
                alumno.contacto_emergencia.numero_contacto_emergencia = request.data["numero_contacto_emergencia"]
                alumno.contacto_emergencia.save()
                return Response(serializer.data, status=HTTP_202_ACCEPTED)
            else:
                return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        else:
            return Response({
                "message": "El alumno no existe"
            }, status=HTTP_404_NOT_FOUND)


class StudentSolicitudCredencialView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, unique: int):
        alumno: Alumno = get_character(unique)

        if alumno is not None:
            solicitudes = alumno.lista_solicitudes()
            serializer = SerializerSolicitud(solicitudes, many=True)
            return Response(serializer.data, status=HTTP_200_OK)
        else:
            return Response({
                "message": "El alumno no existe"
            }, status=HTTP_404_NOT_FOUND)


class StudentGenerarSolicitud(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, unique: int):
        alumno: Alumno = get_character(unique)

        if alumno is not None:
            if alumno.solicitudes.exists() is False:
                if alumno.ficha_medica_existe():
                    if alumno.contacto_emergencia_existe():
                        alumno.generar_solicitud()

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
            elif alumno.get_estado_solicitud() == "aprobada":
                return Response({
                    "message": "Tu solicitud ya fué aprobada"
                }, status=HTTP_200_OK)
                pass
            else:
                return Response({
                    "message": "Ya tienes una solicitud pendiente"
                }, status=HTTP_200_OK)
        else:
            return Response({
                "message": "El alumno no existe"
            }, status=HTTP_404_NOT_FOUND)


class MyCredencial(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, unique: int):
        alumno = get_character(unique)

        if alumno is not None:
            return Response({
                "estado_credencial": alumno.get_estado_credencial(),
                "clave_credencial": alumno.get_clave_credencial()
            }, status=HTTP_200_OK)
        else:
            return Response({
                "message": "El alumno no existe"
            }, status=HTTP_404_NOT_FOUND)
