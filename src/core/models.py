# pylint: disable=line-too-long
# pylint: disable=too-many-lines
# pylint: disable=protected-access

"""Modelos Django para la generación automática de tablas e interfaces CRUD"""

# Imports

import secrets
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.models import Q
from django.utils import timezone


# Funciones base

def aplicar_docstring_como_comentario_de_tabla(clase):
    """Decorador que asigna el docstring de un clase models.Model de Django como comentario de la tabla (Meta.db_table_comment)"""
    if hasattr(clase, '__doc__') and clase.__doc__:
        clase._meta.db_table_comment = clase.__doc__.strip()
    return clase

def nuevo_token_qr():
    """Generador de valores de 32 caracteres hexadecimales aleatorios, criptográficamente seguros, para uso con códigos QR"""
    return secrets.token_hex(MAXLEN_TOKENQR // 2)


# Globales

MAXLEN_IDENTIFICADOR_LARGO              = 10
MAXLEN_IDENTIFICADOR_CORTO              = 2
MAXLEN_NOMBRE                           = 50
MAXLEN_APELLIDO                         = 50
MAXLEN_LOCALIDAD                        = 50
MAXLEN_TODS                             = 50
MAXLEN_TOKENQR                          = 32
MAXLEN_DIRECCION_CALLE_NUM              = 100
MAXLEN_CODIGOPOSTAL                     = 10
MAXLEN_TELEFONO_E164                    = 16
MAXLEN_EMAIL_DIRECCION                  = 254
MAXLEN_EMAIL_ASUNTO                     = 100
MAXLEN_NOMBRE_LARGO                     = 150
MAXLEN_MENSAJE_REMITENTE                = max(MAXLEN_TELEFONO_E164, MAXLEN_EMAIL_DIRECCION)
MAXLEN_MENSAJE_DESTINATARIO             = max(MAXLEN_TELEFONO_E164, MAXLEN_EMAIL_DIRECCION)
EXTENSIONES_CURRICULUM                  = ['pdf', 'docx', 'doc', 'odt']
EXTENSIONES_PLANO                       = ['pdf', 'svg', 'png', 'dwg', 'dxf']


# Clases

@aplicar_docstring_como_comentario_de_tabla
class CalendarioClub(models.Model):
    """Calendario de un club determinado (cierres prioritarios sobre las aperturas)"""
    id_calendario_club = models.AutoField(primary_key=True)
    id_club = models.ForeignKey('Club', models.RESTRICT, db_column='id_club')
    nombre = models.CharField(max_length=MAXLEN_NOMBRE)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    id_tipo_calendario = models.ForeignKey('TipoCalendario', models.RESTRICT, db_column='id_tipo_calendario')
    id_horario_club = models.ForeignKey('HorarioClub', models.RESTRICT, db_column='id_horario_club', blank=True, null=True)
    fecha_alta = models.DateField(default=timezone.now)
    fecha_baja = models.DateField(blank=True, null=True)
    activo = models.BooleanField(default=True)
    comentarios = models.TextField(blank=True, null=True)
    class Meta:
        """Metadatos"""
        db_table = 'calendario_club'
        verbose_name = 'Calendario de club deportivo'
        verbose_name_plural = 'Calendarios de clubes deportivos'

@aplicar_docstring_como_comentario_de_tabla
class CalendarioInstalacion(models.Model):
    """Calendario global o de club para una instalación dada (cierres prioritarios sobre las aperturas)"""
    id_calendario_instalacion = models.AutoField(primary_key=True)
    id_instalacion = models.ForeignKey('Instalacion', models.RESTRICT, db_column='id_instalacion')
    id_club = models.ForeignKey('Club', models.RESTRICT, db_column='id_club', blank=True, null=True, db_comment='Si no indica ningún club, es global')
    nombre = models.CharField(max_length=MAXLEN_NOMBRE)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    id_tipo_calendario = models.ForeignKey('TipoCalendario', models.RESTRICT, db_column='id_tipo_calendario')
    id_horario_instalacion = models.ForeignKey('HorarioInstalacion', models.RESTRICT, db_column='id_horario_instalacion', blank=True, null=True)
    fecha_alta = models.DateField(default=timezone.now)
    fecha_baja = models.DateField(blank=True, null=True)
    activo = models.BooleanField(default=True)
    comentarios = models.TextField(blank=True, null=True)
    class Meta:
        """Metadatos"""
        db_table = 'calendario_instalacion'
        verbose_name = 'Calendario de instalación deportiva'
        verbose_name_plural = 'Calendarios de instalaciones deportivas'

@aplicar_docstring_como_comentario_de_tabla
class CalendarioPista(models.Model):
    """Calendario de una pista dada (cierres prioritarios sobre las aperturas)"""
    id_calendario_pista = models.AutoField(primary_key=True)
    id_pista = models.ForeignKey('Pista', models.RESTRICT, db_column='id_pista')
    nombre = models.CharField(max_length=MAXLEN_NOMBRE)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    id_tipo_calendario = models.ForeignKey('TipoCalendario', models.RESTRICT, db_column='id_tipo_calendario')
    id_horario_pista = models.ForeignKey('HorarioPista', models.RESTRICT, db_column='id_horario_pista', blank=True, null=True)
    fecha_alta = models.DateField(default=timezone.now)
    fecha_baja = models.DateField(blank=True, null=True)
    activo = models.BooleanField(default=True)
    comentarios = models.TextField(blank=True, null=True)
    class Meta:
        """Metadatos"""
        db_table = 'calendario_pista'
        verbose_name = 'Calendario de pista'
        verbose_name_plural = 'Calendarios de pistas'

@aplicar_docstring_como_comentario_de_tabla
class Categoria(models.Model):
    """Categorías globales o de club para jugadores, parejas y equipos"""
    id_categoria = models.AutoField(primary_key=True)
    id_club = models.ForeignKey('Club', models.RESTRICT, db_column='id_club', blank=True, null=True, db_comment='Si no indica ningún club, es global')
    nombre = models.CharField(max_length=MAXLEN_NOMBRE)
    condicion_minedad = models.IntegerField(blank=True, null=True)
    condicion_maxedad = models.IntegerField(blank=True, null=True)
    id_tipo_sexo = models.ForeignKey('TipoSexo', models.RESTRICT, db_column='id_tipo_sexo', blank=True, null=True)
    condicion_minrating = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    condicion_maxrating = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    fecha_alta = models.DateField(default=timezone.now)
    fecha_baja = models.DateField(blank=True, null=True)
    activa = models.BooleanField(default=True)
    comentarios = models.TextField(blank=True, null=True)
    def __str__(self):
        return str(self.nombre)
    class Meta:
        """Metadatos"""
        db_table = 'categoria'
        verbose_name = 'Categoría de club'
        verbose_name_plural = 'Categorías de clubes'

@aplicar_docstring_como_comentario_de_tabla
class CategoriaEquipo(models.Model):
    """Tabla de combinación N:M categoría-equipo"""
    id_categoria_equipo = models.AutoField(primary_key=True)
    id_categoria = models.ForeignKey('Categoria', models.RESTRICT, db_column='id_categoria')
    id_equipo = models.ForeignKey('Equipo', models.RESTRICT, db_column='id_equipo')
    fecha_alta = models.DateField(default=timezone.now)
    fecha_baja = models.DateField(blank=True, null=True)
    activa = models.BooleanField(default=True)
    comentarios = models.TextField(blank=True, null=True)
    class Meta:
        """Metadatos"""
        db_table = 'categoria_equipo'
        verbose_name = 'Categoría de equipo'
        verbose_name_plural = 'Categorías de equipos'

@aplicar_docstring_como_comentario_de_tabla
class CategoriaJugador(models.Model):
    """Tabla de combinación N:M categoría-jugador"""
    id_categoria_jugador = models.AutoField(primary_key=True)
    id_categoria = models.ForeignKey('Categoria', models.RESTRICT, db_column='id_categoria')
    id_jugador = models.ForeignKey('Jugador', models.RESTRICT, db_column='id_jugador')
    fecha_alta = models.DateField(default=timezone.now)
    fecha_baja = models.DateField(blank=True, null=True)
    activa = models.BooleanField(default=True)
    comentarios = models.TextField(blank=True, null=True)
    class Meta:
        """Metadatos"""
        db_table = 'categoria_jugador'
        verbose_name = 'Categoría de jugador'
        verbose_name_plural = 'Categorías de jugadores'

@aplicar_docstring_como_comentario_de_tabla
class CategoriaPareja(models.Model):
    """Tabla de combinación N:M categoría-pareja"""
    id_categoria_pareja = models.AutoField(primary_key=True)
    id_categoria = models.ForeignKey('Categoria', models.RESTRICT, db_column='id_categoria')
    id_pareja = models.ForeignKey('Pareja', models.RESTRICT, db_column='id_pareja')
    fecha_alta = models.DateField(default=timezone.now)
    fecha_baja = models.DateField(blank=True, null=True)
    activa = models.BooleanField(default=True)
    comentarios = models.TextField(blank=True, null=True)
    class Meta:
        """Metadatos"""
        db_table = 'categoria_pareja'
        verbose_name = 'Categoría de pareja'
        verbose_name_plural = 'Categorías de parejas'

@aplicar_docstring_como_comentario_de_tabla
class ClaseJugador(models.Model):
    """Asistencia a clase de un jugador matriculado en un curso"""
    id_clase_jugador = models.AutoField(primary_key=True)
    id_jugador = models.ForeignKey('Jugador', models.RESTRICT, db_column='id_jugador')
    id_pista = models.ForeignKey('Pista', models.RESTRICT, db_column='id_pista')
    id_curso = models.ForeignKey('Curso', models.RESTRICT, db_column='id_curso')
    fecha_hora = models.DateTimeField(blank=True, null=True, db_comment='Momento de llegada del jugador')
    comentarios = models.TextField(blank=True, null=True)
    class Meta:
        """Metadatos"""
        db_table = 'clase_jugador'
        verbose_name = 'Asistencia a clase'
        verbose_name_plural = 'Asistencias a clases'

@aplicar_docstring_como_comentario_de_tabla
class ClaseProfesor(models.Model):
    """Impartición de clase por un profesor en el marco de un curso"""
    id_clase_profesor = models.AutoField(primary_key=True)
    id_profesor = models.ForeignKey('Tecnico', models.RESTRICT, db_column='id_profesor')
    id_curso = models.ForeignKey('Curso', models.RESTRICT, db_column='id_curso')
    id_estado_clase = models.ForeignKey('EstadoClase', models.RESTRICT, db_column='id_estado_clase')
    fecha_hora = models.DateTimeField(blank=True, null=True, db_comment='Momento de llegada del profesor')
    comentarios = models.TextField(blank=True, null=True)
    class Meta:
        """Metadatos"""
        db_table = 'clase_profesor'
        verbose_name = 'Impartición de clase'
        verbose_name_plural = 'Imparticiones de clases'

@aplicar_docstring_como_comentario_de_tabla
class Club(models.Model):
    """Un club deportivo, con o sin instalaciones propias"""
    id_club = models.AutoField(primary_key=True)
    token_qr = models.CharField(unique=True, max_length=MAXLEN_TOKENQR, default=nuevo_token_qr)
    foto = models.ImageField(upload_to='fotos_clubes/', blank=True, null=True)
    nombre = models.CharField(max_length=MAXLEN_NOMBRE)
    direccion_calle_num = models.CharField(max_length=MAXLEN_DIRECCION_CALLE_NUM)
    direccion_localidad = models.CharField(max_length=MAXLEN_LOCALIDAD)
    direccion_codigopostal = models.CharField(max_length=MAXLEN_CODIGOPOSTAL)
    direccion_provincia = models.ForeignKey('Provincia', models.RESTRICT, db_column='direccion_provincia')
    direccion_pais = CountryField(db_column='direccion_pais')
    telefono_fijo = PhoneNumberField(region='ES', unique=True, blank=True, null=True)
    telefono_movil = PhoneNumberField(region='ES', unique=True, blank=True, null=True)
    telefono_otro = PhoneNumberField(region='ES', unique=True, blank=True, null=True)
    email = models.EmailField(unique=True)
    email_adicional = models.EmailField(unique=True, blank=True, null=True)
    sitio_web = models.URLField(unique=True, blank=True, null=True)
    fecha_alta = models.DateField(default=timezone.now)
    fecha_baja = models.DateField(blank=True, null=True)
    activo = models.BooleanField(default=True)
    comentarios = models.TextField(blank=True, null=True)
    def clean(self):
        """Validación de coherencia interna"""
        if not self.telefono_fijo and not self.telefono_movil and not self.telefono_otro:
            raise ValidationError(f"Club {self.id_club}: Es necesario al menos un teléfono !!!")
    def __str__(self):
        return str(self.nombre)
    class Meta:
        """Metadatos"""
        db_table = 'club'
        verbose_name = 'Club deportivo'
        verbose_name_plural = 'Clubes deportivos'

@aplicar_docstring_como_comentario_de_tabla
class Configuracion(models.Model):
    """Configuraciones globales o a nivel de club"""
    id_configuracion = models.AutoField(primary_key=True)
    id_club = models.ForeignKey('Club', models.RESTRICT, db_column='id_club', blank=True, null=True, db_comment='Si no indica ningún club, es global')
    puntos_victoria = models.IntegerField()
    puntos_empate = models.IntegerField()
    puntos_derrota = models.IntegerField()
    token_qr_global = models.CharField(unique=True, max_length=MAXLEN_TOKENQR, default=nuevo_token_qr)
    fecha_alta = models.DateField(default=timezone.now)
    fecha_baja = models.DateField(blank=True, null=True)
    activa = models.BooleanField(default=True)
    comentarios = models.TextField(blank=True, null=True)
    class Meta:
        """Metadatos"""
        db_table = 'configuracion'
        verbose_name = 'Configuración de club'
        verbose_name_plural = 'Configuraciones de clubes'

@aplicar_docstring_como_comentario_de_tabla
class Contrato(models.Model):
    """Contrato: Tabla de combinación N:M técnico-club"""
    id_contrato = models.AutoField(primary_key=True)
    id_tecnico = models.ForeignKey('Tecnico', models.RESTRICT, db_column='id_tecnico')
    id_club = models.ForeignKey('Club', models.RESTRICT, db_column='id_club')
    id_tipo_contrato = models.ForeignKey('TipoContrato', models.RESTRICT, db_column='id_tipo_contrato')
    fecha_alta = models.DateField(default=timezone.now)
    fecha_baja = models.DateField(blank=True, null=True)
    activo = models.BooleanField(default=True)
    comentarios = models.TextField(blank=True, null=True)
    class Meta:
        """Metadatos"""
        db_table = 'contrato'
        verbose_name = 'Contrato [técnico-club]'
        verbose_name_plural = 'Contratos [técnico-club]'

@aplicar_docstring_como_comentario_de_tabla
class Curso(models.Model):
    """Cursos impartidos"""
    id_curso = models.AutoField(primary_key=True)
    id_club = models.ForeignKey('Club', models.RESTRICT, db_column='id_club')
    id_profesor = models.ForeignKey('Tecnico', models.RESTRICT, db_column='id_profesor')
    id_instalacion = models.ForeignKey('Instalacion', models.RESTRICT, db_column='id_instalacion')
    id_categoria = models.ForeignKey('Categoria', models.RESTRICT, db_column='id_categoria')
    token_qr = models.CharField(unique=True, max_length=MAXLEN_TOKENQR, default=nuevo_token_qr)
    foto = models.ImageField(upload_to='fotos_cursos/', blank=True, null=True)
    nombre = models.CharField(max_length=MAXLEN_NOMBRE_LARGO)
    id_tipo_curso = models.ForeignKey('TipoCurso', models.RESTRICT, db_column='id_tipo_curso')
    curso_inicio = models.DateField()
    curso_fin = models.DateField()
    matricula_inicio = models.DateField()
    matricula_fin = models.DateField()
    aforo_minimo = models.IntegerField()
    aforo_maximo = models.IntegerField()
    comentarios = models.TextField(blank=True, null=True)
    class Meta:
        """Metadatos"""
        db_table = 'curso'
        verbose_name = 'Curso impartido'
        verbose_name_plural = 'Cursos impartidos'

@aplicar_docstring_como_comentario_de_tabla
class Dependencia(models.Model):
    """Cada lugar de una instalación para otros propósitos"""
    id_dependencia = models.AutoField(primary_key=True)
    token_qr = models.CharField(unique=True, max_length=MAXLEN_TOKENQR, default=nuevo_token_qr)
    foto = models.ImageField(upload_to='fotos_dependencias/', blank=True, null=True)
    nombre = models.CharField(max_length=MAXLEN_NOMBRE, blank=True, null=True)
    id_instalacion = models.ForeignKey('Instalacion', models.RESTRICT, db_column='id_instalacion')
    id_tipo_dependencia = models.ForeignKey('TipoDependencia', models.RESTRICT, db_column='id_tipo_dependencia')
    tiene_llave = models.BooleanField()
    dimensiones_longitud = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    dimensiones_archura = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    dimensiones_altura = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    fecha_alta = models.DateField(default=timezone.now)
    fecha_baja = models.DateField(blank=True, null=True)
    activa = models.BooleanField(default=True)
    comentarios = models.TextField(blank=True, null=True)
    class Meta:
        """Metadatos"""
        db_table = 'dependencia'
        verbose_name = 'Dependencia de instalación deportiva'
        verbose_name_plural = 'Dependencias de instalaciones deportivas'

@aplicar_docstring_como_comentario_de_tabla
class DestinatarioClub(models.Model):
    """Clubes destinatarios de un mensaje"""
    id_destinatario_club = models.AutoField(primary_key=True)
    id_mensaje = models.ForeignKey('Mensaje', models.RESTRICT, db_column='id_mensaje')
    id_club = models.ForeignKey('Club', models.RESTRICT, db_column='id_club')
    id_tipo_mensaje = models.ForeignKey('TipoMensaje', models.RESTRICT, db_column='id_tipo_mensaje', blank=True, null=True, db_comment='Por si se quiere hacer override del tipo')
    class Meta:
        """Metadatos"""
        db_table = 'destinatario_club'
        verbose_name = 'Destinatario [club]'
        verbose_name_plural = 'Destinatarios [club]'

@aplicar_docstring_como_comentario_de_tabla
class DestinatarioCurso(models.Model):
    """Cursos destinatarios de un mensaje"""
    id_destinatario_curso = models.AutoField(primary_key=True)
    id_mensaje = models.ForeignKey('Mensaje', models.RESTRICT, db_column='id_mensaje')
    id_curso = models.ForeignKey('Curso', models.RESTRICT, db_column='id_curso')
    id_tipo_mensaje = models.ForeignKey('TipoMensaje', models.RESTRICT, db_column='id_tipo_mensaje', blank=True, null=True, db_comment='Por si se quiere hacer override del tipo')
    class Meta:
        """Metadatos"""
        db_table = 'destinatario_curso'
        verbose_name = 'Destinatario [curso]'
        verbose_name_plural = 'Destinatarios [curso]'

@aplicar_docstring_como_comentario_de_tabla
class DestinatarioDirectivo(models.Model):
    """Directivos destinatarios de un mensaje"""
    id_destinatario_directivo = models.AutoField(primary_key=True)
    id_mensaje = models.ForeignKey('Mensaje', models.RESTRICT, db_column='id_mensaje')
    id_directivo = models.ForeignKey('Directivo', models.RESTRICT, db_column='id_directivo')
    id_tipo_mensaje = models.ForeignKey('TipoMensaje', models.RESTRICT, db_column='id_tipo_mensaje', blank=True, null=True, db_comment='Por si se quiere hacer override del tipo')
    class Meta:
        """Metadatos"""
        db_table = 'destinatario_directivo'
        verbose_name = 'Destinatario [directivo]'
        verbose_name_plural = 'Destinatarios [directivo]'

@aplicar_docstring_como_comentario_de_tabla
class DestinatarioEquipo(models.Model):
    """Equipos destinatarios de un mensaje"""
    id_destinatario_equipo = models.AutoField(primary_key=True)
    id_mensaje = models.ForeignKey('Mensaje', models.RESTRICT, db_column='id_mensaje')
    id_equipo = models.ForeignKey('Equipo', models.RESTRICT, db_column='id_equipo')
    id_tipo_mensaje = models.ForeignKey('TipoMensaje', models.RESTRICT, db_column='id_tipo_mensaje', blank=True, null=True, db_comment='Por si se quiere hacer override del tipo')
    class Meta:
        """Metadatos"""
        db_table = 'destinatario_equipo'
        verbose_name = 'Destinatario [equipo]'
        verbose_name_plural = 'Destinatarios [equipo]'

@aplicar_docstring_como_comentario_de_tabla
class DestinatarioInstalacion(models.Model):
    """Instalaciones destinatarias de un mensaje"""
    id_destinatario_instalacion = models.AutoField(primary_key=True)
    id_mensaje = models.ForeignKey('Mensaje', models.RESTRICT, db_column='id_mensaje')
    id_instalacion = models.ForeignKey('Instalacion', models.RESTRICT, db_column='id_instalacion')
    id_tipo_mensaje = models.ForeignKey('TipoMensaje', models.RESTRICT, db_column='id_tipo_mensaje', blank=True, null=True, db_comment='Por si se quiere hacer override del tipo')
    class Meta:
        """Metadatos"""
        db_table = 'destinatario_instalacion'
        verbose_name = 'Destinatario [instalación]'
        verbose_name_plural = 'Destinatarios [instalación]'

@aplicar_docstring_como_comentario_de_tabla
class DestinatarioJugador(models.Model):
    """Jugadores destinatarios de un mensaje"""
    id_destinatario_jugador = models.AutoField(primary_key=True)
    id_mensaje = models.ForeignKey('Mensaje', models.RESTRICT, db_column='id_mensaje')
    id_jugador = models.ForeignKey('Jugador', models.RESTRICT, db_column='id_jugador')
    id_tipo_mensaje = models.ForeignKey('TipoMensaje', models.RESTRICT, db_column='id_tipo_mensaje', blank=True, null=True, db_comment='Por si se quiere hacer override del tipo')
    class Meta:
        """Metadatos"""
        db_table = 'destinatario_jugador'
        verbose_name = 'Destinatario [jugador]'
        verbose_name_plural = 'Destinatarios [jugador]'

@aplicar_docstring_como_comentario_de_tabla
class DestinatarioOperario(models.Model):
    """Operarios destinatarios de un mensaje"""
    id_destinatario_operario = models.AutoField(primary_key=True)
    id_mensaje = models.ForeignKey('Mensaje', models.RESTRICT, db_column='id_mensaje')
    id_operario = models.ForeignKey('Operario', models.RESTRICT, db_column='id_operario')
    id_tipo_mensaje = models.ForeignKey('TipoMensaje', models.RESTRICT, db_column='id_tipo_mensaje', blank=True, null=True, db_comment='Por si se quiere hacer override del tipo')
    class Meta:
        """Metadatos"""
        db_table = 'destinatario_operario'
        verbose_name = 'Destinatario [operario]'
        verbose_name_plural = 'Destinatarios [operario]'

@aplicar_docstring_como_comentario_de_tabla
class DestinatarioPareja(models.Model):
    """Parejas destinatarias de un mensaje"""
    id_destinatario_pareja = models.AutoField(primary_key=True)
    id_mensaje = models.ForeignKey('Mensaje', models.RESTRICT, db_column='id_mensaje')
    id_pareja = models.ForeignKey('Pareja', models.RESTRICT, db_column='id_pareja')
    id_tipo_mensaje = models.ForeignKey('TipoMensaje', models.RESTRICT, db_column='id_tipo_mensaje', blank=True, null=True, db_comment='Por si se quiere hacer override del tipo')
    class Meta:
        """Metadatos"""
        db_table = 'destinatario_pareja'
        verbose_name = 'Destinatario [pareja]'
        verbose_name_plural = 'Destinatarios [pareja]'

@aplicar_docstring_como_comentario_de_tabla
class DestinatarioPista(models.Model):
    """Pistas destinatarias de un mensaje"""
    id_destinatario_pista = models.AutoField(primary_key=True)
    id_mensaje = models.ForeignKey('Mensaje', models.RESTRICT, db_column='id_mensaje')
    id_pista = models.ForeignKey('Pista', models.RESTRICT, db_column='id_pista')
    id_tipo_mensaje = models.ForeignKey('TipoMensaje', models.RESTRICT, db_column='id_tipo_mensaje', blank=True, null=True, db_comment='Por si se quiere hacer override del tipo')
    class Meta:
        """Metadatos"""
        db_table = 'destinatario_pista'
        verbose_name = 'Destinatario [pista]'
        verbose_name_plural = 'Destinatarios [pista]'

@aplicar_docstring_como_comentario_de_tabla
class DestinatarioTecnico(models.Model):
    """Técnicos destinatarios de un mensaje"""
    id_destinatario_tecnico = models.AutoField(primary_key=True)
    id_mensaje = models.ForeignKey('Mensaje', models.RESTRICT, db_column='id_mensaje')
    id_tecnico = models.ForeignKey('Tecnico', models.RESTRICT, db_column='id_tecnico')
    id_tipo_mensaje = models.ForeignKey('TipoMensaje', models.RESTRICT, db_column='id_tipo_mensaje', blank=True, null=True, db_comment='Por si se quiere hacer override del tipo')
    class Meta:
        """Metadatos"""
        db_table = 'destinatario_tecnico'
        verbose_name = 'Destinatario [técnico]'
        verbose_name_plural = 'Destinatarios [técnico]'

@aplicar_docstring_como_comentario_de_tabla
class DestinatarioTorneoDobles(models.Model):
    """Torneos de dobles destinatarios de un mensaje"""
    id_destinatario_torneo_dobles = models.AutoField(primary_key=True)
    id_mensaje = models.ForeignKey('Mensaje', models.RESTRICT, db_column='id_mensaje')
    id_torneo_dobles = models.ForeignKey('TorneoDobles', models.RESTRICT, db_column='id_torneo_dobles')
    id_tipo_mensaje = models.ForeignKey('TipoMensaje', models.RESTRICT, db_column='id_tipo_mensaje', blank=True, null=True, db_comment='Por si se quiere hacer override del tipo')
    class Meta:
        """Metadatos"""
        db_table = 'destinatario_torneo_dobles'
        verbose_name = 'Destinatario [torneo dobles]'
        verbose_name_plural = 'Destinatarios [torneo dobles]'

@aplicar_docstring_como_comentario_de_tabla
class DestinatarioTorneoEquipos(models.Model):
    """Torneos por equipos destinatarios de un mensaje"""
    id_destinatario_torneo_equipos = models.AutoField(primary_key=True)
    id_mensaje = models.ForeignKey('Mensaje', models.RESTRICT, db_column='id_mensaje')
    id_torneo_equipos = models.ForeignKey('TorneoEquipos', models.RESTRICT, db_column='id_torneo_equipos')
    id_tipo_mensaje = models.ForeignKey('TipoMensaje', models.RESTRICT, db_column='id_tipo_mensaje', blank=True, null=True, db_comment='Por si se quiere hacer override del tipo')
    class Meta:
        """Metadatos"""
        db_table = 'destinatario_torneo_equipos'
        verbose_name = 'Destinatario [torneo equipos]'
        verbose_name_plural = 'Destinatarios [torneo equipos]'

@aplicar_docstring_como_comentario_de_tabla
class DestinatarioTorneoIndividual(models.Model):
    """Torneos individuales destinatarios de un mensaje"""
    id_destinatario_torneo_individual = models.AutoField(primary_key=True)
    id_mensaje = models.ForeignKey('Mensaje', models.RESTRICT, db_column='id_mensaje')
    id_torneo_individual = models.ForeignKey('TorneoIndividual', models.RESTRICT, db_column='id_torneo_individual')
    id_tipo_mensaje = models.ForeignKey('TipoMensaje', models.RESTRICT, db_column='id_tipo_mensaje', blank=True, null=True, db_comment='Por si se quiere hacer override del tipo')
    class Meta:
        """Metadatos"""
        db_table = 'destinatario_torneo_individual'
        verbose_name = 'Destinatario [torneo individual]'
        verbose_name_plural = 'Destinatarios [torneo individual]'

@aplicar_docstring_como_comentario_de_tabla
class Directivo(models.Model):
    """Los directivos son personas con un cargo en un club"""
    id_directivo = models.AutoField(primary_key=True)
    id_persona = models.ForeignKey('Persona', models.RESTRICT, db_column='id_persona')
    token_qr = models.CharField(unique=True, max_length=MAXLEN_TOKENQR, default=nuevo_token_qr)
    curriculum = models.FileField(upload_to='curriculums_directivos/', validators=[FileExtensionValidator(EXTENSIONES_CURRICULUM)], blank=True, null=True)
    fecha_alta = models.DateField(default=timezone.now)
    fecha_baja = models.DateField(blank=True, null=True)
    activo = models.BooleanField(default=True)
    comentarios = models.TextField(blank=True, null=True)
    class Meta:
        """Metadatos"""
        db_table = 'directivo'
        verbose_name = 'Directivo de club'
        verbose_name_plural = 'Directivos de clubes'

@aplicar_docstring_como_comentario_de_tabla
class Envio(models.Model):
    """Envío de mensajes a personas"""
    id_envio = models.AutoField(primary_key=True)
    id_mensaje = models.ForeignKey('Mensaje', models.RESTRICT, db_column='id_mensaje')
    token_qr = models.CharField(unique=True, max_length=MAXLEN_TOKENQR, default=nuevo_token_qr)
    remitente = models.CharField(max_length=MAXLEN_MENSAJE_REMITENTE, db_comment='Dirección o número de remitente usado')
    destinatario = models.CharField(max_length=MAXLEN_MENSAJE_DESTINATARIO, db_comment='Dirección o número de destinatario usado')
    id_tipo_mensaje = models.ForeignKey('TipoMensaje', models.RESTRICT, db_column='id_tipo_mensaje', db_comment='Tipo de mensaje finalmente usado')
    id_estado_envio = models.ForeignKey('EstadoEnvio', models.RESTRICT, db_column='id_estado_envio')
    fecha_hora = models.DateTimeField(default=timezone.now, db_comment='Momento de la creación del envío')
    class Meta:
        """Metadatos"""
        db_table = 'envio'
        verbose_name = 'Envío de mensaje'
        verbose_name_plural = 'Envíos de mensajes'

@aplicar_docstring_como_comentario_de_tabla
class Equipo(models.Model):
    """Los equipos son conjuntos de N jugadores y 0-2 técnicos"""
    id_equipo = models.AutoField(primary_key=True)
    id_club = models.ForeignKey('Club', models.RESTRICT, db_column='id_club')
    token_qr = models.CharField(unique=True, max_length=MAXLEN_TOKENQR, default=nuevo_token_qr)
    foto = models.ImageField(upload_to='fotos_equipos/', blank=True, null=True)
    nombre = models.CharField(max_length=MAXLEN_NOMBRE)
    id_tecnico_primero = models.ForeignKey('Tecnico', models.RESTRICT, db_column='id_tecnico_primero', related_name='equipo_id_tecnico_primero_set', blank=True, null=True)
    id_tecnico_segundo = models.ForeignKey('Tecnico', models.RESTRICT, db_column='id_tecnico_segundo', related_name='equipo_id_tecnico_segundo_set', blank=True, null=True)
    fecha_alta = models.DateField(default=timezone.now)
    fecha_baja = models.DateField(blank=True, null=True)
    activo = models.BooleanField(default=True)
    comentarios = models.TextField(blank=True, null=True)
    class Meta:
        """Metadatos"""
        db_table = 'equipo'
        verbose_name = 'Equipo'
        verbose_name_plural = 'Equipos'

@aplicar_docstring_como_comentario_de_tabla
class Etapa(models.Model):
    """Etapa: Tabla de combinación N:M técnico-equipo"""
    id_etapa = models.AutoField(primary_key=True)
    id_tecnico = models.ForeignKey('Tecnico', models.RESTRICT, db_column='id_tecnico')
    id_equipo = models.ForeignKey('Equipo', models.RESTRICT, db_column='id_equipo')
    id_tipo_tecnico_ejercido = models.ForeignKey('Tecnico', models.RESTRICT, db_column='id_tipo_tecnico_ejercido', related_name='etapa_id_tipo_tecnico_ejercido_set', blank=True, null=True)
    fecha_alta = models.DateField(default=timezone.now)
    fecha_baja = models.DateField(blank=True, null=True)
    activa = models.BooleanField(default=True)
    comentarios = models.TextField(blank=True, null=True)
    class Meta:
        """Metadatos"""
        db_table = 'etapa'
        verbose_name = 'Etapa [técnico-equipo]'
        verbose_name_plural = 'Etapas [técnico-equipo]'

@aplicar_docstring_como_comentario_de_tabla
class HorarioClub(models.Model):
    """Horarios de un club determinado"""
    id_horario_club = models.AutoField(primary_key=True)
    id_club = models.ForeignKey('Club', models.RESTRICT, db_column='id_club')
    nombre = models.CharField(max_length=MAXLEN_NOMBRE)
    id_tipo_diasemanal = models.ForeignKey('TipoDiasemanal', models.RESTRICT, db_column='id_tipo_diasemanal')
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    fecha_alta = models.DateField(default=timezone.now)
    fecha_baja = models.DateField(blank=True, null=True)
    activo = models.BooleanField(default=True)
    comentarios = models.TextField(blank=True, null=True)
    class Meta:
        """Metadatos"""
        db_table = 'horario_club'
        verbose_name = 'Horario de club'
        verbose_name_plural = 'Horarios de clubes'

@aplicar_docstring_como_comentario_de_tabla
class HorarioInstalacion(models.Model):
    """Horarios globales o de club para una instalación dada"""
    id_horario_instalacion = models.AutoField(primary_key=True)
    id_instalacion = models.ForeignKey('Instalacion', models.RESTRICT, db_column='id_instalacion')
    id_club = models.ForeignKey('Club', models.RESTRICT, db_column='id_club', blank=True, null=True, db_comment='Si no indica ningún club, es global')
    nombre = models.CharField(max_length=MAXLEN_NOMBRE)
    id_tipo_diasemanal = models.ForeignKey('TipoDiasemanal', models.RESTRICT, db_column='id_tipo_diasemanal')
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    fecha_alta = models.DateField(default=timezone.now)
    fecha_baja = models.DateField(blank=True, null=True)
    activo = models.BooleanField(default=True)
    comentarios = models.TextField(blank=True, null=True)
    class Meta:
        """Metadatos"""
        db_table = 'horario_instalacion'
        verbose_name = 'Horario de instalación deportiva'
        verbose_name_plural = 'Horarios de instalaciones deportivas'

@aplicar_docstring_como_comentario_de_tabla
class HorarioPista(models.Model):
    """Horarios de una pista dada"""
    id_horario_pista = models.AutoField(primary_key=True)
    id_pista = models.ForeignKey('Pista', models.RESTRICT, db_column='id_pista')
    nombre = models.CharField(max_length=MAXLEN_NOMBRE)
    id_tipo_diasemanal = models.ForeignKey('TipoDiasemanal', models.RESTRICT, db_column='id_tipo_diasemanal')
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    fecha_alta = models.DateField(default=timezone.now)
    fecha_baja = models.DateField(blank=True, null=True)
    activo = models.BooleanField(default=True)
    comentarios = models.TextField(blank=True, null=True)
    class Meta:
        """Metadatos"""
        db_table = 'horario_pista'
        verbose_name = 'Horario de pista'
        verbose_name_plural = 'Horarios de pistas'

@aplicar_docstring_como_comentario_de_tabla
class InscripcionEquipo(models.Model):
    """Inscripciones de equipos a torneos"""
    id_inscripcion_equipo = models.AutoField(primary_key=True)
    id_torneo_equipos = models.ForeignKey('TorneoEquipos', models.RESTRICT, db_column='id_torneo_equipos')
    id_equipo = models.ForeignKey('Equipo', models.RESTRICT, db_column='id_equipo')
    fecha = models.DateField()
    id_estado_inscripcion = models.ForeignKey('EstadoInscripcion', models.RESTRICT, db_column='id_estado_inscripcion')
    class Meta:
        """Metadatos"""
        db_table = 'inscripcion_equipo'
        verbose_name = 'Inscripción de equipo en torneo'
        verbose_name_plural = 'Inscripciones de equipos en torneos'

@aplicar_docstring_como_comentario_de_tabla
class InscripcionJugador(models.Model):
    """Inscripciones individuales a torneos"""
    id_inscripcion_jugador = models.AutoField(primary_key=True)
    id_torneo_individual = models.ForeignKey('TorneoIndividual', models.RESTRICT, db_column='id_torneo_individual')
    id_jugador = models.ForeignKey('Jugador', models.RESTRICT, db_column='id_jugador')
    fecha = models.DateField()
    id_estado_inscripcion = models.ForeignKey('EstadoInscripcion', models.RESTRICT, db_column='id_estado_inscripcion')
    class Meta:
        """Metadatos"""
        db_table = 'inscripcion_jugador'
        verbose_name = 'Inscripción de jugador en torneo'
        verbose_name_plural = 'Inscripciones de jugadores en torneos'

@aplicar_docstring_como_comentario_de_tabla
class InscripcionPareja(models.Model):
    """Inscripciones de parejas a torneos"""
    id_inscripcion_pareja = models.AutoField(primary_key=True)
    id_torneo_dobles = models.ForeignKey('TorneoDobles', models.RESTRICT, db_column='id_torneo_dobles')
    id_pareja = models.ForeignKey('Pareja', models.RESTRICT, db_column='id_pareja')
    fecha = models.DateField()
    id_estado_inscripcion = models.ForeignKey('EstadoInscripcion', models.RESTRICT, db_column='id_estado_inscripcion')
    class Meta:
        """Metadatos"""
        db_table = 'inscripcion_pareja'
        verbose_name = 'Inscripción de pareja en torneo'
        verbose_name_plural = 'Inscripciones de parejas en torneos'

@aplicar_docstring_como_comentario_de_tabla
class Instalacion(models.Model):
    """Instalaciones deportivas fijas o temporales donde se juega"""
    id_instalacion = models.AutoField(primary_key=True)
    token_qr = models.CharField(unique=True, max_length=MAXLEN_TOKENQR, default=nuevo_token_qr)
    foto = models.ImageField(upload_to='fotos_instalaciones/', blank=True, null=True)
    plano = models.FileField(upload_to='planos_instalaciones/', validators=[FileExtensionValidator(EXTENSIONES_PLANO)], blank=True, null=True)
    nombre = models.CharField(max_length=MAXLEN_NOMBRE_LARGO)
    direccion_calle_num = models.CharField(max_length=MAXLEN_DIRECCION_CALLE_NUM)
    direccion_localidad = models.CharField(max_length=MAXLEN_LOCALIDAD)
    direccion_codigopostal = models.CharField(max_length=MAXLEN_CODIGOPOSTAL)
    direccion_provincia = models.ForeignKey('Provincia', models.RESTRICT, db_column='direccion_provincia')
    direccion_pais = CountryField(db_column='direccion_pais')
    geoubicacion_latitud = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    geoubicacion_longitud = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    telefono_fijo = PhoneNumberField(region='ES', unique=True, blank=True, null=True)
    telefono_movil = PhoneNumberField(region='ES', unique=True, blank=True, null=True)
    telefono_otro = PhoneNumberField(region='ES', unique=True, blank=True, null=True)
    email = models.EmailField(unique=True)
    email_adicional = models.EmailField(unique=True, blank=True, null=True)
    sitio_web = models.URLField(unique=True, blank=True, null=True)
    fecha_alta = models.DateField(default=timezone.now)
    fecha_baja = models.DateField(blank=True, null=True)
    activa = models.BooleanField(default=True)
    comentarios = models.TextField(blank=True, null=True)
    def clean(self):
        """Validación de coherencia interna"""
        if not self.telefono_fijo and not self.telefono_movil and not self.telefono_otro:
            raise ValidationError(f"Instalacion {self.id_instalacion}: Es necesario al menos un teléfono !!!")
    def __str__(self):
        return str(self.nombre)
    class Meta:
        """Metadatos"""
        db_table = 'instalacion'
        verbose_name = 'Instalación deportiva'
        verbose_name_plural = 'Instalaciones deportivas'

@aplicar_docstring_como_comentario_de_tabla
class Jugador(models.Model):
    """Los jugadores son personas que practican un deporte"""
    id_jugador = models.AutoField(primary_key=True)
    id_persona = models.ForeignKey('Persona', models.RESTRICT, db_column='id_persona')
    token_qr = models.CharField(unique=True, max_length=MAXLEN_TOKENQR, default=nuevo_token_qr)
    num_federado = models.CharField(unique=True, max_length=MAXLEN_IDENTIFICADOR_LARGO, blank=True, null=True)
    id_tipo_lateralidad = models.ForeignKey('TipoLateralidad', models.RESTRICT, db_column='id_tipo_lateralidad')
    fecha_alta = models.DateField(default=timezone.now)
    fecha_baja = models.DateField(blank=True, null=True)
    activo = models.BooleanField(default=True)
    comentarios = models.TextField(blank=True, null=True)
    def __str__(self):
        return str(self.num_federado)
    class Meta:
        """Metadatos"""
        db_table = 'jugador'
        verbose_name = 'Jugador'
        verbose_name_plural = 'Jugadores'

@aplicar_docstring_como_comentario_de_tabla
class Mandato(models.Model):
    """Contrato: Tabla de combinación N:M directivo-club"""
    id_mandato = models.AutoField(primary_key=True)
    id_directivo = models.ForeignKey('Directivo', models.RESTRICT, db_column='id_directivo')
    id_club = models.ForeignKey('Club', models.RESTRICT, db_column='id_club')
    id_tipo_directivo = models.ForeignKey('TipoDirectivo', models.RESTRICT, db_column='id_tipo_directivo')
    fecha_alta = models.DateField(default=timezone.now)
    fecha_baja = models.DateField(blank=True, null=True)
    activo = models.BooleanField(default=True)
    comentarios = models.TextField(blank=True, null=True)
    class Meta:
        """Metadatos"""
        db_table = 'mandato'
        verbose_name = 'Mandato [directivo-club]'
        verbose_name_plural = 'Mandatos [directivo-club]'

@aplicar_docstring_como_comentario_de_tabla
class Material(models.Model):
    """Elementos portables que se almacenan en dependencias"""
    id_material = models.AutoField(primary_key=True)
    token_qr = models.CharField(unique=True, max_length=MAXLEN_TOKENQR, default=nuevo_token_qr)
    foto = models.ImageField(upload_to='fotos_materiales/', blank=True, null=True)
    nombre = models.CharField(max_length=MAXLEN_NOMBRE)
    cantidad = models.IntegerField()
    id_dependencia = models.ForeignKey('Dependencia', models.RESTRICT, db_column='id_dependencia')
    fecha_alta = models.DateField(default=timezone.now)
    fecha_baja = models.DateField(blank=True, null=True)
    activo = models.BooleanField(default=True)
    comentarios = models.TextField(blank=True, null=True)
    def __str__(self):
        return str(self.nombre)
    class Meta:
        """Metadatos"""
        db_table = 'material'
        verbose_name = 'Material'
        verbose_name_plural = 'Materiales'

@aplicar_docstring_como_comentario_de_tabla
class MatriculaJugador(models.Model):
    """Matriculaciones individuales a cursos"""
    id_matricula_jugador = models.AutoField(primary_key=True)
    id_curso = models.ForeignKey('Curso', models.RESTRICT, db_column='id_curso')
    id_jugador = models.ForeignKey('Jugador', models.RESTRICT, db_column='id_jugador', blank=True, null=True)
    fecha_alta = models.DateField(default=timezone.now)
    fecha_baja = models.DateField(blank=True, null=True)
    activa = models.BooleanField(default=True)
    comentarios = models.TextField(blank=True, null=True)
    class Meta:
        """Metadatos"""
        db_table = 'matricula_jugador'
        verbose_name = 'Matrícula [jugador-curso]'
        verbose_name_plural = 'Matrículas [jugador-curso]'

@aplicar_docstring_como_comentario_de_tabla
class Membresia(models.Model):
    """Membresía: Tabla de combinación N:M jugador-equipo"""
    id_membresia = models.AutoField(primary_key=True)
    id_jugador = models.ForeignKey('Jugador', models.RESTRICT, db_column='id_jugador')
    id_equipo = models.ForeignKey('Equipo', models.RESTRICT, db_column='id_equipo')
    id_tipo_membresia = models.ForeignKey('TipoMembresia', models.RESTRICT, db_column='id_tipo_membresia')
    fecha_alta = models.DateField(default=timezone.now)
    fecha_baja = models.DateField(blank=True, null=True)
    activa = models.BooleanField(default=True)
    comentarios = models.TextField(blank=True, null=True)
    class Meta:
        """Metadatos"""
        db_table = 'membresia'
        verbose_name = 'Membresía [jugador-equipo]'
        verbose_name_plural = 'Membresías [jugador-equipo]'

@aplicar_docstring_como_comentario_de_tabla
class Mensaje(models.Model):
    """Mensajes de un club"""
    id_mensaje = models.AutoField(primary_key=True)
    id_remitente = models.ForeignKey('Club', models.RESTRICT, db_column='id_remitente')
    token_qr = models.CharField(unique=True, max_length=MAXLEN_TOKENQR, default=nuevo_token_qr)
    id_tipo_mensaje = models.ForeignKey('TipoMensaje', models.RESTRICT, db_column='id_tipo_mensaje')
    asunto = models.CharField(max_length=MAXLEN_EMAIL_ASUNTO)
    cuerpo = models.TextField(blank=True, null=True)
    fecha_hora = models.DateTimeField(default=timezone.now, db_comment='Momento de la creación del mensaje')
    aplicacion_futura = models.BooleanField(db_comment='¿Se aplica a nuevos miembros?')
    class Meta:
        """Metadatos"""
        db_table = 'mensaje'
        verbose_name = 'Mensaje'
        verbose_name_plural = 'Mensajes'

@aplicar_docstring_como_comentario_de_tabla
class Pareja(models.Model):
    """Las parejas son conjuntos de dos jugadores"""
    id_pareja = models.AutoField(primary_key=True)
    id_club = models.ForeignKey('Club', models.RESTRICT, db_column='id_club', blank=True, null=True)
    token_qr = models.CharField(unique=True, max_length=MAXLEN_TOKENQR, default=nuevo_token_qr)
    foto = models.ImageField(upload_to='fotos_parejas/', blank=True, null=True)
    nombre = models.CharField(max_length=MAXLEN_NOMBRE)
    id_jugador_izquierdo = models.ForeignKey('Jugador', models.RESTRICT, db_column='id_jugador_izquierdo', related_name='pareja_id_jugador_izquierdo_set', blank=False, null=False)
    id_jugador_derecho = models.ForeignKey('Jugador', models.RESTRICT, db_column='id_jugador_derecho', related_name='pareja_id_jugador_derecho_set', blank=False, null=False)
    fecha_alta = models.DateField(default=timezone.now)
    fecha_baja = models.DateField(blank=True, null=True)
    activa = models.BooleanField(default=True)
    comentarios = models.TextField(blank=True, null=True)
    def clean(self):
        """Validación de coherencia interna"""
        # Error si los dos miembros de la pareja tienen valor y apuntan al mismo jugador
        if self.id_jugador_izquierdo and self.id_jugador_derecho and self.id_jugador_izquierdo == self.id_jugador_derecho:
            raise ValidationError('Los jugadores de una pareja deben ser distintos entre sí')
        # Error si la pareja que queremos crear ya existe (con sus miembros en en cualquier orden)
        elif self.__class__.objects.exclude(pk=self.pk).filter(Q(id_jugador_izquierdo=self.id_jugador_izquierdo, id_jugador_derecho=self.id_jugador_derecho) | Q(id_jugador_izquierdo=self.id_jugador_derecho, id_jugador_derecho=self.id_jugador_izquierdo)).exists():
            raise ValidationError('Esta pareja de jugadores ya existe (con sus miembros en cualquier orden)')
    def __str__(self):
        return str(self.nombre)
    class Meta:
        """Metadatos"""
        db_table = 'pareja'
        verbose_name = 'Pareja'
        verbose_name_plural = 'Parejas'

@aplicar_docstring_como_comentario_de_tabla
class PartidoDobles(models.Model):
    """Partidos de dobles sueltos o de torneo, y sus resultados"""
    id_partido_dobles = models.AutoField(primary_key=True)
    id_pareja_local = models.ForeignKey('Pareja', models.RESTRICT, db_column='id_pareja_local', related_name='partidodobles_id_pareja_local_set')
    id_pareja_visitante = models.ForeignKey('Pareja', models.RESTRICT, db_column='id_pareja_visitante', related_name='partidodobles_id_pareja_visitante_set')
    token_qr = models.CharField(unique=True, max_length=MAXLEN_TOKENQR, default=nuevo_token_qr)
    token_qr_confirmacion = models.CharField(unique=True, max_length=MAXLEN_TOKENQR, default=nuevo_token_qr)
    id_estado_partido = models.ForeignKey('EstadoPartido', models.RESTRICT, db_column='id_estado_partido')
    id_pista = models.ForeignKey('Pista', models.RESTRICT, db_column='id_pista', blank=True, null=True)
    id_torneo_dobles = models.ForeignKey('TorneoDobles', models.RESTRICT, db_column='id_torneo_dobles', blank=True, null=True, db_comment='Si pertenece a un torneo')
    ronda_o_jornada = models.IntegerField(blank=True, null=True)
    fecha_hora = models.DateTimeField(db_comment='Momento de celebración del partido')
    tods_formato = models.CharField(max_length=MAXLEN_TODS)
    tods_resultado = models.CharField(max_length=MAXLEN_TODS, blank=True, null=True)
    id_ganador = models.ForeignKey('Pareja', models.RESTRICT, db_column='id_ganador', related_name='partidodobles_id_ganador_set')
    comentarios = models.TextField(blank=True, null=True)
    class Meta:
        """Metadatos"""
        db_table = 'partido_dobles'
        verbose_name = 'Partido de dobles'
        verbose_name_plural = 'Partidos de dobles'

@aplicar_docstring_como_comentario_de_tabla
class PartidoIndividual(models.Model):
    """Partidos individuales sueltos o de torneo, y sus resultados"""
    id_partido_individual = models.AutoField(primary_key=True)
    id_jugador_local = models.ForeignKey('Jugador', models.RESTRICT, db_column='id_jugador_local', related_name='partidoindividual_id_jugador_local_set')
    id_jugador_visitante = models.ForeignKey('Jugador', models.RESTRICT, db_column='id_jugador_visitante', related_name='partidoindividual_id_jugador_visitante_set')
    token_qr = models.CharField(unique=True, max_length=MAXLEN_TOKENQR, default=nuevo_token_qr)
    token_qr_confirmacion = models.CharField(unique=True, max_length=MAXLEN_TOKENQR, default=nuevo_token_qr)
    id_estado_partido = models.ForeignKey('EstadoPartido', models.RESTRICT, db_column='id_estado_partido')
    id_pista = models.ForeignKey('Pista', models.RESTRICT, db_column='id_pista', blank=True, null=True)
    id_torneo_individual = models.ForeignKey('TorneoIndividual', models.RESTRICT, db_column='id_torneo_individual', blank=True, null=True, db_comment='Si pertenece a un torneo')
    ronda_o_jornada = models.IntegerField(blank=True, null=True)
    fecha_hora = models.DateTimeField(db_comment='Momento de celebración del partido')
    tods_formato = models.CharField(max_length=MAXLEN_TODS)
    tods_resultado = models.CharField(max_length=MAXLEN_TODS, blank=True, null=True)
    id_ganador = models.ForeignKey('Jugador', models.RESTRICT, db_column='id_ganador', related_name='partidoindividual_id_ganador_set')
    comentarios = models.TextField(blank=True, null=True)
    class Meta:
        """Metadatos"""
        db_table = 'partido_individual'
        verbose_name = 'Partido individual'
        verbose_name_plural = 'Partidos individuales'

@aplicar_docstring_como_comentario_de_tabla
class Persona(models.Model):
    """Agrupamos todos los tipos de persona (evitamos duplicidades)"""
    id_persona = models.AutoField(primary_key=True)
    foto = models.ImageField(upload_to='fotos_personas/', blank=True, null=True)
    id_tipo_identificacion = models.ForeignKey('TipoIdentificacion', models.RESTRICT, db_column='id_tipo_identificacion')
    docidentidad_valor = models.CharField(max_length=MAXLEN_IDENTIFICADOR_LARGO)
    nombre = models.CharField(max_length=MAXLEN_NOMBRE)
    apellido_primero = models.CharField(max_length=MAXLEN_APELLIDO)
    apellido_segundo = models.CharField(max_length=MAXLEN_APELLIDO, blank=True, null=True)
    id_tipo_sexo = models.ForeignKey('TipoSexo', models.RESTRICT, db_column='id_tipo_sexo')
    direccion_calle_num = models.CharField(max_length=MAXLEN_DIRECCION_CALLE_NUM)
    direccion_localidad = models.CharField(max_length=MAXLEN_LOCALIDAD)
    direccion_codigopostal = models.CharField(max_length=MAXLEN_CODIGOPOSTAL)
    direccion_provincia = models.ForeignKey('Provincia', models.RESTRICT, db_column='direccion_provincia')
    direccion_pais = CountryField(db_column='direccion_pais')
    nacimiento_fecha = models.DateField(blank=True, null=True)
    nacimiento_localidad = models.CharField(max_length=MAXLEN_LOCALIDAD, blank=True, null=True)
    nacimiento_pais = CountryField(db_column='nacimientos_pais')
    telefono_fijo = PhoneNumberField(region='ES', unique=True, blank=True, null=True)
    telefono_movil = PhoneNumberField(region='ES', unique=True, blank=True, null=True)
    telefono_otro = PhoneNumberField(region='ES', unique=True, blank=True, null=True)
    email = models.EmailField(unique=True)
    email_adicional = models.EmailField(unique=True, blank=True, null=True)
    auth_user = models.IntegerField(unique=True, blank=True, null=True, db_comment='Puntero a la tabla auth_user de Django')
    fecha_alta = models.DateField(default=timezone.now)
    fecha_baja = models.DateField(blank=True, null=True)
    activo = models.BooleanField(default=True)
    comentarios = models.TextField(blank=True, null=True)
    def clean(self):
        """Validación de coherencia interna"""
        if not self.telefono_fijo and not self.telefono_movil and not self.telefono_otro:
            raise ValidationError(f"Persona {self.id_persona}: Es necesario al menos un teléfono")
    def __str__(self):
        return f"{self.apellido_primero}{' ' + self.apellido_segundo if self.apellido_segundo else ''}, {self.nombre} [{self.docidentidad_valor}]"
    class Meta:
        """Metadatos"""
        db_table = 'persona'
        verbose_name = 'Persona'
        verbose_name_plural = 'Personas'
        unique_together = (('id_tipo_identificacion', 'docidentidad_valor'),)

@aplicar_docstring_como_comentario_de_tabla
class Pertenencia(models.Model):
    """Pertenencia: Tabla de combinación N:M jugador-club"""
    id_pertenencia = models.AutoField(primary_key=True)
    id_jugador = models.ForeignKey('Jugador', models.RESTRICT, db_column='id_jugador')
    id_club = models.ForeignKey('Club', models.RESTRICT, db_column='id_club')
    fecha_alta = models.DateField(default=timezone.now)
    fecha_baja = models.DateField(blank=True, null=True)
    activa = models.BooleanField(default=True)
    comentarios = models.TextField(blank=True, null=True)
    class Meta:
        """Metadatos"""
        db_table = 'pertenencia'
        verbose_name = 'Pertenencia [jugador-club]'
        verbose_name_plural = 'Pertenencias [jugador-club]'

@aplicar_docstring_como_comentario_de_tabla
class Pista(models.Model):
    """Cada lugar de una instalación donde se juegan partidos"""
    id_pista = models.AutoField(primary_key=True)
    token_qr = models.CharField(unique=True, max_length=MAXLEN_TOKENQR, default=nuevo_token_qr)
    foto = models.ImageField(upload_to='fotos_pistas/', blank=True, null=True)
    nombre = models.CharField(max_length=MAXLEN_NOMBRE, blank=True, null=True)
    id_instalacion = models.ForeignKey('Instalacion', models.RESTRICT, db_column='id_instalacion')
    id_tipo_pista = models.ForeignKey('TipoPista', models.RESTRICT, db_column='id_tipo_pista')
    id_tipo_suelo = models.ForeignKey('TipoSuelo', models.RESTRICT, db_column='id_tipo_suelo')
    iluminada = models.BooleanField()
    tiene_llave = models.BooleanField()
    dimensiones_longitud = models.DecimalField(max_digits=5, decimal_places=2)
    dimensiones_archura = models.DecimalField(max_digits=5, decimal_places=2)
    dimensiones_altura = models.DecimalField(max_digits=4, decimal_places=2)
    fecha_alta = models.DateField(default=timezone.now)
    fecha_baja = models.DateField(blank=True, null=True)
    activa = models.BooleanField(default=True)
    comentarios = models.TextField(blank=True, null=True)
    def __str__(self):
        return str(self.nombre)
    class Meta:
        """Metadatos"""
        db_table = 'pista'
        verbose_name = 'Pista'
        verbose_name_plural = 'Pistas'

@aplicar_docstring_como_comentario_de_tabla
class Provincia(models.Model):
    """Provincias de España"""
    id_provincia = models.AutoField(primary_key=True)
    nombre = models.CharField(unique=True, max_length=MAXLEN_NOMBRE)
    codigo_ine = models.CharField(unique=True, max_length=MAXLEN_IDENTIFICADOR_CORTO)
    def __str__(self):
        return str(self.nombre)
    class Meta:
        """Metadatos"""
        db_table = 'provincia'
        verbose_name = 'Provincia'
        verbose_name_plural = 'Provincias'

@aplicar_docstring_como_comentario_de_tabla
class RankingJugadorClub(models.Model):
    """Ranking de un jugador en un club a lo largo del tiempo"""
    id_ranking_jugador_club = models.AutoField(primary_key=True)
    id_jugador = models.ForeignKey('Jugador', models.RESTRICT, db_column='id_jugador')
    id_club = models.ForeignKey('Club', models.RESTRICT, db_column='id_club')
    victorias = models.IntegerField()
    empates = models.IntegerField()
    derrotas = models.IntegerField()
    puntos = models.IntegerField()
    posicion = models.IntegerField()
    fecha = models.DateField()
    class Meta:
        """Metadatos"""
        db_table = 'ranking_jugador_club'
        verbose_name = 'Ranking de jugador en club'
        verbose_name_plural = 'Rankings de jugadores en clubes'
        unique_together = (('id_jugador', 'id_club', 'fecha'),)

@aplicar_docstring_como_comentario_de_tabla
class RankingJugadorTorneo(models.Model):
    """Ranking de un jugador en un torneo determinado"""
    id_ranking_jugador_torneo = models.AutoField(primary_key=True)
    id_jugador = models.ForeignKey('Jugador', models.RESTRICT, db_column='id_jugador')
    id_torneo_individual = models.ForeignKey('TorneoIndividual', models.RESTRICT, db_column='id_torneo_individual')
    ronda_o_jornada = models.IntegerField()
    victorias = models.IntegerField()
    empates = models.IntegerField()
    derrotas = models.IntegerField()
    puntos = models.IntegerField()
    posicion = models.IntegerField()
    fecha = models.DateField()
    class Meta:
        """Metadatos"""
        db_table = 'ranking_jugador_torneo'
        verbose_name = 'Ranking de jugador en torneo'
        verbose_name_plural = 'Rankings de jugadores en torneos'
        unique_together = (('id_jugador', 'id_torneo_individual', 'ronda_o_jornada'),)

@aplicar_docstring_como_comentario_de_tabla
class RankingParejaClub(models.Model):
    """Ranking de una pareja en un club a lo largo del tiempo"""
    id_ranking_pareja_club = models.AutoField(primary_key=True)
    id_pareja = models.ForeignKey('Pareja', models.RESTRICT, db_column='id_pareja')
    id_club = models.ForeignKey('Club', models.RESTRICT, db_column='id_club')
    victorias = models.IntegerField()
    empates = models.IntegerField()
    derrotas = models.IntegerField()
    puntos = models.IntegerField()
    posicion = models.IntegerField()
    fecha = models.DateField()
    class Meta:
        """Metadatos"""
        db_table = 'ranking_pareja_club'
        verbose_name = 'Ranking de pareja en club'
        verbose_name_plural = 'Rankings de parejas en clubes'
        unique_together = (('id_pareja', 'id_club', 'fecha'),)

@aplicar_docstring_como_comentario_de_tabla
class RankingParejaTorneo(models.Model):
    """Ranking de una pareja en un torneo de dobles determinado"""
    id_ranking_pareja_torneo = models.AutoField(primary_key=True)
    id_pareja = models.ForeignKey('Pareja', models.RESTRICT, db_column='id_pareja')
    id_torneo_dobles = models.ForeignKey('TorneoDobles', models.RESTRICT, db_column='id_torneo_dobles')
    ronda_o_jornada = models.IntegerField()
    victorias = models.IntegerField()
    empates = models.IntegerField()
    derrotas = models.IntegerField()
    puntos = models.IntegerField()
    posicion = models.IntegerField()
    fecha = models.DateField()
    class Meta:
        """Metadatos"""
        db_table = 'ranking_pareja_torneo'
        verbose_name = 'Ranking de pareja en torneo'
        verbose_name_plural = 'Rankings de parejas en torneos'
        unique_together = (('id_pareja', 'id_torneo_dobles', 'ronda_o_jornada'),)

@aplicar_docstring_como_comentario_de_tabla
class Rating(models.Model):
    """Rating de un jugador a lo largo del tiempo"""
    id_rating = models.AutoField(primary_key=True)
    id_jugador = models.ForeignKey('Jugador', models.RESTRICT, db_column='id_jugador')
    wpr_puntuacion = models.DecimalField(max_digits=4, decimal_places=2)
    wpr_incertidumbre = models.IntegerField()
    fecha = models.DateField()
    class Meta:
        """Metadatos"""
        db_table = 'rating'
        verbose_name = 'Rating'
        verbose_name_plural = 'Ratings'
        unique_together = (('id_jugador', 'fecha'),)

@aplicar_docstring_como_comentario_de_tabla
class ReservaClub(models.Model):
    """Reserva de pista de un club, puede que para un equipo concreto"""
    id_reserva_club = models.AutoField(primary_key=True)
    id_pista = models.ForeignKey('Pista', models.RESTRICT, db_column='id_pista')
    id_club = models.ForeignKey('Club', models.RESTRICT, db_column='id_club')
    id_equipo = models.ForeignKey('Equipo', models.RESTRICT, db_column='id_equipo', blank=True, null=True)
    fecha_reserva = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    fecha_solicitud = models.DateTimeField(default=timezone.now)
    fecha_confirmacion = models.DateTimeField(blank=True, null=True)
    fecha_cancelacion = models.DateTimeField(blank=True, null=True)
    fecha_asistencia = models.DateTimeField(blank=True, null=True)
    class Meta:
        """Metadatos"""
        db_table = 'reserva_club'
        verbose_name = 'Reserva de club'
        verbose_name_plural = 'Reservas de clubes'
        unique_together = (('id_pista', 'fecha_reserva', 'hora_inicio', 'hora_fin'),)

@aplicar_docstring_como_comentario_de_tabla
class ReservaCurso(models.Model):
    """Reserva de pista por parte de un curso"""
    id_reserva_curso = models.AutoField(primary_key=True)
    id_pista = models.ForeignKey('Pista', models.RESTRICT, db_column='id_pista')
    id_curso = models.ForeignKey('Curso', models.RESTRICT, db_column='id_curso')
    fecha_reserva = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    fecha_solicitud = models.DateTimeField(default=timezone.now)
    fecha_confirmacion = models.DateTimeField(blank=True, null=True)
    fecha_cancelacion = models.DateTimeField(blank=True, null=True)
    fecha_asistencia = models.DateTimeField(blank=True, null=True)
    class Meta:
        """Metadatos"""
        db_table = 'reserva_curso'
        verbose_name = 'Reserva de curso'
        verbose_name_plural = 'Reservas de cursos'
        unique_together = (('id_pista', 'fecha_reserva', 'hora_inicio', 'hora_fin'),)

@aplicar_docstring_como_comentario_de_tabla
class ReservaJugador(models.Model):
    """Reserva de pista por parte de un jugador"""
    id_reserva_jugador = models.AutoField(primary_key=True)
    id_pista = models.ForeignKey('Pista', models.RESTRICT, db_column='id_pista')
    id_jugador = models.ForeignKey('Jugador', models.RESTRICT, db_column='id_jugador')
    fecha_reserva = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    fecha_solicitud = models.DateTimeField(default=timezone.now)
    fecha_confirmacion = models.DateTimeField(blank=True, null=True)
    fecha_cancelacion = models.DateTimeField(blank=True, null=True)
    fecha_asistencia = models.DateTimeField(blank=True, null=True)
    class Meta:
        """Metadatos"""
        db_table = 'reserva_jugador'
        verbose_name = 'Reserva de jugador'
        verbose_name_plural = 'Reservas de jugadores'
        unique_together = (('id_pista', 'fecha_reserva', 'hora_inicio', 'hora_fin'),)

@aplicar_docstring_como_comentario_de_tabla
class ReservaTorneoDobles(models.Model):
    """Reserva de pista por parte de un torneo de dobles"""
    id_reserva_torneo_dobles = models.AutoField(primary_key=True)
    id_pista = models.ForeignKey('Pista', models.RESTRICT, db_column='id_pista')
    id_torneo_dobles = models.ForeignKey('TorneoDobles', models.RESTRICT, db_column='id_torneo_dobles')
    fecha_reserva = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    fecha_solicitud = models.DateTimeField(default=timezone.now)
    fecha_confirmacion = models.DateTimeField(blank=True, null=True)
    fecha_cancelacion = models.DateTimeField(blank=True, null=True)
    fecha_asistencia = models.DateTimeField(blank=True, null=True)
    class Meta:
        """Metadatos"""
        db_table = 'reserva_torneo_dobles'
        verbose_name = 'Reserva de torneo de dobles'
        verbose_name_plural = 'Reservas de torneos de dobles'
        unique_together = (('id_pista', 'fecha_reserva', 'hora_inicio', 'hora_fin'),)

@aplicar_docstring_como_comentario_de_tabla
class ReservaTorneoEquipos(models.Model):
    """Reserva de pista por parte de un torneo por equipos"""
    id_reserva_torneo_equipos = models.AutoField(primary_key=True)
    id_pista = models.ForeignKey('Pista', models.RESTRICT, db_column='id_pista')
    id_torneo_equipos = models.ForeignKey('TorneoEquipos', models.RESTRICT, db_column='id_torneo_equipos')
    fecha_reserva = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    fecha_solicitud = models.DateTimeField(default=timezone.now)
    fecha_confirmacion = models.DateTimeField(blank=True, null=True)
    fecha_cancelacion = models.DateTimeField(blank=True, null=True)
    fecha_asistencia = models.DateTimeField(blank=True, null=True)
    class Meta:
        """Metadatos"""
        db_table = 'reserva_torneo_equipos'
        verbose_name = 'Reserva de torneo por equipos'
        verbose_name_plural = 'Reservas de torneos por equipos'
        unique_together = (('id_pista', 'fecha_reserva', 'hora_inicio', 'hora_fin'),)

@aplicar_docstring_como_comentario_de_tabla
class ReservaTorneoIndividual(models.Model):
    """Reserva de pista por parte de un torneo individual"""
    id_reserva_torneo_individual = models.AutoField(primary_key=True)
    id_pista = models.ForeignKey('Pista', models.RESTRICT, db_column='id_pista')
    id_torneo_individual = models.ForeignKey('TorneoIndividual', models.RESTRICT, db_column='id_torneo_individual')
    fecha_reserva = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    fecha_solicitud = models.DateTimeField(default=timezone.now)
    fecha_confirmacion = models.DateTimeField(blank=True, null=True)
    fecha_cancelacion = models.DateTimeField(blank=True, null=True)
    fecha_asistencia = models.DateTimeField(blank=True, null=True)
    class Meta:
        """Metadatos"""
        db_table = 'reserva_torneo_individual'
        verbose_name = 'Reserva de torneo individual'
        verbose_name_plural = 'Reservas de torneos individuales'
        unique_together = (('id_pista', 'fecha_reserva', 'hora_inicio', 'hora_fin'),)

@aplicar_docstring_como_comentario_de_tabla
class Tecnico(models.Model):
    """Los técnicos son personas que poseen una titulación"""
    id_tecnico = models.AutoField(primary_key=True)
    id_persona = models.ForeignKey('Persona', models.RESTRICT, db_column='id_persona')
    token_qr = models.CharField(unique=True, max_length=MAXLEN_TOKENQR, default=nuevo_token_qr)
    num_federado = models.CharField(unique=True, max_length=MAXLEN_IDENTIFICADOR_LARGO, blank=True, null=True)
    id_tipo_titulacion = models.ForeignKey('TipoTitulacion', models.RESTRICT, db_column='id_tipo_titulacion')
    fecha_alta = models.DateField(default=timezone.now)
    fecha_baja = models.DateField(blank=True, null=True)
    activo = models.BooleanField(default=True)
    comentarios = models.TextField(blank=True, null=True)
    class Meta:
        """Metadatos"""
        db_table = 'tecnico'
        verbose_name = 'Técnico'
        verbose_name_plural = 'Técnicos'

@aplicar_docstring_como_comentario_de_tabla
class Posesion(models.Model):
    """Posesion: Tabla de combinación N:M instalacion-club"""
    id_posesion = models.AutoField(primary_key=True)
    id_instalacion = models.ForeignKey('Instalacion', models.RESTRICT, db_column='id_instalacion')
    id_club = models.ForeignKey('Club', models.RESTRICT, db_column='id_club')
    id_tipo_posesion = models.ForeignKey('TipoPosesion', models.RESTRICT, db_column='id_tipo_posesion')
    fecha_alta = models.DateField(default=timezone.now)
    fecha_baja = models.DateField(blank=True, null=True)
    activa = models.BooleanField(default=True)
    comentarios = models.TextField(blank=True, null=True)
    class Meta:
        """Metadatos"""
        db_table = 'posesion'
        verbose_name = 'Posesión [instalación-club]'
        verbose_name_plural = 'Posesiones [instalación-club]'

@aplicar_docstring_como_comentario_de_tabla
class TorneoDobles(models.Model):
    """Torneos de dobles"""
    id_torneo_dobles = models.AutoField(primary_key=True)
    id_club = models.ForeignKey('Club', models.RESTRICT, db_column='id_club')
    id_director = models.ForeignKey('Tecnico', models.RESTRICT, db_column='id_director')
    id_instalacion = models.ForeignKey('Instalacion', models.RESTRICT, db_column='id_instalacion')
    id_categoria = models.ForeignKey('Categoria', models.RESTRICT, db_column='id_categoria')
    token_qr = models.CharField(unique=True, max_length=MAXLEN_TOKENQR, default=nuevo_token_qr)
    foto = models.ImageField(upload_to='fotos_torneos_dobles/', blank=True, null=True)
    nombre = models.CharField(max_length=MAXLEN_NOMBRE_LARGO)
    mixto = models.BooleanField(db_comment='¿De parejas mixtas?')
    id_tipo_competicion = models.ForeignKey('TipoCompeticion', models.RESTRICT, db_column='id_tipo_competicion')
    rondas_o_jornadas = models.IntegerField()
    torneo_inicio = models.DateField()
    torneo_fin = models.DateField()
    inscripcion_inicio = models.DateField()
    inscripcion_fin = models.DateField()
    aforo_minimo = models.IntegerField()
    aforo_maximo = models.IntegerField()
    comentarios = models.TextField(blank=True, null=True)
    class Meta:
        """Metadatos"""
        db_table = 'torneo_dobles'
        verbose_name = 'Torneo de dobles'
        verbose_name_plural = 'Torneos de dobles'

@aplicar_docstring_como_comentario_de_tabla
class TorneoEquipos(models.Model):
    """Torneos por equipos"""
    id_torneo_equipos = models.AutoField(primary_key=True)
    id_club = models.ForeignKey('Club', models.RESTRICT, db_column='id_club')
    id_director = models.ForeignKey('Tecnico', models.RESTRICT, db_column='id_director')
    id_instalacion = models.ForeignKey('Instalacion', models.RESTRICT, db_column='id_instalacion')
    id_categoria = models.ForeignKey('Categoria', models.RESTRICT, db_column='id_categoria')
    token_qr = models.CharField(unique=True, max_length=MAXLEN_TOKENQR, default=nuevo_token_qr)
    foto = models.ImageField(upload_to='fotos_torneos_equipos/', blank=True, null=True)
    nombre = models.CharField(max_length=MAXLEN_NOMBRE_LARGO)
    integrantes_minimos = models.IntegerField()
    integrantes_maximos = models.IntegerField()
    id_tipo_competicion = models.ForeignKey('TipoCompeticion', models.RESTRICT, db_column='id_tipo_competicion')
    rondas_o_jornadas = models.IntegerField()
    torneo_inicio = models.DateField()
    torneo_fin = models.DateField()
    inscripcion_inicio = models.DateField()
    inscripcion_fin = models.DateField()
    aforo_minimo = models.IntegerField()
    aforo_maximo = models.IntegerField()
    comentarios = models.TextField(blank=True, null=True)
    class Meta:
        """Metadatos"""
        db_table = 'torneo_equipos'
        verbose_name = 'Torneo por equipos'
        verbose_name_plural = 'Torneos por equipos'

@aplicar_docstring_como_comentario_de_tabla
class TorneoIndividual(models.Model):
    """Torneos individuales"""
    id_torneo_individual = models.AutoField(primary_key=True)
    id_club = models.ForeignKey('Club', models.RESTRICT, db_column='id_club')
    id_director = models.ForeignKey('Tecnico', models.RESTRICT, db_column='id_director')
    id_instalacion = models.ForeignKey('Instalacion', models.RESTRICT, db_column='id_instalacion')
    id_categoria = models.ForeignKey('Categoria', models.RESTRICT, db_column='id_categoria')
    token_qr = models.CharField(unique=True, max_length=MAXLEN_TOKENQR, default=nuevo_token_qr)
    foto = models.ImageField(upload_to='fotos_torneos_individuales/', blank=True, null=True)
    nombre = models.CharField(max_length=MAXLEN_NOMBRE_LARGO)
    id_tipo_competicion = models.ForeignKey('TipoCompeticion', models.RESTRICT, db_column='id_tipo_competicion')
    rondas_o_jornadas = models.IntegerField()
    torneo_inicio = models.DateField()
    torneo_fin = models.DateField()
    inscripcion_inicio = models.DateField()
    inscripcion_fin = models.DateField()
    aforo_minimo = models.IntegerField()
    aforo_maximo = models.IntegerField()
    comentarios = models.TextField(blank=True, null=True)
    class Meta:
        """Metadatos"""
        db_table = 'torneo_individual'
        verbose_name = 'Torneo individual'
        verbose_name_plural = 'Torneos individuales'

@aplicar_docstring_como_comentario_de_tabla
class TipoCalendario(models.Model):
    """Tipos de entradas de calendario"""
    id_tipo_calendario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=MAXLEN_NOMBRE)
    fecha_alta = models.DateField(default=timezone.now)
    fecha_baja = models.DateField(blank=True, null=True)
    activo = models.BooleanField(default=True)
    comentarios = models.TextField(blank=True, null=True)
    def clean(self):
        """Validación de coherencia interna"""
        if self.fecha_baja and self.activo:
            raise ValidationError(f"TipoCalendario {self.id_tipo_calendario}: Activo y con fecha de baja !!!")
        if self.fecha_baja and self.fecha_baja < timezone.now().date():
            self.activo = False
    class Meta:
        """Metadatos"""
        db_table = 'tipo_calendario'
        verbose_name = 'Tipo de calendario'
        verbose_name_plural = 'Tipos de calendario'

