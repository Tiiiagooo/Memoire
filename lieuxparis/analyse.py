"""Analyses croisées artistes ↔ lieux ↔ années (section 4.4 du mémoire).

Toutes les fonctions partent de l'**index** construit par :func:`construire_index` :
une ligne par chanson ::

    {"artiste": "_113", "titre": "...", "date": "2005-10-19", "lieux": ["Vitry", ...]}
"""

import re
from collections import Counter, defaultdict
from typing import Dict, Iterable, List, Optional, Set

from .corpus import Chanson
from .ner import Entites

Index = List[dict]


def construire_index(entites: Entites, modele: str, chansons: Iterable[Chanson] = ()) -> Index:
    """Associe à chaque chanson les lieux détectés par ``modele`` (et sa date si connue)."""
    dates = {(c.artiste, c.titre): c.date for c in chansons}
    index = []
    for artiste, par_titre in entites.items():
        for titre, par_modele in par_titre.items():
            if modele in par_modele:
                index.append({"artiste": artiste, "titre": titre,
                              "date": dates.get((artiste, titre)), "lieux": par_modele[modele]})
    return index


def filtrer_lexique(index: Index, lexique: Set[str]) -> Index:
    """Ne garde que les lieux présents dans le lexique des lieux de Paris."""
    return [{**l, "lieux": [x for x in l["lieux"] if x in lexique]} for l in index]


def lieux_par_artiste(index: Index) -> Dict[str, Dict[str, int]]:
    """{artiste: {lieu: nombre d'occurrences}}, trié par fréquence."""
    compte: Dict[str, Counter] = defaultdict(Counter)
    for ligne in index:
        compte[ligne["artiste"]].update(ligne["lieux"])
    return {a: dict(c.most_common()) for a, c in compte.items()}


def artistes_par_lieu(index: Index) -> Dict[str, Dict[str, int]]:
    """{lieu: {artiste: nombre d'occurrences}}, trié par fréquence."""
    compte: Dict[str, Counter] = defaultdict(Counter)
    for ligne in index:
        for lieu in ligne["lieux"]:
            compte[lieu][ligne["artiste"]] += 1
    return {l: dict(c.most_common()) for l, c in compte.items()}


def chansons_par_lieu(index: Index) -> Dict[str, Dict[str, List[list]]]:
    """{lieu: {artiste: [[titre, date], ...]}} — permet de retrouver où un lieu est cité."""
    sortie: Dict[str, Dict[str, List[list]]] = {}
    for ligne in index:
        for lieu in dict.fromkeys(ligne["lieux"]):
            sortie.setdefault(lieu, {}).setdefault(ligne["artiste"], []).append([ligne["titre"], ligne["date"]])
    return sortie


def frequence_lieux(index: Index) -> Dict[str, int]:
    """Nombre total d'occurrences de chaque lieu dans le corpus."""
    return dict(Counter(l for ligne in index for l in ligne["lieux"]).most_common())


def lieux_par_annee(index: Index, annee: Optional[int] = None) -> Dict[str, Dict[str, int]]:
    """{année: {lieu: occurrences}} pour les chansons datées (ou une seule année)."""
    compte: Dict[str, Counter] = defaultdict(Counter)
    for ligne in index:
        m = re.match(r"(\d{4})", ligne["date"] or "")
        if m and (annee is None or int(m.group(1)) == annee):
            compte[m.group(1)].update(ligne["lieux"])
    return {a: dict(c.most_common()) for a, c in sorted(compte.items())}


def lieux_par_periode(index: Index, bornes=(1940, 2000, 2010, 2019)) -> Dict[str, Dict[str, int]]:
    """Regroupe les lieux par périodes, comme sur les cartes du mémoire
    (1940-2000, 2001-2010, 2011-2019, 2020 et après)."""
    noms = [f"{bornes[0]}-{bornes[1]}"] + [f"{a + 1}-{b}" for a, b in zip(bornes[1:], bornes[2:])] + [f"{bornes[-1] + 1}+"]
    compte: Dict[str, Counter] = {n: Counter() for n in noms}
    for annee, lieux in lieux_par_annee(index).items():
        a = int(annee)
        i = sum(a > b for b in bornes[1:])
        if a >= bornes[0]:
            compte[noms[i]].update(lieux)
    return {n: dict(c.most_common()) for n, c in compte.items()}


def top(dico: Dict[str, int], n: int = 5) -> Dict[str, int]:
    return dict(sorted(dico.items(), key=lambda x: x[1], reverse=True)[:n])
