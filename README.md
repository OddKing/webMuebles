# 🪑 Muebles Barguay - Sistema de Gestión Web

Sistema web completo para la gestión de una empresa de muebles personalizados, desarrollado con Django.

## 📋 Características

### Funcionalidades Principales
- ✅ **Catálogo de Productos** - Galería visual de muebles con gestión desde el panel de administración
- ✅ **Sistema de Cotizaciones** - Solicitud y gestión de cotizaciones personalizadas
- ✅ **Agendamiento de Citas** - Sistema de reserva de reuniones (presenciales y online)
- ✅ **Gestión de Clientes** - CRM básico con historial de cotizaciones y descuentos
- ✅ **Panel de Administración** - Interfaz personalizada para gestión del negocio
- ✅ **Multi-idioma** - Soporte para Español, Inglés y Alemán
- ✅ **Generación de PDFs** - Cotizaciones profesionales en PDF
- ✅ **Scraper de Precios** - Búsqueda automática de precios de materiales
- ✅ **Consentimiento Legal** - Cumplimiento con ISO 27701 y Ley 19.628 de Chile
- ✅ **Notificaciones Email** - Envío automatizado de confirmaciones y cotizaciones

### Aplicaciones Django
- `productos` - Gestión del catálogo de productos
- `materiales` - Administración de materiales de construcción
- `cotizaciones` - Sistema de cotizaciones y citas
- `clientes` - Gestión de clientes y CRM
- `administracion` - Panel de control administrativo

## 🚀 Instalación y Configuración

### Requisitos Previos
- Python 3.10+
- MySQL 8.0+
- pip (gestor de paquetes de Python)

### Paso 1: Clonar el Repositorio
```bash
git clone https://github.com/tu-usuario/webMuebles.git
cd webMuebles
```

### Paso 2: Crear Entorno Virtual
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Paso 3: Instalar Dependencias
```bash
pip install -r requirements.txt
```

### Paso 4: Configurar Variables de Entorno

**Para desarrollo:** El archivo `.env` ya viene incluido en el repositorio con credenciales de desarrollo.

**Para producción:**

1. **Crea un archivo `.env.production`** con credenciales más seguras:
   ```bash
   cp .env .env.production
   ```

2. **Edita `.env.production`** y cambia todas las credenciales:
   ```env
   # Producción - Usar credenciales diferentes
   SECRET_KEY=nueva-clave-secreta-generada
   DEBUG=False
   ALLOWED_HOSTS=tudominio.com,www.tudominio.com
   DB_PASSWORD=contraseña_produccion_muy_segura
   EMAIL_HOST_PASSWORD=contraseña_email_produccion
   ```

3. **En el servidor, renombra el archivo:**
   ```bash
   mv .env.production .env
   ```

> [!WARNING]
> **Repositorio Privado**: El archivo `.env` se incluye en Git por conveniencia. NUNCA hagas este repositorio público sin antes eliminar `.env` del historial.

4. **Generar SECRET_KEY única para producción:**
   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

### Paso 5: Configurar Base de Datos

