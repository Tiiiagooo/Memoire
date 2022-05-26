#!/usr/bin/env python
# coding: utf-8

# # pour le lieu x  dans quel chanson apparait-il ?

# In[4]:


#ouverture et lecture des json
import json
def ouvrir_json(chemin):
    f = open(chemin, encoding="utf-8")
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
    tokenizer = nltk.RegexpTokenizer(r"(\w+,\w+|\w+-\w+|\w+\.\w+\.\w+|\w+\S|\w+|\S|\w+\S|\?|\!)")
    txt_split = tokenizer.tokenize(txt)
    return txt_split
def Splittxt2(txt):
    tokenizer = nltk.RegexpTokenizer(r"(\w+'|\w+\S\w+|\w+-\w+|\w+|\S|\w+\S)")
    txt_split = tokenizer.tokenize(txt)
    return txt_split


# In[7]:


#pour afficher paroles des chansons du fichier echantillon1.json

import json
i = ouvrir_json("echantillon1.json")
start = i["_all/"]
#j'ai créer une liste vide pour regrouper tous les listes de txt (chaque txt et dans une liste)
tous_les_txt = []
for element in start:
    liste_txt = []
    txt = element["lyrics"]
    titre = element["full_title"]
    liste_txt.append(txt)
    tous_les_txt.append(liste_txt)
    print(titre)
    print(liste_txt, "-"*70)
print(tous_les_txt)


# # création d'une liste des lieux de paris

# In[2]:



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


# In[9]:


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


# In[10]:


import nltk
chanson = []
for element in start:
    liste = []
    txt = element["lyrics"]
    try:
        for l in txt.split("\n"):
            #lignes_chanson.append(l)
            liste.append(l)
        chanson.append(liste) #lignes_chanson.append([l])
    except:
        chanson.append(["None"])
        
print(len(chanson))
FP = 0 # On a modifié et on a eu tord
VP = 0 # On a modifié et on a eu raison
FN = 0 # On a pas modifié et on a eu tord
VN = 0 # On a pas modifié et on a eu raison.

#print(chanson)
count = -1
for liste_lignes_chanson in chanson:
    count += 1
    for ligne in liste_lignes_chanson:
        #print(ligne)
        expr = re.compile("^(\w+'|\w+-\w+|\w+)")
        match = expr.finditer(ligne)
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
                        liste_mots = Splittxt2(ligne)      #permet de découper ma ligne en liste de mot.
                        liste_mots[0] = mot_lower            #le mot en début de ligne je le remplace par mot.
                        nouvelle_ligne = " ".join(liste_mots)  #je reassemble ma ligne.
                        nouvelle_ligne = re.sub("\'\s", "\'", nouvelle_ligne)
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
print(len(chanson))


# # Enregistrer les chansons dans un json.

# In[20]:


comptage = 0

num_chanson = []

for i in chanson:
    m = []
    nv_echantillon = "\n".join(i)
    m.append(nv_echantillon)
    #print(m)
    #num_chanson.append(nv_echantillon)
    num_chanson.append(m)
    #print(num_chanson[comptage])
        
    #print(num_chanson[comptage], "\n")
        
        
#print(num_chanson[0])    
Dic_nouvelle_chansons = {}
#Dic_nouvelle_chansons.setdefault()

#Dic_nouvelle_chansons["all"]["Titre_chanson"] = {}
#Dic_nouvelle_chansons["all"]["Auteur"]
#Dic_nouvelle_chansons["all"]["lyrics"] = {}

#Dic_nouvelle_chansons["Titre_chanson"] = {}
#Dic_nouvelle_chansons["lyrics"] = {}
for elem in start:
    #Dic_nouvelle_chansons.setdefault()
    Dic_nouvelle_chansons["all"] = {}
    titre = elem["full_title"]
    try:
        artiste = elem["album"]["artist"]["name"]
    except:
        artiste = "none"
    if titre not in Dic_nouvelle_chansons:
        Dic_nouvelle_chansons["all"]["Titre_chanson"] = titre
        #print(Dic_nouvelle_chansons)
        Dic_nouvelle_chansons["all"]["Auteur"] = artiste
        Dic_nouvelle_chansons["all"]["lyrics"] = num_chanson[comptage]
        comptage += 1

#with open("Data/nouvel_echantillon.json", "w") as w:
    #w.write(json.dumps(Dic_nouvelle_chansons, indent=2))
print(Dic_nouvelle_chansons)


# # Exemple qui fonctionne

# In[16]:


dicoooooooo = {}
count = 0 
for elem in start:
    titre = elem["full_title"]
    dicoooooooo[titre] = {}
    dicoooooooo[titre]["lyrics"] =  {}
    dicoooooooo[titre]["lyrics"] = num_chanson[count]
    count += 1
    
print(dicoooooooo)


# In[ ]:





# In[ ]:




