#!/usr/bin/env python3
#
# -*- coding: utf-8 -*-
# --------------------------------------------------------------------------------------------------------------------------
# Ce programme dessine le déplacement de la terre autour du soleil en subissant l'attraction universelle
# On se place dans un référentiel solaire (soleil immobile)
#
# Ce programme utilise l'interface graphique Tkinter
#
# Auteur        : Christophe Pauliat
# Platformes    : Linux / Windows / MacOS
#
# IMPORTANT: Pour MacOS, utiliser python3 et tkinter depuis https://python.org car le Tk fourni par Apple a des bugs
#            cf. https://www.python.org/download/mac/tcltk/
#
# Versions
#    2020-04-13: version initiale
#
# https://astronomia.fr/7eme_partie/formulaire.php
# a lire : https://stackoverflow.com/questions/5436810/adding-zooming-in-and-out-with-a-tkinter-canvas-widget
# --------------------------------------------------------------------------------------------------------------------------
#
#
# ---------- modules
import tkinter 
from tkinter.font import *
import math
import time
import sys
from functools import partial

# ---------- variables
xe_max      = 1900               # largeur de la fenetre graphique
ye_max      = 1200               # hauteur de la fenetre graphique
xe_soleil   = 1100               # Position X du centre du soleil dans la fenetre graphique
ye_soleil   = 600                # Position Y du centre du soleil dans la fenetre graphique
timer       = 20                 # durée (en ms) entre 2 affichages de position de la planète
delta_temps = 10                 # durée entre 2 calculs de position (en heures)
echelle     = 1e9                # 1 pixel réprésente 1 million de km
zoom        = 100                # zoom en % (25, 50, 100, 200, 400 ou 800)
pause       = False              # pour mettre l'animation en pause

