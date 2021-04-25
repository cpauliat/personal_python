#!/usr/bin/env python3
#
# -*- coding: utf-8 -*-
# --------------------------------------------------------------------------------------------------------------------------
# Ce programme dessine l'ensemble de Mandelbrot et permet de zoomer dessus pour voir les détails
# Il est possible de sauver l'image courante dans un fichier image .png
#
# Auteur : Christophe Pauliat
# Date   : Avril 2021
# --------------------------------------------------------------------------------------------------------------------------


# ---------- modules
import tkinter 
import tkinter.font
import tkinter.messagebox
import tkinter.ttk
import tkinter.filedialog
import math
import cmath
import time
import random
import numpy as np
from PIL import Image
from PIL import ImageColor

# ---------- variables
#hauteur_canvas, xmin, xmax, ymin, ymax = 1200, -2.2, 0.8, -0.1, 1.3
#hauteur_canvas, xmin, xmax, ymin, ymax = 1400, -1, 0, 0, 1
hauteur_canvas, xmin0, xmax0, ymin0, ymax0 = 1350, -2.1234567890123456, 0.8, -1.3, 1.3
p = 2               # puissance p dans la formule: zn+1 = zn ^ p + c

cpt_max = 100   # nb max d'iterations

couleur_fond       = "#4040D0"
couleur_mandelbrot = "black"

xmin, xmax, ymin, ymax = xmin0, xmax0, ymin0, ymax0
largeur_canvas = int (hauteur_canvas * (xmax - xmin) / (ymax - ymin))   # on calcule la largeur pour conserver le ratio 
coords = []


# ---------- fonctions

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

def colors_palette0():
    colors.extend(colors_degrade("white","white",10))

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

# Suite: zn+1 = zn ^ p + c
def znp1(zn, c):
    global p

    z = zn
    for i in range(p - 1):
        z = z * zn
    z = z + c
    return z

def mandelbrot_color(x,y):
    zn = 0
    c  = x + y * 1j
    n  = 0

    while (n < cpt_max) and (abs(zn) <= 2):
        zn = znp1 (zn, c)
        n += 1

    if n == cpt_max:
        return couleur_mandelbrot
    else:
        color_index = int(n / cpt_max * nb_colors)
        return colors [color_index] 

def x_to_xecran(x):
    return int((x - xmin) / (xmax - xmin) * largeur_canvas)

def y_to_yecran(y):
    return int(hauteur_canvas - (y - ymin) / (ymax - ymin) * hauteur_canvas)

def xecran_to_x(xe):
    return float(xe * (xmax - xmin) / largeur_canvas + xmin)

def yecran_to_y(ye):
    return float(ymax - ye * (ymax - ymin) / hauteur_canvas)

def efface_et_resize_canvas():
    global canvas_dessin
    global current_pos_tv

    # on peut sauver une image seulement apres un calcul précis
    save_button["state"] = tkinter.DISABLED

    canvas_dessin.delete("all")
    canvas_dessin.config(width = largeur_canvas)
    current_pos_tv.set("COORDONNEES SOURIS:\n\nx  :                    \n\ny  : ")


def disable_buttons():
    redimensionne_button["state"] = tkinter.DISABLED
    reset_button        ["state"] = tkinter.DISABLED
    zoom_out_button     ["state"] = tkinter.DISABLED
    
def enable_buttons():
    redimensionne_button["state"] = tkinter.NORMAL
    reset_button        ["state"] = tkinter.NORMAL
    zoom_out_button     ["state"] = tkinter.NORMAL

def dessine_mandelbrot(xprecision, yprecision):
    global calcul_en_cours
    global selected_rectangle
    global canvas_dessin
    global myarray

    print (f"Calcul démarré")
    calcul_en_cours = True
    disable_buttons()
    calcul_en_cours_tv.set("CALCUL EN COURS : 0 %")
    fenetre.update()

    t1 = time.time()
    t2 = t1
    for xe in range(0,largeur_canvas,xprecision):
        for ye in range(0,hauteur_canvas,yprecision):
            x = xecran_to_x(xe)
            y = yecran_to_y(ye)
            color = mandelbrot_color(x,y)
            canvas_dessin.create_rectangle(xe, ye, xe+xprecision, ye+yprecision, outline = color, fill = color)
            rgb = ImageColor.getcolor(color,"RGB")
            myarray[ye][xe][0] =  rgb[0]
            myarray[ye][xe][1] =  rgb[1]
            myarray[ye][xe][2] =  rgb[2]
        t3 = time.time()
        # toutes les secondes, on refresh l'écran
        if t3 - t2 > 1:
            t2 = t3
            canvas_dessin.update()
            pct = int(xe / largeur_canvas * 100)
            calcul_en_cours_tv.set(f"CALCUL EN COURS : {pct} %")
            calcul_en_cours_label.update()

    t4 = time.time()
    print (f"Calcul terminée: durée = {t4 - t1:.2f} s.")

    calcul_en_cours_tv.set("CALCUL EN COURS : 100 %")
    calcul_en_cours_label.update()

    canvas_dessin.update()

    calcul_en_cours = False
    calcul_en_cours_tv.set("")
    enable_buttons()

