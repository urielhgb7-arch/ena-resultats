from django.urls import path
from . import views

app_name = "filieres_admin"

urlpatterns = [
    path("list/", views.FiliereListView.as_view(), name="list"),
    path("nouveau/", views.FiliereCreateView.as_view(), name="create"),
    path("<int:pk>/modifier/", views.FiliereUpdateView.as_view(), name="update"),
    path("<int:pk>/supprimer/", views.FiliereDeleteView.as_view(), name="delete"),
]
