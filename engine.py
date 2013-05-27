#! /usr/bin/python
#-*-coding: utf-8 -*-
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import os,sys
from dictionnaire import Dico
print("Construction de la matrice... ")
 
# engine.py
# Crée par Fabien Borel, Hugo Valery et Nicolas Rieul dans le cadre de leur projet ISN 2013
# Cette version non compilée requière évidemment python et son module pyQt
# Ceci est le code principale, mais pour lancer le programme il faut exécuter main.py
# Nécessite aussi dictionnaire.py

# L'arborescence contient des matrices de mots, organisés par noeuds : un pour chaque lettre. Chaque noeud est suivit par une ou plusieurs lettres susceptibles de fournir un mot et ainsi de suite
class Arborescence:
    def __init__(self): # structure d'un noeud (et, indeed, de toute l'arborescence, c'est un peu comme du fractal (sisi))
        self.word = None
        self.children = {}

    def insert(self, word): # pour compléter l'arborescence on injecte les mots un par un (voir la boucle for plus bas)
        node = self # node prend les attributs de l'arborescence (self), donc son dictionnaire children{} qui contient tous les noeuds
        for letter in word:
            if letter not in node.children:
                node.children[letter] = Arborescence() # là, on crée un noeud. Quand je disais que c'était fractal, c'est qu'en fait on reprend la même architecture que l'arborescence et qu'on la place dans ce noeud #inception1

            node = node.children[letter] # là on se place dans le noeud de la lettre "définie" par la boucle for letter in word, la variable node "avance" d'un "pas"

        node.word = word # quand on a fini de créer/se placer dans les noeuds, on donne à la variable "word" (qui était définie dans la structure d'une arborescence/noeud) le mot qui vcient d'etre ajouté

# parcours le dictionnaire et le transpose en arborescence
arbre = Arborescence()
for word in Dico:
    arbre.insert(word)

def search(word, maxCost): # la fonction search retourne une liste des mots qui ont une ressemblance inférieur ou égale à maxCost (même principe que Levenshtein)
    currentRow = range(len(word) + 1)
    results = []

    for letter in arbre.children: # là on est parti pour scanner toutes les branches (en commençant par les premiers noeuds) de l'arborescence
        searchRecursive(arbre.children[letter], letter, word, currentRow, results, maxCost) # c'est là que tout se joue

    return results # voila c'est fini... LOL

def searchRecursive(node, letter, word, previousRow, results, maxCost):
    # bien comprendre qu'on est actuellement dans un noeud
    columns = len(word) + 1
    currentRow = [previousRow[0] + 1] # row les chemins, là on avance de 1

    # construit un chemin pour la lettre, avec une colonne pour chaque lettre du mot
    for column in range(1, columns): # calcul théorique de combien nous couterai l'insert/suppr/remplacement d'un caractère par rapport à où on est dans le mot
        insertCost = currentRow[column - 1] + 1
        deleteCost = previousRow[column] + 1

        if word[column - 1] != letter:
            replaceCost = previousRow[column - 1] + 1
        else:                
            replaceCost = previousRow[column - 1]

        currentRow.append(min(insertCost, deleteCost, replaceCost)) # on ne garde que la distance théorique la moins grande (puisqu'on ne sait pas vraiment, on veut juste éviter d'aller chercher dans un nouveau noeud si on sait déjà que quoi qu'il arrive on ne pourra pas accepter le mot)

    # si la dernière entrée de la ligne indique que la différence ne peut être supérieure au maximum (maxCost) alors on ajoute le mot
    if currentRow[-1] <= maxCost and node.word != None: # en réalité au premier passage, à part pour la branche "a" ou "y", celle ligne est ignorée et on passe à d'autres noeuds car word n'existe pas
        results.append((node.word, currentRow[-1])) # on ajoute le mot et son coût levenshteinien

    # si une entrée dans la ligne est inférieur au max, alors on cherche récursivement chaque branche du noeud, généralement le cas au début
    if min(currentRow) <= maxCost:
        for letter in node.children: #inception2, on scanne les branches à partir de ce noeud
            searchRecursive(node.children[letter], letter, word, currentRow, results, maxCost)
 
def verification(phrase):
    phrase = phrase.replace("1", "").replace("2", "").replace("3", "").replace("4", "").replace("5", "").replace("6", "").replace("7", "").replace("8", "").replace("9", "").replace("0", "").replace("#", "").replace("'", " ").replace('"', " ").replace('-', " ").replace(".", " ").replace(",", " ").replace(":", " ").replace(";", " ").replace("!", " ").replace("?", " ").replace("(", " ").replace(")", " ").replace("/", " ").replace("\\", " ").replace('’', ' ').replace('`', ' ').replace("«", " ").replace("»", " ").replace("_", " ") # enlève un certain nombre de caractères incorrigibles
    phrase = phrase.split() # transforme la phrase en un array de mots
    erreurs = []
    for x in range(len(phrase)):
        if not recherche(phrase[x]):
            erreurs.append(phrase[x])
    return erreurs
 
