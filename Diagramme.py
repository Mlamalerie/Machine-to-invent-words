# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd

alphabet1 = "abcdefghijklmnopqrstuvwxyzàâéèêëîïôùûüÿæœç-"
alphabet2 = "abcdefghijklmnopqrstuvwxyzàâéèêëîïôùûüÿæœç-'"

alphabet = alphabet2


# fonction pour embellir le data
def beautyData(data):
    cols_vides = [col for col in data.columns if data[col].sum() == 0.0]
    ligs_vides = [lig for lig in data.index.values.tolist() if data.loc[lig].sum() == 0.0]
    # supprimer les colonnes et lignes vides
    data = data.drop(cols_vides, axis=1) 
    data = data.drop(ligs_vides, axis=0)  
    return data
    

# mise a jour du tableau pour 1 mot
def majDataAvec1Mot(mot,data):
    mot = mot.lower()
    
    debutl = mot[0] #première lettre du mot
    finl = mot[-1] #dernière lettre du mot
    
    data[str(debutl)]["deb"] += 1
    data["fin"][str(finl)] += 1
    #occurrence = {str(c) : mot.count(c) for c in mot}
    
    for i in range(len(mot)-1):
        data.loc[str(mot[i])][str(mot[i+1])] += 1
        
    

def majDataALLWORDS(dico,data):
    for mot in dico:
        majDataAvec1Mot(mot,data)

def majDataNormaliser(data):
    indexs = data.index.values.tolist()
    for lig in indexs:
        somme = data.loc[lig].sum()
        
        if somme != 0:
            data.loc[lig]/= somme
        
def creerDigramme(dic):
    global alphabet
    listelettres = list(alphabet)
    tab = np.zeros((len(alphabet)+1,len(alphabet)+1))
    data = pd.DataFrame(tab, index = (["deb"] + listelettres), columns = (listelettres + ["fin"]))
    
    majDataALLWORDS(dic,data)
    majDataNormaliser(data)
    return data

''' 
### RANDOM ################
'''

def sortirLettreAlea(lettrePos,diagramme):
    
    listesdechoixsuivant = diagramme.columns.tolist()
    
    listedeproba = diagramme.loc[str(lettrePos)].tolist()
    lettre = np.random.choice(listesdechoixsuivant, p=listedeproba)
    return lettre

def creerMotAleaDiagramme(taille,diagramme):
    res = [sortirLettreAlea('deb',diagramme)]
    
    while res[-1] != "fin" and len(res[:-1])<= taille:
        l = sortirLettreAlea(res[-1],diagramme)
        res.append(l)
        #print(res)
    res = res[0:-1]
    return "".join(res)

def printresultat(cb,nom):
    global data
    chemin = "resultat_"
    chemin += nom
    chemin += ".txt"
    
    loo = []
    with open(chemin,"w") as fic:
        for k in range(cb):
            new = creerMotAleaDiagramme(5,data)
            loo.append(new)
        loo = list(dict.fromkeys(loo))
        loo.sort()
        fic.write("\n".join(loo))
    print(loo[0:10])

def afficher_resultat_ALL_DATA(dossier):
    dossier += "/fr"
