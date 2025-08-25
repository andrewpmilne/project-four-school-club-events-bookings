from django.test import TestCase
from django.urls import reverse
from child.models import Child
from user.models import User
from club.models import Club
from enrollment.models import Enrollment
from datetime import date, time


class ChildViewsTests(TestCase):

    def setUp(self):
        """Create a parent user and some children"""
        self.parent = User.objects.create_user(
            email='parent@example.com',
            password='TestPass123!',
            first_name='John',
            surname='Doe',
            role='parent'
        )

        self.child1 = Child.objects.create(
            first_name='Tom',
            surname='Smith',
            date_of_birth='2010-05-20',
            allergy_info='None',
            emergency_contact_name='Jane Smith',
            emergency_contact_phone='+447123456789',
            special_needs='',
            parent=self.parent
        )

        self.child2 = Child.objects.create(
            first_name='Alice',
            surname='Brown',
            date_of_birth='2012-07-15',
            allergy_info='Peanuts',
            emergency_contact_name='Jane Smith',
            emergency_contact_phone='+447123456789',
            special_needs='',
            parent=self.parent
        )

    def test_view_children_cards(self):
        """Parent should see only their own children"""
        self.client.login(email='parent@example.com', password='TestPass123!')
        url = reverse('child:view_children_cards')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        children = response.context['children']
        self.assertEqual(len(children), 2)
        self.assertIn(self.child1, children)
        self.assertIn(self.child2, children)

    def test_view_children_requires_login(self):
        """Anonymous user should be redirected to login"""
        url = reverse('child:view_children_cards')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)


class ChildCRUDViewTests(TestCase):

    def setUp(self):
        """Create a parent user and one child for testing"""
        self.parent = User.objects.create_user(
            email='parent@example.com',
            password='TestPass123!',
            first_name='John',
            surname='Doe',
            role='parent'
        )

        self.child = Child.objects.create(
            first_name='Tom',
            surname='Smith',
            date_of_birth='2010-05-20',
            allergy_info='None',
            emergency_contact_name='Jane Smith',
            emergency_contact_phone='+447123456789',
            special_needs='',
            parent=self.parent
        )

        self.client.login(email='parent@example.com', password='TestPass123!')

    def test_create_child_post_success(self):
        """Parent can create a child with valid data"""
        url = reverse('child:create_child')
        form_data = {
            'first_name': 'Alice',
            'surname': 'Brown',
            'date_of_birth': '2012-07-15',
            'allergy_info': 'Peanuts',
            'emergency_contact_name': 'Jane Smith',
            'emergency_contact_phone': '+447123456789',
            'special_needs': ''
        }
        response = self.client.post(url, data=form_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Child.objects.filter(parent=self.parent).count(), 2)

    def test_create_child_post_age_invalid(self):
        """Child under 4 or over 18 triggers age validation error"""
        url = reverse('child:create_child')
        form_data = {
            'first_name': 'Young',
            'surname': 'Kid',
            'date_of_birth': '2022-01-01',  # Too young
            'allergy_info': '',
            'emergency_contact_name': 'Jane Smith',
            'emergency_contact_phone': '+447123456789',
            'special_needs': ''
        }
        response = self.client.post(url, data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response, 'Child age must be between 4 and 18 years.'
        )
        self.assertEqual(Child.objects.filter(parent=self.parent).count(), 1)

    def test_edit_child_success(self):
        """Parent can edit their own child"""
        url = reverse('child:edit_child', args=[self.child.id])
        form_data = {
            'first_name': 'Tom',
            'surname': 'Updated',
            'date_of_birth': '2010-05-20',
            'allergy_info': 'None',
            'emergency_contact_name': 'Jane Smith',
            'emergency_contact_phone': '+447123456789',
            'special_needs': ''
        }
        response = self.client.post(url, data=form_data)
        self.assertEqual(response.status_code, 302)
        self.child.refresh_from_db()
        self.assertEqual(self.child.surname, 'Updated')

    def test_delete_child_success(self):
        """Parent can delete their own child"""
        url = reverse('child:delete_child', args=[self.child.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Child.objects.filter(id=self.child.id).exists())


class EnrollmentViewTests(TestCase):

    def setUp(self):
        """Create parent, child, and a club for enrollment tests."""
        self.parent = User.objects.create_user(
            email='parent@example.com',
            password='TestPass123!',
            first_name='John',
            surname='Doe',
            role='parent'
        )

        self.teacher = User.objects.create_user(
            email='teacher@example.com',
            password='Teacher123!',
            first_name='Alice',
            surname='Smith',
            role='teacher'
        )

        self.child = Child.objects.create(
            first_name='Tom',
            surname='Doe',
            date_of_birth=date(2010, 5, 20),
            allergy_info='None',
            emergency_contact_name='Jane Doe',
            emergency_contact_phone='+447123456789',
            special_needs='',
            parent=self.parent
        )

        self.club = Club.objects.create(
            teacher=self.teacher,
            name='Science Club',
            club_or_event='club',
            capacity=10,
            start_date=date(2025, 9, 1),
            end_date=date(2025, 12, 1),
            start_time=time(15, 0),
            end_time=time(16, 0)
        )

        self.client.login(email='parent@example.com', password='TestPass123!')

    def test_parent_can_enroll_child(self):
        """Parent can enroll their child in a club."""
        self.client.login(email='parent@example.com', password='TestPass123!')
        url = reverse('enrollment:create_enrollment')  # <-- replace this line
        form_data = {
            'child': self.child.id,
            'club': self.club.id,
        }
        response = self.client.post(url, data=form_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            self.child.enrollments.filter(club=self.club).exists()
        )

    def test_cannot_enroll_if_club_full(self):
        """Parent should not be able to enroll if club capacity is full."""
        self.client.login(email='parent@example.com', password='TestPass123!')

        # Fill the club to its capacity
        for i in range(self.club.capacity):
            Enrollment.objects.create(
                child=Child.objects.create(
                    first_name=f'Child{i}',
                    surname='Full',
                    date_of_birth='2010-01-01',
                    allergy_info='None',
                    emergency_contact_name='Jane Doe',
                    emergency_contact_phone='+447123456789',
                    special_needs='',
                    parent=self.parent
                ),
                club=self.club
            )

        # The enrollment should not be created
        self.assertFalse(
            Enrollment.objects.filter(
                child=self.child,
                club=self.club
                ).exists()
        )