# ---------- classe planete
class planete:

    def __init__(self, nom, a, e, ech, xes, yes, dt):
        # nom de la planète
        # a        = distance demi-grand axe de l'orbite elliptique
        # e        = excentricité orbité elliptique
        # ech      = échelle utilisée (distance en m pour 1 pixel)
        # xe, ye   = coordonnées écran du centre de la planète
        # xes, yes = coordonnées écran du centre du soleil
        # dt       = durée entre 2 calculs de position (en heures)

        # constantes
        self.m_soleil = 1.9891e30          # masse du soleil (en kg)
        self.g = 6.67259e-11               # constante de gravitation universelle (en N.m2.kg-2 ou m3.kg-1.s-2)
        self.xe_soleil = xes               # Position X du centre du soleil dans la fenetre graphique
        self.ye_soleil = yes               # Position Y du centre du soleil dans la fenetre graphique
        
        # paramètres repris tels quels
        self.nom = nom
        self.e = e                          # excentricité de l'orbite elliptique
        self.a = a                          # demi-grand axe de l'orbite elliptique
        self.echelle_no_zoom = ech
        self.echelle = ech

        # paramètres calculés
        self.dt = 3600 * dt                 # durée entre 2 calculs de position (en s), agit sur la vitesse d'animation
        self.c = e * a                      # focale c de l'orbite elliptique
        self.t0 = 0                         # temps en heure
        self.dernier_quart_orbite = False   # utilisé pour la correction de trajectoire au perihelie
        self.second_quart_orbite = False    # utilisé pour la correction de trajectoire a l'aphelie
        self.premiere_orbite = True         # utilise pour l'affichage de l'orbite

        self.d_perihelie = a - self.c       # position exacte au perihelie
        self.d_aphelie = a + self.c         # position exacte a l'aphelie
        self.d  = self.d_perihelie          # position initiale au périhélie
        self.dx = -self.d                   # position initale sur l'axe Tx sur la gauche
        self.dy = 0                         # position initale sur l'axe Tx sur la gauche
        self.d_min = self.d
        self.d_max = self.d

        self.v_perihelie = math.sqrt(self.g * self.m_soleil * (1 + self.e) / (1 - self.e) / self.a)    # vitesse au périhélie
        self.v_aphelie   = math.sqrt(self.g * self.m_soleil * (1 - self.e) / (1 + self.e) / self.a)    # vitesse au périhélie
        self.v  = self.v_perihelie          # la vitesse initiale est celle au périhélie
        self.vx = 0                         # vitesse initale vers le haut
        self.vy = self.v                    # vitesse initale vers le haut
        self.v_min = self.v
        self.v_max = self.v
                                 
        # on démarre au périhélie positioné a gauche du soleil (grand axe ellipse est horizontal)
        self.xe = xe_soleil - int(self.d_perihelie / self.echelle) # Position X du centre de la planete dans la fenetre graphique
        self.ye = ye_soleil                                        # Position X du centre de la planete dans la fenetre graphique

        self.pause = False

    # accélère ou ralentit la vitesse des planètes à l'écran
    def modifie_delta_temps(self, dt):
        self.dt = 3600 * dt

    # met le calcul de position en pause ou fin de la pause
    def modifie_pause(self, pause):
        self.pause = pause

    # modifie l'echelle en fonction du zoom exprimé en pourcentages
    def modifie_echelle(self, zoom):
        self.echelle = self.echelle_no_zoom * 100 / zoom
        self.premiere_orbite = True

    def calcule_nelle_position(self):

        # si on est en pause, on ne fait rien
        if self.pause: return

        # angle entre vecteur acceleration et axe (Tx) en radians 
        # les vecteurs accelerations et OT sont colinéaires meme sens.
        # - dans le atan() car l'axe des y et l'axe des ye sont sens opposés
        beta = math.atan2 (- (self.ye_soleil - self.ye) , (self.xe_soleil - self.xe))

        # vecteur acceleration: l'acceleration de la planète est a = g * m_soleil / d_terre^2
        acc = self.g * self.m_soleil / self.d**2
        acc_x = acc * math.cos(beta)
        acc_y = acc * math.sin(beta)

        # temps en heures
        self.t0 += self.dt / 3600

        # -- nouveau vecteur vitesse: v = v + dt * a    (dt = delta temps, v = vecteur vitesse, acc = vecteur acceleration)
        self.vx += self.dt * acc_x
        self.vy += self.dt * acc_y

        self.v = math.sqrt(self.vx**2 + self.vy**2)
        self.v_min = min(self.v, self.v_min)
        self.v_max = max(self.v, self.v_max)

        # -- nouvelle position vecteur p (dx,dy) de la planète: p = p + dt * v (vecteurs p et v)
        self.dx += self.dt * self.vx
        self.dy += self.dt * self.vy

        self.d = math.sqrt(self.dx**2 + self.dy**2)
        self.d_min = min(self.d, self.d_min)
        self.d_max = max(self.d, self.d_max)

        # -- correction de trajectoire au périhélie pour éviter déviation orbite à cause erreurs d'arrondi
        if self.dx < 0 and self.dy < 0:
            self.dernier_quart_orbite = True

        if self.dernier_quart_orbite and self.dy >= 0:
            self.v  = self.v_perihelie
            self.vx = 0                         
            self.vy = self.v   

            self.d  = self.d_perihelie       
            self.dx = -self.d                   
            self.dy = 0 

            self.dernier_quart_orbite = False
            #self.premiere_orbite = False
            #print ("Correction de trajectoire pour "+self.nom)

        # -- correction de trajectoire a l'aphelie pour éviter déviation orbite à cause erreurs d'arrondi
        if self.dx > 0 and self.dy > 0:
            self.second_quart_orbite = True

        if self.second_quart_orbite and self.dy <= 0:
            self.v  = self.v_aphelie
            self.vx = 0                         
            self.vy = -self.v   

            self.d  = self.d_aphelie       
            self.dx = self.d                   
            self.dy = 0 

            self.second_quart_orbite = False
            #self.premiere_orbite = False
            #print ("Correction de trajectoire pour "+self.nom)

        # -- nouvelle position de la terre sur l'ecran
        self.de = int(self.d / self.echelle)
        self.xe = int(self.xe_soleil + self.dx / self.echelle)
        self.ye = int(self.ye_soleil - self.dy / self.echelle)

    # -- ON affiche les paramètres
    #message = "Temps (depuis début) : {:.1f} jours \n\n".format(t0 / 24) + \
    #          "Durée d'une orbite   : {:.1f} jours \n\n".format(duree_orbite / 24) + \
    #          "Distance soleil-terre: {:.0f} km \n".format(d_terre / 1000) + \
    #          "   minimum (périhélie) : {:.0f} km \n".format(d_terre_min / 1000) + \
    #          "   maximum (apogée)  : {:.0f} km \n\n".format(d_terre_max / 1000) + \
    #          "Vitesse terre        : {:4.0f} m/s-1 ou {:4.0f} km/h\n".format(v_terre, v_terre * 3.6) + \
    #          "   minimum (apogée)  : {:4.0f} m/s-1 ou {:4.0f} km/h\n".format(v_terre_min, v_terre_min * 3.6) + \
    #          "   maximum (périhélie) : {:4.0f} m/s-1 ou {:4.0f} km/h".format(v_terre_max, v_terre_max * 3.6)
    #label.config(text=message)

    # -- on re-appelle cette fonction au bout d'un certain temps
    #main_window.after(timer, dessine_terre)

