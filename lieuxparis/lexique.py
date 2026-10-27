"""Lexique des lieux de Paris (construit à partir de listes Wikipédia).

Chaque fichier de ``data/lexique_lieux_paris/`` est une liste JSON de noms de
lieux d'une même catégorie (rues, portes, églises, communes d'Île-de-France…).
Les ajouts faits avec :mod:`lieuxparis.enrichissement` (``data/ajouts_lexique.json``)
sont fusionnés automatiquement.
"""

import re
from pathlib import Path
from typing import Dict, Iterable, Set

from . import config
from .fichiers import Chemin, lire_json


class Lexique(frozenset):
    """Ensemble de noms de lieux dont le test d'appartenance ignore la casse :
    « Place de Clichy » est reconnu même si le lexique contient « place de Clichy »."""

    def __new__(cls, lieux=()):
        obj = super().__new__(cls, lieux)
        obj._minuscules = frozenset(l.casefold() for l in obj)
        return obj

    def __contains__(self, lieu) -> bool:
        return isinstance(lieu, str) and lieu.casefold() in self._minuscules


def charger_lexique(dossier: Chemin = config.DOSSIER_LEXIQUE,
                    ajouts: Chemin = config.AJOUTS_LEXIQUE) -> Lexique:
    """Renvoie l'ensemble des noms de lieux de Paris connus."""
    lieux: Set[str] = set()
    for fichier in sorted(Path(dossier).glob("*.json")):
        lieux.update(lire_json(fichier))
    if Path(ajouts).exists():
        for lieu, autres_noms in lire_json(ajouts).items():
            lieux.add(lieu)
            lieux.update(autres_noms or [])
    return Lexique(lieux)


def lexique_par_fichier(dossier: Chemin = config.DOSSIER_LEXIQUE) -> Dict[str, int]:
    """Nombre d'entrées par fichier source du lexique."""
    return {f.stem: len(lire_json(f)) for f in sorted(Path(dossier).glob("*.json"))}


# Regroupement des lieux selon le premier mot de leur nom.
CATEGORIES = [
    ("Château", r"^[Cc]h[aâ]teau"),
    ("Porte", r"^[Pp]orte"),
    ("Église", r"^[EeÉé]glise"),
    ("Place", r"^[Pp]lace"),
    ("Avenue", r"^[Aa]venue"),
    ("Boulevard", r"^[Bb]oulevard"),
    ("Rue", r"^[Rr]ue"),
    ("Cité", r"^[Cc]it[eé]"),
    ("Arrondissement", r"Paris (0[1-9]|1[0-9]|20|arrondissement)$"),
    ("Saint", r"^([Ss]aint|[Ss]t)\b"),
    ("Pont", r"^[Pp]onts?\b"),
]


def classer_lieux(lieux: Iterable[str]) -> Dict[str, Set[str]]:
    """Classe les lieux par catégorie ; le reste va dans « Inclassable »."""
    restants = set(lieux)
    classes: Dict[str, Set[str]] = {}
    for nom, motif in CATEGORIES:
        expr = re.compile(motif)
        classes[nom] = {l for l in restants if expr.search(l)}
        restants -= classes[nom]
    classes["Inclassable"] = restants
    return classes
