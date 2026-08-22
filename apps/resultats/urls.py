from django.urls import path
from . import views

app_name = "resultats"

urlpatterns = [
    path("ue/<int:ue_id>/", views.detail_ue, name="ue_detail"),
    path("ue/<int:ue_id>/classement/", views.detail_ue, name="ue_classement"),
    path("session/<int:session_id>/tableau/", views.tableau_complet_session, name="ue_tableau_complet"),
    path("recherche/", views.recherche_personnelle, name="recherche_personnelle"),
    path("recherche/avancee/", views.recherche_avancee, name="recherche_avancee"),
    path("contact/", views.contact_signalement, name="contact"),
]
