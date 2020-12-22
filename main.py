# -*- coding: utf-8 -*-
import random
import numpy as np
import pandas as pd



alphabet1 = "abcdefghijklmnopqrstuvwxyzàâéèêëîïôùûüÿæœç-"
alphabet2 = "abcdefghijklmnopqrstuvwxyzàâéèêëîïôùûüÿæœç-'"

alphabet = alphabet2

mot = "anticonstitutionnelle"

    


def enlever_accent(mot):
    tablo = { 'éèêẽ' : 'e'
            , 'àâãä'  : 'a'
            , 'ü'    : 'u'
            , 'ö'    : 'o'
            , 'î' : 'i'
            }
    
    mot_sans_accents = ''
    for i in mot:
        for k in tablo:
            if i in k: i = tablo[k]; break
        mot_sans_accents += i
    return mot_sans_accents


''' 
### CREER MOT ALEATOIRE ################
'''

def creeMotAleatoire(taille):
    global alphabet
    res = ""
    for i in range(taille):
        res += random.choice(alphabet)
    return res

''' 
### RECUPERATION MOTS DICTIONNAIRE ################
'''
def get_words_dic(chemin):
    with open(chemin,"r", encoding='utf-8') as fic:
        text = fic.read()
        return(text.split("\n"))
        

def cleanDic(dic):
    suppr = []
    global alphabet
    dic.sort()
    i = 0
    for mot in dic:
        
        if len(mot) > 1:
            dic[i] = enlever_accent(mot)
            for c in mot:
                if c not in alphabet:
                    #print(mot,"##################################")
                    if mot in dic:
                        dic.remove(mot)
                        suppr.append(mot)
        else:
            dic.pop(dic.index(mot))
        i += 1
    return suppr


def syllabe(mot):
    lis = [mot[0]]
    voyelle = "aeiouy"
    
    
 
    for i in range(1,len(mot)):
        if mot[i] in voyelle:
            lis[-1]+= mot[i]
            #print(mot[i])
        else:
            lis.append(mot[i])

    i = 0
    n = len(lis)
    
    while i < n:
        #print(i,lis[i],lis)
        itera = 1
        if len(lis[i])==1:
            if i != 0:
                #print("-",lis[i-1],lis[i+1])
                
                if i < n-1:
                    x = lis[i+1]
                    if len(x) == 1 and x not in voyelle:
                        #print("#")
                        #i -= 1
                        itera = -1
                    
                #print(x)
                lis[i-1] += lis[i]
                lis.pop(i)
                n -= 1
        #print("*",lis[i-1],lis)
        if len(lis[i-1]) >= 3 and 'y' in lis[i-1]:
             #print(lis[i-2])
             bay  = lis[i-1]
             p = 0
             while bay[p] != 'y':
                 p += 1
             #print("#",p,bay)
             lis[i-1] = bay[0:p]
             lis.insert(i,bay[p:])
             i+=1
        i+=itera
             
        
        
    return lis
            


def liste2syllabes(listemots):
    listesy = [syllabe(m) for m in listemots]
    return [sy for mot in listesy for sy in mot]

    
cheminFichier = "data/fr/nomPropre.txt"
listes2mot = get_words_dic(cheminFichier)
kelbaysuppr = cleanDic(listes2mot)

lsyllabes = liste2syllabes(listes2mot)
lsyllabes.sort()
print(len(lsyllabes))
lsyllabes = list(dict.fromkeys(lsyllabes))
print(len(lsyllabes))
print(lsyllabes)


if len(kelbaysuppr) > 0:
    print(kelbaysuppr)

''' 
### CREATION D'UN DIGRAMME ################
'''

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
data = creerDigramme(listes2mot)
print(listes2mot[0:5])
print(beautyData(data))
'''
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

def realword(result,dic): #affiche pourcentage de mot qui existe déjà
    return 1
#printresultat(1000,cheminFichier.split("/")[-1][:-4])


def afficher_resultat_ALL_DATA(dossier):
    dossier += "/fr"
