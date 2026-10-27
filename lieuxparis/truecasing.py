"""Pré-traitement des paroles : adaptation de la casse (« true casing »).

Dans les paroles, chaque ligne commence par une majuscule, ce qui pousse spaCy
à y voir des entités nommées. Le pré-traitement se fait en deux étapes :

1. **Casse** : si le premier mot d'une ligne commence par une majuscule, on le
   met en minuscule quand

   - il existe en minuscule dans le GLAFF (c'est un mot du lexique courant),
   - **et** il n'est pas dans le lexique des lieux de Paris.

   Exemple : « Il est mini Docteur Schweitzer » → « il est mini Docteur Schweitzer »,
   mais « Paris et province » reste inchangé.

2. **Espaces** : on ajoute un espace avant et après chaque retour à la ligne
   (``" \\n "``) pour que spaCy sépare bien le dernier mot d'une ligne du premier
   mot de la suivante.

Chaque décision est comptée pour construire la matrice de confusion du mémoire
(voir :data:`CORRESPONDANCE_MATRICE`).
"""

from collections import Counter
from dataclasses import replace
from typing import Dict, Iterable, List, Set, Tuple

from .corpus import Chanson
from .fichiers import Chemin, lire_json
from .tokenisation import MOTIF_DEBUT_LIGNE

# Décisions possibles pour un mot en début de ligne qui porte une majuscule.
MIS_EN_MINUSCULE = "mis_en_minuscule"          # dans le GLAFF, pas un lieu
GARDE_LIEU_GLAFF = "garde_lieu_dans_glaff"     # dans le GLAFF mais lieu de Paris
GARDE_LIEU = "garde_lieu"                      # hors GLAFF et lieu de Paris
GARDE_INCONNU = "garde_inconnu"                # hors GLAFF, pas un lieu

# Étiquettes utilisées dans le mémoire (figure 4.7).
CORRESPONDANCE_MATRICE = {
    MIS_EN_MINUSCULE: "VP",
    GARDE_LIEU_GLAFF: "FP",
    GARDE_INCONNU: "FN",
    GARDE_LIEU: "VN",
}


def charger_glaff(chemin: Chemin) -> Set[str]:
    """Vocabulaire du GLAFF (formes fléchies)."""
    return set(lire_json(chemin))


def frequences_glaff(chemin_glaff_txt: Chemin) -> Dict[str, float]:
    """Construit ``data/glaff/frequences_glaff.json`` à partir du fichier brut
    ``glaff-1.2.2.txt`` : {forme: somme des fréquences des colonnes 7, 9, 11…}."""
    freq: Dict[str, float] = {}
    with open(chemin_glaff_txt, encoding="utf-8") as f:
        for ligne in f:
            champs = ligne.rstrip("\n").split("|")
            if len(champs) < 2:
                continue
            total = 0.0
            for valeur in champs[6::2]:
                try:
                    total += float(valeur)
                except ValueError:
                    pass
            freq[champs[0]] = total
    return freq


def adapter_ligne(ligne: str, glaff: Set[str], lexique: Set[str]) -> Tuple[str, str]:
    """Applique l'étape 1 à une ligne. Renvoie (nouvelle ligne, décision ou "")."""
    m = MOTIF_DEBUT_LIGNE.match(ligne)
    if not m:
        return ligne, ""
    mot = m.group(0)
    if mot[0] == mot[0].lower():
        return ligne, ""
    minuscule = mot.lower()
    if minuscule in glaff:
        if mot in lexique:
            return ligne, GARDE_LIEU_GLAFF
        return minuscule + ligne[len(mot):], MIS_EN_MINUSCULE
    return ligne, GARDE_LIEU if mot in lexique else GARDE_INCONNU


def adapter_texte(texte: str, glaff: Set[str], lexique: Set[str]) -> Tuple[str, Counter]:
    """Applique les deux étapes à un texte complet."""
    decisions: Counter = Counter()
    lignes = []
    for ligne in texte.split("\n"):
        ligne, decision = adapter_ligne(ligne, glaff, lexique)
        if decision:
            decisions[decision] += 1
        lignes.append(ligne)
    return " \n ".join(lignes), decisions


def pretraiter(chansons: Iterable[Chanson], glaff: Set[str], lexique: Set[str]) -> Tuple[List[Chanson], Counter]:
    """Pré-traite un corpus. Renvoie les chansons modifiées et le total des décisions."""
    total: Counter = Counter()
    sortie = []
    for chanson in chansons:
        if chanson.a_des_paroles:
            texte, decisions = adapter_texte(chanson.paroles, glaff, lexique)
            total.update(decisions)
            chanson = replace(chanson, paroles=texte)
        sortie.append(chanson)
    return sortie, total


def matrice(decisions: Counter) -> dict:
    """Convertit les décisions en VP / FP / FN / VN et calcule les scores."""
    m = {etiquette: decisions.get(cle, 0) for cle, etiquette in CORRESPONDANCE_MATRICE.items()}
    vp, fp, fn = m["VP"], m["FP"], m["FN"]
    precision = vp / (vp + fp) if vp + fp else 0.0
    rappel = vp / (vp + fn) if vp + fn else 0.0
    f = 2 * precision * rappel / (precision + rappel) if precision + rappel else 0.0
    return {**m, "precision": precision, "rappel": rappel, "f_mesure": f}
