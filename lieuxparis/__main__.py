"""Interface en ligne de commande : ``python -m lieuxparis <commande> [options]``.

Lancez ``python -m lieuxparis --help`` ou ``python -m lieuxparis <commande> --help``.
"""

import argparse
import json
import re
import sys
from pathlib import Path

from . import config


def _afficher(obj) -> None:
    print(json.dumps(obj, ensure_ascii=False, indent=2))


def _nom_fichier(texte: str) -> str:
    return re.sub(r"[^\w-]+", "_", texte.lstrip("_")).strip("_").lower() or "sans_nom"


# --------------------------------------------------------------------------- #
# Commandes
# --------------------------------------------------------------------------- #

def cmd_stats(a):
    from .corpus import charger_corpus, statistiques
    _afficher(statistiques(charger_corpus(a.corpus, a.artiste)))


def cmd_lexique(a):
    from .lexique import charger_lexique, classer_lieux, lexique_par_fichier
    lexique = charger_lexique()
    print(f"{len(lexique)} lieux distincts\n\nPar fichier source :")
    for nom, n in sorted(lexique_par_fichier().items(), key=lambda x: -x[1]):
        print(f"  {n:6d}  {nom}")
    print("\nPar catégorie :")
    for cat, lieux in sorted(classer_lieux(lexique).items(), key=lambda x: -len(x[1])):
        print(f"  {len(lieux):6d}  {100 * len(lieux) / len(lexique):5.1f} %  {cat}")


def cmd_ner(a):
    from .corpus import charger_corpus
    from .ner import extraire_lieux
    chansons = charger_corpus(a.corpus, a.artiste)
    extraire_lieux(chansons, a.modeles, sortie=a.sortie)
    print(f"Résultats enregistrés dans {a.sortie}")


def cmd_comparer(a):
    from .fichiers import lire_json
    from .ner import comparer_modeles, lieux_par_modele
    par_modele = lieux_par_modele(lire_json(a.entites), a.artiste)
    _afficher(comparer_modeles(par_modele))
    if a.venn:
        from .visualisation import venn_modeles
        print(f"Diagramme : {venn_modeles(par_modele, a.venn, a.titre)}")


def cmd_pretraiter(a):
    from .corpus import charger_corpus, vers_format_pretraite
    from .fichiers import ecrire_json
    from .lexique import charger_lexique
    from .truecasing import charger_glaff, matrice, pretraiter
    chansons, decisions = pretraiter(charger_corpus(a.corpus, a.artiste),
                                     charger_glaff(a.glaff), charger_lexique())
    ecrire_json(a.sortie, vers_format_pretraite(chansons))
    m = matrice(decisions)
    _afficher({"decisions": dict(decisions), "matrice": m})
    print(f"Corpus pré-traité : {a.sortie}")
    if a.matrice:
        from .visualisation import matrice_confusion
        print(f"Matrice : {matrice_confusion(m['VP'], m['FP'], m['FN'], m['VN'], a.matrice, 'True casing')}")


def cmd_proportions(a):
    from .corpus import charger_corpus
    from .fichiers import ecrire_json
    from .lexique import charger_lexique
    from .proportions import calculer, tableau_latex
    res = calculer(charger_corpus(a.corpus, a.artiste), a.modele, charger_lexique())
    sortie = a.sortie or config.DOSSIER_PROPORTIONS / _nom_fichier(a.artiste[0] if a.artiste else "corpus") / f"proportions_{a.modele}.json"
    ecrire_json(sortie, res)
    print(f"Proportions : {sortie}")
    if a.latex:
        Path(a.latex).write_text(tableau_latex(res), encoding="utf-8")
        print(f"Tableau LaTeX : {a.latex}")


def _index(a, filtrer=True):
    from .analyse import construire_index, filtrer_lexique
    from .corpus import charger_corpus
    from .fichiers import lire_json
    from .lexique import charger_lexique
    index = construire_index(lire_json(a.entites), a.modele, charger_corpus(a.corpus))
    lexique = charger_lexique()
    return (filtrer_lexique(index, lexique) if filtrer and not a.tous_les_lieux else index), lexique


