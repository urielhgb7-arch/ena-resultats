from django.test import TestCase
from django.contrib.auth import get_user_model


class UtilisateurAdminTest(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            email="test@example.com",
            nom="Test User",
            role="validateur",
            password="testpassword123",
        )
        self.assertEqual(user.email, "test@example.com")
        self.assertEqual(user.nom, "Test User")
        self.assertEqual(user.role, "validateur")
        self.assertTrue(user.check_password("testpassword123"))