@aplicar_docstring_como_comentario_de_tabla
class TipoSexo(models.Model):
    """Tipos de sexo posibles"""
    id_tipo_sexo = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=MAXLEN_NOMBRE)
    fecha_alta = models.DateField(default=timezone.now)
    fecha_baja = models.DateField(blank=True, null=True)
    activo = models.BooleanField(default=True)
    comentarios = models.TextField(blank=True, null=True)
    def clean(self):
        """Validación de coherencia interna"""
        if self.fecha_baja and self.activo:
            raise ValidationError(f"TipoSexo {self.id_tipo_sexo}: Activo y con fecha de baja !!!")
        if self.fecha_baja and self.fecha_baja < timezone.now().date():
            self.activo = False
    def __str__(self):
        return str(self.nombre)
    class Meta:
        """Metadatos"""
        db_table = 'tipo_sexo'
        verbose_name = 'Sexo'
        verbose_name_plural = 'Sexos'

@aplicar_docstring_como_comentario_de_tabla
class EstadoClase(models.Model):
    """Estados posibles de una clase"""
    id_estado_clase = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=MAXLEN_NOMBRE)
    fecha_alta = models.DateField(default=timezone.now)
    fecha_baja = models.DateField(blank=True, null=True)
    activo = models.BooleanField(default=True)
    comentarios = models.TextField(blank=True, null=True)
    def clean(self):
        """Validación de coherencia interna"""
        if self.fecha_baja and self.activo:
            raise ValidationError(f"EstadoClase {self.id_estado_clase}: Activo y con fecha de baja !!!")
        if self.fecha_baja and self.fecha_baja < timezone.now().date():
            self.activo = False
    class Meta:
        """Metadatos"""
        db_table = 'estado_clase'
        verbose_name = 'Estado de una clase'
        verbose_name_plural = 'Estados de una clase'

