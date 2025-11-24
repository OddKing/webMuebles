from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Crea el usuario administrador para el panel de administración'

    def handle(self, *args, **options):
        username = 'adminbarguay'
        password = 'barguay.2025'
        email = 'admin@mueblesbarguay.com'
        
        # Verificar si el usuario ya existe
        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(f'El usuario "{username}" ya existe.')
            )
            return
        
        # Crear el usuario administrador
        user = User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )
        
        self.stdout.write(
            self.style.SUCCESS(f'Usuario administrador "{username}" creado exitosamente.')
        )
        self.stdout.write(
            self.style.SUCCESS(f'Email: {email}')
        )
        self.stdout.write(
            self.style.SUCCESS(f'Contraseña: {password}')
        )
