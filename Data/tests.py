from django.contrib.auth import get_user_model
from django.test import Client
from django.test import TestCase
from django.test.client import RequestFactory
from django.urls import reverse

User = get_user_model()


class DataViewTest(TestCase):

    def test_responses(self):
        """
        Tests if pages are being rendered
        """

        response = self.client.get(reverse('home page'))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('ranking'))
        self.assertEqual(response.status_code, 200)
