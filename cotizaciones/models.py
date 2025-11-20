from django.db import models
from django.core.validators import RegexValidator

# Create your models here.

class Cita(models.Model):
    TIPO_REUNION_CHOICES = [
        ('online', 'Online'),
        ('presencial', 'Presencial'),
    ]
    
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('confirmada', 'Confirmada'),
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
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente', verbose_name="Estado")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    
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
        ('pendiente', 'Pendiente'),
        ('en_revision', 'En Revisión'),
        ('cotizada', 'Cotizada'),
        ('aceptada', 'Aceptada'),
        ('rechazada', 'Rechazada'),
    ]
    
    # Producto relacionado (opcional)
    producto = models.ForeignKey(
        'productos.Producto', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        verbose_name="Producto de Referencia"
    )
    
    # Datos del cliente
    nombre_completo = models.CharField(max_length=200, verbose_name="Nombre Completo")
    email = models.EmailField(verbose_name="Email")
    telefono = models.CharField(max_length=17, verbose_name="Teléfono")
    
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
    descripcion_proyecto = models.TextField(verbose_name="Descripción del Proyecto")
    
    # Gestión administrativa
    estado = models.CharField(
        max_length=20, 
        choices=ESTADO_CHOICES, 
        default='pendiente', 
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
    notas_admin = models.TextField(
        blank=True, 
        verbose_name="Notas Administrativas",
        help_text="Notas internas, no visibles para el cliente"
    )
    fecha_solicitud = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Solicitud")
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Última Actualización")
    
    class Meta:
        verbose_name = "Cotización"
        verbose_name_plural = "Cotizaciones"
        ordering = ['-fecha_solicitud']
    
    def __str__(self):
        producto_nombre = self.producto.nombre if self.producto else "Diseño Personalizado"
        return f"{self.nombre_completo} - {producto_nombre} ({self.get_estado_display()})"
