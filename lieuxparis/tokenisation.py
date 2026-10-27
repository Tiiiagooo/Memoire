"""Découpage des paroles en mots.

Le tokeniseur reprend l'expression régulière utilisée dans le mémoire : il garde
ensemble les sigles à points (« C.N.R.S. »), les mots composés à trait d'union
(« Mini-moke ») et isole la ponctuation.
"""

import re
from typing import List

MOTIF_MOT = re.compile(r"\w[\w.]+|\w+-\w+|\w+\S|\w+|\S")

# Premier mot d'une ligne : « j' », « c' », « un-mot » ou un mot simple.
MOTIF_DEBUT_LIGNE = re.compile(r"^(\w+['’]|\w+-\w+|\w+)")


def tokeniser(texte: str) -> List[str]:
    """Renvoie la liste des mots (et signes de ponctuation) d'un texte."""
    return MOTIF_MOT.findall(texte or "")
