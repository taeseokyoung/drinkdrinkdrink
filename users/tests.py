from django.urls import reverse
from rest_framework.test import APITestCase
from .models import User


class SignupUserTest(APITestCase):
    def test_registration_success(self):
        url = reverse("sign_up_view")
        user_data = {
            "user_id": "success_test",
            "password": "1234",
            "password_check": "1234",
            "email": "test@test.com",
            "age": "20",
        }
        response = self.client.post(url, user_data)
        self.assertEqual(response.status_code, 201)

    def test_registration_fail(self):
        url = reverse("sign_up_view")
        user_data = {
            "user_id": "fail_test",
            "password": "1234",
            "password_check": "asdf",
            "email": "test@test.com",
            "age": "20",
        }
        response = self.client.post(url, user_data)
        self.assertEqual(response.status_code, 400)


class LoginUserTest(APITestCase):
    def setUp(self):
        self.admin_data = {
            "user_id": "admin_login_test",
            "password": "1234",
        }
        self.admin_user = User.objects.create_superuser(
            "admin_login_test", "1234", "admin@test.com"
        )
        self.admin_put_data = {"password": "1234", "nickname": "put_admin"}
        self.user = User.objects.create_user(
            user_id="fail_test",
            password="1234",
            email="fail_test@test.com",
            age=20,
        )
        self.user_data = {"user_id": "fail_test", "password": "1234"}

    def test_admin_login(self):
        response = self.client.post(reverse("token_obtain_pair"), self.admin_data)
        self.assertEqual(response.status_code, 200)

    # 일반 유저는 이메일 인증 후 로그인 가능
    def test_user_login(self):
        response = self.client.post(reverse("token_obtain_pair"), self.user_data)
        self.assertEqual(response.status_code, 401)

    def test_get_user(self):
        access_token = self.client.post(
            reverse("token_obtain_pair"), self.admin_data
        ).data["access"]
        response = self.client.get(
            # arg=[self.admin_user.id]유저 id확인
            path=reverse("profile_view", args=[self.admin_user.id]),
            HTTP_AUTHRIZATION=f"Bearer {access_token}",
        )
        self.assertEqual(response.status_code, 200)

    def test_put_user(self):
        access_token = self.client.post(
            reverse("token_obtain_pair"), self.admin_data
        ).data["access"]
        response = self.client.put(
            path=reverse("profile_view", args=[self.admin_user.id]),
            HTTP_AUTHRIZATION=f"Bearer {access_token}",
            data=self.admin_put_data,
        )
        self.assertEqual(response.status_code, 200)

    def test_put_user_fail(self):
        access_token = self.client.post(
            reverse("token_obtain_pair"), self.admin_data
        ).data["access"]
        response = self.client.put(
            path=reverse("profile_view", args=[self.admin_user.id + 1]),
            HTTP_AUTHRIZATION=f"Bearer {access_token}",
            data=self.admin_put_data,
        )
        self.assertEqual(response.status_code, 400)

    def test_delete_user(self):
        access_token = self.client.post(
            reverse("token_obtain_pair"), self.admin_data
        ).data["access"]
        response = self.client.delete(
            path=reverse("profile_view", args=[self.admin_user.id]),
            HTTP_AUTHRIZATION=f"Bearer {access_token}",
        )
        self.assertEqual(response.status_code, 200)

    def test_delete_user_fail(self):
        access_token = self.client.post(
            reverse("token_obtain_pair"), self.admin_data
        ).data["access"]
        response = self.client.delete(
            path=reverse("profile_view", args=[self.admin_user.id + 1]),
            HTTP_AUTHRIZATION=f"Bearer {access_token}",
        )
        self.assertEqual(response.status_code, 400)
