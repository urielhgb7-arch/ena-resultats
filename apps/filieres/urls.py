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

    # AJAX Cascades
    path("ajax/niveaux/", views.ajax_niveaux, name="ajax_niveaux"),
    path("ajax/filieres/", views.ajax_filieres, name="ajax_filieres"),
    path("ajax/semestres/", views.ajax_semestres, name="ajax_semestres"),
    
    # --- ADMIN CBVs ---
    path("admin/list/", views.FiliereListView.as_view(), name="list"),
    path("admin/nouveau/", views.FiliereCreateView.as_view(), name="create"),
    path("admin/<int:pk>/modifier/", views.FiliereUpdateView.as_view(), name="update"),
    path("admin/<int:pk>/supprimer/", views.FiliereDeleteView.as_view(), name="delete"),
]
