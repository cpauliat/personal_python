
# -*- coding: utf-8 -*-
# --------------------------------------------------------------------------------------------------------------------------
# Ce programme permet d'entrer du vocabulaire etranger et sa traduction en francais
# puis ensuite de tester les connaissances de l'utilisateur
# Ce programme utilise l'interface graphique Tkinter
#
# Auteur        : Christophe Pauliat
# Platformes    : Linux / Windows
#
# Versions
#    2017-01-18: Version initiale developpe avec Python 2 et testee sur Linux et Windows
#    2020-04-04: Conversion en Python 3
# --------------------------------------------------------------------------------------------------------------------------

__author__ = "cpauliat"
__date__ = "$Jan 18, 2017 10:27:45 AM$"

# -------- Modules
from tkinter import * 
from tkinter.font import *
from math import *
import tkinter.filedialog
import fileinput
import tkinter.messagebox
import time
import platform
import codecs

# -------- Constantes
LONGUEUR_MAX=40             # longueur maximale d'un mot ou groupe de mots

# -------- Emplacement des fichiers suivant l'operating system
if (platform.system()=="Linux"):
    FOLDER_VOCA="/home/cpauliat/voca"
    FICHIER_STATS="/home/cpauliat/voca/stats.log"
elif (platform.system()=="Windows"):
    FOLDER_VOCA="C:\voca"
    FICHIER_STATS="C:\voca\stats.log"
else:
    print("ERREUR ! OS non supporté ")
    exit (1)
    
# ---------- class liste
class liste_vocabulaire:
    
    def __init__(self):
        self.nb_expressions=0
        self.expr_fr=[]         # liste des expressions francaises
        self.expr_et=[]         # liste des expressions etrangeres
        
    def nb(self):
        return self.nb_expressions
    
    def fr(self,i):
        return self.expr_fr[i]
    
    def et(self,i):
        return self.expr_et[i]
                
    # nettoie une chaine = enlever les " " et les "\n" en fin de chaine et on enleve les " " en debut de chaine
    def chaine_nettoyee(self,chaine):            
        
        if (len(chaine) == 0):
            return chaine
        
        # -- enleve les ' ' et '\n' en fin de chaine
        chaine2 = chaine
        dernier_car=chaine2[len(chaine2)-1]
        #print "AU DEBUT: chaine2= |"+chaine2+"|"
        
        while ( dernier_car == " " or dernier_car == "\n"):
            # on enleve le dernier caractere            
            chaine2=chaine2[:-1]
            #print "ensuite: chaine2= |"+chaine2+"|"
            if (len(chaine2)==0):
                return chaine2
            dernier_car=chaine2[len(chaine2)-1]               
                    
        # -- enleve les ' ' en debut de chaine
        premier_car=chaine2[0]
        
        #print "AU DEBUT: chaine2= |"+chaine2+"|"
        
        while ( premier_car == " "):
            # on enleve le premier caractere            
            chaine2=chaine2[1:]
            #print "ensuite: chaine2= |"+chaine2+"|"
            if (len(chaine2)==0):
                return chaine2
            premier_car=chaine2[0]
        
        return chaine2
    
    def charge (self,nom_fichier):
        # renvoie False si problem dans le fichier
        # renvoie True si fichier OK
        self.nb_expressions=0
        self.expr_fr=[]
        self.expr_et=[]
                  
        fichier=codecs.open(nom_fichier,'r',encoding='utf-8')        
        
        for ligne in fichier.read().split('\n'):
            # si 0 ou +de 2 carac ; dans la ligne, on sort (fichier corrompu)
            if (ligne.count(";") != 1):
                break
            
            # fr = from ligne, 1er champ avant ;
            fr=ligne.split(";")[0]
            # et = from ligne, 2nd champ apres ; 
            et=ligne.split(";")[1]
            
            #print "LIGNE=|"+ligne+"| fr=|"+fr+"| fr_nettoyee=|"+self.chaine_nettoyee(fr)+"| et=|"+et+"| et_nettoyee=|"+self.chaine_nettoyee(et)+"|"
            
            # nettoyage des chaines
            fr=self.chaine_nettoyee(fr)
            et=self.chaine_nettoyee(et)
            
            # si fr ou et est vide, on ignore cette ligne
            if (len(fr)==0 or len(et)==0):
                continue
                
            # 
            self.nb_expressions += 1
            self.expr_fr.append(fr)
            self.expr_et.append(et)
            #print "|" + fr + "|" + et + "|"                       
         
        fichier.close()
        
        # Si aucun expression OK, on return False
        if (self.nb_expressions == 0):
            return False
        else:
            return True          
        

