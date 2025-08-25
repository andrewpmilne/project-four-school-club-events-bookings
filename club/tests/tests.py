from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from datetime import date, time, timedelta
from club.models import Club

User = get_user_model()


class ClubViewsTest(TestCase):
    def setUp(self):
        # Create a teacher user
        self.teacher = User.objects.create_user(
            first_name='Teacher',
            surname='One',
            email='teacher1@example.com',
            password='pass123',
            role='teacher'
        )

        # Client for making requests
        self.client = Client()
        self.client.login(email='teacher1@example.com', password='pass123')

        # Valid club data
        self.valid_club_data = {
            'name': 'Chess Club',
            'club_or_event': 'club',
            'description': 'Fun chess activities',
            'min_age': 8,
            'max_age': 15,
            'capacity': 10,
            'start_time': '15:00',
            'end_time': '16:00',
            'start_date': date.today() + timedelta(days=1),
            'end_date': date.today() + timedelta(days=1),
            'frequency': 'one-off',
        }

    def test_create_club_get(self):
        """
        GET request to create_club should render the form template.
        """
        response = self.client.get(reverse('club:create_club'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'club/create_club.html')

    def test_create_club_post_valid(self):
        """
        POST request with valid data should create a club and redirect.
        """
        response = self.client.post(
            reverse('club:create_club'),
            data=self.valid_club_data
            )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Club.objects.filter(name='Chess Club').exists())

    def test_create_club_post_invalid(self):
        """
        POST request with invalid data (min_age > max_age) should show error.
        """
        data = self.valid_club_data.copy()
        data['min_age'] = 16
        data['max_age'] = 12
        response = self.client.post(reverse('club:create_club'), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            'Maximum age must be greater than or equal to minimum age.'
            )
        self.assertFalse(Club.objects.filter(name='Chess Club').exists())

    def test_list_teacher_clubs(self):
        """
        Teacher should see only their clubs.
        """
        Club.objects.create(
            name='My Club',
            teacher=self.teacher,
            club_or_event='club',
            description='Test',
            min_age=8,
            max_age=15,
            capacity=10,
            start_time=time(15, 0),
            end_time=time(16, 0),
            start_date=date.today(),
            end_date=date.today(),
            frequency='one-off'
        )
        response = self.client.get(reverse('club:list_teacher_clubs'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'My Club')
