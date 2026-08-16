from django.urls import path
from . import views

app_name = "imports"

urlpatterns = [
    path("upload/", views.upload_fichier, name="upload"),
    path("apercu/<int:import_id>/", views.apercu_import, name="apercu"),
]
