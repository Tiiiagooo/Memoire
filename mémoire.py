#!/usr/bin/env python
# coding: utf-8

# In[1]:


#load le modèle medium
#!python -m spacy download fr_core_news_md


# # Ouverture et lecture des json

# In[1]:


#ouverture et lecture des json
import nltk
import spacy
import json
import tqdm
import spacy
def ouvrir_json(chemin):
    f = open(chemin, encoding="UTF-8")
    toto = json.load(f)
    f.close()
    return toto

def ecrire_fichier(chemin, contenu):
  w = open(chemin, "w", encoding="utf-8")
  w.write(contenu)
  w.close()
def lire_fichier(chemin):
  f = open(chemin, "r", encoding="utf-8")
  chaine = f.read()
  f.close()
  return chaine
def Splittxt(txt):
    tokenizer = nltk.RegexpTokenizer(r"(\w+-\w+|\w+\S|(\w\.)*\w.|\w+|\S|\w+\S|\?|\!)")
    txt_split = tokenizer.tokenize(txt)
    return 
def Splittxt4(txt):
    tokenizer = nltk.RegexpTokenizer(r"(\w+-\w+|\w+\S|((\w\.)*\w.)|\w+|\S|\w+\S|\?|\!)")
    txt_split = tokenizer.tokenize(txt)
    return 
def Splittxt3(txt):
    tokenizer = nltk.RegexpTokenizer(r"(\w[\w\.]{1,}|\w+-\w+|\w+\S|\w+|\S|\w+\S|\?|\!)")
    txt_split = tokenizer.tokenize(txt)
    return txt_split
def Splittxt2(txt):
    tokenizer = nltk.RegexpTokenizer(r"(\w+'|\w+-\w+|\w+|\S|\w+\S)")
    txt_split = tokenizer.tokenize(txt)
    return txt_split
#création d'une liste des lieux de paris
import glob
import re

chemin = glob.glob('lieux_paris/*/*')
vrai_entite_nomme = []
dic_lieu = {}
for i in chemin:
    lieux_de_paris = ouvrir_json(i)
    for lieu in lieux_de_paris:
        #print(lieu)
        vrai_entite_nomme.append(lieu)


# In[23]:


phrase = "bonjour, je \t m'appel Tiago\n \n C.N.R.S., R.A.T.T.T.T.T.P"
#nlp = spacy.load('fr_core_news_lg')
to_spacy = []
x = Splittxt3(phrase) 
doc = nlp(phrase)
for token in doc:
    to_spacy.append(token.text)
    
print(to_spacy)
print(x)
print(len(to_spacy))
print(len(x))


# In[ ]:





# # Affichage des paroles du fichier

# In[2]:


liste_models = [["small",  spacy.load('fr_core_news_sm')], #modèle small
                ["medium", spacy.load('fr_core_news_md')], #modèle medium
                ["large",  spacy.load('fr_core_news_lg')]] #modèle large
modele = ["small" , "medium", "large"]


# In[185]:


#pour afficher paroles des chansons du fichier echantillon1.json

import json
corpus = ouvrir_json("tmp.json")
#start = i["_113"]

#print(start)
#1/0
#une liste vide pour regrouper tous les listes de txt (chaque txt et dans une liste)
tous_les_txt = []
#corpus = {"_113":corpus["_113"]}
dic_name = {}
with open("all_entites.json", encoding="utf-8") as f:
    all_entites = json.load(f)
import tqdm
cpt = 0
for nom_artiste, liste_chansons in tqdm.tqdm(corpus.items()):
  
  print(nom_artiste)
  for element in liste_chansons:
    liste_txt = []
    txt = element["lyrics"]
    try:
        txt = str(txt)
    except:
        continue
    titre = element["full_title"]
    all_entites.setdefault(nom_artiste, {})
    all_entites[nom_artiste].setdefault(titre, {})
    if cpt%100==0:
        print(cpt, "chansons faites")
    if len(all_entites[nom_artiste][titre])==3:
        cpt+=1
        continue
    for nom_modele, nlp in liste_models:
        if nom_modele not in  all_entites[nom_artiste][titre]:
            doc = nlp(txt)
            entites = [ent.text for ent in doc.ents if ent.label_=="LOC"]
            all_entites[nom_artiste][titre][nom_modele]= entites
    cpt+=1
    #liste_txt.append(txt)
    #tous_les_txt.append(liste_txt)
    #if cpt%100==0:
        #break
  #if cpt%100==0:
        #break
    
    #print(titre)
    #print(liste_txt, "-"*70)print(len(tous_les_txt))
print(cpt, "chansons faites")
#chanteur = "Jacques Dutronc"
with open("all_entites.json", "w", encoding="utf-8") as w:
    w.write(json.dumps(all_entites, indent=2, ensure_ascii=False))
#print(json.dumps(all_entites, indent =2))


# In[175]:


#for nom_artiste, valeur in all_entites.items():
    #print(nom_artiste)


# # State sur le corpus.

# In[178]:


artiste = []
toutes_les_chansons = []
tous_les_mots = []
nbre_de_texte_traitable = 0
nbre_de_texte_non_traitable = 0
nbre_de_mot_totale = 0
nbre_de_mot_par_chanson = []

for nom_artiste, donnee in tqdm.tqdm(corpus.items()):
    for element in donnee:
        chansons = []
        try:
            #txt = str(parole)
            parole = element["lyrics"]
            chansons.append(parole)
            toutes_les_chansons.append(chansons)
            #nbre_de_texte_traitable += 1
        except:
            chansons.append(None)
            toutes_les_chansons.append(chansons)
            #nbre_de_texte_non_traitable += 1
        titre = element["full_title"]

        
        
        
        
        
        
        
"""
for liste_chansons in tqdm.tqdm(toutes_les_chansons):
    for chanson in liste_chansons:
        try:
            mots = Splittxt3(chanson)
            tous_les_mots.append(mots)
        except:
            tous_les_mots.append([])
        if chanson != None:
            nbre_de_texte_traitable += 1
        else:
            nbre_de_texte_non_traitable += 1
    #artiste.append(chanteur)
print(nbre_de_texte_non_traitable)
print(nbre_de_texte_traitable)
#print(tous_les_mots)
for liste_mots in tqdm.tqdm(tous_les_mots):
    nbre_de_mot_par_chanson.append(len(liste_mots))
    nbre_de_mot_par_chanson.append(0)
    for mot in liste_mots:
        nbre_de_mot_totale += 1
#print(nbre_de_mot_par_chanson)
#print(nbre_de_mot_totale)"""


# In[ ]:





# In[4]:


locatif_sm_before_pre_T = []
locatif_md_before_pre_T = []
locatif_lg_before_pre_T = []
k = 0 

chanteur = "_113"
with open("all_entites.json", encoding="utf-8") as f:
    all_entites = json.load(f)
for artiste, donnee in all_entites.items():
    #print(artiste)
    if artiste == chanteur:
    #if 2 > 1:
        for titre_musique, modele in donnee.items():
            for modele_3, EN in modele.items():
                if modele_3 == "small":
                    for entities in EN:
                        locatif_sm_before_pre_T.append(entities)
                if modele_3 == "medium":
                    for entities in EN:
                        locatif_md_before_pre_T.append(entities)
                if modele_3 == "large":
                    for entities in EN:
                        locatif_lg_before_pre_T.append(entities)
                    #print(y)
            #if modele.keys() == "small":
                #print("oui")
               
            


# # Affichage des EN trouvé par Spacy

# In[8]:


#!python −m spacy download fr_core_news_sm
#!python −m spacy download fr_core_news_md
#!python −m spacy download fr_core_news_lg


# In[5]:


#nlp = spacy.load('fr_core_news_sm') #modèle small
#nlp = spacy.load('fr_core_news_md') #modèle medium
#nlp = spacy.load('fr_core_news_lg') #modèle large
#modele = ["small" , "medium", "large"]
#modele_actif = 2


# In[ ]:





# In[10]:


"""#affichage des EN trouvé par spacy
import nltk
from nltk.tokenize import word_tokenize
import re
import spacy

nlp = spacy.load('fr_core_news_sm') #modèle small
#nlp = spacy.load('fr_core_news_md') #modèle medium
#nlp = spacy.load('fr_core_news_lg') #modèle large
compteur = 0
tokenizer = nltk.RegexpTokenizer(r"(\w+,\w+|\w+-\w+|\w+\.\w+\.\w+|\w+\S|\w+|\S|\w+\S|\?|\!)") #Pour les mots du texte javai pour le 1er
                                                                                              #600 résultats
                                                                                              # j'ai utiliser tokenizer pour séparer les mots du texte.
        
        
EN = []
locatif_small_before_pre_T = []

print("#"*50, "\nvoici les musiques sur lequels l'on va travailler")
#--------------------------------------------------------------------------------------------------------------------


for element in liste_chansons:
        l = element["lyrics"]
        #print(len(tokenizer.tokenize(l)))
        try:
            doc = nlp(l)
            compteur += 1
#--------------------------------------------------------------------------------------------------------------------
            entite_nomme = [] #Initialisation de la liste des entite nommé trouvé par spacy
            
            print("-"*70,"\n Texte numero %s"%(compteur))
            print(doc)
            #print("Ce texte contient ", len(l), " mot")
            split_txt = tokenizer.tokenize(l)
            
            print("\n Ce texte contient ", len(split_txt), " mot d'après mon tokenizer")
            

            print("\n","Traitement...","\n")
            for ent in doc.ents:
                #print(ent.text)
                #print(ent, ent.label_)
                if ent.label_ == "LOC":
                    locatif = ent.text
                    entite_nomme.append(locatif)
                    locatif_small_before_pre_T.append(locatif)
            #print("\n Ce texte contient ", longueur_mots_spacy, " mot d'après spacy")
            print("\n Le texte a trouvé {} Entité Nommé locatif, ce sont: ".format(len(entite_nomme)))
            print(set(entite_nomme))
            EN.append(entite_nomme)
            print(EN)
        except:
            pass
       

    
    #print(type(l))
#etiquettage étrange à cause des maj? et il faut comprendre l'étiquettage."""


