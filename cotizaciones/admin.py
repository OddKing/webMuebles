from django.contrib import admin
from .models import Cita, Cotizacion, ConsentimientoLegal
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
        ('Gestión Administrativa', {
            'fields': ('admin_notas', 'fecha_aprobacion'),
            'classes': ('collapse',)
        }),
        ('Información del Sistema', {
            'fields': ('fecha_creacion',),
            'classes': ('collapse',)
        }),
    ]
    
    readonly_fields = ['fecha_creacion', 'fecha_aprobacion']
    
    actions = ['marcar_aprobada', 'marcar_rechazada', 'marcar_cancelada']
    
    def estado_badge(self, obj):
        """Badge colorido para el estado"""
        colors = {
            'pendiente_aprobacion': '#ffc107',
            'aprobada': '#28a745',
            'rechazada': '#dc3545',
            'cancelada': '#6c757d'
        }
        color = colors.get(obj.estado, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 15px; font-weight: bold;">{}</span>',
            color,
            obj.get_estado_display()
        )
    estado_badge.short_description = "Estado"
    
    @admin.action(description='Marcar como Aprobada')
    def marcar_aprobada(self, request, queryset):
        from django.utils import timezone
        updated = queryset.update(estado='aprobada', fecha_aprobacion=timezone.now())
        self.message_user(request, f'{updated} cita(s) marcada(s) como aprobada.')
    
    @admin.action(description='Marcar como Rechazada')
    def marcar_rechazada(self, request, queryset):
        updated = queryset.update(estado='rechazada')
        self.message_user(request, f'{updated} cita(s) marcada(s) como rechazada.')
    
    @admin.action(description='Marcar como Cancelada')
    def marcar_cancelada(self, request, queryset):
        updated = queryset.update(estado='cancelada')
        self.message_user(request, f'{updated} cita(s) marcada(s) como cancelada.')


@admin.register(Cotizacion)
class CotizacionAdmin(admin.ModelAdmin):
    list_display = ['nombre_completo', 'folio', 'producto', 'material_preferido', 'estado_badge', 'precio_cotizado', 'fecha_solicitud']
    list_display_links = ['nombre_completo']
    list_filter = ['estado', 'material_preferido', 'fecha_solicitud']
    search_fields = ['nombre_completo', 'email', 'descripcion_proyecto', 'folio']
    # date_hierarchy = 'fecha_solicitud'  # Comentado temporalmente por error
    ordering = ['-fecha_solicitud']
    
    fieldsets = [
        ('Cliente', {
            'fields': ('nombre_completo', 'rut', 'email', 'telefono', 'direccion')
        }),
        ('Proyecto', {
            'fields': ('producto', 'descripcion_proyecto', 'foto_lugar')
        }),
        ('Medidas (cm)', {
            'fields': ('medidas_alto', 'medidas_ancho', 'medidas_profundidad')
        }),
        ('Especificaciones', {
            'fields': ('material_preferido',)
        }),
        ('Gestión Administrativa', {
            'fields': ('folio', 'estado', 'precio_cotizado', 'admin_notas', 'fecha_aprobacion'),
            'classes': ('wide',)
        }),
        ('Fechas', {
            'fields': ('fecha_solicitud', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    ]
    
    readonly_fields = ['fecha_solicitud', 'fecha_actualizacion', 'fecha_aprobacion']
    
    actions = ['marcar_aprobada', 'marcar_rechazada', 'marcar_en_revision', 'marcar_cotizada']
    
    def estado_badge(self, obj):
        """Badge colorido para el estado"""
        colors = {
            'pendiente_aprobacion': '#ffc107',
            'aprobada': '#28a745',
            'rechazada': '#dc3545',
            'en_revision': '#17a2b8',
            'cotizada': '#007bff',
            'aceptada': '#198754'
        }
        color = colors.get(obj.estado, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 15px; font-weight: bold;">{}</span>',
            color,
            obj.get_estado_display()
        )
    estado_badge.short_description = "Estado"
    
    @admin.action(description='Marcar como Aprobada')
    def marcar_aprobada(self, request, queryset):
        from django.utils import timezone
        updated = queryset.update(estado='aprobada', fecha_aprobacion=timezone.now())
        self.message_user(request, f'{updated} cotización(es) marcada(s) como aprobada.')
    
    @admin.action(description='Marcar como Rechazada')
    def marcar_rechazada(self, request, queryset):
        updated = queryset.update(estado='rechazada')
        self.message_user(request, f'{updated} cotización(es) marcada(s) como rechazada.')
    
    @admin.action(description='Marcar como En Revisión')
    def marcar_en_revision(self, request, queryset):
        updated = queryset.update(estado='en_revision')
        self.message_user(request, f'{updated} cotización(es) marcada(s) como en revisión.')
    
    @admin.action(description='Marcar como Cotizada')
    def marcar_cotizada(self, request, queryset):
        updated = queryset.update(estado='cotizada')
        self.message_user(request, f'{updated} cotización(es) marcada(s) como cotizada.')


@admin.register(ConsentimientoLegal)
class ConsentimientoLegalAdmin(admin.ModelAdmin):
    """Admin para visualizar registros de consentimiento (solo lectura)"""
    list_display = ['get_nombre', 'get_tipo', 'acepto_terminos', 'acepto_privacidad', 'ip_address', 'fecha_aceptacion']
    list_filter = ['acepto_terminos', 'acepto_privacidad', 'fecha_aceptacion']
    search_fields = ['cita__nombre_completo', 'cotizacion__nombre_completo', 'ip_address']
    # date_hierarchy = 'fecha_aceptacion'
    ordering = ['-fecha_aceptacion']
    
    fieldsets = [
        ('Relación', {
            'fields': ('cita', 'cotizacion')
        }),
        ('Consentimiento', {
            'fields': ('acepto_terminos', 'acepto_privacidad', 'version_terminos', 'version_privacidad')
        }),
        ('Información de Auditoría', {
            'fields': ('ip_address', 'user_agent', 'fecha_aceptacion'),
            'classes': ('wide',)
        }),
    ]
    
    readonly_fields = ['cita', 'cotizacion', 'acepto_terminos', 'acepto_privacidad', 
                      'version_terminos', 'version_privacidad', 'ip_address', 
                      'user_agent', 'fecha_aceptacion']
    
    def has_add_permission(self, request):
        """No permitir crear consentimientos manualmente"""
        return False
    
    def has_delete_permission(self, request, obj=None):
        """No permitir eliminar consentimientos (auditoría)"""
        return False
    
    def get_nombre(self, obj):
        """Obtener nombre del cliente"""
        if obj.cita:
            return obj.cita.nombre_completo
        elif obj.cotizacion:
            return obj.cotizacion.nombre_completo
        return "N/A"
    get_nombre.short_description = "Cliente"
    
    def get_tipo(self, obj):
        """Obtener tipo de registro"""
        if obj.cita:
            return format_html('<span style="background-color: #17a2b8; color: white; padding: 3px 10px; border-radius: 15px;">Cita</span>')
        elif obj.cotizacion:
            return format_html('<span style="background-color: #007bff; color: white; padding: 3px 10px; border-radius: 15px;">Cotización</span>')
        return "N/A"
    get_tipo.short_description = "Tipo"
