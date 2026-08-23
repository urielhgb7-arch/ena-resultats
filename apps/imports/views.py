from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, DeleteView
from django.views import View
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.shortcuts import redirect

from apps.portail_admin.mixins import AdminRequiredMixin
from .models import ImportFichier
from .forms import ImportFichierForm
from .services import extraire_lignes_brutes


class ImportFichierListView(AdminRequiredMixin, ListView):
    model = ImportFichier
    template_name = "imports/import_list.html"
    context_object_name = "imports"
    paginate_by = 20

    def get_queryset(self):
        qs = super().get_queryset()
        statut = self.request.GET.get("statut")
        if statut:
            qs = qs.filter(statut=statut)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["statut_actuel"] = self.request.GET.get("statut", "")
        return context


class ImportFichierCreateView(AdminRequiredMixin, CreateView):
    model = ImportFichier
    form_class = ImportFichierForm
    template_name = "imports/import_form.html"

    def form_valid(self, form):
        import hashlib
        
        fichier = self.request.FILES["fichier"]
        file_hash = hashlib.sha256()
        for chunk in fichier.chunks():
            file_hash.update(chunk)
        hash_hex = file_hash.hexdigest()
        
        if ImportFichier.objects.filter(fichier_hash=hash_hex).exists():
            form.add_error('fichier', "Ce fichier (même empreinte numérique) a déjà été importé.")
            return super().form_invalid(form)
            
        fichier.seek(0)
        
        form.instance.utilisateur = self.request.user
        form.instance.nom_fichier = fichier.name
        form.instance.fichier_hash = hash_hex
        
        response = super().form_valid(form)
        
        # Extraire les lignes brutes
        try:
            lignes = extraire_lignes_brutes(self.object.fichier.path, self.object)
            messages.success(
                self.request, f"{len(lignes)} lignes détectées et prêtes pour le mapping."
            )
        except Exception as e:
            messages.error(self.request, f"Erreur lors de la lecture du fichier : {e}")
            self.object.statut = "annule"
            self.object.save()
            
        return response

    def get_success_url(self):
        return reverse_lazy("imports:detail", kwargs={"pk": self.object.pk})


class ImportFichierDetailView(AdminRequiredMixin, DetailView):
    model = ImportFichier
    template_name = "imports/import_detail.html"
    context_object_name = "import_fichier"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Limiter à 50 pour l'aperçu
        lignes = self.object.lignes.all()
        context["lignes"] = lignes[:50]
        context["has_unresolved"] = any(
            ligne.donnees_brutes.get("match_filiere", {}).get("statut") == "a_valider"
            for ligne in lignes
        )
        return context


class ImportFichierDeleteView(AdminRequiredMixin, DeleteView):
    model = ImportFichier
    template_name = "imports/import_confirm_delete.html"
    success_url = reverse_lazy("imports:list")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "L'import a été supprimé avec succès.")
        return super().delete(request, *args, **kwargs)


from django.db import transaction
from apps.resultats.models import Etudiant, UE, EC, ResultatUE, NoteEC

