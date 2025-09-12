# from django.contrib.auth.models import AbstractUser
# from django.db import models
# from django.utils import timezone

# class Administrador(AbstractUser):
#     ROL_CHOICES = [
#         ('super_admin', 'Super Administrador'),
#         ('admin', 'Administrador'),
#         ('vendedor', 'Vendedor'),
#         ('produccion', 'Producción'),
#         ('diseñador', 'Diseñador'),
#         ('compras', 'Compras'),
#     ]
    
#     ESTADO_CHOICES = [
#         ('activo', 'Activo'),
#         ('suspendido', 'Suspendido'),
#         ('inactivo', 'Inactivo'),
#     ]
    
#     # Campos adicionales
#     nombre_completo = models.CharField(max_length=100)
#     rol = models.CharField(max_length=15, choices=ROL_CHOICES)
#     permisos_especiales = models.JSONField(default=dict, blank=True)
    
#     # Control de acceso
#     estado = models.CharField(max_length=15, choices=ESTADO_CHOICES, default='activo')
#     intentos_login_fallidos = models.PositiveIntegerField(default=0)
#     fecha_ultimo_login = models.DateTimeField(blank=True, null=True)
#     fecha_bloqueo = models.DateTimeField(blank=True, null=True)
    
#     # Información adicional
#     telefono = models.CharField(max_length=20, blank=True)
#     notas_admin = models.TextField(blank=True)
    
#     class Meta:
#         db_table = 'administradores'
#         verbose_name = 'Administrador'
#         verbose_name_plural = 'Administradores'
#         indexes = [
#             models.Index(fields=['username']),
#             models.Index(fields=['email']),
#             models.Index(fields=['rol']),
#             models.Index(fields=['estado']),
#         ]
    
#     def __str__(self):
#         return f"{self.nombre_completo} ({self.get_rol_display()})"
    
#     @property
#     def esta_bloqueado(self):
#         """Verifica si el usuario está bloqueado"""
#         return self.fecha_bloqueo and self.fecha_bloqueo > timezone.now()
    
#     def puede_gestionar_cotizaciones(self):
#         """Verifica si puede gestionar cotizaciones"""
#         return self.rol in ['super_admin', 'admin', 'vendedor']
    
#     def puede_gestionar_produccion(self):
#         """Verifica si puede gestionar producción"""
#         return self.rol in ['super_admin', 'admin', 'produccion']

# class Notificacion(models.Model):
#     TIPO_CHOICES = [
#         ('stock_bajo', 'Stock Bajo'),
#         ('stock_agotado', 'Stock Agotado'),
#         ('cotizacion_vencida', 'Cotización Vencida'),
#         ('pedido_atrasado', 'Pedido Atrasado'),
#         ('compra_pendiente', 'Compra Pendiente'),
#         ('produccion_atrasada', 'Producción Atrasada'),
#         ('cliente_nuevo', 'Cliente Nuevo'),
#         ('pago_pendiente', 'Pago Pendiente'),
#         ('sistema', 'Sistema'),
#     ]
    
#     PRIORIDAD_CHOICES = [
#         ('baja', 'Baja'),
#         ('media', 'Media'),
#         ('alta', 'Alta'),
#         ('critica', 'Crítica'),
#     ]
    
#     CATEGORIA_CHOICES = [
#         ('stock', 'Stock'),
#         ('ventas', 'Ventas'),
#         ('produccion', 'Producción'),
#         ('compras', 'Compras'),
#         ('sistema', 'Sistema'),
#         ('pagos', 'Pagos'),
#     ]
    
#     # Destinatario
#     administrador = models.ForeignKey(Administrador, on_delete=models.CASCADE, null=True, blank=True, related_name='notificaciones')
#     roles_destinatarios = models.JSONField(default=list, blank=True)  # Para notificaciones por rol
    
#     # Clasificación
#     tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
#     prioridad = models.CharField(max_length=10, choices=PRIORIDAD_CHOICES, default='media')
#     categoria = models.CharField(max_length=15, choices=CATEGORIA_CHOICES)
    
#     # Contenido
#     titulo = models.CharField(max_length=150)
#     mensaje = models.TextField()
#     datos_adicionales = models.JSONField(default=dict, blank=True)
    
#     # Referencias
#     tabla_referencia = models.CharField(max_length=50, blank=True)
#     id_referencia = models.PositiveIntegerField(blank=True, null=True)
#     url_accion = models.URLField(blank=True)
    
#     # Control de estado
#     leida = models.BooleanField(default=False)
#     archivada = models.BooleanField(default=False)
#     fecha_creacion = models.DateTimeField(default=timezone.now)
#     fecha_lectura = models.DateTimeField(blank=True, null=True)
#     fecha_expiracion = models.DateTimeField(blank=True, null=True)
    
#     class Meta:
#         db_table = 'notificaciones'
#         verbose_name = 'Notificación'
#         verbose_name_plural = 'Notificaciones'
#         ordering = ['-fecha_creacion']
#         indexes = [
#             models.Index(fields=['administrador', 'leida']),
#             models.Index(fields=['tipo']),
#             models.Index(fields=['prioridad']),
#             models.Index(fields=['fecha_creacion']),
#             models.Index(fields=['tabla_referencia', 'id_referencia']),
#         ]
    
#     def __str__(self):
#         return f"{self.titulo} - {self.get_prioridad_display()}"
    
#     def marcar_como_leida(self):
#         """Marca la notificación como leída"""
#         if not self.leida:
#             self.leida = True
#             self.fecha_lectura = timezone.now()
#             self.save(update_fields=['leida', 'fecha_lectura'])
    
#     @property
#     def esta_expirada(self):
#         """Verifica si la notificación está expirada"""
#         if self.fecha_expiracion:
#             return timezone.now() > self.fecha_expiracion
#         return False
