#!/usr/bin/env python3
#
# -*- coding: utf-8 -*-
# --------------------------------------------------------------------------------------------------------------------------
# Ce programme dessine l'ensemble de Mandelbrot et permet de zoomer dessus pour voir les détails
# Il est possible de sauver l'image courante dans un fichier image .png
#
# Auteur : Christophe Pauliat
# 
# Versions:
#     2021/04/15: Initial version
#     2021/11/23: Using NumPy arrays to speed up computing
#     2021/11/23: Fix minor bugs
# --------------------------------------------------------------------------------------------------------------------------


# ---------- modules
import tkinter
from tkinter.constants import ANCHOR 
import tkinter.font
import tkinter.messagebox
import tkinter.ttk
import tkinter.filedialog
import math
import cmath
import time
import random
import numpy as np
from PIL import Image, ImageTk, ImageColor
from matplotlib import cm

# ---------- variables
hauteur_canvas, xmin_initial, xmax_initial, ymin_initial, ymax_initial = 800, -2.2, 0.8, -1.3, 1.3
#hauteur_canvas, xmin_initial, xmax_initial, ymin_initial, ymax_initial = 500, -1.20, -1.18, 0.29, 0.31
p = p_initial = 2                        # puissance p dans la formule: zn+1 = zn ^ p + c
rayon = rayon_initial = 2                # valeur du module pour laquelle on arrête les iterations
max_iterations = max_iterations_initial = 20     # nb max d'iterations

couleur_fond       = "#4040D0"
couleur_mandelbrot = "black"

xmin, xmax, ymin, ymax = xmin_initial, xmax_initial, ymin_initial, ymax_initial
largeur_canvas = int (hauteur_canvas * (xmax - xmin) / (ymax - ymin))   # on calcule la largeur pour conserver le ratio 
params = []

eps = 0.01

precision_faible = 5

color_factor = 500
logref = math.log(1+color_factor)

# ---------- fonctions

# ---- convertions entre coordonnees reelles et coordonnees graphiques
def x_to_xecran(x):
    return int((x - xmin) / (xmax - xmin) * largeur_canvas)

def y_to_yecran(y):
    return int(hauteur_canvas - (y - ymin) / (ymax - ymin) * hauteur_canvas)

def xecran_to_x(xe):
    return float(xe * (xmax - xmin) / largeur_canvas + xmin)

def yecran_to_y(ye):
    return float(ymax - ye * (ymax - ymin) / hauteur_canvas)

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

def get_color_from_iteration(nb_iterations):
    if nb_iterations == max_iterations:
        return couleur_mandelbrot
    else:
        color_index = int(nb_iterations / max_iterations * nb_colors)
#        color_index2 = int(nb_colors * math.log(color_factor*n/max_iterations + 1) / logref)
#                color_index2 = int(nb_colors * (math.exp(4 * n / max_iterations) - 1) / (math.exp(4) - 1))
        return colors [color_index] 

def calcule_et_affiche():
    global calcul_en_cours
    global selected_rectangle
    global canvas_dessin
    global myarray
    global img

    calcul_en_cours = True
    disable_buttons()
    calcul_en_cours_tv.set("CALCUL EN COURS : 0 %")
    fenetre.update()

    t1 = time.time()
    t2 = t1

    # cree un numpy array m_nb_iter contenant le nombre d'iterations pour chaque point x,y
    x = np.linspace(xmin, xmax, largeur_canvas+1)
    y = np.linspace(ymin, ymax, hauteur_canvas+1)

    ma, mb = np.meshgrid(x, y)
    mc = ma + mb*1j
    mz = np.zeros_like(mc)
    m_nb_iter = max_iterations + np.zeros(mz.shape, dtype=int)

    for i in range(max_iterations):
        mz = mz**p + mc
        diverge = abs(mz) > rayon                    
        div_now = diverge & (m_nb_iter == max_iterations) 
        m_nb_iter[div_now] = i                         
        mz[diverge] = rayon                                

    t3 = time.time()
    print (f"Calcul terminé : durée = {t3 - t1:.2f} s.")

    # Ensuite, cree et affiche une image a partir de cet array
    color_map = cm.rainbow  # cm.gist_earth 
    myarray = np.uint8(color_map(m_nb_iter / max_iterations)*255)
    img =  ImageTk.PhotoImage(image=Image.fromarray(myarray))
    canvas_dessin.create_image(0,0, anchor="nw", image=img)
    canvas_dessin.update()

    t4 = time.time()
    print (f"Affichage terminé t4: durée = {t4 - t3:.2f} s.")

    calcul_en_cours_tv.set("CALCUL EN COURS : 100 %")
    calcul_en_cours_label.update()

    #img = _photo_image(myarray)
    #canvas_dessin.create_image(largeur_canvas, hauteur_canvas, image=img)
    # canvas_dessin.update()

    calcul_en_cours = False
    calcul_en_cours_tv.set("")
    enable_buttons()

