#!/usr/bin/env python
# coding: utf-8

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

# In[3]:


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


# # création d'une liste des lieux de paris

# In[4]:



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


# # Récupération du glaff

# In[24]:


#voc_glaff = []
with open("freq_glaff_10000.json") as f:
    dic = json.load(f)
    print(len(dic))
    voc_glaff = set(dic.keys()) 
    print(len(voc_glaff))

#mot = "XXXXeeeew"
mot = "Créteil"
#mot = "Maxi"
#mot = "Paris"
if mot.lower() in voc_glaff:
    print("dans glaff, on modifie")
    if mot in vrai_entite_nomme:
        print(mot, "FP")
    else:
        print(mot, "VP")
else:
    print("pas glaff, on modifie pas")
    if mot not in vrai_entite_nomme:
        print(mot, "FN")
    else:
        print(mot, "VN")


# In[ ]:





# # Execution du code sur une liste avant de l'executer sur le corpus

# In[14]:


import re
import nltk
#création d'une liste de ligne pour simuler la poésie.
lignes_chanson = ["Je oui bonjour", 
                  "Fzefjkgnsd suis moi est mini", 
                  "Mini-moke et mini-jupe", #"Mini-moke" ne sera pas mis en minuscule comme les autres lignes
                  "Tout oui mal-honnete oui, bonjour",
                  "Paris et sa fonctionne pas",
                  "Créteil et sa fonctionne pas"
                  "Maxistère"]

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
        print(""" "{}"  dans : "{}" """.format(mot, z)) #affiche le mot dans quel ligne il se trouve.
        toto = False
        if mot[0] != mot[0].lower():
            toto = True
        #if mot.istitle(): #si le mot possède une majuscule je le met sans maj. minimoke not istitle()
        if toto == True:
            mot_lower = mot.lower()
            print(mot)
#------------------------------------------------------------------------------------------------------------
            if mot_lower in voc_glaff:                 #s'il est dans le glaff et qu'il correspond 
                print("le mot est dans glaff")   #a un lieu de ma liste des lieux
                if mot in vrai_entite_nomme:     #SINON je l'affiche .
                    print("le mot est un nugget\n ")
                else:
                    print("je suis pas un nugget\n ")
                    liste_mots = Splittxt2(z)      #permet de découper ma ligne en liste de mot.
                    liste_mots[0] = mot_lower            #le mot en début de ligne je le remplace par mot.
                    nouvelle_ligne = " ".join(liste_mots)  #je reassemble ma ligne.
                    print(lignes_chanson, "\n")
                    res = [elem.replace(z,nouvelle_ligne) for elem in lignes_chanson]  #je remplace 
                    lignes_chanson = res               #l'ancienne ligne par une nouvelle ligne.  #VP                          
#------------------------------------------------------------------------------------------------------------

            if mot_lower not in voc_glaff:            #s'il est pas dans le glaff je fait le même procédé ↑.
                print("le mot est pas dans glaff \n ")#ne pas mettre en minuscule. #FN
                #match = [i for i in vrai_entite_nomme]
                #print(match)
                if mot in vrai_entite_nomme:
                    ("je suis un lieu de paris \n ")
                else:
                    ("pas dans lieu de paris")
                #liste_mots = Splittxt2(z)
                #liste_mots[0] = mot
                #nouvelle_ligne = " ".join(liste_mots)
                #print(lignes_chanson, "\n")
                #res = [elem.replace(z,nouvelle_ligne) for elem in lignes_chanson]
                #lignes_chanson = res

        
print(lignes_chanson)


# In[10]:





# # On observe que le traitement fonctionne partout sauf pour Mini-moke

# ## test pour github

# # test 2
