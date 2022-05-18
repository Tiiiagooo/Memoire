#!/usr/bin/env python
# coding: utf-8

# In[311]:


#load le modèle medium
#!python -m spacy download fr_core_news_md


# # Ouverture et lecture des json

# In[45]:


#ouverture et lecture des json
import json
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
    tokenizer = nltk.RegexpTokenizer(r"(\w+,\w+|\w+-\w+|\w+\.\w+\.\w+|\w+\S|\w+|\S|\w+\S|\?|\!)")
    txt_split = tokenizer.tokenize(txt)
    return txt_split
def Splittxt2(txt):
    tokenizer = nltk.RegexpTokenizer(r"(\w+'|\w+-\w+|\w+|\S|\w+\S)")
    txt_split = tokenizer.tokenize(txt)
    return txt_split


# # Affichage des paroles du fichier

# In[46]:


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


# # Création d'une liste lieux de paris 

# In[47]:


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


# # Affichage des EN trouvé par Spacy

# In[42]:


#!python −m spacy download fr_core_news_sm
#!python −m spacy download fr_core_news_md
#!python −m spacy download fr_core_news_lg


# In[230]:


#affichage des EN trouvé par spacy
import nltk
from nltk.tokenize import word_tokenize
import re
import spacy

#nlp = spacy.load('fr_core_news_sm') #modèle small
nlp = spacy.load('fr_core_news_md') #modèle medium
#nlp = spacy.load('fr_core_web_lg') #modèle large
compteur = 0
tokenizer = nltk.RegexpTokenizer(r"(\w+,\w+|\w+-\w+|\w+\.\w+\.\w+|\w+\S|\w+|\S|\w+\S|\?|\!)") #Pour les mots du texte javai pour le 1er
                                                                                              #600 résultats
                                                                                              # j'ai utiliser tokenizer pour séparer les mots du texte.
        
        
EN = []
print("#"*50, "\nvoici les musiques sur lequels l'on va travailler")
#--------------------------------------------------------------------------------------------------------------------
for txt in tous_les_txt :
    for l in txt :
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
            print("\n Ce texte contient ", len(split_txt), " mot")
            print("\n","Traitement...","\n")
            for ent in doc.ents:
                if ent.label_ == "LOC":
                    locatif = ent.text
                    entite_nomme.append(locatif)
            print("\n Le texte a trouvé {} Entité Nommé locatif, ce sont: ".format(len(entite_nomme)))
            print(set(entite_nomme))
            EN.append(entite_nomme)
            print(EN)
        except:
            pass

           
    #print(type(l))
#etiquettage étrange à cause des maj? et il faut comprendre l'étiquettage.


# # Calcul des Proportions des EN de spacy

# In[92]:


#récuperer les fichiers json
import os
import glob
import json
path = "proportion"

liste_fichiers = glob.glob("%s/*.json"%path)
#print(len(liste_fichiers))
#print(liste_fichiers)


# In[231]:


#calcul de la proportion des EN de spacy
import nltk
from nltk.tokenize import word_tokenize
import re
import operator

compteur = 1
tokenizer = nltk.RegexpTokenizer(r"(\w+,\w+|\w+-\w+|\w+\.\w+\.\w+|\w+\S|\w+|\S|\w+\S|\?|\!)")
proportion_EN_spacy = {}
Proportion = []



if os.path.exists("proportion/proportion Entite nomme spacy_medium.json"):
    with open("proportion/proportion Entite nomme spacy_medium.json", encoding='UTF-8') as f:
        a = json.load(f)
        #print(a)
        for c, v in a.items():
            Proportion.append(v)
            #Proportion.append(i[1]) #reprend uniquement mon premier fichier json
else:
    for txt in tous_les_txt :
        for l in txt :
            try:
                    
                doc = nlp(l)
                entite_nomme = []
                split_txt = tokenizer.tokenize(l) 
                for ent in doc.ents:
                    if ent.label_ == "LOC":
                        locatif = ent.text
                    #print(ent.text, ent.label_)
                        entite_nomme.append(locatif)
                    proportion = len(entite_nomme)/len(split_txt)
      
                Proportion.append(proportion*100)
                print("La proportion des EN sur la taille du texte {} est de".format(compteur), proportion*100, "%")
                compteur += 1
                
            except:
                #print(l)
                Proportion.append(0)
                print("La proportion des EN sur la taille du texte {} est de 0%".format(compteur))
                compteur += 1
   

