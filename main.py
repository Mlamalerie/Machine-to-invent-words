0# -*- coding: utf-8 -*-
import random,os
from Digramme import creerDigramme,creerMotAleaDigramme,beautyData
from Trigramme import creerTrigramme,creerMotAleaTrigramme

''' 
### PARAMETRES VARIABLE ################
'''


DOSSIERFILESTXT = "data"

def select_files(orig,i = 0,prof=0,select_dic = {}):
    espace = "  | "*prof
    listefichiers = os.listdir(orig)
    
    
    print( espace,f"### Select a file in '{orig}'")
    for fil in listefichiers:
        fil = orig + "/" + fil
        if os.path.isdir(fil):
            
            i,nada = select_files(fil,i,prof+1,select_dic)
            
           
        else:
            print( espace,f'[{i}] :',fil)
            select_dic[i] = fil
            i+=1
          
    if prof == 0: #tout s'est rempiler
          
        choix = int(input(' >'))
       
        lefichier = select_dic[choix]
        
        return (i,lefichier)
    else:
        
        return (i,None)



alphabet = "abcdefghijklmnopqrstuvwxyzàâéèêëîïôùûüÿæœç"





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
        mot = mot.lower()
        if len(mot) > 1 and len(mot.split(' ')) == 1:
            mot = enlever_accent(mot)
           
            for c in mot:
                if c not in alphabet:
                    #ìprint(c,alphabet6)
                    suppr.append(mot)   
                    ok = False
                    
        else:
            suppr.append(mot)  
            ok = False
            
        if ok:
           
            
            res.append(mot)
    
    res.sort()
    return (suppr,res)

''' ##SEPAR2 MOT PAR SYLLABES
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
kelbaysuppr,listes2mot = cleanDic(listes2mot)
listes2mot = ["mlamali","raoufi","yohan","roukia","noah","morgan"]
lsyllabes = liste2syllabes(listes2mot)
lsyllabes.sort()
print(len(lsyllabes))
lsyllabes = list(dict.fromkeys(lsyllabes))
print(len(lsyllabes))
print(lsyllabes)


if len(kelbaysuppr) > 0:
    print("len suppr :",len(kelbaysuppr))
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

def printresultat(cheminFichier,cb,taille,trig_ok = True):
    liste_mots = get_words_dic(cheminFichier)
    suppr, liste_mots = cleanDic(liste_mots) #clean the list
    print(" * Number of words deleted from {} : {}".format(cheminFichier,len(suppr)))
    print(" * Number of words which to based :",len(liste_mots))
    
    moyennetaille = 0
    for m in liste_mots:
        moyennetaille += len(m)/len(liste_mots)
    print(" * Average words length :", round(moyennetaille,1) ) 
    print("   --- ") 
    
    if not trig_ok:
        data = creerDigramme(liste_mots)
    else:
        data = creerTrigramme(liste_mots)
    #print(beautyData(dataDI)) # afficher le tableau de probabilité
    
    nomEmplacementSauvegarde = "results"
    if not os.path.exists(nomEmplacementSauvegarde):
    	os.makedirs(nomEmplacementSauvegarde)
    
    nom = cheminFichier.split("/")[-1][:-4]
    chemin = nomEmplacementSauvegarde
    
    
    if not trig_ok:
        chemin += "/result_DI_"
    else:
        chemin += "/result_TRI_"
    chemin += cheminFichier.split("/")[-2] +"-"+nom
    chemin += "_"+str(taille)
    chemin += "_"+str(cb) 
    chemin += ".txt"
    
    loo = []
    with open(chemin,"w") as fic: #creer fichier txt
        for k in range(cb): #creer k nouveaux mots
            if not trig_ok:
                new = creerMotAleaDigramme(taille-1,data)
            else:
                new = creerMotAleaTrigramme(liste_mots,taille-1,data)
            
            loo.append(new)
            
        loo = list(dict.fromkeys(loo)) #delete duplicate
        loo.sort() 
        fic.write("\n".join(loo)) 
        
    print(" * The generated words are saved :",chemin,"!")
    print(f" * {round(realword(loo,liste_mots)*100,2)} % of the words already exist in {nom} file")


def genererPhrases_DI(cb):
    liste_mots = get_words_dic("data/fr/" + listefichiers[5])
    suppr, liste_mots = cleanDic(liste_mots)
    dataVerbe =  creerDigramme(liste_mots) 
    print("wait...")
    liste_mots = get_words_dic("data/fr/" + listefichiers[3])
    suppr, liste_mots = cleanDic(liste_mots)
    dataNom =  creerDigramme(liste_mots) 
    print("wait..")
    liste_mots = get_words_dic("data/fr/" + listefichiers[2])
    suppr, liste_mots = cleanDic(liste_mots)
    dataArticle = creerDigramme(liste_mots) 
    print("wait. \n")
    liste_mots = get_words_dic("data/fr/" + listefichiers[1])
    suppr, liste_mots = cleanDic(liste_mots)
    dataAdjectif =  creerDigramme(liste_mots) 
    print(" ~  VERBE + ARTICLE + NOM + ADJECTIF")
    for k in range(cb):
        article = creerMotAleadigramme(3,dataArticle)
        nom = creerMotAleadigramme(10,dataNom)
        while len(nom) < 3:
            nom = creerMotAleadigramme(10,dataNom)
        verbe = creerMotAleadigramme(12,dataVerbe)
        while len(verbe) < 3:
            verbe = creerMotAleadigramme(12,dataVerbe)
        adjectif = creerMotAleadigramme(12,dataAdjectif)
        while len(adjectif) < 2:
            adjectif = creerMotAleadigramme(12,dataAdjectif)
        
        if article[-1] == 's':
            if nom[-1] != "s":
                nom += "s"
            if adjectif[-1] != "s":
                 adjectif += "s"
           
        print(k,"-",verbe,article,nom,adjectif)

def genererPhrases_TRI(cb):
    pass

def genererMots(trig_ok):
    global DOSSIERFILESTXT
    cheminFichierDico = select_files(DOSSIERFILESTXT)[1]
    nb = int(input('#### how many new words to create > '))
    taillemax = int(input('#### max word length > '))
    
    if not trig_ok:
        printresultat(cheminFichierDico,nb,taillemax,False)
    else:
        printresultat(cheminFichierDico,nb,taillemax,True)

    
def Menu_DI():
    print("######### * DIGRAM METHOD *")
    print("######### (0 : Words)")
    print("######### (1 : Sentences)")
    c = int(input(" > "))
    if c == 1:
        cb = int(input(" * how many new sentences to create > "))
        print("wait....")
        genererPhrases_DI(cb)
    else:
        genererMots(False)
    

def Menu_TRI():
    print("######### * TRIGRAM METHOD *")
    print("######### (0 : Words)")
    print("######### (1 : Sentences)")
    #c = int(input(" > "))
    c = 0
    if c == 1:
        cb = int(input(" * how many new sentences to create > "))
        print("wait....")
        #genererPhrases_TRI(cb)
    else:
        genererMots(True)
    
    

def MENU_MAIN():
    print("################## * CHOOSE YOUR METHOD *")
    print("################## (0 : DIGRAMME)")
    print("################## (1 : TRIGRAMME)")
    c = int(input(" > "))
    
    if c == 1:
        Menu_TRI()
    else:
        Menu_DI()
      
    c = int(input("\n (0 : CONTINUE)   (1 : QUIT) > "))
    if c == 0:
        MENU_MAIN()
        
        
MENU_MAIN()