# ---- divers
def efface_et_resize_canvas():
    global canvas_dessin
    global current_pos_tv

    # on peut sauver une image seulement apres un calcul précis
    save_button["state"] = tkinter.DISABLED

    canvas_dessin.delete("all")
    canvas_dessin.config(width = largeur_canvas)
    current_pos_tv.set("COORDONNEES SOURIS:\n\nx  :                    \n\ny  : ")

def disable_buttons():
    valide_params_btn["state"] = tkinter.DISABLED
    params_initiaux_btn["state"] = tkinter.DISABLED
    
def enable_buttons():
    valide_params_btn["state"] = tkinter.NORMAL
    params_initiaux_btn["state"] = tkinter.NORMAL

def sauve_params():
    global params
    params.append ([ xmin, xmax, ymin, ymax, rayon, p, max_iterations ])
    params_precedents_btn["state"] = tkinter.NORMAL

# ---- selection avec la souris d'une zone a zoomer 
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
    selected_area_tv.set(f"ZONE SELECTIONNEE POUR LE ZOOM:\n\nx1 : {xsel1: .16f}\n\ny1 : {ysel1: .16f}\n\nx2 : \n\ny2 : ")
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
    selected_area_tv.set(f"ZONE SELECTIONNEE POUR LE ZOOM:\n\nx1 : {xsel1: .16f}\n\ny1 : {ysel1: .16f}\n\nx2 : {xsel2: .16f}\n\ny2 : {ysel2: .16f}")

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

    selected_area_tv.set("ZONE SELECTIONNEE POUR LE ZOOM:\n\nx1 :                    \n\ny1 : \n\nx2 : \n\ny2 : ")

    selected_area_x2 = event.x
    selected_area_y2 = event.y

    # si les points départ et arrivés sont confondus, on annule la selection
    if selected_area_x2 == selected_area_x1 and selected_area_y2 == selected_area_y1:
        selected_area_x1 = selected_area_x2 = selected_area_y1 = selected_area_y2 = -1
    
    else:
        minx = min(selected_area_x1, selected_area_x2)
        maxx = max(selected_area_x1, selected_area_x2)
        # print (f"DEBUG: x1={selected_area_x1} x2={selected_area_x2} y1={selected_area_y1} y1={selected_area_y2} min={minx} max={maxx}")

        xmin_new = xecran_to_x(min(selected_area_x1, selected_area_x2))
        xmax_new = xecran_to_x(max(selected_area_x1, selected_area_x2))
        ymin_new = yecran_to_y(max(selected_area_y1, selected_area_y2))
        ymax_new = yecran_to_y(min(selected_area_y1, selected_area_y2))
        sauve_params()
        xmin, xmax, ymin, ymax = xmin_new, xmax_new, ymin_new, ymax_new
        largeur_canvas = int (hauteur_canvas * (xmax - xmin) / (ymax - ymin))   # on calcule la largeur pour conserver le ratio 
        zoom_display_area_coords()
        efface_et_resize_canvas()
        calcule_et_affiche()

# ---- gestion des parametres utilisés pour les calculs
def zoom_display_area_coords():
    params_tv[0].set(f"{xmin: .16f}")
    params_tv[1].set(f"{xmax: .16f}")
    params_tv[2].set(f"{ymin: .16f}")
    params_tv[3].set(f"{ymax: .16f}")
    params_tv[4].set(f"{rayon}")
    params_tv[5].set(f"{p}")
    params_tv[6].set(f"{max_iterations}")

def params_reset():
    global xmin
    global xmax
    global ymin
    global ymax   
    global rayon
    global p
    global max_iterations
    global largeur_canvas

    xmin, xmax, ymin, ymax = xmin_initial, xmax_initial, ymin_initial, ymax_initial
    rayon, p, max_iterations = rayon_initial, p_initial, max_iterations_initial
    largeur_canvas = int (hauteur_canvas * (xmax - xmin) / (ymax - ymin))   # on calcule la largeur pour conserver le ratio 
    zoom_display_area_coords()
    efface_et_resize_canvas()
    calcule_et_affiche()