print(len(Proportion))
count = 0
for element in start:
    titre = element["full_title"]
    essaie = [stat for stat in Proportion if stat not in proportion_EN_spacy]
    #print(essaie)
    proportion_EN_spacy[titre] = essaie[count]
    count += 1
#print(proportion_EN_spacy)
with open("proportion/proportion Entite nomme spacy_medium.json", "w") as w:
    w.write(json.dumps(proportion_EN_spacy, indent=2))


# In[232]:


print(json.dumps(proportion_EN_spacy, indent=2))


# In[ ]:





# # Calcul des proportions des EN qui ont match avec les fichiers des lieux de paris

# In[ ]:





# In[233]:


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
if os.path.exists("proportion/proportion Entite matché_medium.json"):
    with open("proportion/proportion Entite matché_medium.json", encoding='UTF-8') as f:
        a = json.load(f)
        for i, c in a.items():
            Proportion2.append(c[1])
            en_Match[i]= [c[0], c[1], c[2]] #reprend uniquement mon premier fichier json
            
else:
    for element in start:
        txt = element["lyrics"]
        #print(element.keys())
        titre = element["full_title"]
        print(titre)
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
                for ent in doc.ents:
                    liste_temporaire.append(ent.text)

                match =  [i for i in liste_temporaire if i in vrai_entite_nomme]#Pour chaque match on calcul la proportion par texte.
                proportion = len(match)/len(split_txt)
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


with open("proportion/proportion Entite matché_medium.json", "w") as w:
    w.write(json.dumps(en_Match, indent=2))       
            
            
print(len(Proportion2))
#print(Proportion2)
#print(en_Match)
#print(proportion_EN_matché)
        


# In[234]:


print(json.dumps(en_Match, indent=2))


# # Proportion des lettres capitale dans les textes

# In[235]:



import nltk
from nltk.tokenize import word_tokenize
import re

compteur = 0
proportion_maj = {}
Proportion3 = []
tokenizer = nltk.RegexpTokenizer(r"(\w+,\w+|\w+-\w+|\w+\.\w+\.\w+|\w+\S|\w+|\S|\w+\S|\?|\!)")

if os.path.exists("proportion des majuscules.json"):
    with open(path_json) as f:
        cle, valeur = json.load(f)
        Proportion3.append(valeur)
else:
     for txt in tous_les_txt:
            for i in txt:
                if i != None:                    
                    majuscule = []
                    txt_split = tokenizer.tokenize(i)
                    #print(txt_split)
                    for eleme in txt_split:
                        if eleme.istitle() == True:
                            majuscule.append(eleme)
                            proportion = (len(majuscule)/len(txt_split))*100
                    Proportion3.append(proportion)
                    compteur += 1
                    print("La proportion des mots en majuscule sur le texte n°{} est de {}".format(compteur, proportion),"%")
                    print("Il y a %s Mot qui on une maj sur %s mot \n"%(len(majuscule), len(txt_split)))

                    #print(majuscule)
                    
                    
                else:
                    #print(i)
                    Proportion3.append(0)
                    compteur += 1
                    print("La proportion des mots en majuscule sur le texte n°{} est de 0% \n".format(compteur))
                
                    
print(len(Proportion3))



count = 0
for element in start:
    titre = element["full_title"]
    essaie = [stat for stat in Proportion3 if stat not in proportion_maj]
    #print(essaie)
    proportion_maj[titre] = essaie[count]
    count += 1
with open("proportion/proportion des majuscules.json", "w") as w:
    w.write(json.dumps(proportion_maj, indent=2))


# In[78]:


print(json.dumps(proportion_maj, indent=2))


# # initialisation d'un dic pr overleaf

# In[236]:



dictionnaire_tableau = {}
compteuur = 0

valeur1 = [v for v in Proportion]
valeur2 = [v for v in Proportion2]
valeur3 = [v for v in Proportion3]


for element in start:
    titre = element["full_title"]
    dictionnaire_tableau[titre] = [valeur1[compteuur], valeur2[compteuur], valeur3[compteuur]]
    compteuur += 1

print(dictionnaire_tableau)


# # affichage pr overleaf
# 

# In[237]:



nom_colone = ["Titre chanson", "Proportion EN spacy", "Proportion EN matché", "Proportion Majuscule"]
print("\\begin{table}")
print("\\centering")
print("\t\\begin{tabular}{|l|l|l|l|}")
print("\t\\hline")
print(" \t %s \\\\" %(" & ".join(nom_colone)))
print("\t\\hline")
#ne pas trier les valeurs tant que toutes les valeurs ne sont pas inscrite.
#ou une boucle qui récupère pour chaque titre leurs valeurs.
for titre, proportion in sorted(dictionnaire_tableau.items(), key=lambda x: x[1], reverse=True):
    ligne = "\t %s... \t& %s \t& %s \t& %s \\\\\n\t\\hline  " %(str(titre[:20]), round(proportion[0], 4), round(proportion[1], 4), round(proportion[2], 4))
    print(ligne)
