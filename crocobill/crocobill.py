#!/usr/bin/env python3
#
# -*- coding: utf-8 -*-
# --------------------------------------------------------------------------------------------------------------------------
# Ce programme est une version Python du jeu Crocobill de JP Munoz (1996, Windows 3.1)
#
# Ce programme utilise l'interface graphique Tkinter
#
# Auteur        : Christophe Pauliat
# Platformes    : Linux / Windows / MacOS
#
# IMPORTANT: Pour MacOS, utiliser Python3 et tkinter depuis https://python.org car le Tk fourni par Apple a des bugs
#            cf. https://www.python.org/download/mac/tcltk/
#
# Versions
#    2020-04-11: version initiale
#    2020-04-19: ajout affichage du bas et bouton quitter
# --------------------------------------------------------------------------------------------------------------------------
#
# TO DO: remettre focus sur fenetre principale apres fermeture d'une fenetre messagebox
#
# ---------- modules
import tkinter 
import tkinter.messagebox
import tkinter.font
import math
import random
import time

# ---------- couleurs
couleur_fond = "#404050"
#couleur_labels = "#00F000"
couleur_labels = "#FF0080"

# ---------- paramètres initiaux
taille_case = 32
niveau_actuel = 1
niveau_dernier = 3
nb_vies_restantes = 3
croco_dir = "G"         # le croco regarde a gauche

# ---------- Niveaux

niveau_string = []
niveau_nb_x = []
niveau_nb_y = []

# niveau 1
niveau_nb_x.append (22)
niveau_nb_y.append (16)
niveau_string.append("MMMMMMMMMMMMMMMMMMMMMM" + \
                     "MHHHHHHHHHHHHHHHHHHHHM" + \
                     "MHHHHHHCHHHHHRHHHHRHHM" + \
                     "MHHHHHHHHHHHHHHHHHHHHM" + \
                     "MHHHHHRHRHRHRHHHHRHHHM" + \
                     "MHHHHHHHHHHHHHHHHRHHHM" + \
                     "MHHHHHRRRHHHHHHOHHRHHM" + \
                     "MHHHHHRORHHHHHHHHRHHHM" + \
                     "MHHHHHRRRHHHHHHHHRHHHM" + \
                     "MHHHHHHHOHHHHHHHHRHHHM" + \
                     "MMMMMMMMMMMMMMHHHRHHHM" + \
                     "MHHHHHHHHHHHHHHHHRHHHM" + \
                     "MHHHHHHHHHHHHHHHOHHHHM" + \
                     "MHHHHHHHHHHMMMMMMMMMMM" + \
                     "MHHHHHHOHHHHHHHHHHHHOM" + \
                     "MMMMMMMMMMMMMMMMMMMMMM")

# niveau 2
niveau_nb_x.append (22)
niveau_nb_y.append (20)
niveau_string.append("MMMMMMMMMMMMMMMMMMMMMM" + \
                     "MCHHHHHHHHHHHHHHHHHHHM" + \
                     "MHMMMMMMMMMMMMMMMMMMHM" + \
                     "MHMHHHHHHHHHHHHHHHHMHM" + \
                     "MHMHMMMMMMMMMMMMMMHMHM" + \
                     "MHMHMHRHRHRHHHHHHMHMHM" + \
                     "MHMHMHHHHHHHHHHHHMHMHM" + \
                     "MHMHMRRHHHHHHHHOHMRMHM" + \
                     "MHMHMOOHMMMMMMHHHMHHHM" + \
                     "MHMHMHRHMHHHHMHHHMVMHM" + \
                     "MHMHRVOHMHOHHMHHHMVMHM" + \
                     "MHMHMVHHMMMMHMHHHMHMHM" + \
                     "MHMHMVHHHOHHHMHHHMHMHM" + \
                     "MHMHMHHMMMMMMMOHHMHMHM" + \
                     "MHMHMHHHHHHHHHHHHMHMHM" + \
                     "MHMHMMMMMMMMOMMMMMHMHM" + \
                     "MHMHHHHHHHHHHHHHHHHMHM" + \
                     "MHMMMMMMRMMMMMMMMMMMHM" + \
                     "MHHHHHHHHHHHHHHHHHHHHM" + \
                     "MMMMMMMMMMMMMMMMMMMMMM")

