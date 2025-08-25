from django.test import TestCase
from django.urls import reverse
from user.models import User


class SignupViewTests(TestCase):

    def test_signup_parent_success(self):
        """
        POST with valid parent data should create
        user and redirect to login
        """
        url = reverse('user:signup')
        data = {
            'email': 'parent@example.com',
            'first_name': 'John',
            'surname': 'Doe',
            'role': 'parent',
            'password': 'StrongPass1!',
            'password_confirm': 'StrongPass1!',
        }
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse('user:login'))
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.first().role, 'parent')

    def test_signup_teacher_invalid_email(self):
        """POST with teacher using wrong email domain shows error"""
        url = reverse('user:signup')
        data = {
            'email': 'teacher@gmail.com',
            'first_name': 'Alice',
            'surname': 'Smith',
            'role': 'teacher',
            'password': 'StrongPass1!',
            'password_confirm': 'StrongPass1!',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Teachers must sign up with an email")
        self.assertEqual(User.objects.count(), 0)
