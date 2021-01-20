# -*- coding: utf-8 -*-
import random,os
from Diagramme import creerDigramme,creerMotAleaDiagramme,beautyData

''' 
### PARAMETRES VARIABLE ################
'''


i = 0
listefichiers = os.listdir("data/fr")

print("#### Select a file")
for txt in listefichiers:
    print(f' ({i})',txt)
    i+=1
choix = int(input(' >'))
cheminFichier = "data/fr/" + listefichiers[choix]

print("#### Select nb new words")
nb = int(input(' >'))
print("#### Select len max each words")
taillemax = int(input(' >'))
alphabet = "abcdefghijklmnopqrstuvwxyzàâéèêëîïôùûüÿæœç"


mot = "anticonstitutionnelle"


def enlever_accent(mot):
    tablo = { 'èêẽ' : 'e'
            , 'àâãä'  : 'a'
            , 'üù'    : 'u'
            , 'ö'    : 'o'
            , 'îï' : 'i'
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
    res = []
    global alphabet
    

    for mot in dic:
        ok = True
        
        if len(mot) > 1 and len(mot.split(' ')) == 1:
            mot = enlever_accent(mot)
            
            for c in mot:
                if c not in alphabet:
                    suppr.append(mot)   
                    ok = False
                    
        else:
            suppr.append(mot)  
            ok = False
            
        if ok:
           
            
            res.append(mot)
    
    res.sort()
    return (suppr,res)


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

'''   
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

''' 
### CREATION DU DIGRAMME ################
'''
def realword(result,dic): #affiche pourcentage de mot qui existe déjà
    cpt = 0
    for mot in result:
        if mot in dic:
            cpt += 1
    
    return cpt/len(result)

def printresultat(cheminFichier,cb,taille):
    liste_mots = get_words_dic(cheminFichier)
    suppr, liste_mots = cleanDic(liste_mots) #clean the list
    print(" * Word deleted :",len(suppr))
    print(" * Size liste de mots :",len(liste_mots))
    
    dataDI = creerDigramme(liste_mots)
    #print(beautyData(dataDI)) # afficher le tableau de probabilité
    
    nomEmplacementSauvegarde = "result"
    if not os.path.exists(nomEmplacementSauvegarde):
    	os.makedirs(nomEmplacementSauvegarde)
    
    nom = cheminFichier.split("/")[-1][:-4]
    chemin = nomEmplacementSauvegarde
    
    chemin += "/result_"
    chemin += nom
    chemin += "_"+str(taille)
    chemin += "_"+str(cb) 
    chemin += ".txt"
    
    loo = []
    with open(chemin,"w") as fic: #creer fichier txt
        for k in range(cb): #creer k nouveaux mots
            new = creerMotAleaDiagramme(taille-1,dataDI)
            loo.append(new)
            
        loo = list(dict.fromkeys(loo))
        loo.sort() 
        fic.write("\n".join(loo)) 
        
    print(" * :",chemin)
    print(f" * % word also existing in {nom} :", realword(loo,liste_mots)*100)



printresultat(cheminFichier,nb,taillemax)


