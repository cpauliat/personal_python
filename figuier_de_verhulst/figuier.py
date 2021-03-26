#!/usr/bin/env python3
#
# -*- coding: utf-8 -*-
# --------------------------------------------------------------------------------------------------------------------------

# Auteur        : Christophe Pauliat
# --------------------------------------------------------------------------------------------------------------------------


# ---------- modules
import tkinter 
import math

# ---------- fonctions
def un(r):
    limits=[]
    u0 = 0.4
    un = u0
    for i in range(10000):
        un = r * un * (1 - un)

    # get last 10 values
    for i in range(10):
        un = r * un * (1 - un)
        limits.append(format(un, '.5f'))

    # remove duplicates values
    limits.sort()
    limits = list( dict.fromkeys(limits))

    #print (r, limits)
    return limits

def dessine_axe():
    canvas_dessin.create_line(espace_axes, hauteur_canvas - espace_axes, espace_axes, espace_axes, fill = couleur_axe, arrow = tkinter.LAST)
    canvas_dessin.create_line(espace_axes, hauteur_canvas - espace_axes, largeur_canvas - espace_axes, hauteur_canvas - espace_axes, fill = couleur_axe, arrow = tkinter.LAST)
    for x in range(1,end):
        canvas_dessin.create_line(x_to_xecran(x), y_to_yecran(0) - 5, x_to_xecran(x), y_to_yecran(0) + 5, fill = couleur_axe)

def x_to_xecran(x):
    return int((x - start) / (end - start) * (largeur_canvas - 2 * espace_axes ) + espace_axes)

def y_to_yecran(y):
    return int(hauteur_canvas - espace_axes - y * (hauteur_canvas - 2 * espace_axes ))

def dessine_figuier(start, end, precision):
    for r2 in range(start * precision, end * precision):
        r = r2 / precision
        limits = un(r)
        for pt in limits:
            xe = x_to_xecran(r)
            ye = y_to_yecran(float(pt))
            canvas_dessin.create_line(xe,ye,xe+1,ye+1,fill = couleur_points)


# ---------- programme principal

if __name__ == '__main__':

    # ---- variables
    start = 0
    end = 4
    precision = 8000
    largeur_canvas = 3400
    hauteur_canvas = 1200
    espace_axes = 50
    couleur_fond = "#4040D0"
    couleur_axe = "white"
    couleur_points = "red"

    # ---- fenêtre principale
    fenetre = tkinter.Tk()
    fenetre.title('Figuier de Verhulst')
    fenetre.config(bg=couleur_fond)
    fenetre.resizable(width=False, height=False)    # on empeche le redimensionnement manuel de la fenetre

    # ---- canvas pour dessiner
    canvas_dessin = tkinter.Canvas(fenetre, bg="black", highlightthickness=0)
    canvas_dessin.pack(padx=10, pady=10)
    canvas_dessin.config(width=largeur_canvas, height=hauteur_canvas)

    # ---- dessine le figuier
    dessine_axe()
    dessine_figuier (start, end, precision)

    # ---- Boucle de la fenetre graphique
    fenetre.mainloop()