# ---------- tester liste       
class tester_voca():
    
    def __init__(self,sens):
        # sens = fr2et pour tester traduction FRANCAIS vers ETRANGER
        #     ou et2fr pour tester traduction ETRANGER vers FRANCAIS
        self.liste=liste_vocabulaire()
        self.label_haut=None
        self.label=[]       # tableau des Widgets Label contenant les expressions a traduire
        self.entry=[]       # tableau des Widgets Entry qui contiendront les expressions traduites par l'utilisateur
        self.label_result=[]                               
        self.rep_ok=[]
        self.num_test=1       
        self.nb_questions=0
        self.fichier=None
        self.sens=sens
                
    def afficher_rep(self):
                
        # on renomme le button Annuler en Sortir
        self.button3.config(text="Sortir")
        
        # on rend invisible le bouton "Afficher les reponses"
        self.button2.grid_remove()
        
        # on modifie le texte en haut de la fenetre
        self.label_haut.config(text="Les bonnes réponses sont affichées. Prends le temps de les retenir\n\nApres, tu peux:\n    - soit cliquer sur Re-tester pour refaire le test uniquement sur ces expressions\n    - soit cliquer sur Sortir pour revenir à la fenêtre principale")
                
        for i in range(self.liste.nb()):
            if (self.rep_ok[i] == True):
                # bonne reponse --> on supprime la ligne
                self.label[i].grid_remove()
                self.entry[i].grid_remove()                
                self.label_result[i].grid_remove()                                
            else:
                # mauvaise reponse, on efface resultat et on affiche la bonne reponse en vert
                self.label_result[i].config(text="")
                self.entry[i].config(fg="green",state='normal')
                self.entry[i].delete(0,END)
                if (self.sens=="fr2et"):
                    self.entry[i].insert(0,self.liste.et(i))
                else:
                    self.entry[i].insert(0,self.liste.fr(i))
                self.entry[i].config(fg="green",state='readonly')                        
        
    def retester(self): 
        
        # on renomme le button Re-tester en Verifier
        self.button1.config(text="Vérifier", command=self.verifier)       
        
        # on rend invisible le bouton "Afficher les reponses"
        self.button2.grid_remove()
        
        # on renomme le button Annuler/Sortir en Sortir
        self.button3.config(text="Annuler")
        
        # on incremente le numero du test
        self.num_test += 1
        
        # on affiche le numero du test
        self.label_numtest.config(text="Liste "+self.fichier.name+" "*20+"Test numéro "+str(self.num_test))
        
        # on modifie le texte en haut de la fenetre
        if (self.sens=="fr2et"):
            self.label_haut.config(text="Pour chaque expression française, entre l'expression étrangère correspondante\npuis presse Vérifier quand tu as terminé")
        else:
            self.label_haut.config(text="Pour chaque expression étrangère, entre l'expression française correspondante\npuis presse Vérifier quand tu as terminé")

        # on efface les widgets des lignes OK (peut etre deja fait dans afficher_rep)        
        # on calcule le nombre de questions dans le nouveau test.
        self.nb_questions=0
        for i in range(self.liste.nb()):
            if (self.rep_ok[i] == True):
                # bonne reponse --> on supprime la ligne
                self.label[i].grid_remove()
                self.entry[i].grid_remove()                
                self.label_result[i].grid_remove()                
            else:
                # mauvaise reponse --> on efface le contenu des labels resultats et des entry
                self.label_result[i].config(text="")                          
                self.entry[i].config(fg=self.default_fg,state='normal')                
                self.entry[i].delete(0,END)                  
                self.nb_questions+=1
        return
    
    def verifier(self): 
        nb_err=0        
        
        for i in range(self.liste.nb()):
                                    
            if (self.sens=="fr2et" and self.entry[i].get() == self.liste.et(i)) or (self.sens=="et2fr" and self.entry[i].get() == self.liste.fr(i)):
                # bonne reponse
                self.label_result[i].config(text="OK", fg="green")
                self.entry[i].config(fg="green", state='readonly')
                self.rep_ok[i]=True
                
            else:
                # mauvaise reponse
                self.label_result[i].config(text="ERREUR", fg="red")
                self.entry[i].config(fg="red", state='readonly')
                nb_err += 1
        
        nb_ok=self.nb_questions - nb_err
        #note=round(20.0*float(nb_ok)/float(self.nb_questions),1)     
        note=int(floor(20.0*nb_ok/self.nb_questions))
        
        if (nb_err == 0):
            # si auncune error, on renomme le bouton Annuler en sortir et on efface les 2 autres
            self.label_haut.config(text="BRAVO ! que des bonnes réponses")
            
            self.button1.grid_remove()
            self.button2.grid_remove()
            self.button3.config(text="Sortir")
            
        else:
            # Sinon, on affiche le bouton "Afficher les reponses"
            
            self.label_haut.config(text="NOTE: "+str(note)+"/20"+"\n"+" "*30+"Bonnes réponses: "+str(nb_ok)+" / "+str(self.nb_questions)+"\n"+" "*30+"Mauvaises réponses: "+str(nb_err)+" / "+str(self.nb_questions))
        
            self.button2.grid(sticky=S+N,column=1,row=0,padx=20,pady=10)      
            self.button2.config(command=self.afficher_rep)
        
            # Et on transforme le bouton Verifier en Retester
            self.button1.config(text="Re-tester", command=self.retester)
        
        # stocker les infos (date;nom liste;sens_traduction;note/20;nb_ok/nb_erreurs;nb_questions;expressions fr;et en erreur) dans le fichier statistiques
        ligne_stats=""
        ligne_stats+=time.strftime('%d/%m/%Y %H:%M',time.localtime())+";"+self.fichier.name+";"+self.sens+";"+str(note)+"/20"+";"+str(nb_ok)+"/"+str(self.nb_questions)
        if (nb_ok != self.nb_questions):            
            for i in range(self.liste.nb()):
                if (self.entry[i].get() != self.liste.et(i)):
                    ligne_stats+=";"+self.liste.fr(i)+";"+self.liste.et(i)
        
        #print ligne_stats
        
        fic_stats=codecs.open(FICHIER_STATS,'a',encoding='utf-8')     
        fic_stats.write(ligne_stats+"\n")
        fic_stats.close()
        
        
        
    # renvoie True si chargement de la liste OK
    def charge_liste(self):    
        # on charge une liste depuis un fichier
        myFormats = [ ('Vocabulaire','*.voc') ]
        self.fichier = tkinter.filedialog.askopenfile(parent=fenetre_principale,mode='rb',initialdir=FOLDER_VOCA,filetypes=myFormats,title='Choisis une liste de vocabulaire')        
        if self.fichier == None:
            return False
        
        # si le fichier ne contient aucun expression correcte
        if (self.liste.charge(self.fichier.name) == False):
            # message erreur
            tkinter.messagebox.showerror(title="Erreur !", message="Erreur dans le fichier !\n\nCe fichier est corrompu !")
            return False
        
        # on initialise la liste des reponses OK (aucune reponse OK au debut)
        for i in range(self.liste.nb()):
            self.rep_ok.append(False)
        
        return True        
        
    def affiche_fenetre(self):    
        # on rend la fenetre principale invisible
        fenetre_principale.withdraw()  
        
        # on cree la nouvelle fenetre
        tester_fenetre=Toplevel(fenetre_principale, bg="white")
        
        if (self.sens=="fr2et"):
            tester_fenetre.title("Tester ton vocabulaire (traduction français vers langue étrangère)")
            couleur_label="#FFD0D0"
            couleur_entry="#D0D0FF"
        else:
            tester_fenetre.title("Tester ton vocabulaire (traduction langue étrangère vers français)")
            couleur_label="#D0D0FF"
            couleur_entry="#FFD0D0"
            
        tester_fenetre.resizable(width=False, height=False)    
        tester_fenetre.bind("<Destroy>",fenetre_detruite)
        
        # ------ Arborescence des widgets
        # tester_tester
        #     tester_frame1
        #         label_num_test
        #         label_haut
        #         tester_sbframe
        #             tester_sbcanvas
        #                 tester_framecanvas
        #                     plusieurs lignes de Label + Entry + Label  
        #             tester_sbsb
        #     tester_frame_boutons
        #         button1
        #         button2
        #         button3
        
        # nb_questions
        # pour le premier test, le nombre de questions est egal au nombre d'expressions
        self.nb_questions=self.liste.nb();
        
        # frame contenant 2 labels et 1 frame
        tester_frame1=Frame(tester_fenetre, bg="white")
        tester_frame1.pack(side="top", expand=True, fill="both") #, padx=10, pady=10)

        # label contenant le nom de la liste et le  numero du test        
        self.label_numtest=Label(tester_frame1, justify=LEFT, anchor=W, width=50, bg="white", font=Font(family='Helvetica', size=24), text="Liste "+self.fichier.name+" "*20+"Test numéro "+str(self.num_test))
        self.label_numtest.pack(side="top",fill="x",padx=10,pady=10)
        
        # label du haut (pour les messages)
        self.label_haut=Label(tester_frame1, justify=LEFT, anchor=W, width=50, bg="white", font=Font(family='Helvetica'))
        if (self.sens=="fr2et"):
            self.label_haut.config(text="Pour chaque expression française, entre l'expression étrangère correspondante\npuis presse Vérifier quand tu as terminé")
        else:
            self.label_haut.config(text="Pour chaque expression étrangère, entre l'expression française correspondante\npuis presse Vérifier quand tu as terminé")
        self.label_haut.pack(side="top",fill="x",padx=10,pady=10)
        self.default_fg=self.label_haut.cget("fg")            # on sauve la couleur fg par defaut
        
        # frame pour contenir un canvas + scrollbar
        tester_sbframe=Frame(tester_frame1,bg="white")
        tester_sbframe.pack(side="top",fill="both",expand=True,padx=10,pady=10)
                 
        # dans cette frame, on cree un scrollbar a droite
        tester_sbsb=Scrollbar(tester_sbframe, orient=VERTICAL, bg="white")
        tester_sbsb.pack(side="right",fill="y")
    
        # dans cette frame, on cree un canvas a gauche associé a ce scrollbar
        tester_sbcanvas=Canvas(tester_sbframe,yscrollcommand=tester_sbsb.set, bg="white")
        tester_sbcanvas.pack(side="left",fill="both",expand=True)
    
        # fin configuration du scrollbar
        tester_sbsb.config(command=tester_sbcanvas.yview) 
    
        # dans le canvas, on cree une frame
        tester_framecanvas=Frame(tester_sbcanvas,bg="white")
    
        # enfin dans cette frame, on cree un tableau de label, entry, label
        for nb in range(self.liste.nb()):
            if (self.sens=="fr2et"):
                text1=self.liste.fr(nb)
            else:
                text1=self.liste.et(nb)
            lab=Label(tester_framecanvas, justify=LEFT, bg=couleur_label, width=40, text=text1, font=Font(family='Helvetica'))
            lab.grid(sticky=N+W+E+S, column=0,row=2+nb,padx=10,pady=2)
            self.label.append(lab)
            
            entry=Entry(tester_framecanvas, justify=LEFT, font=Font(family='Helvetica'), bg=couleur_entry, width=40)
            entry.grid(sticky=N+W+E+S, column=1,row=2+nb,padx=0,pady=2)
            self.entry.append(entry)
            
            res=Label(tester_framecanvas, justify=LEFT, bg="white", font=Font(family='Helvetica'), padx=10, width=6)
            res.grid(sticky=N+W+E+S, column=2,row=2+nb,padx=10,pady=2)
            self.label_result.append(res)         
        
        # fin de configuration du canvas et scrollbar
        tester_sbcanvas.create_window(0,0,window=tester_framecanvas)
        tester_framecanvas.update_idletasks()
        tester_sbcanvas.config(scrollregion=tester_sbcanvas.bbox("all"))
        
        # ------- creation frame pour les boutons
        tester_frame_boutons=Frame(tester_fenetre, bg="white",padx=10,pady=10)
        #CPA tester_frame_boutons.grid(sticky=S+E+W,column=0,row=1)
        tester_frame_boutons.pack(side="bottom",fill="x")   #, expand=True)
        tester_frame_boutons.columnconfigure(0, weight=1)
        tester_frame_boutons.columnconfigure(1, weight=1)
        tester_frame_boutons.columnconfigure(2, weight=1)
        
        # remplissage frame boutons 
        self.button1=Button(tester_frame_boutons, width=15, text="Vérifier", font=Font(family='Helvetica'), command=self.verifier)
        self.button1.grid(sticky=S+N,column=0,row=0,padx=20,pady=10)      
        
        self.button2=Button(tester_frame_boutons, text="Afficher les réponses", font=Font(family='Helvetica'))            
        #self.button2.grid(sticky=S+N,column=1,row=0,padx=20,pady=10)      
        
        self.button3=Button(tester_frame_boutons, width=15, text="Annuler", font=Font(family='Helvetica'), command=tester_fenetre.destroy)
        self.button3.grid(sticky=S+N, column=2,row=0,padx=20,pady=10)       
        
        # calcul taille frame boutons sans attendre
        tester_frame_boutons.update_idletasks()

        # ajustement de la taille du canvas        
        hauteur=min(tester_framecanvas.winfo_height(),tester_framecanvas.winfo_screenheight()-tester_frame_boutons.winfo_height()-self.label_numtest.winfo_height()-self.label_haut.winfo_height()-200)
        largeur=tester_framecanvas.winfo_width()
        tester_sbcanvas.config(width=largeur, height=hauteur)       
        
        
            
    
        
