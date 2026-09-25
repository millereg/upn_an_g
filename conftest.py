import os

import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventario_upn_g.settings')

def pytest_configure():
    django.setup()
