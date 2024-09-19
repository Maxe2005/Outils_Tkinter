import importlib

import tkinter as tk
from typing import Literal
from tkinter import ttk
from math import log
from PIL import Image, ImageTk
from functools import partial

from .Commentaires import Commentaire
from .Boutons import Boutons, Bouton ,Bcombobox
from .Infos import Infos, Infos_generales
from .Reglages import Reglages, Base_Reglages
from .Structure_globale import Entite_superieure, Canvas, Fenetre

__all__ = ["Commentaire",
           "Boutons", "Bouton", "Bcombobox",
           "Infos", "Infos_generales",
           "Reglages", "Base_Reglages",
           "Entite_superieure", "Canvas", "Fenetre"]

"""
def safe_import(module_name, from_list=None, alias=None):
    ""
    Tente d'importer un module ou des éléments spécifiques d'un module, et renvoie les objets importés.
    
    Args:
        module_name (str): Nom du module à importer.
        from_list (list, optional): Liste des éléments à importer depuis le module (pour "from module import ...").
        alias (str or list, optional): Alias ou liste d'alias à utiliser pour les objets importés.

    Returns:
        module or dict or None: Le module ou les éléments importés, ou None s'ils ne sont pas disponibles.
    ""
    try:
        module = importlib.import_module(module_name)
        
        # Si une from_list est fournie, importer les éléments spécifiés
        if from_list:
            imported_items = {}
            for i, item in enumerate(from_list):
                try:
                    imported_item = getattr(module, item)
                    if alias and isinstance(alias, list):
                        imported_items[alias[i]] = imported_item
                    else:
                        imported_items[item] = imported_item
                except AttributeError:
                    print(f"Warning: {item} not found in {module_name}. Some functionalities may not work.")
                    imported_items[item] = None
            return imported_items
        return module if alias is None else {alias: module}[alias]
        
    except ImportError:
        print(f"Warning: {module_name} is not installed. Some functionalities may not work.")
        return None


tk = safe_import('tkinter', alias='tk')  # Pour 'import tkinter as tk'

PIL_objects = safe_import('PIL', from_list=['Image', 'ImageTk'])
if PIL_objects:
    Image = PIL_objects['Image']
    ImageTk = PIL_objects['ImageTk']

tkinter_object = safe_import('tkinter', from_list=['ttk'])
ttk = tkinter_object["ttk"]

typing_object = safe_import('typing', from_list=['Literal'])
Literal = typing_object["Literal"]

math_object = safe_import('math', from_list=['log'])
log = math_object["log"]

functools_object = safe_import('functools', from_list=['partial'])
partial = functools_object["partial"]

"""


