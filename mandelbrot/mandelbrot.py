#!/usr/bin/env python3
#
# -*- coding: utf-8 -*-
# --------------------------------------------------------------------------------------------------------------------------
# Ce programme dessine l'ensemble de Mandelbrot et permet de zoomer dessus
#
# Auteur : Christophe Pauliat
# Date   : Avril 2021
# --------------------------------------------------------------------------------------------------------------------------


# ---------- modules
import tkinter 
import tkinter.font
import tkinter.messagebox
import tkinter.ttk
import math
import cmath
import time
import random

# ---------- variables
#hauteur_canvas, xmin, xmax, ymin, ymax = 1200, -2.2, 0.8, -0.1, 1.3
#hauteur_canvas, xmin, xmax, ymin, ymax = 1400, -1, 0, 0, 1
hauteur_canvas, xmin0, xmax0, ymin0, ymax0 = 1000, -2.2, 0.8, -1.3, 1.3

cpt_max = 100   # nb max d'iterations

couleur_fond = "#4040D0"
couleur_axe = "white"

xmin, xmax, ymin, ymax = xmin0, xmax0, ymin0, ymax0
largeur_canvas = int (hauteur_canvas * (xmax - xmin) / (ymax - ymin))   # on calcule la largeur pour conserver le ratio 
coords = []

# ---------- fonctions
def colors_palette1():
    for i in range(40):
        r = random.randint(0,255)
        v = random.randint(0,255)
        b = random.randint(0,255)
        colors.append(f"#{r:02x}{v:02x}{b:02x}")

def colors_palette2():
    for i in range(100,240,5):
        r = 0
        v = 0
        b = i
        colors.append(f"#{r:02x}{v:02x}{b:02x}")
    for i in range(100,255,2):
        r = 0
        v = i
        b = 0
        colors.append(f"#{r:02x}{v:02x}{b:02x}")
    for i in range(100,255,1):
        r = i
        v = 0
        b = 0
        colors.append(f"#{r:02x}{v:02x}{b:02x}")

def colors_palette3():
    # on passe du bleu au rouge
    # for i in range(100,255,2):
    #     r = i
    #     v = 0
    #     b = 255-i
    for i in range(0,100,1):
        r = int(2.5*i)
        v = 0
        b = 50 - i//2
        colors.append(f"#{r:02x}{v:02x}{b:02x}")
    colors.append("white")
    # on passe du rouge au vert
    for i in range(0,255,1):
        r = 255-i
        v = i
        b = 0
        colors.append(f"#{r:02x}{v:02x}{b:02x}")

def mandelbrot_color_orig(x,y):
    # Zn = Xn + i * Yn
    xn = yn = 0     # z0 = 0
    cx  = x
    cy  = y 

    cpt = 0

    modzn2 = 0      # module de Zn au carré (= Xn^2 + Yn^2)
    while (cpt < cpt_max) and (xn * xn + yn * yn <= 4):
        # Zn+1 = Zn^2 + c
        # Zn   = Xn + i * Yn
        # c    = Cx + i * Cy
        # Zn+1 = Xn+1 + i * Yn+1
        # Xn+1 = Xn^2 - Yn^2 + Cx
        # Yn+1 = 2 * Xn * Yn + Cy
        xnp1 = xn * xn - yn * yn + cx
        ynp1 = 2 * xn * yn + cy
        xn = xnp1
        yn = ynp1
        cpt += 1

    if cpt == cpt_max:
        return "black"
    else:
        color_index = int(cpt / cpt_max * nb_colors)
        return colors [color_index] 

def mandelbrot_color(x,y):
    zn = 0
    c  = x + y * 1j
    n  = 0

    while (n < cpt_max) and (abs(zn) <= 2):
        # Zn+1 = Zn^2 + c
        #zn = zn * zn * zn * zn + c
        zn = zn * zn * cmath.sqrt(zn) + c
        n += 1

    if n == cpt_max:
        return "black"
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

    canvas_dessin.delete("all")
    canvas_dessin.config(width = largeur_canvas)

def disable_buttons():
    reset_button["state"] = tkinter.DISABLED
    zoom_out_button["state"] = tkinter.DISABLED
    cc_precis_button["state"] = tkinter.DISABLED
    
def enable_buttons():
    reset_button["state"] = tkinter.NORMAL
    zoom_out_button["state"] = tkinter.NORMAL
    cc_precis_button["state"] = tkinter.NORMAL

