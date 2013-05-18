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
# Merci de garder cette série de commentaire !
# Thanks to keep those comments alive !

# L'arborescence contient des matrices de mots, organisés par noeuds : un pour chaque lettre. Chaque noeud est suivit par une ou plusieurs lettres susceptibles de fournir un mot et ainsi de suite
class Arborescence:
    def __init__(self):
        self.word = None
        self.children = {}
 
    def insert(self, word):
        node = self
        for letter in word:
            if letter not in node.children:
                node.children[letter] = Arborescence()
 
            node = node.children[letter]
 
        node.word = word
 
# parcours le dictionnaire et le transpose en arborescence
arbre = Arborescence()
for word in Dico:
    arbre.insert(word)
 
# la fonction search retourne une liste des mots qui ont une ressemblance inférieur ou égale à maxCost
def search(word, maxCost):
    currentRow = range(len(word) + 1) # première ligne
    results = []
 
    # recherche récursive sur chaque branche de l'arbre (sélectionnées par les noeuds)
    for letter in arbre.children:
        searchRecursive(arbre.children[letter], letter, word, currentRow, results, maxCost)
 
    return results
 
# la fonction searchRecursive est utilisée par search : elle assure la recherche sur plusieurs lignes (noeuds) pour un même mot
def searchRecursive(node, letter, word, previousRow, results, maxCost):
 
    columns = len(word) + 1
    currentRow = [previousRow[0] + 1]
 
    # construit une ligne pour la lettre, avec une colonne pour chaque lettre du mot, plus une pour le string vide en colonne 0
    for column in range(1, columns):
 
        insertCost = currentRow[column - 1] + 1
        deleteCost = previousRow[column] + 1
 
        if word[column - 1] != letter:
            replaceCost = previousRow[column - 1] + 1
        else:
            replaceCost = previousRow[column - 1]
 
        currentRow.append(min(insertCost, deleteCost, replaceCost))
 
    # si la dernière entrée de la ligne indique que la différence ne peut être supérieure au maximum (maxCost) alors on ajoute le mot
    if currentRow[-1] <= maxCost and node.word != None:
        results.append((node.word, currentRow[-1]))
 
    # si une entrée dans la ligne est inférieur au max, alors on cherche récursivement chaque branche de l'arbre
    if min(currentRow) <= maxCost:
        for letter in node.children:
            searchRecursive(node.children[letter], letter, word, currentRow, results, maxCost)
 
def verification(phrase):
    phrase = phrase.replace("1", " ").replace("2", " ").replace("3", " ").replace("4", " ").replace("5", " ").replace("6", " ").replace("7", " ").replace("8", " ").replace("9", " ").replace("0", " ") # on ne corrige pas les chiffres
    phrase = phrase.replace("'", " ").replace('"', " ").replace('-', " ") # change les ', " et - en espaces
    phrase = phrase.replace(".", "").replace(",", "").replace(":", "").replace(";", "").replace("!", "").replace("?", "").replace("(", "").replace(")", "") # enlève la ponctuation
    phrase = phrase.split() # transforme la phrase en un array de mots
    erreurs = []
    for x in range(len(phrase)):
        if not recherche(phrase[x]):
            erreurs.append(phrase[x])
    return erreurs
 
def recherche(mot):
    mot = mot.replace(".", "").replace(",", "").replace(":", "").replace(";", "").replace("!", "").replace("?", "").replace("(", "").replace(")", "") # enlève la ponctuation
    if mot and not mot in Dico:
        mot = mot.lower() # change le mot en minuscule
        if not mot in Dico and mot != 'c' and mot != 's' and mot != 'j' and mot != 't' and mot != 'y' and mot != 'd' and mot != 'l' and mot != 'n' and mot != 'm' and mot != 'qu':
            return False
    return True
 
def propositions(erreur, valeurmin):
    results = dict(search(erreur, valeurmin))
    return results # il faut trier les résultats, ceux qui sont les plus proches de valeurmin = 1 doivent apparaître les premiers

def correction(phrase, erreurs): # corrige toutes les erreurs arbitrairement
    for x in range(len(erreurs)):
        valeurmin = 3
        results = dict(search(erreurs[x], valeurmin)) # valeurmin est l'écart max de lettres accepté, faudrai le modif en fonction du mot
        newmot = "[introuvable]"

        for result, valeur in list(results.items()):
            if(valeur < valeurmin):
                valeurmin = valeur
                newmot = result
        phrase = phrase.replace(erreurs[x], newmot)
    return phrase
 
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
        if(len(self.origine.toPlainText()) > 1 and self.origine.toPlainText()[-1] == ' '): # si la dernière lettre est un espace on vérifie le mot précédent
            derniermot = self.origine.toPlainText().split()[-1]
            self.ajout_erreurs(derniermot)
 
    def recherche(self):
        self.corrections.clear()
        mot = self.erreurs.selectedItems()[0].text()
        erreur = verification(mot)
        if erreur: # on revérifie que c'est bien une erreur (on sait jamais)
            self.discrimation = erreur[0] # erreur[0] car il ne peut pas y avoir plusieurs erreurs pour un même mot
            corrections = propositions(erreur[0], 3)
            for valeurmin in range(1,3):
                for cle, valeur in corrections.items():
                    if valeur == valeurmin:
                        item = QListWidgetItem(cle)
                        self.corrections.addItem(item)

    def remplace(self):
        if self.discrimation:
            erreur = self.discrimation
            remplacement = self.corrections.selectedItems()[0].text()
            texte = self.origine.toPlainText()
            texte = texte.replace(" "+erreur+" ", " "+remplacement+" ").replace(erreur+" ", remplacement+" ").replace(" "+erreur, " "+remplacement) # l'espace est nécessaire pour ne pas remplacer l'intérieur d'un autre mot qui contient l'erreur par la correction
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

    def infos(self):
        message = QMessageBox.information(self, 'À propos du logiciel', " Ce logiciel a été originellement conçu par Fabien Borel, Hugo Valery et Nicolas Rieul en terminale 8 au lycée Cézanne d'Aix-en-provence dans le cadre de l'option ISN nouvellement créee. \n \n Le logiciel est libre (licence Apache), vous trouverez le code source sur GitHub dans les entrées de l'utilisateur twYnn - https://github.com/twYnn/ \n \n http://isn-product.olympe.in", QMessageBox.Ok)