# In[ ]:





# In[11]:


"""#affichage des EN trouvé par spacy
import nltk
from nltk.tokenize import word_tokenize
import re
import spacy

#nlp = spacy.load('fr_core_news_sm') #modèle small
nlp = spacy.load('fr_core_news_md') #modèle medium
#nlp = spacy.load('fr_core_news_lg') #modèle large
compteur = 0
tokenizer = nltk.RegexpTokenizer(r"(\w+,\w+|\w+-\w+|\w+\.\w+\.\w+|\w+\S|\w+|\S|\w+\S|\?|\!)") #Pour les mots du texte javai pour le 1er
                                                                                              #600 résultats
                                                                                              # j'ai utiliser tokenizer pour séparer les mots du texte.
        
        
EN_md = []
locatif_md_before_pre_T = []
print("#"*50, "\nvoici les musiques sur lequels l'on va travailler")
#--------------------------------------------------------------------------------------------------------------------
for element in liste_chansons:
        l = element["lyrics"]
        #print(len(tokenizer.tokenize(l)))
        try:
            doc = nlp(l)
            compteur += 1
#--------------------------------------------------------------------------------------------------------------------
            entite_nomme = [] #Initialisation de la liste des entite nommé trouvé par spacy
            
            print("-"*70,"\n Texte numero %s"%(compteur))
            print(doc)
            #print("Ce texte contient ", len(l), " mot")
            split_txt = tokenizer.tokenize(l)
            
            print("\n Ce texte contient ", len(split_txt), " mot d'après mon tokenizer")
            

            print("\n","Traitement...","\n")
            for ent in doc.ents:
                #print(ent.text)
                #print(ent, ent.label_)
                if ent.label_ == "LOC":
                    locatif = ent.text
                    entite_nomme.append(locatif)
                    locatif_md_before_pre_T.append(locatif)
            #print("\n Ce texte contient ", longueur_mots_spacy, " mot d'après spacy")
            print("\n Le texte a trouvé {} Entité Nommé locatif, ce sont: ".format(len(entite_nomme)))
            print(set(entite_nomme))
            EN_md.append(entite_nomme)
            print(EN_md)
        except:
            pass


    #print(type(l))
#etiquettage étrange à cause des maj? et il faut comprendre l'étiquettage."""


# In[12]:


"""#affichage des EN trouvé par spacy
import nltk
from nltk.tokenize import word_tokenize
import re
import spacy

#nlp = spacy.load('fr_core_news_sm') #modèle small
#nlp = spacy.load('fr_core_news_md') #modèle medium
nlp = spacy.load('fr_core_news_lg') #modèle large
compteur = 0
tokenizer = nltk.RegexpTokenizer(r"(\w+,\w+|\w+-\w+|\w+\.\w+\.\w+|\w+\S|\w+|\S|\w+\S|\?|\!)") #Pour les mots du texte javai pour le 1er
                                                                                              #600 résultats
                                                                                              # j'ai utiliser tokenizer pour séparer les mots du texte.
        
        
EN_lg = []
locatif_lg_before_pre_T = []
print("#"*50, "\nvoici les musiques sur lequels l'on va travailler")
#--------------------------------------------------------------------------------------------------------------------
for element in liste_chansons:
        l = element["lyrics"]
        #print(len(tokenizer.tokenize(l)))
        try:
            doc = nlp(l)
            compteur += 1
#--------------------------------------------------------------------------------------------------------------------
            entite_nomme = [] #Initialisation de la liste des entite nommé trouvé par spacy
            
            print("-"*70,"\n Texte numero %s"%(compteur))
            print(doc)
            #print("Ce texte contient ", len(l), " mot")
            split_txt = tokenizer.tokenize(l)
            
            print("\n Ce texte contient ", len(split_txt), " mot d'après mon tokenizer")
            

            print("\n","Traitement...","\n")
            for ent in doc.ents:
                #print(ent.text)
                #print(ent, ent.label_)
                if ent.label_ == "LOC":
                    locatif = ent.text
                    entite_nomme.append(locatif)
                    locatif_lg_before_pre_T.append(locatif)
            #print("\n Ce texte contient ", longueur_mots_spacy, " mot d'après spacy")
            print("\n Le texte a trouvé {} Entité Nommé locatif, ce sont: ".format(len(entite_nomme)))
            print(set(entite_nomme))
            EN_lg.append(entite_nomme)
            print(EN_lg)
        except:
            pass

with open("EN_lg.txt", "w", encoding="utf-8") as w:
    w.write(str(EN_lg)) 
    #print(type(l))
#etiquettage étrange à cause des maj? et il faut comprendre l'étiquettage."""


# In[6]:


print(chanteur)


# In[5]:


import matplotlib.pyplot as plt
import numpy as np
from matplotlib_venn import venn3

#chanteur = "Jacques Dutronc"

set1 = set(locatif_sm_before_pre_T)
set2 = set(locatif_md_before_pre_T)
set3 = set(locatif_lg_before_pre_T)

venn3([set1, set2, set3], ('small', 'medium', 'large'),set_colors=("green",
                             "red", "blue"))


plt.savefig("Data/Diagramme sur les EN avant pré-traitement de {}.png".format(chanteur))
plt.show()


# In[14]:


lieux_intersection = []
lieux_intersection2 = []
lieux_intersection3 = []
#lieux_en_commun = []
for lieux in locatif_small_before_pre_T:
    if lieux in locatif_md_before_pre_T:
        if lieux in locatif_lg_before_pre_T:
            lieux_intersection.append(lieux)
for lieux2 in locatif_md_before_pre_T:
    if lieux2 in locatif_small_before_pre_T:
        if lieux2 in locatif_lg_before_pre_T:
            lieux_intersection2.append(lieux2)
for lieux3 in locatif_lg_before_pre_T:
    if lieux3 in locatif_small_before_pre_T:
        if lieux3 in locatif_md_before_pre_T:
            lieux_intersection3.append(lieux2)
#print(lieux_intersection3)
#print(lieux_intersection2)
#print(lieux_intersection)
lieux_en_com = set(lieux_intersection).intersection(lieux_intersection2)
lieux_en_com = list(lieux_en_com)
#lieux_en_commun = set(lieux_intersection3).intersection(lieux_en_com)
#print(len(lieux_en_com))
print(lieux_en_com)
print(locatif_lg_before_pre_T)


# In[ ]:


ll = []
ll2 = []
for lieux2 in locatif_md_before_pre_T:
    if lieux2 not in locatif_lg_before_pre_T:
        #if lieux2 not in locatif_small_before_pre_T:
            ll.append(lieux2)
for lieux in locatif_lg_before_pre_T:
    if lieux in locatif_md_before_pre_T:
        #if lieux not in locatif_md_before_pre_T:
            ll2.append(lieux)
            
print(ll)
print("-"*60)
print(ll2)


# # Calcul des Proportions des EN de spacy

# In[6]:


#récuperer les fichiers json
import os
import glob
import json
path = "proportion"

liste_fichiers = glob.glob("%s/*.json"%path)
#print(len(liste_fichiers))
#print(liste_fichiers)


# In[14]:


#nlp = spacy.load('fr_core_news_sm') #modèle small
#nlp = spacy.load('fr_core_news_md') #modèle medium
nlp = spacy.load('fr_core_news_lg') #modèle large

modele = ["small", "medium", "large"]
modele_actif = 2


# In[8]:


print(chanteur)
nbre_txt  = 0
for nom_artiste, liste_chansons in tqdm.tqdm(corpus.items()):
    if nom_artiste == chanteur:
        for element in liste_chansons:
            try:
                l = element["lyrics"]
                nbre_txt += 1
            except:
                nbre_txt += 1
print(nbre_txt)


# In[9]:


#calcul de la proportion des EN de spacy
import nltk
from nltk.tokenize import word_tokenize
import re
import operator



compteur = 1
tokenizer = nltk.RegexpTokenizer(r"(\w+,\w+|\w+-\w+|\w+\.\w+\.\w+|\w+\S|\w+|\S|\w+\S|\?|\!)")
proportion_EN_locatif_spacy = {}
Proportion = []



if os.path.exists("proportion/proportion Entite nomme locatif spacy_{} {}.json".format(modele[modele_actif], chanteur)):
    with open("proportion/proportion Entite nomme locatif spacy_{} {}.json".format(modele[modele_actif], chanteur), encoding='UTF-8') as f:
        a = json.load(f)
        #print(a)
        for c, v in a.items():
            Proportion.append(v)
            #Proportion.append(i[1]) #reprend uniquement mon premier fichier json
