from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

class AdminSiteTests(TestCase):

    def setup(self):
        """Create test client, add new user for testing, login user"""
        self.client = Client() # Setup Task 1
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@fakedomain.com',
            password='password123'
        ) # Setup Task 2
        self.client.force_login(self.admin_user) # Steup Task 3
        self.user = get_user_model.objects.create_user(
            email='test@fakedomain.com',
            password='password123',
            name='Test user full name'
        ) # Setup Task 4

    def test_users_listed(self):
        """Test that users are listed on user page"""
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)