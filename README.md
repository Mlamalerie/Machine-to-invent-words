# Word inventing machine

We built a program using python able to invent words or simple sentences. (::fr::) <br>
Il existe plusieurs façons de générer aléatoirement des mots. Nous avons utilisé les méthodes d'enchainements digrammes et trigrammes.
Notre programme à besoin d'un dictionnaire de mots pour en créer de nouveau. Pour ce projet nous nous sommes donc procurer sur internet un ensemble de fichier contenant un assez grand nombre de mots français ('adjectifs.txt,"nomPropres.txt', ect.)

### ⚙ How to run it
- Choisir la méthode de création voulu (digramme or trigramme)
- Selectionner le fichier/dictionnaire source sur lequel se baser pour créer nos mots
- Saisir le nombres de nouveaux mots que vous voulez créer
- Saisir la taille maximum que doivent faire ces mots

Vos nouveaux mots seront stockées dans un fichiers txt rangée dans le dossiers /results

### The methods used to create the words 

#### Enchainement de digrammes
Afin de générer des mots plus plausibles, à la lecture, nous orientons le choix de chaque lettre selon des règles probabilistes d’enchaînement de deux lettres. La génération de mot par digrammes est plus complexe que la précédente. Pour pouvoir générer des mots à partir de digrammes, il faut dans un premier temps disposer d’un dictionnaire. Puis pour chaque mot de ce dictionnaire, pour chaque lettre, regarder quelle est la lettre suivante, et mettre à jour la table de probabilité. Il peut être utile de mémoriser quelles lettres commencent un mot, et lesquelles terminent un mot. 
Par exemple, avec le mot informatique, on extrait la table de probabilités suivante :
<img src="screens/tableauinfo.png" width="350" alt="Table de probabilités du mot 'informatique'">
Une fois la table complète de probabilités calculée, il suffit de partir d’une lettre, et d’enchaîner les lettres en fonction de la table de probabilité. En suivant la table 1, et en partant de la lettre t, on génère le mot tique. Bien évidemment, cela n’a aucun sens de faire une table de probabilités sur un seul mot. Plus on prend de mots en compte, plus la table de probabilités reflète correctement l’enchaînement des lettres dans la langue.

#### Enchaînement de trigrammes
La méthode des trigrammes suit la même procédure que la méthode des digrammes, mais au lieu de ne considérer qu’une seule lettre pour regarder la suivante, on considère les deux précédentes. Cela crée une table de probabilités plus conséquente, mais beaucoup plus fine pour la création de mot.

### 📸 Screenshots 

<img src="img/1.PNG" width="250" alt="menu select file">
<img src="img/2.png" width="300" alt="result example">
<img src="img/3.png" width="300" alt="result example">
---
### 📌 Comments

parlé de %
de Webscrapping de commnet j'ai pris les données des commores et pk

Pour rappel, la langue française est composée de 42 lettres, les 26 lettres de l’alphabet latin : 13 voyelles accentuées, le graphème ç, ainsi que les deux ligatures (æ, œ), et aussi le symbole

### 👨🏾‍💻👨🏼‍💻 Auteurs
[Mlamali SAID SALIMO](https://www.linkedin.com/in/mlamalisaidsalimo) and [Josh Bonacorsi](https://www.linkedin.com/in/joshuabonacorsi). <br/>
