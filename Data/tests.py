from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class DataRanking(TestCase):

    def test_empty_database(self):
        """
        Tests if pages are being rendered
        """

        response = self.client.get(reverse('ranking'))
        self.assertEqual(response.status_code, 200)

    def test_populated_database(self):
        """
        Test the page response with a populated database
        """
        pass


class DataHome(TestCase):

    def test_reponse(self):
        """
       Tests if pages are being rendered
       """

        response = self.client.get(reverse('home page'))
        self.assertEqual(response.status_code, 200)