# niveau 3
niveau_nb_x.append (40)
niveau_nb_y.append (20)
niveau_string.append("MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM" + \
                     "MCHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHM" + \
                     "MHMMMMMMMMMMMMMMMMHMMHMMMMMMMMMMMMMMMMHM" + \
                     "MHMHHHHHHHHHHHHHHMHMMHMHHHHHHHHHHHHHHMHM" + \
                     "MHMHMMMMMMMMMMMMHMHMMHMHMMMMMMMMMMMMHMHM" + \
                     "MHMHMHRHRHRHHHHMHMHMMHMHMHRHRHRHHHHMHMHM" + \
                     "MHMHMHHHHHHHHHHMHMHMMHMHMHHHHHHHHHHMHMHM" + \
                     "MHMHMRRHHHHHHOHMRMHMMHMHMRRHHHHHHOHMRMHM" + \
                     "MHMHMOOHMMMMMMHMHHHMMHMHMOOHMMMMMMHMHHHM" + \
                     "MHMHMHRHMHHHHMHMVMHMMHMHMHRHMHHHHMHMVMHM" + \
                     "MHMHRVOHMHOHHMHMVMHMMHMHRVOHMHOHHMHMVMHM" + \
                     "MHMHMVHHMMMMHMHMHMHMMHMHMVHHMMMMHMHMHMHM" + \
                     "MHMHMVHHHOHHHMHMHMHMMHMHMVHHHOHHHMHMHMHM" + \
                     "MHMHMHHMMMMMMMOMHMHMMHMHMHHMMMMMMMOMHMHM" + \
                     "MHMHMHHHHHHHHHHMHMHMMHMHMHHHHHHHHHHMHMHM" + \
                     "MHMHMMMMMMMMOMMMHMHMMHMHMMMMMMMMOMMMHMHM" + \
                     "MHMHHHHHHHHHHHHHHMHMMHMHHHHHHHHHHHHHHMHM" + \
                     "MHMMMMMMRMMMMMMMMMHMMHMMMMMMRMMMMMMMMMHM" + \
                     "MHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHM" + \
                     "MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM")

# ---------- functions

# ---- initialise le tableau
def init_tableau(niv):
    global tableau
    global nb_x
    global nb_y
    global nb_oeufs_restants
    global croco_x
    global croco_y

    # on positionne les paramètres du niveau
    nb_x = niveau_nb_x[niv-1]
    nb_y = niveau_nb_y[niv-1]
    init_string = niveau_string[niv-1] 

    # cree le tableau vide
    tableau = []
    for i in range(nb_x):
        tableau.append(["vide"] * nb_y)

    # initialise chaque case du tableau suivant la chaine du niveau
    abb = "VMHROC"
    cases = [ "vide", "mur", "herbe", "rocher", "oeuf", "croco"]
    nb_oeufs_restants = 0

    p = 0
    for y in range(nb_y):
        for x in range(nb_x):
            pos = abb.find(init_string[p])
            if pos == -1:
                print ("ERREUR INITIALISATION !")
                exit (1)
            else:
                tableau[x][y] = cases[pos]
                if tableau[x][y] == "oeuf": nb_oeufs_restants += 1
                elif tableau[x][y] == "croco":
                    croco_x = x
                    croco_y = y
            p += 1 

# ---- dessin initial du tableau
def dessine_croco(x,y):
    global canvas_dessin
    global taille_case
    global image_croco_g
    global image_croco_d
    global croco_dir
    #canvas_dessin.create_rectangle(x * taille_case, y * taille_case, (x + 1) * taille_case, (y + 1) * taille_case, fill="red")
    if croco_dir == "G":
        canvas_dessin.create_image(x * taille_case, y * taille_case, anchor=tkinter.NW, image=image_croco_g)
    else:
        canvas_dessin.create_image(x * taille_case, y * taille_case, anchor=tkinter.NW, image=image_croco_d)
    
