from django.test import TestCase
from rest_framework.test import APITestCase
from django.urls import reverse


# Create your tests here.
class UserRegistrationAPIViewTestCase(APITestCase):
    def test_registration(self):
        url = reverse("user_view")
        user_data = {
            "nickname": "testuser",
            "user_id": "tester",
            "email": "test@testuser.com",
            "password": "password",
        }
        response = self.client.post(url, user_data)
        self.assertEqual(response.status_code, 201)
