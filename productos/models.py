from django.db import models

# Create your models here.

class Producto(models.Model):
    """Modelo para productos del catálogo"""
    nombre = models.CharField(max_length=200, verbose_name="Nombre del Producto")
    descripcion = models.TextField(verbose_name="Descripción")
    precio = models.DecimalField(
        max_digits=10, 
        decimal_places=0, 
        verbose_name="Precio",
        help_text="Precio en pesos chilenos"
    )
    imagen = models.ImageField(upload_to='productos/', verbose_name="Imagen del Producto")
    orden = models.IntegerField(
        default=0,
        verbose_name="Orden",
        help_text="Orden de visualización (menor número aparece primero)"
    )
    activo = models.BooleanField(default=True, verbose_name="Activo")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Última Actualización")
    
    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ['orden', '-fecha_creacion']
    
    def __str__(self):
        return self.nombre
