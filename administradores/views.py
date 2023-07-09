from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.request import Request
from django.contrib.auth.hashers import make_password
from alumnos.serializers import SerializerStudent
from maestros.serializers import SerializerMaestro
from directivos.serializers import SerializerDirectivo
from administradores.serializers import *
from rest_framework.status import *
from core.models import Directivo, Maestro


def get_character(unique: int, person: str):
    match person:
        case "alumno":
            try:
                return Alumno.objects.get(pk=unique)
            except Alumno.DoesNotExist:
                return None

        case "administrador":
            try:
                return Administrador.objects.get(pk=unique)
            except Administrador.DoesNotExist:
                return None

        case "directivo":
            try:
                return Directivo.objects.get(pk=unique)
            except Directivo.DoesNotExist:
                return None

        case "maestro":
            try:
                return Maestro.objects.get(pk=unique)
            except Maestro.DoesNotExist:
                return None


def get_all_list(person: str):
    match person:
        case "alumnos":
            return Alumno.objects.all()
        case "administradores":
            return Administrador.objects.all()
        case "directivos":
            return Directivo.objects.all()
        case "maestros":
            return Maestro.objects.all()
        case _:
            return None


def filter_user(user: str, unique: int):

    match user:
        case "alumno":
            model: Alumno = get_character(unique, "alumno")
            if model is not None:
                return model
            else:
                return Response({
                    "message": "El alumno no existe"
                })
        case "directivo":
            model: Directivo = get_character(unique, "directivo")
            if model is not None:
                return model
            else:
                return Response({
                    "message": "El directivo no existe"
                })
        case "maestro":
            model: Maestro = get_character(unique, "maestro")
            if model is not None:
                return model
            else:
                return Response({
                    "message": "El maestro no existe"
                })
        case "administrador":
            model: Administrador = get_character(unique, "administrador")
            if model is not None:
                return model
            else:
                return Response({
                    "message": "El administrador no existe"
                })
        case _:
            return Response({
                "message": "Hubo un error en la consulta"
            }, status=HTTP_404_NOT_FOUND)


# ----------------------------------------Views de Operaciones CRUD Administrador------------------------------


class AdminView(APIView):

    def post(self, request: Request):
        request.data["password"] = make_password(request.data["password"])
        serializer = SerializerAdministrador(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class AdminDetailView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, unique: int):
        administrador: Administrador = get_character(unique, "administrador")

        if administrador is not None:
            serializer = SerializerAdministrador(administrador)
            return Response(serializer.data, status=HTTP_200_OK)
        else:
            return Response({
                "message": "El administrador no existe"
            }, status=HTTP_404_NOT_FOUND)

    def patch(self, request: Request, unique: int):
        administrador: Administrador = get_character(unique, "administrador")

        if administrador is not None:
            serializer = SerializerAdministrador(administrador, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=HTTP_202_ACCEPTED)
            else:
                return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        else:
            return Response({
                "message": "El administrador no existe"
            }, status=HTTP_404_NOT_FOUND)


class ChangePasswordAdminView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def patch(self, request: Request, unique: int):
        administrador: Administrador = get_character(unique, "administrador")

        if administrador is not None:
            if administrador.check_password(request.data["old_password"]):
                administrador.set_password(request.data["new_password"])
                administrador.save()
                return Response({
                    "message": "La contraseña fue cambiada con éxito"
                }, status=HTTP_202_ACCEPTED)
            else:
                return Response({
                    "message": "La contraseña no coincide con la actual"
                }, status=HTTP_204_NO_CONTENT)
        else:
            return Response({
                "message": "El administrador no existe"
            }, status=HTTP_404_NOT_FOUND)


