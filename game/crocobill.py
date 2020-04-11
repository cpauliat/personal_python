#!/usr/bin/env python3
#
# -*- coding: utf-8 -*-
# --------------------------------------------------------------------------------------------------------------------------
# Ce programme est une version Python du programme Crocobill de JP Munoz (1996)
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
#    2020-04-11: version initiale
# --------------------------------------------------------------------------------------------------------------------------
#
# TO DO: afficher nb de vies restantes
#
# ---------- modules
import tkinter 
import tkinter.messagebox
import math
import random
import time

# ---------- paramètres initiaux
box_size = 32
niveau_actuel = 1
niveau_dernier = 3
nb_vies_restantes = 3

# ---------- Niveaux

niveau_string = []
niveau_nb_x = []
niveau_nb_y = []

# niveau 1
niveau_nb_x.append (20)
niveau_nb_y.append (20)
niveau_string.append("MMMMMMMMMMMMMMMMMMMM" + \
                     "MHHHHHHHHHHHHHHHHHHM" + \
                     "MHHHHHHHHHHHHHHHHHHM" + \
                     "MHHHHCHHHHHRHHHHRHHM" + \
                     "MHHHHHHHHHHHHHHHHHHM" + \
                     "MHHHRHRHRHRHHHHRHHHM" + \
                     "MHHHHHHHHHHHHHHRHHHM" + \
                     "MHHHRRRHHHHHHOHHRHHM" + \
                     "MHHHRORHHHHHHHHRHHHM" + \
                     "MHHHRRRHHHHHHHHRHHHM" + \
                     "MHHHHHOHHHHHHHHRHHHM" + \
                     "MHHHHHHHHHHHHHHRHHHM" + \
                     "MHHHHHHHHHHHHHHRHHHM" + \
                     "MHHHHHHHHHHHHHOHHHHM" + \
                     "MHHHHHHHHHHHHHHHHHHM" + \
                     "MHHHHOHHHHHHHHHHHHHM" + \
                     "MHHHHHHHHHHHHHHHHHHM" + \
                     "MHHHHHHHHHVVVVVVVVVM" + \
                     "MHHHHHHHHHHHHHHHHHHM" + \
                     "MMMMMMMMMMMMMMMMMMMM")

# niveau 2
niveau_nb_x.append (20)
niveau_nb_y.append (20)
niveau_string.append("MMMMMMMMMMMMMMMMMMMM" + \
                     "MCHHHHHHHHHHHHHHHHHM" + \
                     "MHMMMMMMMMMMMMMMMMHM" + \
                     "MHMHHHHHHHHHHHHHHMHM" + \
                     "MHMHMMMMMMMMMMMMHMHM" + \
                     "MHMHMHRHRHRHHHHMHMHM" + \
                     "MHMHMHHHHHHHHHHMHMHM" + \
                     "MHMHMRRHHHHHHOHMRMHM" + \
                     "MHMHMOOHMMMMMMHMHHHM" + \
                     "MHMHMHRHMHHHHMHMVMHM" + \
                     "MHMHRVOHMHOHHMHMVMHM" + \
                     "MHMHMVHHMMMMHMHMHMHM" + \
                     "MHMHMVHHHOHHHMHMHMHM" + \
                     "MHMHMHHMMMMMMMOMHMHM" + \
                     "MHMHMHHHHHHHHHHMHMHM" + \
                     "MHMHMMMMMMMMOMMMHMHM" + \
                     "MHMHHHHHHHHHHHHHHMHM" + \
                     "MHMMMMMMRMMMMMMMMMHM" + \
                     "MHHHHHHHHHHHHHHHHHHM" + \
                     "MMMMMMMMMMMMMMMMMMMM")

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
    global drawing_canvas
    global box_size
    global image_croco_g
    global image_croco_d
    global croco_dir
    #drawing_canvas.create_rectangle(x * box_size, y * box_size, (x + 1) * box_size, (y + 1) * box_size, fill="red")
    if croco_dir == "G":
        drawing_canvas.create_image(x * box_size, y * box_size, anchor=tkinter.NW, image=image_croco_g)
    else:
        drawing_canvas.create_image(x * box_size, y * box_size, anchor=tkinter.NW, image=image_croco_d)
    
def dessine_croco_mort(x,y):
    global drawing_canvas
    global box_size
    global image_mort
    drawing_canvas.create_rectangle(x * box_size, y * box_size, (x + 1) * box_size, (y + 1) * box_size, fill="red")
    drawing_canvas.create_image(x * box_size, y * box_size, anchor=tkinter.NW, image=image_croco_mort)

