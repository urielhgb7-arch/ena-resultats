1. **Implement `accounts` models**
   - Create `UtilisateurAdmin` inheriting from `AbstractBaseUser` and `PermissionsMixin` to match the schema.
2. **Implement `core` models**
   - Create `AnneeAcademique`, `Niveau`, `Semestre`, `SessionResultat` in `apps/core/models.py`.
3. **Implement `filieres` models**
   - Create `Filiere`, `Specialite`, `UE`, `EC` in `apps/filieres/models.py`.
4. **Implement `imports` models**
   - Create `MappingTemplate`, `ImportFichier`, `LigneBrute` in `apps/imports/models.py`.
5. **Implement `resultats` models**
   - Create `Etudiant`, `NoteEC`, `ResultatUE` in `apps/resultats/models.py`.
6. **Configure Django Apps and Settings**
   - Ensure all apps are registered in `config/settings.py` so `makemigrations` can detect them.
   - Configure basic settings for `AUTH_USER_MODEL`.
7. **Generate Migrations and Test**
   - Run `python manage.py makemigrations` to generate migration files.
   - Run `python manage.py check` to ensure there are no issues.
8. **Pre-commit Steps and Submission**
   - Ensure proper testing, verification, review, and reflection are done.
   - Submit the PR for task 1 (`feat/data-models`).