@aplicar_docstring_como_comentario_de_tabla
class TipoContrato(models.Model):
    """Tipos posibles de contrato"""
    id_tipo_contrato = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=MAXLEN_NOMBRE)
    fecha_alta = models.DateField(default=timezone.now)
    fecha_baja = models.DateField(blank=True, null=True)
    activo = models.BooleanField(default=True)
    comentarios = models.TextField(blank=True, null=True)
    def clean(self):
        """Validación de coherencia interna"""
        if self.fecha_baja and self.activo:
            raise ValidationError(f"TipoContrato {self.id_tipo_contrato}: Activo y con fecha de baja !!!")
        if self.fecha_baja and self.fecha_baja < timezone.now().date():
            self.activo = False
    class Meta:
        """Metadatos"""
        db_table = 'tipo_contrato'
        verbose_name = 'Tipo de contrato'
        verbose_name_plural = 'Tipos de contrato'

@aplicar_docstring_como_comentario_de_tabla
class TipoCurso(models.Model):
    """Tipos posibles de curso"""
    id_tipo_curso = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=MAXLEN_NOMBRE)
    fecha_alta = models.DateField(default=timezone.now)
    fecha_baja = models.DateField(blank=True, null=True)
    activo = models.BooleanField(default=True)
    comentarios = models.TextField(blank=True, null=True)
    def clean(self):
        """Validación de coherencia interna"""
        if self.fecha_baja and self.activo:
            raise ValidationError(f"TipoCurso {self.id_tipo_curso}: Activo y con fecha de baja !!!")
        if self.fecha_baja and self.fecha_baja < timezone.now().date():
            self.activo = False
    class Meta:
        """Metadatos"""
        db_table = 'tipo_curso'
        verbose_name = 'Tipo de curso'
        verbose_name_plural = 'Tipos de curso'

@aplicar_docstring_como_comentario_de_tabla
class TipoDependencia(models.Model):
    """Tipos posibles de dependencia"""
    id_tipo_dependencia = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=MAXLEN_NOMBRE)
    fecha_alta = models.DateField(default=timezone.now)
    fecha_baja = models.DateField(blank=True, null=True)
    activo = models.BooleanField(default=True)
    comentarios = models.TextField(blank=True, null=True)
    def clean(self):
        """Validación de coherencia interna"""
        if self.fecha_baja and self.activo:
            raise ValidationError(f"TipoDependencia {self.id_tipo_dependencia}: Activo y con fecha de baja !!!")
        if self.fecha_baja and self.fecha_baja < timezone.now().date():
            self.activo = False
    class Meta:
        """Metadatos"""
        db_table = 'tipo_dependencia'
        verbose_name = 'Tipo de dependencia'
        verbose_name_plural = 'Tipos de dependencia'

@aplicar_docstring_como_comentario_de_tabla
class TipoMensaje(models.Model):
    """Tipos posibles de mensaje"""
    id_tipo_mensaje = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=MAXLEN_NOMBRE)
    fecha_alta = models.DateField(default=timezone.now)
    fecha_baja = models.DateField(blank=True, null=True)
    activo = models.BooleanField(default=True)
    comentarios = models.TextField(blank=True, null=True)
    def clean(self):
        """Validación de coherencia interna"""
        if self.fecha_baja and self.activo:
            raise ValidationError(f"TipoMensaje {self.id_tipo_mensaje}: Activo y con fecha de baja !!!")
        if self.fecha_baja and self.fecha_baja < timezone.now().date():
            self.activo = False
    class Meta:
        """Metadatos"""
        db_table = 'tipo_mensaje'
        verbose_name = 'Tipo de mensaje'
        verbose_name_plural = 'Tipos de mensaje'

