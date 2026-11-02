from django.test import TestCase
from django.contrib.auth import get_user_model

class UtilisateurAdminTests(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(username="testuser", password="testpassword123")
        self.assertEqual(user.username, "testuser")
        self.assertTrue(user.check_password("testpassword123"))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
