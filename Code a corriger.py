#!/usr/bin/env python
# coding: utf-8

# In[1]:


#ouverture et lecture des json
import nltk
import spacy
import json
import os
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


# In[42]:


import json
import tqdm
corpus = ouvrir_json("tmp.json")


dic_longueur_chanson = {}

for nom_artiste, donnee in tqdm.tqdm(corpus.items()):
    #dic_longueur_chanson = {nom_artiste:{}}
    dic_longueur_chanson.setdefault(nom_artiste, {})
    for element in donnee:
        #chansons = []
        try:
            #txt = str(parole)
            parole = element["lyrics"]
            txt = Splittxt3(parole)
            longueur = len(txt)
            
            #nbre_de_texte_traitable += 1
        except:
            longueur = 0
        titre = element["full_title"]
        #print(nom_artiste, titre, len(txt))
        dic_longueur_chanson[nom_artiste].setdefault(titre, [])
        dic_longueur_chanson[nom_artiste][titre].append(longueur)

with open("Data/Dictionnaire_longueur_chansons.json", "w") as w: 
        w.write(json.dumps(dic_longueur_chanson, indent=2))



# In[77]:


longueur_for_graph = {}
for nom_artiste, dic in dic_longueur_chanson.items():
    longueur_for_graph[nom_artiste] = {}
    for titre, longueur_titre in sorted(dic.items(), key=lambda x: x[1], reverse=False):
        longueur_for_graph[nom_artiste][titre] = longueur_titre


# In[85]:


import matplotlib.pyplot as pyplot
#print(dic_longueur_chanson.keys())
for nom_artiste, dic in dic_longueur_chanson.items():
    if nom_artiste == "_113":
        liste_vide = []
        
        #for titre, longueur_chanson in dic.items():
            liste_vide.append(dic[1][i])
            
            #for chiffre in longueur_chanson:
                #liste_vide.append(chiffre)
        fig, ax1 = pyplot.subplots()
        ax1.set_ylabel("Nombre de mots")
        ax1.plot(liste_vide, 'b-')

        ax1.set_xlabel('longueur des titres de %s'%nom_artiste, color='b')


        fig.tight_layout()
        pyplot.savefig("Data/image memoire/%s.png"%nom_artiste)
        pyplot.show()


# In[ ]:



       


# In[ ]:


artiste = []
toutes_les_chansons = []
tous_les_mots = []
nbre_de_texte_traitable = 0
nbre_de_texte_non_traitable = 0
nbre_de_mot_totale = 0
nbre_de_mot_par_chanson = []
nbre_mot_totale = []
moyenne_toto = []
for i in moyenne_toto:
    moyenne_totale = sum(i)/len(moyenne_toto)
    print(chanteur, moyenne_totale)
chansons.append(parole)
            toutes_les_chansons.append(chansons)
            mots = Splittxt3(parole)
            #print(mots)
            nbre_mot_totale.append(mots)
            moyenne_mot = sum(len(mots))/len(nbre_mot_toto)
            moyenne_toto.append(moyenne_mot)
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
#print(nbre_de_texte_non_traitable)
#print(nbre_de_texte_traitable)
#print(tous_les_mots)
for liste_mots in tqdm.tqdm(tous_les_mots):
    nbre_de_mot_par_chanson.append(len(liste_mots))
    nbre_de_mot_par_chanson.append(0)
    for mot in liste_mots:
        nbre_de_mot_totale += 1
#print(nbre_de_mot_par_chanson)
#print(nbre_de_mot_totale)


# In[3]:


import os
if os.path.exists("Data/Dictionnaire_interro_lieux_paris_large.json"):
    with open("Data/Dictionnaire_interro_lieux_paris_large.json", encoding="UTF-8") as f:
        dic_interro_des_lieux = json.load(f)


# In[ ]:


#dic_for_map = {}
#dic_for_map = {"ID":  ,}
to_map = []
longueur = 0
import tqdm
from geopy.geocoders import Nominatim
for lieu, valeur in tqdm.tqdm(dic_interro_des_lieux.items()):
    date_titre = []
    for artiste, liste in valeur.items():
        
        date = liste[0][1] #date
        titre = liste[0][0] #titre
        date_titre.append(date)
        date_titre.append(date)
        if date is not None:
            paris = ",Iles-de-France"
            geolocator = Nominatim(user_agent="Tiago")
            try:
                location = geolocator.geocode("{}, {}".format(lieu, paris), timeout=20 )
                adresse = location.address
                to_map.append([date, titre, lieu, adresse, location.latitude, location.longitude])
                #print(to_map)
            except:
                pass
print(to_map)

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


1/0
            


# In[ ]:





# In[ ]:





# In[ ]:




