# # =====================================================
# # webMuebles/models.py - APLICACIÓN PRINCIPAL
# # Configuraciones del sitio y modelos base para herencia
# # =====================================================

# from django.db import models
# from django.core.validators import RegexValidator, URLValidator
# from django.utils import timezone
# from django.core.exceptions import ValidationError
# from decimal import Decimal

# # =====================================================
# # MODELOS ABSTRACTOS (Para herencia en otras apps)
# # =====================================================

# class TimestampMixin(models.Model):
#     """
#     Mixin abstracto que proporciona campos de timestamp
#     Para usar en cualquier modelo que necesite auditoría básica
#     """
#     fecha_creacion = models.DateTimeField(
#         default=timezone.now,
#         verbose_name="Fecha de Creación",
#         help_text="Fecha y hora de creación del registro"
#     )
#     fecha_actualizacion = models.DateTimeField(
#         auto_now=True,
#         verbose_name="Fecha de Actualización",
#         help_text="Fecha y hora de la última modificación"
#     )
    
#     class Meta:
#         abstract = True

# class EstadoActivoMixin(models.Model):
#     """
#     Mixin abstracto para manejo de estado activo/inactivo
#     """
#     ESTADO_CHOICES = [
#         ('activo', 'Activo'),
#         ('inactivo', 'Inactivo'),
#     ]
    
#     activo = models.BooleanField(
#         default=True,
#         verbose_name="Activo",
#         help_text="Indica si el registro está activo en el sistema"
#     )
#     estado = models.CharField(
#         max_length=10,
#         choices=ESTADO_CHOICES,
#         default='activo',
#         verbose_name="Estado",
#         db_index=True
#     )
    
#     class Meta:
#         abstract = True
    
#     def activar(self):
#         """Activa el registro"""
#         self.activo = True
#         self.estado = 'activo'
#         self.save(update_fields=['activo', 'estado'])
    
#     def desactivar(self):
#         """Desactiva el registro"""
#         self.activo = False
#         self.estado = 'inactivo'
#         self.save(update_fields=['activo', 'estado'])

# class BaseModel(TimestampMixin, EstadoActivoMixin):
#     """
#     Modelo base que combina timestamp y estado
#     Ideal para la mayoría de modelos del sistema
#     """
#     class Meta:
#         abstract = True
    
#     def clean(self):
#         """Validación personalizada base"""
#         super().clean()
#         # Sincronizar activo y estado
#         if self.activo and self.estado == 'inactivo':
#             self.estado = 'activo'
#         elif not self.activo and self.estado == 'activo':
#             self.activo = False

# # =====================================================
# # CONFIGURACIONES DEL SITIO WEB
# # =====================================================

# class ConfiguracionSitio(BaseModel):
#     """
#     Configuración general del sitio web
#     Solo puede existir un registro activo
#     """
#     # Información de la empresa
#     nombre_empresa = models.CharField(
#         max_length=100,
#         default="Muebles Barguay",
#         verbose_name="Nombre de la Empresa",
#         help_text="Nombre oficial de la empresa"
#     )
    
#     slogan = models.CharField(
#         max_length=200,
#         blank=True,
#         verbose_name="Slogan",
#         help_text="Frase representativa de la empresa"
#     )
    
#     descripcion_empresa = models.TextField(
#         blank=True,
#         verbose_name="Descripción de la Empresa",
#         help_text="Descripción detallada para el sitio web"
#     )
    
#     # Datos de contacto
#     phone_validator = RegexValidator(
#         regex=r'^\+?56?[0-9]{8,9}$',
#         message="Debe ser un número de teléfono chileno válido."
#     )
    
#     telefono_principal = models.CharField(
#         max_length=20,
#         validators=[phone_validator],
#         verbose_name="Teléfono Principal",
#         help_text="Teléfono principal de contacto"
#     )
    
#     telefono_whatsapp = models.CharField(
#         max_length=20,
#         validators=[phone_validator],
#         blank=True,
#         verbose_name="WhatsApp",
#         help_text="Número de WhatsApp para contacto"
#     )
    
#     email_principal = models.EmailField(
#         verbose_name="Email Principal",
#         help_text="Email principal de contacto"
#     )
    