print("\t\end{tabular}")
print("\end{table}")


# # code pour regrouper les lieux de paris.

# In[238]:



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
    [r'^(Saint|saint|st|St)',  "Saint"]]:
    dic_lieu = regroupement_lieu_paris(expr, cle, dic_lieu)
    dic_lieu["inclassable"] = dic_lieu["inclassable"].difference(dic_lieu[cle])
    
print("")
taille_voc = len(set(vrai_entite_nomme))
print(taille_voc)
for cle, liste in dic_lieu.items():
    print(cle,"|", len(dic_lieu[cle]), "|",  len(dic_lieu[cle])/taille_voc)
#print(dic_lieu["Arrondissement"])



# # Code pour construction tableau overleaf

# In[239]:



nom_tableau = ["Lieu", "taille", "proportion"]
print("\t\\begin{tabular}{|l|l|l|}")
print("\t\\hline")
print(" \t %s \\\\" %(" & ".join(nom_tableau)))
print("\t\\hline")

for cle, valeur in dic_lieu.items():
    ligne = "\t %s \t& %s \t& %s \\\\\n\t\\hline  "%(cle, len(dic_lieu[cle]),(len(dic_lieu[cle])/taille_voc)*100)
    print(ligne)
print("\t\end{tabular}")
print("\end{table}") 


# # faire un dictionnaire d'interrogation permettant de lister toutes les chansons qui parle de paris par auteur

# In[276]:


if os.path.exists("Data/Dictionnaire_artiste_to_lieux_paris_medium.json"):
    with open("Data/Dictionnaire_artiste_to_lieux_paris_medium.json", encoding="UTF-8") as f:
        a = json.load(f)
        for i, c in a.items():
            #print(c[0])
            dic_interro[i] = c
print(dic_interro)


# In[282]:



dic_interro = {}

if os.path.exists("Data/Dictionnaire_artiste_to_lieux_paris_medium.json"):
    with open("Data/Dictionnaire_artiste_to_lieux_paris_medium.json", encoding="UTF-8") as f:
        a = json.load(f)
        for i, c in a.items():
            #print(c[0])
            dic_interro[i] = c
        
else:
    for element in start:
        txt = element["lyrics"]
        #print(element.keys())
        titre = element["full_title"]
        try:
            artiste = element["album"]["artist"]["name"]
        except:
            continue
        date = element["release_date"]
        dic_interro.setdefault(artiste, [])
        if 2>1 :
            try:
                doc = nlp(txt)
                liste_temporaire = []
                for ent in doc.ents:
                        if ent.label_ == "LOC":
                            locatif = ent.text
                            #print(locatif)
                            liste_temporaire.append(locatif)
                if locatif in dic_interro:
                    print("deja dans le dictionnaire") #problème le nom de l'artiste existe deja comment l'ajouter au dictionnaire ?
                else:
                    #print(type(liste_temporaire[0]))
                    dic_interro[artiste].append([titre, date, liste_temporaire])


            except:
                pass

print(dic_interro)
T = dic_interro.values()
for artiste, T in dic_interro.items():
    #print(T)
    #nb_nom_paris = len([x for x in T if len x[2]==0])
    nb_total_chanson = len(T)
    print(nb_total_chanson)
    
with open("Data/Dictionnaire_artiste_to_lieux_paris_medium.json", "w") as w:
    w.write(json.dumps(dic_interro, indent=2))


# # Créer un graph des artistes parlant du + "x".
# x = un lieu de paris. 
# somme globale. = pour un lieu qui est l'auteur qui a le plus parlé?

# In[298]:


#somme globale. = pour un lieu qui est l'auteur qui a le plus parlé?
    #print()
dico_des_artistes = {}
dico_des_artistes['Tiago'] = {}
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
dico_des_artistes['k']['Place de Clichy'] = 5

if os.path.exists("Data/Dictionnaire_des_artistes_medium.json"):
    with open("Data/Dictionnaire_des_artistes_medium.json", encoding="UTF-8") as f:
        a = json.load(f)
        for i, c in a.items():
            #print(c[0])
            dico_des_artistes[i] = c
