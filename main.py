#! /usr/bin/python
#-*-coding: utf-8 -*-
from PyQt4.QtGui import *
import engine, sys
 
def main(args):
    a=QApplication(args)
    # Création d'un widget qui servira de fenêtre
    fenetre=engine.Fenetre()
    fenetre.show()
    r=a.exec_()
    return r
 
if __name__=="__main__":
    main(sys.argv)