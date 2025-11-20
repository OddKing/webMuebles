from django.contrib import admin
from .models import Cita, Cotizacion
from django.utils.html import format_html

# Register your models here.

@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    list_display = ['nombre_completo', 'fecha', 'hora', 'tipo_reunion', 'estado_badge', 'email']
    list_display_links = ['nombre_completo']
    list_filter = ['estado', 'tipo_reunion', 'fecha']
    search_fields = ['nombre_completo', 'email', 'telefono']
    date_hierarchy = 'fecha'
    ordering = ['fecha', 'hora']
    
    fieldsets = [
        ('Información del Cliente', {
            'fields': ('nombre_completo', 'email', 'telefono', 'direccion')
        }),
        ('Detalles de la Reunión', {
            'fields': ('tipo_reunion', 'fecha', 'hora', 'estado')
        }),
        ('Información del Sistema', {
            'fields': ('fecha_creacion',),
            'classes': ('collapse',)
        }),
    ]
    
    readonly_fields = ['fecha_creacion']
    
    actions = ['marcar_confirmada', 'marcar_cancelada']
    
    def estado_badge(self, obj):
        """Badge colorido para el estado"""
        colors = {
            'pendiente': '#ffc107',
            'confirmada': '#28a745',
            'cancelada': '#dc3545'
        }
        color = colors.get(obj.estado, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 15px; font-weight: bold;">{}</span>',
            color,
            obj.get_estado_display()
        )
    estado_badge.short_description = "Estado"
    
    @admin.action(description='Marcar como Confirmada')
    def marcar_confirmada(self, request, queryset):
        updated = queryset.update(estado='confirmada')
        self.message_user(request, f'{updated} cita(s) marcada(s) como confirmada.')
    
    @admin.action(description='Marcar como Cancelada')
    def marcar_cancelada(self, request, queryset):
        updated = queryset.update(estado='cancelada')
        self.message_user(request, f'{updated} cita(s) marcada(s) como cancelada.')


@admin.register(Cotizacion)
class CotizacionAdmin(admin.ModelAdmin):
    list_display = ['nombre_completo', 'producto', 'material_preferido', 'estado_badge', 'precio_cotizado', 'fecha_solicitud']
    list_display_links = ['nombre_completo']
    list_filter = ['estado', 'material_preferido', 'fecha_solicitud']
    search_fields = ['nombre_completo', 'email', 'descripcion_proyecto']
    date_hierarchy = 'fecha_solicitud'
    ordering = ['-fecha_solicitud']
    
    fieldsets = [
        ('Cliente', {
            'fields': ('nombre_completo', 'email', 'telefono')
        }),
        ('Proyecto', {
            'fields': ('producto', 'descripcion_proyecto')
        }),
        ('Medidas (cm)', {
            'fields': ('medidas_alto', 'medidas_ancho', 'medidas_profundidad')
        }),
        ('Especificaciones', {
            'fields': ('material_preferido',)
        }),
        ('Gestión Administrativa', {
            'fields': ('estado', 'precio_cotizado', 'notas_admin'),
            'classes': ('wide',)
        }),
        ('Fechas', {
            'fields': ('fecha_solicitud', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    ]
    
    readonly_fields = ['fecha_solicitud', 'fecha_actualizacion']
    
    actions = ['marcar_en_revision', 'marcar_cotizada']
    
    def estado_badge(self, obj):
        """Badge colorido para el estado"""
        colors = {
            'pendiente': '#ffc107',
            'en_revision': '#17a2b8',
            'cotizada': '#007bff',
            'aceptada': '#28a745',
            'rechazada': '#dc3545'
        }
        color = colors.get(obj.estado, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 15px; font-weight: bold;">{}</span>',
            color,
            obj.get_estado_display()
        )
    estado_badge.short_description = "Estado"
    
    @admin.action(description='Marcar como En Revisión')
    def marcar_en_revision(self, request, queryset):
        updated = queryset.update(estado='en_revision')
        self.message_user(request, f'{updated} cotización(es) marcada(s) como en revisión.')
    
    @admin.action(description='Marcar como Cotizada')
    def marcar_cotizada(self, request, queryset):
        updated = queryset.update(estado='cotizada')
        self.message_user(request, f'{updated} cotización(es) marcada(s) como cotizada.')
