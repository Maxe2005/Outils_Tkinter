# Created on 04/04/24
# Author : Maxence CHOISEL

import tkinter as tk
from tkinter import ttk
from typing import Literal
from math import log
from functools import partial


class Entite_superieure () :
    def init_nom_fenetre (self, fenetre) :
        self.fenetre = fenetre
    
    def init_variables_globales (self, tous_les_reglages) :
        """Permet de donner des valeurs arbitraires aux paramètres globaux (params par défaut)"""
        self.reglages_fen = False
        self.infos_fen = False
        self.tous_les_reglages = tous_les_reglages
        
    def lancement_fenetre (self, objet_fenetre:tk.Tk, liste_commentaires:list = []) :
        "Precessus de démarrage de la fenêtre"
        for i in range (3) :
            objet_fenetre.after(500+(i*100), objet_fenetre.redimentionner)
        objet_fenetre.focus()
        for com in liste_commentaires :
            objet_fenetre.after(500, com.test)
        objet_fenetre.protocol("WM_DELETE_WINDOW", partial(self.on_closing, objet_fenetre))
        objet_fenetre.mainloop()
    
    def ouvrir_param_defaut (self, path_fichier, type_de_parametre:str = "") :
        """Télécharge les paramètres par défauts """
        self.path_fichier_parametres_defaut = path_fichier
        self.parametres = {}
        self.autres_parametres = []
        with open(path_fichier) as f :
            if type_de_parametre :
                for ligne in f.readlines()[1:] :
                    l = ligne.split("\n")[0].split(",")
                    if l[0] == "parcoureur" :
                        if len(l[2:]) == 1 :
                            self.parametres[l[1]] = l[2]
                        else :
                            self.parametres[l[1]] = l[2:]
                    else :
                        self.autres_parametres.append(ligne)
            else :
                for ligne in f.readlines()[1:] :
                    l = ligne.split("\n")[0].split(",")
                    if len(l[1:]) == 1 :
                        self.parametres[l[0]] = l[1]
                    else :
                        self.parametres[l[0]] = l[1:]
    
    def save_param_defaut (self) :
        "Sauvegarde les paramètre dans le fichier dédié"
        with open(self.path_fichier_parametres_defaut, "w") as f :
            f.write("# Entitee du parametre, Nom du parametre, valeur du parametre\n")
            for param in self.parametres :
                if type(self.parametres[param]) == list :
                    f.write("parcoureur,"+param+","+",".join(self.parametres[param])+"\n")
                else :
                    f.write("parcoureur,"+param+","+str(self.parametres[param])+"\n")
            for param in self.autres_parametres :
                f.write(param)
    
    def on_closing (self, objet_fenetre) :
        "Permet de sauvegarder les changements effectués dans les réglages au moment de la fermeture de la fenêtre"
        self.save_param_defaut()
        objet_fenetre.destroy()
    
    def infos_generales (self, **kwarg) :
        "Lance ou met en avant la fenêtre des informations générales"
        if self.infos_fen :
            self.infos_fen.lift()
            self.infos_fen.focus()
        else :
            self.infos_fen = Infos_generales(self.fenetre, **kwarg)
            self.infos_fen.protocol("WM_DELETE_WINDOW", self.infos_fen_on_closing)
            self.infos_fen.mainloop()
    
    def infos_fen_on_closing (self) :
        "Permet d'enregistrer la fermeture de la fenêtre"
        self.infos_fen.destroy()
        self.infos_fen = False
    
    def init_reglages (self, **kwargs) :
        "Initialise l'objet fenêtre des réglages sans l'afficher"
        self.reglages_fen = Reglages(self.fenetre)
        self.reglages_fen.init_entitees (self, self.fenetre)
        self.reglages_fen.lancement(self.tous_les_reglages, **kwargs)
        self.reglages_fen.protocol("WM_DELETE_WINDOW", self.reglages_fen_on_closing)
    
    def reglages (self) :
        "Lance ou met en avant la fenêtre des réglages"
        if self.reglages_fen :
            self.reglages_fen.lift()
            self.reglages_fen.focus()
        else :
            self.reglages_fen.mainloop()
    
    def reglages_fen_on_closing (self) :
        "Permet d'enregistrer la fermeture de la fenêtre"
        self.reglages_fen.destroy()
        self.reglages_fen = False

