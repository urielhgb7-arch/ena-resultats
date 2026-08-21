# Guide d'Utilisation - ENA Admin

L'interface d'administration de la plateforme ENA a été refondue pour offrir une ergonomie fluide (Design Monster), sans nécessiter d'expertise technique pour être gérée au quotidien. 

Ce guide est destiné aux **Validateurs** et **Super-Administrateurs**.

## Navigation et Tableau de bord

- **Accès** : L'accès à l'administration est protégé. Utilisez l'URL dédiée (ex: `votre-domaine.com/super-secret-admin/`) pour atteindre le tableau de bord.
- **Interface Mobile** : Si vous accédez depuis une tablette ou un smartphone, le menu latéral se repliera automatiquement. Cliquez sur le bouton "Hamburger" (☰) en haut à gauche pour l'ouvrir.

---

## 1. Gestion des Filières et Unités d'Enseignement (UE)

Ces rubriques vous permettent de paramétrer le référentiel académique avant la saisie des notes.

### Niveaux & Filières
- Dans la barre latérale gauche, cliquez sur **Niveaux & Filières**.
- Vous verrez la liste des filières actuellement configurées.
- **Ajouter** : Cliquez sur le bouton vert "+ Nouvelle Filière". Remplissez les champs (Nom de la filière, attachement au niveau). Vous pouvez y définir si la filière possède des spécialités ou si elle doit avoir une spécialité automatique par défaut.
- **Modifier / Supprimer** : Utilisez les boutons d'actions contextuels situés au bout de chaque ligne du tableau.

### Unités d'Enseignement
- Dans la barre latérale, cliquez sur **Unités d'enseignement**.
- Ici sont gérées les matières (UE).
- **Ajouter** : Cliquez sur "+ Nouvelle UE". Assignez-la à une session académique, indiquez son code (ex: MTH1121), son nom, ses crédits et son statut (Brouillon/Publié).
- Les UEs en statut "Brouillon" ne seront pas visibles par les étudiants.

---

## 2. Procédure d'Importation de Résultats (Fichiers Excel)

La fonctionnalité majeure de la plateforme est la capacité d'ingérer massivement des notes validées depuis des fichiers de PV (Excel).

### Étape 1 : Accéder au module d'import
- Cliquez sur **Imports & PVs** dans la barre latérale de l'administration.
- Ce tableau présente l'historique complet de tous les fichiers ayant été chargés sur la plateforme, avec leur statut (Succès, Échec, Avertissement) et la personne qui a effectué l'import.

### Étape 2 : Préparer votre fichier
- Le fichier doit obligatoirement être au format **`.xlsx`**.
- Assurez-vous que les colonnes soient clairement labellisées (les règles de parsing exactes ont été configurées par l'équipe projet, veuillez vous référer au modèle standard fourni en interne).

### Étape 3 : Uploader le fichier
1. Cliquez sur le bouton bleu **+ Nouvel import**.
2. Une zone de dépôt apparaît. Vous pouvez :
   - Cliquer pour parcourir vos dossiers et sélectionner le PV.
   - Ou glisser et déposer le fichier `.xlsx` directement dans le carré délimité par des tirets.
3. Le système vérifiera immédiatement la taille et le format du fichier.
4. Cliquez sur "Uploader et Valider".

### Étape 4 : Vérification et Correction
Si le fichier présente des anomalies, le statut passera à l'état "Échec" ou "Erreur".
- Un rapport s'affichera à l'écran pour indiquer quelles lignes sont en cause (ex: matricule étudiant inexistant, UE non trouvée).
- Vous devrez corriger l'anomalie dans le fichier original et recommencer l'import.
- L'intégrité de la base de données est garantie : en cas d'erreur de parsing, aucune note n'est injectée à moitié.

---

> [!TIP]
> **Conseil de sécurité** : En tant que validateur, si vous remarquez des tentatives de connexion suspectes sur le portail d'administration, alertez le Super Administrateur immédiatement pour initier une rotation de `l'URL d'administration secrète`.
