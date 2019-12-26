# Création d'un exe pour Windowss avec CX_freeze

from cx_Freeze import setup, Executable

# Modules et images importés à partir du dossier actuel
includefiles = ["Carte.py", "Personnage.py", "Raycasting.py", "Annimation.py",
                "./Images/m1.png", "./Images/m2.png", "./Images/m3.png",
                "./Images/m4.png","./Images/m5.png", "./Images/m6.png",
                "./Images/m7.png", "./Images/m8.png", "./Images/m9.png",
                "./Images/wolf.png", "./Musiques/chanson0.ogg",
                "./Musiques/chanson1.ogg", "./Musiques/chanson2.ogg",
                "./Musiques/son_arme.wav"]

# Modules python importés
additionnelles =  ["math", "random", "numpy", "pygame", "pygame.locals",
                   'numpy.core._methods', 'numpy.lib.format']

# Paramétrage pour la création de l'exe
setup(
    name = "Wolfenstein3D",
    version = "0.2.0",
    description = "Raycasting",
    author = "Allan",
    options = {"build_exe": {"includes":additionnelles,
                             "include_files":includefiles}},
    executables = [Executable("Main.py")]
    )