# ---------- Tester 
def toplevel_tester(sens):
    # sens = fr2et pour tester traduction FRANCAIS vers ETRANGER
    #     ou et2fr pour tester traduction ETRANGER vers FRANCAIS    
    tester=tester_voca(sens)
    if (tester.charge_liste() == True):
        tester.affiche_fenetre()    
        
# ---------- sauver la liste sous un nouveau nom (commun a editer et creer)
def supprime_espace(chaine):
    # on supprime les espaces en fin de la chaine
    while (len(chaine)>0 and chaine[len(chaine)-1]==" "):
        chaine=chaine[:-1]
        
    # on supprime les espaces en debut de la chaine
    while (len(chaine)>0 and chaine[0]==" "):
        chaine=chaine[1:]
    
    return str(chaine)
    
def sauver_liste(text, fenetre, bt1, lab):
    
    chaine=text.get("1.0",END)
    
    liste_correcte=True
    chaine_corrigee=""
    for ligne in chaine.split('\n'):
        if (supprime_espace(ligne)==""):
            continue                    # ignore lignes vides ou ne contenant que des espaces
            
        if (ligne.count(";") != 1):     # on doit avoir un seul ; par ligne non vide
            liste_correcte=False
        else:
            fr=supprime_espace(ligne.split(";")[0])
            et=supprime_espace(ligne.split(";")[1])
            chaine_corrigee+=fr+";"+et+"\n"
            # verifie la taille des expressions (entre 1 et LONGUEUR_MAX caractères)
            if (len(fr) < 1 or len(fr)>LONGUEUR_MAX or len(et)<1 or len(et)>LONGUEUR_MAX):
                liste_correcte=False
                
    if (liste_correcte == False):
        tkinter.messagebox.showerror(title="Erreur !", message="Erreur dans la liste !\n\nVérifie:\n- que tu as un et un seul ; par ligne\n- que les 2 expressions ont entre 1 et "+str(LONGUEUR_MAX)+" charactères")
        return
             
    # -- on demande le nom du fichier si besoin
    nom_fichier=lab.cget("text")
    print("NOM_FICHIER=|"+nom_fichier+"|")
    while (nom_fichier==""):
        myFormats = [ ('vocabulaire','*.voc') ]
        nom_fichier = tkinter.filedialog.asksaveasfilename(parent=fenetre_principale,initialdir=FOLDER_VOCA,filetypes=myFormats,title="Choisis un nom pour cette liste...")
     
    # si le nom de fichier ne finit pas par ".voc", on rajoute ce suffixe
    print("NOM_FICHIER initial = |"+nom_fichier+"|")
    if (len(nom_fichier)<4):
        nom_fichier+=".voc"
    else:
        suffixe=nom_fichier[len(nom_fichier)-4:len(nom_fichier)]
        suffixe=suffixe.lower()
        if (suffixe!=".voc"):
            nom_fichier+=".voc"
    print("NOM_FICHIER corrige = |"+nom_fichier+"|")
    
    # -- on affiche le nom du fichier
    lab.config(text=nom_fichier)
    
    # -- on sauve la liste
    fichier=codecs.open(nom_fichier,'w',encoding='utf-8')
    fichier.write(chaine_corrigee)
    fichier.close   
    
    print("liste sauvee !")
    
    # -- on disable le boutons "Sauver" 
    bt1.config(state=DISABLED)   
    
    
