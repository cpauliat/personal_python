#!/usr/bin/env python3
#
# -*- coding: utf-8 -*-
# --------------------------------------------------------------------------------------------------------------------------
# Ce programme crer un fichier image .png contenant l'image de l'ensemble de Julia demandé
# 
# Auteur : Christophe Pauliat
# Date   : Mai 2021
# --------------------------------------------------------------------------------------------------------------------------


# ---------- modules
import math
import cmath
import time
import random
import sys
import numpy
from PIL import Image
from PIL import ImageColor

# ---------- variables
rayon = 2                # valeur du module pour laquelle on arrête les iterations
p = 2                    # valeur de p dans Zn+1 = Zn ^ p + c

# ---------- fonctions

# ---- Parse arguments
def usage():
    print (f"Usage: {sys.argv[0]} xmin xmax ymin ymax hauteur_image max_iterations cx cy nom_fichier_png")
    exit(1)

def parse_args():
    global xmin, xmax, ymin, ymax, hauteur_image, max_iterations, nom_fichier, largeur_image, valeur_c
    if (len(sys.argv) != 10):
        usage()
    
    xmin = float(sys.argv[1])
    xmax = float(sys.argv[2])
    ymin = float(sys.argv[3])
    ymax = float(sys.argv[4])
    hauteur_image  = int(sys.argv[5])
    max_iterations = int(sys.argv[6])
    cx = float(sys.argv[7])
    cy = float(sys.argv[8])
    nom_fichier    = sys.argv[9]

    # valeur du point C
    valeur_c = cx + cy * 1j

    # on calcule la largeur de l'image pour conserver le ratio
    largeur_image = int (hauteur_image * (xmax - xmin) / (ymax - ymin))

    # si le nom de fichier ne finit pas par ".png", on rajoute .png à la fin
    if nom_fichier[:4] != ".png":
        nom_fichier = nom_fichier + ".png"

# ---- convertions entre coordonnees reelles et coordonnees graphiques
def x_to_xecran(x):
    return int((x - xmin) / (xmax - xmin) * largeur_image)

def y_to_yecran(y):
    return int(hauteur_image - (y - ymin) / (ymax - ymin) * hauteur_image)

def xecran_to_x(xe):
    return float(xe * (xmax - xmin) / largeur_image + xmin)

def yecran_to_y(ye):
    return float(ymax - ye * (ymax - ymin) / hauteur_image)

# ---- gestion des couleurs
def colors_degrade(c1, c2, nbcolors):
    col = []
    [ r1, g1, b1 ] = ImageColor.getcolor(c1,"RGB")
    [ r2, g2, b2 ] = ImageColor.getcolor(c2,"RGB")

    dr = (r2 - r1) / nbcolors
    dg = (g2 - g1) / nbcolors
    db = (b2 - b1) / nbcolors
    for i in range(nbcolors + 1):
        r = int(r1 + i * dr)
        g = int(g1 + i * dg)
        b = int(b1 + i * db)
        col.append(f"#{r:02x}{g:02x}{b:02x}")
        
    return col

def colors_init():
    global colors, nb_colors, couleur_julia

    couleur_julia = "black"
    colors = [ ] 
    colors_palette1()
    nb_colors = len(colors)

def colors_palette1():
    colors.extend(colors_degrade("#000032","#FA0000",100))
    colors.extend(colors_degrade("#FF0000","#00FF00",255))

def colors_palette2():
    colors.extend(colors_degrade("black","green",40))
    colors.extend(colors_degrade("green","red",100))
    colors.extend(colors_degrade("red","orange",200))

def colors_palette3():
    colors.extend(colors_degrade("red","darkorange",50))
    colors.extend(colors_degrade("darkorange","yellow",100))
    colors.extend(colors_degrade("yellow","green",200))
    colors.extend(colors_degrade("green","darkgreen",400))

def get_color_from_iteration(nb_iterations):
    if nb_iterations == max_iterations:
        return couleur_julia
    else:
        color_index = int(nb_iterations / max_iterations * nb_colors)
        return colors [color_index] 

# ---- Calculs
# Suite: zn+1 = zn ^ p + c
def znp1(zn):
    z = zn
    for i in range(p - 1):
        z = z * zn
    z = z + valeur_c
    return z

def julia_iterations_basic(x,y):
    zn = z0 = x + y * 1j
    n  = 0
    while (n < max_iterations) and (abs(zn) <= rayon): 
        zn = znp1 (zn)
        n += 1
    return n

def julia_iterations_periodicity_checking(x,y):
    zn = z0 = x + y * 1j
    n  = 0
    z_old = z0
    while (n < max_iterations) and (abs(zn) <= rayon):
        zn = znp1 (zn)
        n += 1

        if abs(zn - z_old) < 0.01:
            n = max_iterations
            break

        if n % 20 == 0:
            z_old = zn

    return n

def calcule_julia_algo_basic():
    global calcul_en_cours
    global selected_rectangle
    global canvas_dessin
    global myarray

    # on cree un Numpy Array pour contenir l'image calculee
    myarray = numpy.zeros(shape=(hauteur_image,largeur_image,3), dtype=numpy.uint8)

    t1 = time.time()
    for xe in range(0,largeur_image):
        for ye in range(0,hauteur_image):
            x = xecran_to_x(xe)
            y = yecran_to_y(ye)
            color = get_color_from_iteration(julia_iterations_periodicity_checking(x,y))
            rgb = ImageColor.getcolor(color,"RGB")
            myarray[ye][xe][0] =  rgb[0]
            myarray[ye][xe][1] =  rgb[1]
            myarray[ye][xe][2] =  rgb[2]

    t2 = time.time()
    print (f"Calcul terminé: durée = {t2 - t1:.2f} s.")

# ---- Sauvegarde de l'image cree dans un fichier .png
def sauve_image_dans_png():
    mon_image = Image.fromarray(myarray)
    mon_image.save(nom_fichier)
    print (f"Image sauvegardée dans le fichier {nom_fichier}")

# ---------- programme principal
if __name__ == '__main__':

    # initialisation des couleurs
    colors_init()
    
    # parse arguments on the command line
    parse_args()

    # calcule de l'image dans un numpy array
    calcule_julia_algo_basic()

    # sauvegarde de l'image
    sauve_image_dans_png()