from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a new user with a email entry is successful"""
        email = 'testuser@gmail.com'
        password = 'tempPassword123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized (lowercase)"""
        email = 'testuser@GMAIL'
        user = get_user_model().objects.create_user(email, 'testPw123')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test that creating user with no email raises error"""
        with self.assertRaises(ValueError):
            user = get_user_model().objects.create_user(None, 'testPw123')
