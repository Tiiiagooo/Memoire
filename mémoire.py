#!/usr/bin/env python
# coding: utf-8

# In[1]:


#load le modèle large
#!python -m spacy download fr_core_news_lg


# # Ouverture et lecture des json

# In[2]:


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
    tokenizer = nltk.RegexpTokenizer(r"(\w+'|\w+-\w+|\w+|\S|\w+\S)")
    txt_split = tokenizer.tokenize(txt)
    return txt_split


# # Affichage des paroles du fichier

# In[3]:


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

# In[4]:


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

# In[5]:


#affichage des EN trouvé par spacy
import nltk
from nltk.tokenize import word_tokenize
import re
import spacy

nlp = spacy.load('fr_core_news_sm')
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
            print("\n Le texte a trouvé {} Entité Nommé, les locatifs sont: ".format(len(entite_nomme)))
            print(set(entite_nomme))
            EN.append(entite_nomme)
            print(EN)
        except:
            pass

           
    #print(type(l))
#etiquettage étrange à cause des maj? et il faut comprendre l'étiquettage.


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


# In[7]:


#calcul de la proportion des EN de spacy
import nltk
from nltk.tokenize import word_tokenize
import re
import operator

compteur = 1
tokenizer = nltk.RegexpTokenizer(r"(\w+,\w+|\w+-\w+|\w+\.\w+\.\w+|\w+\S|\w+|\S|\w+\S|\?|\!)")
proportion_EN_spacy = {}
Proportion = []



if os.path.exists("proportion/proportion Entite nomme spacy2.json"):
    with open(path_json, encoding='UTF-8') as f:
        a = json.load(f)
        for i in a:
            Proportion.append(i[1]) #reprend uniquement mon premier fichier json
else:
    for txt in tous_les_txt :
        for l in txt :
            try:
                    
                doc = nlp(l)
                entite_nomme = []
                split_txt = tokenizer.tokenize(l) 
                for ent in doc.ents:
                    #print(ent.text, ent.label_)
                    entite_nomme.append(ent.text)
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
    with open("proportion/proportion Entite nomme spacy.json", "w") as w:
        #out = [a, b]
        w.write(json.dumps(proportion_EN_spacy, indent=2))
        


# In[8]:


print(json.dumps(proportion_EN_spacy, indent=2))


# In[ ]:





# # Calcul des proportions des EN qui ont match avec les fichiers des lieux de paris

# In[9]:


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
            
        with open("proportion/proportion Entite matché.json", "w") as w:
            w.write(json.dumps(en_Match, indent=2))       
            
            
print(len(Proportion2))
#print(Proportion2)
#print(en_Match)
#print(proportion_EN_matché)
        


# In[10]:


print(json.dumps(en_Match, indent=2))


# # Proportion des lettres capitale dans les textes

# In[11]:



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


# In[12]:


print(json.dumps(proportion_maj, indent=2))


# # initialisation d'un dic pr overleaf

# In[13]:



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

# In[14]:



nom_colone = ["Titre chanson", "Proportion EN spacy", "Proportion EN matché", "Proportion Majuscule"]
print("\\begin{table}")
print("\t\\begin{tabular}{|l|l|l|l|}")
print("\t\\hline")
print(" \t %s \\\\" %(" & ".join(nom_colone)))
print("\t\\hline")
#ne pas trier les valeurs tant que toutes les valeurs ne sont pas inscrite.
#ou une boucle qui récupère pour chaque titre leurs valeurs.
for titre, proportion in sorted(dictionnaire_tableau.items(), key=lambda x: x[1], reverse=True):
    ligne = "\t %s... \t& %s \t& %s \t& %s \\\\\n\t\\hline  " %(str(titre[:20]), round(proportion[0], 2), round(proportion[1], 2), round(proportion[2], 2))
    print(ligne)
print("\t\end{tabular}")
print("\end{table}")


# # code pour regrouper les lieux de paris.

# In[15]:



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

# In[16]:



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

# In[17]:



dic_interro = {}
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
                        locatif = ent
                        #print(locatif
                        liste_temporaire.append(locatif)
            if locatif in dic_interro:
                print("deja dans le dictionnaire") #problème le nom de l'artiste existe deja comment l'ajouter au dictionnaire ?
            else:
                dic_interro[artiste].append([titre, date, liste_temporaire])
                        
                    
        except:
            pass
print(dic_interro)
T = dic_interro.values()
for artiste, T in dic_interro.items():
    #print(artiste)
    #print(T)
    #nb_nom_paris = len([x for x in T if len x[2]==0])
    nb_total_chanson = len(T)
    print(nb_total_chanson)


# # Créer un graph des artistes parlant du + "x".
# x = un lieu de paris. 
# somme globale. = pour un lieu qui est l'auteur qui a le plus parlé?

# In[18]:


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


# In[20]:


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

Chercherlieux("Saint-Tropez")
Chercherlieux("Mini-moke")
Chercherlieux("Place de Clichy")


# In[ ]:


