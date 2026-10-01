from django.test import TestCase
from django.contrib.auth import get_user_model

class UtilisateurAdminTests(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            email='test@example.com',
            nom='Test User',
            role='visiteur',
            password='testpassword123'
        )
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.nom, 'Test User')
        self.assertEqual(user.role, 'visiteur')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_admin)

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(
            email='super@example.com',
            nom='Super Admin',
            role='super_admin',
            password='superpassword123'
        )
        self.assertEqual(admin_user.email, 'super@example.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_admin)
        self.assertTrue(admin_user.is_staff)