def cmd_analyser(a):
    from . import analyse
    from .fichiers import ecrire_json
    index, _ = _index(a)
    dossier = Path(a.dossier)
    sorties = {
        "lieux_par_artiste": analyse.lieux_par_artiste(index),
        "artistes_par_lieu": analyse.artistes_par_lieu(index),
        "chansons_par_lieu": analyse.chansons_par_lieu(index),
        "frequence_lieux": analyse.frequence_lieux(index),
        "lieux_par_annee": analyse.lieux_par_annee(index),
        "lieux_par_periode": analyse.lieux_par_periode(index),
    }
    for nom, contenu in sorties.items():
        ecrire_json(dossier / f"{nom}_{a.modele}.json", contenu)
    print(f"{len(sorties)} fichiers écrits dans {dossier}/\n\nLieux les plus cités :")
    for lieu, n in analyse.top(sorties["frequence_lieux"], 15).items():
        print(f"  {n:5d}  {lieu}")


def cmd_graphique(a):
    from . import analyse
    from .visualisation import barres
    index, _ = _index(a)
    dossier = Path(a.dossier) / a.modele
    if a.lieu:
        donnees = analyse.artistes_par_lieu(index).get(a.lieu, {})
        titre, nom = f"Artistes citant « {a.lieu} »", a.lieu
    elif a.artiste:
        donnees = analyse.lieux_par_artiste(index).get(a.artiste, {})
        titre, nom = f"Lieux cités par {a.artiste.lstrip('_')}", a.artiste
    else:
        donnees = analyse.lieux_par_annee(index, a.annee).get(str(a.annee), {})
        titre, nom = f"Lieux cités en {a.annee}", str(a.annee)
    if not donnees:
        sys.exit("Aucune donnée pour cette recherche.")
    _afficher(analyse.top(donnees, a.n))
    print(f"Graphique : {barres(donnees, titre, dossier / f'{_nom_fichier(nom)}.png', n=a.n)}")


def cmd_chercher(a):
    from .analyse import chansons_par_lieu
    index, _ = _index(a, filtrer=False)
    resultat = chansons_par_lieu(index).get(a.lieu)
    if not resultat:
        sys.exit(f"« {a.lieu} » n'a été trouvé dans aucune chanson.")
    for artiste, chansons in resultat.items():
        for titre, date in chansons:
            print(f"{artiste.lstrip('_'):25s} {date or 'sans date':12s} {titre}")


def cmd_evaluer(a):
    from .evaluation import evaluer
    from .fichiers import ecrire_json
    res = evaluer(a.reference, a.modele)
    _afficher({"comptes": res["comptes"], "scores": res["scores"]})
    if a.sortie:
        ecrire_json(a.sortie, res)


def cmd_enrichir(a):
    from .enrichissement import enrichir
    from .fichiers import lire_json
    from .lexique import charger_lexique
    from .ner import lieux_par_modele
    candidats = {l for lieux in lieux_par_modele(lire_json(a.entites), a.artiste).values() for l in lieux}
    enrichir(candidats, charger_lexique())


def cmd_carte(a):
    from .carte import carte_plotly, ecrire_csv, lire_csv, points
    if a.depuis_csv:
        lignes = lire_csv(a.csv)
    else:
        index, lexique = _index(a, filtrer=False)
        lignes = points(index, lexique)
        print(f"{len(lignes)} points : {ecrire_csv(lignes, a.csv)}")
    if a.html:
        print(f"Carte interactive : {carte_plotly(lignes, a.html)}")


# --------------------------------------------------------------------------- #
# Analyseur d'arguments
# --------------------------------------------------------------------------- #