def dessine_mandelbrot(xprecision, yprecision):
    global calcul_en_cours
    global selected_rectangle
    global canvas_dessin

    print (f"Calcul démarré")
    calcul_en_cours = True
    disable_buttons()
    calcul_en_cours_tv.set("CALCUL EN COURS\n\n0%")
    fenetre.update()

    t1 = time.time()
    t2 = t1
    for xe in range(0,largeur_canvas,xprecision):
        for ye in range(0,hauteur_canvas,yprecision):
            x = xecran_to_x(xe)
            y = yecran_to_y(ye)
            color = mandelbrot_color(x,y)
            canvas_dessin.create_rectangle(xe, ye, xe+xprecision, ye+yprecision, outline = color, fill = color)
        t3 = time.time()
        # toutes les secondes, on refresh l'écran
        if t3 - t2 > 1:
            t2 = t3
            canvas_dessin.update()
            pct = int(xe / largeur_canvas * 100)
            calcul_en_cours_tv.set(f"CALCUL EN COURS\n\n{pct}%")
            calcul_en_cours_label.update()

    t4 = time.time()
    print (f"Calcul terminée: durée = {t4 - t1:.2f} s.")

    calcul_en_cours_tv.set("CALCUL EN COURS\n\n100%")
    calcul_en_cours_label.update()

    canvas_dessin.update()

    calcul_en_cours = False
    calcul_en_cours_tv.set("\n\n")
    enable_buttons()

def calcule_rapide():
    dessine_mandelbrot(5, 5)

def calcule_precis():
    dessine_mandelbrot(1, 1)

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

    xe = event.x
    ye = event.y
    x  = xecran_to_x(xe)
    y  = yecran_to_y(ye)
    current_pos_tv.set(f"COORDONNEES SOURIS:\n\nxe : {xe}\n\nye : {ye}\n\nx  : {x: .12f}\n\ny  : {y: .12f}")

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
    selected_area_tv.set(f"ZONE SELECTIONNEE:\n\nx1 : {xsel1: .12f}\n\ny1 : {ysel1: .12f}\n\nx2 : \n\ny2 : ")
    selected_rectangle = canvas_dessin.create_rectangle(selected_area_x1, selected_area_y1, selected_area_x1 + 1, selected_area_y1 + 1, fill="", outline = "white")

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
    selected_area_tv.set(f"ZONE SELECTIONNEE:\n\nx1 : {xsel1: .12f}\n\ny1 : {ysel1: .12f}\n\nx2 : {xsel2: .12f}\n\ny2 : {ysel2: .12f}")

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

    #selected_area_tv.set(" \n\n \n\n \n\n \n\n ")
    selected_area_tv.set("ZONE SELECTIONNEE:\n\nx1 : \n\ny1 : \n\nx2 : \n\ny2 : ")

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
    dimensions_tv.set(f"\nZONE ECRAN:\n\nXmin : {xmin: .12f}\n\nXmax : {xmax: .12f}\n\nYmin : {ymin: .12f}\n\nYmax : {ymax: .12f}")

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

# ---- Fin du programme après confirmation
def quitter():
    if tkinter.messagebox.askyesno("Fin du programme","Voulez-vous vraiment quitter l'application ?"): 
        fenetre.destroy()

# ---------- programme principal