else:
    for nom_artiste, liste_chansons in tqdm.tqdm(corpus.items()):
        if nom_artiste == chanteur:
            for element in liste_chansons:
                l = element["lyrics"]
                titre = element["full_title"]
                #print(l)
                try:    
                    doc = nlp(l)
                    entite_nomme = []
                    split_txt = Splittxt3(l) 
                    for ent in doc.ents:
                        if ent.label_ == "LOC":
                            locatif = ent.text
                        #print(ent.text, ent.label_)
                            entite_nomme.append(locatif)
                        proportion = len(entite_nomme)/len(split_txt)
                        proportion_EN_locatif_spacy[titre] = proportion
                    Proportion.append(proportion*100)
                    print("La proportion des EN sur la taille du texte {} est de".format(compteur), proportion*100, "%")
                    compteur += 1

                except:
                    #print(l)
                    Proportion.append(0)
                    proportion_EN_locatif_spacy[titre] = 0
                    print("La proportion des EN sur la taille du texte {} est de 0%".format(compteur))
                    compteur += 1

print(proportion_EN_locatif_spacy)
with open("proportion/proportion Entite nomme locatif spacy_{} {}.json".format(modele[modele_actif], chanteur), "w") as w:
    w.write(json.dumps(proportion_EN_locatif_spacy, indent=2))
"""print(len(Proportion))
count = 0
#print(liste_chansons)
#1/0
for nom_artiste, liste_chansons in tqdm.tqdm(corpus.items()):
    for element in liste_chansons:
        #print(element)
        titre = element["full_title"]
        essaie = [stat for stat in Proportion if stat not in proportion_EN_locatif_spacy]
        proportion_EN_locatif_spacy[titre] = essaie[count]
        #print(proportion_EN_locatif_spacy)
        count += 1
print(proportion_EN_locatif_spacy)
with open("proportion/proportion Entite nomme locatif spacy_{} {}.json".format(modele[modele_actif], chanteur), "w") as w:
    w.write(json.dumps(proportion_EN_locatif_spacy, indent=2))
print(proportion_EN_locatif_spacy)"""


# In[14]:


#calcul de la proportion des EN de spacy
import nltk
from nltk.tokenize import word_tokenize
import re
import operator

compteur = 1
tokenizer = nltk.RegexpTokenizer(r"(\w+,\w+|\w+-\w+|\w+\.\w+\.\w+|\w+\S|\w+|\S|\w+\S|\?|\!)")
proportion_EN_spacy = {}
Proportion4 = []


if os.path.exists("proportion/proportion Entite nomme spacy_{} {}.json".format(modele[modele_actif], chanteur)):
    with open("proportion/proportion Entite nomme spacy_{} {}.json".format(modele[modele_actif], chanteur), encoding='UTF-8') as f:
        a = json.load(f)
        #print(a)
        for c, v in a.items():
            Proportion4.append(v)
else:
    for nom_artiste, liste_chansons in tqdm.tqdm(corpus.items()):
        if nom_artiste == chanteur:
            for element in liste_chansons:
                l = element["lyrics"]
                titre = element["full_title"]
                try:

                    doc = nlp(l)
                    entite_nomme = []
                    split_txt = Splittxt3(l) 
                    for ent in doc.ents:

                        en = ent.text
                        #print(ent.text, ent.label_)
                        entite_nomme.append(en)
                    proportion = len(entite_nomme)/len(split_txt)
                    proportion_EN_spacy[titre] = proportion
                    Proportion4.append(proportion*100)
                    print("La proportion des EN sur la taille du texte {} est de".format(compteur), proportion*100, "%")
                    compteur += 1


                except:
                    #print(l)
                    proportion_EN_spacy[titre] = 0
                    Proportion4.append(0)
                    print("La proportion des EN sur la taille du texte {} est de 0%".format(compteur))
                    compteur += 1
with open("proportion/proportion Entite nomme spacy_{} {}.json".format(modele[modele_actif], chanteur), "w") as w:
    w.write(json.dumps(proportion_EN_spacy, indent=2))
    
"""count = 0
for element in liste_chansons:
    titre = element["full_title"]
    essaie = [stat for stat in Proportion4 if stat not in proportion_EN_spacy]
    #print(essaie)
    proportion_EN_spacy[titre] = essaie[count]
    count += 1
with open("proportion/proportion Entite nomme spacy_{} {}.json".format(modele[modele_actif], chanteur), "w") as w:
    w.write(json.dumps(proportion_EN_spacy, indent=2))
"""


# In[15]:


print(json.dumps(proportion_EN_spacy, indent=2))


# In[ ]:





# # Calcul des proportions des EN qui ont match avec les fichiers des lieux de paris

# In[ ]:





# In[16]:


#Calcul de la proportion des EN qui ont matché avec la liste des lieux de paris
    #pour chaque txt si une entite nommé correspond a une vrai entite nommé alors
    #on ajoute le texte dans un dictionnaire et on ajoute l'entite nommé en valeur
import nltk
from nltk.tokenize import word_tokenize
import re
compteur = 0
tokenizer = nltk.RegexpTokenizer(r"(\w+,\w+|\w+-\w+|\w+\.\w+\.\w+|\w+\S|\w+|\S|\w+\S|\?|\!)")
proportion_EN_matché = {}
Proportion2 = []
en_Match = {}

liste_titre = []
if os.path.exists("proportion/proportion Entite matché_{} {}.json".format(modele[modele_actif], chanteur)):
    with open("proportion/proportion Entite matché_{} {}.json".format(modele[modele_actif], chanteur), encoding='UTF-8') as f:
        a = json.load(f)
        for i, c in a.items():
            Proportion2.append(c[1])
            en_Match[i]= [c[0], c[1], c[2]] #reprend uniquement mon premier fichier json
            
else:
    for nom_artiste, liste_chansons in tqdm.tqdm(corpus.items()):
        if nom_artiste == chanteur:
            for element in liste_chansons:

                txt = element["lyrics"]
                #print(element.keys())
                titre = element["full_title"]

                try:
                    artiste = element["album"]["artist"]["name"]
                except:
                    pass
                date = element["release_date"]
                en_Match.setdefault(titre,[])    
                if 2>1 :
                    try:
                        doc = nlp(txt)
                        liste_temporaire = []
                        freq = []
                        split_txt = Splittxt3(txt)
                        for ent in doc.ents:
                            liste_temporaire.append(ent.text)
                            #print(liste_temporaire)
                        match =  [i for i in liste_temporaire if i in vrai_entite_nomme]#Pour chaque match on calcul la proportion par texte.
                        proportion = (len(match)/len(split_txt))*100
                        print(proportion, "\n")
                        if match :
                            freq.append(match)   
                            en_Match[titre]= [match, proportion, len(freq)]
                        else:
                            en_Match[titre] = ["no match", 0, "none"]

                        Proportion2.append(proportion)

                    except:
                        Proportion2.append(0)
                        print("0\n")
                        en_Match[titre] = ["no match", 0, "none"]


with open("proportion/proportion Entite matché_{} {}.json".format(modele[modele_actif], chanteur), "w") as w:
    w.write(json.dumps(en_Match, indent=2))       
            
            
print(len(Proportion2))
#print(Proportion2)
#print(en_Match)
#print(proportion_EN_matché)


# In[26]:


print(json.dumps(en_Match, indent=2))


# # Proportion des lettres capitale dans les textes

# In[17]:



import nltk
from nltk.tokenize import word_tokenize
import re

compteur = 0
proportion_maj = {}
Proportion3 = []
tokenizer = nltk.RegexpTokenizer(r"(\w+,\w+|\w+-\w+|\w+\.\w+\.\w+|\w+\S|\w+|\S|\w+\S|\?|\!)")

if os.path.exists("proportion des majuscules {}.json".format(chanteur)):
    with open(path_json) as f:
        cle, valeur = json.load(f)
        Proportion3.append(valeur)
else:
     for nom_artiste, liste_chansons in tqdm.tqdm(corpus.items()):
        if nom_artiste == chanteur:
            for element in liste_chansons:
                i = element["lyrics"]
                if 2 > 1:
                    if i != None:                    
                        majuscule = []
                        txt_split = Splittxt3(i)
                        #print(txt_split)
                        for eleme in txt_split:
                            if eleme.istitle() == True:
                                majuscule.append(eleme)
                                proportion = (len(majuscule)/len(txt_split))*100
                                proportion_maj[titre] = proportion
                        Proportion3.append(proportion)
                        compteur += 1
                        print("La proportion des mots en majuscule sur le texte n°{} est de {}".format(compteur, proportion),"%")
                        print("Il y a %s Mot qui on une maj sur %s mot \n"%(len(majuscule), len(txt_split)))

                        #print(majuscule)


                    else:
                        #print(i)
                        proportion_maj[titre] = proportion
                        Proportion3.append(0)
                        compteur += 1
                        print("La proportion des mots en majuscule sur le texte n°{} est de 0% \n".format(compteur))

with open("proportion/proportion des majuscules {}.json".format(chanteur), "w") as w:
    w.write(json.dumps(proportion_maj, indent=2))


"""count = 0
for element in liste_chansons:
    titre = element["full_title"]
    essaie = [stat for stat in Proportion3 if stat not in proportion_maj]
    #print(essaie)
    proportion_maj[titre] = essaie[count]
    count += 1"""


# In[28]:


print(json.dumps(proportion_maj, indent=2))


# # initialisation d'un dic pr overleaf

# In[28]:



dictionnaire_tableau = {}
compteuur = 0

valeur1 = [v for v in Proportion]
valeur2 = [v for v in Proportion4]
valeur3 = [v for v in Proportion2]
valeur4 = [v for v in Proportion3]
print(valeur1[compteuur])
for nom_artiste, liste_chansons in tqdm.tqdm(corpus.items()):
    if nom_artiste == chanteur:
        for element in liste_chansons:
            titre = element["full_title"]
            dictionnaire_tableau[titre] = [valeur1[compteuur], valeur2[compteuur], valeur3[compteuur], valeur4[compteuur]]
            compteuur += 1