1. **Crear base de datos MySQL:**
   ```sql
   CREATE DATABASE web CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

2. **Ejecutar migraciones:**
   ```bash
   python manage.py migrate
   ```

3. **Crear superusuario:**
   ```bash
   python manage.py createsuperuser
   ```

### Paso 6: Recopilar Archivos Estáticos
```bash
python manage.py collectstatic
```

### Paso 7: Ejecutar el Servidor de Desarrollo
```bash
python manage.py runserver
```

Accede a: [http://127.0.0.1:8000](http://127.0.0.1:8000)

## 🔐 Configuración de Seguridad

### Variables de Entorno Requeridas

| Variable | Descripción | Ejemplo |
|----------|-------------|---------|
| `SECRET_KEY` | Clave secreta de Django | `django-insecure-...` |
| `DEBUG` | Modo debug (False en producción) | `False` |
| `ALLOWED_HOSTS` | Hosts permitidos | `example.com,www.example.com` |
| `DB_NAME` | Nombre de la base de datos | `web` |
| `DB_USER` | Usuario de la base de datos | `admin` |
| `DB_PASSWORD` | Contraseña de la base de datos | `********` |
| `DB_HOST` | Host de la base de datos | `localhost` |
| `EMAIL_HOST` | Servidor SMTP | `smtp.gmail.com` |
| `EMAIL_HOST_USER` | Usuario de email | `contacto@empresa.com` |
| `EMAIL_HOST_PASSWORD` | Contraseña de email | `********` |

### ⚠️ IMPORTANTE - Producción

Antes de desplegar a producción, asegúrate de:

- [ ] Establecer `DEBUG=False` en `.env`
- [ ] Configurar `ALLOWED_HOSTS` con tu dominio real
- [ ] Usar una `SECRET_KEY` fuerte y única
- [ ] Habilitar HTTPS (el proyecto ya tiene configuración SSL)
- [ ] Configurar correctamente el servidor de base de datos
- [ ] Revisar permisos de archivos media
- [ ] Configurar backups automatizados

## 📁 Estructura del Proyecto

```
webMuebles/
├── administracion/      # App de administración
├── clientes/           # App de gestión de clientes
├── cotizaciones/       # App de cotizaciones y citas
├── materiales/         # App de materiales
├── productos/          # App de productos
├── static/             # Archivos estáticos (CSS, JS, imágenes)
├── templates/          # Templates HTML
├── webMuebles/         # Configuración principal del proyecto
│   ├── settings.py     # Configuración (usando variables de entorno)
│   ├── urls.py         # URLs principales
│   └── wsgi.py         # WSGI config
├── .env                # Variables de entorno (NO COMMITEAR)
├── .env.example        # Plantilla de variables de entorno
├── .gitignore          # Archivos ignorados por Git
├── manage.py           # Utilidad de gestión de Django
└── requirements.txt    # Dependencias de Python
```

## 🛠️ Panel de Administración

### Acceso
- **URL Admin Django:** [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
- **Panel Personalizado:** [http://127.0.0.1:8000/admin-panel/](http://127.0.0.1:8000/admin-panel/)

### Funcionalidades del Panel
- Gestión de cotizaciones pendientes
- Aprobación/rechazo de citas
- Administración de productos
- Gestión de clientes
- Búsqueda de precios de materiales
- Generación de PDFs

## 📧 Configuración de Email

El proyecto soporta diferentes backends de email:

### Gmail (ejemplo)
```env
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_USE_SSL=False
EMAIL_HOST_USER=tu_email@gmail.com
EMAIL_HOST_PASSWORD=tu_app_password
```

### Servidor SMTP Corporativo
```env
EMAIL_HOST=mail.tuempresa.cl
EMAIL_PORT=465
EMAIL_USE_SSL=True
EMAIL_USE_TLS=False
EMAIL_HOST_USER=contacto@tuempresa.cl
EMAIL_HOST_PASSWORD=tu_contraseña
```

## 🌐 Internacionalización

El proyecto soporta múltiples idiomas:
- 🇪🇸 Español (predeterminado)
- 🇬🇧 Inglés
- 🇩🇪 Alemán

Para agregar traducciones:
```bash
python manage.py makemessages -l es
python manage.py compilemessages
```

## 🧪 Testing

```bash
# Ejecutar todos los tests
python manage.py test

# Test de una app específica
python manage.py test cotizaciones

# Con coverage
coverage run --source='.' manage.py test
coverage report
```

## 📝 Comandos Útiles

```bash
# Crear nueva migración
python manage.py makemigrations

# Ver SQL de migración
python manage.py sqlmigrate app_name 0001

# Verificar problemas
python manage.py check

# Verificar deployment
python manage.py check --deploy

# Limpiar sesiones expiradas
python manage.py clearsessions
```

## 🔒 Seguridad

Este proyecto implementa las siguientes medidas de seguridad:

- ✅ Variables de entorno para credenciales sensibles
- ✅ HTTPS forzado en producción
- ✅ Cookies seguras (Secure, HttpOnly)
- ✅ Protección CSRF
- ✅ Headers de seguridad (XSS, Content-Type-Sniffing)
- ✅ HSTS (HTTP Strict Transport Security)
- ✅ Validación de contraseñas robusta
- ✅ Registro de consentimiento legal (GDPR compatible)

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto es privado y propietario de Muebles Barguay.

## 📞 Soporte

Para soporte técnico, contacta a:
- **Email:** contacto@mueblesbarguay.cl
- **Teléfono:** +569 1234 5678
- **Dirección:** Av Lo Espejo 964, El Bosque, Santiago

---

**Desarrollado con ❤️ para Muebles Barguay**
