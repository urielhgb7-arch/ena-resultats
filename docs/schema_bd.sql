-- ============================================================
-- SCHEMA : Plateforme de resultats ENA (v4 - avec staging import)
-- PostgreSQL
-- ============================================================

-- ---------- NETTOYAGE (permet de relancer le script sans erreur) ----------
-- CASCADE supprime automatiquement les contraintes/index dependants,
-- l'ordre de la liste n'a donc pas d'importance ici.

DROP TABLE IF EXISTS
    ligne_brute, import_fichier, mapping_template, utilisateur_admin,
    resultat_ue, note_ec, etudiant, ec, ue, session_resultat,
    semestre, specialite, filiere, niveau, annee_academique CASCADE;

-- ---------- ARBORESCENCE ACADEMIQUE ----------

CREATE TABLE annee_academique (
    id SERIAL PRIMARY KEY,
    libelle VARCHAR(20) NOT NULL,           -- ex: "2025-2026"
    active BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE niveau (
    id SERIAL PRIMARY KEY,
    annee_id INTEGER NOT NULL REFERENCES annee_academique(id) ON DELETE CASCADE,
    libelle VARCHAR(10) NOT NULL             -- L1, L2, L3
);

CREATE TABLE filiere (
    id SERIAL PRIMARY KEY,
    niveau_id INTEGER NOT NULL REFERENCES niveau(id) ON DELETE CASCADE,
    nom VARCHAR(150) NOT NULL,
    a_des_specialites BOOLEAN NOT NULL DEFAULT TRUE,      -- FALSE pour Secrétariat de Gestion
    specialite_unique_auto BOOLEAN NOT NULL DEFAULT FALSE -- TRUE pour STID
);

CREATE TABLE specialite (
    id SERIAL PRIMARY KEY,
    filiere_id INTEGER NOT NULL REFERENCES filiere(id) ON DELETE CASCADE,
    nom VARCHAR(150) NOT NULL
);

CREATE TABLE semestre (
    id SERIAL PRIMARY KEY,
    filiere_id INTEGER NOT NULL REFERENCES filiere(id) ON DELETE CASCADE,
    libelle VARCHAR(20) NOT NULL,           -- "Semestre 1"...
    type VARCHAR(30) NOT NULL DEFAULT 'normal' -- normal, stage
);

CREATE TABLE session_resultat (
    id SERIAL PRIMARY KEY,
    semestre_id INTEGER NOT NULL REFERENCES semestre(id) ON DELETE CASCADE,
    specialite_id INTEGER REFERENCES specialite(id) ON DELETE SET NULL, -- NULL si tronc commun
    type VARCHAR(30) NOT NULL              -- normale, rattrapage, ajournement, re_enjambement
);

-- ---------- UE / EC ----------

CREATE TABLE ue (
    id SERIAL PRIMARY KEY,
    session_id INTEGER NOT NULL REFERENCES session_resultat(id) ON DELETE CASCADE,
    code VARCHAR(30) NOT NULL,              -- ex: MTH1121
    nom VARCHAR(200) NOT NULL,
    credits INTEGER NOT NULL CHECK (credits > 0), -- nombre de credits ECTS/LMD de l'UE
    fichier_pdf_archive VARCHAR(300),       -- chemin du PV officiel signé (archive)
    date_publication DATE,
    statut VARCHAR(20) NOT NULL DEFAULT 'brouillon' -- brouillon, publie
);

CREATE TABLE ec (
    id SERIAL PRIMARY KEY,
    ue_id INTEGER NOT NULL REFERENCES ue(id) ON DELETE CASCADE,
    code VARCHAR(10) NOT NULL,              -- EC1, EC2
    nom VARCHAR(200) NOT NULL
);

-- ---------- ETUDIANTS ET RESULTATS ----------

CREATE TABLE etudiant (
    id SERIAL PRIMARY KEY,
    matricule VARCHAR(30) UNIQUE,           -- nullable si pas dispo pour anciennes promos
    annee_promo VARCHAR(10),                -- ex: "26" vu sur le PV réel
    nom VARCHAR(150) NOT NULL,
    prenom VARCHAR(150) NOT NULL
);

CREATE TABLE note_ec (
    id SERIAL PRIMARY KEY,
    etudiant_id INTEGER NOT NULL REFERENCES etudiant(id) ON DELETE CASCADE,
    ec_id INTEGER NOT NULL REFERENCES ec(id) ON DELETE CASCADE,
    import_id INTEGER,                      -- FK vers import_fichier, ajoutée plus bas
    note NUMERIC(4,2) NOT NULL,
    UNIQUE (etudiant_id, ec_id)
);

CREATE TABLE resultat_ue (
    id SERIAL PRIMARY KEY,
    etudiant_id INTEGER NOT NULL REFERENCES etudiant(id) ON DELETE CASCADE,
    ue_id INTEGER NOT NULL REFERENCES ue(id) ON DELETE CASCADE,
    import_id INTEGER,                      -- FK vers import_fichier, ajoutée plus bas
    moyenne_ue NUMERIC(4,2) NOT NULL,        -- moyenne des EC de cette UE pour cet etudiant
                                              -- (calculee a l'import/saisie, stockee en dur :
                                              --  ne pas recalculer dynamiquement depuis note_ec,
                                              --  car ce chiffre correspond au PV officiel signe)
    statut VARCHAR(5) NOT NULL,              -- V, NV, V*  (valeurs à confirmer avec le Bureau)
    UNIQUE (etudiant_id, ue_id)
);

-- ---------- UTILISATEURS / ADMIN ----------

CREATE TABLE utilisateur_admin (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(150) NOT NULL,
    email VARCHAR(200) UNIQUE NOT NULL,
    role VARCHAR(30) NOT NULL,               -- visiteur, validateur, super_admin
    mot_de_passe VARCHAR(255) NOT NULL
);

-- ---------- COUCHE IMPORT / STAGING ----------

CREATE TABLE mapping_template (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(150) NOT NULL,
    config_colonnes JSONB NOT NULL          -- décrit la structure du fichier Excel source
);

CREATE TABLE import_fichier (
    id SERIAL PRIMARY KEY,
    nom_fichier VARCHAR(300) NOT NULL,
    date_import TIMESTAMP NOT NULL DEFAULT NOW(),
    utilisateur_id INTEGER REFERENCES utilisateur_admin(id) ON DELETE SET NULL,
    mapping_id INTEGER REFERENCES mapping_template(id) ON DELETE SET NULL,
    statut VARCHAR(20) NOT NULL DEFAULT 'en_attente' -- en_attente, valide, applique, annule
);

CREATE TABLE ligne_brute (
    id SERIAL PRIMARY KEY,
    import_id INTEGER NOT NULL REFERENCES import_fichier(id) ON DELETE CASCADE,
    numero_ligne INTEGER NOT NULL,
    donnees_brutes JSONB NOT NULL,           -- ligne Excel telle quelle, structure libre
    statut_traitement VARCHAR(20) NOT NULL DEFAULT 'en_attente'
);

-- Ajout des FK différées vers import_fichier (créée après pour éviter un cycle de dépendance)
ALTER TABLE note_ec ADD CONSTRAINT fk_note_ec_import
    FOREIGN KEY (import_id) REFERENCES import_fichier(id) ON DELETE SET NULL;

ALTER TABLE resultat_ue ADD CONSTRAINT fk_resultat_ue_import
    FOREIGN KEY (import_id) REFERENCES import_fichier(id) ON DELETE SET NULL;

-- ---------- INDEX UTILES ----------

CREATE INDEX idx_etudiant_matricule ON etudiant(matricule);
CREATE INDEX idx_etudiant_nom_prenom ON etudiant(nom, prenom);
CREATE INDEX idx_ue_session ON ue(session_id);
CREATE INDEX idx_resultat_ue_etudiant ON resultat_ue(etudiant_id);
CREATE INDEX idx_note_ec_etudiant ON note_ec(etudiant_id);