class ValiderImportView(AdminRequiredMixin, View):
    def post(self, request, pk):
        import_fichier = get_object_or_404(ImportFichier, pk=pk)
        
        if import_fichier.statut != 'en_attente':
            messages.error(request, "Cet import ne peut plus être validé.")
            return redirect("imports:detail", pk=pk)
            
        try:
            with transaction.atomic():
                is_global = import_fichier.type_import == "global"
                
                if not is_global:
                    session_resultat = import_fichier.session
                    if not session_resultat:
                        raise Exception("Aucune session n'est associée à cet import spécifique.")
                else:
                    if not import_fichier.annee_academique or not import_fichier.semestre:
                        raise Exception("L'année académique et le semestre sont obligatoires pour un import global.")
                
                # Check for mapping (for now we assume extraction produced standard JSON)
                if not import_fichier.mapping:
                    raise Exception("Aucun modèle de mapping n'a été sélectionné.")
                
                lignes_en_erreur = 0
                for ligne in import_fichier.lignes.all():
                    donnees = ligne.donnees_brutes
                    matricule = donnees.get("matricule")
                    nom_prenoms = donnees.get("nom_prenoms", "")
                    
                    if not matricule:
                        ligne.statut_traitement = 'erreur'
                        ligne.message_erreur = "Matricule manquant"
                        ligne.save()
                        lignes_en_erreur += 1
                        continue
                        
                    etudiant, _ = Etudiant.objects.get_or_create(
                        matricule=matricule,
                        defaults={"nom": nom_prenoms.split(' ')[0], "prenom": " ".join(nom_prenoms.split(' ')[1:])}
                    )
                    
                    resultats_ue = donnees.get("resultats_par_ue", {})
                    ligne_has_error = False
                    
                    for ue_code, dict_notes in resultats_ue.items():
                        # Scoping UE par (code, session)
                        if is_global:
                            # 1. Obtenir la filière matchée
                            match_info = donnees.get("match_filiere", {})
                            if match_info.get("statut") != "auto":
                                ligne.statut_traitement = 'erreur'
                                ligne.message_erreur = f"Filière non reconnue: {match_info.get('entree')}"
                                ligne_has_error = True
                                break
                            
                            candidat_filiere = match_info.get("candidat")
                            
                            # 2. Chercher l'UE dans l'année académique et semestre pour cette filière
                            ue = UE.objects.filter(
                                code=ue_code,
                                session__semestre__libelle=import_fichier.semestre,
                                session__semestre__filiere__nom=candidat_filiere,
                                session__semestre__filiere__niveau__annee=import_fichier.annee_academique
                            ).first()
                            
                            if not ue:
                                ligne.statut_traitement = 'erreur'
                                ligne.message_erreur = f"UE {ue_code} introuvable pour la filière {candidat_filiere} ({import_fichier.semestre})"
                                ligne_has_error = True
                                break
                        else:
                            ue, _ = UE.objects.get_or_create(
                                code=ue_code,
                                session=session_resultat,
                                defaults={"nom": f"UE {ue_code}", "credits": 30, "statut": "brouillon"}
                            )
                        
                        moy_ue = dict_notes.get("Moy UE")
                        est_validee = dict_notes.get("R") == "V"
                        
                        try:
                            moy_ue_val = float(moy_ue) if moy_ue is not None else None
                            if moy_ue_val is not None and not (0 <= moy_ue_val <= 20):
                                raise ValueError(f"Moyenne UE invalide: {moy_ue_val}")
                        except ValueError as e:
                            ligne.statut_traitement = 'erreur'
                            ligne.message_erreur = str(e)
                            ligne.save()
                            ligne_has_error = True
                            lignes_en_erreur += 1
                            break
                            
                        resultat_ue, _ = ResultatUE.objects.get_or_create(
                            etudiant=etudiant,
                            ue=ue,
                            defaults={"moyenne_ue": moy_ue_val, "statut": "V" if est_validee else "NV", "import_fichier": import_fichier}
                        )
                        
                        # Traitement des ECs
                        for ec_key, ec_val in dict_notes.items():
                            if ec_key in ["Moy UE", "R"]:
                                continue
                                
                            try:
                                note_val = float(ec_val) if ec_val is not None else None
                                if note_val is not None and not (0 <= note_val <= 20):
                                    raise ValueError(f"Note EC {ec_key} invalide: {note_val}")
                            except ValueError as e:
                                ligne.statut_traitement = 'erreur'
                                ligne.message_erreur = str(e)
                                ligne.save()
                                ligne_has_error = True
                                lignes_en_erreur += 1
                                break
                            
                            ec, _ = EC.objects.get_or_create(
                                code=ec_key,
                                ue=ue,
                                defaults={"nom": f"EC {ec_key}", "coefficient": 1}
                            )
                            NoteEC.objects.get_or_create(
                                resultat_ue=resultat_ue,
                                ec=ec,
                                defaults={"valeur": note_val}
                            )
                    
                    if not ligne_has_error:
                        ligne.statut_traitement = 'traitee'
                        ligne.message_erreur = ""
                        ligne.save()
                
                if lignes_en_erreur > 0:
                    raise Exception(f"{lignes_en_erreur} ligne(s) comportent des erreurs (ex: notes hors 0-20). Veuillez corriger le fichier.")
                
                import_fichier.statut = 'valide'
                import_fichier.save()
                
                messages.success(request, "L'import a été validé. Les notes sont enregistrées en statut BROUILLON.")
                
        except Exception as e:
            messages.error(request, f"Erreur lors de la validation : {e}")
            
        return redirect("imports:detail", pk=pk)


from apps.filieres.models import Filiere

class ImportFichierResolveView(AdminRequiredMixin, View):
    def get(self, request, pk):
        import_fichier = get_object_or_404(ImportFichier, pk=pk)
        if import_fichier.statut != 'en_attente':
            messages.error(request, "Cet import ne peut plus être modifié.")
            return redirect("imports:detail", pk=pk)

        # Trouver les feuilles non reconnues
        feuilles_a_valider = set()
        for ligne in import_fichier.lignes.all():
            match_info = ligne.donnees_brutes.get("match_filiere", {})
            if match_info.get("statut") == "a_valider":
                feuilles_a_valider.add(match_info.get("entree"))
                
        if not feuilles_a_valider:
            messages.info(request, "Aucune correspondance manuelle requise.")
            return redirect("imports:detail", pk=pk)
            
        filieres_officielles = Filiere.objects.values_list('nom', flat=True).distinct().order_by('nom')
        
        return render(request, "imports/import_resolve.html", {
            "import_fichier": import_fichier,
            "feuilles": sorted(list(feuilles_a_valider)),
            "filieres": filieres_officielles
        })

    def post(self, request, pk):
        import_fichier = get_object_or_404(ImportFichier, pk=pk)
        
        # Mettre à jour les lignes avec les choix manuels
        lignes = import_fichier.lignes.all()
        modifications_count = 0
        
        with transaction.atomic():
            for ligne in lignes:
                match_info = ligne.donnees_brutes.get("match_filiere", {})
                entree = match_info.get("entree")
                
                if match_info.get("statut") == "a_valider" and entree:
                    choix = request.POST.get(f"resolve_{entree}")
                    if choix:
                        # Mettre à jour le JSON de la ligne
                        donnees = ligne.donnees_brutes
                        donnees["match_filiere"]["statut"] = "auto"  # On le force à auto pour passer la validation
                        donnees["match_filiere"]["candidat"] = choix
                        ligne.donnees_brutes = donnees
                        ligne.save()
                        modifications_count += 1
                        
        messages.success(request, f"Correspondances manuelles enregistrées. Vous pouvez maintenant valider l'import.")
        return redirect("imports:detail", pk=pk)

