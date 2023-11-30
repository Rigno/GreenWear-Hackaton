from django.test import TestCase
from django.test import Client
from django.urls import reverse


# --- TEST VIEWS --- #
class MyViewTests(TestCase):
    
    def setUp(self):
        self.client = Client()

    def test_view_response(self):
        client = Client()
        views_to_test = ['product']
        for view_name in views_to_test:
            with self.subTest(view_name=view_name):
                response = client.get(reverse(view_name))
                self.assertEqual(response.status_code, 200)
