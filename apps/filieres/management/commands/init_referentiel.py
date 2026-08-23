import logging
from django.core.management.base import BaseCommand
from django.db import transaction
from apps.filieres.models import AnneeAcademique, Niveau, Filiere, Specialite, Semestre

class Command(BaseCommand):
    help = "Initialise le référentiel académique officiel (Niveaux, Filières, Spécialités, Semestres)"

    def add_arguments(self, parser):
        parser.add_argument(
            '--annee',
            type=str,
            default="2024-2025",
            help='Libellé de l\'année académique (ex: 2024-2025)'
        )

    def handle(self, *args, **options):
        annee_libelle = options['annee']
        
        with transaction.atomic():
            annee, created = AnneeAcademique.objects.get_or_create(
                libelle=annee_libelle,
                defaults={"active": True}
            )
            
            if created:
                self.stdout.write(self.style.SUCCESS(f"Année académique '{annee_libelle}' créée."))
            else:
                self.stdout.write(f"Utilisation de l'année académique existante : '{annee_libelle}'.")

            # Définition des niveaux
            niveaux_def = {
                "L1": ["Semestre 1", "Semestre 2"],
                "L2": ["Semestre 3", "Semestre 4"],
                "L3": ["Semestre 5", "Semestre 6"]
            }

            # Définition des filières et spécialités
            filieres_def = [
                {
                    "nom": "Administration des Finances",
                    "specialites": [
                        "Administration des Impôts",
                        "Administration des Finances et du Trésor",
                        "Gestion des Marchés Publics",
                        "Administration Hospitalière Universitaire et Intendance"
                    ],
                    "specialite_unique_auto": False
                },
                {
                    "nom": "Administration Générale",
                    "specialites": [
                        "Administration Territoriale et de Sécurité Sociale",
                        "Diplomatie et Relations Internationales",
                        "AGT"
                    ],
                    "specialite_unique_auto": False
                },
                {
                    "nom": "Sciences Techniques et d'Information Documentaire",
                    "specialites": [
                        "Archivistique, Bibliothéconomie et Documentation (BIDOC)"
                    ],
                    "specialite_unique_auto": True
                },
                {
                    "nom": "Secrétariat de Gestion",
                    "specialites": [],
                    "specialite_unique_auto": False
                }
            ]

            for niv_libelle, semestres in niveaux_def.items():
                niveau, _ = Niveau.objects.get_or_create(annee=annee, libelle=niv_libelle)
                
                for f_def in filieres_def:
                    # En L1, aucune filière n'a de spécialité (tronc commun)
                    # Sauf pour Secrétariat de gestion qui n'a de spécialité nulle part.
                    a_des_specialites = (niv_libelle in ["L2", "L3"]) and (len(f_def["specialites"]) > 0)
                    
                    filiere, _ = Filiere.objects.get_or_create(
                        niveau=niveau,
                        nom=f_def["nom"],
                        defaults={
                            "a_des_specialites": a_des_specialites,
                            "specialite_unique_auto": f_def["specialite_unique_auto"] if a_des_specialites else False
                        }
                    )
                    
                    # Mise à jour si la filière existe déjà mais qu'on veut s'assurer des flags
                    if not _:
                        filiere.a_des_specialites = a_des_specialites
                        filiere.specialite_unique_auto = f_def["specialite_unique_auto"] if a_des_specialites else False
                        filiere.save()

                    # Création des spécialités (uniquement pour L2/L3 si pertinent)
                    if a_des_specialites:
                        for spec_nom in f_def["specialites"]:
                            Specialite.objects.get_or_create(filiere=filiere, nom=spec_nom)

                    # Création des semestres pour cette filière
                    for sem_libelle in semestres:
                        # S6 = stage (L3)
                        sem_type = "stage" if sem_libelle == "Semestre 6" else "normal"
                        
                        Semestre.objects.get_or_create(
                            filiere=filiere,
                            libelle=sem_libelle,
                            defaults={"type": sem_type}
                        )

            self.stdout.write(self.style.SUCCESS(f"Référentiel académique intégré avec succès pour {annee_libelle} !"))