# ---------- fonctions
def animation_demarre(planete, fichier_gif):
    global drawing_canvas

    photo_image = tkinter.PhotoImage(file=fichier_gif)
    image = drawing_canvas.create_image(planete.xe, planete.ye, anchor=tkinter.CENTER, image=photo_image)
    text = drawing_canvas.create_text(planete.xe + 30, planete.ye + 20, text=planete.nom, font=Font(family='Arial', size=14), fill="red")
    animation_continue(planete, image, photo_image, text)

def animation_continue(planete, image, photo_image, text):
    global main_window
    global drawing_canvas
    global timer

    # IMPORTANT: bien que la variable photo_image ne soit pas utilisee ici, il faut la passer en argument
    # pour eviter que le garbage collector de Python ne la supprime et que l'image disparaisse a l'ecran 

    # dessine un point à l'ancienne position pour matérialiser la premiere orbite
    if planete.premiere_orbite:
        drawing_canvas.create_line (planete.xe, planete.ye, planete.xe+1, planete.ye+1, fill="#606060", tags = "delete_on_zoom")

    # calcule la nouvelle position
    planete.calcule_nelle_position()

    # on deplace la planete 
    drawing_canvas.coords(image, planete.xe, planete.ye)

    # on déplace le texte indiquant le nom de la planète (x et Y sont relatifs a la position actuelle)
    drawing_canvas.coords(text, planete.xe + 30, planete.ye + 20)

    # re-appelle cette fonction dans un certain temps
    main_window.after(timer, animation_continue, planete, image, photo_image, text)

def modifie_zoom(op, txt):
    global zoom
    global drawing_canvas

    # zoom = 25, 50, 100, 200, 400 ou 800
    if op == "+":
        if zoom < 800: zoom = zoom * 2
    else:
        if zoom > 25: zoom = zoom // 2 

    drawing_canvas.itemconfigure (txt, text="zoom: {:d} %".format(zoom))

    # on supprime les lignes montrants les orbites
    drawing_canvas.delete("delete_on_zoom")

    mercure.modifie_echelle(zoom)
    venus.modifie_echelle(zoom)
    terre.modifie_echelle(zoom)
    mars.modifie_echelle(zoom)
    jupiter.modifie_echelle(zoom)

def modifie_vitesse(op, txt):
    global delta_temps
    global drawing_canvas

    if op == "+":
        if delta_temps < 1024: delta_temps = delta_temps * 2
    else:
        if delta_temps > 1: delta_temps = delta_temps // 2

    drawing_canvas.itemconfigure (txt, text="delta temps: {:d} h".format(delta_temps))
    mercure.modifie_delta_temps(delta_temps)
    venus.modifie_delta_temps(delta_temps)
    terre.modifie_delta_temps(delta_temps)
    mars.modifie_delta_temps(delta_temps)
    jupiter.modifie_delta_temps(delta_temps)

def pause_continue():
    global pause
    global bt_pause

    if pause:
        pause = False
        bt_pause.config(text="Pause")
    else:
        pause = True
        bt_pause.config(text="Continue")
    
    mercure.modifie_pause(pause)
    venus.modifie_pause(pause)
    terre.modifie_pause(pause)
    mars.modifie_pause(pause)
    jupiter.modifie_pause(pause)

