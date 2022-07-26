# -*- coding: utf-8 -*-
import spacy
from spacy.scorer import Scorer
from spacy.tokens import Doc
ner_model_path = "fr_core_news_lg"
ner_model = spacy.load(ner_model_path) 



# +
from spacy.training import Example
from itertools import groupby


def evaluate(pred, gold, dic_res):#soit une liste de tuples (start, end, entite) soit juste une liste d'entités
    
    #print(pred)
    ent_pred = [x[-1] for x in pred]
    ent_gold = [x[-1] for x in gold]
    
    count_pred = {x : ent_pred.count(x) for x in ent_pred}
    count_gold = {x : ent_gold.count(x) for x in ent_gold}
    
    liste_VP = set(ent_pred).intersection(set(ent_gold))
    liste_FP = set(ent_pred).difference(set(ent_gold))
    liste_FN = set(ent_gold).difference(set(ent_pred))
    dic_res["data"].append({"Liste_VP":list(liste_VP), "Liste_FP":list(liste_FP), "Liste_FN":list(liste_FN)})
    #pour la macro c'est facile, on compte chaque entité qu'une fois
    dic_res["macro"]["VP"]+=len(liste_VP)
    dic_res["macro"]["FP"]+=len(liste_FP)
    dic_res["macro"]["FN"]+=len(liste_FN)
    
    #Pour la micro mesure on va s'intéresser aux effectifs
    for VP in liste_VP:
        vp = min([count_pred[VP], count_gold[VP]])
        fp = max([0, count_pred[VP] - count_gold[VP]])#Si on a trop d'occurrences
        fn = max([0, count_gold[VP] - count_pred[VP]])#Si on en manque
        dic_res["micro"]["VP"]+= vp
        dic_res["micro"]["FP"]+= fp
        dic_res["micro"]["FN"]+= fn
    for fp in liste_FP:
        dic_res["micro"]["FP"]+= count_pred[fp]
    for fn in liste_FN:
        dic_res["micro"]["FN"]+= count_gold[fn]
    return dic_res

import json
with open("evaluation_tiago1.xlsx.json") as f:
  examples = json.load(f)

dic_res = {"micro":{"VP":0, "FP":0, "FN":0}, "macro":{"VP":0, "FP":0, "FN":0}, "data":[]}

for example in examples:
    text = example["text"]
    txt_traite = ner_model(text)
    locations = [(tok.start, tok.start+len(tok.text), tok.text) for tok in txt_traite.ents if tok.label_=="LOC"]
    dic_res = evaluate(locations, example["entities"], dic_res)
    
print(json.dumps(dic_res, indent =2))


# -

def get_eval(dic_res):
  D = {}
  for type_eval, dic in dic_res.items():
    VP = dic["VP"]
    FP = dic["FP"]
    FN = dic["FN"]
    P = VP/(VP+FP)
    R = VP/(VP+FN)
    F = (2*P*R)/(P+R)
    D[type_eval] = {"Précision":P, "Rappel":R, "F-mesure":F}


