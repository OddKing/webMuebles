
import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR=os.path.join(BASE_DIR,'templates')
STATIC_DIR=os.path.join(BASE_DIR,'static')
STATIC_ROOT = '/root/django_proyectos/web/staticfiles'
# STATIC_ROOT for production - comment out for development
# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-uh!nw6(j5v7b8%q-!l21ramynuwtl72&x#1q7tr9b=(=_atnw%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'server.mueblesbarguay.cl']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'productos',
    'materiales',
    'cotizaciones',
    'clientes',
    'administracion'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'webMuebles.urls'



TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'webMuebles.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": 'web',
        "USER": "admin",
        "PASSWORD": "123momiaes",
        "HOST": "server.mueblesbarguay.cl", 
        "OPTIONS": {
            "charset": "utf8mb4",
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
        }
    }
}






# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'es'

from django.utils.translation import gettext_lazy as _

LANGUAGES = [
    ('es', _('Español')),
    ('en', _('English')),
    ('de', _('Deutsch')),
]

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]

TIME_ZONE = "America/Santiago"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS=[STATIC_DIR]

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ==============================================================================
# AUTENTICACIÓN
# ==============================================================================
LOGIN_URL = 'admin_login'  # Redirigir a panel de admin personalizado
LOGIN_REDIRECT_URL = 'admin_dashboard'
LOGOUT_REDIRECT_URL = 'admin_login'


# ==============================================================================
# EMAIL CONFIGURATION - Servidor Corporativo
# ==============================================================================
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# Configuracion del servidor SMTP (solicitar a tu proveedor de hosting)
EMAIL_HOST = 'mail.mueblesbarguay.cl'  
EMAIL_PORT = 465 
#EMAIL_USE_TLS = False  # Si es puerto 587
EMAIL_USE_SSL = True  # Si es puerto 465, descomentar y comentar EMAIL_USE_TLS

# Credenciales del email corporativo
EMAIL_HOST_USER = 'contacto@mueblesbarguay.cl'
EMAIL_HOST_PASSWORD = 'barguay.2025'  

# Email de envio
DEFAULT_FROM_EMAIL = 'Muebles Barguay <contacto@mueblesbarguay.cl>'
EMAIL_SUBJECT_PREFIX = '[Muebles Barguay] '

# Informacionde la empresa
COMPANY_NAME = 'Muebles Barguay'
COMPANY_ADDRESS = 'Av Lo Espejo 964, El Bosque, Santiago'
COMPANY_PHONE = '+569 1234 5678'  # TODO: Actualizar con telefono real
COMPANY_EMAIL = 'contacto@mueblesbarguay.cl'

# ==============================================================================
# MEDIA FILES CONFIGURATION - Archivos subidos por usuarios
# ==============================================================================
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'