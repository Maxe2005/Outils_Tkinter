# Created on 19/09/24
# Author : Maxence CHOISEL

#import tkinter as tk
#from tkinter import ttk

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
    
    def lancement (self, reglages) :
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
        
        self.lancement_tous_les_reglages(reglages)
        
        self.init_header()
        self.ajout_separation(position=2, boss=self, color="green", is_separation_principale=True)
        self.canvas.grid(column=0, row=3)
        scrollbar_x.grid(column=0, row=4, columnspan=2, sticky=tk.EW)
        scrollbar_y.grid(column=1, row=0, rowspan=4, sticky=tk.NS)
        
        self.after(100, self.canvas.yview_moveto, '0')
        self.after(100, self.resize_canvas)
        #self.resizable(False, True)
        self.focus_set()
    
    def lancement_tous_les_reglages (self, reglages) :
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
            if callable(self.tous_les_reglages[reglage.name].init_entitees) :
                self.tous_les_reglages[reglage.name].init_entitees()
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

