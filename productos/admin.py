from django.contrib import admin
from .models import Producto
from django.utils.html import format_html

# Register your models here.

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['thumbnail_preview', 'nombre', 'precio_formateado', 'orden', 'activo', 'fecha_creacion']
    list_display_links = ['thumbnail_preview', 'nombre']
    list_filter = ['activo', 'fecha_creacion']
    search_fields = ['nombre', 'descripcion']
    list_editable = ['activo', 'orden']
    readonly_fields = ['imagen_preview', 'fecha_creacion', 'fecha_actualizacion']
    
    fieldsets = [
        ('Información del Producto', {
            'fields': ('nombre', 'descripcion', 'precio')
        }),
        ('Imagen', {
            'fields': ('imagen', 'imagen_preview')
        }),
        ('Configuración', {
            'fields': ('orden', 'activo')
        }),
        ('Metadatos', {
            'fields': ('fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    ]
    
    def thumbnail_preview(self, obj):
        """Miniatura para el listado"""
        if obj.imagen:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 5px;" />',
                obj.imagen.url
            )
        return "Sin imagen"
    thumbnail_preview.short_description = "Imagen"
    
    def precio_formateado(self, obj):
        """Precio formateado con separador de miles"""
        return f"${obj.precio:,.0f}".replace(",", ".")
    precio_formateado.short_description = "Precio"
    precio_formateado.admin_order_field = 'precio'
    
    def imagen_preview(self, obj):
        """Vista previa grande para el formulario"""
        if obj.imagen:
            return format_html(
                '<img src="{}" style="max-width: 300px; max-height: 300px; border-radius: 10px;" />',
                obj.imagen.url
            )
        return "No hay imagen cargada"
    imagen_preview.short_description = "Vista Previa"
    
    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }
