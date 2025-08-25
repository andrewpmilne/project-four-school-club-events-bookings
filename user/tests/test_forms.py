from django.test import TestCase
from user.forms import SignupForm
from django.contrib.auth import get_user_model
from user.forms import EmailAuthenticationForm

User = get_user_model()


class SignupFormTests(TestCase):
    def test_parent_signup_form_creates_user(self):
        """SignupForm should create a parent user with valid data"""
        form_data = {
            'email': 'parent@example.com',
            'first_name': 'John',
            'surname': 'Doe',
            'role': 'parent',
            'password': 'StrongPass1!',
            'password_confirm': 'StrongPass1!',
        }
        form = SignupForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)

        user = form.save()
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(user.email, 'parent@example.com')
        self.assertTrue(user.check_password('StrongPass1!'))
        self.assertEqual(user.role, 'parent')

    def test_teacher_signup_form_creates_user(self):
        """SignupForm should create a teacher user
        with a valid .sch.uk email"""
        form_data = {
            'email': 'teacher@school.sch.uk',
            'first_name': 'Alice',
            'surname': 'Smith',
            'role': 'teacher',
            'password': 'StrongPass1!',
            'password_confirm': 'StrongPass1!',
        }
        form = SignupForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)

        user = form.save()
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(user.email, 'teacher@school.sch.uk')
        self.assertTrue(user.check_password('StrongPass1!'))
        self.assertEqual(user.role, 'teacher')


class LoginFormTests(TestCase):

    def test_login_form_valid_credentials(self):
        """Form should be valid if email and password match a user"""
        # Create a test user
        User.objects.create_user(
            email='testuser@example.com',
            password='TestPass123!',
            first_name='Test',
            surname='User',
            role='parent'
        )

        # Provide credentials to the login form
        form_data = {
            'username': 'testuser@example.com',
            'password': 'TestPass123!',
        }
        form = EmailAuthenticationForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)