print(dictionnaire_tableau)


# # affichage pr overleaf
# 

# In[30]:



nom_colone = ["Titre chanson", "Prop locatif","Prop EN", "Prop match", "Prop Maj"]
print("\\begin{table}")
print("\\centering")
print("\t\\begin{tabular}{|l|l|l|l|l|}")
print("\t\\hline")
print(" \t %s \\\\" %(" & ".join(nom_colone)))
print("\t\\hline")
#ne pas trier les valeurs tant que toutes les valeurs ne sont pas inscrite.
#ou une boucle qui récupère pour chaque titre leurs valeurs.
for titre, proportion in sorted(dictionnaire_tableau.items(), key=lambda x: x[1], reverse=True):
    ligne = "\t %s... \t& %s \t& %s \t& %s \t& %s \\\\\n\t\\hline  " %(str(titre[:20]), round(proportion[0], 4), round(proportion[1], 4), round(proportion[2], 4), round(proportion[3], 4))
    print(ligne)
print("\t\end{tabular}")
print("\end{table}")


# # code pour regrouper les lieux de paris.

# In[31]:



liste_inclassable = []
for lieux in vrai_entite_nomme:
    liste_inclassable.append(lieux)
    dic_lieu["unclassable"] = set(liste_inclassable)
    #print(dic_lieu)
dic_lieu = {"inclassable":set(vrai_entite_nomme)}
def regroupement_lieu_paris(expression_reguliere, cle, dic_lieu):
    liste_classable = []
    for lieux in vrai_entite_nomme:
        match = re.search(expression_reguliere, lieux)#re.I ?
        if not match:
            pass    
        else:
            liste_classable.append(lieux)
    dic_lieu[cle] = set(liste_classable)
    return dic_lieu
for expr, cle in [
    [r'^(Chateau|chateau|château|Château)', "Chateau"],
    [r'^(Porte|porte)', "Porte"],
    [r'^(Eglise|eglise|Église|église)',"Eglise"],
    [r'^(Place|place)', "Place"],
    [r'^(Avenue|avenue)',"Avenue"],
    #[r'Michel', "Michel"],
    [r'^(Boulevard|boulevard)', "Boulevard"],
    [r'^(Rue|rue)', "Rue"],
    [r'^(Cite|cite|Cité|cité)', "Cite"],
    [r'Paris ([0][1-9]|[1][0]|[1][1-9]|20|arrondissement)$', "Arrondissement"],
    [r'^(Saint|saint|st|St)',  "Saint"],
    [r'^(Pont|pont|ponts|Ponts)', "Pont"]]:
    dic_lieu = regroupement_lieu_paris(expr, cle, dic_lieu)
    dic_lieu["inclassable"] = dic_lieu["inclassable"].difference(dic_lieu[cle])
   


#print("")
taille_voc = len(set(vrai_entite_nomme))
print(taille_voc)
#print(dic_lieu)
dic_lieu_to_overleaf = {}
for cle, liste in dic_lieu.items():
    dic_lieu_to_overleaf[cle] = len(dic_lieu[cle])
    #print(cle, len(dic_lieu[cle]))
#print("-"*60)
#print(dic_lieu_to_overleaf)
for cle, liste in sorted(dic_lieu_to_overleaf.items(), key=lambda x: x[1], reverse=True):
    #print(len(dic_lieu[cle]))
    print(cle,"|", len(dic_lieu[cle]), "|",  len(dic_lieu[cle])/taille_voc)
#print(dic_lieu["Arrondissement"])



# # Code pour construction tableau overleaf

# In[32]:



nom_tableau = ["Lieu", "taille", "proportion"]
print("\t\\begin{tabular}{|l|l|l|}")
print("\t\\hline")
print(" \t %s \\\\" %(" & ".join(nom_tableau)))
print("\t\\hline")

for cle, valeur in sorted(dic_lieu_to_overleaf.items(), key=lambda x: x[1], reverse=True):
    ligne = "\t %s \t& %s \t& %s \\\\\n\t\\hline  "%(cle, len(dic_lieu[cle]),len(dic_lieu[cle])/taille_voc)
    print(ligne)
print("\t\end{tabular}")
print("\end{table}") 


# # pré-traitement adaptation casse
# Si le mot au début de la ligne est en majuscule, on le met en minuscule s'il valide les deux conditions suivantes :
# 
# - Il "existe en minuscule dans le Glaff"
# 
# - Il "n'es pas pas dans la ressource de noms de lieux"
# 
# Par exemple, si j'ai :
# 
# Il est maxi Docteur Schweitzer Il- --> il
# 
# Maximum et maxibus Maximum --> maximum
# 
# Maxistère et termaxus --> maxistère
# 
# par contre dans
# 
# "Paris et province" --> Paris ne bouge pas car s'il existe en minuscule dans le Glaff il est présent dans la ressource
# 
# La véritable "recréation" de phrases ce sera une étape pour plus tard, car ça va être assez compliqué !

# In[33]:


"""import re

path = "GLAFF/glaff-1.2.2.txt"
f = open(path, encoding='UTF-8')

ligne = f.readline()
cpt=0
dic_glaff = {}
while len(ligne)>1:
    cpt+=1
    elems = re.split("\|", re.sub("\n", "", ligne))
    freq = 0
    forme = elems[0]
    for index in range(6, len(elems)+1, 2):
        freq+=float(elems[index])
    dic_glaff[forme] = freq
    ligne = f.readline()
    cpt = 10000"""
#w = open("freq_glaff_%i.json"%cpt, "w")
#w.write(json.dumps(dic_glaff, indent=2))
#w.close()


# In[157]:


import json
#voc_glaff = []
with open("freq_glaff_10000.json") as f:
    dic = json.load(f)
    print(len(dic))
    voc_glaff = set(dic.keys()) 
    print(len(voc_glaff))

mot = "météoriser"
if mot in voc_glaff:
    print(mot)


# In[155]:


import json
import tqdm
corpus = ouvrir_json("tmp.json")
chanteur = []
cpt = 0

#with open("all_entites.json", encoding="utf-8") as f:
    #all_entites = json.load(f)
for nom_artiste, liste_chansons in tqdm.tqdm(corpus.items()):
    chanteur.append(nom_artiste)
    for element in liste_chansons:
        #txt = element["lyrics"]
        try:
            txt = element["lyrics"]
            #txt = str(txt)
        except:
            continue
        titre = element["full_title"]



# In[ ]:



  
  #print(nom_artiste)
  
    
   
    titre = element["full_title"]
    all_entites.setdefault(nom_artiste, {})
    all_entites[nom_artiste].setdefault(titre, {})
    if cpt%100==0:
        print(cpt, "chansons faites")
    if len(all_entites[nom_artiste][titre])==3:
        cpt+=1
        continue
    for nom_modele, nlp in liste_models:
        if nom_modele not in  all_entites[nom_artiste][titre]:
            doc = nlp(txt)
            entites = [ent.text for ent in doc.ents if ent.label_=="LOC"]
            all_entites[nom_artiste][titre][nom_modele]= entites
    cpt+=1
    #liste_txt.append(txt)
    #tous_les_txt.append(liste_txt)
    if cpt%100==0:
        break
  if cpt%100==0:
        break
    
    #print(titre)
    #print(liste_txt, "-"*70)print(len(tous_les_txt))
print(cpt, "chansons faites")
#chanteur = "Jacques Dutronc"
#with open("all_entites.json", "w", encoding="utf-8") as w:
    #w.write(json.dumps(all_entites, indent=2, ensure_ascii=False))
#print(json.dumps(all_entites, indent =2))


# In[158]:


import nltk
chanson = []
for nom_artiste, donnee in tqdm.tqdm(corpus.items()):
    #if nom_artiste == chanteur:
    if 2>1:
        for element in donnee:
            liste = []
            txt = element["lyrics"]
            try:
                for l in txt.split("\n"):
                    #lignes_chanson.append(l)
                    liste.append(l)
                chanson.append(liste) #lignes_chanson.append([l])
            except:
                chanson.append([])
        
FP = 0 # On a modifié et on a eu tord
VP = 0 # On a modifié et on a eu raison
FN = 0 # On a pas modifié et on a eu tord
VN = 0 # On a pas modifié et on a eu raison.

