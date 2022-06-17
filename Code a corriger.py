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


# In[ ]:





# In[77]:





# In[ ]:





# In[ ]:



       


# In[ ]:





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



            


# In[ ]:





# In[ ]:





# In[ ]:




