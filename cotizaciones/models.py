from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from decimal import Decimal

class Cotizacion(models.Model):
    ESTADO_CHOICES = [
        ('borrador', 'Borrador'),
        ('pendiente', 'Pendiente'),
        ('enviada', 'Enviada'),
        ('aprobada', 'Aprobada'),
        ('rechazada', 'Rechazada'),
        ('vencida', 'Vencida'),
        ('cancelada', 'Cancelada'),
    ]
    
    URGENCIA_CHOICES = [
        ('muy_urgente', 'Muy Urgente'),
        ('urgente', 'Urgente'),
        ('normal', 'Normal'),
        ('flexible', 'Flexible'),
    ]
    
    # Campos principales
    numero_cotizacion = models.CharField(max_length=20, unique=True, editable=False)
    cliente = models.ForeignKey('clientes.Cliente', on_delete=models.PROTECT, related_name='cotizaciones')
    administrador = models.ForeignKey('administracion.Administrador', on_delete=models.SET_NULL, null=True, blank=True, related_name='cotizaciones_creadas')
    
    # Información del proyecto
    nombre_proyecto = models.CharField(max_length=150, blank=True)
    descripcion_general = models.TextField()
    dimensiones_personalizadas = models.CharField(max_length=100, blank=True)
    material_solicitado = models.CharField(max_length=80, blank=True)
    ubicacion_instalacion = models.TextField(blank=True)
    
    # Preferencias del cliente
    requiere_reunion = models.BooleanField(default=True)
    urgencia = models.CharField(max_length=15, choices=URGENCIA_CHOICES, default='normal')
    presupuesto_estimado_cliente = models.CharField(max_length=50, blank=True)
    
    # Cálculos y precios
    subtotal_materiales = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    subtotal_mano_obra = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    descuento_porcentaje = models.DecimalField(max_digits=5, decimal_places=2, default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    descuento_monto = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    precio_total = models.DecimalField(max_digits=12, decimal_places=2)
    
    # Estados y fechas
    estado = models.CharField(max_length=15, choices=ESTADO_CHOICES, default='borrador')
    fecha_cotizacion = models.DateTimeField(default=timezone.now)
    fecha_vencimiento = models.DateTimeField(blank=True, null=True)
    fecha_respuesta_cliente = models.DateTimeField(blank=True, null=True)
    fecha_ultima_modificacion = models.DateTimeField(auto_now=True)
    
    # Archivos y observaciones
    archivo_planos = models.FileField(upload_to='cotizaciones/planos/', blank=True)
    observaciones_internas = models.TextField(blank=True)
    observaciones_cliente = models.TextField(blank=True)
    
    class Meta:
        db_table = 'cotizaciones'
        verbose_name = 'Cotización'
        verbose_name_plural = 'Cotizaciones'
        ordering = ['-fecha_cotizacion']
        indexes = [
            models.Index(fields=['cliente']),
            models.Index(fields=['estado']),
            models.Index(fields=['fecha_cotizacion']),
            models.Index(fields=['fecha_vencimiento']),
            models.Index(fields=['numero_cotizacion']),
        ]
    
    def __str__(self):
        return f"{self.numero_cotizacion} - {self.cliente.nombre}"
    
    def save(self, *args, **kwargs):
        if not self.numero_cotizacion:
            self.numero_cotizacion = self.generar_numero_cotizacion()
        
        # Calcular precio total automáticamente
        self.calcular_precio_total()
        
        super().save(*args, **kwargs)
    
    def generar_numero_cotizacion(self):
        """Genera un número único de cotización"""
        año = timezone.now().year
        ultimo_numero = Cotizacion.objects.filter(
            numero_cotizacion__startswith=f'COT-{año}'
        ).count() + 1
        return f'COT-{año}-{ultimo_numero:03d}'
    
    def calcular_precio_total(self):
        """Calcula el precio total considerando descuentos"""
        subtotal = self.subtotal_materiales + self.subtotal_mano_obra
        
        if self.descuento_porcentaje > 0:
            self.descuento_monto = subtotal * (self.descuento_porcentaje / 100)
        
        self.precio_total = subtotal - self.descuento_monto
    
    @property
    def esta_vencida(self):
        """Verifica si la cotización está vencida"""
        if self.fecha_vencimiento:
            return timezone.now() > self.fecha_vencimiento
        return False
    
    @property
    def dias_para_vencer(self):
        """Calcula los días restantes para vencimiento"""
        if self.fecha_vencimiento:
            delta = self.fecha_vencimiento - timezone.now()
            return delta.days
        return None
    
    def puede_convertirse_a_pedido(self):
        """Verifica si la cotización puede convertirse en pedido"""
        return self.estado == 'aprobada'

class CotizacionItem(models.Model):
    cotizacion = models.ForeignKey(Cotizacion, on_delete=models.CASCADE, related_name='items')
    producto = models.ForeignKey('productos.Producto', on_delete=models.SET_NULL, null=True, blank=True, related_name='cotizaciones')
    
    # Detalles del item
    nombre_item = models.CharField(max_length=150)
    descripcion_detallada = models.TextField(blank=True)
    cantidad = models.PositiveIntegerField(default=1)
    dimensiones_finales = models.CharField(max_length=100, blank=True)
    material_final = models.CharField(max_length=80, blank=True)
    color_acabado = models.CharField(max_length=50, blank=True)
    
    # Precios
    precio_unitario_materiales = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    precio_unitario_mano_obra = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    precio_unitario_total = models.DecimalField(max_digits=10, decimal_places=2)
    precio_total_item = models.DecimalField(max_digits=12, decimal_places=2)
    
    # Tiempos
    dias_fabricacion_estimados = models.PositiveIntegerField(default=15)
    
    class Meta:
        db_table = 'cotizacion_items'
        verbose_name = 'Item de Cotización'
        verbose_name_plural = 'Items de Cotización'
        indexes = [
            models.Index(fields=['cotizacion']),
            models.Index(fields=['producto']),
        ]
    
    def __str__(self):
        return f"{self.cotizacion.numero_cotizacion} - {self.nombre_item}"
    
    def save(self, *args, **kwargs):
        # Calcular precios automáticamente
        self.precio_unitario_total = self.precio_unitario_materiales + self.precio_unitario_mano_obra
        self.precio_total_item = self.precio_unitario_total * self.cantidad
        super().save(*args, **kwargs)
