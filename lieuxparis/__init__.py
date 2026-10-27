"""Observer automatiquement l'évocation des lieux de Paris dans la chanson francophone.

Code du mémoire de M1 « Langue et Informatique » (Sorbonne Université, 2022),
réorganisé en modules :

- :mod:`lieuxparis.corpus`        lecture des corpus de paroles et statistiques
- :mod:`lieuxparis.lexique`       lexique des lieux de Paris et catégories
- :mod:`lieuxparis.ner`           détection des entités nommées avec spaCy
- :mod:`lieuxparis.truecasing`    pré-traitement (adaptation de la casse avec le GLAFF)
- :mod:`lieuxparis.proportions`   proportions d'entités / de majuscules par chanson
- :mod:`lieuxparis.analyse`       index artistes ↔ lieux ↔ années
- :mod:`lieuxparis.evaluation`    précision, rappel, F-mesure (micro et macro)
- :mod:`lieuxparis.visualisation` diagrammes de Venn, histogrammes, matrices
- :mod:`lieuxparis.carte`         géolocalisation des lieux et carte
- :mod:`lieuxparis.enrichissement` enrichissement manuel du lexique

L'ensemble est pilotable en ligne de commande : ``python -m lieuxparis --help``.
"""

__version__ = "1.0.0"
