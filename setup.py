from setuptools import setup, find_packages

setup(
    name="Outils_Tkinter",  # Nom de ton projet
    version="0.1.0",  # Version de ton projet
    description="Fourni une base de fenêtre, canvas, grille, boutons, reglages, ... pour l'affichage simple d'un jeu avec Tkinter",
    #long_description=open("README.md").read(),  # Utilisation du fichier README comme description complète
    author="Maxence CHOISEL",  # Nom de l'auteur
    author_email="maxencechoisel@gmail.com",  # Adresse email de l'auteur
    url="https://github.com/Maxe2005/Outils_Tkinter",  # URL du dépôt GitHub ou site du projet
    packages=find_packages(),  # Inclut tous les packages Python dans le projet
    install_requires=[  # Liste des dépendances du projet
        "Pillow>=10.4.0"
    ],
    classifiers=[  # Catégories pour ton projet (optionnel, mais utile pour PyPI)
        "Programming Language :: Python :: 3"
    ],
    python_requires=">=3.6",
)
