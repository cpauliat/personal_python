#!/usr/bin/env python3
#
# -*- coding: utf-8 -*-
# --------------------------------------------------------------------------------------------------------------------------
# Ce programme dessine le déplacement de la lune autour de la Terre en subissant l'attraction universelle
# On se place dans un référentiel Terrestre (Terre immobile)
#
# Ce programme utilise l'interface graphique Tkinter
#
# Auteur        : Christophe Pauliat
# Platformes    : Linux / Windows / MacOS
#
# IMPORTANT: Pour MacOS, utiliser Python3 et tkinter depuis https://python.org car le Tk fourni par Apple a des bugs
#            cf. https://www.python.org/download/mac/tcltk/
#
# TO DO: rajouter boutons accelerer, ralentir, quitter
#
# Versions
#    2020-04-13: version initiale
#    2020-04-14: optimisation (deplacement de l'image avec coords au lieu de delete puis create)
# --------------------------------------------------------------------------------------------------------------------------
#
#
# ---------- modules
import tkinter 
from tkinter.font import *
import math
import time

# ---------- paramètres initiaux

# -- vitesse de déplacement sur écran
timer = 25      # en ms, plus c'est petit, plus la lune bouge vite, valeurs possibles: 12.5, 25, 50, 100, 200, 400, 800

# -- constante gravitationnelle
g = 6.67259e-11       # constante de gravitation universelle (en N.m2.kg-2 ou m3.kg-1.s-2)

# -- terre
m_terre = 5.9736e24           # masse de la Terre (en kg)
gm = g * m_terre

# -- lune (position initiale au périgée)
m_lune = 7.3477e22            # masse de la lune (en kg)
v_lune_perigee = 1076         # périgée: vitesse initiale (maximale) de la lune (en m.s-1)
d_lune_perigee = 363.3e6      # périgée: distance initiale (minimale) entre le centre de la lune et le centre de la terre (en m)

# -- ecran
xe_max   = 1200               # largeur de la fenetre graphique
ye_max   = 800                # hauteur de la fenetre graphique
xe_terre = 800                # Position X du centre de la Terre dans la fenetre graphique
ye_terre = 400                # Position Y du centre de la Terre dans la fenetre graphique
xe_lune_perigee  = 800        # Position X initiale du centre de la lune dans la fenetre graphique
ye_lune_perigee  = 100        # Position Y initiale du centre de la lune dans la fenetre graphique

# ---------- variables

# pause
pause = True

# vitesse lune et distance terre-lune
v_lune = v_lune_perigee
d_lune = d_lune_perigee

# coordonnees écran centre de la lune 
xe_lune = xe_lune_perigee
ye_lune = ye_lune_perigee

# vecteur vitesse de la lune (composantes en m.s-1)
vx_perigee = v_lune_perigee
vy_perigee = 0
vx = vx_perigee
vy = vy_perigee

# Distance reelle correspondant a un pixel sur la fenetre graphique (en m.pixel-1)
echelle = d_lune / math.sqrt ( (xe_terre - xe_lune)**2 + (ye_terre - ye_lune)**2 )

# vecteur position de la lune (centre de la Terre = centre du repere), (composantes en m)
px_perigee = 0
py_perigee = d_lune_perigee
px = px_perigee
py = py_perigee

# durée d'une orbite en heures
duree_orbite = 0

# temps en secondes
t0 = 0

# delta temps (en secondes)
delta_temps = 3600          

# min, max 
d_lune_min = d_lune_max = d_lune
v_lune_min = v_lune_max = v_lune

# orbite
dernier_quart_orbite = False
orbite_complete = False

# ---------- fonctions
def dessine_axes():
    # axes Tx et Ty
    drawing_canvas.create_line (0, ye_terre, xe_max-1, ye_terre, dash=(2, 2), fill="#000080")
    drawing_canvas.create_line (xe_terre, 0, xe_terre, ye_max-1, dash=(2, 2), fill="#000080")

    # perigee
    drawing_canvas.create_line (xe_lune_perigee - 5, ye_lune_perigee - 5, xe_lune_perigee + 5, ye_lune_perigee + 5, fill="red")
    drawing_canvas.create_line (xe_lune_perigee - 5, ye_lune_perigee + 5, xe_lune_perigee + 5, ye_lune_perigee - 5, fill="red")
    label_perigee = tkinter.Label(drawing_canvas, text="périgée", font=Font(family='Arial', size=16), bg="black", fg="red")
    drawing_canvas.create_window (xe_lune_perigee + 15, ye_lune_perigee - 50, window=label_perigee, anchor=tkinter.NW)

    # apogee
    label_apogee = tkinter.Label(drawing_canvas, text="apogée", font=Font(family='Arial', size=16), bg="black", fg="red")
    drawing_canvas.create_window (xe_lune_perigee + 15, ye_max - 40, window=label_apogee, anchor=tkinter.NW)

