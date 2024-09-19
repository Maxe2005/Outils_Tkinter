# Created on 19/09/24
# Author : Maxence CHOISEL



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

