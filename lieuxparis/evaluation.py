"""Évaluation de la REN de spaCy face à une annotation manuelle.

Fichier de référence attendu (JSON) — une liste d'exemples ::

    [{"text": "…paroles…", "entities": [[debut, fin, "Place de Clichy"], ...]}, ...]

Deux façons de compter :

- **macro** : chaque entité distincte n'est comptée qu'une fois par texte ;
- **micro** : on compte les occurrences (une entité citée 3 fois compte 3 fois).
"""

from collections import Counter
from typing import Dict, Sequence

from . import config
from .fichiers import Chemin, lire_json
from .ner import charger_modele


def _vide() -> dict:
    return {"micro": {"VP": 0, "FP": 0, "FN": 0}, "macro": {"VP": 0, "FP": 0, "FN": 0}, "details": []}


def comparer(predites: Sequence[str], attendues: Sequence[str], res: dict) -> dict:
    """Ajoute à ``res`` les VP / FP / FN d'un texte."""
    n_pred, n_gold = Counter(predites), Counter(attendues)
    vp, fp, fn = set(n_pred) & set(n_gold), set(n_pred) - set(n_gold), set(n_gold) - set(n_pred)
    res["details"].append({"VP": sorted(vp), "FP": sorted(fp), "FN": sorted(fn)})

    res["macro"]["VP"] += len(vp)
    res["macro"]["FP"] += len(fp)
    res["macro"]["FN"] += len(fn)

    for e in vp:
        res["micro"]["VP"] += min(n_pred[e], n_gold[e])
        res["micro"]["FP"] += max(0, n_pred[e] - n_gold[e])   # trop d'occurrences
        res["micro"]["FN"] += max(0, n_gold[e] - n_pred[e])   # occurrences manquées
    res["micro"]["FP"] += sum(n_pred[e] for e in fp)
    res["micro"]["FN"] += sum(n_gold[e] for e in fn)
    return res


def scores(res: dict) -> Dict[str, Dict[str, float]]:
    """Précision, rappel et F-mesure pour les comptes micro et macro."""
    sortie = {}
    for type_eval in ("micro", "macro"):
        vp, fp, fn = (res[type_eval][k] for k in ("VP", "FP", "FN"))
        p = vp / (vp + fp) if vp + fp else 0.0
        r = vp / (vp + fn) if vp + fn else 0.0
        f = 2 * p * r / (p + r) if p + r else 0.0
        sortie[type_eval] = {"precision": p, "rappel": r, "f_mesure": f}
    return sortie


def evaluer(chemin_reference: Chemin, modele: str = "large") -> dict:
    """Évalue un modèle spaCy sur un fichier d'annotations de référence."""
    nlp = charger_modele(modele)
    res = _vide()
    for exemple in lire_json(chemin_reference):
        doc = nlp(exemple["text"])
        predites = [e.text for e in doc.ents if e.label_ == config.ETIQUETTE_LIEU]
        attendues = [e[-1] for e in exemple["entities"]]
        comparer(predites, attendues, res)
    return {"comptes": {k: res[k] for k in ("micro", "macro")}, "scores": scores(res), "details": res["details"]}
