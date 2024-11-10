CREATE TABLE IF NOT EXISTS airflow_table (
    objet_de_marche VARCHAR(255),
    maitre_d_ouvrage VARCHAR(255),
    date_publication_marches_publics DATE,
    date_ouverture_plis DATE,
    date_achevement_commission_travaux DATE,
    journaux_publications TEXT,
    liste_concurrents_admissible TEXT,
    liste_concurrents_retenu TEXT,
    liste_concurrents_infractueux TEXT,
    montant_ttc NUMERIC
);