#     email_cotizaciones = models.EmailField(
#         blank=True,
#         verbose_name="Email Cotizaciones",
#         help_text="Email específico para recibir cotizaciones"
#     )
    
#     # Ubicación
#     direccion_completa = models.TextField(
#         verbose_name="Dirección Completa",
#         help_text="Dirección física de la empresa"
#     )
    
#     ciudad = models.CharField(
#         max_length=100,
#         default="Santiago",
#         verbose_name="Ciudad"
#     )
    
#     region = models.CharField(
#         max_length=100,
#         default="Región Metropolitana",
#         verbose_name="Región"
#     )
    
#     codigo_postal = models.CharField(
#         max_length=20,
#         blank=True,
#         verbose_name="Código Postal"
#     )
    
#     # Coordenadas para mapa
#     latitud = models.DecimalField(
#         max_digits=10,
#         decimal_places=8,
#         blank=True,
#         null=True,
#         verbose_name="Latitud",
#         help_text="Coordenada de latitud para Google Maps"
#     )
    
#     longitud = models.DecimalField(
#         max_digits=11,
#         decimal_places=8,
#         blank=True,
#         null=True,
#         verbose_name="Longitud",
#         help_text="Coordenada de longitud para Google Maps"
#     )
    
#     # Redes sociales
#     url_facebook = models.URLField(
#         blank=True,
#         verbose_name="Facebook URL",
#         help_text="URL completa del perfil de Facebook"
#     )
    
#     url_instagram = models.URLField(
#         blank=True,
#         verbose_name="Instagram URL",
#         help_text="URL completa del perfil de Instagram"
#     )
    
#     url_linkedin = models.URLField(
#         blank=True,
#         verbose_name="LinkedIn URL",
#         help_text="URL completa del perfil de LinkedIn"
#     )
    
#     # Horarios de atención
#     horario_atencion = models.TextField(
#         blank=True,
#         verbose_name="Horario de Atención",
#         help_text="Horarios de atención al público",
#         default="Lunes a Viernes: 9:00 - 18:00\nSábados: 9:00 - 13:00"
#     )
    
#     # Configuraciones del sitio web
#     mensaje_bienvenida = models.TextField(
#         verbose_name="Mensaje de Bienvenida",
#         help_text="Mensaje que aparece en la página principal",
#         default="Bienvenido a Muebles Barguay, expertos en muebles a medida"
#     )
    
#     mensaje_cotizacion = models.TextField(
#         verbose_name="Mensaje Formulario Cotización",
#         help_text="Mensaje que aparece en el formulario de cotización",
#         default="Obtén tu cotización personalizada en minutos"
#     )
    
#     tiempo_respuesta_cotizacion = models.PositiveIntegerField(
#         default=2,
#         verbose_name="Tiempo de Respuesta (Horas)",
#         help_text="Tiempo promedio de respuesta para cotizaciones"
#     )
    
#     # Logo y favicon
#     logo = models.ImageField(
#         upload_to='configuracion/logos/',
#         blank=True,
#         verbose_name="Logo Principal",
#         help_text="Logo principal de la empresa (recomendado: PNG transparente)"
#     )
    
#     favicon = models.ImageField(
#         upload_to='configuracion/favicon/',
#         blank=True,
#         verbose_name="Favicon",
#         help_text="Icono pequeño para el navegador (16x16 o 32x32 px)"
#     )
    
#     # Configuraciones de negocio
#     porcentaje_adelanto_defecto = models.DecimalField(
#         max_digits=5,
#         decimal_places=2,
#         default=50.00,
#         verbose_name="% Adelanto por Defecto",
#         help_text="Porcentaje de adelanto predeterminado para pedidos"
#     )
    
#     dias_vencimiento_cotizacion = models.PositiveIntegerField(
#         default=30,
#         verbose_name="Días Vencimiento Cotización",
#         help_text="Días de validez por defecto para cotizaciones"
#     )
    
#     # SEO
#     meta_description = models.TextField(
#         max_length=160,
#         blank=True,
#         verbose_name="Meta Description",
#         help_text="Descripción para buscadores (máx. 160 caracteres)"
#     )
    
