from django.contrib import admin
from .models import Producto, Categoria

# Register your models here.

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'slug', 'orden')
    prepopulated_fields = {'slug': ('nombre',)}
    search_fields = ('nombre',)
    ordering = ('orden', 'nombre')

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'precio', 'orden', 'activo', 'fecha_creacion')
    list_filter = ('activo', 'categoria', 'fecha_creacion')
    search_fields = ('nombre', 'descripcion')
    list_editable = ('precio', 'orden', 'activo', 'categoria')
    ordering = ('orden', '-fecha_creacion')