@aplicar_docstring_como_comentario_de_tabla
class EstadoEnvio(models.Model):
    """Estados posibles de un envío"""
    id_estado_envio = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=MAXLEN_NOMBRE)
    fecha_alta = models.DateField(default=timezone.now)
    fecha_baja = models.DateField(blank=True, null=True)
    activo = models.BooleanField(default=True)
    comentarios = models.TextField(blank=True, null=True)
    def clean(self):
        """Validación de coherencia interna"""
        if self.fecha_baja and self.activo:
            raise ValidationError(f"EstadoEnvio {self.id_estado_envio}: Activo y con fecha de baja !!!")
        if self.fecha_baja and self.fecha_baja < timezone.now().date():
            self.activo = False
    class Meta:
        """Metadatos"""
        db_table = 'estado_envio'
        verbose_name = 'Estado de un envío'
        verbose_name_plural = 'Estados de un envío'

@aplicar_docstring_como_comentario_de_tabla
class TipoDiasemanal(models.Model):
    """Días de la semana"""
    id_tipo_diasemanal = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=MAXLEN_NOMBRE)
    fecha_alta = models.DateField(default=timezone.now)
    fecha_baja = models.DateField(blank=True, null=True)
    activo = models.BooleanField(default=True)
    comentarios = models.TextField(blank=True, null=True)
    def clean(self):
        """Validación de coherencia interna"""
        if self.fecha_baja and self.activo:
            raise ValidationError(f"TipoDiasemanal {self.id_tipo_diasemanal}: Activo y con fecha de baja !!!")
        if self.fecha_baja and self.fecha_baja < timezone.now().date():
            self.activo = False
    def __str__(self):
        return str(self.nombre)
    class Meta:
        """Metadatos"""
        db_table = 'tipo_diasemanal'
        verbose_name = 'Día de la semana'
        verbose_name_plural = 'Días de la semana'