def dessine_terre():
    global image_terre
    #drawing_canvas.create_oval (xe_terre - re_terre, ye_terre - re_terre, xe_terre + re_terre, ye_terre + re_terre, fill="blue")
    drawing_canvas.create_image(xe_terre, ye_terre, anchor=tkinter.CENTER, image=image_terre)

def dessine_lune():
    global xe_lune
    global ye_lune
    global xe_max
    global ye_max
    global main_window
    global vx
    global vy
    global px
    global py
    global echelle
    global crash_lune
    global d_lune
    global m_terre
    global m_lune
    global lune
    global t0
    global label
    global d_lune_min
    global d_lune_max
    global v_lune
    global v_lune_min
    global v_lune_max
    global timer
    global image_lune
    global duree_orbite
    global dernier_quart_orbite
    global orbite_complete

    # ---- On ne bouge que si on n'est pas en pause
    if not(pause):

        # -- Si on n'a pas encore fait une orbite complète,
        # -- on crée un point à l'ancienne position du centre de la lune pour matérialiser l'orbite
        if not(orbite_complete):
            drawing_canvas.create_line (xe_lune, ye_lune, xe_lune+1, ye_lune+1, fill="grey")

        # -- temps en secondes
        t0 += delta_temps 

        # -- on calcule le nouveau vecteur vitesse de la lune 
        # angle entre vecteur acceleration et axe (Tx) en radians 
        # les vecteurs accelerations et OT sont colinéaires meme sens.

        # dans le atan() car l'axe des y et l'axe des ye sont sens opposés
        beta = math.atan2 (- (ye_terre - ye_lune) , (xe_terre - xe_lune))

        # vecteur acceleration
        # l'acceleration de la lune est a = g * m_terre / d_lune^2
        a = gm / (px**2 + py**2)
        ax = a * math.cos(beta)
        ay = a * math.sin(beta)

        # -- nouveau vecteur vitesse: v = v + dt * a    (dt = delta temps, a = vecteur vitesse)
        vx += delta_temps * ax
        vy += delta_temps * ay

        # -- nouvelle position de la lune: p = p + dt * v (vecteurs p et v)
        px += delta_temps * vx
        py += delta_temps * vy
        v_lune = math.sqrt(vx**2 + vy**2)
        v_lune_min = min(v_lune, v_lune_min)
        v_lune_max = max(v_lune, v_lune_max)

        # -- nouvelle distance lune terre en m
        d_lune = math.sqrt(px**2 + py**2)
        d_lune_min = min(d_lune, d_lune_min)
        d_lune_max = max(d_lune, d_lune_max)

        # -- nouvelle distance lune terre sur l'écran en pixels
        de_lune = int(d_lune / echelle)

        # -- nouvelle position de la lune sur l'ecran
        xe_lune = int(xe_terre + px / echelle)
        ye_lune = int(ye_terre - py / echelle)

        # -- si on rentre dans le dernier quart d'orbite, on le note pour se préparer à la fin d'orbite et à la correction de trajectoire
        if not(dernier_quart_orbite) and px < 0 and py > 0: 
            dernier_quart_orbite = True

        # -- correction de trajectoire (déviation de l'orbite a cause erreurs d'arrondi)
        if dernier_quart_orbite and px > 0:
            d_lune = d_lune_perigee
            v_lune = v_lune_perigee

            vx = vx_perigee
            vy = vy_perigee

            px = px_perigee
            py = py_perigee

            xe_lune = xe_lune_perigee
            ye_lune = ye_lune_perigee

            duree_orbite = t0
            t0 = 0

            dernier_quart_orbite = False
            orbite_complete = True

        # -- On déplace l'image de la lune
        drawing_canvas.coords(lune, xe_lune, ye_lune)

        # -- ON affiche les paramètres
        message = "Temps (depuis début): {:.1f} jours \n\n".format(t0 / 24 / 3600) + \
                  "Durée d'une orbite  : {:.1f} jours \n\n".format(duree_orbite / 24 / 3600) + \
                  "Distance Terre-lune : {:.0f} km \n".format(d_lune / 1000) + \
                  "   minimum (périgée): {:.0f} km \n".format(d_lune_min / 1000) + \
                  "   maximum (apogée) : {:.0f} km \n\n".format(d_lune_max / 1000) + \
                  "Vitesse lune        : {:4.0f} m/s-1 ou {:4.0f} km/h\n".format(v_lune, v_lune * 3.6) + \
                  "   minimum (apogée) : {:4.0f} m/s-1 ou {:4.0f} km/h\n".format(v_lune_min, v_lune_min * 3.6) + \
                  "   maximum (périgée): {:4.0f} m/s-1 ou {:4.0f} km/h".format(v_lune_max, v_lune_max * 3.6)
        label.config(text=message)

    # ---- pause ou pas, on re-appelle cette fonction au bout d'un certain temps
    main_window.after(int(timer), dessine_lune)

