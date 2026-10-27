"""Enrichissement manuel du lexique (section 4.5 du mémoire).

Pour chaque lieu détecté par spaCy mais absent du lexique, on demande à un
humain s'il s'agit bien d'un lieu de Paris et s'il connaît d'autres noms pour
ce lieu. Les réponses sont ajoutées à ``data/ajouts_lexique.json``, qui est
ensuite pris en compte par :func:`lieuxparis.lexique.charger_lexique`.
"""

from pathlib import Path
from typing import Dict, Iterable, List, Set

from . import config
from .fichiers import Chemin, ecrire_json, lire_json


def _oui(question: str) -> bool:
    while True:
        r = input(f"{question} [o/n/q] ").strip().lower()
        if r in {"o", "oui", "y"}:
            return True
        if r in {"n", "non"}:
            return False
        if r in {"q", "quitter"}:
            raise KeyboardInterrupt


def enrichir(candidats: Iterable[str], lexique: Set[str], sortie: Chemin = config.AJOUTS_LEXIQUE) -> Dict[str, List[str]]:
    """Session interactive ; « q » pour s'arrêter (les réponses déjà données sont gardées)."""
    ajouts: Dict[str, List[str]] = lire_json(sortie) if Path(sortie).exists() else {}
    a_voir = sorted({c for c in candidats if c not in lexique and c not in ajouts})
    print(f"{len(a_voir)} lieux à vérifier. Tapez « q » pour arrêter.\n")
    try:
        for i, lieu in enumerate(a_voir, start=1):
            if not _oui(f"({i}/{len(a_voir)}) « {lieu} » est-il un lieu de Paris ?"):
                continue
            autres = []
            if _oui("  Ce lieu a-t-il d'autres noms ?"):
                print("  Un nom par ligne, ligne vide pour terminer.")
                while nom := input("  > ").strip():
                    autres.append(nom)
            ajouts[lieu] = autres
            ecrire_json(sortie, ajouts)
    except (KeyboardInterrupt, EOFError):
        print("\nArrêt.")
    ecrire_json(sortie, ajouts)
    return ajouts
