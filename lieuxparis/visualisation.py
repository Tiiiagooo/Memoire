"""Graphiques : diagrammes de Venn, histogrammes « top 5 », matrices de confusion."""

from pathlib import Path
from typing import Dict, List, Optional

import matplotlib

matplotlib.use("Agg")  # pas d'affichage : on enregistre directement les images
import matplotlib.pyplot as plt  # noqa: E402

from .fichiers import Chemin  # noqa: E402

COULEURS_MODELES = ("#2e7d32", "#c62828", "#1565c0")


def _enregistrer(fig, sortie: Chemin) -> Path:
    sortie = Path(sortie)
    sortie.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(sortie, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return sortie


def venn_modeles(par_modele: Dict[str, List[str]], sortie: Chemin, titre: Optional[str] = None) -> Path:
    """Diagramme de Venn des lieux distincts trouvés par small / medium / large."""
    from matplotlib_venn import venn3

    noms = ["small", "medium", "large"]
    fig, ax = plt.subplots(figsize=(5, 4))
    venn3([set(par_modele.get(n, [])) for n in noms], noms, set_colors=COULEURS_MODELES, ax=ax)
    if titre:
        ax.set_title(titre)
    return _enregistrer(fig, sortie)


def barres(valeurs: Dict[str, int], titre: str, sortie: Chemin, n: int = 5,
           xlabel: str = "", ylabel: str = "Occurrences") -> Path:
    """Histogramme des ``n`` plus grandes valeurs."""
    items = sorted(valeurs.items(), key=lambda x: x[1], reverse=True)[:n]
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar([k.lstrip("_") for k, _ in items], [v for _, v in items], color="#2e7d32", width=0.5)
    ax.set_title(titre)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.tick_params(axis="x", rotation=20)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    return _enregistrer(fig, sortie)


def matrice_confusion(vp: int, fp: int, fn: int, vn: int, sortie: Chemin, titre: str = "") -> Path:
    """Matrice de confusion : lignes VRAI / FAUX, colonnes POSITIF / NÉGATIF."""
    import seaborn as sns

    fig, ax = plt.subplots(figsize=(4.5, 4))
    sns.heatmap([[vp, vn], [fp, fn]], annot=True, fmt="d", cmap="Reds", cbar=False, ax=ax,
                xticklabels=["POSITIF", "NÉGATIF"], yticklabels=["VRAI", "FAUX"])
    if titre:
        ax.set_title(titre)
    return _enregistrer(fig, sortie)
