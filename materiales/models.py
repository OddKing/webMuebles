from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone

class CategoriaMaterial(models.Model):
    nombre = models.CharField(max_length=60, unique=True)
    descripcion = models.TextField(blank=True)
    fecha_creacion = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'categorias_materiales'
        verbose_name = 'Categoría de Material'
        verbose_name_plural = 'Categorías de Materiales'
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre

class Material(models.Model):
    TIPO_GESTION_CHOICES = [
        ('stock_permanente', 'Stock Permanente'),
        ('compra_por_pedido', 'Compra por Pedido'),
    ]
    
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('descontinuado', 'Descontinuado'),
        ('agotado', 'Agotado'),
    ]
    
    categoria_material = models.ForeignKey(CategoriaMaterial, on_delete=models.PROTECT, related_name='materiales')
    nombre_material = models.CharField(max_length=120)
    descripcion = models.TextField(blank=True)
    tipo_gestion = models.CharField(max_length=20, choices=TIPO_GESTION_CHOICES)
    unidad_medida = models.CharField(max_length=20)  # 'unidad', 'm2', 'ml', 'kg'
    precio_unitario_actual = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    proveedor_principal = models.CharField(max_length=100, blank=True)
    proveedores_alternativos = models.JSONField(default=list, blank=True)
    
    # Solo para materiales con stock permanente
    stock_actual = models.DecimalField(max_digits=10, decimal_places=3, default=0, validators=[MinValueValidator(0)])
    stock_minimo = models.DecimalField(max_digits=10, decimal_places=3, default=0, validators=[MinValueValidator(0)])
    stock_maximo = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True)
    
    estado = models.CharField(max_length=15, choices=ESTADO_CHOICES, default='activo')
    fecha_ultima_compra = models.DateTimeField(blank=True, null=True)
    fecha_actualizacion_precio = models.DateTimeField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'materiales'
        verbose_name = 'Material'
        verbose_name_plural = 'Materiales'
        ordering = ['categoria_material', 'nombre_material']
        indexes = [
            models.Index(fields=['categoria_material']),
            models.Index(fields=['tipo_gestion']),
            models.Index(fields=['estado']),
            models.Index(fields=['stock_actual', 'stock_minimo']),  # Para alertas
            models.Index(fields=['proveedor_principal']),
        ]
    
    def __str__(self):
        return f"{self.nombre_material} ({self.unidad_medida})"
    
    @property
    def necesita_reposicion(self):
        """Verifica si el material necesita reposición"""
        if self.tipo_gestion == 'stock_permanente':
            return self.stock_actual <= self.stock_minimo
        return False
    
    @property
    def porcentaje_stock(self):
        """Calcula el porcentaje de stock disponible"""
        if self.tipo_gestion == 'stock_permanente' and self.stock_maximo:
            return (self.stock_actual / self.stock_maximo) * 100
        return None
    
    def actualizar_stock(self, cantidad, tipo_movimiento, motivo=""):
        """Actualiza el stock y registra el movimiento"""
        if self.tipo_gestion == 'stock_permanente':
            stock_anterior = self.stock_actual
            
            if tipo_movimiento == 'entrada':
                self.stock_actual += cantidad
            elif tipo_movimiento == 'salida':
                self.stock_actual = max(0, self.stock_actual - cantidad)
            
            self.save(update_fields=['stock_actual'])
            
            # Aquí podrías registrar en HistorialStock si lo implementas
            return True
        return False

class ProductoMaterial(models.Model):
    """Relación muchos a muchos entre productos y materiales"""
    producto = models.ForeignKey('productos.Producto', on_delete=models.CASCADE, related_name='materiales_necesarios')
    material = models.ForeignKey(Material, on_delete=models.PROTECT, related_name='productos_que_lo_usan')
    cantidad_necesaria = models.DecimalField(max_digits=10, decimal_places=3, validators=[MinValueValidator(0.001)])
    es_material_principal = models.BooleanField(default=False)
    notas_uso = models.TextField(blank=True)
    
    class Meta:
        db_table = 'producto_materiales'
        verbose_name = 'Material de Producto'
        verbose_name_plural = 'Materiales de Productos'
        unique_together = ['producto', 'material']
        indexes = [
            models.Index(fields=['producto']),
            models.Index(fields=['material']),
        ]
    
    def __str__(self):
        return f"{self.producto.nombre_producto} - {self.material.nombre_material}"