print(tograph)
for cle, valeur in tograph.items():
    g = tograph[cle]
    print(g)


# In[21]:


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
    
    plt.savefig('images/%s.png'%cle)
    plt.show()


# In[ ]:


#pour le pourcentage des lieux de paris.
#somme a l'interieur d'un auteur = exemple 80% des EN sont des lieux de paris.
#somme globale. = pour un lieu qui est l'auteur qui a le plus parlé?


# In[ ]:


#sur quelque texte faire une sortie ou chaque token du txt et l'étiquette donner par spacy 


# In[ ]:


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

# In[ ]:


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


# In[ ]:


#stat sur date, lieu le plus fréquent, 
#


# In[22]:


#voc_glaff = []
with open("freq_glaff_10000.json") as f:
    dic = json.load(f)
    print(len(dic))
    voc_glaff = set(dic.keys()) 
    print(len(voc_glaff))

mot = "météoriser"
if mot in voc_glaff:
    print(mot)


# # Erreur il ne fait la boucle que sur le 1er élement de la liste (à cause du remove)

# In[32]:


import re
import nltk
lignes_chanson = ["Je oui bonjour", 
                  "Fzefjkgnsd suis moi est mini", 
                  "Mini-moke et mini-jupe",
                  "Tout oui mal-honnete oui, bonjour"]
#expr = re.compile("(\w+\S\w+|\w+)")
#expr = re.compile("^(\w+'|\w+-\w+|\w+)")
#match = expr.finditer(mot)
for z in lignes_chanson:
    print(type(z))
    expr = re.compile("^(\w+'|\w+-\w+|\w+)")
    match = expr.finditer(z)
    for m in match:
        mot = m.group(0)
        print(""" "{}"  dans : "{}" """.format(mot, z))
        if mot.istitle():
            mot = mot.lower()
            if mot in voc_glaff:
                print("le mot est dans glaff")
                if mot in vrai_entite_nomme:
                    print("le mot est un nugget ")
                else:
                    print("je suis pas un nugget ")
                    liste_mots = Splittxt2(z)
                    liste_mots[0] = mot
                    nouvelle_ligne = " ".join(liste_mots)
                    #liste = ['Python', '5', 'py', '4', 'PHP', '8']
                    # affichage de la liste
                    #print("liste originale : " + str(liste))
                    #remplacement
                    #res = [elem.replace('4', '5') for elem in liste]
                    print(lignes_chanson, "\n")
                    res = [elem.replace(z,nouvelle_ligne) for elem in lignes_chanson]
                    lignes_chanson = res
                    #lignes_chanson.remove(z)
                    #lignes_chanson.append(res)
                    #print(res, "\n")
                    #lignes_chanson.append(nouvelle_ligne)
                    #lignes_chanson.pop(0)
                   
                    #lignes_chanson.remove(z)
                    #print(lignes_chanson, "\n")

            if mot not in voc_glaff:
                print("le mot est pas dans glaff")
                liste_mots = Splittxt2(z)
                liste_mots[0] = mot
                nouvelle_ligne = " ".join(liste_mots)
                #lignes_chanson.append(nouvelle_ligne)
                #lignes_chanson.pop(0)
                print(lignes_chanson, "\n")
                
                res = [elem.replace(z,nouvelle_ligne) for elem in lignes_chanson]
                lignes_chanson = res
                #lignes_chanson.remove(z)
                #lignes_chanson.append(res)
                #print(res, "\n")
                #lignes_chanson.remove(z)
                #print(lignes_chanson, "\n")
        #lignes_chanson.pop(0)
        
print(lignes_chanson)


# In[30]:


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
    
    
    
for z in lignes_chanson:
    expr = re.compile("^(\w+'|\w+-\w+|\w+)")
    match = expr.finditer(z)
    for m in match:
        mot = m.group(0)
        #print(""" "{}"  dans : "{}" """.format(mot, z))
        if mot.istitle():
            mot = mot.lower()
            if mot in voc_glaff:
                #print("le mot est dans glaff")
                if mot in vrai_entite_nomme:
                    print("le mot {} est un nugget ".format(mot))
                else:
                    #print("je suis pas un nugget ")
                    liste_mots = Splittxt2(z)
                    liste_mots[0] = mot
                    nouvelle_ligne = " ".join(liste_mots)

                    #print(lignes_chanson, "\n")
                    res = [elem.replace(z,nouvelle_ligne) for elem in lignes_chanson]
                    lignes_chanson = res


            else:
                #print("le mot est pas dans glaff")
                liste_mots = Splittxt2(z)
                liste_mots[0] = mot
                nouvelle_ligne = " ".join(liste_mots)
                #lignes_chanson.append(nouvelle_ligne)
                #lignes_chanson.pop(0)
                #print(lignes_chanson, "\n")
                
                res = [elem.replace(z,nouvelle_ligne) for elem in lignes_chanson]
                lignes_chanson = res
        
#print(lignes_chanson)


# In[25]:


print(lignes_chanson)


# In[ ]:





# In[ ]:


help(list)


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




