# 🔒 Security Policy - Muebles Barguay

## Configuración de Seguridad

Este documento describe las prácticas de seguridad implementadas y las mejores prácticas para mantener el sistema seguro.

## 🔐 Variables de Entorno

### Configuración para Repositorio Privado

Este proyecto mantiene el archivo `.env` en el repositorio por conveniencia, dado que es un repositorio **privado**. Sin embargo, se deben seguir estas pautas:

> [!WARNING]
> **Nunca hagas el repositorio público** sin antes eliminar el archivo `.env` y todo su historial de Git.

> [!IMPORTANT]
> **Para producción**: Crea un archivo `.env.production` con credenciales diferentes y más seguras. Este archivo SÍ está en `.gitignore`.

### Estrategia de Archivos de Entorno

- **`.env`** - Desarrollo/Staging (rastreado en git)
- **`.env.local`** - Sobrescrituras locales (ignorado)
- **`.env.production`** - Producción real (ignorado, nunca commitear)

### Archivo .env Requerido

Crea un archivo `.env` en la raíz del proyecto con las siguientes variables:

```env
# Django Core
SECRET_KEY=<clave-secreta-unica>
DEBUG=False  # SIEMPRE False en producción
ALLOWED_HOSTS=tudominio.com,www.tudominio.com

# Base de Datos
DB_ENGINE=django.db.backends.mysql
DB_NAME=nombre_bd
DB_USER=usuario_bd
DB_PASSWORD=contraseña_segura
DB_HOST=localhost
DB_PORT=3306

# Email SMTP
EMAIL_HOST=smtp.tuservidor.com
EMAIL_PORT=465
EMAIL_USE_SSL=True
EMAIL_HOST_USER=correo@empresa.com
EMAIL_HOST_PASSWORD=contraseña_email
DEFAULT_FROM_EMAIL=Empresa <correo@empresa.com>

# Información de la Empresa
COMPANY_NAME=Nombre Empresa
COMPANY_EMAIL=contacto@empresa.com
COMPANY_PHONE=+56 9 XXXX XXXX
COMPANY_ADDRESS=Dirección completa
```

### Generar SECRET_KEY Segura

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## 🛡️ Medidas de Seguridad Implementadas

### 1. Protección de Credenciales
- ✅ Todas las credenciales en variables de entorno
- ✅ Archivo `.env` en `.gitignore`
- ✅ Plantilla `.env.example` sin valores reales

### 2. HTTPS y Cookies Seguras (Producción)
```python
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

### 3. Headers de Seguridad
```python
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000
```

### 4. Validación de Contraseñas
- Similitud con atributos del usuario
- Longitud mínima
- Contraseñas comunes bloqueadas
- Contraseñas numéricas bloqueadas

### 5. Protección CSRF
- Tokens CSRF en todos los formularios
- Validación automática de Django

### 6. Consentimiento Legal
- Registro de IP y User Agent
- Versionado de términos y políticas
- Cumplimiento con Ley 19.628 (Chile)

## ⚠️ Checklist de Seguridad para Producción

### Antes del Deployment

- [ ] **Cambiar `DEBUG=False`** en `.env`
- [ ] **Generar nueva `SECRET_KEY`** única para producción
- [ ] **Configurar `ALLOWED_HOSTS`** con dominios reales
- [ ] **Usar HTTPS** (certificado SSL válido)
- [ ] **Passwords robustas** para base de datos y email
- [ ] **Limitar acceso SSH** al servidor
- [ ] **Firewall configurado** (solo puertos necesarios)
- [ ] **Backups automatizados** de base de datos
- [ ] **Logs centralizados** y monitoreados
- [ ] **Actualizar dependencias** a versiones seguras

### Configuración del Servidor

```bash
# Verificar configuración de seguridad
python manage.py check --deploy

# Debe retornar sin warnings en producción
```

### Permisos de Archivos

```bash
# Archivos de configuración
chmod 600 .env

# Directorio media (si contiene datos sensibles)
chmod 750 media/

# Archivos de código
chmod 644 *.py
```

## 🔍 Auditoría de Seguridad

### Revisar Logs Regularmente

```bash
# Logs de Django
tail -f logs/django.log

# Logs de acceso
tail -f logs/access.log
```

### Búsqueda de Credenciales Expuestas

```bash
# Verificar que no hay credenciales en Git
git log --all --full-history --source -- *password* *secret* *.env

# Resultado esperado: vacío
```

### Actualización de Dependencias

```bash
# Listar paquetes desactualizados
pip list --outdated

# Actualizar paquetes de seguridad
pip install --upgrade django
pip install --upgrade mysqlclient
```

## 🚨 Reporte de Vulnerabilidades

Si encuentras una vulnerabilidad de seguridad, por favor:

1. **NO** abras un issue público
2. Envía un email a: seguridad@mueblesbarguay.cl
3. Incluye:
   - Descripción detallada de la vulnerabilidad
   - Pasos para reproducirla
   - Impacto potencial
   - Sugerencias de mitigación (opcional)

## 📋 Rotación de Credenciales

### Cambio de SECRET_KEY

```bash
# 1. Generar nueva clave
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# 2. Actualizar .env
SECRET_KEY=nueva_clave_generada

# 3. Reiniciar aplicación
# Nota: Invalidará todas las sesiones activas
```

### Cambio de Password de Base de Datos

```sql
-- MySQL
ALTER USER 'usuario'@'localhost' IDENTIFIED BY 'nueva_contraseña_segura';
FLUSH PRIVILEGES;
```

Luego actualizar `.env`:
```env
DB_PASSWORD=nueva_contraseña_segura
```

## 🔐 Mejores Prácticas

### 1. Contraseñas
- Mínimo 16 caracteres
- Combinar mayúsculas, minúsculas, números y símbolos
- Usar gestor de contraseñas (1Password, LastPass, Bitwarden)
- No reutilizar contraseñas

### 2. Acceso SSH
```bash
# Usar keys SSH en lugar de contraseñas
ssh-keygen -t ed25519 -C "tu_email@ejemplo.com"

# Deshabilitar login por contraseña
# En /etc/ssh/sshd_config:
# PasswordAuthentication no
```

### 3. Base de Datos
- Usuario específico con privilegios limitados
- No usar root para la aplicación
- Conexiones desde localhost o VPN
- Encriptar conexiones (SSL/TLS)

### 4. Backups
- Backups diarios automatizados
- Almacenamiento encriptado
- Probar restauración regularmente
- Retención de 30 días mínimo

### 5. Monitoring
- Configurar alertas de errores (Sentry)
- Monitorear intentos de acceso fallidos
- Alertas de uso anormal de recursos
- Logs de auditoría

## 📚 Recursos Adicionales

- [Django Security](https://docs.djangoproject.com/en/stable/topics/security/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Mozilla Web Security](https://infosec.mozilla.org/guidelines/web_security)

## 📅 Historial de Seguridad

### 2025-11-26
- ✅ Migración a variables de entorno
- ✅ Implementación de headers de seguridad
- ✅ Actualización de .gitignore
- ✅ Documentación de seguridad creada

---

**Última actualización:** 26 de Noviembre de 2025
