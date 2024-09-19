# Created on 19/09/24
# Author : Maxence CHOISEL

import tkinter as tk
from PIL import Image, ImageTk
from .Reglages import Reglages
from functools import partial

class Entite_superieure () :
    def init_variables_tres_globales (self) :
        """Permet de donner des valeurs arbitraires aux paramètres globaux (params par défaut)"""
        self.is_reglages_fen_on = False
        self.is_infos_fen_on = False
        
    def lancement_fenetre (self, liste_commentaires:list = []) :
        "Precessus de démarrage de la fenêtre"
        for i in range (3) :
            self.fenetre.after(500+(i*100), self.fenetre.redimentionner)
        self.fenetre.focus()
        for com in liste_commentaires :
            self.fenetre.after(500, com.test)
        self.fenetre.protocol("WM_DELETE_WINDOW", partial(self.on_closing, self.fenetre))
        self.fenetre.mainloop()
    
    def ouvrir_param_defaut (self, path_fichier, type_de_parametre:str = "") :
        """Télécharge les paramètres par défauts """
        self.path_fichier_parametres_defaut = path_fichier
        self.parametres = {}
        self.autres_parametres = []
        with open(path_fichier) as f :
            if type_de_parametre :
                for ligne in f.readlines()[1:] :
                    li = ligne.split("\n")[0].split(",")
                    if li[0] == type_de_parametre :
                        if len(li[2:]) == 1 :
                            self.parametres[li[1]] = li[2]
                        else :
                            self.parametres[li[1]] = li[2:]
                    else :
                        self.autres_parametres.append(ligne)
            else :
                for ligne in f.readlines()[1:] :
                    li = ligne.split("\n")[0].split(",")
                    if len(li[1:]) == 1 :
                        self.parametres[li[0]] = li[1]
                    else :
                        self.parametres[li[0]] = li[1:]
    
    def save_param_defaut (self) :
        "Sauvegarde les paramètre dans le fichier dédié"
        with open(self.path_fichier_parametres_defaut, "w") as f :
            f.write("# Entitee du parametre, Nom du parametre, valeur du parametre\n")
            for param in self.parametres :
                if type(self.parametres[param]) is list :
                    f.write("parcoureur,"+param+","+",".join(self.parametres[param])+"\n")
                else :
                    f.write("parcoureur,"+param+","+str(self.parametres[param])+"\n")
            for param in self.autres_parametres :
                f.write(param)
    
    def on_closing (self, objet_fenetre) :
        "Permet de sauvegarder les changements effectués dans les réglages au moment de la fermeture de la fenêtre"
        self.save_param_defaut()
        objet_fenetre.destroy()
    
    def init_infos_generales (self, nom_sous_class_infos_generales) :
        self.nom_sous_class_infos_generales = nom_sous_class_infos_generales
    
    def infos_generales (self) :
        "Lance ou met en avant la fenêtre des informations générales"
        if self.is_infos_fen_on :
            self.infos_fen.lift()
            self.infos_fen.focus()
        else :
            self.infos_fen = self.nom_sous_class_infos_generales(self.fenetre, self)
            self.infos_fen.protocol("WM_DELETE_WINDOW", self.infos_fen_on_closing)
            self.is_infos_fen_on = True
            self.infos_fen.mainloop()
    
    def infos_fen_on_closing (self) :
        "Permet d'enregistrer la fermeture de la fenêtre"
        self.infos_fen.destroy()
        self.is_infos_fen_on = False
    
    def init_reglages (self, tous_les_reglages) :
        "Initialise l'objet fenêtre des réglages sans l'afficher. Pour l'afficher : appeller la fonction 'reglages'"
        self.tous_les_reglages = tous_les_reglages
    
    def reglages (self) :
        "Lance ou met en avant la fenêtre des réglages"
        if self.is_reglages_fen_on :
            self.reglages_fen.lift()
            self.reglages_fen.focus()
        else :
            self.reglages_fen = Reglages(self.fenetre)
            self.reglages_fen.init_entitees (self, self.fenetre)
            self.reglages_fen.lancement(self.tous_les_reglages)
            self.reglages_fen.protocol("WM_DELETE_WINDOW", self.reglages_fen_on_closing)
            self.is_reglages_fen_on = True
            self.reglages_fen.mainloop()
    
    def reglages_fen_on_closing (self) :
        "Permet d'enregistrer la fermeture de la fenêtre"
        self.reglages_fen.destroy()
        self.is_reglages_fen_on = False


class Fenetre (tk.Tk) :
    def init_logo (self, boss, params=[0,0]) :
        self.logo = tk.Button(boss, command=self.big_boss.infos_generales)
        self.logo.grid(column=params[0], row=params[1])
    
    def open_image (self, path, x_max=200, pourcentage_x_max=70) :
        self.image = Image.open(path)
        xx, yy = self.image.size
        ratio = xx / yy
        x = round(pourcentage_x_max/100 * x_max)
        y = round(x / ratio)
        self.image = self.image.resize((x,y))
        self.image_photo = ImageTk.PhotoImage(self.image)
        self.logo["image"] = self.image_photo


class Canvas (tk.Canvas) :
    def __init__ (self, color) :
        tk.Canvas.__init__(self)
        self.couleurs(change=False, initial_value=color)
    
    def taille_auto (self) :
        "Calcule la taille en pixel d'un coté des cases carré à partir de la hauteur h et le la longeur l de la grille de définition"
        if self.winfo_height() / self.grille.y < self.winfo_width() / self.grille.x :
            self.taille = self.winfo_height() / (self.grille.y+1)
        else :
            self.taille = self.winfo_width() / (self.grille.x+1)
    
    def origines (self) :
        "Calcule et renvoi sous forme de tuple les origines en x et y (en haut à gauche du canvas)"
        self.origine_x = (self.winfo_width() - (self.taille * (self.grille.x-1))) / 2
        self.origine_y = (self.winfo_height() - (self.taille * (self.grille.y-1))) / 2
        assert self.origine_x > 0 and self.origine_y > 0
    
    def barre_verticale (self, ox, oy, t, color) :
        """Trace dans le canvas une ligne verticale.
        Depuis les coordonées (x,y) = (<ox>,<oy>),
        vers la droite sur <t> pixels et
        avec la couleur <color>"""
        self.create_line (ox,oy,ox,oy+t, fill= color)
    
    def barre_horizontale (self, ox, oy, t, color) :
        """Trace dans le canvas une ligne verticale.
        Depuis les coordonées (x,y) = (<ox>,<oy>),
        vers la droite sur <t> pixels et
        avec la couleur <color>"""
        self.create_line (ox,oy,ox+t,oy, fill= color)
    
    def couleurs (self, change=True, initial_value=False, event=None) :
        if change :
            if self.couleur_mode == "white" :
                self.couleur_mode = "black"
            else :
                self.couleur_mode = "white"
        elif initial_value :
            self.couleur_mode = initial_value
        if self.couleur_mode == "white" :
            self.color_canvas = "white"
            self["bg"] = self.color_canvas
            self.color_grille = "black"
            self.color_balle = "blue"
            self.oposit_color_balle = "red"
            self.color_balle_out = "black"
        elif self.couleur_mode == "black" :
            self.color_canvas = "black"
            self["bg"] = self.color_canvas
            self.color_grille = "white"
            self.color_balle = "red"
            self.oposit_color_balle = "blue"
            self.color_balle_out = "white"
        if change :
            self.refresh_lab()

