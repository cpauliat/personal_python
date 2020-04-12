#!/usr/bin/env python3
#
# -*- coding: utf-8 -*-
# --------------------------------------------------------------------------------------------------------------------------
# Ce programme est une adaptation du célèbre Rubix Cube
#
# Ce programme utilise l'interface graphique Tkinter
#
# Auteur        : Christophe Pauliat
# Platformes    : Linux / Windows / MacOS
#
# IMPORTANT: Pour MacOS, utiliser Python3 et tkinter depuis https://python.org car le Tcm/Tk fourni par Apple a des bugs
#            cf. https://www.python.org/download/mac/tcltk/
#
# Versions
#    2016-01-02: version initiale
#    2020-04-12: conversion en Python 3
# --------------------------------------------------------------------------------------------------------------------------
#

__author__ = "cpauliat"

from tkinter import * 
import tkinter.filedialog
from time import *
import math
import pickle

class rubix:
    #faces = ['avant','arriere','gauche','droite','haut','bas']
    #couleurs = ['jaune','blanc','rouge','orange','bleu','vert']
         
    # numerotation des cases d'une face:
    # 0 = centre
    # 1 = cote gauche haut, puis numerotation en cercle dans sens aiguille montre
    # 1 2 3
    # 8 0 4
    # 7 6 5
        
