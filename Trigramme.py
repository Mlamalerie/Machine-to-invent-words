# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import random
from Digramme import majDataNormaliser

alphabet = "abcdefghijklmnopqrstuvwxyzàâéèêëîïôùûüÿæœç"


"""
Cette fonction permet à partir d'une liste de caractères comme ["a","b",c"] de donner une nouvelle liste 
["aa","ab","ac","ba","bb","bc","ca","cb","cc"] avec tous les couples possibles
"""

def couple(liste) : # permet de créer une liste de couple de caractères de l'alphabet du genre aa ; ab ; ac...
    res = []
    for lettre in liste :
        for x in liste :
            res.append(lettre+x)
    return res

def recupereCouple(mot): #permet de convertir "Salut" en "sa ; al ; lu ; ut" ( on le casse en couple de lettres )
    mot = mot.lower()
    return [''.join(pair) for pair in zip(mot[:-1], mot[1:])]

def stockCouples(dico) :
    res = []
    for mot in dico :
        try:
            res.extend(recupereCouple(mot)) #ajouté
        except:
            print(mot,recupereCouple(mot))
    return res


#La fonction motTrigramme permet de remplir un dataframe à partir d'un mot donné ( sans normalisation )
def motTrigramme(mot,dataframe):
    mot = mot.lower() 
    lmot = recupereCouple(mot) # on convertit le mot en une liste de couples de lettres
    lmot = list(set(lmot)) # permet de supprimer les doublons de la liste 
    dataframe['fin'][lmot[-1]]+=1
    for i in lmot :
        for j in range(len(mot)-2) :
            if i==(mot[j]+mot[j+1]):
                dataframe[mot[j+2]][i] += 1
                
def creerTrigramme(dic): # permet de créer le tableau trigramme à partir d'un dictionnaire
    global alphabet
    nom_lignes = couple(alphabet)
    lettres = list(alphabet)
    tableau = np.zeros((len(alphabet)*len(alphabet),len(alphabet)+1))
    dataframe = pd.DataFrame(tableau, index = (nom_lignes), columns = (lettres + ["fin"]))
    for mot in dic :
        motTrigramme(mot,dataframe)
    majDataNormaliser(dataframe)
    return(dataframe) # on retourne le digramme fini

#Cette fonction permet en fonction de notre couple de lettres ( qui peut être ab, bc, ca ect...), de générer la lettre suivante à partir des probabilités contenu dans le trigramme.
def sortirLettreAlea2(couple_actuel,trigramme): 
    listes_des_choix_suivants = trigramme.columns.tolist() # on liste toutes les lettres qui peuvent suivre comme a,b,.. et fin
    liste_des_proba = trigramme.loc[str(couple_actuel)].tolist() # on liste les proba liees a chaque choix
    lettre_suivante = np.random.choice(listes_des_choix_suivants, p=liste_des_proba) # on pioche une lettre selon les proba
    return(lettre_suivante)

"""
Cette fonction est la fonction final, elle permet de générer un mot suivant la méthode des Trigrammes ! 
Par convention on prendra les deux premières lettres parmi les couples rencontrés dans le dictionnaire
"""

def creerMotAleaTrigramme(listemots,taillemax,trigramme):
   
    i = random.randint(0, len(listemots)-1) # on genere les deux premieres lettres en prenant aleatoirement un couple stocké
    res = []
    res.append(listemots[i][0]) # on stocke la premiere lettre
    res.append(listemots[i][1]) # on stocke la deuxieme lettre
    while res[-1] != "fin" and len(res[:-1])<= taillemax:
        if trigramme.loc[res[-2]+res[-1]].sum()!=1 : # si on a jamais rencontré le couple généré par le digramme 
            l="fin"
        else :
            l = sortirLettreAlea2(res[-2]+res[-1],trigramme)
        res.append(l)
    res = res[0:-1]
    return "".join(res)
