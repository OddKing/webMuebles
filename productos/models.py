from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
import json
from webMuebles.models import BaseModel

class CategoriaProducto(models.Model):
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
    ]
    
    nombre_categoria = models.CharField(max_length=80, unique=True)
    descripcion = models.TextField(blank=True)
    imagen_categoria = models.ImageField(upload_to='categorias/', blank=True)
    estado = models.CharField(max_length=15, choices=ESTADO_CHOICES, default='activo')
    orden_visualizacion = models.PositiveIntegerField(default=0)
    fecha_creacion = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'categorias'
        verbose_name = 'Categoría de Producto'
        verbose_name_plural = 'Categorías de Productos'
        ordering = ['orden_visualizacion', 'nombre_categoria']
        indexes = [
            models.Index(fields=['estado']),
            models.Index(fields=['orden_visualizacion']),
        ]
    
    def __str__(self):
        return self.nombre_categoria

class Producto(BaseModel):
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
        ('descontinuado', 'Descontinuado'),
    ]
    
    categoria = models.ForeignKey(CategoriaProducto, on_delete=models.PROTECT, related_name='productos')
    nombre_producto = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True)
    imagen_principal = models.ImageField(upload_to='productos/', blank=True)
    galeria_imagenes = models.JSONField(default=list, blank=True)  # Lista de URLs de imágenes
    dimensiones_estandar = models.CharField(max_length=100, blank=True)
    material_principal = models.CharField(max_length=80, blank=True)
    tiempo_fabricacion_dias = models.PositiveIntegerField(default=15)
    precio_base = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    estado = models.CharField(max_length=15, choices=ESTADO_CHOICES, default='activo')
    es_personalizable = models.BooleanField(default=True)
    popularidad = models.PositiveIntegerField(default=0)
    fecha_creacion = models.DateTimeField(default=timezone.now)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'productos'
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['-popularidad', 'nombre_producto']
        indexes = [
            models.Index(fields=['categoria']),
            models.Index(fields=['estado']),
            models.Index(fields=['material_principal']),
            models.Index(fields=['-popularidad']),
        ]
    
    def __str__(self):
        return f"{self.nombre_producto} ({self.categoria.nombre_categoria})"
    
    def incrementar_popularidad(self):
        """Incrementa la popularidad cuando se cotiza el producto"""
        self.popularidad += 1
        self.save(update_fields=['popularidad'])
    
    def get_precio_formateado(self):
        """Devuelve el precio en formato chileno"""
        if self.precio_base:
            return f"${self.precio_base:,.0f}".replace(',', '.')
        return "Precio bajo consulta"