def modifie_vitesse(op, txt):
    global timer            # valeurs possibles: 12.5, 25, 50, 100, 200, 400, 800
    global drawing_canvas

    if op == "+":
        if timer >= 25: timer = timer / 2
    else:
        if timer <= 400: timer = timer * 2
    
    drawing_canvas.itemconfigure (txt, text="Rafraichissement toutes les {:d} ms".format(int(timer)))


def pause_continue():
    global pause
    global bt_pause

    if pause:
        pause = False
        bt_pause.config(text="Pause")
    else:
        pause = True
        bt_pause.config(text="Continuer")

# ---------- programme principal
if __name__ == '__main__':
    # ---- Main Window
    main_window = tkinter.Tk()
    main_window.title('Attraction Universelle : Terre - Lune')

    # ---- Drawing canvas
    drawing_frame = tkinter.Frame(main_window)
    drawing_frame.pack(side=tkinter.LEFT, padx=0, pady=0)

    drawing_canvas = tkinter.Canvas(drawing_frame, height=ye_max, width=xe_max, bg="black")
    drawing_canvas.pack(side=tkinter.LEFT)

    # ---- Label pour afficher les paramètres lunaires
    message=""
    label = tkinter.Label(drawing_canvas, text=message, font=Font(family='Courier new', size=14), justify=tkinter.LEFT, bg="black", fg="yellow")
    drawing_canvas.create_window (20, ye_max - 210, window=label, anchor=tkinter.NW)

    # ---- Charge les images GIF
    image_terre = tkinter.PhotoImage(file="images/terre.gif")
    image_lune  = tkinter.PhotoImage(file="images/lune.gif")

    # ---- dessin des axes Tx, Ty
    dessine_axes()

    # ---- Dessin de la Terre
    dessine_terre()

    # ---- Dessin de la lune 
    lune = drawing_canvas.create_image(xe_lune, ye_lune, anchor=tkinter.CENTER, image=image_lune)
    dessine_lune()
   
    # ---- rajout des boutons dans le canvas
    t_dt   = drawing_canvas.create_text  (30, 40, anchor=tkinter.NW, text="Rafraichissement toutes les {:d} ms".format(timer), font=Font(family='Courier New', size=14), fill="yellow")

    bt_vitesse_p = tkinter.Button (main_window, text="Accélérer", height=2, width=10, command=lambda: modifie_vitesse("+", t_dt))
    bt_vitesse_m = tkinter.Button (main_window, text="Ralentir",  height=2, width=10, command=lambda: modifie_vitesse("-", t_dt))
    bt_pause     = tkinter.Button (main_window, text="Démarrer",  height=2, width=10, command=pause_continue)
    bt_quit      = tkinter.Button (main_window, text="Quitter",   height=2, width=10, command=main_window.destroy)

    drawing_canvas.create_window(30, 80, anchor=tkinter.NW, window=bt_vitesse_p)
    drawing_canvas.create_window(140, 80, anchor=tkinter.NW, window=bt_vitesse_m)
    drawing_canvas.create_window(30, 130, anchor=tkinter.NW, window=bt_pause)
    drawing_canvas.create_window(xe_max - 30, 40,  anchor=tkinter.NE, window=bt_quit)

    # ---- Boucle de la fenetre graphique
    main_window.mainloop()