def recherche(mot):
    mot = mot.lower() # change le mot en minuscule
    if not mot in Dico and mot != 'c' and mot != 's' and mot != 'j' and mot != 't' and mot != 'y' and mot != 'd' and mot != 'l' and mot != 'n' and mot != 'm' and mot != 'qu':
        return False
    return True
 
def propositions(erreur, valeurmin):
    results = dict(search(erreur, valeurmin))
    return results # il faut trier les résultats, ceux qui sont les plus proches de valeurmin = 1 doivent apparaître les premiers

def correction(phrase, erreurs): # corrige toutes les erreurs arbitrairement
    for x in range(len(erreurs)):
        newmot = ""
        valeurmin = 0
        while not newmot:
            valeurmin += 1
            result = dict(search(erreurs[x], valeurmin))
            if result:
                newmot = next(iter(result.keys())) # selectionne le premier index du dictionnaire
        phrase = remplacer(phrase, erreurs[x], newmot)
    return phrase

def remplacer(texte, erreur, remplacement): # remplace toutes les erreurs par leur correction
    newremplacement = "" # met une majuscule dans la correction si l'erreur comportait des majuscules
    if len(remplacement) > len(erreur):
        for x in range(len(erreur)):
            if erreur[x].istitle():
                newremplacement = newremplacement + str(remplacement[x]).upper()
            else:
                newremplacement = newremplacement + remplacement[x]
        newremplacement += remplacement[len(erreur):] # sinon il manque des mots
    else:
        for x in range(len(remplacement)):
            if erreur[x].istitle():
                newremplacement = newremplacement + str(remplacement[x]).upper()
            else:
                newremplacement = newremplacement + remplacement[x]
    texte = " "+texte # on ajoute un espace au début pour contourner les conditions suivantes qui sans l'espace ne réctifirait pas le 1er mot
    texte = texte.replace(" "+erreur+" ", " "+newremplacement+" ").replace("'"+erreur+" ", "'"+newremplacement+" ").replace('"'+erreur+" ", '"'+newremplacement+" ").replace("("+erreur+" ", "("+newremplacement+" ").replace("-"+erreur+" ", "-"+newremplacement+" ").replace("_"+erreur+" ", "_"+newremplacement+" ").replace("."+erreur+" ", "."+newremplacement+" ").replace("!"+erreur+" ", "!"+newremplacement+" ").replace("?"+erreur+" ", "?"+newremplacement+" ").replace("'"+erreur+"'", "'"+newremplacement+"'").replace('"'+erreur+'"', '"'+newremplacement+'"').replace('('+erreur+')', '('+newremplacement+')').replace("'"+erreur+"'", "'"+newremplacement+"'").replace(" "+erreur+"'", " "+newremplacement+"'").replace(" "+erreur+'"', " "+newremplacement+'"').replace(" "+erreur+")", " "+newremplacement+")").replace(" "+erreur+"-", " "+newremplacement+"-").replace(" "+erreur+"_", " "+newremplacement+"_") # ces conditions sont nécessaires aux remplacements car un mot juste peut contenir l'erreur !
    return texte[1:] # on retranche tout ce qui est après le premier caractère, donc l'espace mis au début
 
