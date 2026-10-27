"""Géolocalisation des lieux cités et carte (section 4.4 du mémoire).

Deux étapes :

1. **Géocodage** avec Nominatim (OpenStreetMap) via ``geopy``. La recherche est
   limitée à l'Île-de-France (sinon « Chapelle » ou « Vincennes » peuvent
   atterrir n'importe où en France), les requêtes sont espacées d'une seconde
   comme l'exigent les conditions d'usage du service, et les réponses sont mises
   en cache dans ``resultats/carte/cache_geocodage.json``.

2. **Carte interactive** avec plotly : un point par lieu et par période, dont la
   taille dépend du nombre de chansons qui le citent. Le survol affiche les
   chansons ; un clic sur la légende masque ou affiche une période.

Le CSV intermédiaire s'importe aussi dans Google My Maps ou uMap.
"""

import csv
import math
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Optional, Set

from tqdm import tqdm

from . import config
from .analyse import Index
from .fichiers import Chemin, ecrire_json, lire_json

ENTETE = ["id", "lieu", "artiste", "titre", "date", "adresse", "latitude", "longitude"]

# Rectangle englobant l'Île-de-France : (sud-ouest, nord-est) en (latitude, longitude).
ILE_DE_FRANCE = [(48.12, 1.44), (49.24, 3.56)]


# --------------------------------------------------------------------------- #
# Géocodage
# --------------------------------------------------------------------------- #

def geocoder(lieux: Set[str], cache: Chemin = config.CACHE_GEOCODAGE,
             agent: str = "memoire-lieux-paris") -> Dict[str, Optional[dict]]:
    """Renvoie {lieu: {"adresse", "latitude", "longitude"} ou None si introuvable}.

    Chaque lieu est d'abord cherché comme « <lieu>, Paris », puis seul ; dans les
    deux cas seuls les résultats situés en Île-de-France sont acceptés.
    """
    from geopy.exc import GeopyError
    from geopy.extra.rate_limiter import RateLimiter
    from geopy.geocoders import Nominatim

    deja: Dict[str, Optional[dict]] = lire_json(cache) if Path(cache).exists() else {}
    a_faire = sorted(l for l in lieux if l not in deja)
    if not a_faire:
        return deja

    nominatim = Nominatim(user_agent=agent, timeout=30)
    geocode = RateLimiter(nominatim.geocode, min_delay_seconds=1, max_retries=1, swallow_exceptions=False)
    try:
        for i, lieu in enumerate(tqdm(a_faire, desc="Géocodage", unit="lieu"), start=1):
            loc = None
            for requete in (f"{lieu}, Paris", lieu):
                loc = geocode(requete, viewbox=ILE_DE_FRANCE, bounded=True, country_codes="fr")
                if loc:
                    break
            deja[lieu] = ({"adresse": loc.address, "latitude": loc.latitude, "longitude": loc.longitude}
                          if loc else None)
            if i % 25 == 0:
                ecrire_json(cache, deja)
    except GeopyError as err:
        # Service injoignable : on garde ce qui a été fait, la prochaine exécution reprendra.
        print(f"Géocodage interrompu ({type(err).__name__}) — relancez la commande plus tard.")
    ecrire_json(cache, deja)
    introuvables = sorted(l for l in a_faire if l in deja and deja[l] is None)
    if introuvables:
        print(f"{len(introuvables)} lieux introuvables (ex. : {', '.join(introuvables[:5])}). "
              "Vous pouvez les corriger à la main dans le cache.")
    return deja


def points(index: Index, lexique: Set[str], exclus: Set[str] = config.LIEUX_EXCLUS_CARTE,
           cache: Chemin = config.CACHE_GEOCODAGE) -> List[dict]:
    """Une ligne par (lieu, chanson) pour les lieux du lexique, géolocalisée."""
    occurrences = [(lieu, l) for l in index for lieu in dict.fromkeys(l["lieux"])
                   if lieu in lexique and lieu not in exclus]
    coords = geocoder({lieu for lieu, _ in occurrences}, cache=cache)
    sortie = []
    for lieu, ligne in occurrences:
        c = coords.get(lieu)
        if c:
            sortie.append({"id": len(sortie), "lieu": lieu, "artiste": ligne["artiste"].lstrip("_"),
                           "titre": ligne["titre"].replace("\xa0", " "),
                           "date": ligne["date"] or "", **c})
    return sortie


def ecrire_csv(lignes: List[dict], sortie: Chemin = config.CARTE_CSV) -> Path:
    sortie = Path(sortie)
    sortie.parent.mkdir(parents=True, exist_ok=True)
    with open(sortie, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=ENTETE, delimiter=";")
        w.writeheader()
        w.writerows(lignes)
    return sortie


def lire_csv(chemin: Chemin = config.CARTE_CSV) -> List[dict]:
    with open(chemin, encoding="utf-8") as f:
        return list(csv.DictReader(f, delimiter=";"))


