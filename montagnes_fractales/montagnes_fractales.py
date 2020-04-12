#!/usr/bin/env python3
#
# -*- coding: utf-8 -*-
# --------------------------------------------------------------------------------------------------------------------------
# Ce programme est une version Python d'un programme de Montagnes Fractales initialement écrit en Turbo Pascal
# en 1993 pendant mes études en école d'ingénieur (ENST - Telecom Paris)
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
#    2020-03-23: version initiale
# --------------------------------------------------------------------------------------------------------------------------


import array
import random
import math
import time
from tkinter import *
import tkinter.filedialog as FD

class mountain:
 
    # size must be a power of 2 (64, 128, 256...)
    def __init__(self,size,drawing_canvas):
        self.numero = 0
        self.size  = size
        self.size2 = size//2
        self.drawing_canvas=drawing_canvas

        # init array of altitudes 
        self.zdata = [[0] * (size + 1) for x in range(size + 1)]        # 2D array of integers 0..size, 0..size

        # compute mountain
        self.compute_rectangle()
        #self.pyramid()

    # ------------ return z value for point (x,y) with x and y in [-size/2,size+2]
    def z(self,x,y):
        return self.zdata[x+self.size2][y+self.size2]

    # ------------ set z value for point (x,y) with x and y in [-size/2,size+2]
    def set_z(self,x,y,z):
        self.zdata[x+self.size2][y+self.size2] = z

    # ------------ Compute the fractal mountain as pyramid
    def pyramid(self):
        for x in range(self.size2 + 1):
            for y in range(self.size2 + 1):
                z = self.size2 - max(x,y)
                self.set_z( x, y, z)
                self.set_z(-x, y, z)
                self.set_z( x,-y, z)
                self.set_z(-x,-y, z)
        self.zmin  = 0
        self.zmax  = self.size2

    # ------------ Compute the fractal mountain with rectangles method
    def compute_rectangle(self):

        # initialize with 0 everywhere and 1 on the border
        for x in range(self.size + 1):
            for y in range(self.size + 1):
              self.zdata[x][y] = 0
        for n in range(self.size + 1):
            self.zdata[n][0] = self.zdata[n][self.size] = self.zdata[0][n] = self.zdata[self.size][n] = 1
        self.zmin  = 0
        self.zmax  = 1
        self.set_z(0,0,1) 

        p1x = p1y = p2y = p4x = -self.size2
        p2x = p3x = p3y = p4y =  self.size2
        self.recursive_computing(p1x,p1y, p2x,p2y, p3x,p3y, p4x,p4y)

    # p1 = botton left corner
    # p2 = bottom right corner
    # p3 = top right corner
    # p4 = top left corner
    def recursive_computing(self ,p1x,p1y, p2x,p2y, p3x,p3y, p4x,p4y):
        def random_height(d):
            return random.randint(0,d) - d // random.randint(2,6)

        distance = p2x - p1x

        # end of recursivity
        if distance <= 1: 
            return

        p5x, p5y = (p1x + p2x) // 2, (p1y + p2y) // 2      # p5 = middle of [p1,p2]
        p6x, p6y = (p2x + p3x) // 2, (p2y + p3y) // 2      # p6 = middle of [p2,p3]
        p7x, p7y = (p3x + p4x) // 2, (p3y + p4y) // 2      # p7 = middle of [p3,p4]
        p8x, p8y = (p4x + p1x) // 2, (p4y + p1y) // 2      # p8 = middle of [p4,p1]
        p9x, p9y = p5x, p6y                                # p9 = middle of [p5,p7] or [p6,p8]

        # only changed altitude of points not yet changed
        if  self.z(p5x, p5y) == 0: self.set_z(p5x, p5y, (self.z(p1x,p1y) + self.z(p2x,p2y)) // 2 + random_height(distance))
        if  self.z(p6x, p6y) == 0: self.set_z(p6x, p6y, (self.z(p2x,p2y) + self.z(p3x,p3y)) // 2 + random_height(distance))
        if  self.z(p7x, p7y) == 0: self.set_z(p7x, p7y, (self.z(p3x,p3y) + self.z(p4x,p4y)) // 2 + random_height(distance))
        if  self.z(p8x, p8y) == 0: self.set_z(p8x, p8y, (self.z(p4x,p4y) + self.z(p1x,p1y)) // 2 + random_height(distance))
        if  self.z(p9x, p9y) == 0: self.set_z(p9x, p9y, (self.z(p5x,p5y) + self.z(p6x,p6y) + self.z(p7x,p7y) + self.z(p8x,p8y)) // 4 + random_height(distance))

        # update zmin and zmax
        self.zmax = max (self.zmax, self.z(p5x, p5y), self.z(p6x, p6y), self.z(p7x, p7y), self.z(p8x, p8y), self.z(p9x, p9y))
        self.zmin = min (self.zmin, self.z(p5x, p5y), self.z(p6x, p6y), self.z(p7x, p7y), self.z(p8x, p8y), self.z(p9x, p9y))

        # now compute altitutes in the 4 sub-squares
        self.recursive_computing (p1x,p1y, p5x,p5y, p9x,p9y, p8x,p8y)       # square p1,p5,p9,p8
        self.recursive_computing (p5x,p5y, p2x,p2y, p6x,p6y, p9x,p9y)       # square p5,p2,p6,p9
        self.recursive_computing (p9x,p9y, p6x,p6y, p3x,p3y, p7x,p7y)       # square p9,p6,p3,p7
        self.recursive_computing (p8x,p8y, p9x,p9y, p7x,p7y, p4x,p4y)       # square p8,p9,p7,p4 

    # ------------ Print array of altitudes
    def print(self):
        print ("zmin={:d} zmax={:d}".format(self.zmin,self.zmax))
        for y in range(-self.size2, self.size2 + 1):
            for x in range(-self.size2, self.size2 + 1):
                print("{:2d} ".format(self.z(x,y)), end='')
            print ("")

    # ------------ Return a RGB color depending on altitude z 
    def z_color(self, z, zmax_water, zmin_forest, zmin_snow):

        if z < zmax_water:
            # blue colors for water
            #pct = (z - self.zmin) / (zmax_water - self.zmin)
            #col = "#{:02x}{:02x}{:02x}".format(0, 0, int(80+ 140 * pct))
            col = "#0000D0"
        elif z < zmin_forest:
            # brown colors for ground
            pct = (z - zmax_water) / (zmin_forest - zmax_water)
            col = "#{:02x}{:02x}{:02x}".format(int(0.5 * 1.25 * (50+80*pct)), int(0.5 * (50+80*pct)), 0)
        elif z < zmin_snow:
            # green colors for forest
            pct = (z - zmin_forest) / (zmin_snow - zmin_forest)
            col = "#{:02x}{:02x}{:02x}".format(0, int(0.5 * (50+80*pct)), 0)
        else:
            # grey/white colors for snow
            if self.zmax != zmin_snow: 
                pct = (z - zmin_snow) / (self.zmax - zmin_snow)
            else:
                pct = 0
            col = "#{:02x}{:02x}{:02x}".format(int(170+80*pct), int(170+80*pct), int(170+80*pct))
        return col

    # ------------ Draw the fractal mountain in 3D 
    # phi   = view angle vs x0z plan (0..350 degrees)
    # theta = view angle (elevation) vs x0y plan (0..90 degrees)
    # xmax, ymax   = size of canvas for drawing
    def draw_3d_view_mode(self, phi, theta, xmax, ymax):

        # -- Coordinates
        # in the mountain : x,y,z     (integer)
        # on the view plan: vpx, vpy  (float)
        # on the screen   : xe, ye    (integer)

        # calculate the vpx and vpy coordinates on the view plan of a point from its x,y,z coordinates
        def convert(x,y,z):
            vpx = -x * sin_phi             + y * cos_phi
            vpy = -x * sin_theta * cos_phi - y * sin_theta * sin_phi + (z-self.zmin) * cos_theta
            # print ("DEBUG: convert(): x={:3d} y={:3d} ----> vpx={:4f} vpy={:4f}".format(x,y,vpx,vpy))
            return vpx, vpy

        # calculate min and max for the vpx and vpy coordinates on the view plan 
        def view_plan_min_max():

            # compute x and y coordinates on the view plan for the 8 summits of parallelogram containing mountain
            vpxa, vpya = convert (-self.size2, -self.size2, self.zmax)  
            vpxb, vpyb = convert (-self.size2, -self.size2, self.zmin)
            vpxc, vpyc = convert ( self.size2, -self.size2, self.zmax)
            vpxd, vpyd = convert ( self.size2, -self.size2, self.zmin)
            vpxe, vpye = convert (-self.size2,  self.size2, self.zmax)
            vpxf, vpyf = convert (-self.size2,  self.size2, self.zmin)
            vpxg, vpyg = convert ( self.size2,  self.size2, self.zmax)
            vpxh, vpyh = convert ( self.size2,  self.size2, self.zmin)

            # then calculate min and max
            l_vpx_min = min (vpxa, vpxb, vpxc, vpxd, vpxe, vpxf, vpxg, vpxh)
            l_vpx_max = max (vpxa, vpxb, vpxc, vpxd, vpxe, vpxf, vpxg, vpxh)
            l_vpy_min = min (vpya, vpyb, vpyc, vpyd, vpye, vpyf, vpyg, vpyh)
            l_vpy_max = max (vpya, vpyb, vpyc, vpyd, vpye, vpyf, vpyg, vpyh)

            #print ("DEBUG: view_plan_min_max(): l_vpx_min={:f}, l_vpx_max={:f}, l_vpy_min={:f}, l_vpy_max={:f}".format(l_vpx_min, l_vpx_max, l_vpy_min, l_vpy_max))
            return l_vpx_min, l_vpx_max, l_vpy_min, l_vpy_max

        # calculate x and y coordinates on screen from x,y coordinates in the view plan
        def coord_ecran(vpx,vpy):
            xe = int(xmax * (vpx - vpx_min) / (vpx_max - vpx_min))
            ye = int(ymax * (vpy - vpy_max) / (vpy_min - vpx_max))
            return xe,ye

        # draw the polygon using 4 points starting with x,y
        def trace_A(x,y):
            # sous_trace1a: calculate the vpx and vpy coordinates in the view plan
            # of the 4 points:   P1(x,y)   P2(x,y+1)   P3(x+1,y+1)   P4(x+1,y)
            vpx_p1, vpy_p1 = convert(x  , y  , max (zmax_water, self.z(x  , y  )))
            vpx_p2, vpy_p2 = convert(x  , y+1, max (zmax_water, self.z(x  , y+1)))
            vpx_p3, vpy_p3 = convert(x+1, y+1, max (zmax_water, self.z(x+1, y+1)))
            vpx_p4, vpy_p4 = convert(x+1, y  , max (zmax_water, self.z(x+1, y  )))

            # sous_trace2: calculate the xe, ye screen coordinates for the 4 points of the rectangle
            xe_p1, ye_p1 = coord_ecran (vpx_p1, vpy_p1)
            xe_p2, ye_p2 = coord_ecran (vpx_p2, vpy_p2)
            xe_p3, ye_p3 = coord_ecran (vpx_p3, vpy_p3)
            xe_p4, ye_p4 = coord_ecran (vpx_p4, vpy_p4)

            # sous_trace3: draw the polygone between the 4 points
            # print ("DEBUG: trace_A()   P1={:d},{:d} P2={:d},{:d} P3={:d},{:d} P4={:d},{:d}".format(xe_p1,ye_p1, xe_p2,ye_p2, xe_p3,ye_p3, xe_p4,ye_p4))
            rgb_color = self.z_color(self.z(x,y), zmax_water, zmin_forest, zmin_snow)
            self.drawing_canvas.create_polygon(xe_p1,ye_p1, xe_p2,ye_p2, xe_p3,ye_p3, xe_p4,ye_p4, fill=rgb_color, outline=rgb_color)

        # calculate altitute of limits between terrains
        zmax_water  = self.zmin + ((self.zmax-self.zmin) * level_water)  // 100
        zmin_forest = self.zmin + ((self.zmax-self.zmin) * level_forest) // 100
        zmin_snow   = self.zmin + ((self.zmax-self.zmin) * level_snow)   // 100

        # use variables for sinus and cosinus to avoid computing it each time
        sin_theta = math.sin (theta / 180 * math.pi)
        cos_theta = math.cos (theta / 180 * math.pi)
        sin_phi   = math.sin (phi   / 180 * math.pi)
        cos_phi   = math.cos (phi   / 180 * math.pi)

        #print ("DEBUG: sin_theta={:f} cos_theta={:f} sin_phi={:f} cos_phi={:f}".format(sin_theta, cos_theta, sin_phi, cos_phi))

        # calculate min and max for the vpx and vpy coordinates on the view plan 
        vpx_min, vpx_max, vpy_min, vpy_max = view_plan_min_max()

        # First, clear canvas
        self.drawing_canvas.delete("all")

        # Then draw in 
        if phi < 90:
            for x in range(-self.size2, self.size2):
                for y in range(-self.size2, self.size2):
                    trace_A(x,y)

        elif phi < 180:
            for x in range(self.size2 - 1, -self.size2 - 1, -1):
                for y in range(-self.size2, self.size2):
                    trace_A(x,y)

        elif phi < 270:
            for x in range(self.size2 - 1, -self.size2 - 1, -1):
                for y in range(self.size2 - 1, -self.size2 - 1, -1):
                    trace_A(x,y)

        else:
            for x in range(-self.size2, self.size2):
                for y in range(self.size2 - 1, -self.size2 - 1, -1):
                    trace_A(x,y)

        return

    # ------------ Draw the fractal mountain in 2D (aerial_view)
    # level_water  = relative level of water/ground limit  (between 1 and 99)
    # level_forest = relative level of ground/forest limit (between 1 and 99, greater than level_water)
    # level_snow   = relative level of forest/snow limit   (between 1 and 99, greater than level_forest)
    def draw_2d_view_mode(self):
        zmax_water  = self.zmin + ((self.zmax - self.zmin) * level_water)  // 100
        zmin_forest = self.zmin + ((self.zmax - self.zmin) * level_forest) // 100
        zmin_snow   = self.zmin + ((self.zmax - self.zmin) * level_snow)   // 100

        # First, clear canvas
        self.drawing_canvas.delete("all")

        # then display 2D view
        for y in range(-self.size2, self.size2):
            for x in range(-self.size2, self.size2):
                n = canvas_size / self.size
                rgb_color = self.z_color(self.z(x,y), zmax_water, zmin_forest, zmin_snow)
                self.drawing_canvas.create_rectangle( (x+self.size2)*n, (y+self.size2)*n, (x+self.size2)*n + n, (y+self.size2)*n + n, width=0, fill=rgb_color) 

# ------------ view modes
def switch_view_mode():
    global view_mode
    global view_mode_sv1
    global angle_phi_label 
    global angle_phi_value_label
    global angle_phi_plus_button
    global angle_phi_minus_button
    global angle_theta_label
    global angle_theta_value_label
    global angle_theta_plus_button
    global angle_theta_minus_button

    if view_mode == "2D":
        # switch to 3D
        view_mode = "3D"
        view_mode_sv1.set("3 dimensions view mode")
        view_mode_sv2.set("Switch to 2D view mode")

        angle_phi_label.config(state=NORMAL)
        angle_phi_value_label.config(state=NORMAL)
        angle_phi_plus_button.config(state=NORMAL)
        angle_phi_minus_button.config(state=NORMAL)

        angle_theta_label.config(state=NORMAL)
        angle_theta_value_label.config(state=NORMAL)
        angle_theta_plus_button.config(state=NORMAL)
        angle_theta_minus_button.config(state=NORMAL)
        
        my_mountain.draw_3d_view_mode(phi, theta, canvas_size, canvas_size)    

    else:
        # switch to 2D
        view_mode = "2D"
        view_mode_sv1.set("2 dimensions view mode")
        view_mode_sv2.set("Switch to 3D view mode")

        angle_phi_label.config(state=DISABLED)
        angle_phi_value_label.config(state=DISABLED)
        angle_phi_plus_button.config(state=DISABLED)
        angle_phi_minus_button.config(state=DISABLED)

        angle_theta_label.config(state=DISABLED)
        angle_theta_value_label.config(state=DISABLED)
        angle_theta_plus_button.config(state=DISABLED)
        angle_theta_minus_button.config(state=DISABLED)

        my_mountain.draw_2d_view_mode()    
    return

# ------------ Actions triggered by buttons
def snow_minus():
    global level_snow
    global snow_value_sv
    global auto_redisplay
    if level_snow >= level_forest + 2:
        level_snow -= 2
        snow_value_sv.set(": "+str(level_snow))
        if auto_redisplay.get() == 1:     # auto-redisplay checkbutton checked
            redisplay()
    
def snow_plus():
    global level_snow
    global snow_value_sv
    global auto_redisplay
    if level_snow <= 98:
        level_snow += 2
        snow_value_sv.set(": "+str(level_snow))
        if auto_redisplay.get() == 1:     # auto-redisplay checkbutton checked
            redisplay()

def forest_minus():
    global level_forest
    global forest_value_sv
    global auto_redisplay
    if level_forest >= level_water + 2:
        level_forest -= 2
        forest_value_sv.set(": "+str(level_forest))
        if auto_redisplay.get() == 1:     # auto-redisplay checkbutton checked
            redisplay()
    
def forest_plus():
    global level_forest
    global forest_value_sv
    global auto_redisplay
    if level_forest <= level_snow - 2:
        level_forest += 2
        forest_value_sv.set(": "+str(level_forest))
        if auto_redisplay.get() == 1:     # auto-redisplay checkbutton checked
            redisplay()

def water_minus():
    global level_water
    global water_value_sv
    global auto_redisplay
    if level_water >= 2:
        level_water -= 2
        water_value_sv.set(": "+str(level_water))
        if auto_redisplay.get() == 1:     # auto-redisplay checkbutton checked
            redisplay()
    
def water_plus():
    global level_water
    global water_value_sv
    global auto_redisplay
    if level_water <= level_forest - 2:
        level_water += 2
        water_value_sv.set(": "+str(level_water))
        if auto_redisplay.get() == 1:     # auto-redisplay checkbutton checked
            redisplay()

def angle_phi_minus():
    global phi
    global angle_phi_value_sv
    global auto_redisplay
    phi -= 10
    if phi < 0: phi = 350
    angle_phi_value_sv.set(": "+str(phi)+"°")
    if auto_redisplay.get() == 1:     # auto-redisplay checkbutton checked
        redisplay()

def angle_phi_plus():
    global phi
    global angle_phi_value_sv
    global auto_redisplay
    phi += 10
    if phi > 350: phi = 0
    angle_phi_value_sv.set(": "+str(phi)+"°")
    if auto_redisplay.get() == 1:     # auto-redisplay checkbutton checked
        redisplay()

def angle_theta_minus():
    global theta
    global angle_theta_value_sv
    global auto_redisplay
    if theta >= 10: 
        theta -= 10
        angle_theta_value_sv.set(": "+str(theta)+"°")
        if auto_redisplay.get() == 1:     # auto-redisplay checkbutton checked
            redisplay()

def angle_theta_plus():
    global theta
    global angle_theta_value_sv
    global auto_redisplay
    if theta <= 80:
        theta += 10
        angle_theta_value_sv.set(": "+str(theta)+"°")
        if auto_redisplay.get() == 1:     # auto-redisplay checkbutton checked
            redisplay()

def zoom_minus():
    global zoom
    global zoom_value_sv
    if zoom > 25: 
        zoom = zoom // 2
        zoom_value_sv.set(": "+str(zoom)+"%")

def zoom_plus():
    global zoom
    global zoom_value_sv
    if zoom < 400: 
        zoom = zoom * 2
        zoom_value_sv.set(": "+str(zoom)+"%")

def redisplay():
    global view_mode
    global phi
    global theta
    global canvas_size
    global my_mountain
    if view_mode == "2D":
        my_mountain.draw_2d_view_mode()
    else:
        my_mountain.draw_3d_view_mode(phi, theta, xmax=canvas_size, ymax=canvas_size)
    return

def recalculate():
    global my_mountain
    my_mountain.compute_rectangle()
    redisplay()
    return

def save():
    global my_mountain
    global level_water
    global level_forest
    global level_snow

    filename = FD.asksaveasfilename(title = "Select file",filetypes = (("mountain files","*.fmnt"),("all files","*.*")))
    filename = filename + ".fmnt"

    try:
        my_file = open (filename,'w')
        my_file.write("BEGIN BACKUP MOUNTAIN\n")
        my_file.write(str(level_water)+'\n')
        my_file.write(str(level_forest)+'\n')
        my_file.write(str(level_snow)+'\n')
        my_file.write(str(my_mountain.zmin)+'\n')
        my_file.write(str(my_mountain.zmax)+'\n')
        for x in range(my_mountain.size + 1):
            for y in range(my_mountain.size + 1):
                my_file.write(str(my_mountain.zdata[x][y])+'\n')
        my_file.write("END BACKUP MOUNTAIN\n")
        my_file.close()
    except:
        print ("ERROR: cannot write to file "+filename+ "!")

    return

def load():
    global my_mountain
    global level_water
    global level_forest
    global level_snow
    global snow_value_sv
    global forest_value_sv
    global water_value_sv
   
    filename = FD.askopenfilename(title = "Select file",filetypes = (("mountain files","*.fmnt"),("all files","*.*")))

    try:
        my_file = open (filename,'r')
        text = my_file.readline()
        if text != "BEGIN BACKUP MOUNTAIN\n":
            print ("ERROR: invalid content !")
        level_water = int(my_file.readline())
        level_forest = int(my_file.readline())
        level_snow = int(my_file.readline())
        my_mountain.zmin = int(my_file.readline())
        my_mountain.zmax = int(my_file.readline())
        for x in range(my_mountain.size + 1):
            for y in range(my_mountain.size + 1):
                my_mountain.zdata[x][y] = int(my_file.readline())
        text = my_file.readline()
        if text != "END BACKUP MOUNTAIN\n":
            print ("ERROR: invalid content !")
        my_file.close()
    except:
        print ("ERROR: cannot read mountain from file "+filename+ ": permissions errors or invalid content !")

    # update levels
    snow_value_sv.set(": "+str(level_snow))
    forest_value_sv.set(": "+str(level_forest))
    water_value_sv.set(": "+str(level_water))

    # Redisplay mountain once loaded
    redisplay()

    return

# ------------ Level 2 Frames design  
def view_mode_frame_design(l_frame):
    global view_mode_sv1
    global view_mode_sv2

    view_mode_sv1 = StringVar()
    view_mode_sv1.set("3 dimensions view mode")
    view_mode_label = Label(l_frame, textvariable=view_mode_sv1, font=("Helvetica", 28), bg="grey", fg="black")
    view_mode_label.pack(side=TOP, fill=X, padx=5, pady=5)

    view_mode_sv2 = StringVar()
    view_mode_sv2.set("Switch to 2D view mode")
    view_mode_button = Button(l_frame, textvariable=view_mode_sv2, highlightbackground='#3E4149', command=switch_view_mode)
    view_mode_button.pack(side=TOP, fill=X, padx=5, pady=5)

    return

def parameters_frame_design(l_frame):
    global snow_value_sv
    global forest_value_sv
    global water_value_sv
    global angle_phi_value_sv
    global angle_theta_value_sv
    global zoom_value_sv
    global angle_phi_label 
    global angle_phi_value_label
    global angle_phi_plus_button
    global angle_phi_minus_button
    global angle_theta_label
    global angle_theta_value_label
    global angle_theta_plus_button
    global angle_theta_minus_button
    global auto_redisplay

    #https://stackoverflow.com/questions/1529847/how-to-change-the-foreground-or-background-colour-of-a-tkinter-button-on-mac-os

    # -- snow level
    snow_label = Label(l_frame, text="Snow start level (0-100)", anchor='nw', bg="grey", fg="black")
    snow_label.grid(row=0, column=0, padx=5, pady=5, sticky='we')

    snow_value_sv = StringVar()
    snow_value_sv.set(": "+str(level_snow))
    snow_value_label = Label(l_frame, textvariable=snow_value_sv, anchor='nw', bg="grey", fg="black")
    snow_value_label.grid(row=0, column=1, padx=5, pady=5, sticky='we')

    snow_minus_button = Button(l_frame, text="-", highlightbackground='#3E4149', command=snow_minus)
    snow_minus_button.grid(row=0, column=2, padx=5, pady=5)

    snow_plus_button = Button(l_frame, text="+", highlightbackground='#3E4149', command=snow_plus)
    snow_plus_button.grid(row=0, column=3, padx=5, pady=5)

    # -- forest level
    forest_label = Label(l_frame, text="Forest start level (0-100)", anchor='nw', bg="grey", fg="black")
    forest_label.grid(row=1, column=0, padx=5, pady=5, sticky='we')

    forest_value_sv = StringVar()
    forest_value_sv.set(": "+str(level_forest))
    forest_value_label = Label(l_frame, textvariable=forest_value_sv, anchor='nw', bg="grey", fg="black")
    forest_value_label.grid(row=1, column=1, padx=5, pady=5, sticky='we')

    forest_minus_button = Button(l_frame, text="-", highlightbackground='#3E4149', command=forest_minus)
    forest_minus_button.grid(row=1, column=2, padx=5, pady=5)

    forest_plus_button = Button(l_frame, text="+", highlightbackground='#3E4149', command=forest_plus)
    forest_plus_button.grid(row=1, column=3, padx=5, pady=5)

    # -- water level
    water_label = Label(l_frame, text="Water stop level (0-100)", anchor='nw', bg="grey", fg="black")
    water_label.grid(row=2, column=0, padx=5, pady=5, sticky='we')

    water_value_sv = StringVar()
    water_value_sv.set(": "+str(level_water))
    water_value_label = Label(l_frame, textvariable=water_value_sv, anchor='nw', bg="grey", fg="black")
    water_value_label.grid(row=2, column=1, padx=5, pady=5, sticky='we')

    water_minus_button = Button(l_frame, text="-", highlightbackground='#3E4149', command=water_minus)
    water_minus_button.grid(row=2, column=2, padx=5, pady=5)

    water_plus_button = Button(l_frame, text="+", highlightbackground='#3E4149', command=water_plus)
    water_plus_button.grid(row=2, column=3, padx=5, pady=5)

    # -- angle phi
    angle_phi_label = Label(l_frame, text="Angle PHI (0°-350°)", anchor='nw', bg="grey", fg="black")
    angle_phi_label.grid(row=3, column=0, padx=5, pady=5, sticky='we')

    angle_phi_value_sv = StringVar()
    angle_phi_value_sv.set(": "+str(phi)+"°")
    angle_phi_value_label = Label(l_frame, textvariable=angle_phi_value_sv, anchor='nw', bg="grey", fg="black")
    angle_phi_value_label.grid(row=3, column=1, padx=5, pady=5, sticky='we')

    angle_phi_minus_button = Button(l_frame, text="-", highlightbackground='#3E4149', command=angle_phi_minus)
    angle_phi_minus_button.grid(row=3, column=2, padx=5, pady=5)

    angle_phi_plus_button = Button(l_frame, text="+", highlightbackground='#3E4149', command=angle_phi_plus)
    angle_phi_plus_button.grid(row=3, column=3, padx=5, pady=5)

    # -- angle theta
    angle_theta_label = Label(l_frame, text="Angle THETA (0°-90°) ", anchor='nw', bg="grey", fg="black")
    angle_theta_label.grid(row=4, column=0, padx=5, pady=5, sticky='we')

    angle_theta_value_sv = StringVar()
    angle_theta_value_sv.set(": "+str(theta)+"°")
    angle_theta_value_label = Label(l_frame, textvariable=angle_theta_value_sv, anchor='nw', bg="grey", fg="black")
    angle_theta_value_label.grid(row=4, column=1, padx=5, pady=5, sticky='we')

    angle_theta_minus_button = Button(l_frame, text="-", highlightbackground='#3E4149', command=angle_theta_minus)
    angle_theta_minus_button.grid(row=4, column=2, padx=5, pady=5)

    angle_theta_plus_button = Button(l_frame, text="+", highlightbackground='#3E4149', command=angle_theta_plus)
    angle_theta_plus_button.grid(row=4, column=3, padx=5, pady=5)

    # -- zoom
    zoom_label = Label(l_frame, text="Zoom", anchor='nw', bg="grey", fg="black")
    zoom_label.grid(row=5, column=0, padx=5, pady=5, sticky='we')

    zoom_value_sv = StringVar()
    zoom_value_sv.set(": "+str(zoom)+"%")
    zoom_value_label = Label(l_frame, textvariable=zoom_value_sv, anchor='nw', justify='left', bg="grey", fg="black")
    zoom_value_label.grid(row=5, column=1, padx=5, pady=5, sticky='we')

    zoom_minus_button = Button(l_frame, text="-", highlightbackground='#3E4149', command=zoom_minus)
    zoom_minus_button.grid(row=5, column=2, padx=5, pady=5)

    zoom_plus_button = Button(l_frame, text="+", highlightbackground='#3E4149', command=zoom_plus)
    zoom_plus_button.grid(row=5, column=3, padx=5, pady=5)

    # -- auto redisplay
    auto_redisplay = IntVar()
    auto_redisplay_chkbox = Checkbutton(l_frame, text="Automatic redisplay when updating a parameter", var=auto_redisplay, anchor='nw', bg="grey", fg="black")
    auto_redisplay_chkbox.grid(row=6, column=0, columnspan=4, padx=5, pady=5, sticky='we')
    auto_redisplay_chkbox.select()

    return

def actions_frame_design(l_frame):
    redisplay_button = Button(l_frame, text="Redisplay", highlightbackground='#3E4149', command=redisplay)
    redisplay_button.pack(side=TOP, fill=X, padx=5, pady=5)

    recalculate_button = Button(l_frame, text="Recalculate", highlightbackground='#3E4149', command=recalculate)
    recalculate_button.pack(side=TOP, fill=X, padx=5, pady=5)

    save_button = Button(l_frame, text="Save", fg="black", highlightbackground='#3E4149', command=save)
    save_button.pack(side=TOP, fill=X, padx=5, pady=5)

    load_button = Button(l_frame, text="Load", fg="black", highlightbackground='#3E4149', command=load)
    load_button.pack(side=TOP, fill=X, padx=5, pady=5)

    quit_button = Button(l_frame, text="Quit", fg="black", highlightbackground='#3E4149', command=main_window.quit)
    quit_button.pack(side=TOP, fill=X, padx=5, pady=5)
    return

# ============================== Main, using class mountain

global canvas_size 
global view_mode_sv1
global view_mode
global level_water
global level_forest
global level_snow

if __name__ == '__main__':

    # -------- Initialize variables
    view_mode = "3D"
    phi = 30            # between 0 and 350 degrees (step is 10°)
    theta = 30          # between 0 and 90 degrees (step is 10°)
    canvas_size = 800   # size of drawing canvas (square)
    resolution = 128    # power of 2: 8, 16, 32, 64, 128, 256...
    zoom = 100          # percentage. can be 25, 50, 100, 200, 400     
    level_water = 50    # max level of water (0-100, even)
    level_forest = 76   # min level of forest (0-100, even), >= level_water
    level_snow = 90     # min level of snow (0-100, even), >= level_forest

    # -------- GUI design
    # 2 Level 1 frames from left to right: control_frame, drawing_frame
    # inside control_frame (level 2 widgets): 3 frames from top to bottom: view_mode_frame, parameters_frame, actions_frame
    # inside zoom_frame (level 3 widgets): from top to bottom: zoom_label, zoom_in_button, zoom_out_button 
    # inside drawing_frame: 1 Level 2 canvas
    
    # ---- Main Window
    main_window = Tk()
    main_window.title('Fractal Mountain')
    #main_window.geometry('1100x1100+0+0')

    # ---- Control frame and sub-widgets
    # Control frame on the left
    control_frame=Frame(main_window, bg="grey")
    control_frame.pack(side=LEFT, fill=Y, padx=0, pady=0)

    # View mode frame inside control frame to display label and button related to vie mode
    view_mode_frame = Frame(control_frame, bg="grey")
    view_mode_frame.pack(side=TOP, fill=X, padx=10, pady=20)
    view_mode_frame_design(view_mode_frame)

    # Parameters frame inside control frame to display labels and button related to parameters (levels, zoom, angles)
    parameters_frame = Frame(control_frame, bg="grey")
    parameters_frame.pack(side=TOP, fill=X, padx=10, pady=20)
    parameters_frame_design(parameters_frame)

    # Actions frame inside control frame to display labels and buttons for redisplay, recalculate, save, load, quit
    actions_frame = Frame(control_frame, bg="grey")
    actions_frame.pack(side=TOP, fill=X, padx=10, pady=20)
    actions_frame_design(actions_frame)

    # ---- Drawing frame and sub-widgets
    # Drawing frame on the right
    drawing_frame = Frame(main_window)
    drawing_frame.pack(side=LEFT, fill=Y, padx=0, pady=0)

    # Canvas inside drawing frame
    drawing_canvas = Canvas(drawing_frame, height=canvas_size, width=canvas_size, bg="grey")        
    drawing_canvas.pack(side=LEFT)
      
    # bouton Quitter
    #bt_quit=Button(frame_bt_quit, text="Quitter", bg="red", command=main_window.quit)
    #bt_quit.pack(side=LEFT, fill=X, padx=5, pady=5)
    
    # bouton Sauvegarder
    #bt_save=Button(frame_bt_quit, text="Sauvegarder", bg="grey", command=sauve)
    #bt_save.pack(side=LEFT, fill=X, padx=5, pady=5)
    
    # bouton Charger
    #bt_load=Button(frame_bt_quit, text="Charger", bg="grey", command=charge)
    #bt_load.pack(side=LEFT, fill=X, padx=5, pady=5)

    # -------- Creation of fractal mountain
    my_mountain = mountain(resolution, drawing_canvas)
    #my_mountain.print()
        
    # Draw the mountain in 3D
    my_mountain.draw_3d_view_mode(phi, theta, xmax=canvas_size, ymax=canvas_size)

    main_window.mainloop()