#print(chanson)
count = -1
for liste_lignes_chanson in tqdm.tqdm(chanson):
    count += 1
    for ligne in liste_lignes_chanson:
        expr = re.compile("^(\w+'|\w+-\w+|\w+)")
        match = expr.finditer(ligne)
        
        #print(ligne)
        #ici je créer une expression pour récuperer tous les mots en début de ligne, 
        #certain commençant par "j'" ou "c'" d'autre par un tiret "un-mot", je ne sais pas s'il y a
        #d'autre mot différent.
    #------------------------------------------------------------------------------------------------------------ 
        for m in match:
            mot = m.group(0) #la variable mot prend la chaine de caractère trouvé par mon match.
            #print(""" "{}"  dans : "{}" """.format(mot, z)) #affiche le mot dans quel ligne il se trouve.
            toto = False
            if mot[0] != mot[0].lower():
                toto = True
            #if mot.istitle(): #si le mot possède une majuscule je le met sans maj. minimoke not istitle()
            if toto == True:
                mot_lower = mot.lower()
                #print(mot)
    #------------------------------------------------------------------------------------------------------------
                if mot_lower in voc_glaff:                 #s'il est dans le glaff et qu'il correspond 
                    #print("le mot est dans glaff")   #a un lieu de ma liste des lieux
                    if mot in vrai_entite_nomme:     #SINON je l'affiche .
                        print("le mot est un nugget\n ")
                        FP += 1
                    else:
                        
                        #print("je suis pas un nugget\n ")
                        liste_mots = Splittxt3(ligne)#permet de découper ma ligne en liste de mot.
                        #print(liste_mots)
                        #1/0
                        #print(liste_mots)
                        liste_mots[0] = mot_lower            #le mot en début de ligne je le remplace par mot.
                        nouvelle_ligne = " ".join(liste_mots)  #je reassemble ma ligne.
                        for apo in ["’", "'"]:
                          nouvelle_ligne = re.sub(f"{apo} ", f"{apo}", nouvelle_ligne)
                          nouvelle_ligne = re.sub(f" {apo}", f"{apo}", nouvelle_ligne)
                        #nouvelle_ligne = re.sub("\'\s", "\'", nouvelle_ligne)
                        #print(lignes_chanson, "\n")
                        res = [elem.replace(ligne,nouvelle_ligne) for elem in liste_lignes_chanson]  #je remplace 
                        VP += 1
                        liste_lignes_chanson = res   #l'ancienne ligne par une nouvelle ligne.  #VP 
                        chanson[count] = liste_lignes_chanson
                    

                        
    #------------------------------------------------------------------------------------------------------------

                elif mot_lower not in voc_glaff:#s'il est pas dans le glaff je fait le même procédé ↑.

                    #print("le mot est pas dans glaff \n ")#ne pas mettre en minuscule. #FN
                    #match = [i for i in vrai_entite_nomme]
                    if mot not in vrai_entite_nomme:
                        #print("pas dans lieu de paris")
                        FN += 1
                    else:
                        #print("je suis un lieu de paris \n ")
                        VN += 1

#print(chanson)
#print(count)
#print(len(chanson))
#Problème au niveau du .join les mots comme l'index sont écrit de cet manière l' index.


# In[31]:


print(chanson)


# In[184]:


comptage = 0

num_chanson = []

for i in tqdm.tqdm(chanson):
    m = []
    nv_echantillon = " \n ".join(i)
    m.append(nv_echantillon)
    #print(m)
    #num_chanson.append(nv_echantillon)
    num_chanson.append(m)
    #print(num_chanson[comptage])
        
    #print(num_chanson[comptage], "\n")
        
        
#print(num_chanson[0])    
Dic_nouvelle_chansons = {}
#Dic_nouvelle_chansons.setdefault(nom_artiste,[])
#Dic_nouvelle_chansons[nom_artiste] = []
#print(Dic_nouvelle_chansons)
#Dic_nouvelle_chansons["all"].setdefault(,[])


for nom_artiste, donnee in tqdm.tqdm(corpus.items()):
    Dic_nouvelle_chansons.setdefault(nom_artiste,[])
    #if nom_artiste == chanteur:
    if 2>1:
        for element in donnee:
            #Dic_nouvelle_chansons.setdefault()
            titre = element["full_title"]
            try:
                artiste = element["album"]["artist"]["name"]
            except:
                artiste = "none"
            try:
                date = element["release_date"]
            except:
                date = "None"
            #if titre not in Dic_nouvelle_chansons:
            if 2>1:
                dic_tempo = {"Titre_chanson":titre, "Auteur":artiste, "lyrics":num_chanson[comptage], "Date":date}
                Dic_nouvelle_chansons[nom_artiste].append(dic_tempo)
                #print(Dic_nouvelle_chansons)
                ###Dic_nouvelle_chansons["all"]["Auteur"] = artiste
                #Dic_nouvelle_chansons["all"]["lyrics"] = num_chanson[comptage]
                comptage += 1
        #print(Dic_nouvelle_chansons)
    #print(nom_artiste)
    #print(Dic_nouvelle_chansons)
with open("Data/parole pre traiter/nouvel_echantillon.json", "w") as w:
    w.write(json.dumps(Dic_nouvelle_chansons, indent=2))


#for toto in Dic_nouvelle_chansons["all"][:5]:
    #print(json.dumps(toto, indent=2))#


# In[181]:


#print(Dic_nouvelle_chansons)


# # Matrice de confusion

# In[186]:


print("FP = ",FP)
print("VP = ",VP)
print("FN = ",FN)
print("VN = ",VN)
confusion_matrice = FP, VP, FN, VN


# In[4]:


FP =  0
VP =  1262
FN =  307
VN =  2


# In[5]:


accuracy = VP/(VP + FP)
rappel = VP / (VP + FN)
f_mesure = (2*(accuracy*rappel))/(accuracy+rappel)
print("accuracy = ",accuracy)
print("rappel = ",rappel)
print("f_mesure = ",f_mesure)


# In[189]:


import seaborn as sn
import pandas as pd
import matplotlib.pyplot as plt
array = [[VP,FP],
        [VN, FN]]
fig, ax = plt.subplots(figsize=(5,5))
df_cm = pd.DataFrame(array, index=["VRAI", "FAUX"], columns=["POSITIF","NEGATIF"])
# plt.figure(figsize=(10,7))

#sn.set(font_scale=1) # for label size
sn.heatmap(df_cm, annot=True, cmap = plt.cm.Reds, fmt ="d") # font size
plt.savefig("Data/Matrice_confusion_{}.png".format("all_artiste"))
plt.show()


# In[ ]:





# # Récuperer mon nouveau fichier json et detecter les EN dessus.
# for i in chanson:
#     #print(i)
#     nv_echantillon = "\n".join(i)
#     #print(nv_echantillon)
#     doc = nlp(nv_echantillon)
#     for ent in doc.ents:
#         if ent.label_ == "LOC":
#             locatif = ent.text
#             print(locatif)
#             if locatif in vrai_entite_nomme:
#                 print("#"*79, "\n", locatif,"\n","#"*79)

# In[78]:


#chanteur = "_113"


# In[11]:


path_to_Spacy = "Data/parole pre traiter/nouvel_echantillon.json"

corpus2 = ouvrir_json(path_to_Spacy)
#print(i)


# In[ ]:


#statt sur le corpus


# In[12]:


import tqdm
import json
nom_artiste = " "
corpus2 = ouvrir_json(path_to_Spacy)
artiste = []
toutes_les_chansons = []
tous_les_mots = []
nbre_de_texte_traitable = 0
nbre_de_texte_non_traitable = 0
nbre_de_mot_totale = 0
nbre_de_mot_par_chanson = []
dic_nbre_de_mot = {}
dic_nbre_de_mot = {nom_artiste:{}, titre:{}}

for nom_artiste, donnee in tqdm.tqdm(corpus.items()):
    for element in donnee:
        chansons = []
        titre = element["full_title"]
        try:
            #txt = str(parole)
            parole = element["lyrics"]
            mots = Splittxt3(parole)
            chansons.append(mots)
            dic_nbre_de_mot[titre].setdefault(len(mots), 0)
            dic_nbre_de_mot[titre][len(mots)]+=1 
            dic_nbre_de_mot[nom_artiste].setdefault(len(chansons), 0)
            dic_nbre_de_mot[nom_artiste][len(chansons)]+=1
            #chansons.append(parole)
            #toutes_les_chansons.append(chansons)
            #nbre_de_texte_traitable += 1
            #print(dic_nbre_de_mot)
            #1/0
        except:
            pass
            #mots = None
            #chansons.append(mots)
            #dic_nbre_de_mot[titre].setdefault(mots, 0)
            #dic_nbre_de_mot[titre][0]+=1 
            #dic_nbre_de_mot[nom_artiste].setdefault(len(chansons), 0)
            #dic_nbre_de_mot[nom_artiste][len(chansons)]+=1
            #chansons.append(None)
            #toutes_les_chansons.append(chansons)
            #nbre_de_texte_non_traitable += 1
            #print(dic_nbre_de_mot)
            #1/0
        
        #print(dic_nbre_de_mot)
        #1/0
        

print(dic_nbre_de_mot)   
        
        
        
        
        
        
        
"""
for liste_chansons in tqdm.tqdm(toutes_les_chansons):
    for chanson in liste_chansons:
        try:
            mots = Splittxt3(chanson)
            tous_les_mots.append(mots)
        except:
            tous_les_mots.append([])
        if chanson != None:
            nbre_de_texte_traitable += 1
        else:
            nbre_de_texte_non_traitable += 1
    #artiste.append(chanteur)
print(nbre_de_texte_non_traitable)
print(nbre_de_texte_traitable)
#print(tous_les_mots)
for liste_mots in tqdm.tqdm(tous_les_mots):
    nbre_de_mot_par_chanson.append(len(liste_mots))
    nbre_de_mot_par_chanson.append(0)
    for mot in liste_mots:
        nbre_de_mot_totale += 1
#print(nbre_de_mot_par_chanson)
#print(nbre_de_mot_totale)"""


# In[ ]:





# In[80]:


#pour afficher paroles des chansons du fichier echantillon1.json
import tqdm
import json
corpus2 = ouvrir_json(path_to_Spacy)
cpt = 0
#start = i["_113"]
all_entites2 = {}
#print(start)
#1/0
#une liste vide pour regrouper tous les listes de txt (chaque txt et dans une liste)
tous_les_txt = []
#corpus = {"_113":corpus["_113"]}
dic_name = {}

if os.path.exists("all_entites2.json"):
    with open("all_entites2.json", encoding="utf-8") as f:
        all_entites2 = json.load(f)
