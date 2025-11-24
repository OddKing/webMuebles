from django.db import models
from django.core.validators import RegexValidator

# Create your models here.

class Cita(models.Model):
    TIPO_REUNION_CHOICES = [
        ('online', 'Online'),
        ('presencial', 'Presencial'),
    ]
    
    ESTADO_CHOICES = [
        ('pendiente_aprobacion', 'Pendiente de Aprobación'),
        ('aprobada', 'Aprobada'),
        ('rechazada', 'Rechazada'),
        ('cancelada', 'Cancelada'),
    ]
    
    # Validador para teléfono
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="El número de teléfono debe estar en el formato: '+999999999'. Hasta 15 dígitos permitidos."
    )
    
    nombre_completo = models.CharField(max_length=200, verbose_name="Nombre Completo")
    telefono = models.CharField(validators=[phone_regex], max_length=17, verbose_name="Teléfono")
    direccion = models.CharField(max_length=300, verbose_name="Dirección")
    email = models.EmailField(verbose_name="Email")
    tipo_reunion = models.CharField(max_length=20, choices=TIPO_REUNION_CHOICES, verbose_name="Tipo de Reunión")
    fecha = models.DateField(verbose_name="Fecha de Reunión")
    hora = models.TimeField(verbose_name="Hora de Reunión")
    meeting_link = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name="Link de Reunión Online",
        help_text="Link de Google Meet generado automáticamente para reuniones online"
    )
    estado = models.CharField(max_length=25, choices=ESTADO_CHOICES, default='pendiente_aprobacion', verbose_name="Estado")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    fecha_aprobacion = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Aprobación")
    admin_notas = models.TextField(blank=True, verbose_name="Notas del Administrador", help_text="Razón de rechazo o notas internas")
    
    class Meta:
        verbose_name = "Cita"
        verbose_name_plural = "Citas"
        ordering = ['fecha', 'hora']
    
    def __str__(self):
        return f"{self.nombre_completo} - {self.fecha} {self.hora}"


class Cotizacion(models.Model):
    """Modelo para solicitudes de cotización de productos"""
    MATERIAL_CHOICES = [
        ('pino', 'Pino'),
        ('roble', 'Roble'),
        ('mdf', 'MDF'),
        ('melamina', 'Melamina'),
        ('otro', 'Otro'),
    ]
    
    ESTADO_CHOICES = [
        ('pendiente_aprobacion', 'Pendiente de Aprobación'),
        ('aprobada', 'Aprobada'),
        ('rechazada', 'Rechazada'),
        ('en_revision', 'En Revisión'),
        ('cotizada', 'Cotizada'),
        ('aceptada', 'Aceptada'),
    ]
    
    # Producto relacionado (opcional)
    producto = models.ForeignKey(
        'productos.Producto', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        verbose_name="Producto de Referencia"
    )
    
    # Cliente relacionado (opcional) - para clientes habituales
    cliente = models.ForeignKey(
        'clientes.Cliente',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Cliente Habitual",
        help_text="Vincular con un cliente registrado en el sistema"
    )
    
    # Datos del cliente
    nombre_completo = models.CharField(max_length=200, verbose_name="Nombre Completo")
    rut = models.CharField(max_length=12, verbose_name="RUT", help_text="Formato: 12.345.678-9", blank=True)
    direccion = models.CharField(max_length=300, verbose_name="Dirección", blank=True)
    email = models.EmailField(verbose_name="Email")
    telefono = models.CharField(max_length=17, verbose_name="Teléfono", blank=True)
    
    # Requisitos del proyecto
    medidas_alto = models.DecimalField(
        max_digits=6, 
        decimal_places=2, 
        verbose_name="Alto (cm)",
        help_text="Altura en centímetros"
    )
    medidas_ancho = models.DecimalField(
        max_digits=6, 
        decimal_places=2, 
        verbose_name="Ancho (cm)",
        help_text="Ancho en centímetros"
    )
    medidas_profundidad = models.DecimalField(
        max_digits=6, 
        decimal_places=2, 
        verbose_name="Profundidad (cm)",
        help_text="Profundidad en centímetros"
    )
    material_preferido = models.CharField(
        max_length=20, 
        choices=MATERIAL_CHOICES, 
        verbose_name="Material Preferido"
    )
    descripcion_proyecto = models.TextField(verbose_name="Descripción del Proyecto", blank=True)
    foto_lugar = models.ImageField(
        upload_to='cotizaciones/fotos/',
        verbose_name="Foto del Lugar",
        blank=True,
        null=True,
        help_text="Foto del espacio donde se instalará el mueble"
    )
    
    # Gestión administrativa
    folio = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Folio",
        help_text="Número de folio único (ej: COT-001)",
        blank=True
    )
    estado = models.CharField(
        max_length=25, 
        choices=ESTADO_CHOICES, 
        default='pendiente_aprobacion', 
        verbose_name="Estado"
    )
    precio_cotizado = models.DecimalField(
        max_digits=10, 
        decimal_places=0, 
        null=True, 
        blank=True,
        verbose_name="Precio Cotizado ($)",
        help_text="Precio en pesos chilenos"
    )
    admin_notas = models.TextField(
        blank=True, 
        verbose_name="Notas Administrativas",
        help_text="Notas internas, no visibles para el cliente"
    )
    fecha_solicitud = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Solicitud")
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Última Actualización")
    fecha_aprobacion = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Aprobación")
    
    class Meta:
        verbose_name = "Cotización"
        verbose_name_plural = "Cotizaciones"
        ordering = ['-fecha_solicitud']
    
    def __str__(self):
        producto_nombre = self.producto.nombre if self.producto else "Diseño Personalizado"
        return f"{self.nombre_completo} - {producto_nombre} ({self.get_estado_display()})"


