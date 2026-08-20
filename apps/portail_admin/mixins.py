from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

class AdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Mixin pour les Class-Based Views limitant l'accès aux utilisateurs Staff.
    """
    def test_func(self):
        return self.request.user.is_staff
