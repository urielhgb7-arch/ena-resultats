CREATE TABLE UtilisateurAdmin (
    id SERIAL PRIMARY KEY,
    username VARCHAR(150) UNIQUE NOT NULL,
    -- (Django fields)
);

CREATE TABLE AnneeAcademique (
    id SERIAL PRIMARY KEY,
    annee VARCHAR(9) UNIQUE NOT NULL -- ex: "2023-2024"
);

CREATE TABLE Niveau (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(50) UNIQUE NOT NULL -- ex: "Licence 1"
);

CREATE TABLE Filiere (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(100) UNIQUE NOT NULL,
    a_des_specialites BOOLEAN DEFAULT FALSE,
    specialite_unique_auto BOOLEAN DEFAULT FALSE
);

CREATE TABLE Specialite (
    id SERIAL PRIMARY KEY,
    filiere_id INTEGER REFERENCES Filiere(id),
    nom VARCHAR(100) NOT NULL
);

CREATE TABLE Semestre (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(50) NOT NULL,
    niveau_id INTEGER REFERENCES Niveau(id)
);

CREATE TABLE SessionResultat (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(100) NOT NULL -- ex: "Normale", "Rattrapage"
);

CREATE TABLE UE (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(200) NOT NULL,
    code VARCHAR(50) UNIQUE NOT NULL,
    credits INTEGER NOT NULL
);

CREATE TABLE EC (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(200) NOT NULL,
    code VARCHAR(50) UNIQUE NOT NULL,
    ue_id INTEGER REFERENCES UE(id)
);

CREATE TABLE Etudiant (
    id SERIAL PRIMARY KEY,
    matricule VARCHAR(50) UNIQUE NOT NULL,
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL
);

CREATE TABLE NoteEC (
    id SERIAL PRIMARY KEY,
    etudiant_id INTEGER REFERENCES Etudiant(id),
    ec_id INTEGER REFERENCES EC(id),
    valeur DECIMAL(5, 2)
);

CREATE TABLE ResultatUE (
    id SERIAL PRIMARY KEY,
    etudiant_id INTEGER REFERENCES Etudiant(id),
    ue_id INTEGER REFERENCES UE(id),
    session_id INTEGER REFERENCES SessionResultat(id),
    moyenne_ue DECIMAL(5, 2) NOT NULL -- Fixed rule!
);

CREATE TABLE ImportFichier (
    id SERIAL PRIMARY KEY,
    fichier VARCHAR(255) NOT NULL,
    date_import TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE LigneBrute (
    id SERIAL PRIMARY KEY,
    import_id INTEGER REFERENCES ImportFichier(id),
    donnees JSONB NOT NULL
);

CREATE TABLE MappingTemplate (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(100) UNIQUE NOT NULL,
    mapping JSONB NOT NULL
);