def dessine_croco_mort(x,y):
    global canvas_dessin
    global taille_case
    global image_mort
    canvas_dessin.create_rectangle(x * taille_case, y * taille_case, (x + 1) * taille_case, (y + 1) * taille_case, fill="red")
    canvas_dessin.create_image(x * taille_case, y * taille_case, anchor=tkinter.NW, image=image_croco_mort)

def dessine_mur(x,y):
    global canvas_dessin
    global taille_case
    global image_mur
    #canvas_dessin.create_rectangle(x * taille_case, y * taille_case, (x + 1) * taille_case, (y + 1) * taille_case, fill="#404040")
    canvas_dessin.create_image(x * taille_case, y * taille_case, anchor=tkinter.NW, image=image_mur)

def dessine_herbe(x,y):
    global canvas_dessin
    global taille_case
    global image_herbe
    #canvas_dessin.create_rectangle(x * taille_case, y * taille_case, (x + 1) * taille_case, (y + 1) * taille_case, fill="green")
    canvas_dessin.create_image(x * taille_case, y * taille_case, anchor=tkinter.NW, image=image_herbe)

def dessine_rocher(x,y):
    global canvas_dessin
    global taille_case
    global image_rocher
    #canvas_dessin.create_oval(x * taille_case, y * taille_case, (x + 1) * taille_case, (y + 1) * taille_case, fill="grey")
    canvas_dessin.create_image(x * taille_case, y * taille_case, anchor=tkinter.NW, image=image_rocher)

def dessine_oeuf(x,y):
    global canvas_dessin
    global taille_case
    global image_oeuf
    canvas_dessin.create_image(x * taille_case, y * taille_case, anchor=tkinter.NW, image=image_oeuf)

def dessine_vide(x,y):
    global canvas_dessin
    global taille_case
    canvas_dessin.create_rectangle(x * taille_case, y * taille_case, (x + 1) * taille_case, (y + 1) * taille_case, fill="black")

def dessine_tableau():
    global nb_x
    global nb_y
    global taille_case
    global canvas_dessin
    global label_niveau
    global label_nb_oeufs
    global label_nb_vies
    global niveau_actuel
    global nb_vies_restantes
    global nb_oeufs_restants

    # Dimensionne le canvas à la valeur nécessaire au niveau actuel
    canvas_dessin.config(width=taille_case*nb_x, height=taille_case*nb_y)

    # dessine chaque case du tableau
    for x in range(nb_x):
        for y in range(nb_y):
            if tableau[x][y] == "croco":  
                dessine_croco(x,y)
            if tableau[x][y] == "mur":  
                dessine_mur(x,y)
            elif tableau[x][y] == "herbe":  
                dessine_herbe(x,y)
            elif tableau[x][y] == "rocher":  
                dessine_rocher(x,y)
            elif tableau[x][y] == "oeuf":  
                dessine_oeuf(x,y)
            elif tableau[x][y] == "vide":  
                dessine_vide(x,y)

    # on affiche le numéro du niveau
    label_niveau.config(text="Niveau {:d}".format(niveau_actuel))

    # on affiche le nombre d'oeufs restants
    label_nb_oeufs.config(text="Oeufs restants: {:d}".format(nb_oeufs_restants))

    # on affiche le nombre de vies restantes
    label_nb_vies.config(text="Vies restantes: {:d}".format(nb_vies_restantes))

# ---- le croco attrape une oeuf
def attrape_oeuf():
    global nb_oeufs_restants
    global fenetre
    global label_nb_oeufs
    global canvas_dessin
    global taille_case
    global croco_x
    global croco_y

    # on décremente le nombre d'oeufs restants
    nb_oeufs_restants -= 1
    label_nb_oeufs.config(text="Oeufs restants: {:d}".format(nb_oeufs_restants))

    # Effet visuel: MIAM !!
    text = canvas_dessin.create_text (croco_x * taille_case, croco_y * taille_case, text="MIAM !!", fill="red", font=tkinter.font.Font(family='Arial', size=32))
    fenetre.update()
    time.sleep(0.5)
    canvas_dessin.delete(text)

    # si c'était le dernier oeuf, on a réussi ce niveau
    if nb_oeufs_restants == 0:
        gagne()

