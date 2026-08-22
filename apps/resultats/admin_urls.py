from django.urls import path
from . import views

app_name = "resultats_admin"

urlpatterns = [
    path("list/", views.UEListView.as_view(), name="ue_list"),
    path("nouveau/", views.UECreateView.as_view(), name="ue_create"),
    path("<int:pk>/modifier/", views.UEUpdateView.as_view(), name="ue_update"),
    path("<int:pk>/supprimer/", views.UEDeleteView.as_view(), name="ue_delete"),
]