@aplicar_docstring_como_comentario_de_tabla
class EstadoInscripcion(models.Model):
    """Estados posibles de una inscripción"""
    id_estado_inscripcion = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=MAXLEN_NOMBRE)
    fecha_alta = models.DateField(default=timezone.now)
    fecha_baja = models.DateField(blank=True, null=True)
    activo = models.BooleanField(default=True)
    comentarios = models.TextField(blank=True, null=True)
    def clean(self):
        """Validación de coherencia interna"""
        if self.fecha_baja and self.activo:
            raise ValidationError(f"EstadoInscripcion {self.id_estado_inscripcion}: Activo y con fecha de baja !!!")
        if self.fecha_baja and self.fecha_baja < timezone.now().date():
            self.activo = False
    class Meta:
        """Metadatos"""
        db_table = 'estado_inscripcion'
        verbose_name = 'Estado de una inscripción'
        verbose_name_plural = 'Estados de una inscripción'

@aplicar_docstring_como_comentario_de_tabla
class TipoLateralidad(models.Model):
    """Tipos posibles de lateralidad"""
    id_tipo_lateralidad = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=MAXLEN_NOMBRE)
    fecha_alta = models.DateField(default=timezone.now)
    fecha_baja = models.DateField(blank=True, null=True)
    activo = models.BooleanField(default=True)
    comentarios = models.TextField(blank=True, null=True)
    def clean(self):
        """Validación de coherencia interna"""
        if self.fecha_baja and self.activo:
            raise ValidationError(f"TipoLateralidad {self.id_tipo_lateralidad}: Activo y con fecha de baja !!!")
        if self.fecha_baja and self.fecha_baja < timezone.now().date():
            self.activo = False
    def __str__(self):
        return str(self.nombre)
    class Meta:
        """Metadatos"""
        db_table = 'tipo_lateralidad'
        verbose_name = 'Tipo de lateralidad'
        verbose_name_plural = 'Tipos de lateralidad'

