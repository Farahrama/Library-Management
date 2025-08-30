from django.test import TestCase
from django.urls import reverse

class SmokeTest(TestCase):
    def test_homepage_runs(self):
        response = self.client.get("/")
        self.assertIn(response.status_code, [200, 404])