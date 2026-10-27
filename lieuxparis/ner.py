"""Reconnaissance d'entités nommées (REN) avec les trois modèles français de spaCy.

Résultat produit par :func:`extraire_lieux` (ex. ``resultats/entites/*.json``) ::

    {"<artiste>": {"<titre>": {"small": [...], "medium": [...], "large": [...]}}}

Le calcul est long sur le corpus complet : le fichier de sortie sert de cache et
le traitement reprend là où il s'était arrêté.
"""

from functools import lru_cache
from pathlib import Path
from typing import Dict, Iterable, List, Optional

from tqdm import tqdm

from . import config
from .corpus import Chanson
from .fichiers import Chemin, ecrire_json, lire_json

Entites = Dict[str, Dict[str, Dict[str, List[str]]]]


@lru_cache(maxsize=None)
def charger_modele(nom: str):
    """Charge un modèle spaCy à partir de son alias (small / medium / large)."""
    import spacy

    paquet = config.MODELES_SPACY.get(nom, nom)
    try:
        return spacy.load(paquet)
    except OSError as err:
        raise SystemExit(
            f"Le modèle spaCy « {paquet} » n'est pas installé.\n"
            f"Installez-le avec : python -m spacy download {paquet}"
        ) from err


def lieux_detectes(texte: str, modele: str) -> List[str]:
    """Entités étiquetées LOC dans un texte."""
    doc = charger_modele(modele)(texte)
    return [ent.text for ent in doc.ents if ent.label_ == config.ETIQUETTE_LIEU]


def extraire_lieux(chansons: Iterable[Chanson], modeles: Iterable[str] = ("small", "medium", "large"),
                   sortie: Optional[Chemin] = None, sauvegarde_tous: int = 200) -> Entites:
    """Applique chaque modèle à chaque chanson et renvoie les lieux détectés."""
    modeles = list(modeles)
    resultats: Entites = lire_json(sortie) if sortie and Path(sortie).exists() else {}
    chansons = [c for c in chansons if c.a_des_paroles]

    for i, chanson in enumerate(tqdm(chansons, desc="REN", unit="chanson"), start=1):
        deja = resultats.setdefault(chanson.artiste, {}).setdefault(chanson.titre, {})
        for modele in modeles:
            if modele not in deja:
                deja[modele] = lieux_detectes(chanson.paroles, modele)
        if sortie and i % sauvegarde_tous == 0:
            ecrire_json(sortie, resultats)

    if sortie:
        ecrire_json(sortie, resultats)
    return resultats


def lieux_par_modele(entites: Entites, artiste: Optional[str] = None) -> Dict[str, List[str]]:
    """Aplatis les résultats : toutes les occurrences de lieux, par modèle."""
    par_modele: Dict[str, List[str]] = {}
    for nom_artiste, chansons in entites.items():
        if artiste is not None and nom_artiste != artiste:
            continue
        for modeles in chansons.values():
            for modele, lieux in modeles.items():
                par_modele.setdefault(modele, []).extend(lieux)
    return par_modele


def comparer_modeles(par_modele: Dict[str, List[str]]) -> dict:
    """Lieux trouvés par les trois modèles, et propres à chacun."""
    ensembles = {m: set(l) for m, l in par_modele.items()}
    communs = set.intersection(*ensembles.values()) if ensembles else set()
    propres = {
        m: sorted(e - set().union(*(x for n, x in ensembles.items() if n != m)))
        for m, e in ensembles.items()
    }
    return {
        "nombre_par_modele": {m: len(e) for m, e in ensembles.items()},
        "communs": sorted(communs),
        "propres": propres,
    }