def construire_parseur() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="python -m lieuxparis",
                                description="Lieux de Paris dans la chanson francophone — outils du mémoire.")
    sp = p.add_subparsers(dest="commande", required=True, metavar="<commande>")

    def ajout(nom, fonction, aide):
        s = sp.add_parser(nom, help=aide, description=aide)
        s.set_defaults(fonction=fonction)
        return s

    def opt_corpus(s, defaut=config.CORPUS_PRETRAITE):
        s.add_argument("--corpus", type=Path, default=defaut, help=f"corpus JSON (défaut : {defaut.relative_to(config.RACINE)})")

    def opt_artistes(s):
        s.add_argument("--artiste", nargs="+", help="clé(s) d'artiste à garder (ex. _113 « Jacques Dutronc »)")

    def opt_index(s):
        opt_corpus(s)
        s.add_argument("--entites", type=Path, default=config.ENTITES_AVANT,
                       help="résultats de la REN (défaut : resultats/entites/avant_pretraitement.json)")
        s.add_argument("--modele", default="large", choices=list(config.MODELES_SPACY))
        s.add_argument("--tous-les-lieux", action="store_true",
                       help="garder tous les lieux détectés, pas seulement ceux du lexique")

    s = ajout("stats", cmd_stats, "statistiques sur un corpus")
    opt_corpus(s); opt_artistes(s)

    ajout("lexique", cmd_lexique, "taille et catégories du lexique des lieux de Paris")

    s = ajout("ner", cmd_ner, "détecter les lieux avec spaCy (small / medium / large)")
    opt_corpus(s); opt_artistes(s)
    s.add_argument("--modeles", nargs="+", default=["small", "medium", "large"], choices=list(config.MODELES_SPACY))
    s.add_argument("--sortie", type=Path, required=True, help="fichier JSON de résultats (sert aussi de reprise)")

    s = ajout("comparer", cmd_comparer, "comparer les lieux trouvés par les trois modèles (+ diagramme de Venn)")
    s.add_argument("--entites", type=Path, default=config.ENTITES_APRES)
    s.add_argument("--artiste", help="limiter à un artiste")
    s.add_argument("--venn", type=Path, help="enregistrer le diagramme de Venn (PNG)")
    s.add_argument("--titre", help="titre du diagramme")

    s = ajout("pretraiter", cmd_pretraiter, "true casing + espaces autour des retours à la ligne")
    opt_corpus(s, config.CORPUS_ECHANTILLON); opt_artistes(s)
    s.add_argument("--glaff", type=Path, default=config.GLAFF_FREQUENCES)
    s.add_argument("--sortie", type=Path, required=True)
    s.add_argument("--matrice", type=Path, help="enregistrer la matrice de confusion (PNG)")

    s = ajout("proportions", cmd_proportions, "proportions d'entités nommées et de majuscules par chanson")
    opt_corpus(s); opt_artistes(s)
    s.add_argument("--modele", default="large", choices=list(config.MODELES_SPACY))
    s.add_argument("--sortie", type=Path)
    s.add_argument("--latex", type=Path, help="écrire aussi un tableau LaTeX")

    s = ajout("analyser", cmd_analyser, "index artistes ↔ lieux ↔ années (fichiers JSON)")
    opt_index(s)
    s.add_argument("--dossier", type=Path, default=config.DOSSIER_ANALYSE)

    s = ajout("graphique", cmd_graphique, "histogramme top N pour un lieu, un artiste ou une année")
    opt_index(s)
    g = s.add_mutually_exclusive_group(required=True)
    g.add_argument("--lieu"); g.add_argument("--artiste"); g.add_argument("--annee", type=int)
    s.add_argument("-n", type=int, default=5)
    s.add_argument("--dossier", type=Path, default=config.DOSSIER_FIGURES / "top5")

    s = ajout("chercher", cmd_chercher, "dans quelles chansons un lieu est-il cité ?")
    opt_index(s)
    s.add_argument("lieu")

    s = ajout("evaluer", cmd_evaluer, "précision / rappel / F-mesure face à une annotation manuelle")
    s.add_argument("reference", type=Path, help="JSON d'annotations [{text, entities}]")
    s.add_argument("--modele", default="large", choices=list(config.MODELES_SPACY))
    s.add_argument("--sortie", type=Path, help="enregistrer le détail (JSON)")

    s = ajout("enrichir", cmd_enrichir, "compléter le lexique à la main avec les lieux trouvés par spaCy")
    s.add_argument("--entites", type=Path, default=config.ENTITES_APRES)
    s.add_argument("--artiste")

    s = ajout("carte", cmd_carte, "géolocaliser les lieux cités (CSV) et/ou produire une carte HTML")
    opt_index(s)
    s.add_argument("--csv", type=Path, default=config.CARTE_CSV)
    s.add_argument("--html", type=Path, help="carte interactive HTML (plotly)")
    s.add_argument("--depuis-csv", action="store_true", help="ne pas géocoder : partir du CSV existant")
    return p


def main(argv=None):
    args = construire_parseur().parse_args(argv)
    args.fonction(args)


if __name__ == "__main__":
    main()