# ---- C'est gagne: Le croco a mange tous les oeufs du niveau
# http://tkinter.fdex.eu/doc/popdial.html
def gagne():
    global niveau_actuel
    global niveau_dernier
    global fenetre
    if niveau_actuel < niveau_dernier:
        tkinter.messagebox.showinfo("Gagné","Bravo ! Vous avez réussi le niveau {:d}. \n\nCliquer OK pour passer au niveau suivant".format(niveau_actuel))
        niveau_actuel += 1
        init_tableau(niveau_actuel)
        dessine_tableau()
        #fenetre.focus_set()     # on met le focus la fenetre principale pour éviter de devoir cliquer dans la fenetre avant de jouer
    else:
        tkinter.messagebox.showinfo("Gagné","Bravo ! Vous avez réussi le dernier niveau\n\nCliquer OK pour sortir du programme")
        exit (0)

# ---- deplacement du croco
def bouge(event):
    global croco
    global canvas_dessin
    global fenetre
    global croco_x
    global croco_y
    global nb_x
    global nb_x
    global taille_case
    global croco_dir

    croco_bouge = False
    bouge_rocher = False
    rocher_va_tomber = False
    oeuf_attrape = False
    croco_x_old = croco_x
    croco_y_old = croco_y

    #print ("KEY PRESSED")

    # le croco essaie de bouger sur la gauche
    if event.keysym == 'Left' and croco_x > 0:
        croco_dir = "G"
        # on bouge si la case destination contient de l'herbe, une oeuf, du vide ou un rocher sans rien derriere
        if tableau[croco_x-1][croco_y] in [ "herbe", "oeuf", "vide" ] or \
           (croco_x-2 >= 0 and tableau[croco_x-1][croco_y] == "rocher" and tableau[croco_x-2][croco_y] == "vide"): 
            croco_bouge = True
            if tableau[croco_x-1][croco_y] == "oeuf": 
                oeuf_attrape = True
            elif tableau[croco_x-1][croco_y] == "rocher": 
                bouge_rocher = True
                rocher_x = -2
            # si le croco a un rocher au dessus de lui, ce rocher va tomber apres que le croco ait bouge
            if croco_y-1 >= 0 and tableau[croco_x][croco_y-1] == "rocher":
                rocher_va_tomber = True
                rx = croco_x
                ry = croco_y-1
            croco_x = croco_x - 1
 
    # le croco essaie de bouger sur la droite
    elif event.keysym == 'Right' and croco_x < nb_x - 1:
        croco_dir = "D"
        # on bouge si la case destination contient de l'herbe, une oeuf, du vide ou un rocher sans rien derriere
        if tableau[croco_x+1][croco_y] in [ "herbe", "oeuf", "vide" ] or \
           (croco_x+2 <= nb_x-1 and tableau[croco_x+1][croco_y] == "rocher" and tableau[croco_x+2][croco_y] == "vide"): 
            croco_bouge = True
            if tableau[croco_x+1][croco_y] == "oeuf": 
                oeuf_attrape = True
            elif tableau[croco_x+1][croco_y] == "rocher": 
                bouge_rocher = True
                rocher_x = 2
            # si le croco a un rocher au dessus de lui, ce rocher va tomber apres que le croco ait bouge
            if croco_y-1 >= 0 and tableau[croco_x][croco_y-1] == "rocher":
                rocher_va_tomber = True
                rx = croco_x
                ry = croco_y-1
            croco_x = croco_x + 1
 
    # le croco essaie de bouger vers le haut
    elif event.keysym == 'Up' and croco_y > 0:
        # on bouge si la case destination contient de l'herbe, une oeuf ou du vide
        if tableau[croco_x][croco_y-1] in [ "herbe", "oeuf", "vide" ]:
            croco_bouge = True
            if tableau[croco_x][croco_y-1] == "oeuf": 
                oeuf_attrape = True
            croco_y = croco_y - 1
 
    # le croco essaie de bouger vers le bas
    elif event.keysym == 'Down' and croco_y < nb_y - 1:
        # on bouge si la case destination contient de l'herbe, une oeuf ou du vide
        if tableau[croco_x][croco_y+1] in [ "herbe", "oeuf", "vide" ]:
            croco_bouge = True
            if tableau[croco_x][croco_y+1] == "oeuf": 
                oeuf_attrape = True
            # si le croco a un rocher au dessus de lui, ce rocher va tomber apres que le croco ait bouge
            if croco_y-1 >= 0 and tableau[croco_x][croco_y-1] == "rocher":
                rocher_va_tomber = True
                rx = croco_x
                ry = croco_y-1
            croco_y = croco_y + 1

    # si on a bouge, on met a jour l'affichage
    if croco_bouge:

        # on dessine une case vide à l'ancienne position du croco
        dessine_vide(croco_x_old, croco_y_old)
        tableau[croco_x_old][croco_y_old] = "vide"

        # on affiche le croco à sa nouvelle position
        dessine_croco(croco_x, croco_y)
        tableau[croco_x][croco_y] = "croco"

        # update display
        fenetre.update()

        # si le croco a poussé un rocher sur une case vide, on affiche le rocher
        if bouge_rocher:
            dessine_rocher(croco_x_old+rocher_x, croco_y_old)
            tableau[croco_x_old+rocher_x][croco_y_old] = "rocher"
            rocher_tombe(croco_x_old+rocher_x, croco_y_old, False)
        
        # si le croco avait un rocher au dessus de lui avant de bouger, ce rocher va tomber
        if rocher_va_tomber:
            rocher_tombe(rx,ry,False)

        # si le croco a attrapé un oeuf
        if oeuf_attrape:
            attrape_oeuf()
        
