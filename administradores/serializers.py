from rest_framework.serializers import ModelSerializer, CharField
import importlib

module = importlib.import_module('core.models')
Administrador = module.Administrador
FichaMedica = module.FichaMedica
GradoDeEstudio = module.GradoDeEstudio
ContactoEmergencia = module.ContactoEmergencia
SolicitudCredencial = module.SolicitudCredencial
Alumno = module.Alumno
Carrera = module.Carrera
Cuatrimestre = module.Cuatrimestre


class SerializerAdministrador(ModelSerializer):
    password = CharField(write_only=True)

    class Meta:
        model = Administrador
        fields = "__all__"

    def to_representation(self, instance: Administrador):
        representation = super().to_representation(instance)

        if instance.contacto_emergencia_existe() and instance.ficha_medica_existe():
            instance.crearCredencial()
            instance.activar_credencial()

        if instance.is_superuser is False:
            instance.hacerAdmin()

        representation["ficha_medica"] = {
            "tipo_sangre": instance.get_tipo_sangre(),
            "alergias": instance.get_alergias(),
            "enfermedades_cronicas": instance.get_enfermedades_cronicas()
        }
        representation["contacto_emergencia"] = {
            "nombre_contacto_emergencia": instance.get_nombre_contacto_emergencia(),
            "numero_contacto_emergencia": instance.get_numero_contacto_emergencia()
        }
        representation["solicitud"] = {
            "fecha_solicitud": instance.get_fecha_solicitud(),
            "estado": instance.get_estado_solicitud(),
            "tipo_solicitud": instance.get_tipo_solicitud(),
        }
        representation["credencial"] = {
            "estado_credencial": instance.get_estado_credencial(),
            "clave_credencial": instance.get_clave_credencial()
        }
        return representation


class SerializerFichaMedica(ModelSerializer):
    class Meta:
        model = FichaMedica
        fields = "__all__"


class SerializerContactoEmergencia(ModelSerializer):
    class Meta:
        model = ContactoEmergencia
        fields = "__all__"


class SerializerSolicitudesAlumnos(ModelSerializer):
    class Meta:
        model = SolicitudCredencial
        fields = "__all__"


class SerializerGradoEstudio(ModelSerializer):
    class Meta:
        model = GradoDeEstudio
        fields = "__all__"


class SerializerCuatrimestre(ModelSerializer):
    class Meta:
        model = Cuatrimestre
        fields = "__all__"


class SerializerCarrera(ModelSerializer):
    class Meta:
        model = Carrera
        fields = "__all__"