# ---------- creer/modifier liste        
#def editer_active_boutons(txt,bt1,event):
def editer_active_boutons(event):
    
    global editer_bouton_sauver
    if (len(event.char)!=0):
        editer_bouton_sauver.config(state=NORMAL)
        
def toplevel_editer(action):    
    
    # fonction appelee soit avec modifier soit avec creer
    # si modifier, faut demander le nom du fichier
    if (action=="modifier"):
        # D'abord, on charge une liste depuis un fichier
        myFormats = [ ('Vocabulaire','*.voc') ]
    
        fichier = tkinter.filedialog.askopenfile(parent=fenetre_principale,mode='r',initialdir=FOLDER_VOCA,filetypes=myFormats,title='Choisis une liste de vocabulaire')        
        if fichier == None:
            return
    
        chaine=fichier.read()
        nom_fichier=fichier.name
        fichier.close()    
    else:
        nom_fichier=""
        chaine=""
    
    # on rend la fenetre principale invisible
    fenetre_principale.withdraw()
        
    editer_fenetre=Toplevel(fenetre_principale)
    if (action=="modifier"):
        editer_fenetre.title("Afficher ou modifier une liste de vocabulaire")
    else:
        editer_fenetre.title("Créer une nouvelle liste de vocabulaire")
        
    editer_fenetre.resizable(width=False, height=False)
    editer_fenetre.bind("<Destroy>",fenetre_detruite)
    
    editer_frame=Frame(editer_fenetre, width=600, height=500)
    editer_frame.grid(sticky=N+S+E+W)
    #, column=2, row=3)
    editer_frame.columnconfigure(0, weight=1)
    editer_frame.columnconfigure(1, weight=1)        

    editer_label=Label(editer_frame, justify=LEFT, anchor=W, text="Entre une liste d'expressions en français ainsi que leur traduction dans la langue étrangère de ton choix sous la forme\nexpression française 1;traduction langue étrangère 1\nexpression française 2;traduction langue étrangère 2\n...")
    editer_label.grid(sticky=N+W+E+S, column=0, row=0, columnspan=2, padx=10, pady=10)
    
    editer_text=Text(editer_frame, height=20)
    editer_text.grid(sticky=N+W+E+S, column=0, row=1, columnspan=2, padx=10, pady=0)
    if (nom_fichier!=""):
        editer_text.delete("1.0",END)
        editer_text.insert(END,chaine)
    editer_text.update_idletasks()

    
    editer_label_nomfichier=Label(editer_frame, justify=LEFT, anchor=W, text=nom_fichier)
    editer_label_nomfichier.grid(sticky=N+W+E+S, column=0, row=2, columnspan=2, padx=10, pady=0)
    
    global editer_bouton_sauver
    
    editer_bouton_sauver=Button(editer_frame, text="Sauver", state=DISABLED)
    editer_bouton_sauver.grid(column=0,row=3, padx=10, pady=10)
    editer_bouton_sauver.update()
    
    editer_bouton_sauver.config(command= lambda: sauver_liste (editer_text, editer_fenetre, editer_bouton_sauver, editer_label_nomfichier))
        
    editer_bouton_sortir=Button(editer_frame, text="Sortir", command=editer_fenetre.destroy)
    editer_bouton_sortir.grid(column=1,row=3, padx=10, pady=10)   
    
    editer_text.bind('<Key>', editer_active_boutons)
    
    

