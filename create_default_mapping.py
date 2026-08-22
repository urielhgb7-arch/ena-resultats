import os
import django
import json
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.imports.models import MappingTemplate

config = {
    "numero_col": 1,
    "matricule_col": 2,
    "nom_prenoms_col": 3,
    "auto_detect_ue": True,
    "ue_row": 1,
    "ec_row": 2,
    "data_start_row": 3
}

obj, created = MappingTemplate.objects.get_or_create(
    nom="PV ENA Standard (En-têtes fusionnés)",
    defaults={"config_colonnes": config}
)

if created:
    print(f"Modèle de mapping créé: {obj.nom}")
else:
    print(f"Le modèle existe déjà: {obj.nom}")
