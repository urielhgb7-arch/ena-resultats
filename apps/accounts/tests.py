from django.test import TestCase
from .models import UtilisateurAdmin

class UtilisateurAdminTest(TestCase):
    def test_create_user(self):
        user = UtilisateurAdmin.objects.create_user(
            email='test@example.com', nom='Test User', role='visiteur', password='testpassword'
        )
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.nom, 'Test User')
        self.assertEqual(user.role, 'visiteur')
        self.assertTrue(user.check_password('testpassword'))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        admin = UtilisateurAdmin.objects.create_superuser(
            email='admin@example.com', nom='Admin User', password='adminpassword'
        )
        self.assertEqual(admin.email, 'admin@example.com')
        self.assertEqual(admin.nom, 'Admin User')
        self.assertEqual(admin.role, 'super_admin')
        self.assertTrue(admin.check_password('adminpassword'))
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)
