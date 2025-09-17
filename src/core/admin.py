"""Modelos Django a registrar en la interfaz de administración"""

from django.apps import apps
from django.contrib import admin
from guardian.admin import GuardedModelAdmin
import djf_surveys.models

# Títulos de la pestaña del navegador, cabecera principal y admin login
admin.site.site_title = "Picklefree"
admin.site.site_header = "Administración de Picklefree"
admin.site.index_title = "Panel principal de gestión"

# Ponemos las etiquetas de django-form-surveys en español
djf_surveys.models.Answer._meta.verbose_name = "Respuesta"
djf_surveys.models.Answer._meta.verbose_name_plural = "Respuestas"
djf_surveys.models.Question._meta.verbose_name = "Pregunta"
djf_surveys.models.Question._meta.verbose_name_plural = "Preguntas"
djf_surveys.models.Survey._meta.verbose_name = "Encuesta"
djf_surveys.models.Survey._meta.verbose_name_plural = "Encuestas"
djf_surveys.models.UserAnswer._meta.verbose_name = "Encuesta ya respondida"
djf_surveys.models.UserAnswer._meta.verbose_name_plural = "Encuestas ya respondidas"
djf_surveys.models.TermsValidators._meta.verbose_name = "Validador personalizado"
djf_surveys.models.TermsValidators._meta.verbose_name_plural = "Validadores personalizados"

# Definimos en una lista los modelos que no queremos mostrar en la interfaz de administración
modelos_sin_interfaz_administracion = [
    'DestinatarioClub', 'DestinatarioCurso', 'DestinatarioDirectivo',
    'DestinatarioEquipo', 'DestinatarioInstalacion', 'DestinatarioJugador',
    'DestinatarioPareja', 'DestinatarioOperario', 'DestinatarioPista',
    'DestinatarioTecnico', 'DestinatarioTorneoDobles', 'DestinatarioTorneoEquipos',
    'DestinatarioTorneoIndividual', 'Operario']

# Definimos en un diccionario los campos que queremos que sean de sólo lectura en cada modelo
campos_solo_lectura = {
    'Club'                  : ['token_qr'],
    'Configuracion'         : ['token_qr_global'],
    'Curso'                 : ['token_qr'],
    'Dependencia'           : ['token_qr'],
    'Directivo'             : ['token_qr'],
    'Envio'                 : ['token_qr'],
    'Equipo'                : ['token_qr'],
    'Instalacion'           : ['token_qr'],
    'Jugador'               : ['token_qr'],
    'Material'              : ['token_qr'],
    'Mensaje'               : ['token_qr'],
    'Operario'              : ['token_qr'],
    'Pareja'                : ['token_qr'],
    'PartidoDobles'         : ['token_qr', 'token_qr_confirmacion'],
    'PartidoIndividual'     : ['token_qr', 'token_qr_confirmacion'],
    'Pista'                 : ['token_qr'],
    'Tecnico'               : ['token_qr'],
    'TorneoDobles'          : ['token_qr'],
    'TorneoEquipos'         : ['token_qr'],
    'TorneoIndividual'      : ['token_qr']
}

# Obtenemos la configuración de la app cuyos modelos queremos registrar
app = apps.get_app_config('core')

# Los iteramos y tratamos uno a uno
for modelo in app.get_models():

    # Siempre que no sea un modelo sin interfaz de administración...
    if modelo.__name__ not in modelos_sin_interfaz_administracion:

        # Extraemos del diccionario la lista de campos de sólo lectura del modelo que tratamos
        campos_solo_lectura_del_modelo = campos_solo_lectura.get(modelo.__name__, [])

        # Creamos "al vuelo" un ModelAdmin personalizado para dicho modelo en particular
        # Heredamos de GuardedModelAdmin para que tengan permisos a nivel de objeto
        class ModelAdminPersonalizado(GuardedModelAdmin):
            """ModelAdmin personalizado para un modelo concreto"""
            readonly_fields = campos_solo_lectura_del_modelo

        # Y lo registramos como su interfaz de administración
        admin.site.register(modelo, ModelAdminPersonalizado)
