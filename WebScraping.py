# -*- coding: utf-8 -*-
"""
Web Scraping Zone
Created on Feb 2021

Github: https://www.github.com/Mlamalerie

"""

import requests
import os
from bs4 import BeautifulSoup



url2 = "https://comcom-style.skyrock.com/97100248-Les-prenoms-comoriens.html"
url = "http://olivierdelgado.free.fr/0livier/prenoms%20Feminins%20comoriens.htm"



def recup_words_on(url):
    response = requests.get(url)
    if response.ok:
        res = []
        soup = BeautifulSoup(response.text,'lxml')
        #print(response.text)
        trs = soup.findAll('tr')
        trs = [tr for tr in trs if tr['style'] == 'height:18.75pt']
        
        #print(trs)
        #print(len(trs))
        
        for tr in trs:
            tds = tr.findAll('td')
            #print(tds)
            tds = [td for td in tds if len(td.text) > 0]
            for td in tds:
                #print(td['class'],(td.text))
                mot = td.text.split(':')[0].strip()
                if len(mot.split(',')) > 1:
                    for m in mot.split(','):
                        res.append(m.strip())   
                else:
                    res.append(mot)
        res = [mot.lower().split(" ")[0] for mot in res ]
        return res
    
words = recup_words_on(url) 

def save(liste_mots,namefile):    
    nomEmplacementSauvegarde = "data"
    if not os.path.exists(nomEmplacementSauvegarde):
    	os.makedirs(nomEmplacementSauvegarde)
    nomEmplacementSauvegarde += "/km"
    if not os.path.exists(nomEmplacementSauvegarde):
    	os.makedirs(nomEmplacementSauvegarde)
    nomEmplacementSauvegarde += '/' + namefile
    
    with open(nomEmplacementSauvegarde,"w",encoding="utf8") as fic: #creer fichier txt   
        liste_mots = list(dict.fromkeys(liste_mots)) #delete duplicate
        liste_mots.sort() 
        fic.write("\n".join(liste_mots)) 
        
    print(" * saved :",nomEmplacementSauvegarde,"!")
        
print(len(words)) 
save(words,"prenomFille.txt")  
    
   
