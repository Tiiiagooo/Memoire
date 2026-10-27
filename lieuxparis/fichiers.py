"""Lecture / écriture de fichiers JSON."""

import json
from pathlib import Path
from typing import Any, Union

Chemin = Union[str, Path]


def lire_json(chemin: Chemin) -> Any:
    with open(chemin, encoding="utf-8") as f:
        return json.load(f)


def ecrire_json(chemin: Chemin, contenu: Any, indent: int = 2) -> Path:
    chemin = Path(chemin)
    chemin.parent.mkdir(parents=True, exist_ok=True)
    with open(chemin, "w", encoding="utf-8") as f:
        json.dump(contenu, f, ensure_ascii=False, indent=indent)
    return chemin