#     meta_keywords = models.TextField(
#         blank=True,
#         verbose_name="Meta Keywords",
#         help_text="Palabras clave separadas por comas"
#     )
    
#     # Control de versión
#     version_sitio = models.CharField(
#         max_length=20,
#         default="1.0.0",
#         verbose_name="Versión del Sitio"
#     )
    
#     class Meta:
#         db_table = 'configuracion_sitio'
#         verbose_name = "Configuración del Sitio"
#         verbose_name_plural = "Configuración del Sitio"
    
#     def clean(self):
#         """Validaciones personalizadas"""
#         super().clean()
        
#         # Validar que solo haya una configuración activa
#         if self.activo:
#             activas = ConfiguracionSitio.objects.filter(activo=True).exclude(pk=self.pk)
#             if activas.exists():
#                 raise ValidationError("Solo puede existir una configuración activa.")
        
#         # Validar coordenadas
#         if self.latitud and not (-90 <= self.latitud <= 90):
#             raise ValidationError("La latitud debe estar entre -90 y 90 grados.")
        
#         if self.longitud and not (-180 <= self.longitud <= 180):
#             raise ValidationError("La longitud debe estar entre -180 y 180 grados.")
        
#         # Validar porcentaje de adelanto
#         if not (0 <= self.porcentaje_adelanto_defecto <= 100):
#             raise ValidationError("El porcentaje de adelanto debe estar entre 0 y 100.")
    
#     def save(self, *args, **kwargs):
#         self.clean()
#         super().save(*args, **kwargs)
    
#     def __str__(self):
#         return f"Configuración - {self.nombre_empresa}"
    
#     @classmethod
#     def get_configuracion_activa(cls):
#         """Obtiene la configuración activa del sitio"""
#         try:
#             return cls.objects.filter(activo=True).first()
#         except cls.DoesNotExist:
#             return None
    
#     @property
#     def telefono_whatsapp_formateado(self):
#         """Devuelve el WhatsApp en formato de enlace"""
#         if self.telefono_whatsapp:
#             # Remover espacios y caracteres especiales
#             numero = self.telefono_whatsapp.replace(' ', '').replace('+', '').replace('-', '')
#             return f"https://wa.me/{numero}"
#         return None
    
#     @property
#     def coordenadas_maps(self):
#         """Devuelve las coordenadas para Google Maps"""
#         if self.latitud and self.longitud:
#             return f"{self.latitud},{self.longitud}"
#         return None

# # =====================================================
# # CONFIGURACIONES ESPECÍFICAS (Clave-Valor)
# # =====================================================

# class ConfiguracionEspecifica(BaseModel):
#     """
#     Configuraciones específicas del sistema en formato clave-valor
#     Para configuraciones técnicas o temporales
#     """
#     TIPO_CHOICES = [
#         ('texto', 'Texto'),
#         ('numero', 'Número'),
#         ('booleano', 'Verdadero/Falso'),
#         ('json', 'JSON'),
#         ('email', 'Email'),
#         ('url', 'URL'),
#     ]
    
#     clave = models.CharField(
#         max_length=100,
#         unique=True,
#         verbose_name="Clave",
#         help_text="Identificador único de la configuración"
#     )
    
#     valor = models.TextField(
#         verbose_name="Valor",
#         help_text="Valor de la configuración"
#     )
    
#     tipo_dato = models.CharField(
#         max_length=15,
#         choices=TIPO_CHOICES,
#         default='texto',
#         verbose_name="Tipo de Dato",
#         help_text="Tipo de dato almacenado"
#     )
    
#     descripcion = models.TextField(
#         blank=True,
#         verbose_name="Descripción",
#         help_text="Descripción de para qué sirve esta configuración"
#     )
    
#     solo_lectura = models.BooleanField(
#         default=False,
#         verbose_name="Solo Lectura",
#         help_text="Si está marcado, no se puede modificar desde el admin"
#     )
    
#     categoria = models.CharField(
#         max_length=50,
#         blank=True,
#         verbose_name="Categoría",
#         help_text="Categoría para agrupar configuraciones",
#         db_index=True
#     )
    
