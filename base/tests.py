from django.test import TestCase

from bs4 import BeautifulSoup
from django.urls import reverse
from django.conf import settings



class TestCore1(TestCase):

    def test_index(self):
        response = self.client.get(reverse("landingpage"))
        self.assertEqual(response.status_code, 200)
