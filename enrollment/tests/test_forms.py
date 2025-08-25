from django.test import TestCase
from django.contrib.auth import get_user_model
from datetime import date, time, timedelta
from enrollment.forms import EnrollmentForm
from enrollment.models import Enrollment
from child.models import Child
from club.models import Club

User = get_user_model()


class EnrollmentFormTest(TestCase):
    def setUp(self):
        # Create a parent user
        self.parent = User.objects.create_user(
            first_name='Parent',
            surname='One',
            email='parent1@example.com',
            password='pass123',
            role='parent'
        )

        # Create a child
        self.child = Child.objects.create(
            first_name='Child',
            surname='One',
            date_of_birth=date.today() - timedelta(days=8*365),  # 8 years old
            parent=self.parent
        )

        # Create a teacher user
        self.teacher = User.objects.create_user(
            first_name='Teacher',
            surname='One',
            email='teacher1@example.com',
            password='pass123',
            role='teacher'
        )

        # Create a club
        self.club = Club.objects.create(
            teacher=self.teacher,
            name='Chess Club',
            club_or_event='club',
            description='Fun chess',
            min_age=6,
            max_age=12,
            capacity=2,
            start_time=time(15, 0),
            end_time=time(16, 0),
            start_date=date.today() + timedelta(days=1),
            end_date=date.today() + timedelta(days=1),
            frequency='one-off'
        )

    def test_valid_enrollment_form(self):
        """
        Should create an enrollment if child
        meets age requirements and club has space.
        """
        form = EnrollmentForm(
            data={'child': self.child.id,
                  'club': self.club.id}
                  )
        self.assertTrue(form.is_valid())
        enrollment = form.save()
        self.assertEqual(enrollment.child, self.child)
        self.assertEqual(enrollment.club, self.club)

    def test_child_too_young(self):
        """
        Should raise a validation error if child is below min_age.
        """
        # Make child 5 years old
        self.child.date_of_birth = date.today() - timedelta(days=5*365)
        self.child.save()
        form = EnrollmentForm(
            data={'child': self.child.id,
                  'club': self.club.id}
                  )
        self.assertFalse(form.is_valid())
        self.assertIn('is too young', str(form.errors))

    def test_child_already_enrolled(self):
        """
        Should raise a validation error
        if child is already enrolled in the same club.
        """
        Enrollment.objects.create(child=self.child, club=self.club)
        form = EnrollmentForm(
            data={'child': self.child.id,
                  'club': self.club.id}
                  )
        self.assertFalse(form.is_valid())
        self.assertIn('already enrolled', str(form.errors))

    def test_club_capacity_full(self):
        """
        Should raise a validation error if club has reached max capacity.
        """
        # Fill the club
        another_child = Child.objects.create(
            first_name='Child2',
            surname='Two',
            date_of_birth=date.today() - timedelta(days=8*365),
            parent=self.parent
        )
        Enrollment.objects.create(child=self.child, club=self.club)
        Enrollment.objects.create(child=another_child, club=self.club)

        # Try enrolling a new child
        third_child = Child.objects.create(
            first_name='Child3',
            surname='Three',
            date_of_birth=date.today() - timedelta(days=8*365),
            parent=self.parent
        )
        form = EnrollmentForm(
            data={'child': third_child.id,
                  'club': self.club.id}
                  )
        self.assertFalse(form.is_valid())
        self.assertIn('has reached its maximum capacity', str(form.errors))

    def test_time_conflict(self):
        """
        Should raise a validation error
        if child is enrolled in overlapping club.
        """
        # Existing overlapping club
        overlapping_club = Club.objects.create(
            teacher=self.teacher,
            name='Overlapping Club',
            club_or_event='club',
            description='Overlap test',
            min_age=6,
            max_age=12,
            capacity=5,
            start_time=time(15, 30),  # overlaps 15:00-16:00
            end_time=time(16, 30),
            start_date=date.today() + timedelta(days=1),
            end_date=date.today() + timedelta(days=1),
            frequency='one-off'
        )
        Enrollment.objects.create(child=self.child, club=self.club)

        form = EnrollmentForm(
            data={'child': self.child.id,
                  'club': overlapping_club.id}
                  )
        self.assertFalse(form.is_valid())
        self.assertIn('overlaps with', str(form.errors))
