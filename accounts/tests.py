from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from accounts.forms import SignUpForm, LoginForm

User = get_user_model()


class TestLoginView(TestCase):
    def setUp(self) -> None:
        self.url = reverse("accounts:login")
        self.user = User.objects.create_user(username="test", password="test")

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context["form"], LoginForm)
        self.assertTemplateUsed(response, "accounts/login.html")

    def test_post(self):
        response = self.client.post(self.url, {"username": "test", "password": "test"})
        self.assertRedirects(response, reverse("books:home"))
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_post_invalid(self):
        response = self.client.post(self.url, {"username": "test", "password": "wrong"})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        self.assertTemplateUsed(response, "accounts/login.html")
        self.assertIsInstance(response.context["form"], LoginForm)

    def test_post_invalid_form(self):
        response = self.client.post(self.url, {"username": "test"})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        self.assertTemplateUsed(response, "accounts/login.html")
        self.assertIsInstance(response.context["form"], LoginForm)
        self.assertFormError(response, "form", "password", "This field is required.")


class TestSignUpView(TestCase):
    def setUp(self) -> None:
        self.url = reverse("accounts:signup")
        self.valid_data = {
            "username": "test",
            "password": "test1234",
            "password2": "test1234",
            "email": "test@gmail.com",
        }

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context["form"], SignUpForm)
        self.assertTemplateUsed(response, "accounts/signup.html")

    def test_post(self):
        self.assertEqual(User.objects.count(), 0)
        response = self.client.post(
            self.url,
            self.valid_data,
        )
        self.assertRedirects(response, reverse("books:home"))
        self.assertEqual(User.objects.count(), 1)
        user = User.objects.first()
        self.assertEqual(user.username, self.valid_data["username"])
        self.assertTrue(user.check_password(self.valid_data["password"]))
        self.assertTrue(user.is_authenticated)
        response = self.client.post(
            self.url,
            self.valid_data,
        )
        self.assertFormError(response, "form", "username", "Username already exists")


    def test_post_invalid(self):
        response = self.client.post(
            self.url,
            {
                **self.valid_data,
                "password2": "wrong",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        self.assertTemplateUsed(response, "accounts/signup.html")
        self.assertIsInstance(response.context["form"], SignUpForm)
        self.assertFormError(response, "form", "password2", "Passwords do not match")

    def test_post_invalid_form(self):
        response = self.client.post(
            self.url,
            {
                **self.valid_data,
                "username": "",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        self.assertTemplateUsed(response, "accounts/signup.html")
        self.assertIsInstance(response.context["form"], SignUpForm)
        self.assertFormError(response, "form", "username", "This field is required.")

    def test_post_invalid_email(self):
        response = self.client.post(
            self.url,
            {
                **self.valid_data,
                "email": "test",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        self.assertTemplateUsed(response, "accounts/signup.html")
        self.assertIsInstance(response.context["form"], SignUpForm)
        self.assertFormError(response, "form", "email", "Enter a valid email address.")

    def test_post_invalid_password(self):
        response = self.client.post(
            self.url,
            {
                **self.valid_data,
                "password": "test",
                "password2": "test",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        self.assertTemplateUsed(response, "accounts/signup.html")
        self.assertIsInstance(response.context["form"], SignUpForm)
        self.assertFormError(response, "form", "password", "Password must be at least 8 characters")
