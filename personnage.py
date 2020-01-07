# -*- coding: utf-8 -*

# ________________________WOLFENSTEIN 3D - PERSONNAGE__________________________
# =============================================================================
# personnage.py
# Version 0.2 (29 Décembre 2018)
# PAJANY Allan
# 3ème Année - Licence Informatique - UTLN
# =============================================================================

""" Module regroupant les fonctions permettant le placement et déplacement du
    joueur.
"""

from carte import *

# Tableaux des cosinus et sinus
_COSTAB, _SINTAB = cos_sin_tab()


# ==========================================================================- #
# ===================|        FONCTIONS PRIVEES       |====================== #
# =========================================================================== #

# Recherche de cases libres
# -----------------------------------------------------------------------------
def _libre(carte):
    """ Recherche des cases libre dans la carte. """

    cases_libres = deque()
    c_app = cases_libres.append
    for idx in range(UNITE + (UNITE // 2), (LARGEUR - UNITE), UNITE):
        for idy in range(UNITE + (UNITE // 2), (HAUTEUR - UNITE), UNITE):
            if not carte[idy // UNITE][idx // UNITE]:
                c_app((idx, idy))

    return cases_libres


# =========================================================================== #
# ==================|        FONCTIONS PUBLIQUES        |==================== #
# =========================================================================== #

# Représentation du joeur
# -----------------------------------------------------------------------------
def init_joueur(carte):
    """ Retourne des coordonnées aléatoires du joueur, position et angle. """

    posx, posy = choice(_libre(carte))

    return posx, posy, randint(0, 360)


# Fonction déplaçant le joueur
# -----------------------------------------------------------------------------
def deplacement(posx, posy, angle, pas, carte, sens):
    """ Fonction permettant le déplacement du joueur (x, y) selon son angle
    d'orientation avec un pas caractérisant la vitesse. 'sens' sert à indiquer
    le sens de déplacement : 1 avant et -1 arrière. """

    # Calcul du prochain déplacemnt
    x_tmp = posx + trunc(_COSTAB[angle] * pas) // sens
    y_tmp = posy - trunc(_SINTAB[angle] * pas) // sens
    # Récupération des indices
    idx, idy = indice_case(x_tmp, y_tmp, UNITE)

    # Vérifie la possibilité de déplacement en (x, y). Gère les colisions avec
    # les murs, (x, y) prendront leur valeurs finales (x_tmp, y_tmp) que si ces
    # derniers ne sont pas dans des murs. Permet aussi de glisser sur les murs.
    if not carte[posy // UNITE][idx]:
        posx = x_tmp

    if not carte[idy][posx // UNITE]:
        posy = y_tmp

    return posx, posy


# Rotation à droite ou à gauche
# -----------------------------------------------------------------------------
def rotation(angle, pas):
    """ Retourne un angle de rotation d'un pas égale à la vitesse. """

    return (angle + pas) % 360
