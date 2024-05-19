import os
import django
from django.conf import settings
from ferremas.ferremas import settings  # Asume que my_settings es tu archivo de configuración de Django

os.environ['DJANGO_SETTINGS_MODULE'] = 'ferremas.settings'
django.setup()

# Ahora puedes importar de Django y rest_framework
from rest_framework import viewsets, permissions, status
from views import get_dolar_data

import unittest
from views import get_dolar_data

class TestMyFunctions(unittest.TestCase):
    def test_get_dolar_data(self):
        dolar_value = get_dolar_data()
        # Aquí puedes poner una aserción que tenga sentido para tu caso.
        # Por ejemplo, si sabes que el valor del dólar siempre debe ser mayor que 0, puedes hacer:
        self.assertTrue(dolar_value > 0)

if __name__ == '__main__':
    unittest.main()
