"""
Test for models
"""
from django.test import TestCase
from django.contrib.auth import get_user_model

class ModelTests(TestCase):
    """ test models."""

    def test_create_user_with_email_successful(self):
        """ test creating user with email successful"""
        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        "Test user with normalized email"
        sample_emails = [
            ['test1@EXAMPLE.com','test1@example.com'],
            ['Test2@example.com','Test2@example.com'],
            ['TEST3@EXAMPLE.COM','TEST3@example.com'],
            ['test4@example.COM','test4@example.com']
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email, expected)

    def test_new_user_witout_email_raises_error(self):
        """ Test creating a user without email is raises Valuerror"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test123')

    def test_create_superuser(self):
        """ Test creating a superuser"""
        user = get_user_model().objects.create_superuser(
            'admin@example.com',
            'test123'
        )
        self.assertTrue(user.is_superuser)