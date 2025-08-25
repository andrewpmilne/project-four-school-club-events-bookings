from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from datetime import date, time, timedelta
from club.models import Club
from child.models import Child
from enrollment.models import Enrollment

User = get_user_model()


class EnrollmentViewsTest(TestCase):
    def setUp(self):
        # Parent and Teacher users
        self.parent = User.objects.create_user(
            first_name='Parent',
            surname='One',
            email='parent@example.com',
            password='pass123',
            role='parent'
        )
        self.teacher = User.objects.create_user(
            first_name='Teacher',
            surname='One',
            email='teacher@example.com',
            password='pass123',
            role='teacher'
        )

        # Child
        self.child = Child.objects.create(
            first_name='Child',
            surname='One',
            date_of_birth=date.today() - timedelta(days=8*365),  # 8 years old
            parent=self.parent
        )

        # Club
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

    def test_create_enrollment_view(self):
        """
        POSTing valid data should create an enrollment.
        """
        self.client.force_login(self.parent)
        url = reverse('enrollment:create_enrollment')
        response = self.client.post(
            url,
            {'child': self.child.id, 'club': self.club.id}
            )
        self.assertRedirects(response, reverse('user:parent_dashboard'))
        self.assertEqual(Enrollment.objects.count(), 1)
        self.assertEqual(Enrollment.objects.first().child, self.child)

    def test_create_enrollment_with_club_view(self):
        """
        POSTing valid data with pre-selected club should create an enrollment.
        """
        self.client.force_login(self.parent)
        url = reverse(
            'enrollment:create_enrollment_with_club',
            args=[self.club.id]
            )
        response = self.client.post(
            url,
            {'child': self.child.id,
             'club': self.club.id}
             )
        self.assertRedirects(response, reverse('user:parent_dashboard'))
        self.assertEqual(Enrollment.objects.count(), 1)

    def test_cancel_enrollment_view(self):
        """
        POSTing to cancel enrollment should remove it.
        """
        enrollment = Enrollment.objects.create(
            child=self.child,
            club=self.club
            )
        self.client.force_login(self.parent)
        url = reverse('enrollment:cancel_enrollment', args=[enrollment.id])
        response = self.client.post(url)
        self.assertRedirects(
            response,
            reverse(
                'enrollment:cancel_enrollment_page'
                ))
        self.assertEqual(Enrollment.objects.count(), 0)

    def test_cancel_enrollment_page_view(self):
        """
        Page should show all enrollments for parent's children.
        """
        Enrollment.objects.create(child=self.child, club=self.club)
        self.client.force_login(self.parent)
        url = reverse('enrollment:cancel_enrollment_page')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.child.first_name)
        self.assertContains(response, self.club.name)
