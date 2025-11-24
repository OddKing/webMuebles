import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webMuebles.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Eliminar el usuario si ya existe
if User.objects.filter(username='admin').exists():
    User.objects.filter(username='admin').delete()
    print("Usuario 'admin' existente eliminado.")

# Crear el nuevo superusuario
User.objects.create_superuser(
    username='admin',
    email='admin@mueblesbarguay.cl',
    password='senior2025'
)

print("✓ Superusuario creado exitosamente!")
print("  Username: admin")
print("  Password: senior2025")