#class Fenetre (tk.Tk) :


class Reglages (tk.Toplevel) :
    def __init__ (self, boss) :
        tk.Toplevel.__init__(self, boss)
        self.x = 550
        self.y = 500
        self.title("Réglages")
        self.geometry(str(self.x)+"x"+str(self.y))
        self.grid_columnconfigure(0, weight= 1)
        self.grid_columnconfigure(1, weight= 0)
        self.grid_rowconfigure(0, weight= 0)
        self.grid_rowconfigure(1, weight= 0)
        self.grid_rowconfigure(2, weight= 0)
        self.grid_rowconfigure(3, weight= 1)
        self.grid_rowconfigure(4, weight= 0)
        
        self.width_titres = 35
    
    def lancement (self, reglages, **kwargs) :
        self.canvas = tk.Canvas(self)
        self.content = tk.Frame(self.canvas)
        self.content.bind("<Configure>", self.resize_frame)
        #self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.bind('<Enter>', self._bound_to_mousewheel)
        self.bind('<Leave>', self._unbound_to_mousewheel)
        
        scrollbar_y=tk.Scrollbar(self, orient=tk.VERTICAL, command=self.canvas.yview)
        scrollbar_x=tk.Scrollbar(self, orient=tk.HORIZONTAL, command=self.canvas.xview)
        
        self.canvas.create_window((0, 0), window=self.content)
        self.canvas.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        self.lancement_tous_les_reglages(reglages, **kwargs)
        
        self.init_header()
        self.ajout_separation(position=2, boss=self, color="green", is_separation_principale=True)
        self.canvas.grid(column=0, row=3)
        scrollbar_x.grid(column=0, row=4, columnspan=2, sticky=tk.EW)
        scrollbar_y.grid(column=1, row=0, rowspan=4, sticky=tk.NS)
        
        self.after(100, self.canvas.yview_moveto, '0')
        self.after(100, self.resize_canvas)
        #self.resizable(False, True)
        self.focus_set()
    
    def lancement_tous_les_reglages (self, reglages, **kwargs) :
        self.tous_les_reglages = {}
        self.separations = []
        i = 0
        for regl in reglages :
            if i > 0 :
                self.ajout_separation(position=i)
                i += 1
            reglage = regl(self.content)
            self.tous_les_reglages[reglage.name] = reglage
            self.tous_les_reglages[reglage.name].init_entitees_de_base(self, self.big_boss, self.fenetre)
            self.tous_les_reglages[reglage.name].init_entitees(**kwargs)
            self.tous_les_reglages[reglage.name].lancement()
            self.tous_les_reglages[reglage.name].grid(row=i)
            i += 1
    
    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def _bound_to_mousewheel(self, event):
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
    
    def _unbound_to_mousewheel(self, event):
        self.canvas.unbind_all("<MouseWheel>")
    
    def resize_canvas(self) :
        self.canvas.configure(width=self.content.winfo_width(),\
            height=self.content.winfo_height())
    
    def init_entitees (self, big_boss, fenetre) :
        self.big_boss = big_boss
        self.fenetre = fenetre
    
    def resize_frame(self, event=None):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))        
    
    def ajout_separation (self, position, boss=None, color="grey", is_separation_principale=False) :
        if boss is None :
            boss = self.content
        separation = tk.Text(boss, bg=color, pady=5, height=1, font=("Helvetica", 1))
        separation['state'] = 'disabled'
        if is_separation_principale :
            separation.grid(column=0, row=position, sticky=tk.NSEW)
        else :
            self.separations.append(separation)
            separation.grid(column=0, row=position, pady=30, sticky=tk.NSEW)
    
    def init_header (self) :        
        self.header = tk.Frame(self, border=10)
        self.header.grid(column=0, row=0, sticky=tk.NSEW)
        self.header.grid_columnconfigure(0, weight= 1)
        self.header.grid_columnconfigure(1, weight= 1)
        self.header.grid_columnconfigure(2, weight= 1)
        
        btn = tk.Button(self.header, text="Tout", command=self.afficher_tous_params, font=("Helvetica", 14), bg="green", fg="white")
        btn.grid(column=0, row=0, sticky=tk.W)
        
        noms_reglages = list(self.tous_les_reglages.keys())
        self.combobox_header = ttk.Combobox(self.header, values=noms_reglages, state="readonly", justify="center", width=15, height=15, style="TCombobox", font=("Helvetica", 13))
        self.combobox_header.set("Réglages")
        self.combobox_header.bind("<<ComboboxSelected>>", self.affiche_type_reglage_particulier)
        self.combobox_header.grid(column=1, row=0)
        
        btn = tk.Button(self.header, text="Appliquer", command=self.appliquer_modifications, font=("Helvetica", 14), bg="blue", fg="white")
        btn.grid(column=2, row=0, sticky=tk.E)
        
        self.var_alerte_mauvaise_entree = tk.IntVar()
        self.var_alerte_mauvaise_entree.set(int(self.big_boss.parametres["lab alea alerte mauvaise entree"]))
        checkbtn_alerte_mauvaise_entree = tk.Checkbutton(self, variable= self.var_alerte_mauvaise_entree ,compound=tk.LEFT, text="Alerte pour mauvaise entrée", border=10, font=("Helvetica", 13))
        checkbtn_alerte_mauvaise_entree.grid(column=0, row=1, sticky=tk.W)
    
    def effacer_tous_reglages (self) :
        for nom_reg in self.tous_les_reglages :
            self.tous_les_reglages[nom_reg].grid_forget()
        for sep in self.separations :
            sep.grid_forget()
        self.separations = []
    
    def affiche_type_reglage_particulier (self, event=None) :
        reglage = self.combobox_header.get()
        self.combobox_header.set("Réglages")
        self.effacer_tous_reglages()
        self.tous_les_reglages[reglage].grid(column=0, row=0)
        self.after(100, self.resize_canvas)
        self.after(100, self.resize_frame)
        self.after(100, self.canvas.yview_moveto, '0')
    
    def afficher_tous_params (self) :
        self.effacer_tous_reglages()
        i = 0
        for name_reg in self.tous_les_reglages :
            if i > 0 :
                self.ajout_separation(position=i)
                i += 1
            self.tous_les_reglages[name_reg].grid(row=i)
            i += 1
        self.after(100, self.resize_canvas)
        self.after(100, self.canvas.yview_moveto, '0')
    
    def appliquer_modifications (self) :
        for reg_name in self.tous_les_reglages :
            self.tous_les_reglages[reg_name].appliquer_modifications()
        self.big_boss.parametres["lab alea alerte mauvaise entree"] = self.var_alerte_mauvaise_entree.get()

