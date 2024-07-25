from django.test import TestCase
from django.urls import reverse
from .models import Cliente, EstadoRegistro

class IntegrationTestCase(TestCase):

    def setUp(self):
        self.estado = EstadoRegistro.objects.create(estregnom='Activo')
        self.cliente_data = {
            'clidni': '87654321',
            'clinom': 'Ana',
            'cliape': 'García',
            'clitel': '987654321',
            'clidir': 'Avenida Siempreviva 742',
            'cliusu': 'anagarcia',
            'clicon': 'password',
            'clicor': 'ana@example.com',
            'clifecreg': '2023-07-20',
            'estregcod': self.estado.estregcod  # Utiliza estregcod en lugar de id
        }

    def test_form_submission(self):
        response = self.client.post(reverse('cliente_add'), self.cliente_data)
        self.assertEqual(response.status_code, 302)  # Redirección esperada

    def test_view_and_model_integration(self):
        response = self.client.post(reverse('cliente_add'), self.cliente_data)
        self.assertEqual(response.status_code, 302)
        # Verificar que el cliente fue creado
        cliente = Cliente.objects.get(clidni='87654321')
        self.assertEqual(cliente.clinom, 'Ana')
        self.assertEqual(cliente.cliape, 'García')