# ---------- programme principal
if __name__ == '__main__':
    # ---- Main Window
    main_window = tkinter.Tk()
    main_window.title('Attraction Universelle : Système Solaire')

    # ---- Drawing canvas
    drawing_frame = tkinter.Frame(main_window)
    drawing_frame.pack(side=tkinter.LEFT, padx=0, pady=0)

    drawing_canvas = tkinter.Canvas(drawing_frame, height=ye_max, width=xe_max, bg="black")
    drawing_canvas.pack(side=tkinter.LEFT)

    # ---- Label pour afficher les paramètres lunaires
    #message=""
    #label = tkinter.Label(drawing_canvas, text=message, font=Font(family='Courier new', size=14), justify=tkinter.LEFT, bg="black", fg="yellow")
    #drawing_canvas.create_window (20, ye_max - 210, window=label, anchor=tkinter.NW)

    # ---- rajout des boutons dans le canvas
    t_zoom = drawing_canvas.create_text  (90, 40, anchor=tkinter.NW, text="zoom: 100%", font=Font(family='Courier New', size=16), fill="yellow")
    t_dt   = drawing_canvas.create_text  (90, 80, anchor=tkinter.NW, text="delta temps: 10 h", font=Font(family='Courier New', size=16), fill="yellow")

    bt_zoom_p    = tkinter.Button (main_window, text="+", command=lambda: modifie_zoom("+", t_zoom))
    bt_zoom_m    = tkinter.Button (main_window, text="-", command=lambda: modifie_zoom("-", t_zoom))
    bt_vitesse_p = tkinter.Button (main_window, text="+", command=lambda: modifie_vitesse("+", t_dt))
    bt_vitesse_m = tkinter.Button (main_window, text="-", command=lambda: modifie_vitesse("-", t_dt))
    bt_pause     = tkinter.Button (main_window, text="Pause",     command=pause_continue)
    bt_quit      = tkinter.Button (main_window, text="Quitter",   command=main_window.destroy)

    drawing_canvas.create_window(30, 40, anchor=tkinter.NW, window=bt_zoom_p)
    drawing_canvas.create_window(60, 40, anchor=tkinter.NW, window=bt_zoom_m)
    drawing_canvas.create_window(30, 80, anchor=tkinter.NW, window=bt_vitesse_p)
    drawing_canvas.create_window(60, 80, anchor=tkinter.NW, window=bt_vitesse_m)
    drawing_canvas.create_window(30,120, anchor=tkinter.NW, window=bt_pause)
    drawing_canvas.create_window(xe_max - 30, 40,  anchor=tkinter.NE, window=bt_quit)

    # ---- dessin des axes Tx, Ty
    drawing_canvas.create_line (0, ye_soleil, xe_max-1, ye_soleil, dash=(2, 2), fill="#000080")
    drawing_canvas.create_line (xe_soleil, 0, xe_soleil, ye_max-1, dash=(2, 2), fill="#000080")

    # ---- dessin du Soleil
    image_soleil = tkinter.PhotoImage(file="images/soleil.gif")
    drawing_canvas.create_image(xe_soleil, ye_soleil, anchor=tkinter.CENTER, image=image_soleil)

    # ---- Instantiation des planètes
    mercure = planete (nom="Mercure", a=57.90923e9, e=0.205604,    ech=echelle, xes=xe_soleil, yes=ye_soleil, dt=delta_temps)
    venus   = planete (nom="Vénus",   a=108.2095e9, e=0.00678,     ech=echelle, xes=xe_soleil, yes=ye_soleil, dt=delta_temps)
    terre   = planete (nom="Terre",   a=149.6e9,    e=0.016711236, ech=echelle, xes=xe_soleil, yes=ye_soleil, dt=delta_temps)
    mars    = planete (nom="Mars",    a=227.944e9,  e=0.09339,     ech=echelle, xes=xe_soleil, yes=ye_soleil, dt=delta_temps)
    jupiter = planete (nom="Jupiter", a=778.340e9,  e=0.04839,     ech=echelle, xes=xe_soleil, yes=ye_soleil, dt=delta_temps)
    saturne = planete (nom="Saturne", a=1426.7e9,   e=0.0539,      ech=echelle, xes=xe_soleil, yes=ye_soleil, dt=delta_temps)
    uranus  = planete (nom="Uranus",  a=2870.7e9,   e=0.04726,     ech=echelle, xes=xe_soleil, yes=ye_soleil, dt=delta_temps)
    neptune = planete (nom="Neptune", a=4498.4e9,   e=0.00859,     ech=echelle, xes=xe_soleil, yes=ye_soleil, dt=delta_temps)

    # ---- Affiche l'animation des planetes
    animation_demarre(mercure, "images/mercure.gif")
    animation_demarre(venus,   "images/venus.gif")
    animation_demarre(terre,   "images/terre.gif")
    animation_demarre(mars,    "images/mars.gif")
    animation_demarre(jupiter, "images/jupiter.gif")
    animation_demarre(saturne, "images/jupiter.gif")
    animation_demarre(uranus,  "images/jupiter.gif")
    animation_demarre(neptune, "images/jupiter.gif")

    # ---- Boucle de la fenetre graphique
    main_window.mainloop()
