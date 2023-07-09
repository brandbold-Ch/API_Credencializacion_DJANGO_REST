from rest_framework.serializers import ModelSerializer, CharField
from core.models import Maestro, FichaMedica, Credencial, ContactoEmergencia, SolicitudCredencial


class SerializerMaestro(ModelSerializer):
    password = CharField(write_only=True)

    class Meta:
        model = Maestro
        fields = "__all__"

    def to_representation(self, instance: Maestro):
        representation = super().to_representation(instance)

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


class SerializerSolicitud(ModelSerializer):
    class Meta:
        model = SolicitudCredencial
        fields = "__all__"


class SerializerCredencial(ModelSerializer):
    class Meta:
        model = Credencial
        fields = "__all__"
