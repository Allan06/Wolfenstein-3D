# -*- coding: utf-8 -*

# __________________________WOLFENSTEIN 3D - CARTE_____________________________
# =============================================================================
# carte.py
# Version 0.3 (21 Février 2019)
# PAJANY Allan
# 3ème Année - Licence Informatique - UTLN
# =============================================================================

"""  Module carte.py contenant les constantes globales ainsi que les focntions
     liées à la génération d'une carte.
"""

from math import cos, sin, trunc
from random import choice, randint
from collections import deque

# =========================================================================== #
# ====================|            CONSTANTES          |===================== #
# =========================================================================== #

# Dimensions de la Window
# -----------------------------------------------------------------------------
UNITE = 64                            # Dimension d'une case (nombre de pixels)
CASE_L = 120                         # Nombre de cases en largeur (140 pour FS)
CASE_H = trunc(CASE_L * (1080 / 1920))             # Nombre de cases en hauteur
WINDOW_L, WINDOW_H = CASE_L * UNITE, CASE_H * UNITE

# Dimensions de la Viewport
# -----------------------------------------------------------------------------
_MULT = 13
LARGEUR, HAUTEUR = CASE_L * _MULT, CASE_H * _MULT     # Largeur/hauteur fenêtre
U_CARTE = LARGEUR // CASE_L                                 # Taille d'une case
NB_COUL, RAD = 11, 180 / 3.1415926535897   # Nbr couleurs/textures max, Radians


# =========================================================================== #
# ====================|        FONCTIONS PRIVEES       |===================== #
# =========================================================================== #

# Affiche la matrice représentative de la carte
# -----------------------------------------------------------------------------
def _afficher_matrice(carte):
    """ Procédure permettant l'affichage de la matrice de la carte. """

    print(f"Dimensions: {LARGEUR}*{HAUTEUR}  CASES: {CASE_L}*{CASE_H}  "
          f"Unite: {UNITE}\n" + CASE_L * 3 * "=")
    for ligne in carte:
        print(ligne)

    print(CASE_L * 3 * "=" + "\n")


# =========================================================================== #
# ==================|        FONCTIONS PUBLIQUES        |==================== #
# =========================================================================== #

# Initialisaton de la matrice
# -----------------------------------------------------------------------------
def creer_matrice_carte(densite):
    """ Initilise une matrice selon le nombre de cases en largeur*hauteur selon
    une densité (float). La densité [0:1] represente le nombre de 1 dans la
    matrice. Plus elle sera grande plus on aura de 1.
    La variation [0, 1] permet d'obtenir des couleurs variés pour les murs. """

    carte = [[0] * CASE_L for _ in range(CASE_H)]
    # Remplissage de la matrice
    # ---------------------------------------------------------------------
    # Mur du haut/bas
    for idx in range(CASE_L):
        carte[0][idx], carte[CASE_H - 1][idx] = 1, 1

    # Mur de gauche/droite
    for idy in range(1, CASE_H - 1):
        carte[idy][0], carte[idy][CASE_L - 1] = 1, 1

    case_n, case_m = CASE_L - 1, CASE_H - 1             # Nombre de cases vides
    nbr_elmts = trunc(densite * (case_n * case_m))       # n*m = Max d'éléments
    # Remplissage de la liste "l_indice" avec les indices (i, j)
    l_indice = [(i, j) for i in range(1, case_m) for j in range(1, case_n)]
    # Initialisation des valeurs de la carte aléatoirement

    for _ in range(nbr_elmts):
        elemt = choice(l_indice)
        carte[elemt[0]][elemt[1]] = 1
        l_indice.remove(elemt)

    for lig in range(CASE_H):
        carte[lig] = tuple(carte[lig])

    _afficher_matrice(carte)

    return tuple(carte)


# Crée une carte avec variation de couleurs
# -----------------------------------------------------------------------------
def varation(matrice):
    """ Fcontion créant une nouvelle matrice avec des couleurs variées. """

    carte = []
    for lig in range(CASE_H):
        carte += [list(matrice[lig])]

    for idy in range(CASE_H):
        for idx in range(CASE_L):
            if carte[idy][idx]:
                carte[idy][idx] = randint(1, NB_COUL - 1)

    _afficher_matrice(carte)

    return tuple(carte)


# Lit un fichier de matrice
# -----------------------------------------------------------------------------
def recuperer_fichier_matrice(nom):
    """ Fonction récupérant la matrice d'un fichier 'fichier'. """

    with open(nom, 'r') as fichier:
        taille = len(fichier.readline())
        carte = [[0] * taille for _ in range(taille)]
        fichier.seek(0)
        for lig in range(taille):
            ligne = fichier.readline()
            for col in range(taille):
                carte[lig][col] = ligne[col * 2]
                # Pas de 2 en raison des virgules

    return carte


# Creation tablea de cosinus/sinus
# -----------------------------------------------------------------------------
def cos_sin_tab():
    """ Fonction créant les tables des cosinus et sinus. """

    costab, sintab = deque(), deque()
    for deg in range(361):
        costab.append(cos(deg / RAD))
        sintab.append(sin(deg / RAD))

    return tuple(costab), tuple(sintab)


# Recupère les cordonnées d'une case
# -----------------------------------------------------------------------------
def indice_case(posx, posy, unite):
    """ Retourne les coordonnées d'une case selon la position/les unités. """

    return trunc(posx) // unite, trunc(posy) // unite