#     class Meta:
#         db_table = 'configuraciones_especificas'
#         verbose_name = "Configuración Específica"
#         verbose_name_plural = "Configuraciones Específicas"
#         ordering = ['categoria', 'clave']
#         indexes = [
#             models.Index(fields=['clave']),
#             models.Index(fields=['categoria']),
#             models.Index(fields=['activo']),
#         ]
    
#     def __str__(self):
#         return f"{self.clave} = {self.valor[:50]}..."
    
#     def clean(self):
#         """Validar el valor según el tipo de dato"""
#         super().clean()
        
#         if self.tipo_dato == 'numero':
#             try:
#                 float(self.valor)
#             except ValueError:
#                 raise ValidationError("El valor debe ser un número válido.")
        
#         elif self.tipo_dato == 'booleano':
#             if self.valor.lower() not in ['true', 'false', '1', '0', 'si', 'no']:
#                 raise ValidationError("El valor debe ser verdadero o falso.")
        
#         elif self.tipo_dato == 'email':
#             from django.core.validators import validate_email
#             try:
#                 validate_email(self.valor)
#             except ValidationError:
#                 raise ValidationError("El valor debe ser un email válido.")
        
#         elif self.tipo_dato == 'url':
#             validator = URLValidator()
#             try:
#                 validator(self.valor)
#             except ValidationError:
#                 raise ValidationError("El valor debe ser una URL válida.")
        
#         elif self.tipo_dato == 'json':
#             import json
#             try:
#                 json.loads(self.valor)
#             except json.JSONDecodeError:
#                 raise ValidationError("El valor debe ser un JSON válido.")
    
#     def get_valor_typed(self):
#         """Devuelve el valor convertido al tipo correcto"""
#         if self.tipo_dato == 'numero':
#             try:
#                 if '.' in self.valor:
#                     return float(self.valor)
#                 return int(self.valor)
#             except ValueError:
#                 return 0
        
#         elif self.tipo_dato == 'booleano':
#             return self.valor.lower() in ['true', '1', 'si']
        
#         elif self.tipo_dato == 'json':
#             import json
#             try:
#                 return json.loads(self.valor)
#             except json.JSONDecodeError:
#                 return {}
        
#         return self.valor
    
#     @classmethod
#     def get_config(cls, clave, default=None):
#         """Obtiene una configuración por su clave"""
#         try:
#             config = cls.objects.get(clave=clave, activo=True)
#             return config.get_valor_typed()
#         except cls.DoesNotExist:
#             return default
    
#     @classmethod
#     def set_config(cls, clave, valor, tipo_dato='texto', descripcion=''):
#         """Establece o actualiza una configuración"""
#         config, created = cls.objects.get_or_create(
#             clave=clave,
#             defaults={
#                 'valor': str(valor),
#                 'tipo_dato': tipo_dato,
#                 'descripcion': descripcion,
#                 'activo': True
#             }
#         )
#         if not created:
#             config.valor = str(valor)
#             config.tipo_dato = tipo_dato
#             if descripcion:
#                 config.descripcion = descripcion
#             config.save()
#         return config

# # =====================================================
# # LOGS DE ACTIVIDAD DEL SISTEMA
# # =====================================================

# class LogActividad(models.Model):
#     """
#     Registro de actividades importantes del sistema
#     Para auditoría y seguimiento
#     """
#     NIVEL_CHOICES = [
#         ('debug', 'Debug'),
#         ('info', 'Información'),
#         ('warning', 'Advertencia'),
#         ('error', 'Error'),
#         ('critical', 'Crítico'),
#     ]
    
#     CATEGORIA_CHOICES = [
#         ('sistema', 'Sistema'),
#         ('usuario', 'Usuario'),
#         ('cotizacion', 'Cotización'),
#         ('pedido', 'Pedido'),
#         ('stock', 'Stock'),
#         ('compra', 'Compra'),
#         ('email', 'Email'),
#         ('api', 'API'),
#     ]
    
#     # Información del log
#     nivel = models.CharField(
#         max_length=10,
#         choices=NIVEL_CHOICES,
#         default='info',
#         db_index=True
#     )
    
#     categoria = models.CharField(
#         max_length=20,
#         choices=CATEGORIA_CHOICES,
#         default='sistema',
#         db_index=True
#     )
    