#    def __init__(self,my_canvas_2d,my_canvas_3d):
    def __init__(self,my_canvas_3d):
        self.face_av = ['yellow','yellow','yellow','yellow','yellow','yellow','yellow','yellow','yellow']
        self.face_ar = ['white','white','white','white','white','white','white','white','white']
        self.face_ga = ['red','red','red','red','red','red','red','red','red']
        self.face_dr = ['orange','orange','orange','orange','orange','orange','orange','orange','orange']
        self.face_ha = ['blue','blue','blue','blue','blue','blue','blue','blue','blue']
        self.face_ba = ['green','green','green','green','green','green','green','green','green']
        self.actions = ['debut']
        
        #self.my_canvas_2d=my_canvas_2d
        self.my_canvas_3d=my_canvas_3d
    
    def save (self,nom_fichier):
        fichier = open (nom_fichier,"wb")
        pickle.dump ([self.face_av, self.face_ar, self.face_ga, self.face_dr, self.face_ha, self.face_ba, self.actions], fichier)
        fichier.close()        
        
    def load (self,fichier):
        liste_de_liste = pickle.load (fichier)
        fichier.close()
        
        self.face_av = list(liste_de_liste[0])
        self.face_ar = list(liste_de_liste[1])
        self.face_ga = list(liste_de_liste[2])
        self.face_dr = list(liste_de_liste[3])
        self.face_ha = list(liste_de_liste[4])
        self.face_ba = list(liste_de_liste[5])
        self.actions = list(liste_de_liste[6])
        
        self.dessine()       
    
    def change_vue_vers_gauche(self,stocke_action,bt_undo):
               
        if stocke_action == 1:
            self.actions.append("CV_G") 
            bt_undo.config(state=NORMAL)
            print(self.actions)
            
        old_fga = list(self.face_ga)
        
        old_ga=list(self.face_ga)
        self.face_ga=self.face_av
        self.face_av=self.face_dr
        self.face_dr=self.face_ar
        self.face_ar=old_ga
        
        old_ha=list(self.face_ha)
        self.face_ha[1]=old_ha[7]
        self.face_ha[2]=old_ha[8]
        self.face_ha[3]=old_ha[1]
        self.face_ha[4]=old_ha[2]
        self.face_ha[5]=old_ha[3]
        self.face_ha[6]=old_ha[4]
        self.face_ha[7]=old_ha[5]
        self.face_ha[8]=old_ha[6]
        
        old_ba=list(self.face_ba)
        self.face_ba[7]=old_ba[1]
        self.face_ba[8]=old_ba[2]
        self.face_ba[1]=old_ba[3]
        self.face_ba[2]=old_ba[4]
        self.face_ba[3]=old_ba[5]
        self.face_ba[4]=old_ba[6]
        self.face_ba[5]=old_ba[7]
        self.face_ba[6]=old_ba[8]
        
        self.dessine()
        
    def change_vue_vers_droite(self,stocke_action,bt_undo):
               
        if stocke_action == 1:
            self.actions.append("CV_D") 
            bt_undo.config(state=NORMAL)
            print(self.actions)
                
        old_dr=list(self.face_dr)
        self.face_dr=self.face_av
        self.face_av=self.face_ga
        self.face_ga=self.face_ar
        self.face_ar=old_dr
        
        old_ba=list(self.face_ba)
        self.face_ba[1]=old_ba[7]
        self.face_ba[2]=old_ba[8]
        self.face_ba[3]=old_ba[1]
        self.face_ba[4]=old_ba[2]
        self.face_ba[5]=old_ba[3]
        self.face_ba[6]=old_ba[4]
        self.face_ba[7]=old_ba[5]
        self.face_ba[8]=old_ba[6]
        
        old_ha=list(self.face_ha)
        self.face_ha[7]=old_ha[1]
        self.face_ha[8]=old_ha[2]
        self.face_ha[1]=old_ha[3]
        self.face_ha[2]=old_ha[4]
        self.face_ha[3]=old_ha[5]
        self.face_ha[4]=old_ha[6]
        self.face_ha[5]=old_ha[7]
        self.face_ha[6]=old_ha[8]
        
        self.dessine()        
        
    def change_vue_vers_haut(self,stocke_action,bt_undo):
               
        if stocke_action == 1:
            self.actions.append("CV_H") 
            bt_undo.config(state=NORMAL)
            print(self.actions)
                
        old_ar=list(self.face_ar)
        self.face_ar[0]=self.face_ha[0]
        self.face_ar[1]=self.face_ha[5]
        self.face_ar[2]=self.face_ha[6]
        self.face_ar[3]=self.face_ha[7]
        self.face_ar[4]=self.face_ha[8]
        self.face_ar[5]=self.face_ha[1]
        self.face_ar[6]=self.face_ha[2]
        self.face_ar[7]=self.face_ha[3]
        self.face_ar[8]=self.face_ha[4]
        self.face_ha=list(self.face_av)
        self.face_av=list(self.face_ba)
        self.face_ba[0]=old_ar[0]
        self.face_ba[1]=old_ar[5]
        self.face_ba[2]=old_ar[6]
        self.face_ba[3]=old_ar[7]
        self.face_ba[4]=old_ar[8]
        self.face_ba[5]=old_ar[1]
        self.face_ba[6]=old_ar[2]
        self.face_ba[7]=old_ar[3]
        self.face_ba[8]=old_ar[4]
        
        old_ga=list(self.face_ga)
        self.face_ga[1]=old_ga[3]
        self.face_ga[2]=old_ga[4]
        self.face_ga[3]=old_ga[5]
        self.face_ga[4]=old_ga[6]
        self.face_ga[5]=old_ga[7]
        self.face_ga[6]=old_ga[8]
        self.face_ga[7]=old_ga[1]
        self.face_ga[8]=old_ga[2]
        
        old_dr=list(self.face_dr)
        self.face_dr[3]=old_dr[1]
        self.face_dr[4]=old_dr[2]
        self.face_dr[5]=old_dr[3]
        self.face_dr[6]=old_dr[4]
        self.face_dr[7]=old_dr[5]
        self.face_dr[8]=old_dr[6]
        self.face_dr[1]=old_dr[7]
        self.face_dr[2]=old_dr[8]
        
        self.dessine()        
        
    def change_vue_vers_bas(self,stocke_action,bt_undo):
               
        if stocke_action == 1:
            self.actions.append("CV_B") 
            bt_undo.config(state=NORMAL)
            print(self.actions)
                
        old_ar=list(self.face_ar)
        self.face_ar[0]=self.face_ba[0]
        self.face_ar[1]=self.face_ba[5]
        self.face_ar[2]=self.face_ba[6]
        self.face_ar[3]=self.face_ba[7]
        self.face_ar[4]=self.face_ba[8]
        self.face_ar[5]=self.face_ba[1]
        self.face_ar[6]=self.face_ba[2]
        self.face_ar[7]=self.face_ba[3]
        self.face_ar[8]=self.face_ba[4]
        self.face_ba=list(self.face_av)
        self.face_av=list(self.face_ha)
        self.face_ha[0]=old_ar[0]
        self.face_ha[1]=old_ar[5]
        self.face_ha[2]=old_ar[6]
        self.face_ha[3]=old_ar[7]
        self.face_ha[4]=old_ar[8]
        self.face_ha[5]=old_ar[1]
        self.face_ha[6]=old_ar[2]
        self.face_ha[7]=old_ar[3]
        self.face_ha[8]=old_ar[4]    
        
        old_dr=list(self.face_dr)
        self.face_dr[1]=old_dr[3]
        self.face_dr[2]=old_dr[4]
        self.face_dr[3]=old_dr[5]
        self.face_dr[4]=old_dr[6]
        self.face_dr[5]=old_dr[7]
        self.face_dr[6]=old_dr[8]
        self.face_dr[7]=old_dr[1]
        self.face_dr[8]=old_dr[2]
        
        old_ga=list(self.face_ga)
        self.face_ga[3]=old_ga[1]
        self.face_ga[4]=old_ga[2]
        self.face_ga[5]=old_ga[3]
        self.face_ga[6]=old_ga[4]
        self.face_ga[7]=old_ga[5]
        self.face_ga[8]=old_ga[6]
        self.face_ga[1]=old_ga[7]
        self.face_ga[2]=old_ga[8]
        
        self.dessine()        
        
        
    def dessine_3d_ga_ha (self, x, y, px, py):
               
        # -- dessine face gauche
        self.my_canvas_3d.create_polygon(x-3*px, y-3*py, x-2*px, y-2*py, x-2*px, y+0*py, x-3*px, y-1*py, fill=self.face_ga[1]) 
        self.my_canvas_3d.create_polygon(x-2*px, y-2*py, x-1*px, y-1*py, x-1*px, y+1*py, x-2*px, y+0*py, fill=self.face_ga[2]) 
        self.my_canvas_3d.create_polygon(x-1*px, y-1*py, x+0*px, y+0*py, x+0*px, y+2*py, x-1*px, y+1*py, fill=self.face_ga[3]) 
        self.my_canvas_3d.create_polygon(x-3*px, y-1*py, x-2*px, y+0*py, x-2*px, y+2*py, x-3*px, y+1*py, fill=self.face_ga[8]) 
        self.my_canvas_3d.create_polygon(x-2*px, y+0*py, x-1*px, y+1*py, x-1*px, y+3*py, x-2*px, y+2*py, fill=self.face_ga[0]) 
        self.my_canvas_3d.create_polygon(x-1*px, y+1*py, x+0*px, y+2*py, x+0*px, y+4*py, x-1*px, y+3*py, fill=self.face_ga[4]) 
        self.my_canvas_3d.create_polygon(x-3*px, y+1*py, x-2*px, y+2*py, x-2*px, y+4*py, x-3*px, y+3*py, fill=self.face_ga[7]) 
        self.my_canvas_3d.create_polygon(x-2*px, y+2*py, x-1*px, y+3*py, x-1*px, y+5*py, x-2*px, y+4*py, fill=self.face_ga[6]) 
        self.my_canvas_3d.create_polygon(x-1*px, y+3*py, x+0*px, y+4*py, x+0*px, y+6*py, x-1*px, y+5*py, fill=self.face_ga[5]) 
        #Label(my_canvas_3d,text="0").place(x=x+px+10, y=y+3*py+25)       
        
                
        # -- dessine face avant 
        self.my_canvas_3d.create_polygon(x     , y     , x+1*px, y-1*py, x+1*px, y+1*py, x     , y+2*py, fill=self.face_av[1]) 
        self.my_canvas_3d.create_polygon(x+1*px, y-1*py, x+2*px, y-2*py, x+2*px, y+0*py, x+1*px, y+1*py, fill=self.face_av[2]) 
        self.my_canvas_3d.create_polygon(x+2*px, y-2*py, x+3*px, y-3*py, x+3*px, y-1*py, x+2*px, y+0*py, fill=self.face_av[3]) 
        self.my_canvas_3d.create_polygon(x     , y+2*py, x+1*px, y+1*py, x+1*px, y+3*py, x     , y+4*py, fill=self.face_av[8]) 
        self.my_canvas_3d.create_polygon(x+1*px, y+1*py, x+2*px, y+0*py, x+2*px, y+2*py, x+1*px, y+3*py, fill=self.face_av[0]) 
        self.my_canvas_3d.create_polygon(x+2*px, y+0*py, x+3*px, y-1*py, x+3*px, y+1*py, x+2*px, y+2*py, fill=self.face_av[4])                 
        self.my_canvas_3d.create_polygon(x     , y+4*py, x+1*px, y+3*py, x+1*px, y+5*py, x     , y+6*py, fill=self.face_av[7]) 
        self.my_canvas_3d.create_polygon(x+1*px, y+3*py, x+2*px, y+2*py, x+2*px, y+4*py, x+1*px, y+5*py, fill=self.face_av[6]) 
        self.my_canvas_3d.create_polygon(x+2*px, y+2*py, x+3*px, y+1*py, x+3*px, y+3*py, x+2*px, y+4*py, fill=self.face_av[5])         
        
        # -- dessine face haut
        self.my_canvas_3d.create_polygon(x+0*px, y-6*py, x+1*px, y-5*py, x+0*px, y-4*py, x-1*px, y-5*py, fill=self.face_ha[3]) 
        self.my_canvas_3d.create_polygon(x+1*px, y-5*py, x+2*px, y-4*py, x+1*px, y-3*py, x+0*px, y-4*py, fill=self.face_ha[4]) 
        self.my_canvas_3d.create_polygon(x+2*px, y-4*py, x+3*px, y-3*py, x+2*px, y-2*py, x+1*px, y-3*py, fill=self.face_ha[5]) 
        self.my_canvas_3d.create_polygon(x-1*px, y-5*py, x+0*px, y-4*py, x-1*px, y-3*py, x-2*px, y-4*py, fill=self.face_ha[2]) 
        self.my_canvas_3d.create_polygon(x+0*px, y-4*py, x+1*px, y-3*py, x+0*px, y-2*py, x-1*px, y-3*py, fill=self.face_ha[0]) 
        self.my_canvas_3d.create_polygon(x+1*px, y-3*py, x+2*px, y-2*py, x+1*px, y-1*py, x+0*px, y-2*py, fill=self.face_ha[6]) 
        self.my_canvas_3d.create_polygon(x-2*px, y-4*py, x-1*px, y-3*py, x-2*px, y-2*py, x-3*px, y-3*py, fill=self.face_ha[1]) 
        self.my_canvas_3d.create_polygon(x-1*px, y-3*py, x+0*px, y-2*py, x-1*px, y-1*py, x-2*px, y-2*py, fill=self.face_ha[8]) 
        self.my_canvas_3d.create_polygon(x+0*px, y-2*py, x+1*px, y-1*py, x+0*px, y+0*py, x-1*px, y-1*py, fill=self.face_ha[7]) 
        
        # -- lignes de separations face gauche
        self.my_canvas_3d.create_line (x-3*px, y-3*py, x+0*px, y+0*py, width=4, fill="black")
        self.my_canvas_3d.create_line (x-3*px, y-1*py, x+0*px, y+2*py, width=4, fill="black")
        self.my_canvas_3d.create_line (x-3*px, y+1*py, x+0*px, y+4*py, width=4, fill="black")
        self.my_canvas_3d.create_line (x-3*px, y+3*py, x+0*px, y+6*py, width=4, fill="black")
        self.my_canvas_3d.create_line (x-3*px, y-3*py, x-3*px, y+3*py, width=4, fill="black")
        self.my_canvas_3d.create_line (x-2*px, y-2*py, x-2*px, y+4*py, width=4, fill="black")
        self.my_canvas_3d.create_line (x-1*px, y-1*py, x-1*px, y+5*py, width=4, fill="black")
        self.my_canvas_3d.create_line (x+0*px, y+0*py, x+0*px, y+6*py, width=4, fill="black")
        
        # -- lignes de separations face avant
        self.my_canvas_3d.create_line (x+0*px, y+0*py, x+3*px, y-3*py, width=4, fill="black")
        self.my_canvas_3d.create_line (x+0*px, y+2*py, x+3*px, y-1*py, width=4, fill="black")
        self.my_canvas_3d.create_line (x+0*px, y+4*py, x+3*px, y+1*py, width=4, fill="black")
        self.my_canvas_3d.create_line (x+0*px, y+6*py, x+3*px, y+3*py, width=4, fill="black")
        self.my_canvas_3d.create_line (x+0*px, y+0*py, x+0*px, y+6*py, width=4, fill="black")
        self.my_canvas_3d.create_line (x+1*px, y-1*py, x+1*px, y+5*py, width=4, fill="black")
        self.my_canvas_3d.create_line (x+2*px, y-2*py, x+2*px, y+4*py, width=4, fill="black")
        self.my_canvas_3d.create_line (x+3*px, y-3*py, x+3*px, y+3*py, width=4, fill="black")
        
        # -- lignes de separations face haute        
        self.my_canvas_3d.create_line (x+0*px, y-6*py, x+3*px, y-3*py, width=4, fill="black")
        self.my_canvas_3d.create_line (x-1*px, y-5*py, x+2*px, y-2*py, width=4, fill="black")
        self.my_canvas_3d.create_line (x-2*px, y-4*py, x+1*px, y-1*py, width=4, fill="black")
        self.my_canvas_3d.create_line (x-3*px, y-3*py, x+0*px, y+0*py, width=4, fill="black")
        
        self.my_canvas_3d.create_line (x+0*px, y-6*py, x-3*px, y-3*py, width=4, fill="black")
        self.my_canvas_3d.create_line (x+1*px, y-5*py, x-2*px, y-2*py, width=4, fill="black")
        self.my_canvas_3d.create_line (x+2*px, y-4*py, x-1*px, y-1*py, width=4, fill="black")
        self.my_canvas_3d.create_line (x+3*px, y-3*py, x+0*px, y+0*py, width=4, fill="black")
        
                
    def dessine_3d_ga_ba(self, x, y, px, py):                            
        
        # -- dessine face gauche
        self.my_canvas_3d.create_polygon(x-3*px, y-3*py, x-2*px, y-4*py, x-2*px, y-2*py, x-3*px, y-1*py, fill=self.face_ga[1]) 
        self.my_canvas_3d.create_polygon(x-2*px, y-4*py, x-1*px, y-5*py, x-1*px, y-3*py, x-2*px, y-2*py, fill=self.face_ga[2]) 
        self.my_canvas_3d.create_polygon(x-1*px, y-5*py, x+0*px, y-6*py, x+0*px, y-4*py, x-1*px, y-3*py, fill=self.face_ga[3])         
        self.my_canvas_3d.create_polygon(x-3*px, y-1*py, x-2*px, y-2*py, x-2*px, y+0*py, x-3*px, y+1*py, fill=self.face_ga[8]) 
        self.my_canvas_3d.create_polygon(x-2*px, y-2*py, x-1*px, y-3*py, x-1*px, y-1*py, x-2*px, y+0*py, fill=self.face_ga[0]) 
        self.my_canvas_3d.create_polygon(x-1*px, y-3*py, x+0*px, y-4*py, x+0*px, y-2*py, x-1*px, y-1*py, fill=self.face_ga[4]) 
        self.my_canvas_3d.create_polygon(x-3*px, y+1*py, x-2*px, y+0*py, x-2*px, y+2*py, x-3*px, y+3*py, fill=self.face_ga[7]) 
        self.my_canvas_3d.create_polygon(x-2*px, y+0*py, x-1*px, y-1*py, x-1*px, y+1*py, x-2*px, y+2*py, fill=self.face_ga[6]) 
        self.my_canvas_3d.create_polygon(x-1*px, y-1*py, x+0*px, y-2*py, x+0*px, y+0*py, x-1*px, y+1*py, fill=self.face_ga[5])         
        
        # -- dessine face avant
        self.my_canvas_3d.create_polygon(x+0*px, y-6*py, x+1*px, y-5*py, x+1*px, y-3*py, x+0*px, y-4*py, fill=self.face_av[1]) 
        self.my_canvas_3d.create_polygon(x+1*px, y-5*py, x+2*px, y-4*py, x+2*px, y-2*py, x+1*px, y-3*py, fill=self.face_av[2]) 
        self.my_canvas_3d.create_polygon(x+2*px, y-4*py, x+3*px, y-3*py, x+3*px, y-1*py, x+2*px, y-2*py, fill=self.face_av[3])
        self.my_canvas_3d.create_polygon(x+0*px, y-4*py, x+1*px, y-3*py, x+1*px, y-1*py, x+0*px, y-2*py, fill=self.face_av[8]) 
        self.my_canvas_3d.create_polygon(x+1*px, y-3*py, x+2*px, y-2*py, x+2*px, y+0*py, x+1*px, y-1*py, fill=self.face_av[0]) 
        self.my_canvas_3d.create_polygon(x+2*px, y-2*py, x+3*px, y-1*py, x+3*px, y+1*py, x+2*px, y+0*py, fill=self.face_av[4])        
        self.my_canvas_3d.create_polygon(x+0*px, y-2*py, x+1*px, y-1*py, x+1*px, y+1*py, x+0*px, y+0*py, fill=self.face_av[7]) 
        self.my_canvas_3d.create_polygon(x+1*px, y-1*py, x+2*px, y+0*py, x+2*px, y+2*py, x+1*px, y+1*py, fill=self.face_av[6]) 
        self.my_canvas_3d.create_polygon(x+2*px, y+0*py, x+3*px, y+1*py, x+3*px, y+3*py, x+2*px, y+2*py, fill=self.face_av[5])         
        
        # -- dessine face bas        
        self.my_canvas_3d.create_polygon(x+0*px, y+0*py, x+1*px, y+1*py, x+0*px, y+2*py, x-1*px, y+1*py, fill=self.face_ba[1]) 
        self.my_canvas_3d.create_polygon(x+1*px, y+1*py, x+2*px, y+2*py, x+1*px, y+3*py, x+0*px, y+2*py, fill=self.face_ba[2]) 
        self.my_canvas_3d.create_polygon(x+2*px, y+2*py, x+3*px, y+3*py, x+2*px, y+4*py, x+1*px, y+3*py, fill=self.face_ba[3]) 
        self.my_canvas_3d.create_polygon(x-1*px, y+1*py, x+0*px, y+2*py, x-1*px, y+3*py, x-2*px, y+2*py, fill=self.face_ba[8]) 
        self.my_canvas_3d.create_polygon(x+0*px, y+2*py, x+1*px, y+3*py, x+0*px, y+4*py, x-1*px, y+3*py, fill=self.face_ba[0]) 
        self.my_canvas_3d.create_polygon(x+1*px, y+3*py, x+2*px, y+4*py, x+1*px, y+5*py, x+0*px, y+4*py, fill=self.face_ba[4]) 
        self.my_canvas_3d.create_polygon(x-2*px, y+2*py, x-1*px, y+3*py, x-2*px, y+4*py, x-3*px, y+3*py, fill=self.face_ba[7]) 
        self.my_canvas_3d.create_polygon(x-1*px, y+3*py, x+0*px, y+4*py, x-1*px, y+5*py, x-2*px, y+4*py, fill=self.face_ba[6]) 
        self.my_canvas_3d.create_polygon(x+0*px, y+4*py, x+1*px, y+5*py, x+0*px, y+6*py, x-1*px, y+5*py, fill=self.face_ba[5]) 
        
        # -- lignes de separations face gauche
        self.my_canvas_3d.create_line (x-3*px, y-3*py, x+0*px, y-6*py, width=4, fill="black")
        self.my_canvas_3d.create_line (x-3*px, y-1*py, x+0*px, y-4*py, width=4, fill="black")
        self.my_canvas_3d.create_line (x-3*px, y+1*py, x+0*px, y-2*py, width=4, fill="black")
        self.my_canvas_3d.create_line (x-3*px, y+3*py, x+0*px, y+0*py, width=4, fill="black")        
        self.my_canvas_3d.create_line (x-3*px, y-3*py, x-3*px, y+3*py, width=4, fill="black")
        self.my_canvas_3d.create_line (x-2*px, y-4*py, x-2*px, y+2*py, width=4, fill="black")
        self.my_canvas_3d.create_line (x-1*px, y-5*py, x-1*px, y+1*py, width=4, fill="black")
        self.my_canvas_3d.create_line (x+0*px, y-6*py, x+0*px, y+0*py, width=4, fill="black")
        
        # -- lignes de separations face avant
        self.my_canvas_3d.create_line (x+0*px, y-6*py, x+3*px, y-3*py, width=4, fill="black")
        self.my_canvas_3d.create_line (x+0*px, y-4*py, x+3*px, y-1*py, width=4, fill="black")
        self.my_canvas_3d.create_line (x+0*px, y-2*py, x+3*px, y+1*py, width=4, fill="black")
        self.my_canvas_3d.create_line (x+0*px, y+0*py, x+3*px, y+3*py, width=4, fill="black")    
        self.my_canvas_3d.create_line (x+0*px, y-6*py, x+0*px, y+0*py, width=4, fill="black")
        self.my_canvas_3d.create_line (x+1*px, y-5*py, x+1*px, y+1*py, width=4, fill="black")
        self.my_canvas_3d.create_line (x+2*px, y-4*py, x+2*px, y+2*py, width=4, fill="black")
        self.my_canvas_3d.create_line (x+3*px, y-3*py, x+3*px, y+3*py, width=4, fill="black")
        
        # -- lignes de separations face bas  
        self.my_canvas_3d.create_line (x+0*px, y+0*py, x+3*px, y+3*py, width=4, fill="black")
        self.my_canvas_3d.create_line (x-1*px, y+1*py, x+2*px, y+4*py, width=4, fill="black")
        self.my_canvas_3d.create_line (x-2*px, y+2*py, x+1*px, y+5*py, width=4, fill="black")
        self.my_canvas_3d.create_line (x-3*px, y+3*py, x+0*px, y+6*py, width=4, fill="black")
        self.my_canvas_3d.create_line (x+0*px, y+0*py, x-3*px, y+3*py, width=4, fill="black")
        self.my_canvas_3d.create_line (x+1*px, y+1*py, x-2*px, y+4*py, width=4, fill="black")
        self.my_canvas_3d.create_line (x+2*px, y+2*py, x-1*px, y+5*py, width=4, fill="black")
        self.my_canvas_3d.create_line (x+3*px, y+3*py, x+0*px, y+6*py, width=4, fill="black")
        
    def dessine_3d_dr_ha (self, x, y, px, py):
               
        # -- dessine face avant
        self.my_canvas_3d.create_polygon(x-3*px, y-3*py, x-2*px, y-2*py, x-2*px, y+0*py, x-3*px, y-1*py, fill=self.face_av[1]) 
        self.my_canvas_3d.create_polygon(x-2*px, y-2*py, x-1*px, y-1*py, x-1*px, y+1*py, x-2*px, y+0*py, fill=self.face_av[2]) 
        self.my_canvas_3d.create_polygon(x-1*px, y-1*py, x+0*px, y+0*py, x+0*px, y+2*py, x-1*px, y+1*py, fill=self.face_av[3]) 
        self.my_canvas_3d.create_polygon(x-3*px, y-1*py, x-2*px, y+0*py, x-2*px, y+2*py, x-3*px, y+1*py, fill=self.face_av[8]) 
        self.my_canvas_3d.create_polygon(x-2*px, y+0*py, x-1*px, y+1*py, x-1*px, y+3*py, x-2*px, y+2*py, fill=self.face_av[0]) 
        self.my_canvas_3d.create_polygon(x-1*px, y+1*py, x+0*px, y+2*py, x+0*px, y+4*py, x-1*px, y+3*py, fill=self.face_av[4]) 
        self.my_canvas_3d.create_polygon(x-3*px, y+1*py, x-2*px, y+2*py, x-2*px, y+4*py, x-3*px, y+3*py, fill=self.face_av[7]) 
        self.my_canvas_3d.create_polygon(x-2*px, y+2*py, x-1*px, y+3*py, x-1*px, y+5*py, x-2*px, y+4*py, fill=self.face_av[6]) 
        self.my_canvas_3d.create_polygon(x-1*px, y+3*py, x+0*px, y+4*py, x+0*px, y+6*py, x-1*px, y+5*py, fill=self.face_av[5]) 
                
        # -- dessine face droite 
        self.my_canvas_3d.create_polygon(x     , y     , x+1*px, y-1*py, x+1*px, y+1*py, x     , y+2*py, fill=self.face_dr[1]) 
        self.my_canvas_3d.create_polygon(x+1*px, y-1*py, x+2*px, y-2*py, x+2*px, y+0*py, x+1*px, y+1*py, fill=self.face_dr[2]) 
        self.my_canvas_3d.create_polygon(x+2*px, y-2*py, x+3*px, y-3*py, x+3*px, y-1*py, x+2*px, y+0*py, fill=self.face_dr[3]) 
        self.my_canvas_3d.create_polygon(x     , y+2*py, x+1*px, y+1*py, x+1*px, y+3*py, x     , y+4*py, fill=self.face_dr[8]) 
        self.my_canvas_3d.create_polygon(x+1*px, y+1*py, x+2*px, y+0*py, x+2*px, y+2*py, x+1*px, y+3*py, fill=self.face_dr[0]) 
        self.my_canvas_3d.create_polygon(x+2*px, y+0*py, x+3*px, y-1*py, x+3*px, y+1*py, x+2*px, y+2*py, fill=self.face_dr[4])                 
        self.my_canvas_3d.create_polygon(x     , y+4*py, x+1*px, y+3*py, x+1*px, y+5*py, x     , y+6*py, fill=self.face_dr[7]) 
        self.my_canvas_3d.create_polygon(x+1*px, y+3*py, x+2*px, y+2*py, x+2*px, y+4*py, x+1*px, y+5*py, fill=self.face_dr[6]) 
        self.my_canvas_3d.create_polygon(x+2*px, y+2*py, x+3*px, y+1*py, x+3*px, y+3*py, x+2*px, y+4*py, fill=self.face_dr[5])         
        
        # -- dessine face haut
        self.my_canvas_3d.create_polygon(x+0*px, y-6*py, x+1*px, y-5*py, x+0*px, y-4*py, x-1*px, y-5*py, fill=self.face_ha[1]) 
        self.my_canvas_3d.create_polygon(x+1*px, y-5*py, x+2*px, y-4*py, x+1*px, y-3*py, x+0*px, y-4*py, fill=self.face_ha[2]) 
        self.my_canvas_3d.create_polygon(x+2*px, y-4*py, x+3*px, y-3*py, x+2*px, y-2*py, x+1*px, y-3*py, fill=self.face_ha[3]) 
        self.my_canvas_3d.create_polygon(x-1*px, y-5*py, x+0*px, y-4*py, x-1*px, y-3*py, x-2*px, y-4*py, fill=self.face_ha[8]) 
        self.my_canvas_3d.create_polygon(x+0*px, y-4*py, x+1*px, y-3*py, x+0*px, y-2*py, x-1*px, y-3*py, fill=self.face_ha[0]) 
        self.my_canvas_3d.create_polygon(x+1*px, y-3*py, x+2*px, y-2*py, x+1*px, y-1*py, x+0*px, y-2*py, fill=self.face_ha[4]) 
        self.my_canvas_3d.create_polygon(x-2*px, y-4*py, x-1*px, y-3*py, x-2*px, y-2*py, x-3*px, y-3*py, fill=self.face_ha[7]) 
        self.my_canvas_3d.create_polygon(x-1*px, y-3*py, x+0*px, y-2*py, x-1*px, y-1*py, x-2*px, y-2*py, fill=self.face_ha[6]) 
        self.my_canvas_3d.create_polygon(x+0*px, y-2*py, x+1*px, y-1*py, x+0*px, y+0*py, x-1*px, y-1*py, fill=self.face_ha[5]) 
        
        # -- lignes de separations face avant
        self.my_canvas_3d.create_line (x-3*px, y-3*py, x+0*px, y+0*py, width=4, fill="black")
        self.my_canvas_3d.create_line (x-3*px, y-1*py, x+0*px, y+2*py, width=4, fill="black")
        self.my_canvas_3d.create_line (x-3*px, y+1*py, x+0*px, y+4*py, width=4, fill="black")
        self.my_canvas_3d.create_line (x-3*px, y+3*py, x+0*px, y+6*py, width=4, fill="black")
        self.my_canvas_3d.create_line (x-3*px, y-3*py, x-3*px, y+3*py, width=4, fill="black")
        self.my_canvas_3d.create_line (x-2*px, y-2*py, x-2*px, y+4*py, width=4, fill="black")
        self.my_canvas_3d.create_line (x-1*px, y-1*py, x-1*px, y+5*py, width=4, fill="black")
        self.my_canvas_3d.create_line (x+0*px, y+0*py, x+0*px, y+6*py, width=4, fill="black")
        
        # -- lignes de separations face droite
        self.my_canvas_3d.create_line (x+0*px, y+0*py, x+3*px, y-3*py, width=4, fill="black")
        self.my_canvas_3d.create_line (x+0*px, y+2*py, x+3*px, y-1*py, width=4, fill="black")
        self.my_canvas_3d.create_line (x+0*px, y+4*py, x+3*px, y+1*py, width=4, fill="black")
        self.my_canvas_3d.create_line (x+0*px, y+6*py, x+3*px, y+3*py, width=4, fill="black")
        self.my_canvas_3d.create_line (x+0*px, y+0*py, x+0*px, y+6*py, width=4, fill="black")
        self.my_canvas_3d.create_line (x+1*px, y-1*py, x+1*px, y+5*py, width=4, fill="black")
        self.my_canvas_3d.create_line (x+2*px, y-2*py, x+2*px, y+4*py, width=4, fill="black")
        self.my_canvas_3d.create_line (x+3*px, y-3*py, x+3*px, y+3*py, width=4, fill="black")
        
        # -- lignes de separations face haute
        self.my_canvas_3d.create_line (x+0*px, y-6*py, x+3*px, y-3*py, width=4, fill="black")
        self.my_canvas_3d.create_line (x-1*px, y-5*py, x+2*px, y-2*py, width=4, fill="black")
        self.my_canvas_3d.create_line (x-2*px, y-4*py, x+1*px, y-1*py, width=4, fill="black")
        self.my_canvas_3d.create_line (x-3*px, y-3*py, x+0*px, y+0*py, width=4, fill="black")        
        self.my_canvas_3d.create_line (x+0*px, y-6*py, x-3*px, y-3*py, width=4, fill="black")
        self.my_canvas_3d.create_line (x+1*px, y-5*py, x-2*px, y-2*py, width=4, fill="black")
        self.my_canvas_3d.create_line (x+2*px, y-4*py, x-1*px, y-1*py, width=4, fill="black")
        self.my_canvas_3d.create_line (x+3*px, y-3*py, x+0*px, y+0*py, width=4, fill="black")                
        
    def dessine_3d_dr_ba(self, x, y, px, py):
        
        # -- dessine face avant
        self.my_canvas_3d.create_polygon(x-3*px, y-3*py, x-2*px, y-4*py, x-2*px, y-2*py, x-3*px, y-1*py, fill=self.face_av[1]) 
        self.my_canvas_3d.create_polygon(x-2*px, y-4*py, x-1*px, y-5*py, x-1*px, y-3*py, x-2*px, y-2*py, fill=self.face_av[2]) 
        self.my_canvas_3d.create_polygon(x-1*px, y-5*py, x+0*px, y-6*py, x+0*px, y-4*py, x-1*px, y-3*py, fill=self.face_av[3])         
        self.my_canvas_3d.create_polygon(x-3*px, y-1*py, x-2*px, y-2*py, x-2*px, y+0*py, x-3*px, y+1*py, fill=self.face_av[8]) 
        self.my_canvas_3d.create_polygon(x-2*px, y-2*py, x-1*px, y-3*py, x-1*px, y-1*py, x-2*px, y+0*py, fill=self.face_av[0]) 
        self.my_canvas_3d.create_polygon(x-1*px, y-3*py, x+0*px, y-4*py, x+0*px, y-2*py, x-1*px, y-1*py, fill=self.face_av[4]) 
        self.my_canvas_3d.create_polygon(x-3*px, y+1*py, x-2*px, y+0*py, x-2*px, y+2*py, x-3*px, y+3*py, fill=self.face_av[7]) 
        self.my_canvas_3d.create_polygon(x-2*px, y+0*py, x-1*px, y-1*py, x-1*px, y+1*py, x-2*px, y+2*py, fill=self.face_av[6]) 
        self.my_canvas_3d.create_polygon(x-1*px, y-1*py, x+0*px, y-2*py, x+0*px, y+0*py, x-1*px, y+1*py, fill=self.face_av[5])         
        
        # -- dessine face droite
        self.my_canvas_3d.create_polygon(x+0*px, y-6*py, x+1*px, y-5*py, x+1*px, y-3*py, x+0*px, y-4*py, fill=self.face_dr[1]) 
        self.my_canvas_3d.create_polygon(x+1*px, y-5*py, x+2*px, y-4*py, x+2*px, y-2*py, x+1*px, y-3*py, fill=self.face_dr[2]) 
        self.my_canvas_3d.create_polygon(x+2*px, y-4*py, x+3*px, y-3*py, x+3*px, y-1*py, x+2*px, y-2*py, fill=self.face_dr[3])
        self.my_canvas_3d.create_polygon(x+0*px, y-4*py, x+1*px, y-3*py, x+1*px, y-1*py, x+0*px, y-2*py, fill=self.face_dr[8]) 
        self.my_canvas_3d.create_polygon(x+1*px, y-3*py, x+2*px, y-2*py, x+2*px, y+0*py, x+1*px, y-1*py, fill=self.face_dr[0]) 
        self.my_canvas_3d.create_polygon(x+2*px, y-2*py, x+3*px, y-1*py, x+3*px, y+1*py, x+2*px, y+0*py, fill=self.face_dr[4])        
        self.my_canvas_3d.create_polygon(x+0*px, y-2*py, x+1*px, y-1*py, x+1*px, y+1*py, x+0*px, y+0*py, fill=self.face_dr[7]) 
        self.my_canvas_3d.create_polygon(x+1*px, y-1*py, x+2*px, y+0*py, x+2*px, y+2*py, x+1*px, y+1*py, fill=self.face_dr[6]) 
        self.my_canvas_3d.create_polygon(x+2*px, y+0*py, x+3*px, y+1*py, x+3*px, y+3*py, x+2*px, y+2*py, fill=self.face_dr[5])         
        
        # -- dessine face bas        
        self.my_canvas_3d.create_polygon(x+0*px, y+0*py, x+1*px, y+1*py, x+0*px, y+2*py, x-1*px, y+1*py, fill=self.face_ba[3]) 
        self.my_canvas_3d.create_polygon(x+1*px, y+1*py, x+2*px, y+2*py, x+1*px, y+3*py, x+0*px, y+2*py, fill=self.face_ba[4]) 
        self.my_canvas_3d.create_polygon(x+2*px, y+2*py, x+3*px, y+3*py, x+2*px, y+4*py, x+1*px, y+3*py, fill=self.face_ba[5]) 
        self.my_canvas_3d.create_polygon(x-1*px, y+1*py, x+0*px, y+2*py, x-1*px, y+3*py, x-2*px, y+2*py, fill=self.face_ba[2]) 
        self.my_canvas_3d.create_polygon(x+0*px, y+2*py, x+1*px, y+3*py, x+0*px, y+4*py, x-1*px, y+3*py, fill=self.face_ba[0]) 
        self.my_canvas_3d.create_polygon(x+1*px, y+3*py, x+2*px, y+4*py, x+1*px, y+5*py, x+0*px, y+4*py, fill=self.face_ba[6]) 
        self.my_canvas_3d.create_polygon(x-2*px, y+2*py, x-1*px, y+3*py, x-2*px, y+4*py, x-3*px, y+3*py, fill=self.face_ba[1]) 
        self.my_canvas_3d.create_polygon(x-1*px, y+3*py, x+0*px, y+4*py, x-1*px, y+5*py, x-2*px, y+4*py, fill=self.face_ba[8]) 
        self.my_canvas_3d.create_polygon(x+0*px, y+4*py, x+1*px, y+5*py, x+0*px, y+6*py, x-1*px, y+5*py, fill=self.face_ba[7]) 
        
        # -- lignes de separations face avant
        self.my_canvas_3d.create_line (x-3*px, y-3*py, x+0*px, y-6*py, width=4, fill="black")
        self.my_canvas_3d.create_line (x-3*px, y-1*py, x+0*px, y-4*py, width=4, fill="black")
        self.my_canvas_3d.create_line (x-3*px, y+1*py, x+0*px, y-2*py, width=4, fill="black")
        self.my_canvas_3d.create_line (x-3*px, y+3*py, x+0*px, y+0*py, width=4, fill="black")        
        self.my_canvas_3d.create_line (x-3*px, y-3*py, x-3*px, y+3*py, width=4, fill="black")
        self.my_canvas_3d.create_line (x-2*px, y-4*py, x-2*px, y+2*py, width=4, fill="black")
        self.my_canvas_3d.create_line (x-1*px, y-5*py, x-1*px, y+1*py, width=4, fill="black")
        self.my_canvas_3d.create_line (x+0*px, y-6*py, x+0*px, y+0*py, width=4, fill="black")
        
        # -- lignes de separations face droite
        self.my_canvas_3d.create_line (x+0*px, y-6*py, x+3*px, y-3*py, width=4, fill="black")
        self.my_canvas_3d.create_line (x+0*px, y-4*py, x+3*px, y-1*py, width=4, fill="black")
        self.my_canvas_3d.create_line (x+0*px, y-2*py, x+3*px, y+1*py, width=4, fill="black")
        self.my_canvas_3d.create_line (x+0*px, y+0*py, x+3*px, y+3*py, width=4, fill="black")    
        self.my_canvas_3d.create_line (x+0*px, y-6*py, x+0*px, y+0*py, width=4, fill="black")
        self.my_canvas_3d.create_line (x+1*px, y-5*py, x+1*px, y+1*py, width=4, fill="black")
        self.my_canvas_3d.create_line (x+2*px, y-4*py, x+2*px, y+2*py, width=4, fill="black")
        self.my_canvas_3d.create_line (x+3*px, y-3*py, x+3*px, y+3*py, width=4, fill="black")
        
        # -- lignes de separations face bas
        self.my_canvas_3d.create_line (x+0*px, y+0*py, x+3*px, y+3*py, width=4, fill="black")
        self.my_canvas_3d.create_line (x-1*px, y+1*py, x+2*px, y+4*py, width=4, fill="black")
        self.my_canvas_3d.create_line (x-2*px, y+2*py, x+1*px, y+5*py, width=4, fill="black")
        self.my_canvas_3d.create_line (x-3*px, y+3*py, x+0*px, y+6*py, width=4, fill="black")
        self.my_canvas_3d.create_line (x+0*px, y+0*py, x-3*px, y+3*py, width=4, fill="black")
        self.my_canvas_3d.create_line (x+1*px, y+1*py, x-2*px, y+4*py, width=4, fill="black")
        self.my_canvas_3d.create_line (x+2*px, y+2*py, x-1*px, y+5*py, width=4, fill="black")
        self.my_canvas_3d.create_line (x+3*px, y+3*py, x+0*px, y+6*py, width=4, fill="black")
        
    def dessine_2d (self):
        # -- dessine face haut
        x=220
        y=20        
        self.my_canvas_2d.create_rectangle(x    ,y    ,x+45 ,y+45 ,fill=self.face_ha[1]) 
        self.my_canvas_2d.create_rectangle(x+50 ,y    ,x+95 ,y+45 ,fill=self.face_ha[2]) 
        self.my_canvas_2d.create_rectangle(x+100,y    ,x+145,y+45 ,fill=self.face_ha[3]) 
        self.my_canvas_2d.create_rectangle(x    ,y+50 ,x+45 ,y+95 ,fill=self.face_ha[8]) 
        self.my_canvas_2d.create_rectangle(x+50 ,y+50 ,x+95 ,y+95 ,fill=self.face_ha[0]) 
        self.my_canvas_2d.create_rectangle(x+100,y+50 ,x+145,y+95 ,fill=self.face_ha[4]) 
        self.my_canvas_2d.create_rectangle(x    ,y+100,x+45 ,y+145,fill=self.face_ha[7]) 
        self.my_canvas_2d.create_rectangle(x+50 ,y+100,x+95 ,y+145,fill=self.face_ha[6]) 
        self.my_canvas_2d.create_rectangle(x+100,y+100,x+145,y+145,fill=self.face_ha[5]) 
        
        # -- dessine face gauche
        x=20
        y=220
        self.my_canvas_2d.create_rectangle(x    ,y    ,x+45 ,y+45 ,fill=self.face_ga[1]) 
        self.my_canvas_2d.create_rectangle(x+50 ,y    ,x+95 ,y+45 ,fill=self.face_ga[2]) 
        self.my_canvas_2d.create_rectangle(x+100,y    ,x+145,y+45 ,fill=self.face_ga[3]) 
        self.my_canvas_2d.create_rectangle(x    ,y+50 ,x+45 ,y+95 ,fill=self.face_ga[8]) 
        self.my_canvas_2d.create_rectangle(x+50 ,y+50 ,x+95 ,y+95 ,fill=self.face_ga[0]) 
        self.my_canvas_2d.create_rectangle(x+100,y+50 ,x+145,y+95 ,fill=self.face_ga[4]) 
        self.my_canvas_2d.create_rectangle(x    ,y+100,x+45 ,y+145,fill=self.face_ga[7]) 
        self.my_canvas_2d.create_rectangle(x+50 ,y+100,x+95 ,y+145,fill=self.face_ga[6]) 
        self.my_canvas_2d.create_rectangle(x+100,y+100,x+145,y+145,fill=self.face_ga[5]) 
    
        # -- dessine face avant
        x=220
        y=220
        self.my_canvas_2d.create_rectangle(x    ,y    ,x+45 ,y+45 ,fill=self.face_av[1]) 
        self.my_canvas_2d.create_rectangle(x+50 ,y    ,x+95 ,y+45 ,fill=self.face_av[2]) 
        self.my_canvas_2d.create_rectangle(x+100,y    ,x+145,y+45 ,fill=self.face_av[3]) 
        self.my_canvas_2d.create_rectangle(x    ,y+50 ,x+45 ,y+95 ,fill=self.face_av[8]) 
        self.my_canvas_2d.create_rectangle(x+50 ,y+50 ,x+95 ,y+95 ,fill=self.face_av[0]) 
        self.my_canvas_2d.create_rectangle(x+100,y+50 ,x+145,y+95 ,fill=self.face_av[4]) 
        self.my_canvas_2d.create_rectangle(x    ,y+100,x+45 ,y+145,fill=self.face_av[7]) 
        self.my_canvas_2d.create_rectangle(x+50 ,y+100,x+95 ,y+145,fill=self.face_av[6]) 
        self.my_canvas_2d.create_rectangle(x+100,y+100,x+145,y+145,fill=self.face_av[5]) 
        
        # -- dessine face droite
        x=420
        y=220
        self.my_canvas_2d.create_rectangle(x    ,y    ,x+45 ,y+45 ,fill=self.face_dr[1]) 
        self.my_canvas_2d.create_rectangle(x+50 ,y    ,x+95 ,y+45 ,fill=self.face_dr[2]) 
        self.my_canvas_2d.create_rectangle(x+100,y    ,x+145,y+45 ,fill=self.face_dr[3]) 
        self.my_canvas_2d.create_rectangle(x    ,y+50 ,x+45 ,y+95 ,fill=self.face_dr[8]) 
        self.my_canvas_2d.create_rectangle(x+50 ,y+50 ,x+95 ,y+95 ,fill=self.face_dr[0]) 
        self.my_canvas_2d.create_rectangle(x+100,y+50 ,x+145,y+95 ,fill=self.face_dr[4]) 
        self.my_canvas_2d.create_rectangle(x    ,y+100,x+45 ,y+145,fill=self.face_dr[7]) 
        self.my_canvas_2d.create_rectangle(x+50 ,y+100,x+95 ,y+145,fill=self.face_dr[6]) 
        self.my_canvas_2d.create_rectangle(x+100,y+100,x+145,y+145,fill=self.face_dr[5]) 

        # -- dessine face arriere
        x=620
        y=220
        self.my_canvas_2d.create_rectangle(x    ,y    ,x+45 ,y+45 ,fill=self.face_ar[1]) 
        self.my_canvas_2d.create_rectangle(x+50 ,y    ,x+95 ,y+45 ,fill=self.face_ar[2]) 
        self.my_canvas_2d.create_rectangle(x+100,y    ,x+145,y+45 ,fill=self.face_ar[3]) 
        self.my_canvas_2d.create_rectangle(x    ,y+50 ,x+45 ,y+95 ,fill=self.face_ar[8]) 
        self.my_canvas_2d.create_rectangle(x+50 ,y+50 ,x+95 ,y+95 ,fill=self.face_ar[0]) 
        self.my_canvas_2d.create_rectangle(x+100,y+50 ,x+145,y+95 ,fill=self.face_ar[4]) 
        self.my_canvas_2d.create_rectangle(x    ,y+100,x+45 ,y+145,fill=self.face_ar[7]) 
        self.my_canvas_2d.create_rectangle(x+50 ,y+100,x+95 ,y+145,fill=self.face_ar[6]) 
        self.my_canvas_2d.create_rectangle(x+100,y+100,x+145,y+145,fill=self.face_ar[5]) 

        # -- dessine face bas
        x=220
        y=420
        self.my_canvas_2d.create_rectangle(x    ,y    ,x+45 ,y+45 ,fill=self.face_ba[1]) 
        self.my_canvas_2d.create_rectangle(x+50 ,y    ,x+95 ,y+45 ,fill=self.face_ba[2]) 
        self.my_canvas_2d.create_rectangle(x+100,y    ,x+145,y+45 ,fill=self.face_ba[3]) 
        self.my_canvas_2d.create_rectangle(x    ,y+50 ,x+45 ,y+95 ,fill=self.face_ba[8]) 
        self.my_canvas_2d.create_rectangle(x+50 ,y+50 ,x+95 ,y+95 ,fill=self.face_ba[0]) 
        self.my_canvas_2d.create_rectangle(x+100,y+50 ,x+145,y+95 ,fill=self.face_ba[4]) 
        self.my_canvas_2d.create_rectangle(x    ,y+100,x+45 ,y+145,fill=self.face_ba[7]) 
        self.my_canvas_2d.create_rectangle(x+50 ,y+100,x+95 ,y+145,fill=self.face_ba[6]) 
        self.my_canvas_2d.create_rectangle(x+100,y+100,x+145,y+145,fill=self.face_ba[5]) 
        
    def dessine (self):
        #self.dessine_2d()
        
        # -- 3D: cote = 50
        c=50
        py=int(0.5*c)
        px=int(c*0.707)
        
        self.dessine_3d_ga_ha(250,250,px,py)
        self.dessine_3d_dr_ha(650,250,px,py)
        self.dessine_3d_ga_ba(250,600,px,py)
        self.dessine_3d_dr_ba(650,600,px,py)
        
    def tourne_av_plus(self,stocke_action,bt_undo):
        old_fav = list(self.face_av)
                    
        if stocke_action == 1:
            self.actions.append("AV+")                    
            bt_undo.config(state=NORMAL)
            print(self.actions)
        
        self.face_av[1] = old_fav[7]
        self.face_av[2] = old_fav[8]
        self.face_av[3] = old_fav[1]                
        self.face_av[4] = old_fav[2]
        self.face_av[5] = old_fav[3]
        self.face_av[6] = old_fav[4]
        self.face_av[7] = old_fav[5]
        self.face_av[8] = old_fav[6]  
                                    
        # haut 
        old_fha   = list(self.face_ha)
        self.face_ha[5] = self.face_ga[3]
        self.face_ha[6] = self.face_ga[4]
        self.face_ha[7] = self.face_ga[5]
        
        # droite 
        old_fdr  = list(self.face_dr)
        self.face_dr[1] = old_fha[7]
        self.face_dr[8] = old_fha[6]
        self.face_dr[7] = old_fha[5]
        
        # bas 
        old_fba   = list(self.face_ba)
        self.face_ba[1] = old_fdr[7]
        self.face_ba[2] = old_fdr[8]
        self.face_ba[3] = old_fdr[1]
        
        # gauche 
        self.face_ga[3] = old_fba[1]
        self.face_ga[4] = old_fba[2]
        self.face_ga[5] = old_fba[3]
        
        # on redessine le cube
        self.dessine()  
        
    def tourne_av_moins(self,stocke_action,bt_undo):
        old_fav = list(self.face_av)
                     
        if stocke_action == 1:
            self.actions.append("AV-") 
            bt_undo.config(state=NORMAL)
            print(self.actions)

        
        self.face_av[1] = old_fav[3]
        self.face_av[2] = old_fav[4]
        self.face_av[3] = old_fav[5]                
        self.face_av[4] = old_fav[6]
        self.face_av[5] = old_fav[7]
        self.face_av[6] = old_fav[8]
        self.face_av[7] = old_fav[1]
        self.face_av[8] = old_fav[2]  
                                    
        # haut 
        old_fha   = list(self.face_ha)
        self.face_ha[7] = self.face_dr[1]
        self.face_ha[6] = self.face_dr[8]
        self.face_ha[5] = self.face_dr[7]
        
        # gauche 
        old_fga  = list(self.face_ga)
        self.face_ga[5] = old_fha[7]
        self.face_ga[4] = old_fha[6]
        self.face_ga[3] = old_fha[5]
        
        # bas 
        old_fba   = list(self.face_ba)
        self.face_ba[1] = old_fga[3]
        self.face_ba[2] = old_fga[4]
        self.face_ba[3] = old_fga[5]
        
        # droite
        self.face_dr[1] = old_fba[3]
        self.face_dr[8] = old_fba[2]
        self.face_dr[7] = old_fba[1]
        
        # on redessine le cube
        self.dessine()    
         
    def tourne_ga_plus(self,stocke_action,bt_undo):
        old_fga = list(self.face_ga)
        
        if stocke_action == 1:
            self.actions.append("G+") 
            bt_undo.config(state=NORMAL)
            print(self.actions)

        
        self.face_ga[1] = old_fga[7]
        self.face_ga[2] = old_fga[8]
        self.face_ga[3] = old_fga[1]                
        self.face_ga[4] = old_fga[2]
        self.face_ga[5] = old_fga[3]
        self.face_ga[6] = old_fga[4]
        self.face_ga[7] = old_fga[5]
        self.face_ga[8] = old_fga[6]  
                                    
        # haut 
        old_fha   = list(self.face_ha)
        self.face_ha[7] = self.face_ar[3]
        self.face_ha[8] = self.face_ar[4]
        self.face_ha[1] = self.face_ar[5]
        
        # avant
        old_fav  = list(self.face_av)
        self.face_av[7] = old_fha[7]
        self.face_av[8] = old_fha[8]
        self.face_av[1] = old_fha[1]
        
        # bas 
        old_fba   = list(self.face_ba)
        self.face_ba[7] = old_fav[7]
        self.face_ba[8] = old_fav[8]
        self.face_ba[1] = old_fav[1]
        
        # arriere 
        self.face_ar[3] = old_fba[7]
        self.face_ar[4] = old_fba[8]
        self.face_ar[5] = old_fba[1]
        
        # on redessine le cube
        self.dessine()  
        
    def tourne_ga_moins(self,stocke_action,bt_undo):
        old_fga = list(self.face_ga)

        if stocke_action == 1:
            self.actions.append("G-")        
            bt_undo.config(state=NORMAL)
            print(self.actions)
        
        self.face_ga[1] = old_fga[3]
        self.face_ga[2] = old_fga[4]
        self.face_ga[3] = old_fga[5]                
        self.face_ga[4] = old_fga[6]
        self.face_ga[5] = old_fga[7]
        self.face_ga[6] = old_fga[8]
        self.face_ga[7] = old_fga[1]
        self.face_ga[8] = old_fga[2]  
                                    
        # haut 
        old_fha   = list(self.face_ha)
        self.face_ha[1] = self.face_av[1]
        self.face_ha[8] = self.face_av[8]
        self.face_ha[7] = self.face_av[7]
        
        # arriere
        old_far  = list(self.face_ar)
        self.face_ar[5] = old_fha[1]
        self.face_ar[4] = old_fha[8]
        self.face_ar[3] = old_fha[7]
        
        # bas 
        old_fba   = list(self.face_ba)
        self.face_ba[1] = old_far[5]
        self.face_ba[8] = old_far[4]
        self.face_ba[7] = old_far[3]
    
        # avant
        self.face_av[1] = old_fba[1]
        self.face_av[8] = old_fba[8]
        self.face_av[7] = old_fba[7]
        
        # on redessine le cube
        self.dessine()    
         
    def tourne_dr_plus(self,stocke_action,bt_undo):
        old_fdr = list(self.face_dr)
                     
        if stocke_action == 1:
            self.actions.append("D+")  
            bt_undo.config(state=NORMAL)
            print(self.actions)
        
        self.face_dr[1] = old_fdr[7]
        self.face_dr[2] = old_fdr[8]
        self.face_dr[3] = old_fdr[1]                
        self.face_dr[4] = old_fdr[2]
        self.face_dr[5] = old_fdr[3]
        self.face_dr[6] = old_fdr[4]
        self.face_dr[7] = old_fdr[5]
        self.face_dr[8] = old_fdr[6]  
                                    
        # haut 
        old_fha   = list(self.face_ha)
        self.face_ha[5] = self.face_av[5]
        self.face_ha[4] = self.face_av[4]
        self.face_ha[3] = self.face_av[3]
        
        # arriere
        old_far  = list(self.face_ar)
        self.face_ar[1] = old_fha[5]
        self.face_ar[8] = old_fha[4]
        self.face_ar[7] = old_fha[3]
        
        # bas
        old_fba   = list(self.face_ba)
        self.face_ba[3] = old_far[7]
        self.face_ba[4] = old_far[8]
        self.face_ba[5] = old_far[1]
        
        # avant
        self.face_av[3] = old_fba[3]
        self.face_av[4] = old_fba[4]
        self.face_av[5] = old_fba[5]
        
        # on redessine le cube
        self.dessine()  
        
    def tourne_dr_moins(self,stocke_action,bt_undo):
        old_fdr = list(self.face_dr)
                     
        if stocke_action == 1:
            self.actions.append("D-")             
            bt_undo.config(state=NORMAL)
            print(self.actions)
        
        self.face_dr[1] = old_fdr[3]
        self.face_dr[2] = old_fdr[4]
        self.face_dr[3] = old_fdr[5]                
        self.face_dr[4] = old_fdr[6]
        self.face_dr[5] = old_fdr[7]
        self.face_dr[6] = old_fdr[8]
        self.face_dr[7] = old_fdr[1]
        self.face_dr[8] = old_fdr[2]  
                                    
        # haut 
        old_fha   = list(self.face_ha)
        self.face_ha[5] = self.face_ar[1]
        self.face_ha[4] = self.face_ar[8]
        self.face_ha[3] = self.face_ar[7]
        
        # avant
        old_fav  = list(self.face_av)
        self.face_av[5] = old_fha[5]
        self.face_av[4] = old_fha[4]
        self.face_av[3] = old_fha[3]
        
        # bas 
        old_fba   = list(self.face_ba)
        self.face_ba[3] = old_fav[3]
        self.face_ba[4] = old_fav[4]
        self.face_ba[5] = old_fav[5]
        
        # arriere
        self.face_ar[1] = old_fba[5]
        self.face_ar[8] = old_fba[4]
        self.face_ar[7] = old_fba[3]
        
        # on redessine le cube
        self.dessine()    
         
    def tourne_ar_plus(self,stocke_action,bt_undo):
        old_far = list(self.face_ar)
        
        if stocke_action == 1:
            self.actions.append("AR+") 
            bt_undo.config(state=NORMAL)
            print(self.actions)
                     
        self.face_ar[1] = old_far[7]
        self.face_ar[2] = old_far[8]
        self.face_ar[3] = old_far[1]                
        self.face_ar[4] = old_far[2]
        self.face_ar[5] = old_far[3]
        self.face_ar[6] = old_far[4]
        self.face_ar[7] = old_far[5]
        self.face_ar[8] = old_far[6]  
                                    
        # haut
        old_fha   = list(self.face_ha)
        self.face_ha[1] = self.face_dr[3]
        self.face_ha[2] = self.face_dr[4]
        self.face_ha[3] = self.face_dr[5]
        
        # gauche
        old_fga  = list(self.face_ga)
        self.face_ga[7] = old_fha[1]
        self.face_ga[8] = old_fha[2]
        self.face_ga[1] = old_fha[3]
        
        # bas
        old_fba   = list(self.face_ba)
        self.face_ba[5] = old_fga[7]
        self.face_ba[6] = old_fga[8]
        self.face_ba[7] = old_fga[1]
        
        # droite
        self.face_dr[3] = old_fba[5]
        self.face_dr[4] = old_fba[6]
        self.face_dr[5] = old_fba[7]
        
        # on redessine le cube
        self.dessine()  
        
    def tourne_ar_moins(self,stocke_action,bt_undo):
        old_far = list(self.face_ar)

        if stocke_action == 1:
            self.actions.append("AR-")            
            bt_undo.config(state=NORMAL)
            print(self.actions)
                     
        self.face_ar[1] = old_far[3]
        self.face_ar[2] = old_far[4]
        self.face_ar[3] = old_far[5]                
        self.face_ar[4] = old_far[6]
        self.face_ar[5] = old_far[7]
        self.face_ar[6] = old_far[8]
        self.face_ar[7] = old_far[1]
        self.face_ar[8] = old_far[2]  
                                    
        # haut 
        old_fha   = list(self.face_ha)
        self.face_ha[3] = self.face_ga[1]
        self.face_ha[2] = self.face_ga[8]
        self.face_ha[1] = self.face_ga[7]
        
        # droite
        old_fdr  = list(self.face_dr)
        self.face_dr[5] = old_fha[3]
        self.face_dr[4] = old_fha[2]
        self.face_dr[3] = old_fha[1]
        
        # bas
        old_fba   = list(self.face_ba)
        self.face_ba[7] = old_fdr[5]
        self.face_ba[6] = old_fdr[4]
        self.face_ba[5] = old_fdr[3]
        
        # gauche
        self.face_ga[1] = old_fba[7]
        self.face_ga[8] = old_fba[6]
        self.face_ga[7] = old_fba[5]
        
        # on redessine le cube
        self.dessine()    
         
    def tourne_ha_plus(self, stocke_action,bt_undo):
        old_fha = list(self.face_ha)
                           
        if stocke_action == 1:
            self.actions.append("H+")                    
            bt_undo.config(state=NORMAL)
            print(self.actions)
        
        self.face_ha[1] = old_fha[7]
        self.face_ha[2] = old_fha[8]
        self.face_ha[3] = old_fha[1]                
        self.face_ha[4] = old_fha[2]
        self.face_ha[5] = old_fha[3]
        self.face_ha[6] = old_fha[4]
        self.face_ha[7] = old_fha[5]
        self.face_ha[8] = old_fha[6]  
                                    
        # arriere 
        old_far   = list(self.face_ar)
        self.face_ar[1] = self.face_ga[1]
        self.face_ar[2] = self.face_ga[2]
        self.face_ar[3] = self.face_ga[3]
        
        # droite
        old_fdr  = list(self.face_dr)
        self.face_dr[1] = old_far[1]
        self.face_dr[2] = old_far[2]
        self.face_dr[3] = old_far[3]
        
        # avant
        old_fav   = list(self.face_av)
        self.face_av[1] = old_fdr[1]
        self.face_av[2] = old_fdr[2]
        self.face_av[3] = old_fdr[3]
        
        # gauche
        self.face_ga[1] = old_fav[1]
        self.face_ga[2] = old_fav[2]
        self.face_ga[3] = old_fav[3]
        
        # on redessine le cube
        self.dessine()  
        
    def tourne_ha_moins(self, stocke_action, bt_undo):
        old_fha = list(self.face_ha)
        
        if stocke_action == 1:
            self.actions.append("H-")               
            bt_undo.config(state=NORMAL)
            print(self.actions)
        
        self.face_ha[1] = old_fha[3]
        self.face_ha[2] = old_fha[4]
        self.face_ha[3] = old_fha[5]                
        self.face_ha[4] = old_fha[6]
        self.face_ha[5] = old_fha[7]
        self.face_ha[6] = old_fha[8]
        self.face_ha[7] = old_fha[1]
        self.face_ha[8] = old_fha[2]  
                                    
        # arriere
        old_far   = list(self.face_ar)
        self.face_ar[3] = self.face_dr[3]
        self.face_ar[2] = self.face_dr[2]
        self.face_ar[1] = self.face_dr[1]
        
        # gauche
        old_fga  = list(self.face_ga)
        self.face_ga[3] = old_far[3]
        self.face_ga[2] = old_far[2]
        self.face_ga[1] = old_far[1]
        
        # avant
        old_fav   = list(self.face_av)
        self.face_av[3] = old_fga[3]
        self.face_av[2] = old_fga[2]
        self.face_av[1] = old_fga[1]
        
        # droit
        self.face_dr[3] = old_fav[3]
        self.face_dr[2] = old_fav[2]
        self.face_dr[1] = old_fav[1]
        
        # on redessine le cube
        self.dessine()    
         
    def tourne_ba_plus(self,stocke_action,bt_undo):
        old_fba = list(self.face_ba)
                          
        if stocke_action == 1:
            self.actions.append("B+")     
            bt_undo.config(state=NORMAL)
            print(self.actions)
        
        self.face_ba[1] = old_fba[7]
        self.face_ba[2] = old_fba[8]
        self.face_ba[3] = old_fba[1]                
        self.face_ba[4] = old_fba[2]
        self.face_ba[5] = old_fba[3]
        self.face_ba[6] = old_fba[4]
        self.face_ba[7] = old_fba[5]
        self.face_ba[8] = old_fba[6]  
                                    
        # avant
        old_fav   = list(self.face_av)
        self.face_av[5] = self.face_ga[5]
        self.face_av[6] = self.face_ga[6]
        self.face_av[7] = self.face_ga[7]
        
        # droite
        old_fdr  = list(self.face_dr)
        self.face_dr[7] = old_fav[7]
        self.face_dr[6] = old_fav[6]
        self.face_dr[5] = old_fav[5]
        
        # arriere
        old_far   = list(self.face_ar)
        self.face_ar[7] = old_fdr[7]
        self.face_ar[6] = old_fdr[6]
        self.face_ar[5] = old_fdr[5]
        
        # gauche
        self.face_ga[7] = old_far[7]
        self.face_ga[6] = old_far[6]
        self.face_ga[5] = old_far[5]
        
        # on redessine le cube
        self.dessine()  
        
    def tourne_ba_moins(self,stocke_action,bt_undo):
        old_fba = list(self.face_ba)
               
        if stocke_action == 1:
            self.actions.append("B-")             
            bt_undo.config(state=NORMAL)
            print(self.actions)
        
        self.face_ba[1] = old_fba[3]
        self.face_ba[2] = old_fba[4]
        self.face_ba[3] = old_fba[5]                
        self.face_ba[4] = old_fba[6]
        self.face_ba[5] = old_fba[7]
        self.face_ba[6] = old_fba[8]
        self.face_ba[7] = old_fba[1]
        self.face_ba[8] = old_fba[2]  
                                    
        # avant
        old_fav   = list(self.face_av)
        self.face_av[7] = self.face_dr[7]
        self.face_av[6] = self.face_dr[6]
        self.face_av[5] = self.face_dr[5]
        
        # gauche
        old_fga  = list(self.face_ga)
        self.face_ga[7] = old_fav[7]
        self.face_ga[6] = old_fav[6]
        self.face_ga[5] = old_fav[5]
        
        # arriere
        old_far   = list(self.face_ar)
        self.face_ar[7] = old_fga[7]
        self.face_ar[6] = old_fga[6]
        self.face_ar[5] = old_fga[5]
        
        # droite
        self.face_dr[7] = old_far[7]
        self.face_dr[6] = old_far[6]
        self.face_dr[5] = old_far[5]
        
        # on redessine le cube
        self.dessine()            
        
    def undo(self,bt_undo):        
              
        action=self.actions.pop()
        
        if action == "debut":
            self.actions.append("debut")
                        
        if action == "G+":
            self.tourne_ga_moins(0,bt_undo)

        if action == "G-":
            self.tourne_ga_plus(0,bt_undo)

        if action == "D+":
            self.tourne_dr_moins(0,bt_undo)

        if action == "D-":
            self.tourne_dr_plus(0,bt_undo)

        if action == "H+":
            self.tourne_ha_moins(0,bt_undo)

        if action == "H-":
            self.tourne_ha_plus(0,bt_undo)

        if action == "B+":
            self.tourne_ba_moins(0,bt_undo)

        if action == "B-":
            self.tourne_ba_plus(0,bt_undo)

        if action == "AV+":
            self.tourne_av_moins(0,bt_undo)

        if action == "AV-":
            self.tourne_av_plus(0,bt_undo)

        if action == "AR+":
            self.tourne_ar_moins(0,bt_undo)

        if action == "AR-":
            self.tourne_ar_plus(0,bt_undo)
        
        if action == "CV_G":
            self.change_vue_vers_droite(0,bt_undo)

        if action == "CV_D":
            self.change_vue_vers_gauche(0,bt_undo)

        if action == "CV_H":
            self.change_vue_vers_bas(0,bt_undo)

        if action == "CV_B":
            self.change_vue_vers_haut(0,bt_undo)

        print(self.actions)    
        
        if len(self.actions) == 1:
            bt_undo.config(state=DISABLED)
        
    
