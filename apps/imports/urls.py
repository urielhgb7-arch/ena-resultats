from django.urls import path
from . import views

app_name = "imports"

urlpatterns = [
    path("", views.ImportFichierListView.as_view(), name="list"),
    path("nouveau/", views.ImportFichierCreateView.as_view(), name="create"),
    path("<int:pk>/", views.ImportFichierDetailView.as_view(), name="detail"),
    path("<int:pk>/supprimer/", views.ImportFichierDeleteView.as_view(), name="delete"),
]
