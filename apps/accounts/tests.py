from django.test import TestCase
from django.contrib.auth import get_user_model

class UtilisateurAdminModelTests(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(email="test@example.com", nom="Test User", role="visiteur", password="password")
        self.assertEqual(user.email, "test@example.com")
        self.assertEqual(user.nom, "Test User")
        self.assertEqual(user.role, "visiteur")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(email="super@example.com", nom="Super User", password="password")
        self.assertEqual(admin_user.email, "super@example.com")
        self.assertEqual(admin_user.nom, "Super User")
        self.assertEqual(admin_user.role, "super_admin")
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)

    def test_email_required(self):
        User = get_user_model()
        with self.assertRaises(ValueError):
            User.objects.create_user(email="", nom="Test", role="visiteur", password="password")