else:

    for nom_artiste, liste_chansons in tqdm.tqdm(corpus2.items()):
      for element in liste_chansons:
        liste_txt = []
        txt = element["lyrics"]
        try:
            txt = str(txt)
        except:
            continue
        titre = element["Titre_chanson"]
        all_entites2.setdefault(nom_artiste, {})
        all_entites2[nom_artiste].setdefault(titre, {})
        if cpt%100==0:
            print(cpt, "chansons faites")
        if len(all_entites2[nom_artiste][titre])==3:
            cpt+=1
            continue
        for nom_modele, nlp in liste_models:
            if nom_modele not in all_entites2[nom_artiste][titre]:
                doc = nlp(txt)
                entites = [ent.text for ent in doc.ents if ent.label_=="LOC"]
                all_entites2[nom_artiste][titre][nom_modele]= entites
        cpt+=1
        #liste_txt.append(txt)
        #tous_les_txt.append(liste_txt)
        #if cpt%1000==0:
            #break
      #if cpt%1000==0:
            #break

        #print(titre)
        #print(liste_txt, "-"*70)print(len(tous_les_txt))
    print(cpt, "chansons faites")
    #chanteur = "Jacques Dutronc"
with open("all_entites2.json", "w", encoding="utf-8") as w:
    w.write(json.dumps(all_entites2, indent=2, ensure_ascii=False))
#print(json.dumps(all_entites, indent =2))


# In[ ]:


"""
nlp = spacy.load('fr_core_news_sm') #modèle small
#nlp = spacy.load('fr_core_news_md') #modèle medium
#nlp = spacy.load('fr_core_news_lg') #modèle large
   
locatif_sm = []
EN = []
compteur = 0
tokenizer = nltk.RegexpTokenizer(r"(\w+,\w+|\w+-\w+|\w+\.\w+\.\w+|\w+\S|\w+|\S|\w+\S|\?|\!)") #Pour les mots du texte javai pour le 1er
                                                                                              #600 résultats
                                                                                              # j'ai utiliser tokenizer pour séparer les mots du texte.
        
print("#"*50, "\nvoici les musiques sur lequels l'on va travailler \n")
for lk in debut:
    new_parole = lk["lyrics"]
    new_artiste = lk["Auteur"]
    new_titre = lk["Titre_chanson"]
    for parole in new_parole:
        try:
            doc = nlp(parole)
            compteur += 1
    #--------------------------------------------------------------------------------------------------------------------
            entite_nomme = [] #Initialisation de la liste des entite nommé trouvé par spacy

            print("-"*70,"\n Texte n°%s \n"%(compteur))
            print(doc)
            #print("Ce texte contient ", len(l), " mot")
            print("\n","Traitement...","\n")
            for ent in doc.ents:
                #print(ent.text)

                if ent.label_ == "LOC":
                    locatif = ent.text
                    entite_nomme.append(locatif)
                    locatif_sm.append(locatif)
            #print("\n Ce texte contient ", longueur_mots_spacy, " mot d'après spacy")
            print("\n Le texte a trouvé {} Entité Nommé locatif, ce sont: ".format(len(entite_nomme)))
            print(set(entite_nomme))
            EN.append(entite_nomme)
            print(EN)
        except:
            pass"""


# In[ ]:


"""
#nlp = spacy.load('fr_core_news_sm') #modèle small
nlp = spacy.load('fr_core_news_md') #modèle medium
#nlp = spacy.load('fr_core_news_lg') #modèle large
  
locatif_md = []
EN = []
compteur = 0
tokenizer = nltk.RegexpTokenizer(r"(\w+,\w+|\w+-\w+|\w+\.\w+\.\w+|\w+\S|\w+|\S|\w+\S|\?|\!)") #Pour les mots du texte javai pour le 1er
                                                                                              #600 résultats
                                                                                              # j'ai utiliser tokenizer pour séparer les mots du texte.
        
print("#"*50, "\nvoici les musiques sur lequels l'on va travailler \n")
for lk in debut:
    new_parole = lk["lyrics"]
    new_artiste = lk["Auteur"]
    new_titre = lk["Titre_chanson"]
    for parole in new_parole:
        try:
            doc = nlp(parole)
            compteur += 1
    #--------------------------------------------------------------------------------------------------------------------
            entite_nomme = [] #Initialisation de la liste des entite nommé trouvé par spacy

            print("-"*70,"\n Texte n°%s \n"%(compteur))
            print(doc)
            #print("Ce texte contient ", len(l), " mot")
            print("\n","Traitement...","\n")
            for ent in doc.ents:
                #print(ent.text)

                if ent.label_ == "LOC":
                    locatif = ent.text
                    entite_nomme.append(locatif)
                    locatif_md.append(locatif)
            #print("\n Ce texte contient ", longueur_mots_spacy, " mot d'après spacy")
            print("\n Le texte a trouvé {} Entité Nommé locatif, ce sont: ".format(len(entite_nomme)))
            print(set(entite_nomme))
            EN.append(entite_nomme)
            print(EN)
        except:
            pass"""


# In[ ]:


"""
#nlp = spacy.load('fr_core_news_sm') #modèle small
#nlp = spacy.load('fr_core_news_md') #modèle medium
nlp = spacy.load('fr_core_news_lg') #modèle large

locatif_lg = []
EN2 = []
compteur = 0
tokenizer = nltk.RegexpTokenizer(r"(\w+,\w+|\w+-\w+|\w+\.\w+\.\w+|\w+\S|\w+|\S|\w+\S|\?|\!)") #Pour les mots du texte javai pour le 1er
                                                                                              #600 résultats
                                                                                              # j'ai utiliser tokenizer pour séparer les mots du texte.
        
print("#"*50, "\nvoici les musiques sur lequels l'on va travailler \n")
for lk in debut:
    new_parole = lk["lyrics"]
    new_artiste = lk["Auteur"]
    new_titre = lk["Titre_chanson"]
    for parole in new_parole:
        try:
            doc = nlp(parole)
            compteur += 1
    #--------------------------------------------------------------------------------------------------------------------
            entite_nomme = [] #Initialisation de la liste des entite nommé trouvé par spacy

            print("-"*70,"\n Texte n°%s \n"%(compteur))
            print(doc)
            #print("Ce texte contient ", len(l), " mot")
            print("\n","Traitement...","\n")
            for ent in doc.ents:
                #print(ent.text)

                if ent.label_ == "LOC":
                    locatif = ent.text
                    entite_nomme.append(locatif)
                    locatif_lg.append(locatif)
            #print("\n Ce texte contient ", longueur_mots_spacy, " mot d'après spacy")
            print("\n Le texte a trouvé {} Entité Nommé locatif, ce sont: ".format(len(entite_nomme)))
            print(set(entite_nomme))
            EN2.append(entite_nomme)
            print(EN2)
        except:
            pass"""


# # Enregistrer les lieux trouver par spacy pour en faire un diagramme de venn

# In[66]:


locatif_sm = []
locatif_md = []
locatif_lg = []
k = 0 
#chanteur = "Jacques Dutronc"
with open("all_entites2.json", encoding="utf-8") as f:
    all_entites2 = json.load(f)
for nom_artiste, donnee in all_entites2.items():
    if nom_artiste == chanteur:
    #if 2 > 1:
        for titre_musique, modele in donnee.items():
            for modele_3, EN in modele.items():
                if modele_3 == "small":
                    for entities in EN:
                        locatif_sm.append(entities)
                if modele_3 == "medium":
                    for entities in EN:
                        locatif_md.append(entities)
                if modele_3 == "large":
                    for entities in EN:
                        locatif_lg.append(entities)
                    #print(y)
            #if modele.keys() == "small":
                #print("oui")
            


# In[45]:


lieux_intersection = []
lieux_intersection2 = []
lieux_intersection3 = []
#lieux_en_commun = []
for lieux in locatif_sm:
    if lieux in locatif_md:
        if lieux in locatif_lg:
            lieux_intersection.append(lieux)
for lieux2 in locatif_md:
    if lieux2 in locatif_sm:
        if lieux2 in locatif_lg:
            lieux_intersection2.append(lieux2)
for lieux3 in locatif_lg:
    if lieux3 in locatif_sm:
        if lieux3 in locatif_md:
            lieux_intersection3.append(lieux2)
#print(lieux_intersection3)
#print(lieux_intersection2)
#print(lieux_intersection)
lieux_en_com = set(lieux_intersection).intersection(lieux_intersection2)
lieux_en_com = list(lieux_en_com)
#lieux_en_commun = set(lieux_intersection3).intersection(lieux_en_com)
#print(len(lieux_en_com))
#print(lieux_en_com)
print(locatif_sm)


# In[ ]:


ll = []
ll2 = []
for lieux2 in locatif_md:
    if lieux2 not in locatif_lg:
        #if lieux2 not in locatif_small_before_pre_T:
            ll.append(lieux2)
for lieux in locatif_lg:
    if lieux in locatif_md:
        #if lieux not in locatif_md_before_pre_T:
            ll2.append(lieux)
            
print(ll)
print("-"*60)
print(ll2)


# In[61]:


import numpy as np
import matplotlib.pyplot as plt
from matplotlib_venn import venn3


set1 = set(locatif_sm)
set2 = set(locatif_md)
set3 = set(locatif_lg)

venn3([set1, set2, set3], ('small', 'medium', 'large'),set_colors=("green",
                             "red", "blue"))

plt.savefig("Data/%s.png"%"Diagramme sur les EN de {}".format(chanteur))
plt.show()


# In[ ]:





# In[ ]:





# # faire un dictionnaire d'interrogation permettant de faire des analyses dessus.

# In[2]:


#nlp = spacy.load('fr_core_news_sm') #modèle small
#nlp = spacy.load('fr_core_news_md') #modèle medium
#nlp = spacy.load('fr_core_news_lg') #modèle large

