# -*- coding: utf-8 -*

# ________________________WOLFENSTEIN 3D - RAYCASTING__________________________
# =============================================================================
# raycasting.py
# Version 0.8 (21 Février 2019)
# PAJANY Allan
# 3ème Année - Licence Informatique - UTLN
# =============================================================================

""" Module disposant des fonctions pour la création du moteur définissant le
    raycasting, le calcul d'intersections, lancer de rayons...
"""

from threading import Thread
from math import tan, hypot
from personnage import *

CENTRE_L = LARGEUR // 2                                     # Milieu du terrain


class Ray(Thread):

    def __init__(self, p_inter, p_id, p_unite, p_angle, p_carte):
        Thread.__init__(self)
        self.x_inter = p_inter[0]
        self.y_inter = p_inter[1]
        self.angle = p_angle
        self.unite = p_unite[0]
        self.utmp = p_unite[1]
        self.id_x = p_id[0]
        self.id_y = p_id[1]
        self.carte = p_carte

    def run(self):
        while 0 < self.id_x < CASE_L and 0 < self.id_y < CASE_H and not self.carte[self.id_y][self.id_x]:
            self.x_inter += self.utmp
            self.y_inter += self.utmp * tan(-self.angle)
            self.id_x, self.id_y = indice_case(self.x_inter, self.y_inter, self.unite)

    def get_intersection(self):
        return self.x_inter, self.y_inter


# =========================================================================== #
# ====================|        FONCTIONS PRIVEES       |===================== #
# =========================================================================== #

# Calul des intersections horizontales
# -----------------------------------------------------------------------------
def _intersection_horizontale(posx, posy, angle, unite):
    """ Fonction retournant la première intersection horizontale. """

    # Premier et deuxième quadrant
    if angle < 3.1415926535897:
        yhor = (posy // unite * unite) - 0.0000000001
        # -0.0001 évite que le rayon traverse les murs, les irrégularités entre
        # blocs, colonne de pixels ressortant du passage d'un bloc à un autre.

    # Troisième et quatrième quadrant
    else:
        yhor = (posy // unite * unite) + unite

    # J'ajoute une petite valeur à la tangente pour éviter la division par 0
    return posx + (posy - yhor) / (tan(angle) + 0.000001), yhor


# Calul des intersections verticales
# -----------------------------------------------------------------------------
def _intersection_verticale(posx, posy, angle, unite):
    """ Fonction retournant la première intersection verticale. """

    # Deuxième et troisième quadrant
    if 1.57079632679489 < angle < 4.71238898038469:
        xver = (posx // unite * unite) - 0.0000000001

    # Premier et quatrième quadrant
    else:
        xver = (posx // unite * unite) + unite

    return xver, posy + (posx - xver) * tan(angle)


# =========================================================================== #
# ==================|        FONCTIONS PUBLIQUES        |==================== #
# =========================================================================== #

# Projection d'un point d'une window vers viewport
# -----------------------------------------------------------------------------
def projection(posx, posy, dvx, dvy):
    """ Projete un point pos de l'espace window dans la viewport. """

    return posx * dvx // WINDOW_L, posy * dvy // WINDOW_H


# Calcul la hauteur d'un mur
# -----------------------------------------------------------------------------
def hauteur_mur(dist_mur, champ_vision):
    """ Calcule la hauteur d'un mur selon la distance joueur/mur. """

    return UNITE / dist_mur * CENTRE_L / champ_vision


# Dimensions perçues du sprite
# -----------------------------------------------------------------------------
def dimensions_sprite(sprite, dist_mur, dist_virt):
    """ Fonction retournant la dimension perçues des sprites selon ses
    dimensions réelles, la distance du mur et la distance virutelle. """

    return sprite[0] * dist_virt / dist_mur, sprite[1] * dist_virt / dist_mur


# Retourne la liste des intersections avec les murs
# -----------------------------------------------------------------------------
def lancer_rayon(posx, posy, angle, champ_vision, col_pixel, unite, largeur,
                 carte, res):
    """ Retourne la liste des intersections avec les murs selon les coordonnées
    du joueur, son champ de vision, le nombre d'unité d'une case, la largeur et
    hauteur du terrain. col_pixel = taiile d'une colonne de pixel. """

    l_inter = deque()         # Création de la liste stockant les intersections
    l_app = l_inter.append
    angle = (angle + champ_vision / 2) % 6.2831853071795     # Départ du lancer
    for _ in range(0, largeur, res):

        # Intersection horizontale
        # ---------------------------------------------------------------------
        xhor, yhor = _intersection_horizontale(posx, posy, angle, unite)
        # utmp décrémente/incrémente (xhor, yhor) en fontion de l'angle
        utmp = -unite if angle < 3.1415926535897 else unite
        # Récupération des numéros de cases
        idx, idy = indice_case(xhor, yhor, unite)
        # Parcours la carte tant qu'on ne sort pas et qu'il n'y a pas de mur
        while 0 < idx < CASE_L and 0 < idy < CASE_H and not carte[idy][idx]:
            # Calcul de la prochaine intersection horizontale
            yhor += utmp
            xhor += utmp / (tan(-angle) + 0.000001)
            idx, idy = indice_case(xhor, yhor, unite)

        # Intersection verticale
        # ---------------------------------------------------------------------
        xver, yver = _intersection_verticale(posx, posy, angle, unite)
        utmp = -unite if 1.57079632679489 < angle < 4.71238898038469 else unite
        idx, idy = indice_case(xver, yver, unite)
        while 0 < idx < CASE_L and 0 < idy < CASE_H and not carte[idy][idx]:
            xver += utmp
            yver += utmp * tan(-angle)
            idx, idy = indice_case(xver, yver, unite)

        # Calcul de la distance horizontale et verticale joueur/mur
        dsth = hypot(xhor - posx, yhor - posy) + 1
        dstv = hypot(xver - posx, yver - posy) + 1
        # Recupération du point le plus proche du joueur
        if dsth < dstv:
            # (xhor|ver, yhor|ver, distance_mur, angle*, case intersecté
            #  xhor|yver**, verification du changement d'intersection***)
            l_app((xhor, yhor, dsth, angle, xhor / unite - xhor // unite,
                   1 if xhor % unite < 0.3 else 0))

        else:
            l_app((xver, yver, dstv, angle, yver / unite - yver // unite,
                   1 if yver % unite < 0.3 else 0))

        # Prochain angle. %2pi pour éviter les valeurs négatives
        angle = (angle - col_pixel) % 6.2831853071795
        # * L'angle est récupéré pour effectué la correction du fish eyes
        # ** On récupère la case intersectée pour obtenir par la suite la
        # position de la colonne de texture à afficher.
        # *** Je vérifie si on a changé d'intersection, si la variable de
        # vérification est à 1 cela implique que l'on avait précédemment trouvé
        # une intersection inverse à celle actuelle. Cela permettra dans le
        # dessin des murs de créer les bordures.

    return l_inter
