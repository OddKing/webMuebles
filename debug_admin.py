import os
import sys
import django
from django.conf import settings
from django.test import RequestFactory
from django.contrib.auth.models import User, AnonymousUser

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webMuebles.settings')
django.setup()

from cotizaciones.views_admin import admin_dashboard

def test_admin_dashboard():
    factory = RequestFactory()
    request = factory.get('/admin-panel/')
    
    # Create a superuser for testing
    try:
        user = User.objects.get(username='admin_test')
    except User.DoesNotExist:
        user = User.objects.create_superuser('admin_test', 'admin@example.com', 'password')
        
    request.user = user
    
    try:
        response = admin_dashboard(request)
        print(f"Status Code: {response.status_code}")
        print("Content preview:", response.content[:200])
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_admin_dashboard()