def dessine_mur(x,y):
    global drawing_canvas
    global box_size
    global image_mur
    #drawing_canvas.create_rectangle(x * box_size, y * box_size, (x + 1) * box_size, (y + 1) * box_size, fill="#404040")
    drawing_canvas.create_image(x * box_size, y * box_size, anchor=tkinter.NW, image=image_mur)

def dessine_herbe(x,y):
    global drawing_canvas
    global box_size
    global image_herbe
    #drawing_canvas.create_rectangle(x * box_size, y * box_size, (x + 1) * box_size, (y + 1) * box_size, fill="green")
    drawing_canvas.create_image(x * box_size, y * box_size, anchor=tkinter.NW, image=image_herbe)

def dessine_rocher(x,y):
    global drawing_canvas
    global box_size
    global image_rocher
    #drawing_canvas.create_oval(x * box_size, y * box_size, (x + 1) * box_size, (y + 1) * box_size, fill="grey")
    drawing_canvas.create_image(x * box_size, y * box_size, anchor=tkinter.NW, image=image_rocher)

def dessine_oeuf(x,y):
    global drawing_canvas
    global box_size
    global image_oeuf
    #bs2 = box_size // 2
    #bsl = box_size // 2.5
    #bsc = box_size // 5.5
    #x0 = x * box_size + bs2 + 1
    #y0 = y * box_size + bs2 + 2
    #x1 = int (x0 + bsl * math.cos(90 * math.pi / 180))
    #y1 = int (y0 - bsl * math.sin(90 * math.pi / 180))
    #x2 = int (x0 + bsc * math.cos(126 * math.pi / 180))
    #y2 = int (y0 - bsc * math.sin(126 * math.pi / 180))
    #x3 = int (x0 + bsl * math.cos(162 * math.pi / 180))
    #y3 = int (y0 - bsl * math.sin(162 * math.pi / 180))
    #x4 = int (x0 + bsc * math.cos(198 * math.pi / 180))
    #y4 = int (y0 - bsc * math.sin(198 * math.pi / 180))
    #x5 = int (x0 + bsl * math.cos(234 * math.pi / 180))
    #y5 = int (y0 - bsl * math.sin(234 * math.pi / 180))
    #x6 = int (x0 + bsc * math.cos(270 * math.pi / 180))
    #y6 = int (y0 - bsc * math.sin(270 * math.pi / 180))
    #x7 = int (x0 + bsl * math.cos(306 * math.pi / 180))
    #y7 = int (y0 - bsl * math.sin(306 * math.pi / 180))
    #x8 = int (x0 + bsc * math.cos(342 * math.pi / 180))
    #y8 = int (y0 - bsc * math.sin(342 * math.pi / 180))
    #x9 = int (x0 + bsl * math.cos(18  * math.pi / 180))
    #y9 = int (y0 - bsl * math.sin(18  * math.pi / 180))
    #x10= int (x0 + bsc * math.cos(54  * math.pi / 180))
    #y10= int (y0 - bsc * math.sin(54  * math.pi / 180))
    #drawing_canvas.create_oval(x * box_size, y * box_size, (x + 1) * box_size, (y + 1) * box_size, fill="orange")
    #drawing_canvas.create_polygon(x1,y1, x2,y2, x3,y3, x4,y4, x5,y5, x6,y6, x7,y7, x8,y8, x9,y9, x10,y10, fill="yellow")
    drawing_canvas.create_image(x * box_size, y * box_size, anchor=tkinter.NW, image=image_oeuf)

def dessine_vide(x,y):
    global drawing_canvas
    global box_size
    drawing_canvas.create_rectangle(x * box_size, y * box_size, (x + 1) * box_size, (y + 1) * box_size, fill="black")

def dessine_tableau():
    global nb_x
    global nb_y
    global box_size
    global main_window
    global drawing_canvas

    # Dimensionne le canvas à la valeur nécessaire au niveau actuel
    drawing_canvas.config(width=box_size*nb_x, height=box_size*nb_y)

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

    main_window.update()
    time.sleep(5)


# ---- le croco attrape une oeuf
def attrape_oeuf():
    global nb_oeufs_restants

    nb_oeufs_restants -= 1
    # TO DO: rajouter un son ou effet visuel
    #print ("oeuf attrape ! reste {:d} oeufs".format(nb_oeufs_restants))

    if nb_oeufs_restants == 0:
        # C'est gagne
        gagne()