def sauve():
    myFormats = [ ('Rubix','*.rubix') ]
    nom_fichier = tkinter.filedialog.asksaveasfilename(parent=fenetre,initialdir="/tmp",filetypes=myFormats,title="Save the cube as...")
    if len(nom_fichier) > 0:
        mon_cube.save(nom_fichier)

def charge():
    myFormats = [ ('Rubix','*.rubix') ]
    fichier = tkinter.filedialog.askopenfile(parent=fenetre,initialdir="/tmp",mode='rb',filetypes=myFormats,title='Choose a cube file')        
    if fichier != None:
        mon_cube.load(fichier)

    
# -- main     
if __name__ == '__main__':

    fenetre = Tk()

    fenetre.title('Rubix')
    fenetre.geometry('900x1020+0+0')

    # frame de dessin
    frame_dessin=Frame(fenetre)
    frame_dessin.pack(side=TOP, fill=X)

    # Canvas pour dessin 2D du cube
    #my_canvas_2d=Canvas(frame_dessin, height=600, width=800, bg="black")        
    #my_canvas_2d.pack(side=LEFT)
    
    # Canvas pour dessin 3D du cube
    my_canvas_3d=Canvas(frame_dessin, height=900, width=900, bg="grey")        
    my_canvas_3d.pack(side=LEFT)
    
    # creation du cube
    mon_cube = rubix(my_canvas_3d)

    # frame de boutons
    frame_bt_quit=Frame(fenetre, height=40)
    frame_bt_quit.pack(side=TOP, fill=X)
   
    # bouton Quitter
    bt_quit=Button(frame_bt_quit, text="Quitter", bg="red", command=fenetre.quit)
    bt_quit.pack(side=LEFT, fill=X, padx=5, pady=5)
    
    # bouton Sauvegarder
    bt_save=Button(frame_bt_quit, text="Sauvegarder", bg="grey", command=sauve)
    bt_save.pack(side=LEFT, fill=X, padx=5, pady=5)
    
    # bouton Charger
    bt_load=Button(frame_bt_quit, text="Charger", bg="grey", command=charge)
    bt_load.pack(side=LEFT, fill=X, padx=5, pady=5)
    
    # bouton Undo
    bt_undo=Button(frame_bt_quit, text="UNDO", bg="grey")
    bt_undo.pack(side=LEFT, fill=X, padx=50, pady=5)
    bt_undo.config(state=DISABLED)
    bt_undo.config(command=  lambda: mon_cube.undo(bt_undo))   

    # Boutons
    Button(my_canvas_3d, command= lambda: mon_cube.tourne_ha_plus(1,bt_undo),  text="Haut -1 ---->").place(x=600,y=50)
    Button(my_canvas_3d, command= lambda: mon_cube.tourne_ha_moins(1,bt_undo), text="<---- Haut +1").place(x=200,y=50)
    Button(my_canvas_3d, command= lambda: mon_cube.tourne_ba_plus(1,bt_undo),  text="Bas +1 ----->").place(x=600,y=800)
    Button(my_canvas_3d, command= lambda: mon_cube.tourne_ba_moins(1,bt_undo), text="<----- Bas -1").place(x=200,y=800)
    
    Button(my_canvas_3d, command= lambda: mon_cube.tourne_ga_moins(1,bt_undo), text="^||||| Gauche -",wraplength=1).place(x=50,y=150)
    Button(my_canvas_3d, command= lambda: mon_cube.tourne_ga_plus(1,bt_undo),  text="Gauche + |||||V",wraplength=1).place(x=50,y=500)
    Button(my_canvas_3d, command= lambda: mon_cube.tourne_dr_moins(1,bt_undo), text="^||||| Droite -",wraplength=1).place(x=800,y=150)
    Button(my_canvas_3d, command= lambda: mon_cube.tourne_dr_plus(1,bt_undo),  text="Droite + |||||V",wraplength=1).place(x=800,y=500)
    
    Button(my_canvas_3d, command= lambda: mon_cube.tourne_av_plus(1,bt_undo),  text="Avant +1 ----->").place(x=400,y=420)
    Button(my_canvas_3d, command= lambda: mon_cube.tourne_av_moins(1,bt_undo), text="<----- Avant -1").place(x=400,y=370)    
    Button(my_canvas_3d, command= lambda: mon_cube.tourne_ar_plus(1,bt_undo),  text="Arriere +1 ----->").place(x=400,y=520)
    Button(my_canvas_3d, command= lambda: mon_cube.tourne_ar_moins(1,bt_undo), text="<----- Arriere -1").place(x=400,y=470)
    
    Button(my_canvas_3d, command= lambda: mon_cube.change_vue_vers_droite(1,bt_undo), text="=====>>").place(x=750,y=400)
    Button(my_canvas_3d, command= lambda: mon_cube.change_vue_vers_gauche(1,bt_undo), text="<<=====").place(x=50,y=400)
    Button(my_canvas_3d, command= lambda: mon_cube.change_vue_vers_haut(1,bt_undo),   text="^||||",wraplength=1).place(x=440,y=100)
    Button(my_canvas_3d, command= lambda: mon_cube.change_vue_vers_bas(1,bt_undo),    text="||||V",wraplength=1).place(x=440,y=750)
    
    # on dessine le cube
    mon_cube.dessine()
    
    fenetre.mainloop()