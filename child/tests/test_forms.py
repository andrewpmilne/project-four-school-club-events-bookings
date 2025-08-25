from django.test import TestCase
from child.forms import ChildForm
from child.models import Child
from user.models import User


class ChildFormTests(TestCase):

    def test_parent_can_create_child(self):
        """ChildForm should create a child instance with a parent assigned"""
        # Create a parent user
        parent = User.objects.create_user(
            email='parent@example.com',
            password='TestPass123!',
            first_name='John',
            surname='Doe',
            role='parent'
        )

        form_data = {
            'first_name': 'Bukayo',
            'surname': 'Saka',
            'date_of_birth': '2010-05-20',
            'allergy_info': 'None',
            'emergency_contact_name': 'Mikel Arteta',
            'emergency_contact_phone': '+447123456789',
            'special_needs': '',
        }
        form = ChildForm(data=form_data)

        self.assertTrue(form.is_valid(), form.errors)

        child = form.save(commit=False)
        child.parent = parent
        child.save()

        self.assertEqual(Child.objects.count(), 1)
        self.assertEqual(child.first_name, 'Bukayo')
        self.assertEqual(child.surname, 'Saka')
        self.assertEqual(child.parent, parent)


class ChildFormValidationTests(TestCase):

    def setUp(self):
        """Create a parent user for assigning to children"""
        self.parent = User.objects.create_user(
            email='parent@example.com',
            password='TestPass123!',
            first_name='John',
            surname='Doe',
            role='parent'
        )

        # Create an existing child for duplicate tests
        self.existing_child = Child.objects.create(
            first_name='Tom',
            surname='Smith',
            date_of_birth='2010-05-20',
            allergy_info='None',
            emergency_contact_name='Jane Smith',
            emergency_contact_phone='+447123456789',
            special_needs='',
            parent=self.parent
        )

    def test_duplicate_child(self):
        """Form should be invalid if child with same details exists"""
        form_data = {
            'first_name': 'Tom',
            'surname': 'Smith',
            'date_of_birth': '2010-05-20',
            'allergy_info': 'None',
            'emergency_contact_name': 'Jane Smith',
            'emergency_contact_phone': '+447123456789',
            'special_needs': '',
        }
        form = ChildForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('__all__', form.errors)
        self.assertIn('already registered', form.errors['__all__'][0])

    def test_missing_required_fields(self):
        """Form should be invalid if required fields are missing"""
        form_data = {
            'first_name': '',
            'surname': 'Smith',
            'date_of_birth': '',
            'allergy_info': 'None',
            'emergency_contact_name': '',
            'emergency_contact_phone': '',
            'special_needs': '',
        }
        form = ChildForm(data=form_data)
        self.assertFalse(form.is_valid())
        required_fields = [
            'first_name',
            'date_of_birth',
            'emergency_contact_name',
            'emergency_contact_phone'
        ]
        for field in required_fields:
            self.assertIn(field, form.errors)
            self.assertIn('This field is required.', form.errors[field])