for cle,valeur in dic_interro.items():
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
with open("Data/Dictionnaire_des_artistes_medium.json", "w") as w:
    w.write(json.dumps(dico_des_artistes, indent=2))


# In[297]:


print(json.dumps(dico_des_artistes, indent=2))


# In[305]:


import re
#print(dico_des_artistes['Jacques Dutronc'])

tograph = {}
"""e = "Mini-moke"
for cle, valeur in dico_des_artistes.items():
    test = dico_des_artistes[cle]
    #print(type(test))
    for c, v in test.items():
        if c == e:
            tograph[cle] = v
print(tograph)"""

def Chercherlieux(un_lieu_de_paris):
    l = un_lieu_de_paris 
    tograph[l] = {}
    for cle, valeur in dico_des_artistes.items():
        dico_du_dico = dico_des_artistes[cle]
        for c, v in dico_du_dico.items():
            if c == un_lieu_de_paris:
                tograph[l][cle] = v
    return tograph[l]


Chercherlieux("Mini-moke")
Chercherlieux("Place de Clichy")
Chercherlieux("Créteil")
Chercherlieux("Saint-Tropez")


# In[306]:


print(tograph)
for cle, valeur in tograph.items():
    g = tograph[cle]
    print(g)


# In[303]:


import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure()
for cle, valeur in tograph.items():
    g = tograph[cle]
    x = g.keys()
    height = g.values()
    width = 0.50
    #x2 = plt.xlabel(x,color="r")
    #plt.ylabel(height,color="r")
    plt.title(cle, color='r')
    plt.bar(x, height, width, color='green')
    
    plt.savefig('Data/image_medium/%s.png'%cle)
    plt.show()


# In[22]:


#pour le pourcentage des lieux de paris.
#somme a l'interieur d'un auteur = exemple 80% des EN sont des lieux de paris.
#somme globale. = pour un lieu qui est l'auteur qui a le plus parlé?


# In[23]:


#sur quelque texte faire une sortie ou chaque token du txt et l'étiquette donner par spacy 


# In[24]:


#BIO, detecter les personnes 


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

# In[25]:


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


# In[26]:


#stat sur date, lieu le plus fréquent, 
#


# In[307]:


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


# In[ ]:





# # Erreur il ne fait la boucle que sur le 1er élement de la liste (à cause du remove)

# In[28]:





# In[308]:


compteur = 0
lignes_chanson = []
for element in start:
    txt = element["lyrics"]
    #print(element.keys())
    titre = element["full_title"]
    try:
        artiste = element["album"]["artist"]["name"]
    except:
        continue
    date = element["release_date"]
    try:
        for l in txt.split("\n"):
            lignes_chanson.append(l)

    except:
        pass
    
FP = 0 # On a modifié et on a eu tord
VP = 0 # On a modifié et on a eu raison
FN = 0 # On a pas modifié et on a eu tord
VN = 0 # On a pas modifié et on a eu raison.
#------------------------------------------------------------------------------------------------------------
#boucle qui parcours ma liste lignes_chanson
for z in lignes_chanson:
    expr = re.compile("^(\w+'|\w+-\w+|\w+)")
    match = expr.finditer(z)
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
                    liste_mots = Splittxt2(z)      #permet de découper ma ligne en liste de mot.
                    liste_mots[0] = mot_lower            #le mot en début de ligne je le remplace par mot.
                    nouvelle_ligne = " ".join(liste_mots)  #je reassemble ma ligne.
                    #print(lignes_chanson, "\n")
                    res = [elem.replace(z,nouvelle_ligne) for elem in lignes_chanson]  #je remplace 
                    lignes_chanson = res               #l'ancienne ligne par une nouvelle ligne.  #VP 
                    VP += 1
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
                #liste_mots = Splittxt2(z)
                #liste_mots[0] = mot
                #nouvelle_ligne = " ".join(liste_mots)
                #print(lignes_chanson, "\n")
                #res = [elem.replace(z,nouvelle_ligne) for elem in lignes_chanson]
                #lignes_chanson = res

        

    


# In[33]:


print(lignes_chanson)


# In[309]:


print("FP = ",FP)
print("VP = ",VP)
print("FN = ",FN)
print("VN = ",VN)


# In[310]:


accuracy = VP/(VP + FP)
rappel = VP / (VP + FN)
f_mesure = (2*(accuracy*rappel))/(accuracy+rappel)
print("accuracy = ",accuracy)
print("rappel = ",rappel)
print("f_mesure = ",f_mesure)


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





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




