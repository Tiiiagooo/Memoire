"""Proportions calculées sur chaque chanson (section 4.1.1 du mémoire).

Pour chaque chanson, en pourcentage du nombre de mots :

- ``en_lieux``     entités nommées étiquetées LOC par spaCy ;
- ``en_toutes``    toutes les entités nommées trouvées par spaCy ;
- ``en_lexique``   entités nommées présentes dans le lexique des lieux de Paris ;
- ``majuscules``   mots commençant par une majuscule.
"""

from typing import Dict, Iterable, List, Set

from tqdm import tqdm

from . import config
from .corpus import Chanson
from .ner import charger_modele
from .tokenisation import tokeniser


def _pourcentage(n: int, total: int) -> float:
    return 100 * n / total if total else 0.0


def proportions_chanson(texte: str, modele: str, lexique: Set[str]) -> dict:
    mots = tokeniser(texte)
    doc = charger_modele(modele)(texte)
    entites = [e.text for e in doc.ents]
    lieux = [e.text for e in doc.ents if e.label_ == config.ETIQUETTE_LIEU]
    dans_lexique = [e for e in entites if e in lexique]
    majuscules = [m for m in mots if m.istitle()]
    return {
        "mots": len(mots),
        "en_lieux": _pourcentage(len(lieux), len(mots)),
        "en_toutes": _pourcentage(len(entites), len(mots)),
        "en_lexique": _pourcentage(len(dans_lexique), len(mots)),
        "majuscules": _pourcentage(len(majuscules), len(mots)),
        "lieux_du_lexique": dans_lexique,
    }


def calculer(chansons: Iterable[Chanson], modele: str, lexique: Set[str]) -> Dict[str, dict]:
    sortie = {}
    for c in tqdm(list(chansons), desc=f"Proportions ({modele})", unit="chanson"):
        if c.a_des_paroles:
            sortie[c.titre] = proportions_chanson(c.paroles, modele, lexique)
        else:
            sortie[c.titre] = {"mots": 0, "en_lieux": 0.0, "en_toutes": 0.0,
                               "en_lexique": 0.0, "majuscules": 0.0, "lieux_du_lexique": []}
    return sortie


COLONNES = [("en_lieux", "Prop. lieux"), ("en_toutes", "Prop. EN"),
            ("en_lexique", "Prop. lexique"), ("majuscules", "Prop. maj.")]


def tableau_latex(proportions: Dict[str, dict], longueur_titre: int = 30) -> str:
    """Tableau LaTeX (trié par proportion de lieux décroissante), prêt pour Overleaf."""
    lignes: List[str] = [
        r"\begin{table}",
        r"\centering",
        r"\begin{tabular}{|l|r|r|r|r|}",
        r"\hline",
        "Titre & " + " & ".join(n for _, n in COLONNES) + r" \\",
        r"\hline",
    ]
    tri = sorted(proportions.items(), key=lambda x: x[1]["en_lieux"], reverse=True)
    for titre, p in tri:
        titre = titre.replace("\xa0", " ").replace("&", r"\&")
        if len(titre) > longueur_titre:
            titre = titre[:longueur_titre] + "…"
        valeurs = " & ".join(f"{p[c]:.2f}" for c, _ in COLONNES)
        lignes += [f"{titre} & {valeurs} \\\\", r"\hline"]
    lignes += [r"\end{tabular}", r"\end{table}"]
    return "\n".join(lignes)
