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
from productos.views import catalogo
from cotizaciones.views import agendar_reunion, get_horarios_disponibles

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', portada, name='vista_base'),
    path('catalogo/', catalogo, name='catalogo'),
    path('agendar/', agendar_reunion, name='agendar_reunion'),
    path('api/horarios-disponibles/', get_horarios_disponibles, name='horarios_disponibles'),
    path('terminos/', terminos_condiciones, name='terminos'),
    path('privacidad/', politica_privacidad, name='privacidad'),
]

# Servir archivos media en desarrollo
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Personalizar títulos del Admin
admin.site.site_header = "🪑 Muebles Barguay - Panel de Administración"
admin.site.site_title = "Muebles Barguay Admin"
admin.site.index_title = "Bienvenido al Panel de Gestión"