def params_precedents():
    global xmin
    global xmax
    global ymin
    global ymax
    global rayon
    global p
    global max_iterations
    global largeur_canvas

    if len(params) > 0:
        xmin, xmax, ymin, ymax, rayon, p, max_iterations = params.pop()
        if len(params) == 0:
            params_precedents_btn["state"] = tkinter.DISABLED    
        zoom_display_area_coords()
        largeur_canvas = int (hauteur_canvas * (xmax - xmin) / (ymax - ymin))   # on calcule la largeur pour conserver le ratio 
        efface_et_resize_canvas()
        calcule_et_affiche()

def valide_params():
    global xmin
    global xmax
    global ymin
    global ymax
    global rayon
    global p
    global max_iterations
    global largeur_canvas

    try:
        xmin_tmp = float(params_tv[0].get())
        xmax_tmp = float(params_tv[1].get())
        ymin_tmp = float(params_tv[2].get())
        ymax_tmp = float(params_tv[3].get())
        rayon_tmp = float(params_tv[4].get())
        p_tmp     = int(params_tv[5].get())
        max_iterations_tmp = int(params_tv[6].get())
    except Exception as err:
        tkinter.messagebox.showerror(title="Paramètres invalides", message="ERREUR: les paramètres sont invalides ! "+str(err))
        return

    # vérifie validité des paramètres
    if xmin_tmp >= xmax_tmp or ymin_tmp >= ymax_tmp:
        tkinter.messagebox.showerror(title="Paramètres invalides", message="ERREUR: les paramètres sont invalides !")
        return

    # si les params sont valides, on les accepte
    sauve_params()
    xmin, xmax, ymin, ymax, rayon = xmin_tmp, xmax_tmp, ymin_tmp, ymax_tmp, rayon_tmp
    p, max_iterations             = p_tmp, max_iterations_tmp
    largeur_canvas = int (hauteur_canvas * (xmax - xmin) / (ymax - ymin))   # on calcule la largeur pour conserver le ratio 
    efface_et_resize_canvas()
    calcule_et_affiche()

# ---- Sauvegarde de l'image cree avec calcul precis dans un fichier .png
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

# ---- Fin du programme après confirmation
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
    params_names = [ "Xmin        : ", "Xmax        : ", "Ymin        : ", "Ymax        : ", "Rayon R     : ", "Puissance P : ", "Itérations  : "]
    font_cn16 = tkinter.font.Font(family='Courier new', size=16)
    font_ar16 = tkinter.font.Font(family='Arial', size=16)
    font_ar18 = tkinter.font.Font(family='Arial', size=18)
    font_ar20 = tkinter.font.Font(family='Arial', size=20, weight='bold')
    params_tv = []
    for i in range(len(params_names)):
        params_tv.append(tkinter.StringVar())
    params_tv[4].set(rayon_initial);            # R: valeur du module ou l'on arrête les iterations
    params_tv[5].set(p_initial);                # P: puissance p dans la formule Zn+1 = Zn^p + c
    params_tv[6].set(max_iterations_initial);   # nb max d'iterations

    current_pos_tv     = tkinter.StringVar()
    calcul_en_cours_tv = tkinter.StringVar()
    selected_area_tv   = tkinter.StringVar()

    zoom_display_area_coords()
    current_pos_tv.set("COORDONNEES SOURIS:\n\nx  :                    \n\ny  : ")
    calcul_en_cours_tv.set("")
    selected_area_tv.set("ZONE SELECTIONNEE POUR LE ZOOM:\n\nx1 :                    \n\ny1 : \n\nx2 : \n\ny2 : ")

    frame_controle = tkinter.Frame(fenetre, bg = couleur_frame)
    frame_controle.pack(side = tkinter.LEFT, fill = tkinter.Y)

    formule_label   = tkinter.Label (frame_controle, anchor = tkinter.W, font = font_cn16, text = "Zn+1 = Zn ^ p + c", bg = couleur_frame, fg = couleur_selection)
    params_frame      = tkinter.Frame(frame_controle, bg = couleur_frame)
    for i in range(len(params_names)):
        tkinter.Label (params_frame, anchor = tkinter.W, font = font_cn16, text = params_names[i], bg = couleur_frame, fg = couleur_texte).grid(sticky = tkinter.N+tkinter.W, column=0, row=i, pady = 5)
        tkinter.Entry (params_frame, justify = tkinter.LEFT, font = font_cn16, width = 26 - len(params_names[i]), bg = couleur_frame, fg = couleur_texte, relief = tkinter.FLAT, highlightcolor = "red", textvariable = params_tv[i]).grid(sticky = tkinter.N+tkinter.W+tkinter.E, column=1, row=i, pady = 5)
    valide_params_btn     = tkinter.Button(frame_controle, text = "VALIDE PARAMETRES",     font = font_ar18, height = 2, fg = "green", command = valide_params)
    params_initiaux_btn   = tkinter.Button(frame_controle, text = "PARAMETRES INITIAUX",   font = font_ar18, height = 2, fg = "green", command = params_reset)
    params_precedents_btn = tkinter.Button(frame_controle, text = "PARAMETRES PRECEDENTS", font = font_ar18, height = 2, fg = "green", command = params_precedents)
    params_precedents_btn["state"] = tkinter.DISABLED
    save_quit_frame       = tkinter.Frame (frame_controle, bg = couleur_frame)
    save_button           = tkinter.Button(save_quit_frame, text = "SAUVER",  font = font_ar18, height = 2,  fg = "green", command = sauver_png, state = tkinter.DISABLED)
    quit_button           = tkinter.Button(save_quit_frame, text = "QUITTER", font = font_ar18, height = 2,  fg = "red",   command = quitter)
    current_pos_label     = tkinter.Label (frame_controle, justify = tkinter.LEFT, font = font_cn16, textvariable = current_pos_tv, bg = couleur_frame, fg = couleur_coords_souris)
    calcul_en_cours_label = tkinter.Label (frame_controle, justify = tkinter.CENTER, font = font_ar20, textvariable = calcul_en_cours_tv, bg = couleur_frame, fg = couleur_calcul_en_cours)
    selected_area_label   = tkinter.Label (frame_controle, justify = tkinter.LEFT, font = font_cn16, textvariable = selected_area_tv, bg = couleur_frame, fg = couleur_selection)
    separator1            = tkinter.ttk.Separator (frame_controle, orient = 'horizontal')
    separator1b           = tkinter.ttk.Separator (frame_controle, orient = 'horizontal')
    separator2            = tkinter.ttk.Separator (frame_controle, orient = 'horizontal')
    separator3            = tkinter.ttk.Separator (frame_controle, orient = 'horizontal')
    separator4            = tkinter.ttk.Separator (frame_controle, orient = 'horizontal')

    formule_label.pack        (side = tkinter.TOP, padx = 20, pady = 10,  fill = tkinter.X)
    separator1.pack           (side = tkinter.TOP, padx = 0,  pady = 5,   fill = tkinter.X)
    params_frame.pack         (side = tkinter.TOP, padx = 20, pady = 0,   fill = tkinter.X)
    valide_params_btn.pack    (side = tkinter.TOP, padx = 20, pady = 10,  fill = tkinter.X)
    separator1b.pack          (side = tkinter.TOP, padx = 0,  pady = 5,   fill = tkinter.X)
    params_initiaux_btn.pack  (side = tkinter.TOP, padx = 20, pady = 10,  fill = tkinter.X)
    params_precedents_btn.pack(side = tkinter.TOP, padx = 20, pady = 10,  fill = tkinter.X)
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
    separator5    = tkinter.ttk.Separator (fenetre, orient = 'vertical')
    separator5.pack (side = tkinter.LEFT, padx = 0,  pady = 0,   fill = tkinter.Y)
    canvas_dessin = tkinter.Canvas(fenetre, bg = "black", highlightthickness = 0)
    canvas_dessin.pack(side = tkinter.LEFT, padx = 20)
    canvas_dessin.config(width = largeur_canvas, height = hauteur_canvas)

    # ---- Events souris dans le canvas
    canvas_dessin.bind('<Motion>', affiche_position_souris_in_canvas)
    canvas_dessin.bind('<ButtonPress-1>',   select_area_start)
    canvas_dessin.bind('<B1-Motion>',       select_area_change)
    canvas_dessin.bind('<ButtonRelease-1>', select_area_end)

    # ---- On affiche l'ensemble de Mandelbrot en calcul rapide après n ms
    fenetre.after (500, calcule_et_affiche)

    # ---- Boucle de la fenetre graphique
    fenetre.mainloop()