modele = ["small", "medium", "large"]
modele_actif = 2


# In[81]:


print(chanteur)


# In[3]:


import os


dic_interro = {}

if os.path.exists("Data/Dictionnaire_artiste_to_lieux_paris_{}.json".format(modele[modele_actif])):
    with open("Data/Dictionnaire_artiste_to_lieux_paris_{}.json".format(modele[modele_actif]), encoding="UTF-8") as f:
        a = json.load(f)
        for i, c in a.items():
            #print(c[0])
            dic_interro[i] = c
else:
    for nom_artiste, liste_chansons in tqdm.tqdm(corpus2.items()):

      #if nom_artiste == chanteur:
          for element in liste_chansons:
            paroles = element["lyrics"]

            #print(element.keys())
            titre = element["Titre_chanson"]
            try:
                artiste = element["Auteur"]
                #print(type(artiste))
            except:
                artiste = "None"
            try:
                date = element["Date"]
            except:
                date = "None"
            dic_interro.setdefault(nom_artiste, [])
            for txt in paroles:
                if 2>1 :
                    try:
                        doc = nlp(txt)
                        liste_temporaire = []
                        for ent in doc.ents:
                                if ent.label_ == "LOC":
                                    locatif = ent.text
                                    liste_temporaire.append(locatif)
                        if locatif in dic_interro:
                            print("deja dans le dictionnaire") #problème le nom de l'artiste existe deja comment l'ajouter au dictionnaire ?
                        else:
                            #print(type(liste_temporaire[0]))
                            dic_interro[nom_artiste].append([titre, date, liste_temporaire])


                    except:
                        pass

#print(dic_interro)
T = dic_interro.values()
for nom_artiste, T in dic_interro.items():
    #print(T)
    nb_nom_paris = len([x for x in T if len(x[2])==0])
    nb_total_chanson = len(T)
    print(nom_artiste, nb_nom_paris,"nom de lieu cité ")
    print("sur ", nb_total_chanson, "nombre totale de chanson")
    
with open("Data/Dictionnaire_artiste_to_lieux_paris_{}.json".format(modele[modele_actif]), "w") as w:
    w.write(json.dumps(dic_interro, indent=2))


# # Créer un graph des artistes parlant du + "x".
# x = un lieu de paris. 
# somme globale. = pour un lieu qui est l'auteur qui a le plus parlé?

# In[204]:


#print(dic_interro)


# In[4]:


#somme globale. = pour un lieu qui est l'auteur qui a le plus parlé?
    #print()
dico_des_artistes = {}
"""dico_des_artistes['Tiago'] = {}
dico_des_artistes['Tiago']['Mini-moke'] = 3
dico_des_artistes['Tiago']['Place de Clichy'] = 20
dico_des_artistes['dygor'] = {}
dico_des_artistes['dygor']['Mini-moke'] = 40
dico_des_artistes['dygor']['Place de Clichy'] = 15
dico_des_artistes['Ulysse'] = {}
dico_des_artistes['Ulysse']['Mini-moke'] = 5
dico_des_artistes['Ulysse']['non'] = 2
dico_des_artistes['k'] = {}
dico_des_artistes['k']['Mini-moke'] = 2
dico_des_artistes['k']['Place de Clichy'] = 5"""

if os.path.exists("Data/Dictionnaire_des_artistes_{}.json".format(modele[modele_actif])):
    with open("Data/Dictionnaire_des_artistes_{}.json".format(modele[modele_actif]), encoding="UTF-8") as f:
        a = json.load(f)
        for i, c in a.items():
            #print(c[0])
            dico_des_artistes[i] = c
else:
    for cle,valeur in dic_interro.items():
        #print(cle)
        
        dico_en = {}
        for i in range(len(valeur)):
            #print(valeur[i][2])
            for entite in valeur[i][2]:
                z = str(entite)
                #print(type(z))
                if z not in dico_en:
                    dico_en[z]=1
                else:
                    dico_en[z]+=1
        dico_des_artistes[cle]=dico_en
dico_des_artistes
with open("Data/Dictionnaire_des_artistes_{}.json".format(modele[modele_actif]), "w") as w:
    w.write(json.dumps(dico_des_artistes, indent=2))


# In[210]:


print(json.dumps(dico_des_artistes, indent=2))


# # Pour un lieux quel artiste en parle

# In[ ]:


#test
"""e = "Mini-moke"
for cle, valeur in dico_des_artistes.items():
    test = dico_des_artistes[cle]
    #print(type(test))
    for c, v in test.items():
        if c == e:
            tograph[cle] = v
print(tograph)"""


# In[8]:


import re
#print(dico_des_artistes['Jacques Dutronc'])

tograph = {}


def Chercherlieux(un_lieu):
    l = un_lieu
    tograph[l] = {}
    for cle, valeur in dico_des_artistes.items():
        dico_du_dico = dico_des_artistes[cle]
        for c, v in dico_du_dico.items():
            if c == un_lieu:
                tograph[l][cle] = v
    return tograph[l]



Chercherlieux("Place de Clichy")
Chercherlieux("Créteil")
Chercherlieux("Saint-Tropez")
Chercherlieux("Paris")
Chercherlieux("Lilas")


# In[ ]:


#a faire chercher les lieux qui commence par place


# In[9]:


#print(tograph)

tograph_trier = {}
for lieu, valeur in tograph.items():
    #g = tograph[lieu]
    #print(g)
    #print(lieu, valeur)
    tograph_trier[lieu] = {}
    for artiste, frequence in sorted(valeur.items(), key=lambda x: x[1], reverse=True):
        tograph_trier[lieu][artiste] = frequence
#print(tograph_trier)
for lieu2 , valeur in tograph_trier.items():
    for artiste, frequence in valeur.items():
        cinq_premier_lieux = [k for k in valeur.keys()][:5]
        cinq_premier_frequence = [k for k in valeur.values()][:5]
        print(cinq_premier_frequence, cinq_premier_lieux, frequence)
        break
            
    #g = tograph_trier[cle]
    #print(g)


# In[482]:


print(tograph_trier)


# In[10]:


import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure()
for lieu2 , valeur in tograph_trier.items():
    for artiste, frequence in valeur.items():
        #if artiste <= 5:
        if 2 > 1:
            #print(lieu2, frequence)
            #g = tograph_trier[cle]
            y = cinq_premier_frequence = [k for k in valeur.values()][:5]
            x = cinq_premier_lieux = [k for k in valeur.keys()][:5]
            width = 0.50
            #x2 = plt.xlabel(x,color="r")
            #plt.ylabel(height,color="r")
            plt.title(lieu2, color='r')
            plt.bar(x, y, width, color='green')

            plt.savefig('Data/image_large/%s.png'%lieu2)
            plt.show()
            break


# # Pour chaque lieux calculer sa fréquence dans le corpus¶

# In[11]:


for lieu, dico in tograph.items():
    total_apparition_corpus = 0
    for artiste, apparition in dico.items():
        total_apparition_corpus += apparition
       #print(lieu, total_apparition_corpus)
    print(lieu, total_apparition_corpus)


# In[ ]:


#pour le pourcentage des lieux de paris.
#somme a l'interieur d'un auteur = exemple 80% des EN sont des lieux de paris.
#somme globale. = pour un lieu qui est l'auteur qui a le plus parlé?


# # le lieu le plus fréquent pr un artiste

# In[5]:


#somme globale. = pour un lieu qui est l'auteur qui a le plus parlé?
    #print()
dico_des_lieux = {}


for cle, valeur in dic_interro.items():
    #dico_en = {}
    for i in range(len(valeur)):
        dico_tempo = {}
        for entite in valeur[i][2]:
            #print(entite)
            dico_des_lieux.setdefault(entite, {})
            dico_des_lieux[entite].setdefault(cle, 0)
            dico_des_lieux[entite][cle]+=1
            
with open("Data/Dictionnaire_lieux_paris_{}.json".format(modele[modele_actif]), "w") as w:
    w.write(json.dumps(dico_des_lieux, indent=2))

#print(dico_des_lieux)


# In[13]:


tograph2 = {}
def ChercherArtiste(nom_artiste):
    l = nom_artiste
    tograph2[l] = {}
    for cle, valeur in dico_des_lieux.items():
        if cle in vrai_entite_nomme:
            dico_du_dico = dico_des_lieux[cle]
            for c, v in dico_du_dico.items():
                if c == l:
                    tograph2[l][cle] = v
    return tograph2[l]
ChercherArtiste("_JoeDassin")


# In[14]:


tograph2_trier = {}
#count = 0
for cle, valeur in tograph2.items():
    g = tograph2[cle]
    #print(g.values())
    for artiste, frequence in sorted(valeur.items(), key=lambda x: x[1], reverse=True):
        tograph2_trier[artiste] = frequence
        
cinq_premier_lieux = [k for k in tograph2_trier.keys()][:5]
#print(premier_lieux)
        #count += 1
#print(tograph2)
print(tograph2_trier)

#code a modifier pour récuperer les 5 premières valeur du dic.


# In[15]:


import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure()
for cle, valeur in tograph2.items():
#if 2>0:
    cinq_premier_lieux_item = [k for k in tograph2_trier.items()][:5]
    cinq_premier_lieux_keys = [k for k in tograph2_trier.keys()][:5]
    cinq_premier_lieux_values = [k for k in tograph2_trier.values()][:5]
    g = cinq_premier_lieux
    x = cinq_premier_lieux_keys
    height = cinq_premier_lieux_values
    width = 0.50
    #x2 = plt.xlabel(x,color="r")
    #plt.ylabel(height,color="r")
    plt.title(cle, color='r')
    plt.bar(x, height, width, color='green')
    
    plt.savefig('Data/image_{}/{}.png'.format(modele[modele_actif],cle))
    plt.show()       


