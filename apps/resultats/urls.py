from django.urls import path
from . import views

app_name = "resultats"

urlpatterns = [
    path("ue/<int:ue_id>/", views.detail_ue, name="ue_detail"),
]