def calcule_rapide():
    global myarray

    # on cree un Numpy Array pour contenir l'image calculee
    myarray = np.zeros(shape=(hauteur_canvas,largeur_canvas,3), dtype=np.uint8)
    dessine_mandelbrot(5, 5)

    # apres le calcul rapide, on peut activer le bouton calcul precis
    cc_precis_button["state"] = tkinter.NORMAL

def calcule_precis():
    # un fois le calcul precis démarré, on peut desactiver le bouton calcul precis
    cc_precis_button["state"] = tkinter.DISABLED
    
    # calcul et affichage
    dessine_mandelbrot(1, 1)

    # on peut sauver une image seulement apres un calcul précis
    save_button["state"] = tkinter.NORMAL

def sauve_coords():
    global coords
    coords.append ([ xmin, xmax, ymin, ymax ])
    print ("DEBUG: coords = ",coords)

# ---- events souris
def affiche_position_souris_in_canvas(event):
    global current_pos_tv

    # aucune action possible si calcul/affichage en cours
    if calcul_en_cours:
        return

    x  = xecran_to_x(event.x)
    y  = yecran_to_y(event.y)
    current_pos_tv.set(f"COORDONNEES SOURIS:\n\nx  : {x: .16f}\n\ny  : {y: .16f}")

def select_area_start(event):
    global selected_area_x1
    global selected_area_x2
    global selected_area_y1
    global selected_area_y2
    global selected_rectangle
    global xsel1
    global ysel1

    # aucune action possible si calcul/affichage en cours
    if calcul_en_cours:
        return

    selected_area_x1 = selected_area_x2 = event.x
    selected_area_y1 = selected_area_y2 = event.y
    xsel1 = xecran_to_x(selected_area_x1)
    ysel1 = yecran_to_y(selected_area_y1)
    selected_area_tv.set(f"ZONE SELECTIONNEE:\n\nx1 : {xsel1: .16f}\n\ny1 : {ysel1: .16f}\n\nx2 : \n\ny2 : ")
    selected_rectangle = canvas_dessin.create_rectangle(selected_area_x1, selected_area_y1, selected_area_x1 + 1, selected_area_y1 + 1, fill = "", outline = "white")

def select_area_change(event):
    global selected_area_x1
    global selected_area_x2
    global selected_area_y1
    global selected_area_y2
    global selected_rectangle
    global xsel2
    global ysel2

    # aucune action possible si calcul/affichage en cours
    if calcul_en_cours:
        return

    selected_area_x2 = event.x
    selected_area_y2 = event.y

    xsel2 = xecran_to_x(selected_area_x2)
    ysel2 = yecran_to_y(selected_area_y2)
    selected_area_tv.set(f"ZONE SELECTIONNEE:\n\nx1 : {xsel1: .16f}\n\ny1 : {ysel1: .16f}\n\nx2 : {xsel2: .16f}\n\ny2 : {ysel2: .16f}")

    canvas_dessin.coords(selected_rectangle, selected_area_x1, selected_area_y1, selected_area_x2, selected_area_y2)