@aplicar_docstring_como_comentario_de_tabla
class TipoDirectivo(models.Model):
    """Tipos posibles de directivo"""
    id_tipo_directivo = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=MAXLEN_NOMBRE)
    fecha_alta = models.DateField(default=timezone.now)
    fecha_baja = models.DateField(blank=True, null=True)
    activo = models.BooleanField(default=True)
    comentarios = models.TextField(blank=True, null=True)
    def clean(self):
        """Validación de coherencia interna"""
        if self.fecha_baja and self.activo:
            raise ValidationError(f"TipoDirectivo {self.id_tipo_directivo}: Activo y con fecha de baja !!!")
        if self.fecha_baja and self.fecha_baja < timezone.now().date():
            self.activo = False
    def __str__(self):
        return str(self.nombre)
    class Meta:
        """Metadatos"""
        db_table = 'tipo_directivo'
        verbose_name = 'Tipo de directivo'
        verbose_name_plural = 'Tipos de directivo'

@aplicar_docstring_como_comentario_de_tabla
class TipoMembresia(models.Model):
    """Tipos posibles de membresía"""
    id_tipo_membresia = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=MAXLEN_NOMBRE)
    fecha_alta = models.DateField(default=timezone.now)
    fecha_baja = models.DateField(blank=True, null=True)
    activo = models.BooleanField(default=True)
    comentarios = models.TextField(blank=True, null=True)
    def clean(self):
        """Validación de coherencia interna"""
        if self.fecha_baja and self.activo:
            raise ValidationError(f"TipoMembresia {self.id_tipo_membresia}: Activo y con fecha de baja !!!")
        if self.fecha_baja and self.fecha_baja < timezone.now().date():
            self.activo = False
    def __str__(self):
        return str(self.nombre)
    class Meta:
        """Metadatos"""
        db_table = 'tipo_membresia'
        verbose_name = 'Tipo de membresía'
        verbose_name_plural = 'Tipos de membresía'