class ConsentimientoLegal(models.Model):
    """
    Modelo para registrar el consentimiento de usuarios a los Términos y Condiciones
    y Política de Privacidad. Cumple con ISO 27701 y Ley 19.628 de Chile.
    """
    # Relación con Cita o Cotización (uno de los dos debe estar presente)
    cita = models.OneToOneField(
        Cita, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name='consentimiento',
        verbose_name="Cita Relacionada"
    )
    cotizacion = models.OneToOneField(
        Cotizacion, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name='consentimiento',
        verbose_name="Cotización Relacionada"
    )
    
    # Información de consentimiento
    acepto_terminos = models.BooleanField(default=False, verbose_name="Aceptó Términos y Condiciones")
    acepto_privacidad = models.BooleanField(default=False, verbose_name="Aceptó Política de Privacidad")
    
    # Versiones de documentos aceptados
    version_terminos = models.CharField(
        max_length=20, 
        default='1.0',
        verbose_name="Versión de Términos y Condiciones"
    )
    version_privacidad = models.CharField(
        max_length=20, 
        default='1.0',
        verbose_name="Versión de Política de Privacidad"
    )
    
    # Información técnica para auditoría
    ip_address = models.GenericIPAddressField(
        verbose_name="Dirección IP",
        help_text="IP desde donde se aceptaron los términos"
    )
    user_agent = models.CharField(
        max_length=500,
        verbose_name="User Agent",
        help_text="Navegador y sistema operativo del usuario"
    )
    
    # Timestamps
    fecha_aceptacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha y Hora de Aceptación"
    )
    
    class Meta:
        verbose_name = "Consentimiento Legal"
        verbose_name_plural = "Consentimientos Legales"
        ordering = ['-fecha_aceptacion']
        
    def __str__(self):
        if self.cita:
            return f"Consentimiento - Cita: {self.cita.nombre_completo} ({self.fecha_aceptacion.strftime('%d/%m/%Y %H:%M')})"
        elif self.cotizacion:
            return f"Consentimiento - Cotización: {self.cotizacion.nombre_completo} ({self.fecha_aceptacion.strftime('%d/%m/%Y %H:%M')})"
        return f"Consentimiento - {self.fecha_aceptacion.strftime('%d/%m/%Y %H:%M')}"
    
    def clean(self):
        """Validar que al menos una relación (cita o cotización) esté presente"""
        from django.core.exceptions import ValidationError
        if not self.cita and not self.cotizacion:
            raise ValidationError('Debe estar relacionado con una Cita o una Cotización')
        if self.cita and self.cotizacion:
            raise ValidationError('No puede estar relacionado con ambos, Cita y Cotización')
