from django.test import TestCase
from django.contrib.auth import get_user_model

UtilisateurAdmin = get_user_model()

class UtilisateurAdminTests(TestCase):
    def test_create_user_default_role(self):
        user = UtilisateurAdmin.objects.create_user(username="testuser", password="password123")
        self.assertEqual(user.role, UtilisateurAdmin.Role.VISITEUR)

    def test_create_superuser_role(self):
        admin_user = UtilisateurAdmin.objects.create_superuser(username="admin", password="password123")
        admin_user.role = UtilisateurAdmin.Role.SUPER_ADMIN
        admin_user.save()
        self.assertEqual(admin_user.role, UtilisateurAdmin.Role.SUPER_ADMIN)
        self.assertTrue(admin_user.is_superuser)
        self.assertTrue(admin_user.is_staff)
