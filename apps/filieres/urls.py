from django.urls import path
from . import views

app_name = "filieres"

urlpatterns = [
    path("", views.accueil, name="accueil"),
    path("annee/<int:annee_id>/", views.liste_niveaux, name="niveaux"),
    path("niveau/<int:niveau_id>/", views.liste_filieres, name="filieres"),
    path("filiere/<int:filiere_id>/specialites/", views.liste_specialites, name="specialites"),
    path("filiere/<int:filiere_id>/semestres/", views.liste_semestres, name="semestres"),
    path(
        "filiere/<int:filiere_id>/specialite/<int:specialite_id>/semestres/",
        views.liste_semestres,
        name="semestres_avec_specialite",
    ),
    path("semestre/<int:semestre_id>/sessions/", views.liste_sessions, name="sessions"),
    path("session/<int:session_id>/ue/", views.liste_ue, name="ue_liste"),
]
