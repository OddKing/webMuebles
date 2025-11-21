"""
URL configuration for webMuebles project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from administracion.views import portada, terminos_condiciones, politica_privacidad
from administracion.views_productos import lista_productos, crear_producto, editar_producto, eliminar_producto
from productos.views import catalogo
from cotizaciones.views import agendar_reunion, get_horarios_disponibles, solicitar_cotizacion, cotizacion_enviada
from cotizaciones.views_admin import (
    admin_login, admin_logout, admin_dashboard,
    admin_cotizaciones_pendientes, admin_citas_pendientes,
    aprobar_cotizacion, rechazar_cotizacion,
    aprobar_cita, rechazar_cita, preview_quote_pdf
)
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.urls import include

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
]

urlpatterns += [
    path('admin/', admin.site.urls),
    path('', portada, name='index'),
    path('catalogo/', catalogo, name='catalogo'),
    path('agendar/', agendar_reunion, name='agendar_reunion'),
    path('api/horarios-disponibles/', get_horarios_disponibles, name='horarios_disponibles'),
    path('cotizacion/<int:producto_id>/', solicitar_cotizacion, name='solicitar_cotizacion'),
    path('cotizacion/enviada/', cotizacion_enviada, name='cotizacion_enviada'),
    path('terminos/', terminos_condiciones, name='terminos'),
    path('privacidad/', politica_privacidad, name='privacidad'),
    
    # Admin Panel Routes
    path('admin-panel/login/', admin_login, name='admin_login'),
    path('admin-panel/logout/', admin_logout, name='admin_logout'),
    path('admin-panel/', admin_dashboard, name='admin_dashboard'),
    path('admin-panel/cotizaciones/', admin_cotizaciones_pendientes, name='admin_cotizaciones'),
    path('admin-panel/citas/', admin_citas_pendientes, name='admin_citas'),
    path('admin-panel/cotizacion/<int:cotizacion_id>/aprobar/', aprobar_cotizacion, name='aprobar_cotizacion'),
    path('admin-panel/cotizacion/<int:cotizacion_id>/rechazar/', rechazar_cotizacion, name='rechazar_cotizacion'),
    path('admin-panel/cotizacion/<int:cotizacion_id>/pdf/', preview_quote_pdf, name='preview_quote_pdf'),
    path('admin-panel/cita/<int:cita_id>/aprobar/', aprobar_cita, name='aprobar_cita'),
    path('admin-panel/cita/<int:cita_id>/rechazar/', rechazar_cita, name='rechazar_cita'),
    
    # Product Management Routes
    path('admin-panel/productos/', lista_productos, name='admin_lista_productos'),
    path('admin-panel/productos/crear/', crear_producto, name='admin_crear_producto'),
    path('admin-panel/productos/editar/<int:producto_id>/', editar_producto, name='admin_editar_producto'),
    path('admin-panel/productos/eliminar/<int:producto_id>/', eliminar_producto, name='admin_eliminar_producto'),
]

# Servir archivos media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Personalizar títulos del Admin
admin.site.site_header = "🪑 Muebles Barguay - Panel de Administración"
admin.site.site_title = "Muebles Barguay Admin"
admin.site.index_title = "Bienvenido al Panel de Gestión"
