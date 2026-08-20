from django.urls import path
from . import views

app_name = "portail_admin"

urlpatterns = [
    path("", views.dashboard_validateur, name="dashboard_validateur"),
    path("super/", views.dashboard_superadmin, name="dashboard_superadmin"),
]