class AdminMedicalRecordView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, unique: int):
        administrador: Administrador = get_character(unique, "administrador")

        if administrador is not None:
            return Response({
                "tipo_sangre": administrador.get_tipo_sangre(),
                "alergias": administrador.get_alergias(),
                "enfermedades_cronicas": administrador.get_enfermedades_cronicas()
            }, status=HTTP_302_FOUND)
        else:
            return Response({
                "message": "El administrador no existe"
            }, status=HTTP_404_NOT_FOUND)

    def post(self, request: Request, unique: int):
        administrador: Administrador = get_character(unique, "administrador")

        if administrador is not None:
            serializer = SerializerFichaMedica(data=request.data)

            if serializer.is_valid():
                administrador.crearFichaMedica(request.data["tipo_sangre"], request.data["alergias"],
                                               request.data["enfermedades_cronicas"])
                return Response(serializer.data, status=HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        else:
            return Response({
                "message": "El administrador no existe"
            }, status=HTTP_404_NOT_FOUND)

    def put(self, request: Request, unique: int):
        administrador: Administrador = get_character(unique, "administrador")

        if administrador is not None:
            serializer = SerializerFichaMedica(data=request.data)

            if serializer.is_valid():
                administrador.ficha_medica.tipo_sangre = request.data["tipo_sangre"]
                administrador.ficha_medica.alergias = request.data["alergias"]
                administrador.ficha_medica.enfermedades_cronicas = request.data["enfermedades_cronicas"]
                administrador.ficha_medica.save()
                return Response(serializer.data, status=HTTP_202_ACCEPTED)
            else:
                return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        else:
            return Response({
                "message": "El usuario no existe"
            }, status=HTTP_404_NOT_FOUND)


class AdminContactEmergencyView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, unique: int):
        administrador: Administrador = get_character(unique, "administrador")

        if administrador is not None:
            return Response({
                "nombre_contacto_emergencia": administrador.get_nombre_contacto_emergencia(),
                "numero_contacto_emergencia": administrador.get_numero_contacto_emergencia()
            }, status=HTTP_302_FOUND)
        else:
            return Response({
                "message": "El usuario no existe"
            }, status=HTTP_404_NOT_FOUND)

    def post(self, request: Request, unique: int):
        administrador: Administrador = get_character(unique, "administrador")

        if administrador is not None:
            serializer = SerializerContactoEmergencia(data=request.data)

            if serializer.is_valid():
                administrador.crearContactoEmergencia(request.data["nombre_contacto_emergencia"],
                                                      request.data["numero_contacto_emergencia"])
                return Response(serializer.data, status=HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        else:
            return Response({
                "message": "El usuario no existe"
            }, status=HTTP_404_NOT_FOUND)

    def put(self, request: Request, unique: int):
        administrador: Administrador = get_character(unique, "administrador")

        if administrador is not None:
            serializer = SerializerContactoEmergencia(data=request.data)

            if serializer.is_valid():
                administrador.contacto_emergencia.nombre_contacto_emergencia = request.data[
                    "nombre_contacto_emergencia"]
                administrador.contacto_emergencia.numero_contacto_emergencia = request.data[
                    "numero_contacto_emergencia"]
                administrador.contacto_emergencia.save()
                return Response(serializer.data, status=HTTP_202_ACCEPTED)
            else:
                return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        else:
            return Response({
                "message": "El administrador no existe"
            }, status=HTTP_404_NOT_FOUND)


class ActivateCredentialView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def filter_option(self, option: str, model):
        match option:
            case "activar":
                model.activar_credencial()
                return Response({
                    "message": "Credencial activada"
                }, status=HTTP_200_OK)

            case "desactivar":
                model.desactivar_credencial()
                return Response({
                    "message": "Credencial desactivada"
                }, status=HTTP_200_OK)

            case _:
                return Response({
                    "message": "Hubo un error en la consulta"
                }, status=HTTP_404_NOT_FOUND)

    def get(self, request: Request, unique: int, other: int, user: str, option: str):
        administrador: Administrador = get_character(unique, "administrador")

        if administrador is not None:
            filter_request = filter_user(user, other)
            if type(filter_request).__name__ != "Response":
                selection = self.filter_option(option, filter_request)
                return selection
            else:
                return filter_request

        else:
            return Response({
                "message": "El administrador no existe"
            })


class ValidateRequestView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def filter_option(self, option: str, model):
        match option:
            case "aceptar":
                if model.get_estado_solicitud() == "pendiente":
                    model.aprobar_solicitud()
                    if model.credencial is None:
                        model.crearCredencial()
                        return Response({
                            "message": "Credencial creada con éxito, ahora debes activarla"
                        }, status=HTTP_201_CREATED)
                    else:
                        return Response({
                            "message": "Ya existe una credencial"
                        }, status=HTTP_200_OK)
                else:
                    return Response({
                        "message": "Ya fué aprobada"
                    }, status=HTTP_200_OK)

            case "denegar":
                if model.get_estado_solicitud() == "pendiente":
                    model.rechazar_solicitud()
                    return Response({
                        "message": "Solicitud denegada"
                    }, status=HTTP_406_NOT_ACCEPTABLE)
                else:
                    return Response({
                        "message": "La solicitud ya fué denegada"
                    }, status=HTTP_200_OK)
            case _:
                return Response({
                    "message": "Hubo un error en la consulta"
                }, status=HTTP_404_NOT_FOUND)

    def get(self, request: Request, unique: int, user: str, other: int, option: str):
        administrador: Administrador = get_character(unique, "administrador")

        if administrador is not None:
            filter_request = filter_user(user, other)
            if type(filter_request).__name__ != "Response":
                selection = self.filter_option(option, filter_request)
                return selection
            else:
                return filter_request

        else:
            return Response({
                "message": "El administrador no existe"
            })


class ListadoSolicitudesView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_list_dict(self, status: str, model):

        match status:
            case "pendientes":
                return Response(
                    [
                        {
                            "id": x.id,
                            "fecha_solicitud": x.get_fecha_solicitud(),
                            "estado": x.get_estado_solicitud(),
                            "tipo_solicitud": x.get_tipo_solicitud(),
                        }
                        for x in model if x.get_estado_solicitud() == "pendiente"
                    ],
                    status=HTTP_200_OK)

            case "aprobados":
                return Response(
                    [
                        {
                            "id": x.id,
                            "fecha_solicitud": x.get_fecha_solicitud(),
                            "estado": x.get_estado_solicitud(),
                            "tipo_solicitud": x.get_tipo_solicitud(),
                        }
                        for x in model if x.get_estado_solicitud() == "aprobada"
                    ],
                    status=HTTP_200_OK)

            case "rechazados":
                return Response(
                    [
                        {
                            "id": x.id,
                            "fecha_solicitud": x.get_fecha_solicitud(),
                            "estado": x.get_estado_solicitud(),
                            "tipo_solicitud": x.get_tipo_solicitud(),
                        }
                        for x in model if x.get_estado_solicitud() == "rechazada"
                    ],
                    status=HTTP_200_OK)
            case _:
                return Response({
                    "message": "Hubo un error en la consulta"
                }, status=HTTP_404_NOT_FOUND)

    def get(self, request: Request, unique: int, user: str, status: str):
        administrador: Administrador = get_character(unique, "administrador")

        if administrador is not None:
            model = get_all_list(user)
            if model is not None:
                return self.get_list_dict(status, model)
            else:
                return Response({
                    "message": "Hubo un error en la consulta"
                }, status=HTTP_404_NOT_FOUND)
        else:
            return Response({
                "message": "El administrador no existe"
            }, status=HTTP_404_NOT_FOUND)


# --------------------------------------Views de Operaciones CRUD Alumnos-----------------------------------


class ListadoAlumnos(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, unique: int):
        administrador: Administrador = get_character(unique, "administrador")

        if administrador is not None:
            alumno = Alumno.objects.all()
            serializer = SerializerStudent(alumno, many=True)
            return Response(serializer.data, status=HTTP_200_OK)
        else:
            return Response({
                "message": "El administrador no existe"
            }, status=HTTP_404_NOT_FOUND)


class ListadoDetailAlumno(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, unique: int, other: int):
        administrador: Administrador = get_character(unique, "administrador")
        alumno: Alumno = get_character(other, "alumno")

        if administrador is not None:
            if alumno is not None:
                serializer = SerializerStudent(alumno)
                return Response(serializer.data, status=HTTP_200_OK)
            else:
                return Response({
                    "message": "El alumno no existe"
                }, status=HTTP_404_NOT_FOUND)
        else:
            return Response({
                "message": "El administrador no existe"
            }, status=HTTP_404_NOT_FOUND)

    def patch(self, request: Request, unique: int, other: int):
        administrador: Administrador = get_character(unique, "administrador")
        alumno: Alumno = get_character(other, "alumno")

        if administrador is not None:
            if alumno is not None:
                request.data["password"] = make_password(request.data["password"])
                serializer = SerializerStudent(alumno, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=HTTP_202_ACCEPTED)
                else:
                    return Response(serializer.errors, status=HTTP_204_NO_CONTENT)
            else:
                return Response({
                    "message": "El alumno no existe"
                }, status=HTTP_404_NOT_FOUND)
        else:
            return Response({
                "message": "El administrador no existe"
            }, status=HTTP_404_NOT_FOUND)


# -----------------------------------------Views de Operaciones CRUD Directivos--------------------------------


class ListadoDirectivos(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, unique: int):
        administrador: Administrador = get_character(unique, "administrador")

        if administrador is not None:
            directivos = Directivo.objects.all()
            serializer = SerializerDirectivo(directivos, many=True)
            return Response(serializer.data, status=HTTP_200_OK)
        else:
            return Response({
                "message": "El administrador no existe"
            }, status=HTTP_404_NOT_FOUND)


class ListadoDetailDirectivo(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, unique: int, other: int):
        administrador: Administrador = get_character(unique, "administrador")
        directivo: Directivo = get_character(other, "directivo")

        if administrador is not None:
            if directivo is not None:
                serializer = SerializerDirectivo(directivo)
                return Response(serializer.data, status=HTTP_200_OK)
            else:
                return Response({
                    "message": "El directivo no existe"
                }, status=HTTP_404_NOT_FOUND)
        else:
            return Response({
                "message": "El administrador no existe"
            }, status=HTTP_404_NOT_FOUND)

    def patch(self, request: Request, unique: int, other: int):
        administrador: Administrador = get_character(unique, "administrador")
        directivo: Directivo = get_character(other, "directivo")

        if administrador is not None:
            if directivo is not None:
                request.data["password"] = make_password(request.data["password"])
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
        else:
            return Response({
                "message": "El administrador no existe"
            }, status=HTTP_404_NOT_FOUND)


# -------------------------------------Views de Operaciones CRUD Maestros --------------------------------


class ListadoMaestros(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, unique: int):
        administrador: Administrador = get_character(unique, "administrador")

        if administrador is not None:
            maestros = Maestro.objects.all()
            serializer = SerializerMaestro(maestros, many=True)
            return Response(serializer.data, status=HTTP_200_OK)
        else:
            return Response({
                "message": "El maestro no existe"
            }, status=HTTP_404_NOT_FOUND)


class ListadoDetailMaestro(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, unique: int, other: int):
        administrador: Administrador = get_character(unique, "administrador")
        maestro: Maestro = get_character(other, "maestro")

        if administrador is not None:
            if maestro is not None:
                serializer = SerializerMaestro(maestro)
                return Response(serializer.data, status=HTTP_200_OK)
            else:
                return Response({
                    "message": "El maestro no existe"
                }, status=HTTP_404_NOT_FOUND)
        else:
            return Response({
                "message": "El administrador no existe"
            }, status=HTTP_404_NOT_FOUND)

    def patch(self, request: Request, unique: int, other: int):
        administrador: Administrador = get_character(unique, "administrador")
        maestro: Maestro = get_character(other, "maestro")

        if administrador is not None:
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
        else:
            return Response({
                "message": "El administrador no existe"
            }, status=HTTP_404_NOT_FOUND)


# ----------------------------Views de UPTAP---------------------------------------------


class ProfessionView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):
        carrera = Carrera.objects.all()
        serializer = SerializerCarrera(carrera, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

    def post(self, request: Request):
        serializer = SerializerCarrera(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        else:
            return Response(serializer.errors, status=HTTP_204_NO_CONTENT)


class GradoEstudioView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):
        grado_estudio = GradoDeEstudio.objects.all()
        serializer = SerializerGradoEstudio(grado_estudio, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

    def post(self, request: Request):
        serializer = SerializerGradoEstudio(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        else:
            return Response(serializer.errors, status=HTTP_204_NO_CONTENT)


class CuatrimestreView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):
        cuatrimestre = Cuatrimestre.objects.all()
        serializer = SerializerCuatrimestre(cuatrimestre, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

    def post(self, request: Request):
        serializer = SerializerCuatrimestre(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        else:
            return Response(serializer.errors, status=HTTP_204_NO_CONTENT)
