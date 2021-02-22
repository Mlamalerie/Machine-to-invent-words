# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd

alphabet = "abcdefghijklmnopqrstuvwxyzàâéèêëîïôùûüÿæœç"
''' 
### CREATION DU TABLEAU DE PROBABILITE digramme ################
'''
#~~ fonction pour embellir l'affichage du data digramme
def beautyData(data):
    cols_vides = [col for col in data.columns if data[col].sum() == 0.0]
    ligs_vides = [lig for lig in data.index.values.tolist() if data.loc[lig].sum() == 0.0]
    # supprimer les colonnes et lignes vides
    data = data.drop(cols_vides, axis=1) 
    data = data.drop(ligs_vides, axis=0)  
    return data
    

#~~ mise a jour du tableau de probabilité pour 1 mot
def majDataAvec1Mot(mot,data):
    mot = mot.lower()
    
    debutl = mot[0] #première lettre du mot
    finl = mot[-1] #dernière lettre du mot
    
    data[str(debutl)]["deb"] += 1
    data["fin"][str(finl)] += 1
    
    for i in range(len(mot)-1):
        data.loc[str(mot[i])][str(mot[i+1])] += 1
        
    
        
    
#~~ mise a jour du tableau de probabilité pour tout un dictionnaire
def majDataALLWORDS(dico,data):
    for mot in dico:
        try:
            majDataAvec1Mot(mot,data)
        except:
            print(mot,"error majDataAvec1mot !")

#~~ fct pour normaliser le tableau de proba
def majDataNormaliser(data):
    indexs = data.index.values.tolist()
    for lig in indexs:
        somme = data.loc[lig].sum()
        
        if somme != 0:
            data.loc[lig]/= somme

#~~ creer le tableau de probabilité a partir d'une liste de mots
def creerDigramme(dic):
    global alphabet
    listelettres = list(alphabet) #creer une liste de lettre à partir de l'alphabet
    tab = np.zeros((len(alphabet)+1,len(alphabet)+1)) # tableau numpy vide
    
    #creation du dataFrame à 2 dimension
    data = pd.DataFrame(tab, index = (["deb"] + listelettres), columns = (listelettres + ["fin"])) 
    
    
    majDataALLWORDS(dic,data) # mettre a jour le nombre d'occurence de chaque mot du dictionnaire
    majDataNormaliser(data) # normaliser le tout
    return data

''' 
### CREATION DE MOT ALEATOIRE EN FCT DU DIGRAMME ################
'''
#~~ sortirLettreAlea() qui retourne une lettre aléatoire, en fonction de la lettre de depart mis en parametre
def sortirLettreAlea(lettrePos,digramme):
    
    listesdechoixsuivant = digramme.columns.tolist()
    
    listedeproba = digramme.loc[str(lettrePos)].tolist()
    lettre = np.random.choice(listesdechoixsuivant, p=listedeproba)
    return lettre

#~~ creerMotAleadigramme() qui retourne un mot aléatoire
def creerMotAleaDigramme(taille,digramme):

    res = [sortirLettreAlea('deb',digramme)]
    
    while res[-1] != "fin" and len(res[:-1])<= taille:
        try:
            l = sortirLettreAlea(res[-1],digramme)
        except:
            print("error sortirLettreAlea ..",res)
        else:
            res.append(l)
        #print(res)
    res = res[0:-1]
    return "".join(res)



    