if __name__ == '__main__':

    # ---- other variables
    colors = [ ]
    colors_palette3()
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
    fenetre.config(bg="black")
    fenetre.resizable(width=False, height=False)    # on empeche le redimensionnement manuel de la fenetre

    # ---- frame de controle
    font_cn16 = tkinter.font.Font(family='Courier new', size=16)
    font_ar18 = tkinter.font.Font(family='Arial', size=18)
    font_ar20 = tkinter.font.Font(family='Arial', size=20, weight='bold')
    dimensions_tv      = tkinter.StringVar()
    current_pos_tv     = tkinter.StringVar()
    calcul_en_cours_tv = tkinter.StringVar()
    selected_area_tv   = tkinter.StringVar()

    zoom_display_area_coords()
    #current_pos_tv.set(" \n\n \n\n \n\n \n\n ")
    current_pos_tv.set("COORDONNEES SOURIS:\n\nxe : \n\nye : \n\nx  : \n\ny  : ")
    calcul_en_cours_tv.set("\n\n")
    #selected_area_tv.set(" \n\n \n\n \n\n \n\n ")
    selected_area_tv.set("ZONE SELECTIONNEE:\n\nx1 : \n\ny1 : \n\nx2 : \n\ny2 : ")

    frame_controle = tkinter.Frame(fenetre, bg=couleur_frame)
    frame_controle.pack(side=tkinter.LEFT, fill=tkinter.Y)

    quit_button           = tkinter.Button(frame_controle, text = "QUITTER", font = font_ar18, height = 2,  command = quitter)
    reset_button          = tkinter.Button(frame_controle, text = "ZOOM RESET", font = font_ar18, height = 2, width = 20, command = zoom_reset)
    zoom_out_button       = tkinter.Button(frame_controle, text = "ZOOM OUT",   font = font_ar18, height = 2, command = zoom_out)
    dimensions_label      = tkinter.Label (frame_controle, justify = tkinter.LEFT, font = font_cn16, textvariable = dimensions_tv, bg = couleur_frame, fg = couleur_texte)
    cc_precis_button      = tkinter.Button(frame_controle, text = "CALCUL PRECIS", font = font_ar18, height = 2, command = calcule_precis)
    current_pos_label     = tkinter.Label (frame_controle, justify = tkinter.LEFT, font = font_cn16, textvariable = current_pos_tv, bg = couleur_frame, fg = couleur_coords_souris)
    calcul_en_cours_label = tkinter.Label (frame_controle, justify = tkinter.CENTER, font = font_ar20, textvariable = calcul_en_cours_tv, bg = couleur_frame, fg = couleur_calcul_en_cours)
    selected_area_label   = tkinter.Label (frame_controle, justify = tkinter.LEFT, font = font_cn16, textvariable = selected_area_tv, bg = couleur_frame, fg = couleur_selection)
    separator1            = tkinter.ttk.Separator (frame_controle,orient='horizontal')
    separator2            = tkinter.ttk.Separator (frame_controle,orient='horizontal')
    separator3            = tkinter.ttk.Separator (frame_controle,orient='horizontal')
    separator4            = tkinter.ttk.Separator (frame_controle,orient='horizontal')

    dimensions_label.pack     (side=tkinter.TOP, padx=20, pady=10,  fill=tkinter.X)
    separator1.pack           (side=tkinter.TOP, padx=0,  pady=5,   fill=tkinter.X)
    quit_button.pack          (side=tkinter.TOP, padx=20, pady=10,  fill=tkinter.X)
    reset_button.pack         (side=tkinter.TOP, padx=20, pady=10,  fill=tkinter.X)
    zoom_out_button.pack      (side=tkinter.TOP, padx=20, pady=10,  fill=tkinter.X)
    cc_precis_button.pack     (side=tkinter.TOP, padx=20, pady=10,  fill=tkinter.X)
    separator2.pack           (side=tkinter.TOP, padx=0,  pady=5,   fill=tkinter.X)
    current_pos_label.pack    (side=tkinter.TOP, padx=20, pady=10,  fill=tkinter.X)
    separator3.pack           (side=tkinter.TOP, padx=0,  pady=0,   fill=tkinter.X)
    calcul_en_cours_label.pack(side=tkinter.TOP, padx=20, pady=10,  fill=tkinter.X)
    separator4.pack           (side=tkinter.TOP, padx=0,  pady=0,   fill=tkinter.X)
    selected_area_label.pack  (side=tkinter.TOP, padx=20, pady=20,  fill=tkinter.X)

    # ---- canvas pour dessiner
    xe0 = x_to_xecran(0)
    ye0 = y_to_yecran(0)
    canvas_dessin = tkinter.Canvas(fenetre, bg="black", highlightthickness=0)
    canvas_dessin.pack(side=tkinter.LEFT)
    canvas_dessin.config(width=largeur_canvas, height=hauteur_canvas)

    # ---- Events souris dans le canvas
    canvas_dessin.bind('<Motion>', affiche_position_souris_in_canvas)
    canvas_dessin.bind('<ButtonPress-1>',   select_area_start)
    canvas_dessin.bind('<B1-Motion>',       select_area_change)
    canvas_dessin.bind('<ButtonRelease-1>', select_area_end)

    # ---- On affiche l'ensemble de Mandelbrot en calcul rapide après n ms
    fenetre.after (500, calcule_rapide)

    # ---- Boucle de la fenetre graphique
    fenetre.mainloop()


