from django.db import models
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator

class Cliente(models.Model):
    """Modelo para gestionar clientes habituales de la empresa"""
    
    # Validador para RUT chileno
    rut_regex = RegexValidator(
        regex=r'^\d{1,2}\.\d{3}\.\d{3}[-][0-9kK]{1}$|^\d{7,8}[-][0-9kK]{1}$',
        message="RUT debe estar en formato: 12.345.678-9"
    )
    
    # Validador para teléfono
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Número de teléfono debe estar en formato: '+999999999'. Hasta 15 dígitos."
    )
    
    # Información básica
    nombre_completo = models.CharField(
        max_length=200, 
        verbose_name="Nombre Completo",
        help_text="Nombre completo del cliente"
    )
    
    rut = models.CharField(
        validators=[rut_regex],
        max_length=12,
        unique=True,
        verbose_name="RUT",
        help_text="RUT único del cliente (formato: 12.345.678-9)"
    )
    
    email = models.EmailField(
        verbose_name="Email",
        help_text="Email principal de contacto"
    )
    
    telefono = models.CharField(
        validators=[phone_regex],
        max_length=17,
        blank=True,
        verbose_name="Teléfono",
        help_text="Teléfono de contacto"
    )
    
    direccion = models.CharField(
        max_length=300,
        blank=True,
        verbose_name="Dirección",
        help_text="Dirección principal del cliente"
    )
    
    # Información corporativa (opcional)
    empresa = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Empresa",
        help_text="Nombre de la empresa (si es cliente corporativo)"
    )
    
    # Información comercial
    descuento_habitual = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="Descuento Habitual (%)",
        help_text="Porcentaje de descuento por ser cliente recurrente (0-100)"
    )
    
    # Notas internas
    notas = models.TextField(
        blank=True,
        verbose_name="Notas Internas",
        help_text="Notas y observaciones internas sobre el cliente"
    )
    
    # Control de estado
    activo = models.BooleanField(
        default=True,
        verbose_name="Cliente Activo",
        help_text="Indica si el cliente está activo en el sistema"
    )
    
    # Timestamps
    fecha_registro = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de Registro",
        help_text="Fecha en que se registró el cliente"
    )
    
    ultima_actualizacion = models.DateTimeField(
        auto_now=True,
        verbose_name="Última Actualización",
        help_text="Última vez que se modificó el registro"
    )
    
    ultima_cotizacion = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Última Cotización",
        help_text="Fecha de la última cotización realizada para este cliente"
    )
    
    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ['-ultima_cotizacion', '-fecha_registro']
        indexes = [
            models.Index(fields=['rut']),
            models.Index(fields=['email']),
            models.Index(fields=['-ultima_cotizacion']),
        ]
    
    def __str__(self):
        if self.empresa:
            return f"{self.nombre_completo} - {self.empresa}"
        return self.nombre_completo
    
    def get_numero_cotizaciones(self):
        """Retorna el número total de cotizaciones del cliente"""
        return self.cotizacion_set.count()
    
    def get_cotizaciones_aprobadas(self):
        """Retorna cotizaciones aprobadas del cliente"""
        return self.cotizacion_set.filter(estado='aprobada').count()
    
    def get_total_cotizado(self):
        """Retorna el total cotizado (suma de precios de cotizaciones aprobadas)"""
        from django.db.models import Sum
        total = self.cotizacion_set.filter(
            estado__in=['aprobada', 'aceptada'],
            precio_cotizado__isnull=False
        ).aggregate(Sum('precio_cotizado'))['precio_cotizado__sum']
        return total or 0