# ---- On teste si le rocher peut tomber (si vide sous le rocher)
def rocher_tombe(x,y,rocher_en_train_de_tomber):
    global fenetre

    fenetre.update()
    if y+1 < nb_y and tableau[x][y+1] == "vide":
        # delai pour voir l'animation du rocher qui tombe
        time.sleep (0.3)

        # le rocher tombe d'une case
        dessine_vide(x, y)
        tableau[x][y] = "vide"

        dessine_rocher(x, y+1)
        tableau[x][y+1] = "rocher"

        # on regarde s'il y avait un autre rocher sur le rocher qui vient de tomber
        # si oui, cet autre rocher tombe aussi
        if y-1 >= 0 and tableau[x][y-1] == "rocher":
            rocher_tombe(x,y-1,False)

        # on teste si le 1er rocher peut encore tomber
        rocher_tombe(x,y+1,True)

    # si le rocher est deja tombe d'au moins une case et que le croco est juste dessus, 
    # le croco se fait ecraser et perd une vie
    if rocher_en_train_de_tomber and y+1 < nb_y and tableau[x][y+1] == "croco":
        dessine_croco_mort(x,y+1)
        fenetre.update()
        croco_perd_une_vie()

# ----- le croco perf une vie
def croco_perd_une_vie():
    global niveau_actuel
    global niveau_dernier
    global nb_vies_restantes
    global fenetre

    # on décremente le nombre de vies restantes
    nb_vies_restantes -= 1
    label_nb_vies.config(text="Vies restantes: {:d}".format(nb_vies_restantes))
    fenetre.update()

    if nb_vies_restantes >= 1:
        message = "Aie ! \nLe croco s'est pris un rocher sur la tête\net a perdu une vie. \n\nCliquer OK pour recommencer ce niveau\n\n"
        if nb_vies_restantes > 1: 
            message = message + "Il reste {:d} vies.".format(nb_vies_restantes)
        else:
            message = message + "ATTENTION, il reste 1 seule vie."

        tkinter.messagebox.showinfo("Une vie perdue", message)
        init_tableau(niveau_actuel)
        dessine_tableau()
        #fenetre.focus_set()     # on met le focus la fenetre principale pour éviter de devoir cliquer dans la fenetre avant de jouer
    else:
        tkinter.messagebox.showinfo("Perdu","Le croco a perdu toutes ses vies.\n\nCliquer OK pour sortir du programme")
        exit (2)    