class Base_Reglages (tk.Frame) :
    def __init__ (self, boss, name) :
        tk.Frame.__init__(self, boss, border=10)
        self.name = name
    
    def init_entitees_de_base (self, boss, big_boss, fenetre) :
        self.boss = boss
        self.big_boss = big_boss
        self.fenetre = fenetre
    
    def lancement (self, titre) :
        "Initialise la zone de titre"
        self.text = tk.Text(self, wrap= tk.WORD, width=self.boss.width_titres, height=1, padx=50, pady=30, font=("Helvetica", 15))
        self.text.insert(0.1, titre)
        self.text['state'] = 'disabled'
        self.text.tag_add('entier','1.0',tk.END)
        self.text.tag_config('entier', justify=tk.CENTER)
        self.text.grid(column=0, row=0, sticky=tk.NSEW)


class Boutons (tk.Frame) :
    def __init__(self, boss, big_boss, fenetre:tk.Tk, class_comentaire=None) :
        tk.Frame.__init__(self, boss)
        self.big_boss = big_boss
        self.fenetre = fenetre
        self.items = {}
        if class_comentaire is None :
            self.class_comentaire = Commentaire
        else :
            self.class_comentaire = class_comentaire
    
    def init_grid (self, nb_lignes=1, nb_colones=1) :
        "Permet de définir la zone que vas occuper les boutons"
        self.nb_lignes = nb_lignes
        self.nb_colones = nb_colones
        for i in range (self.nb_colones) :
            self.grid_columnconfigure(i, weight= 1)
        for i in range (self.nb_lignes) :
            self.grid_rowconfigure(i, weight= 1)
    
    def init_visible_debut (self) :
        "Enregistre tous les boutons visible au lancement"
        self.is_visible_debut = []
        for bout in self.items :
            if self.items[bout][2] == "Visible" :
                self.is_visible_debut.append(bout)

    def def_bouton (self, nom_affiche:str, effet, position, boss=None, nom_diminutif:str = "", visibilite:str = "Visible", type_combobox:list = [], sticky:str="") :
        """Permet de définir un bouton

        Args:
            - nom_affiche (str): Nom visible sur le bouton
            - effet (_fonction_): la fonction à appeler si le bouton est préssé.
            - position (int or tuple of int): la position pour grid (column, row). Si le nombre de colones (ou de lignes) est de 1, seul le row est nesséssaire (et inversement pour colomn).
            - boss (_type_, optional): entitée sur leaquelle est placé le bouton . Defaults to own class Boutons.
            - nom_diminutif (str, optional): nom plus cours. Defaults to "".
            - visibilite (str, optional): visible dès le début? (valeurs possibles : 'Visible' ou 'Caché'). Defaults to "Visible".
            - type_combobox (list, optional): si le bouton est un ttk.Combobox remplire la list avec la liste des éléments à mettre dans le combobox. Defaults to [] (means off).
            - sticky (str, optional) : Permet d'ajouter un sticky sur le positionement du bouton.
            - commentaire (str, optional): ajoute un commentaire avec le bouton. Defaults to "".
            - aligne_in (str, optional): Alignement du texte à l'interieur du commentaire. Defaults to "center".
            - position_out (list, optional): L'ordre d'essai de positionnement autour du widget ('L' pour left, 'R' pour right, 'T' pour top et 'B' pour bottom). Defaults to ["L","B","R","T"].
        """
        if not(nom_diminutif) :
            nom_diminutif = nom_affiche
        if boss is None :
            boss = self
        if type_combobox :
            btn = Bcombobox(boss, effet, position, visibilite, nom_affiche, values=type_combobox)
            self.items[nom_diminutif] = btn
        else :
            btn = Bouton (boss, position, visibilite, text=nom_affiche, command=effet)
            self.items[nom_diminutif] = btn
        if visibilite == "Visible" :
            if self.nb_colones == 1 :
                ligne = self.items[nom_diminutif].position
                colone = 0
            elif self.nb_lignes == 1 :
                colone= self.items[nom_diminutif].position
                ligne = 0
            else :
                colone = self.items[nom_diminutif].position[0]
                ligne = self.items[nom_diminutif].position[1]
            if sticky :
                self.items[nom_diminutif].grid(column= colone, row= ligne, sticky= sticky)
            else :
                self.items[nom_diminutif].grid(column= colone, row= ligne)
        return btn

    def redimentionner (self, text_size = None) :
        "Redimentionne le texte des boutons et de leurs commentaires "
        if text_size is None :
            text_size = int(5*log(self.fenetre.winfo_width()/100))
        for bout in self.items :
            self.items[bout].configure(font=("Verdana", text_size))
            if self.items[bout].commentaire :
                self.items[bout].commentaire.commentaire_label.config(font=("Verdana", text_size))

    def afficher (self, nom_bouton) :
        self.items[nom_bouton].grid(row= self.items[nom_bouton].position)
        self.items[nom_bouton].visibilite = "Visible"

    def cacher (self, nom_bouton) :
        self.items[nom_bouton].grid_forget()
        self.items[nom_bouton].visibilite = "Caché"

    def affiche_boutons_debut (self) :
        for bout in self.is_visible_debut :
            self.afficher(bout)
    
    def cache_tout_sauf (self, ele=[]) :
        for bout in self.items :
            if bout not in ele :
                self.cacher(bout)
    
    def renommer (self, nom_bouton:str, new_nom_bouton:str) :
        assert nom_bouton in self.items
        if type(self.items[nom_bouton]) == Bouton :
            self.items[nom_bouton].configure(text= new_nom_bouton)
        elif type(self.items[nom_bouton]) == Bcombobox :
            self.items[nom_bouton].set(new_nom_bouton)

    def is_visible (self, nom_bouton:str) :
        return self.items[nom_bouton].visibilite == "Visible"
    
    def supprimer (self, nom_bouton:str) :
        self.cacher (nom_bouton)
        self.items[nom_bouton].destroy()

class Bouton (tk.Button) :
    def __init__ (self, boss, position, visibilite, **kwarg) :
        tk.Button.__init__(self, boss, **kwarg)
        self.position = position
        self.visibilite = visibilite
        self.commentaire = False
    
    def add_commentaire (self, fenetre, texte, **kwarg) :
        "Permet d'attacher un commentaire au bouton"
        self.commentaire = Commentaire(fenetre, self, texte, **kwarg)
        return self.commentaire

class Bcombobox (ttk.Combobox) :
    def __init__ (self, boss, effet, position, visibilite, nom_affiche, **kwarg) :
        ttk.Combobox.__init__(self, boss, state="readonly", justify="center", width=12, height=2, takefocus=False, style="TCombobox", **kwarg)
        self.position = position
        self.visibilite = visibilite
        self.commentaire = False
        self.set(nom_affiche)
        self.bind("<<ComboboxSelected>>", lambda event:effet(self, event))
    
    def add_commentaire (self, fenetre, texte, **kwarg) :
        "Permet d'attacher un commentaire au bouton"
        self.commentaire = Commentaire(fenetre, self, texte, **kwarg)
        return self.commentaire


class Commentaire (tk.Toplevel) :
    def __init__(self, fenetre, widget, texte:str, aligne_in:str = "center" | Literal["center", "left", "right","top", "bottom"] , position_out:list = ["L","B","R","T"]) -> None :
        """Permet d'affecter un commentaire à un widget

        Args:
            - fenetre (tk.Tk or tk.Toplevel): la fenêtre parente du commentaire
            - widget (_widget tkiner_): le widget auquel est attaché et destiné le commentaire
            - texte (str): le contenu du commentaire
            - aligne_in (str, optional): Alignement du texte à l'interieur du commentaire. Defaults to "center".
            - position_out (list, optional): L'ordre d'essai de positionnement autour du widget ('L' pour left, 'R' pour right, 'T' pour top et 'B' pour bottom). Defaults to ["L","B","R","T"].
        """
        tk.Toplevel.__init__(self, master=fenetre)
        self.fenetre = fenetre
        self.widget = widget
        self.position_out = position_out
        self.init_position_out_posibles()
        self.withdraw()  # Masquer initialement le commentaire
        self.overrideredirect(True)  # Supprimer la bordure de la fenêtre
        #if aligne_in == "center" :
        just = tk.CENTER
        if aligne_in == "left" :
            just = tk.LEFT
        elif aligne_in == "right" :
            just = tk.RIGHT
        elif aligne_in == "top" :
            just = tk.TOP
        elif aligne_in == "bottom" :
            just = tk.BOTTOM
        self.commentaire_label = tk.Label(self, text=texte, justify=just, bg="grey", fg="white")
        self.commentaire_label.grid()
        self.marge_bouton = 10  # En pixels
        self.widget.bind("<Enter>", self.attendre_avant_afficher)
        self.widget.bind("<Leave>", self.effacer_commentaire)

    def init_position_out_posibles (self) :
        self.position_out_posibles = {}
        self.position_out_posibles["L"] = self.def_pos_left
        self.position_out_posibles["B"] = self.def_pos_bottom
        self.position_out_posibles["R"] = self.def_pos_right
        self.position_out_posibles["T"] = self.def_pos_top
    
    def attendre_avant_afficher (self, event=None) :
        self.affichage_possible = True
        self.after(1000, self.afficher_commentaire)
    
    def afficher_commentaire(self) :
        if self.affichage_possible :
            x, y = self.widget.winfo_rootx(), self.widget.winfo_rooty()
            self.position_out_posibles[self.position_out[0]](x, y)
            self.verif_not_out_window()
            i = 1
            self.conditions(x,y)
            while (self.at_least_one_corner_in or self.passing_in_front) and i < len(self.position_out) :
                self.position_out_posibles[self.position_out[i]](x, y)
                self.verif_not_out_window()
                i += 1
                self.conditions(x,y)
            if i == len(self.position_out) :
                self.def_pos_bottom(x, y)
            self.geometry(f"+{self.pos_x}+{self.pos_y}") 
            self.deiconify()  # Afficher le commentaire
    
    def conditions (self, x, y) :
        x1_in = self.pos_x < x < self.pos_x + self.winfo_width()
        x2_in = self.pos_x < x + self.widget.winfo_width() < self.pos_x + self.winfo_width()
        y1_in = self.pos_y < y < self.pos_y + self.winfo_height()
        y2_in = self.pos_y < y + self.widget.winfo_height() < self.pos_y + self.winfo_height()
        self.at_least_one_corner_in = (x1_in or x2_in) and (y1_in or y2_in)
        x1_avant = self.pos_x > x
        x2_apres = x + self.widget.winfo_height() > self.pos_x + self.winfo_height()
        y1_avant = self.pos_y > y
        y2_apres = y + self.widget.winfo_height() > self.pos_y + self.winfo_height()
        passing_in_front_x = x1_avant and x2_apres and (y1_in or y2_in)
        passing_in_front_y = y1_avant and y2_apres and (x1_in or x2_in)
        hide_completely = x1_avant and x2_apres and y1_avant and y2_apres
        self.passing_in_front = passing_in_front_x or passing_in_front_y or hide_completely
    
    def def_pos_left (self, x, y) :
        self.pos_x = x - self.winfo_width() - self.marge_bouton
        self.pos_y = round(y + (self.widget.winfo_height()/2) - self.winfo_height()/2)
    
    def def_pos_right (self, x, y) :
        self.pos_x = x + self.widget.winfo_width() + self.marge_bouton
        self.pos_y = round(y + (self.widget.winfo_height()/2) - self.winfo_height()/2)
    
    def def_pos_bottom (self, x, y) :
        self.pos_x = round(x + (self.widget.winfo_width() / 2) - (self.winfo_width() / 2))
        self.pos_y = y + self.widget.winfo_height() + self.marge_bouton
    
    def def_pos_top (self, x, y) :
        self.pos_x = round(x + (self.widget.winfo_width() / 2) - (self.winfo_width() / 2))
        self.pos_y = y - self.winfo_height() - self.marge_bouton
    
    def verif_not_out_window(self) :
        marge = 10  # En pixels
        if self.pos_x - marge < self.fenetre.winfo_rootx() :
            self.pos_x = self.fenetre.winfo_rootx() + marge
        elif self.pos_x + self.winfo_width() + marge > self.fenetre.winfo_rootx() + self.fenetre.winfo_width() :
            self.pos_x = self.fenetre.winfo_rootx() + self.fenetre.winfo_width() - self.winfo_width() - marge
        if self.pos_y < self.fenetre.winfo_rooty() - marge :
            self.pos_y = self.fenetre.winfo_rooty() + marge
        elif self.pos_y + self.winfo_height() + marge > self.fenetre.winfo_rooty() + self.fenetre.winfo_height() :
            self.pos_y = self.fenetre.winfo_rooty() + self.fenetre.winfo_height() - self.winfo_height() - marge
    
    def effacer_commentaire(self, event):
        self.affichage_possible = False
        self.withdraw()  # Masquer le commentaire lorsque le curseur quitte le bouton

    def test (self) :
        """
        Permet d'afficher brièvement le commentaire pour que la fenêtre puisse correctement définir ses dimentions
        """
        self.deiconify()
        self.after(200, self.withdraw)


class Infos (tk.Toplevel) :
    def __init__(self, boss, titre:str = "test", texte:str = "test", pourcentage_largeur:int = 90, police:str = "arial", taille_police:int = 15, color:int = "white") :
        tk.Toplevel.__init__(self,boss)
        self.boss = boss
        self.title(titre)
        taille_ligne_max = 0
        for ligne in texte.split("\n") :
            if len(ligne) > taille_ligne_max :
                taille_ligne_max = len(ligne)
        self.text = tk.Text(self, wrap= tk.WORD, width=int((pourcentage_largeur/100)*taille_ligne_max), height=texte.count("\n")+6, padx=30, pady=30, font=(police, taille_police), bg=color)
        self.text.insert(1.0, titre+"\n\n", ("titre"))
        self.text.insert("end", texte, ("content"))
        self.text.insert('end', '\n\nMax :)'+" "*10, ("footer")) 
        self.text.tag_config('titre', font=police+" "+str(taille_police+2), justify=tk.CENTER)
        self.text.tag_config('content', justify=tk.CENTER)
        self.text.tag_config('footer', justify=tk.RIGHT)
        self.text['state'] = 'disabled'
        self.text.pack()
        self.resizable(False, False)
        self.focus_set()
        self.mainloop()

class Infos_generales (tk.Toplevel) :
    def __init__ (self, boss) :
        tk.Toplevel.__init__(self, boss)
        self.title("Informations Générales")
        self.nb_lignes = 2
        self.nb_colones = 1
        for i in range (self.nb_colones) :
            self.grid_columnconfigure(i, weight= 1) 
        for i in range (self.nb_lignes) :
            self.grid_rowconfigure(i, weight= 1)
        
        self.resizable(False, False)
        self.focus_set()
    
    def init_titre_et_texte (self, titre:str = "TITRE", contenu:str = "CONTENU", pourcentage_largeur:int = 90, police:str = "Helvetica", taille_police:int = 15, color:int = "white") :
        taille_ligne_max = 0
        for ligne in contenu.split("\n") :
            if len(ligne) > taille_ligne_max :
                taille_ligne_max = len(ligne)
        text = tk.Text(self, wrap= tk.WORD, width=int((pourcentage_largeur/100)*taille_ligne_max), height=contenu.count("\n")+6, padx=30, pady=30, font=(police, taille_police), bg=color)
        text.insert(0.1, titre, ("titre"))
        text.insert("end", "\n\n\n")
        text.insert("end", contenu, ("content"))
        text.tag_config("titre", foreground="red", font=("Helvetica", 20), justify='center')
        text.tag_config("content", justify="center")
        text['state'] = 'disabled'
        text.grid(column=0, row=0, sticky=tk.NSEW)
        
        
        bouton_1 = tk.Button (self, text="Ouvrir le Builder de Labyrinthes", padx=20, pady=10, font=("Helvetica", 13), bg="blue", fg= "white", \
            command=self.big_boss.lancement_builder_labs)
        bouton_1.configure(state = 'disabled', bg="grey")
        bouton_1.grid(column=0, row=1)