def select_area_end(event):
    global selected_area_x1
    global selected_area_x2
    global selected_area_y1
    global selected_area_y2
    global xmin
    global xmax
    global ymin
    global ymax
    global largeur_canvas

    # aucune action possible si calcul/affichage en cours
    if calcul_en_cours:
        return

    selected_area_tv.set("ZONE SELECTIONNEE:\n\nx1 :                    \n\ny1 : \n\nx2 : \n\ny2 : ")

    selected_area_x2 = event.x
    selected_area_y2 = event.y

    # si les points départ et arrivés sont confondus, on annule la selection
    if selected_area_x2 == selected_area_x1 and selected_area_y2 == selected_area_y1:
        selected_area_x1 = selected_area_x2 = selected_area_y1 = selected_area_y2 = -1
    
    else:
        minx = min(selected_area_x1, selected_area_x2)
        maxx = max(selected_area_x1, selected_area_x2)
        print (f"DEBUG: x1={selected_area_x1} x2={selected_area_x2} y1={selected_area_y1} y1={selected_area_y2} min={minx} max={maxx}")

        xmin_new = xecran_to_x(min(selected_area_x1, selected_area_x2))
        xmax_new = xecran_to_x(max(selected_area_x1, selected_area_x2))
        ymin_new = yecran_to_y(max(selected_area_y1, selected_area_y2))
        ymax_new = yecran_to_y(min(selected_area_y1, selected_area_y2))
        sauve_coords()
        xmin, xmax, ymin, ymax = xmin_new, xmax_new, ymin_new, ymax_new
        largeur_canvas = int (hauteur_canvas * (xmax - xmin) / (ymax - ymin))   # on calcule la largeur pour conserver le ratio 
        zoom_display_area_coords()
        efface_et_resize_canvas()
        calcule_rapide()

def zoom_display_area_coords():
    dimensions_tv[0].set(f"{xmin: .16f}")
    dimensions_tv[1].set(f"{xmax: .16f}")
    dimensions_tv[2].set(f"{ymin: .16f}")
    dimensions_tv[3].set(f"{ymax: .16f}")

def zoom_reset():
    global xmin
    global xmax
    global ymin
    global ymax   
    global largeur_canvas

    xmin, xmax, ymin, ymax = xmin0, xmax0, ymin0, ymax0
    largeur_canvas = int (hauteur_canvas * (xmax - xmin) / (ymax - ymin))   # on calcule la largeur pour conserver le ratio 
    zoom_display_area_coords()
    efface_et_resize_canvas()
    calcule_rapide()

def zoom_out():
    global xmin
    global xmax
    global ymin
    global ymax
    global largeur_canvas

    xmin, xmax, ymin, ymax = coords.pop()
    zoom_display_area_coords()

    largeur_canvas = int (hauteur_canvas * (xmax - xmin) / (ymax - ymin))   # on calcule la largeur pour conserver le ratio 
    efface_et_resize_canvas()
    calcule_rapide()

    #print (f"DEBUG: xmin = {xmin}  xmax = {xmax}  ymin = {ymin}  ymax = {ymax}  coords = {coords}")

def redimensionne():
    global xmin
    global xmax
    global ymin
    global ymax
    global largeur_canvas

    sauve_coords()

    xmin = float(dimensions_tv[0].get())
    xmax = float(dimensions_tv[1].get())
    ymin = float(dimensions_tv[2].get())
    ymax = float(dimensions_tv[3].get())

    # to do: test if xmin >= xmax or ymin >= max, 

    largeur_canvas = int (hauteur_canvas * (xmax - xmin) / (ymax - ymin))   # on calcule la largeur pour conserver le ratio 
    efface_et_resize_canvas()
    calcule_rapide()

# ---- Fin du programme après confirmation
def sauver_png():
    myFormats = [ ('Image PNG','*.png') ]
    nom_fichier = tkinter.filedialog.asksaveasfilename(parent = fenetre, initialdir = "images", filetypes = myFormats, title="Choisir un nom pour le fichier PNG")
     
    if nom_fichier == "":
        return
        
    # si le nom de fichier ne finit pas par ".png", on rajoute ce suffixe
    if (len(nom_fichier)<4):
        nom_fichier+=".png"
    else:
        suffixe=nom_fichier[len(nom_fichier)-4:len(nom_fichier)]
        suffixe=suffixe.lower()
        if (suffixe!=".png"):
            nom_fichier+=".png"

    mon_image = Image.fromarray(myarray)
    mon_image.save(nom_fichier)

def quitter():
    if tkinter.messagebox.askyesno("Fin du programme","Voulez-vous vraiment quitter l'application ?"): 
        fenetre.destroy()

# ---------- programme principal

