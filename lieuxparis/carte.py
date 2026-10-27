"""Géolocalisation des lieux cités et carte (section 4.4 du mémoire).

Les lieux sont géocodés avec Nominatim (OpenStreetMap) via ``geopy``. Les
réponses sont mises en cache pour ne pas réinterroger le service, et les
requêtes sont espacées d'une seconde comme l'exigent ses conditions d'usage.

Le CSV produit s'importe directement dans Google My Maps ou uMap ; une carte
HTML interactive peut aussi être générée avec ``folium`` (optionnel).
"""

import csv
from pathlib import Path
from typing import Dict, List, Optional, Set

from tqdm import tqdm

from . import config
from .analyse import Index
from .fichiers import Chemin, ecrire_json, lire_json

ENTETE = ["id", "lieu", "artiste", "titre", "date", "adresse", "latitude", "longitude"]


def geocoder(lieux: Set[str], cache: Chemin = config.CACHE_GEOCODAGE,
             contexte: str = "Paris, Île-de-France, France",
             agent: str = "memoire-lieux-paris") -> Dict[str, Optional[dict]]:
    """Renvoie {lieu: {"adresse", "latitude", "longitude"} ou None si introuvable}."""
    from geopy.exc import GeopyError
    from geopy.extra.rate_limiter import RateLimiter
    from geopy.geocoders import Nominatim

    deja: Dict[str, Optional[dict]] = lire_json(cache) if Path(cache).exists() else {}
    a_faire = sorted(l for l in lieux if l not in deja)
    if a_faire:
        geocode = RateLimiter(Nominatim(user_agent=agent, timeout=30).geocode,
                              min_delay_seconds=1, max_retries=1, swallow_exceptions=False)
        try:
            for i, lieu in enumerate(tqdm(a_faire, desc="Géocodage", unit="lieu"), start=1):
                loc = geocode(f"{lieu}, {contexte}")
                deja[lieu] = ({"adresse": loc.address, "latitude": loc.latitude, "longitude": loc.longitude}
                              if loc else None)
                if i % 25 == 0:
                    ecrire_json(cache, deja)
        except GeopyError as err:
            # Service injoignable : on garde ce qui a été fait, la prochaine exécution reprendra.
            print(f"Géocodage interrompu ({type(err).__name__}) — relancez la commande plus tard.")
        ecrire_json(cache, deja)
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


def periode(date: str) -> str:
    """Périodes utilisées sur les cartes du mémoire."""
    if not date[:4].isdigit():
        return "sans date"
    a = int(date[:4])
    return "1940-2000" if a <= 2000 else "2001-2010" if a <= 2010 else "2011-2019" if a <= 2019 else "2020+"


COULEURS_PERIODES = {"1940-2000": "#6a1b9a", "2001-2010": "#1565c0", "2011-2019": "#2e7d32",
                     "2020+": "#ef6c00", "sans date": "#757575"}


def carte_html(lignes: List[dict], sortie: Chemin) -> Path:
    """Carte interactive (nécessite ``pip install folium``)."""
    import folium

    m = folium.Map(location=[48.8566, 2.3522], zoom_start=11, tiles="OpenStreetMap")
    for l in lignes:
        p = periode(l["date"])
        folium.CircleMarker(
            location=[float(l["latitude"]), float(l["longitude"])], radius=5,
            color=COULEURS_PERIODES[p], fill=True, fill_opacity=0.8,
            popup=folium.Popup(f"<b>{l['lieu']}</b><br>{l['titre']}<br>{l['date'] or 'sans date'}", max_width=300),
            tooltip=f"{l['lieu']} ({p})",
        ).add_to(m)
    legende = "".join(f'<div><span style="color:{c}">●</span> {p}</div>' for p, c in COULEURS_PERIODES.items())
    m.get_root().html.add_child(folium.Element(
        f'<div style="position:fixed;bottom:20px;left:20px;z-index:999;background:white;'
        f'padding:8px 12px;border-radius:6px;font:13px sans-serif;box-shadow:0 1px 4px #0003">{legende}</div>'))
    sortie = Path(sortie)
    sortie.parent.mkdir(parents=True, exist_ok=True)
    m.save(str(sortie))
    return sortie
