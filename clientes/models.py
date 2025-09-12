from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone
from webMuebles.models import BaseModel

class Cliente(BaseModel):
    
    TIPO_CLIENTE_CHOICES = [
        ('particular', 'Particular'),
        ('empresa', 'Empresa'),
    ]
    
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
        ('bloqueado', 'Bloqueado'),
    ]
    
    # Validador para teléfono chileno
    phone_validator = RegexValidator(
        regex=r'^\+?56?[0-9]{8,9}$',
        message="Número de teléfono debe ser formato chileno válido."
    )
    
    nombre = models.CharField(max_length=100)
    email = models.EmailField(max_length=150, unique=True, blank=True, null=True)
    telefono = models.CharField(max_length=20, validators=[phone_validator])
    telefono_secundario = models.CharField(max_length=20, blank=True, validators=[phone_validator])
    direccion = models.TextField(blank=True)
    tipo_cliente = models.CharField(max_length=15, choices=TIPO_CLIENTE_CHOICES, default='particular')
    estado = models.CharField(max_length=15, choices=ESTADO_CHOICES, default='activo')
    fecha_registro = models.DateTimeField(default=timezone.now)
    fecha_ultima_compra = models.DateTimeField(blank=True, null=True)
    notas_cliente = models.TextField(blank=True)
    
    class Meta:
        db_table = 'clientes'
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['-fecha_registro']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['telefono']),
            models.Index(fields=['tipo_cliente']),
            models.Index(fields=['estado']),
        ]
    
    def __str__(self):
        return f"{self.nombre} ({self.get_tipo_cliente_display()})"
    
    @property
    def telefono_formateado(self):
        """Devuelve el teléfono en formato chileno estándar"""
        phone = self.telefono.replace('+56', '').replace(' ', '')
        if len(phone) == 9:
            return f"+56 9 {phone[1:5]} {phone[5:]}"
        return self.telefono
    
    def tiene_cotizaciones_activas(self):
        """Verifica si el cliente tiene cotizaciones pendientes"""
        return self.cotizaciones.filter(estado__in=['pendiente', 'enviada']).exists()