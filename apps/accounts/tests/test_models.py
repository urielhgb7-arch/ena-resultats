from django.test import TestCase
from apps.accounts.models import UtilisateurAdmin


class UtilisateurAdminTest(TestCase):
    def test_create_user(self):
        user = UtilisateurAdmin.objects.create_user(
            username="testadmin", password="password123"
        )
        self.assertEqual(user.username, "testadmin")
        self.assertTrue(user.check_password("password123"))
