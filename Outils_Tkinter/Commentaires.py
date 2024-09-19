# Created on 19/09/24
# Author : Maxence CHOISEL

#import tkinter as tk
#from typing import Literal

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

