from django.test import TestCase
from club.forms import ClubForm
from club.models import Club
from django.contrib.auth import get_user_model
from datetime import date, time, timedelta

User = get_user_model()


class ClubFormTest(TestCase):
    def setUp(self):
        # Create a teacher user
        self.teacher = User.objects.create_user(
            first_name='teacher1',
            surname='teacher1',
            email='teacher@school.sch.uk',
            password='pass123',
            role='teacher'
        )

    def test_club_can_be_created(self):
        """
        Should create an instance of a Club when the form is valid.
        """
        data = {
            'name': 'Chess Club',
            'club_or_event': 'club',
            'description': 'Fun chess activities',
            'min_age': 8,
            'max_age': 15,
            'capacity': 10,
            'start_time': time(15, 0),
            'end_time': time(16, 0),
            'start_date': date.today(),
            'end_date': date.today(),
            'frequency': 'one-off',
        }

        form = ClubForm(data=data)
        self.assertTrue(form.is_valid(), form.errors)

        # Save the form and check the club exists in DB
        club = form.save(commit=False)
        club.teacher = self.teacher
        club.save()

        self.assertEqual(Club.objects.count(), 1)
        self.assertEqual(Club.objects.first().name, 'Chess Club')

    def test_club_invalid_age_range(self):
        """
        Should raise a validation error if min_age is greater than max_age.
        """
        data = {
            'name': 'Science Club',
            'club_or_event': 'club',
            'description': 'Fun science experiments',
            'min_age': 16,  # intentionally higher than max_age
            'max_age': 12,
            'capacity': 10,
            'start_time': time(15, 0),
            'end_time': time(16, 0),
            'start_date': date.today(),
            'end_date': date.today(),
            'frequency': 'one-off',
        }

        form = ClubForm(data=data)

        # Form should be invalid
        self.assertFalse(form.is_valid())

        # Check that the error is on max_age
        self.assertIn('max_age', form.errors)
        self.assertEqual(
            form.errors['max_age'][0],
            'Maximum age must be greater than or equal to minimum age.'
        )

    def test_club_start_date_in_past(self):
        """
        Should raise a validation error if start_date is in the past.
        """
        past_date = date.today() - timedelta(days=1)  # yesterday

        data = {
            'name': 'History Club',
            'club_or_event': 'club',
            'description': 'Learn history',
            'min_age': 8,
            'max_age': 15,
            'capacity': 10,
            'start_time': time(15, 0),
            'end_time': time(16, 0),
            'start_date': past_date,
            'end_date': past_date,
            'frequency': 'one-off',
        }

        form = ClubForm(data=data)

        # Form should be invalid
        self.assertFalse(form.is_valid())

        # Check that the error is on start_date
        self.assertIn('start_date', form.errors)
        self.assertEqual(
            form.errors['start_date'][0],
            'Start date cannot be in the past.'
        )