# ---------
# Chaque fois qu'on ouvre une fenetre TopLevel, on masque la fenetre principale
# pour empecher l'ouverture de multiple Toplevel.
# On a "trappé" l'evenement destroy sur ces fenetres TopLevel pour 
# rafficher la fenetre principale quand on ferme la fenetre Toplevel
def fenetre_detruite(event):  
    # on rend visible la fenetre Root a nouveau
    fenetre_principale.deiconify()

# -------------------- PROGRAMME PRINCIPAL
if __name__ == "__main__":
    
    my_pad=20
    my_width=15
    my_height=5
    
    global fenetre_principale
    
    fenetre_principale = Tk()
    fenetre_principale.title('Apprends ton vocabulaire étranger')
    fenetre_principale.resizable(width=False, height=False)
    #fenetre.minsize()
    #fenetre.maxsize()

    # frame principale (TO DO: rendre la frame resizable avec la fenetre)
    frame_principale=Frame(fenetre_principale, bg="white")
    frame_principale.grid(sticky=N+S+E+W)
        
    # Font du texte dans les boutons
    my_font=Font(family='Helvetica',size=20)
    my_font2=Font(family='Helvetica',size=14)
    
    # bouton Creer 
    bt_creer=Button(frame_principale, text="CREER\nUNE LISTE", bg="#D0FFD0", activebackground="#40FF40", width=my_width, height=my_height, font=my_font, relief="flat", command=lambda: toplevel_editer("creer"))
    bt_creer.grid(row=0, column=0, padx=my_pad, pady=my_pad)
        
    # bouton Editer
    bt_editer=Button(frame_principale, text="AFFICHER\nou MODIFIER\nUNE LISTE", bg="#FFFFD0", activebackground="#FFFF40", width=my_width, height=my_height, font=my_font, relief="flat", command=lambda: toplevel_editer("modifier"))
    bt_editer.grid(row=0, column=1, padx=my_pad, pady=my_pad)
    
    # bouton Tester
    bt_tester=Button(frame_principale, text="TESTER\nFRANCAIS\nvers\nETRANGER", bg="#FFD0D0", activebackground="#FF4040", width=my_width, height=my_height, font=my_font, relief="flat", command=lambda: toplevel_tester("fr2et"))
    bt_tester.grid(row=1, column=0, padx=my_pad, pady=my_pad)
        
    # bouton Statistiques
    bt_stats=Button(frame_principale, text="TESTER\nETRANGER\nvers\nFRANCAIS", bg="#D0D0FF", activebackground="#4040FF", width=my_width, height=my_height, font=my_font, relief="flat", command=lambda: toplevel_tester("et2fr"))
    bt_stats.grid(row=1, column=1, padx=my_pad, pady=my_pad)
        
    # bouton Quitter
    bt_quitter=Button(frame_principale, text="QUITTER", bg="#D0D0D0", activebackground="#707070", font=my_font2, relief="flat", command=fenetre_principale.quit)
    bt_quitter.grid(row=2, column=0, columnspan=2, sticky=W+E+N+S, padx=my_pad, pady=my_pad)
        
    fenetre_principale.mainloop()
