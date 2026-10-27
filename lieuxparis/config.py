"""Chemins et constantes partagés par tous les modules."""

from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent

DATA = RACINE / "data"
RESULTATS = RACINE / "resultats"

# --- Données d'entrée -------------------------------------------------------
CORPUS_ECHANTILLON = DATA / "corpus" / "echantillon_jacques_dutronc.json"
CORPUS_PRETRAITE = DATA / "corpus_pretraite" / "corpus_complet.json"
DOSSIER_LEXIQUE = DATA / "lexique_lieux_paris"
AJOUTS_LEXIQUE = DATA / "ajouts_lexique.json"
GLAFF_FREQUENCES = DATA / "glaff" / "frequences_glaff.json"

# --- Résultats --------------------------------------------------------------
ENTITES_AVANT = RESULTATS / "entites" / "avant_pretraitement.json"
ENTITES_APRES = RESULTATS / "entites" / "apres_pretraitement.json"
DOSSIER_ANALYSE = RESULTATS / "analyse"
DOSSIER_FIGURES = RESULTATS / "figures"
DOSSIER_PROPORTIONS = RESULTATS / "proportions"
CARTE_CSV = RESULTATS / "carte" / "lieux_geolocalises.csv"
CACHE_GEOCODAGE = RESULTATS / "carte" / "cache_geocodage.json"

# --- spaCy ------------------------------------------------------------------
MODELES_SPACY = {
    "small": "fr_core_news_sm",
    "medium": "fr_core_news_md",
    "large": "fr_core_news_lg",
}
ETIQUETTE_LIEU = "LOC"

# Lieux trop généraux, exclus de la cartographie.
LIEUX_EXCLUS_CARTE = {"Paris", "Seine", "Europe", "Amérique"}
