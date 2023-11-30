from django.test import TestCase
from django.test import Client
from .models import Cart, CartItem
from django.urls import reverse


# --- TEST VIEWS --- #
class MyViewTests(TestCase):
    
    def setUp(self):
        self.client = Client()

    def test_view_response(self):
        client = Client()
        response = client.get(reverse('cart'))
        self.assertEqual(response.status_code, 200)        
        

# -- TEST MODELS --- #
class MyModelTests(TestCase):

    def test_model_creation(self):
        obj = Cart.objects.create(name='Test')
        self.assertEqual(Cart.objects.count(), 1)
        self.assertEqual(obj.name, 'Test')