# ---- On recommence le niveau actuel après confirmation
def recommencer():
    global niveau_actuel

    if tkinter.messagebox.askyesno("On recommence","Voulez-vous vraiment recommencer le niveau actuel ?"): 
        init_tableau(niveau_actuel)
        dessine_tableau()

# ---- Fin du programme après confirmation
def quitter():
    if tkinter.messagebox.askyesno("Fin du programme","Voulez-vous vraiment quitter le jeu ?"): 
        fenetre.destroy()

# ---------- programme principal
if __name__ == '__main__':

    # ---- fenêtre principale
    fenetre = tkinter.Tk()
    fenetre.title('Crocobill')
    fenetre.config(bg=couleur_fond)
    fenetre.resizable(width=False, height=False)    # on empeche le redimensionnement manuel de la fenetre

    # ---- canvas pour dessiner
    canvas_dessin = tkinter.Canvas(fenetre, bg="black", highlightthickness=0)
    canvas_dessin.pack(padx=20, pady=20)

    # ---- Charge les images GIF
    image_mur        = tkinter.PhotoImage(file="images/mur.gif")
    image_herbe      = tkinter.PhotoImage(file="images/herbe.gif")
    image_rocher     = tkinter.PhotoImage(file="images/rocher.gif")
    image_oeuf       = tkinter.PhotoImage(file="images/oeuf.gif")
    image_croco_g    = tkinter.PhotoImage(file="images/croco-gauche.gif")
    image_croco_d    = tkinter.PhotoImage(file="images/croco-droit.gif")
    image_croco_mort = tkinter.PhotoImage(file="images/croco-mort.gif")

    # ---- Initialise le tableau 
    init_tableau(niveau_actuel)

    # ---- Une frame en bas pour afficher des infos et bouton quitter
    frame_bas = tkinter.Frame(fenetre, bg=couleur_fond)
    frame_bas.pack(fill=tkinter.X, padx=20, pady=0)

    #relief=tkinter.RIDGE, 
    label_niveau = tkinter.Label(frame_bas, text="", font=tkinter.font.Font(family='Arial', size=20), bg=couleur_fond, fg=couleur_labels)
    label_niveau.grid(row=0, column=0, padx=5, pady=0)

    label_nb_oeufs = tkinter.Label(frame_bas, text="", font=tkinter.font.Font(family='Arial', size=20), bg=couleur_fond, fg=couleur_labels)
    label_nb_oeufs.grid(row=0, column=1, padx=5, pady=0)

    label_nb_vies = tkinter.Label(frame_bas, text="", font=tkinter.font.Font(family='Arial', size=20), bg=couleur_fond, fg=couleur_labels)
    label_nb_vies.grid(row=0, column=2, padx=5, pady=0)

    boutton_recommencer = tkinter.Button(frame_bas, text=" Recommencer ", font=tkinter.font.Font(family='Arial', size=20), bg=couleur_fond, fg="black", command=recommencer)
    boutton_recommencer.grid(row=0, column=3, padx=5, pady=0)

    boutton_quitter = tkinter.Button(frame_bas, text=" Quitter ", font=tkinter.font.Font(family='Arial', size=20), bg=couleur_fond, fg="black", command=quitter)
    boutton_quitter.grid(row=0, column=4, padx=5, pady=0)

    frame_bas.columnconfigure(0, weight=1)
    frame_bas.columnconfigure(1, weight=1)
    frame_bas.columnconfigure(2, weight=1)
    frame_bas.columnconfigure(3, weight=1)
    frame_bas.columnconfigure(4, weight=1)

    # juste pour afficher un espace sous la frame précédente
    tkinter.Frame(fenetre, bg=couleur_fond).pack(fill=tkinter.X, padx=20, pady=10)

    # ---- On affiche le tableau à l'écran
    dessine_tableau()

    # ---- Appelle la fonction bouge si l'utilisateur presse une touche
    fenetre.bind("<KeyPress>", bouge)

    # ---- Boucle de la fenetre graphique
    fenetre.mainloop()