class Fenetre(QWidget):
 
    def __init__(self):
        QWidget.__init__(self)
        super(Fenetre, self).__init__()
        self.initialisation()
       
    def initialisation(self):
 
        self.discrimation = ""

        self.origineTitle = QLabel('Phrases à corriger : ')
        self.origine = QTextEdit()
        self.verif_all = QPushButton('Vérifier tout le texte', None)
        self.corrige_all = QPushButton('Corriger automatiquement le texte', None)
 
        self.erreursTitle = QLabel('Erreurs observés : ')
        self.erreurs = QListWidget()
 
        self.correctionsTitle = QLabel('Propositions de correction : ')
        self.corrections = QListWidget()

        self.initialisation = QPushButton('Vider les erreurs', None)
        self.apropos = QPushButton('À propos du logiciel', None)
 
        self.grid = QGridLayout()
        self.grid.setSpacing(4)
 
        self.grid.addWidget(self.origineTitle, 0, 0)
        self.grid.addWidget(self.origine, 1, 0, 1, 4)
        self.grid.addWidget(self.verif_all, 2, 2)
        self.grid.addWidget(self.corrige_all, 2, 3)
 
        self.grid.addWidget(self.erreursTitle, 3, 0)
        self.grid.addWidget(self.erreurs, 4, 0, 1, 2)
        self.grid.addWidget(self.correctionsTitle, 3, 2)
        self.grid.addWidget(self.corrections, 4, 2, 1, 2)

        self.grid.addWidget(self.initialisation, 5, 1)
        self.grid.addWidget(self.apropos, 5, 3)
 
        # événements
        self.connect(self.origine, SIGNAL("textChanged()"), self.verif) # vérifie si le dernier mot est une erreur oupa
        self.connect(self.erreurs, SIGNAL("itemDoubleClicked(QListWidgetItem*)"), self.recherche) # vérifie si le dernier mot est une erreur oupa
        self.connect(self.corrections, SIGNAL("itemDoubleClicked(QListWidgetItem*)"), self.remplace) # remplace l'erreur par la correction
        self.connect(self.initialisation, SIGNAL("clicked()"), self.initialize) # donne des infos sur le logiciel
        self.connect(self.apropos, SIGNAL("clicked()"), self.infos) # donne des infos sur le logiciel
        self.connect(self.verif_all, SIGNAL("clicked()"), self.verification_all) # donne des infos sur le logiciel
        self.connect(self.corrige_all, SIGNAL("clicked()"), self.correction_all) # donne des infos sur le logiciel
       
        self.setLayout(self.grid)
        self.setFixedSize(800, 600)
        self.setWindowTitle('Correcteur Orthographique - ISN 2013')
        self.show()

    def ajout_erreurs(self, texte):
        erreur = verification(texte)
        if erreur:
            for x in range(len(erreur)): # si la vérification retourne plusieurs erreurs (j'écri <=> ['écri'] et jeys'écri <=> ['jeys', 'écri'])
                if not self.erreurs.findItems(erreur[x], Qt.MatchFixedString):
                    item = QListWidgetItem(erreur[x])
                    self.erreurs.addItem(item)
 
    # définition des événements
    def verif(self):
        texte = self.origine.toPlainText()
        if(len(texte) > 1 and (texte[-1] == ' ' or texte[-1] == '.' or texte[-1] == '!' or texte[-1] == '?' or texte[-1] == "'")): # si la dernière lettre est un espace ou de la ponctuation on vérifie le mot précédent
            derniermot = texte.split()[-1]
            self.ajout_erreurs(derniermot)
 
    def recherche(self):
        self.corrections.clear()
        mot = self.erreurs.selectedItems()[0].text()
        erreur = verification(mot)
        if erreur: # on revérifie que c'est bien une erreur (on sait jamais)
            self.discrimation = erreur[0] # erreur[0] car il ne peut pas y avoir plusieurs erreurs pour un même mot
            corrections = propositions(erreur[0], 3)
            for valeurmin in range(1,4):
                for cle, valeur in corrections.items():
                    if valeur == valeurmin:
                        item = QListWidgetItem(cle)
                        if valeur == 1:
                            item.setBackground(QColor(34, 187, 34, 190)) # couleurs rgba
                        if valeur == 2:
                            item.setBackground(QColor(221, 221, 34, 190))
                        elif valeur == 3:
                            item.setBackground(QColor(187, 34, 34, 190))
                        self.corrections.addItem(item)

    def remplace(self):
        if self.discrimation:
            erreur = self.discrimation
            remplacement = self.corrections.selectedItems()[0].text()
            texte = self.origine.toPlainText()
            texte = remplacer(texte, erreur, remplacement)
            self.origine.setText(texte)

    def verification_all(self): # ajoute a la liste d'erreurs vidée auparavent toutes les erreurs du texte d'un coup
        self.erreurs.clear()
        self.corrections.clear()
        texte = self.origine.toPlainText()
        self.ajout_erreurs(texte)

    def correction_all(self): # corrige tout de façon arbitraire
        self.erreurs.clear()
        self.corrections.clear()
        texte = self.origine.toPlainText()
        erreurs = verification(texte)
        newtexte = correction(texte, erreurs)
        self.origine.setText(newtexte)

    def initialize(self):
        self.erreurs.clear()
        self.corrections.clear()

    def infos(self):
        message = QMessageBox.information(self, 'À propos du logiciel', " Ce logiciel a été originellement conçu par Fabien Borel, Hugo Valery et Nicolas Rieul en terminale 8 au lycée Cézanne d'Aix-en-provence dans le cadre de l'option ISN nouvellement créée. \n\nMode d'emploi : \n - Tapez vos phrases dans le bloc situé en haut, à chaque espace ou ponctuation, le dernier mot est analysé. S'il n'existe pas, il est signalé en bas à gauche. \n - Pour analyser une erreur et obtenir des corrections il faut double-cliquer dessus. Les corrections proposées sont triées par ordre de pertinence. En vert ce sont les mots qui n'ont qu'un caractère de changé (ou ajouté), en jaune 2 et en rouge 3, les propositions de corrections s'arrêtent à 3 pour des soucis de rapidité. \n\nLe logiciel est libre (licence Apache), vous trouverez le code source sur GitHub dans les entrées de l'utilisateur twYnn - https://github.com/twYnn/ \n \n                                     http://isn-product.olympe.in \n", QMessageBox.Ok)