# ---- C'est gagne: Le croco a mange tous les oeufs du niveau
# http://tkinter.fdex.eu/doc/popdial.html
def gagne():
    global niveau_actuel
    global niveau_dernier
    global main_window
    if niveau_actuel < niveau_dernier:
        tkinter.messagebox.showinfo("Gagné","Bravo ! Vous avez réussi le niveau {:d}. \n\nCliquer OK pour passer au niveau suivant".format(niveau_actuel))
        niveau_actuel += 1
        init_tableau(niveau_actuel)
        dessine_tableau()
        main_window.title('Crocobill: niveau '+str(niveau_actuel))
        main_window.update()
    else:
        tkinter.messagebox.showinfo("Gagné","Bravo ! Vous avez réussi le dernier niveau\n\nCliquer OK pour sortir du programme")
        exit (0)

# ---- deplacement du croco
def move(event):
    global croco
    global drawing_canvas
    global main_window
    global croco_x
    global croco_y
    global nb_x
    global nb_x
    global box_size
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

        # delete croco in previous position
        # drawing_canvas.delete(croco)

        # draw empty space in the previous location of croco
        dessine_vide(croco_x_old, croco_y_old)
        tableau[croco_x_old][croco_y_old] = "vide"

        # display croco in new position
        dessine_croco(croco_x, croco_y)
        tableau[croco_x][croco_y] = "croco"

        # update display
        main_window.update()

        # si le croco a pousse un rocher sur une case vide, on affiche le rocher
        if bouge_rocher:
            dessine_rocher(croco_x_old+rocher_x, croco_y_old)
            tableau[croco_x_old+rocher_x][croco_y_old] = "rocher"
            rocher_tombe(croco_x_old+rocher_x, croco_y_old, False)
        
        # si le croco avait un rocher au dessus de lui avant de bouger, ce rocher va tomber
        elif rocher_va_tomber:
            rocher_tombe(rx,ry,False)

        if oeuf_attrape:
            attrape_oeuf()
        
# ---- On teste si le rocher peut tomber (si vide sous le rocher)
def rocher_tombe(x,y,rocher_en_train_de_tomber):
    global main_window

    main_window.update()
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
        main_window.update()
        croco_perd_une_vie()

# ----- le croco perf une vie
def croco_perd_une_vie():
    global niveau_actuel
    global niveau_dernier
    global nb_vies_restantes

    nb_vies_restantes -= 1

    if nb_vies_restantes >= 1:
        message = "Aie ! \nLe croco s'est pris un rocher sur la tête\net a perdu une vie. \n\nCliquer OK pour recommencer ce niveau\n\n"
        if nb_vies_restantes > 1: 
            message = message + "Il reste {:d} vies.".format(nb_vies_restantes)
        else:
            message = message + "ATTENTION, il reste 1 seule vie."

        tkinter.messagebox.showinfo("Une vie perdu", message)
        init_tableau(niveau_actuel)
        dessine_tableau()
    else:
        tkinter.messagebox.showinfo("Perdu","Le croco a perdu toutes ses vies.\n\nCliquer OK pour sortir du programme")
        exit (2)    

# ---------- programme principal
if __name__ == '__main__':

    # ---- Main Window
    main_window = tkinter.Tk()
    main_window.title('Crocobill: niveau '+str(niveau_actuel))

    # ---- Drawing canvas
    drawing_frame = tkinter.Frame(main_window)
    drawing_frame.pack(side=tkinter.LEFT, padx=0, pady=0)

    drawing_canvas = tkinter.Canvas(drawing_frame, bg="black")
    drawing_canvas.pack(side=tkinter.LEFT)

    # ---- Charge les images GIF
    image_mur        = tkinter.PhotoImage(file="images/mur.gif")
    image_herbe      = tkinter.PhotoImage(file="images/herbe.gif")
    image_rocher     = tkinter.PhotoImage(file="images/rocher.gif")
    image_oeuf       = tkinter.PhotoImage(file="images/oeuf.gif")
    image_croco_g    = tkinter.PhotoImage(file="images/croco-gauche.gif")
    image_croco_d    = tkinter.PhotoImage(file="images/croco-droit.gif")
    image_croco_mort = tkinter.PhotoImage(file="images/croco-mort.gif")

    # ---- 
    #dummy_label = tkinter.Label(main_window)
    #dummy_label.image = image_mur
    #dummy_label.pack()

    # ---- Direction du croco pour affichage image croco gauche or croco droite
    croco_dir = "G"

    # ---- Dessine tableau 
    init_tableau(niveau_actuel)
    dessine_tableau()

    # ---- Monitor keyboards
    main_window.bind("<KeyPress>", move)

    # ---- Boucle de la fenetre graphique
    main_window.mainloop()
