# ⚠️ NOTA IMPORTANTE SOBRE CREDENCIALES

## Configuración Actual

Este proyecto **incluye el archivo `.env` en el repositorio Git** por las siguientes razones:

1. ✅ El repositorio es **privado**
2. ✅ Simplifica el deployment en el servidor
3. ✅ No requiere configuración manual después de clonar

## 🔒 Precauciones de Seguridad

### ⚠️ NUNCA hagas este repositorio público

Si en algún momento necesitas hacer público este repositorio:

1. **Elimina `.env` del historial de Git:**
   ```bash
   # Usar BFG Repo-Cleaner o git filter-branch
   git filter-branch --force --index-filter \
     "git rm --cached --ignore-unmatch .env" \
     --prune-empty --tag-name-filter cat -- --all
   ```

2. **Agrega `.env` a `.gitignore`:**
   ```bash
   echo ".env" >> .gitignore
   git add .gitignore
   git commit -m "Add .env to gitignore"
   ```

3. **Force push (¡cuidado!):**
   ```bash
   git push origin --force --all
   ```

### 🎯 Mejores Prácticas para Producción

Aunque `.env` está en el repo, **SIEMPRE** usa credenciales diferentes para producción:

#### Desarrollo (en `.env` del repo)
```env
DB_PASSWORD=123momiaes          # ⚠️ Contraseña débil, solo para dev
DEBUG=True                       # OK para desarrollo
SECRET_KEY=django-insecure-...   # Clave de desarrollo
```

#### Producción (crear `.env.production` localmente)
```env
DB_PASSWORD=Gk#9mP@xL2$vN8qR   # ✅ Contraseña fuerte
DEBUG=False                      # ✅ SIEMPRE False en producción  
SECRET_KEY=nuevo-secreto-generado # ✅ Clave única de producción
```

## 🚀 Workflow Recomendado

### Para Desarrollo Local
1. Clona el repositorio
2. El `.env` ya está incluido
3. Ejecuta `python manage.py runserver`

### Para Deployment en Servidor
1. Clona el repositorio en el servidor
2. Crea `.env.production` con credenciales seguras
3. Renombra: `mv .env.production .env`
4. O sobrescribe: `cp .env.production .env`

### Alternativa: Variables de Entorno del Sistema

En producción, también puedes usar variables de entorno del sistema en lugar de `.env`:

```bash
# En el servidor (Linux)
export SECRET_KEY="nueva-clave-secreta"
export DEBUG="False"
export DB_PASSWORD="contraseña-segura"

# Ejecutar Django
python manage.py runserver
```

## 📋 Checklist de Seguridad

Antes de deployment a producción:

- [ ] Crear `.env.production` con credenciales diferentes
- [ ] Cambiar `DEBUG=False`
- [ ] Generar nueva `SECRET_KEY`
- [ ] Usar contraseñas fuertes (16+ caracteres)
- [ ] Configurar `ALLOWED_HOSTS` correctamente
- [ ] Verificar que el repositorio siga siendo privado
- [ ] Configurar backups de credenciales
- [ ] Documentar las credenciales en un gestor seguro (1Password, LastPass, etc.)

## 🔐 Gestión de Contraseñas

**Recomendación:** Usa un gestor de contraseñas para almacenar:
- SECRET_KEY de producción
- Contraseñas de base de datos
- Credenciales de email
- Claves SSH

Gestores recomendados:
- 1Password (empresarial)
- Bitwarden (código abierto)
- LastPass
- KeePassXC (offline)

## 📞 En Caso de Exposición

Si accidentalmente expones credenciales:

1. **Inmediato:** Cambia todas las contraseñas expuestas
2. **Revoca keys:** Genera nuevas SECRET_KEY
3. **Audita logs:** Verifica accesos sospechosos
4. **Notifica:** Informa al equipo
5. **Limpia historial:** Elimina credenciales del historial de Git

---

**Última actualización:** 26 de Noviembre de 2025