# --------------------------------------------------------------------------- #
# Carte plotly
# --------------------------------------------------------------------------- #

# Périodes des cartes du mémoire, dans l'ordre chronologique.
PERIODES = ["1940-2000", "2001-2010", "2011-2019", "2020+", "sans date"]

# Palette Okabe-Ito : lisible par les personnes daltoniennes.
COULEURS_PERIODES = {"1940-2000": "#E69F00", "2001-2010": "#0072B2", "2011-2019": "#009E73",
                     "2020+": "#CC79A7", "sans date": "#999999"}


def periode(date: str) -> str:
    if not (date or "")[:4].isdigit():
        return "sans date"
    a = int(date[:4])
    return "1940-2000" if a <= 2000 else "2001-2010" if a <= 2010 else "2011-2019" if a <= 2019 else "2020+"


def regrouper(lignes: List[dict], max_titres: int = 8) -> List[dict]:
    """Regroupe les citations par (lieu, période) : une bulle par groupe.

    Quand un même lieu est cité à plusieurs périodes, les bulles sont légèrement
    décalées autour du point réel pour ne pas se recouvrir.
    """
    groupes: Dict[tuple, dict] = {}
    for l in lignes:
        cle = (l["lieu"], periode(l["date"]))
        g = groupes.setdefault(cle, {"lieu": l["lieu"], "periode": cle[1], "adresse": l["adresse"],
                                     "lat": float(l["latitude"]), "lon": float(l["longitude"]),
                                     "chansons": [], "artistes": set()})
        g["chansons"].append(f"{l['titre']} ({l['date'][:4] or 's.d.'})")
        g["artistes"].add(l["artiste"])

    periodes_par_lieu = defaultdict(list)
    for lieu, p in groupes:
        periodes_par_lieu[lieu].append(p)

    sortie = []
    for (lieu, p), g in groupes.items():
        voisines = sorted(periodes_par_lieu[lieu], key=PERIODES.index)
        if len(voisines) > 1:  # petit décalage en cercle (≈ 150 m)
            angle = 2 * math.pi * voisines.index(p) / len(voisines)
            g["lat"] += 0.0013 * math.sin(angle)
            g["lon"] += 0.002 * math.cos(angle)
        n = len(g["chansons"])
        liste = "<br>".join("• " + c for c in g["chansons"][:max_titres])
        if n > max_titres:
            liste += f"<br>… et {n - max_titres} autres"
        sortie.append({**g, "n": n, "nb_artistes": len(g["artistes"]), "liste": liste})
    return sortie


def carte_plotly(lignes: List[dict], sortie: Chemin,
                 titre: str = "Lieux de Paris cités dans la chanson francophone",
                 autonome: bool = False, fond: str = "carto-positron") -> Path:
    """Carte interactive HTML (nécessite ``pip install plotly``).

    Avec ``autonome=True``, la bibliothèque plotly.js est incluse dans le fichier
    (≈ 5 Mo) : la page s'ouvre sans dépendre du CDN de plotly.
    ``fond`` : style du fond de carte (« carto-positron », « open-street-map »,
    « carto-darkmatter », « white-bg » pour un fond blanc hors ligne…).
    """
    import plotly.graph_objects as go

    bulles = regrouper(lignes)
    fig = go.Figure()
    for p in PERIODES:
        groupe = sorted((b for b in bulles if b["periode"] == p), key=lambda b: -b["n"])
        if not groupe:
            continue
        fig.add_trace(go.Scattermap(
            name=f"{p} ({sum(b['n'] for b in groupe)})",
            lat=[b["lat"] for b in groupe],
            lon=[b["lon"] for b in groupe],
            mode="markers",
            marker=dict(size=[8 + 5 * math.sqrt(b["n"]) for b in groupe],
                        color=COULEURS_PERIODES[p], opacity=0.8),
            customdata=[[b["lieu"], b["n"], b["nb_artistes"], b["liste"], p] for b in groupe],
            hovertemplate=("<b>%{customdata[0]}</b> — %{customdata[4]}<br>"
                           "%{customdata[1]} chanson(s), %{customdata[2]} artiste(s)<br><br>"
                           "%{customdata[3]}<extra></extra>"),
        ))

    fig.update_layout(
        title=dict(text=f"{titre}<br><sup>Taille = nombre de chansons · "
                        "cliquez sur une période pour la masquer</sup>", x=0.01),
        map=dict(style=fond, center=dict(lat=48.8566, lon=2.3522), zoom=10),
        legend=dict(title="Période (nb de citations)", x=0.01, y=0.02, bgcolor="rgba(255,255,255,0.85)"),
        hoverlabel=dict(bgcolor="white", font_size=12, align="left"),
        margin=dict(l=0, r=0, t=60, b=0),
    )
    sortie = Path(sortie)
    sortie.parent.mkdir(parents=True, exist_ok=True)
    fig.write_html(sortie, include_plotlyjs=True if autonome else "cdn", config={"scrollZoom": True, "displaylogo": False})
    return sortie