if __name__ == '__main__':

    # ---- other variables
    colors = [ ]
    colors_palette1()
    nb_colors = len(colors)
    calcul_en_cours = False
    couleur_boutons         = "#F04040"
    couleur_frame           = "#202020"
    couleur_texte           = "#FFFF00"
    couleur_coords_souris   = "#FF8000"
    couleur_selection       = "#00E000"
    couleur_calcul_en_cours = "red"
    selected_area_x1 = selected_area_x2 = selected_area_y1 = selected_area_y2 = -1
    xsel1 = ysel1 = xsel2 = ysel2 = 0

    # ---- fenêtre principale
    fenetre = tkinter.Tk()
    fenetre.title('Ensemble de Mandelbrot')
    fenetre.resizable(width=False, height=False)    # on empeche le redimensionnement manuel de la fenetre

    # ---- frame de controle
    font_cn16 = tkinter.font.Font(family='Courier new', size=16)
    font_ar16 = tkinter.font.Font(family='Arial', size=16)
    font_ar18 = tkinter.font.Font(family='Arial', size=18)
    font_ar20 = tkinter.font.Font(family='Arial', size=20, weight='bold')
    power_tv  = tkinter.StringVar()
    dimensions_tv = []
    for i in range (4):
        dimensions_tv.append(tkinter.StringVar())
    current_pos_tv     = tkinter.StringVar()
    calcul_en_cours_tv = tkinter.StringVar()
    selected_area_tv   = tkinter.StringVar()

    power_tv.set("2")
    zoom_display_area_coords()
    current_pos_tv.set("COORDONNEES SOURIS:\n\nx  :                    \n\ny  : ")
    calcul_en_cours_tv.set("")
    selected_area_tv.set("ZONE SELECTIONNEE:\n\nx1 :                    \n\ny1 : \n\nx2 : \n\ny2 : ")

    frame_controle = tkinter.Frame(fenetre, bg = couleur_frame)
    frame_controle.pack(side = tkinter.LEFT, fill = tkinter.Y)

    formule_label   = tkinter.Label (frame_controle, anchor = tkinter.W, font = font_cn16, text = "Zn+1 = Zn ^ p + c", bg = couleur_frame, fg = couleur_selection)
    power_frame     = tkinter.Frame (frame_controle, bg = couleur_frame)
    power_label     = tkinter.Label (power_frame, anchor = tkinter.W, font = font_cn16, text = "p = ", bg = couleur_frame, fg = couleur_selection)
    power_entry     = tkinter.Entry (power_frame, justify = tkinter.LEFT, font = font_cn16, width = 3, bg = couleur_frame, fg = couleur_texte, relief = tkinter.FLAT, highlightcolor = "red", textvariable = power_tv)
    power_button    = tkinter.Button(power_frame, text = "  PUISSANCE  ", font = font_ar18, height = 2, fg = "green", command = zoom_reset)

    dimensions_frame      = tkinter.Frame(frame_controle, bg = couleur_frame)
    dims_text = [ "Xmin : ", "Xmax : ", "Ymin : ", "Ymax : "]
    for i in range(4):
        tkinter.Label (dimensions_frame, anchor = tkinter.W, font = font_cn16, text = dims_text[i], bg = couleur_frame, fg = couleur_texte).grid(sticky = tkinter.N+tkinter.W, column=0, row=i, pady = 5)
        tkinter.Entry (dimensions_frame, justify = tkinter.LEFT, font = font_cn16, width = 19, bg = couleur_frame, fg = couleur_texte, relief = tkinter.FLAT, highlightcolor = "red", textvariable = dimensions_tv[i]).grid(sticky = tkinter.N+tkinter.W+tkinter.E, column=1, row=i, pady = 5)
    redimensionne_button  = tkinter.Button(frame_controle, text = "REDIMENSIONNE", font = font_ar18, height = 2, fg = "green", command = redimensionne)
    reset_button          = tkinter.Button(frame_controle, text = "DIMENSIONS INITIALES", font = font_ar18, height = 2, fg = "green", command = zoom_reset)
    zoom_out_button       = tkinter.Button(frame_controle, text = "   DIMENSIONS PRECEDENTES   ", font = font_ar18, height = 2, fg = "green", command = zoom_out)
    cc_precis_button      = tkinter.Button(frame_controle, text = "CALCUL PRECIS", font = font_ar18, height = 2, fg = "blue", state = tkinter.DISABLED, command = calcule_precis)
    save_quit_frame       = tkinter.Frame (frame_controle, bg = couleur_frame)
    save_button           = tkinter.Button(save_quit_frame, text = "SAUVER", font = font_ar18, height = 2,  fg = "green", state = tkinter.DISABLED, command = sauver_png)
    quit_button           = tkinter.Button(save_quit_frame, text = "QUITTER", font = font_ar18, height = 2,  fg = "red", command = quitter)
    current_pos_label     = tkinter.Label (frame_controle, justify = tkinter.LEFT, font = font_cn16, textvariable = current_pos_tv, bg = couleur_frame, fg = couleur_coords_souris)
    calcul_en_cours_label = tkinter.Label (frame_controle, justify = tkinter.CENTER, font = font_ar20, textvariable = calcul_en_cours_tv, bg = couleur_frame, fg = couleur_calcul_en_cours)
    selected_area_label   = tkinter.Label (frame_controle, justify = tkinter.LEFT, font = font_cn16, textvariable = selected_area_tv, bg = couleur_frame, fg = couleur_selection)
    separator1            = tkinter.ttk.Separator (frame_controle, orient = 'horizontal')
    separator2            = tkinter.ttk.Separator (frame_controle, orient = 'horizontal')
    separator3            = tkinter.ttk.Separator (frame_controle, orient = 'horizontal')
    separator4            = tkinter.ttk.Separator (frame_controle, orient = 'horizontal')

    formule_label.pack        (side = tkinter.TOP, padx = 20, pady = 10,  fill = tkinter.X)
    power_frame.pack          (side = tkinter.TOP, padx = 20, pady = 10,   fill = tkinter.X)
    power_label.pack          (side = tkinter.LEFT, padx = 0, pady = 0,   fill = tkinter.X)
    power_entry.pack          (side = tkinter.LEFT, padx = 0, pady = 0,   fill = tkinter.X)
    power_button.pack         (side = tkinter.LEFT, padx = 20, pady = 0,   fill = tkinter.X)
    separator1.pack           (side = tkinter.TOP, padx = 0,  pady = 5,   fill = tkinter.X)
    dimensions_frame.pack     (side = tkinter.TOP, padx = 20, pady = 0,   fill = tkinter.X)
    redimensionne_button.pack (side = tkinter.TOP, padx = 20, pady = 10,  fill = tkinter.X)
    reset_button.pack         (side = tkinter.TOP, padx = 20, pady = 10,  fill = tkinter.X)
    zoom_out_button.pack      (side = tkinter.TOP, padx = 20, pady = 10,  fill = tkinter.X)
    cc_precis_button.pack     (side = tkinter.TOP, padx = 20, pady = 10,  fill = tkinter.X)
    save_quit_frame.pack      (side = tkinter.TOP, padx = 10, pady = 10,  fill = tkinter.X)
    save_quit_frame.columnconfigure (0, weight = 1)
    save_quit_frame.columnconfigure (1, weight = 1)
    save_button.grid          (sticky = tkinter.N+tkinter.W+tkinter.E, column=0, row=0, padx = 10)    
    quit_button.grid          (sticky = tkinter.N+tkinter.W+tkinter.E, column=1, row=0, padx = 10)
    separator2.pack           (side = tkinter.TOP, padx = 0,  pady = 5,   fill = tkinter.X)
    current_pos_label.pack    (side = tkinter.TOP, padx = 20, pady = 10,  fill = tkinter.X)
    separator3.pack           (side = tkinter.TOP, padx = 0,  pady = 0,   fill = tkinter.X)
    calcul_en_cours_label.pack(side = tkinter.TOP, padx = 20, pady = 10,  fill = tkinter.X)
    separator4.pack           (side = tkinter.TOP, padx = 0,  pady = 0,   fill = tkinter.X)
    selected_area_label.pack  (side = tkinter.TOP, padx = 20, pady = 20,  fill = tkinter.X)

    # ---- canvas pour dessiner
    xe0 = x_to_xecran(0)
    ye0 = y_to_yecran(0)
    canvas_dessin = tkinter.Canvas(fenetre, bg = "black", highlightthickness = 0)
    canvas_dessin.pack(side = tkinter.LEFT)
    canvas_dessin.config(width = largeur_canvas, height = hauteur_canvas)

    # ---- Events souris dans le canvas
    canvas_dessin.bind('<Motion>', affiche_position_souris_in_canvas)
    canvas_dessin.bind('<ButtonPress-1>',   select_area_start)
    canvas_dessin.bind('<B1-Motion>',       select_area_change)
    canvas_dessin.bind('<ButtonRelease-1>', select_area_end)

    # ---- On affiche l'ensemble de Mandelbrot en calcul rapide après n ms
    fenetre.after (500, calcule_rapide)

    # ---- Boucle de la fenetre graphique
    fenetre.mainloop()