@aplicar_docstring_como_comentario_de_tabla
class EstadoPartido(models.Model):
    """Estados posibles de un partido"""
    id_estado_partido = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=MAXLEN_NOMBRE)
    fecha_alta = models.DateField(default=timezone.now)
    fecha_baja = models.DateField(blank=True, null=True)
    activo = models.BooleanField(default=True)
    comentarios = models.TextField(blank=True, null=True)
    def clean(self):
        """Validación de coherencia interna"""
        if self.fecha_baja and self.activo:
            raise ValidationError(f"EstadoPartido {self.id_estado_partido}: Activo y con fecha de baja !!!")
        if self.fecha_baja and self.fecha_baja < timezone.now().date():
            self.activo = False
    class Meta:
        """Metadatos"""
        db_table = 'estado_partido'
        verbose_name = 'Estado de un partido'
        verbose_name_plural = 'Estados de un partido'

@aplicar_docstring_como_comentario_de_tabla
class TipoIdentificacion(models.Model):
    """Tipos posibles de identificación"""
    id_tipo_identificacion = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=MAXLEN_NOMBRE)
    fecha_alta = models.DateField(default=timezone.now)
    fecha_baja = models.DateField(blank=True, null=True)
    activo = models.BooleanField(default=True)
    comentarios = models.TextField(blank=True, null=True)
    def clean(self):
        """Validación de coherencia interna"""
        if self.fecha_baja and self.activo:
            raise ValidationError(f"TipoIdentificacion {self.id_tipo_identificacion}: Activo y con fecha de baja !!!")
        if self.fecha_baja and self.fecha_baja < timezone.now().date():
            self.activo = False
    def __str__(self):
        return str(self.nombre)
    class Meta:
        """Metadatos"""
        db_table = 'tipo_identificacion'
        verbose_name = 'Tipo de identificación'
        verbose_name_plural = 'Tipos de identificación'

@aplicar_docstring_como_comentario_de_tabla
class TipoPista(models.Model):
    """Tipos posibles de pista"""
    id_tipo_pista = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=MAXLEN_NOMBRE)
    fecha_alta = models.DateField(default=timezone.now)
    fecha_baja = models.DateField(blank=True, null=True)
    activo = models.BooleanField(default=True)
    comentarios = models.TextField(blank=True, null=True)
    def clean(self):
        """Validación de coherencia interna"""
        if self.fecha_baja and self.activo:
            raise ValidationError(f"TipoPista {self.id_tipo_pista}: Activo y con fecha de baja !!!")
        if self.fecha_baja and self.fecha_baja < timezone.now().date():
            self.activo = False
    def __str__(self):
        return str(self.nombre)
    class Meta:
        """Metadatos"""
        db_table = 'tipo_pista'
        verbose_name = 'Tipo de pista'
        verbose_name_plural = 'Tipos de pista'

@aplicar_docstring_como_comentario_de_tabla
class TipoSuelo(models.Model):
    """Tipos posibles de suelo"""
    id_tipo_suelo = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=MAXLEN_NOMBRE)
    fecha_alta = models.DateField(default=timezone.now)
    fecha_baja = models.DateField(blank=True, null=True)
    activo = models.BooleanField(default=True)
    comentarios = models.TextField(blank=True, null=True)
    def clean(self):
        """Validación de coherencia interna"""
        if self.fecha_baja and self.activo:
            raise ValidationError(f"TipoSuelo {self.id_tipo_suelo}: Activo y con fecha de baja !!!")
        if self.fecha_baja and self.fecha_baja < timezone.now().date():
            self.activo = False
    def __str__(self):
        return str(self.nombre)
    class Meta:
        """Metadatos"""
        db_table = 'tipo_suelo'
        verbose_name = 'Tipo de suelo'
        verbose_name_plural = 'Tipos de suelo'

@aplicar_docstring_como_comentario_de_tabla
class TipoTitulacion(models.Model):
    """Tipos posibles de titulación"""
    id_tipo_titulacion = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=MAXLEN_NOMBRE)
    fecha_alta = models.DateField(default=timezone.now)
    fecha_baja = models.DateField(blank=True, null=True)
    activo = models.BooleanField(default=True)
    comentarios = models.TextField(blank=True, null=True)
    def clean(self):
        """Validación de coherencia interna"""
        if self.fecha_baja and self.activo:
            raise ValidationError(f"TipoTitulacion {self.id_tipo_titulacion}: Activo y con fecha de baja !!!")
        if self.fecha_baja and self.fecha_baja < timezone.now().date():
            self.activo = False
    def __str__(self):
        return str(self.nombre)
    class Meta:
        """Metadatos"""
        db_table = 'tipo_titulacion'
        verbose_name = 'Tipo de titulación'
        verbose_name_plural = 'Tipos de titulación'

@aplicar_docstring_como_comentario_de_tabla
class TipoPosesion(models.Model):
    """Tipos posibles de posesión"""
    id_tipo_posesion = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=MAXLEN_NOMBRE)
    fecha_alta = models.DateField(default=timezone.now)
    fecha_baja = models.DateField(blank=True, null=True)
    activo = models.BooleanField(default=True)
    comentarios = models.TextField(blank=True, null=True)
    def clean(self):
        """Validación de coherencia interna"""
        if self.fecha_baja and self.activo:
            raise ValidationError(f"TipoPosesion {self.id_tipo_posesion}: Activo y con fecha de baja !!!")
        if self.fecha_baja and self.fecha_baja < timezone.now().date():
            self.activo = False
    def __str__(self):
        return str(self.nombre)
    class Meta:
        """Metadatos"""
        db_table = 'tipo_posesion'
        verbose_name = 'Tipo de posesión'
        verbose_name_plural = 'Tipos de posesión'

@aplicar_docstring_como_comentario_de_tabla
class TipoCompeticion(models.Model):
    """Tipos posibles de competición"""
    id_tipo_competicion = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=MAXLEN_NOMBRE)
    fecha_alta = models.DateField(default=timezone.now)
    fecha_baja = models.DateField(blank=True, null=True)
    activo = models.BooleanField(default=True)
    comentarios = models.TextField(blank=True, null=True)
    def clean(self):
        """Validación de coherencia interna"""
        if self.fecha_baja and self.activo:
            raise ValidationError(f"TipoCompeticion {self.id_tipo_competicion}: Activo y con fecha de baja !!!")
        if self.fecha_baja and self.fecha_baja < timezone.now().date():
            self.activo = False
    def __str__(self):
        return str(self.nombre)
    class Meta:
        """Metadatos"""
        db_table = 'tipo_competicion'
        verbose_name = 'Tipo de competición'
        verbose_name_plural = 'Tipos de competición'

@aplicar_docstring_como_comentario_de_tabla
class Operario(models.Model):
    """Los operarios son personas que poseen una capacitación"""
    id_operario = models.AutoField(primary_key=True)
    id_persona = models.ForeignKey('Persona', models.RESTRICT, db_column='id_persona')
    token_qr = models.CharField(unique=True, max_length=MAXLEN_TOKENQR, default=nuevo_token_qr)
    id_tipo_capacitacion = models.ForeignKey('TipoCapacitacion', models.RESTRICT, db_column='id_tipo_capacitacion')
    fecha_alta = models.DateField(default=timezone.now)
    fecha_baja = models.DateField(blank=True, null=True)
    activo = models.BooleanField(default=True)
    comentarios = models.TextField(blank=True, null=True)
    class Meta:
        """Metadatos"""
        db_table = 'operario'
        verbose_name = 'Operario'
        verbose_name_plural = 'Operarios'

@aplicar_docstring_como_comentario_de_tabla
class Empleo(models.Model):
    """Contrato: Tabla de combinación N:M operario-instalación"""
    id_empleo = models.AutoField(primary_key=True)
    id_operario = models.ForeignKey('Operario', models.RESTRICT, db_column='id_operario')
    id_instalacion = models.ForeignKey('Instalacion', models.RESTRICT, db_column='id_instalacion')
    id_tipo_empleo = models.ForeignKey('TipoEmpleo', models.RESTRICT, db_column='id_tipo_empleo')
    fecha_alta = models.DateField(default=timezone.now)
    fecha_baja = models.DateField(blank=True, null=True)
    activo = models.BooleanField(default=True)
    comentarios = models.TextField(blank=True, null=True)
    class Meta:
        """Metadatos"""
        db_table = 'empleo'
        verbose_name = 'Empleo [operario-instalación]'
        verbose_name_plural = 'Empleos [operario-instalación]'

@aplicar_docstring_como_comentario_de_tabla
class TipoEmpleo(models.Model):
    """Tipos posibles de empleo"""
    id_tipo_empleo = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=MAXLEN_NOMBRE)
    fecha_alta = models.DateField(default=timezone.now)
    fecha_baja = models.DateField(blank=True, null=True)
    activo = models.BooleanField(default=True)
    comentarios = models.TextField(blank=True, null=True)
    def clean(self):
        """Validación de coherencia interna"""
        if self.fecha_baja and self.activo:
            raise ValidationError(f"TipoEmpleo {self.id_tipo_empleo}: Activo y con fecha de baja !!!")
        if self.fecha_baja and self.fecha_baja < timezone.now().date():
            self.activo = False
    class Meta:
        """Metadatos"""
        db_table = 'tipo_empleo'
        verbose_name = 'Tipo de empleo'
        verbose_name_plural = 'Tipos de empleo'

@aplicar_docstring_como_comentario_de_tabla
class TipoCapacitacion(models.Model):
    """Tipos posibles de capacitación"""
    id_tipo_capacitacion = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=MAXLEN_NOMBRE)
    fecha_alta = models.DateField(default=timezone.now)
    fecha_baja = models.DateField(blank=True, null=True)
    activo = models.BooleanField(default=True)
    comentarios = models.TextField(blank=True, null=True)
    def clean(self):
        """Validación de coherencia interna"""
        if self.fecha_baja and self.activo:
            raise ValidationError(f"TipoCapacitacion {self.id_tipo_capacitacion}: Activo y con fecha de baja !!!")
        if self.fecha_baja and self.fecha_baja < timezone.now().date():
            self.activo = False
    def __str__(self):
        return str(self.nombre)
    class Meta:
        """Metadatos"""
        db_table = 'tipo_capacitacion'
        verbose_name = 'Tipo de capacitación'
        verbose_name_plural = 'Tipos de capacitación'
