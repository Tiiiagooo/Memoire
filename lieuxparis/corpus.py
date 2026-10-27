"""Lecture des corpus de paroles de chansons.

Deux formats coexistent dans le dépôt :

* **format Genius** (corpus brut, ex. ``echantillon_jacques_dutronc.json``) ::

    {"<artiste>": [{"full_title": ..., "lyrics": "...", "release_date": ...,
                    "album": {"artist": {"name": ...}}, ...}, ...]}

* **format pré-traité** (sortie du true casing, ex. ``corpus_complet.json``) ::

    {"<artiste>": [{"Titre_chanson": ..., "Auteur": ..., "Date": ...,
                    "lyrics": ["..."]}, ...]}

:func:`charger_corpus` lit les deux et renvoie une liste de :class:`Chanson`.
"""

from collections import Counter
from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional

from .fichiers import Chemin, lire_json
from .tokenisation import tokeniser


@dataclass
class Chanson:
    artiste: str            # clé de l'artiste dans le corpus (ex. "_113")
    titre: str
    paroles: Optional[str]  # None quand Genius n'a pas fourni les paroles
    date: Optional[str] = None
    auteur: Optional[str] = None

    @property
    def a_des_paroles(self) -> bool:
        return bool(self.paroles)


def _depuis_genius(artiste: str, element: dict) -> Chanson:
    paroles = element.get("lyrics")
    try:
        auteur = element["album"]["artist"]["name"]
    except (KeyError, TypeError):
        auteur = None
    return Chanson(
        artiste=artiste,
        titre=element.get("full_title", ""),
        paroles=paroles if isinstance(paroles, str) else None,
        date=element.get("release_date"),
        auteur=auteur,
    )


def _depuis_pretraite(artiste: str, element: dict) -> Chanson:
    paroles = element.get("lyrics")
    if isinstance(paroles, list):
        paroles = "\n".join(p for p in paroles if isinstance(p, str))
    return Chanson(
        artiste=artiste,
        titre=element.get("Titre_chanson", ""),
        paroles=paroles or None,
        date=element.get("Date"),
        auteur=element.get("Auteur"),
    )


def charger_corpus(chemin: Chemin, artistes: Optional[Iterable[str]] = None) -> List[Chanson]:
    """Charge un corpus (format Genius ou pré-traité).

    ``artistes`` permet de ne garder que certains artistes (clés du JSON).
    """
    donnees: Dict[str, list] = lire_json(chemin)
    garder = set(artistes) if artistes else None
    chansons = []
    for artiste, elements in donnees.items():
        if garder is not None and artiste not in garder:
            continue
        for element in elements:
            if "Titre_chanson" in element:
                chansons.append(_depuis_pretraite(artiste, element))
            else:
                chansons.append(_depuis_genius(artiste, element))
    return chansons


def vers_format_pretraite(chansons: Iterable[Chanson]) -> Dict[str, list]:
    """Sérialise des chansons au format pré-traité (celui de ``corpus_pretraite/``)."""
    sortie: Dict[str, list] = {}
    for c in chansons:
        sortie.setdefault(c.artiste, []).append({
            "Titre_chanson": c.titre,
            "Auteur": c.auteur,
            "lyrics": [c.paroles] if c.paroles else [],
            "Date": c.date,
        })
    return sortie


def statistiques(chansons: List[Chanson]) -> dict:
    """Quelques chiffres sur le corpus (nombre d'artistes, de chansons, de mots…)."""
    avec_paroles = [c for c in chansons if c.a_des_paroles]
    longueurs = [len(tokeniser(c.paroles)) for c in avec_paroles]
    dates = [c.date[:4] for c in chansons if c.date]
    decennies = Counter(f"{a[:3]}0" for a in dates if a.isdigit())
    return {
        "artistes": len({c.artiste for c in chansons}),
        "chansons": len(chansons),
        "chansons_avec_paroles": len(avec_paroles),
        "chansons_sans_paroles": len(chansons) - len(avec_paroles),
        "chansons_datees": len(dates),
        "mots": sum(longueurs),
        "mots_par_chanson_moyenne": round(sum(longueurs) / len(longueurs), 1) if longueurs else 0,
        "chansons_par_decennie": dict(sorted(decennies.items())),
    }


def longueurs_chansons(chansons: List[Chanson]) -> Dict[str, Dict[str, int]]:
    """Nombre de mots par chanson, regroupé par artiste."""
    sortie: Dict[str, Dict[str, int]] = {}
    for c in chansons:
        sortie.setdefault(c.artiste, {})[c.titre] = len(tokeniser(c.paroles)) if c.paroles else 0
    return sortie