# In[6]:


dic_interro_des_lieux = {}
#print(dic_interro.items())
if os.path.exists("Data/Dictionnaire_interro_lieux_paris_{}.json".format(modele[modele_actif])):
    with open("Data/Dictionnaire_interro_lieux_paris_{}.json".format(modele[modele_actif]), encoding="UTF-8") as f:
        dic_interro_des_lieux = json.load(f)
else:
    for artiste, valeur in dic_interro.items():
        for i in range(len(valeur)):
            #print(valeur[i][0]) #titre
            #print(valeur[i][2]) #entité
            #print(valeur[i][1]) #date
            for entite in valeur[i][2]:
                dic_interro_des_lieux.setdefault(entite, {})
                dic_interro_des_lieux[entite].setdefault(artiste, [])
                dic_interro_des_lieux[entite][artiste].append([valeur[i][0],valeur[i][1]])
#print(dic_interro_des_lieux)
            
with open("Data/Dictionnaire_interro_lieux_paris_{}.json".format(modele[modele_actif]), "w") as w:
    w.write(json.dumps(dic_interro_des_lieux, indent=2)) 
    


# In[175]:


print(json.dumps(dic_interro_des_lieux, indent=2))


# In[18]:



def infolieu():
    cpt = 0 
    recherche = input()
    for lieu, dico in dic_interro_des_lieux.items():
        if lieu == recherche:
        #print(dico.items())

            for artiste, valeur in dico.items():
                #print(valeur[0][1]) #date
                #print(valeur[0][0]) #titre
                for i in valeur:
                    #continue
                    cpt += 1
                    print(lieu, "\t",artiste,"\t", i, cpt)
    return None
infolieu()


# In[19]:


dic_for_date = {}

for nom_artiste, valeur in dic_interro.items():
    for x in valeur:
        titre = x[0]
        date = x[1]
        if date != None:
            dic_for_date.setdefault(date, [])
            for lieu in x[2]:
                #print(lieu)
                if lieu in vrai_entite_nomme:
                    #print(lieu)
                    dic_for_date[date].append([lieu, titre])
        #print(x[1]) #Date
print(dic_for_date)


# In[179]:


import re

dictionnaire = {}          
def find_lieu_titre_par_annee(annee, dictionnaire):
    years = r"%s-\d\d-\d\d"%annee
    for date, valeur in dic_for_date.items():
        match = re.search(years, date)
        if match:
            dictionnaire.setdefault(annee, {})
            for x in valeur:
                lieu = x[0]
                dictionnaire[annee].setdefault(lieu, 0)
                dictionnaire[annee][lieu] += 1
    return dictionnaire


# In[180]:


observation = {}
cpt = 1950

while cpt <= 2000:
    print(find_lieu_titre_par_annee(cpt, observation))
    cpt += 1


# In[193]:


tograph3 = {}
find_lieu_titre_par_annee(2010, tograph3)


# In[194]:


freq = []
lieu = []


for date, valeur in tograph3.items():
    toto = sorted([[freq, nom] for nom,freq in valeur.items()], reverse=True)
    for i in range(len(toto)):
        freq.append(toto[i][0])
        lieu.append(toto[i][1])

print(toto)
print(freq)
print(lieu)
    #cinq_premier_lieux_values = toto[:5]
    #print(cinq_premier_lieux_values)


# In[195]:


#fig = plt.figure()
import matplotlib.pyplot as plt
import numpy as np
x = [x for x in lieu][:5]
height = [x for x in freq][:5]
width = 0.50
    #x2 = plt.xlabel(x,color="r")
    #plt.ylabel(height,color="r")
plt.title(date, color='r')
plt.bar(x, height, width, color='green')

plt.savefig('Data/image_{}/{}.png'.format(modele[modele_actif],date))
plt.show()       


# # Un code qui propose le lieu detecter par spacy et l'ajoute dans le corpus lieux de paris pour le compléter.

# In[77]:


tous_les_locatifs = []

for lieux in locatif_sm:
    tous_les_locatifs.append(lieux)
#print(lieux_des_3_modèles)
for lieux in locatif_md:
    tous_les_locatifs.append(lieux)
for lieux in locatif_lg:
    tous_les_locatifs.append(lieux)   
lieux_des_3_modèles = set(tous_les_locatifs)
#print(lieux_des_3_modèles)

with open("Data/Tous_les_lieux_paris_detecte.json", "w") as w:
    w.write(json.dumps(tous_les_locatifs))


# In[ ]:


oui = "oui"
non = "non"
fini = "stop"
dictionnaire_to_corpus_lieux = {}

for lieux in lieux_des_3_modèles:
    if lieux not in vrai_entite_nomme:
        ajout_dans_corpus = input("""Ce lieux "%s" est-il un lieux de paris ? Répondez par oui/non :""" %lieux)
        if ajout_dans_corpus == oui:
            dictionnaire_to_corpus_lieux.setdefault(lieux, [])
            precision = input("Ce lieux possède t'il d'autre nom que vous connaissez? Répondez par oui/non :")
            autre_nom = []
            if precision == oui:
                nom = input("""insérez les autres nom, sinon écrivez "stop" pour arreter :""")
                autre_nom.append(nom)
                while nom != fini:
                    nom = input("""insérez un autres nom, sinon écrivez "stop" pour arreter :""")
                    autre_nom.append(nom)
                autre_nom.pop(-1)
                dictionnaire_to_corpus_lieux[lieux].append(autre_nom)
                    #faire répéter la commande autant de fois jusqu'a ce qu'il disent non.
            if precision == non:
                dictionnaire_to_corpus_lieux[lieux].append(None)
                continue
        if ajout_dans_corpus == non:
            pass
with open("Data/Dictionnaire lieux implémenté.json", "w") as w:

    w.write(json.dumps(dictionnaire_to_corpus_lieux, indent=2))


# In[ ]:


#sur quelque texte faire une sortie ou chaque token du txt et l'étiquette donner par spacy 


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# 

# In[ ]:





# In[ ]:





# 

# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# # Statistique sur les mots qui sont avant le lieu

# In[ ]:





# In[ ]:





# 

# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[21]:


for lieu, valeur in dic_interro_des_lieux.items():
    for artiste, liste in valeur.items():
        date = liste[0][1] #date
        titre = liste[0][0] #titre
        print(date)


# # Lieux dans google map

# In[221]:


#pip install geopy


# In[ ]:


#dic_for_map = {}
#dic_for_map = {"ID":  ,}
to_map = []
import tqdm
from geopy.geocoders import Nominatim
for lieu, valeur in tqdm.tqdm(dic_interro_des_lieux.items()):
    for artiste, liste in valeur.items():
        date = liste[0][1] #date
        titre = liste[0][0] #titre
        paris = ",Iles-de-France"
        geolocator = Nominatim(user_agent="Tiago")
        try:
            location = geolocator.geocode("{}, {}".format(lieu, paris), timeout=20 )
            adresse = location.address
            to_map.append([lieu, adresse, location.latitude, location.longitude, date, titre])
        except:
            pass
        
        #print(location.address)
        #print((location.latitude, location.longitude))
        #print(location.raw)

import csv
with open('to_map.csv', 'w', newline='') as file:
    writer = csv.writer(file, quoting=csv.QUOTE_ALL,delimiter=';')
    writer.writerows(to_map)
#with open("to_map.csv", "w" ,newline='') as csvfile:
    #writer = csv.writer(csvfile)
    #writer.writerow(to_map)
    #spamreader = csv.reader(csvfile, delimiter=' ', quotechar= '|')
    #for row in spamreader:
        #print('; '.join(row))
print(to_map)


# In[ ]:


#dic_for_map = {}
#dic_for_map = {"ID":  ,}
to_map = []
import tqdm
from geopy.geocoders import Nominatim
for lieu, valeur in tqdm.tqdm(dic_interro_des_lieux.items()):
    for artiste, liste in valeur.items():
        date = liste[0][1] #date
        titre = liste[0][0] #titre
        paris = ",Iles-de-France"
        geolocator = Nominatim(user_agent="Tiago")
        try:
            location = geolocator.geocode("{}, {}".format(lieu, paris), timeout=60 )
            adresse = location.address
            to_map.append([lieu, adresse, location.latitude, location.longitude, date, titre])
        except:
            pass
        
        #print(location.address)
        #print((location.latitude, location.longitude))
        #print(location.raw)

import csv
with open('to_map.csv', 'w', newline='') as file:
    writer = csv.writer(file, quoting=csv.QUOTE_ALL,delimiter=';')
    writer.writerows(to_map)
#with open("to_map.csv", "w" ,newline='') as csvfile:
    #writer = csv.writer(csvfile)
    #writer.writerow(to_map)
    #spamreader = csv.reader(csvfile, delimiter=' ', quotechar= '|')
    #for row in spamreader:
        #print('; '.join(row))
print(to_map)


# In[226]:


from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="Tiago")

location = geolocator.reverse("50.3588778, 3.4940984")

print(location.address)
print((location.latitude, location.longitude))

print(location.raw))


# In[233]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# 

# In[ ]:





# In[ ]:





# # Tache a effecuté
# finir la partir structure des musiques (rythme =/= métrique)
# a quel endroit l'artiste va parler du lieu (refrain ou couplet ?)
# statistique sur les mots (like memoire blanc)
# partie sur la NER
# 

# In[ ]:





# In[ ]:




