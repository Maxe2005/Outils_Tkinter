# Created on 19/09/24
# Author : Maxence CHOISEL

import tkinter as tk
from tkinter import ttk
from math import log
from .Commentaires import Commentaire

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
        if type(self.items[nom_bouton]) is Bouton :
            self.items[nom_bouton].configure(text= new_nom_bouton)
        elif type(self.items[nom_bouton]) is Bcombobox :
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