#     mensaje = models.TextField(
#         verbose_name="Mensaje",
#         help_text="Descripción de la actividad"
#     )
    
#     datos_adicionales = models.JSONField(
#         default=dict,
#         blank=True,
#         verbose_name="Datos Adicionales",
#         help_text="Información adicional en formato JSON"
#     )
    
#     # Referencias
#     usuario = models.ForeignKey(
#         'administracion.Administrador',
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True,
#         verbose_name="Usuario",
#         help_text="Usuario que realizó la acción"
#     )
    
#     direccion_ip = models.GenericIPAddressField(
#         null=True,
#         blank=True,
#         verbose_name="Dirección IP"
#     )
    
#     user_agent = models.TextField(
#         blank=True,
#         verbose_name="User Agent",
#         help_text="Información del navegador/cliente"
#     )
    
#     # Metadatos
#     fecha_creacion = models.DateTimeField(
#         default=timezone.now,
#         db_index=True
#     )
    
#     class Meta:
#         db_table = 'log_actividad'
#         verbose_name = "Log de Actividad"
#         verbose_name_plural = "Logs de Actividad"
#         ordering = ['-fecha_creacion']
#         indexes = [
#             models.Index(fields=['-fecha_creacion']),
#             models.Index(fields=['nivel', 'categoria']),
#             models.Index(fields=['usuario']),
#         ]
    
#     def __str__(self):
#         return f"[{self.get_nivel_display()}] {self.categoria} - {self.mensaje[:50]}..."
    
#     @classmethod
#     def log(cls, mensaje, nivel='info', categoria='sistema', usuario=None, datos=None, request=None):
#         """Método conveniente para crear logs"""
#         datos_adicionales = datos or {}
        
#         direccion_ip = None
#         user_agent = ""
        
#         if request:
#             direccion_ip = cls.get_client_ip(request)
#             user_agent = request.META.get('HTTP_USER_AGENT', '')
        
#         return cls.objects.create(
#             nivel=nivel,
#             categoria=categoria,
#             mensaje=mensaje,
#             datos_adicionales=datos_adicionales,
#             usuario=usuario,
#             direccion_ip=direccion_ip,
#             user_agent=user_agent
#         )
    
#     @staticmethod
#     def get_client_ip(request):
#         """Obtiene la IP real del cliente"""
#         x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
#         if x_forwarded_for:
#             ip = x_forwarded_for.split(',')[0]
#         else:
#             ip = request.META.get('REMOTE_ADDR')
#         return ip

# # =====================================================
# # MANAGER PERSONALIZADO PARA CONFIGURACIÓN
# # =====================================================

# class ConfiguracionSitioManager(models.Manager):
#     """Manager personalizado para ConfiguracionSitio"""
    
#     def get_activa(self):
#         """Obtiene la configuración activa"""
#         return self.filter(activo=True).first()
    
#     def get_o_crear_defecto(self):
#         """Obtiene la configuración activa o crea una por defecto"""
#         config = self.get_activa()
#         if not config:
#             config = self.create(
#                 nombre_empresa="Muebles Barguay",
#                 telefono_principal="+56912345678",
#                 email_principal="contacto@mueblesbarguay.cl",
#                 direccion_completa="Santiago, Chile",
#                 activo=True
#             )
#         return config

# # Asignar el manager personalizado
# ConfiguracionSitio.objects = ConfiguracionSitioManager()

# # =====================================================
# # SIGNALS PARA AUTOMATIZACIÓN
# # =====================================================

# from django.db.models.signals import post_save, post_delete
# from django.dispatch import receiver

# @receiver(post_save, sender=ConfiguracionSitio)
# def configuracion_sitio_post_save(sender, instance, created, **kwargs):
#     """Signal ejecutado después de guardar configuración"""
#     if created:
#         LogActividad.log(
#             f"Nueva configuración del sitio creada: {instance.nombre_empresa}",
#             nivel='info',
#             categoria='sistema',
#             datos={'configuracion_id': instance.id}
#         )
#     else:
#         LogActividad.log(
#             f"Configuración del sitio actualizada: {instance.nombre_empresa}",
#             nivel='info',
#             categoria='sistema',
#             datos={'configuracion_id': instance.id}
#         )