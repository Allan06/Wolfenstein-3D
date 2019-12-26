# -*- coding: utf-8 -*

# _________________________WOLFENSTEIN 3D - ANNIMATION_________________________
# =============================================================================
# annimation.py
# Version 0.6 (21 Février 2019)
# PAJANY Allan
# 3ème Année - Licence Informatique - UTLN
# =============================================================================

""" Module contenant toutes les fonctions liés aux dessins et à l'annimation du
    monde et de la carte.
"""

from pygame import Surface, draw, transform, display, font, image
from pygame.locals import *
from raycasting import *

# =========================================================================== #
# ====================|            CONSTANTES          |===================== #
# =========================================================================== #

# Initialisation de la fenetre
# -----------------------------------------------------------------------------
SET_MODE = display.set_mode
FENETRE = SET_MODE((LARGEUR, HAUTEUR), HWSURFACE | DOUBLEBUF)
display.set_caption("WOLFENSTEIN 3D")
display.set_icon(image.load("./Images/wolf.png"))        # Icones de la fenêtre

# Initialisation de la police et de la position d'affichage
# -----------------------------------------------------------------------------
font.init()
_PTAILLE = 14
_POLICE = font.SysFont("rockwell", _PTAILLE)

# Dimensions de la mini map
# -----------------------------------------------------------------------------
_COEF = 0.25 / 5                              # Rapport de taille de la minimap
UNITE_C = trunc(UNITE * _COEF + 0.05)          # Taille d'une case de la minmap
# Largeur/hauteur de la mini map
MINIMAP_L, MINIMAP_H = CASE_L * UNITE_C, CASE_H * UNITE_C

# Position en x des textes concernant les informations et les aides
# -----------------------------------------------------------------------------
_XINF1 = trunc(WINDOW_L * _COEF)
_XINF2, _XINF3 = _XINF1 + 130, _XINF1 + 220
_XINF4, _XINF5, _XINF6 = _XINF1 + 280, _XINF1 + 420, _XINF1 + 580

# Variables de dessins globales
# -----------------------------------------------------------------------------
FILL, BLIT, _RENDER = FENETRE.fill, FENETRE.blit, _POLICE.render
_SCALE, _FLIP = transform.scale, transform.flip
_LINE, _CIRCLE = draw.line, draw.circle

# Tableau des ordonnées
_ORD = tuple([_PTAILLE * i for i in range(2, 8)])


# =========================================================================== #
# ====================|        FONCTIONS PRIVEES       |===================== #
# =========================================================================== #

# Coloration d'une case
# -----------------------------------------------------------------------------
def _colorer_case(posx, posy, unite, couleur):
    """ Colore une case à la position (posx, posy) de taille unite. """

    FILL(couleur, (posx * unite, posy * unite, unite, unite))


# Creation de la grille
# -----------------------------------------------------------------------------
def _dessiner_grille(unite, largeur, hauteur, couleur=(90, 90, 70)):
    """ Crée une grille largeur * hauteur avec des cases de taille "unite". """

    # Lignes
    for lig in range(CASE_H + 1):
        FILL(couleur, (0, lig * unite, largeur, 1))

    # Colonnes
    for col in range(CASE_L + 1):
        FILL(couleur, (col * unite, 0, 1, hauteur))


# Dessine les éléments sur la minimap
# -----------------------------------------------------------------------------
def _placer_element(posx, posy, taille, couleur):
    """ Représenter graphiquement un élément à une position (posx, posy). """

    _CIRCLE(FENETRE, couleur, (posx, posy), taille)


# Dessine les rayons
# -----------------------------------------------------------------------------
def _dessin_rayons(posx, posy, l_inter, couleur):
    """ Dessine les rayons partant du joueur aux intersections de l_inter. """

    for inter in l_inter:
        _LINE(FENETRE, couleur, (posx, posy), (inter[0], inter[1]))


# Dessine la carte
# -----------------------------------------------------------------------------
def _dessiner_carte(unite, largeur, hauteur, carte, couleur=(80, 80, 80)):
    """ Creation de la carte selon ses dimensions et le nombre d'unités. """

    # _dessiner_grille(unite, largeur, hauteur)
    for idy in range(CASE_H):
        for idx in range(CASE_L):
            if carte[idy][idx]:
                _colorer_case(idx, idy, unite, couleur)


# Création des reflets des textures (expérimentale)
# -----------------------------------------------------------------------------
def _reflets_murs(posx, posy, h_mur, couleur, res):
    """ Crée des reflets murales au sol selon la position, hauteur du mur. """

    # Création d'une surface noire transparente pour améliorer l'effet
    surf_noir = creer_surface(res, h_mur)
    surf_noir.fill((0, 0, 0, 150))
    FILL(couleur, (posx, posy + 1, res, h_mur))
    # Assombrissement de la surface
    BLIT(surf_noir, (posx, posy + 1))


# Création des reflets des textures (expérimentale)
# -----------------------------------------------------------------------------
def _reflets_murs_texture(surface, posx, posy, h_mur, res):
    """ Créee des reflets des textures murales au sol.
    En paramètres, la surface à refleter, sa position et sa hauteur. """

    # Création d'une surface noire transparente pour améliorer l'effet
    surf_noir = creer_surface(res, h_mur)
    surf_noir.fill((0, 0, 0, 230))
    # Rotation de la colonne de texture de 180° et collage de la colonne du mur
    BLIT(_FLIP(surface, 0, 1), (posx, posy + 1))
    # Assombrissement de la surface
    BLIT(surf_noir, (posx, posy + 1))


# =========================================================================== #
# ==================|        FONCTIONS PUBLIQUES        |==================== #
# =========================================================================== #

# Affiche les informations du joueurs
# -----------------------------------------------------------------------------
def afficher_informations(x, y, angle, vision, v_angle, v_depl, fps, tps, mode,
                          aff_carte, variation, ombre, reflet, texture, mvmts,
                          musique, coul_mur, res, couleur=(255, 255, 255)):
    """ Procédure permettant l'affichage des informations du joueur et du jeu :
    Coordonnées, la carte, le fps, le temps, les paramètres des rendus... """

    # Informations du jeu
    # -------------------------------------------------------------------------
    # Position
    BLIT(_RENDER(f"Position: x: {x}  y: {y}", 1, couleur), (_XINF1, 0))
    # Angle
    BLIT(_RENDER(f"Angle: {angle}°", 1, couleur), (_XINF1, _PTAILLE))
    # Taille de la fenetre
    BLIT(_RENDER(f"Unite/cases: {UNITE} {CASE_L}*{CASE_H}", 1, couleur),
         (_XINF1, _ORD[0]))
    # Résolution
    BLIT(_RENDER(f"Pixel: {LARGEUR}*{HAUTEUR}", 1, couleur), (_XINF1, _ORD[1]))
    BLIT(_RENDER(f"Résolution: {res}", 1, couleur), (_XINF1, _ORD[2]))
    # Champ de vision
    BLIT(_RENDER(f"Ch. visuel: {vision}°", 1, couleur), (_XINF2, 0))
    # Vitesse de rotation
    BLIT(_RENDER(f"Vit. rot: {v_angle}", 1, couleur), (_XINF2, _PTAILLE))
    # Vitesse de déplacement
    BLIT(_RENDER(f"Vit. depl: {v_depl}", 1, couleur), (_XINF2, _ORD[0]))
    # Images par seconde
    BLIT(_RENDER(f"FPS: {trunc(fps)}", 1, couleur), (_XINF3, 0))
    # Temps
    BLIT(_RENDER(f"Tps: {tps}s", 1, couleur), (_XINF3, _PTAILLE))

    # Aides touches
    # -------------------------------------------------------------------------
    # Mode carte/jeu
    BLIT(_RENDER("F1: 3D" if mode else "F1: Carte", 1, couleur), (_XINF4, 0))
    # Affichage ou non des informations
    BLIT(_RENDER("F2: Affiche/cache infos", 1, couleur), (_XINF4, _PTAILLE))
    # Affichage de la minimap
    BLIT(_RENDER("F3: Affiche carte = ON" if aff_carte else
                 "F3: Affiche carte = OFF", 1, couleur), (_XINF4, _ORD[0]))
    # Variation des couleurs
    BLIT(_RENDER("F4: Couleurs diff. = ON" if variation else
                 "F4: Couleurs diff. = OFF", 1, couleur), (_XINF4, _ORD[1]))
    # Activation de l'ombrage expérimental
    BLIT(_RENDER("F5: Ombres = ON" if ombre else
                 "F5: Ombres = OFF", 1, couleur), (_XINF4, _ORD[2]))
    # Activation des reflets
    BLIT(_RENDER("F6: Reflets = ON" if reflet else
                 "F6: Reflets = OFF", 1, couleur), (_XINF4, _ORD[3]))
    # Activation des textures
    BLIT(_RENDER("F7: Texture = ON" if texture else
                 "F7: Texture = OFF", 1, couleur), (_XINF4, _ORD[4]))
    # Activation des mouvements de déplacement
    BLIT(_RENDER("F8: Mouvements = ON" if mvmts else
                 "F8: Mouvements = OFF", 1, couleur), (_XINF4, _ORD[5]))
    # Variation de la vitesse de rotation
    BLIT(_RENDER("4/6: Aug/dim vit. rotation", 1, couleur), (_XINF5, 0))
    # Variation de la vitesse de déplacement
    BLIT(_RENDER("+/-: Aug/dim vit. depl.", 1, couleur), (_XINF5, _PTAILLE))
    # Variation du champ de vision
    BLIT(_RENDER("8/2: Aug/dim ch. visuel", 1, couleur), (_XINF5, _ORD[0]))
    # Tirer
    BLIT(_RENDER("5: Tirer", 1, couleur), (_XINF5, _ORD[1]))
    # Musique suiante
    BLIT(_RENDER("n: Musique suiv.", 1, couleur), (_XINF5, _ORD[2]))
    # Mettre la musique en paue
    BLIT(_RENDER("Espace: Musique = Lecture" if musique else
                 "Espace: Musique = Pause", 1, couleur), (_XINF5, _ORD[3]))
    # Plein écran
    BLIT(_RENDER("f: Plein écran", 1, couleur), (_XINF5, _ORD[4]))
    # Prendre capture d'écran
    BLIT(_RENDER("s: Capture d'écran", 1, couleur), (_XINF5, _ORD[5]))
    # Modifier les ouleurs RGB des murs (uniforme)
    if not variation:
        BLIT(_RENDER("Couleur mur", 1, couleur), (_XINF6, 0))
        BLIT(_RENDER(f"     r: {coul_mur[0]}", 1, couleur), (_XINF6, _PTAILLE))
        BLIT(_RENDER(f"     g: {coul_mur[1]}", 1, couleur), (_XINF6,  _ORD[0]))
        BLIT(_RENDER(f"     b: {coul_mur[2]}", 1, couleur), (_XINF6,  _ORD[1]))


# Génération de couleur
# -----------------------------------------------------------------------------
def generer_couleur():
    """ Génère aléatoirement une couleur de type RGB. """

    return randint(0, 255), randint(0, 255), randint(0, 255)


# Genère liste et dictionnaire de texture/couleurs
# -----------------------------------------------------------------------------
def generer_couleurs_textures(liste_img):
    """ Fonction génerant un dictionnaire de couleurs aléatoire ainsi qu'une
    une liste d'image chargés à partir de la liste_img. """

    liste_texture_mur, dict_coul_mur = deque(), {}
    for ind in range(NB_COUL):
        dict_coul_mur[ind + 1] = generer_couleur()
        liste_texture_mur.append(image.load(liste_img[ind]).convert_alpha())

    return tuple(liste_texture_mur), dict_coul_mur


# Création surface minimap
# -----------------------------------------------------------------------------
def creer_surface(largeur, hauteur):
    """ Crée une surface (largeur * hauteur) pour l'insertion de la carte. """

    surface = Surface((largeur, hauteur))

    # Permet d'utiliser la valeur alpha [0, 255] pour la transparence
    return surface.convert_alpha(surface)


# Création de la minmap selon sa position, celui du joueur
# -----------------------------------------------------------------------------
def creer_map(posx, posy, angle, champ_vision, col_pixel, carte, unite,
              largeur, hauteur, j_taille, couleur, res):
    """ Procédure permettant la création de la minimap en superposition.
    posx, posy, angle : Coordonnées du joueur.
    champ de vision, carte : Valeur du champ de vision, matrice. """

    # Projection des coordonnées du joueur dans la minimap
    posx, posy = projection(posx, posy, largeur, hauteur)
    # Placement du joeur dans la minimap
    _placer_element(posx, posy, j_taille, (255, 0, 0))
    # Création de la liste des intersections
    l_inter = lancer_rayon(posx, posy, angle, champ_vision, col_pixel, unite,
                           largeur, carte, res)
    _dessin_rayons(posx, posy, l_inter, couleur)             # Rendu des rayons
    # Création des la grille et coloration des cases
    _dessiner_carte(unite, largeur, hauteur, carte)


# Création de murs de couleurs
# -----------------------------------------------------------------------------
def dessin_murs(posx, posy, h_mur, couleur, reflet, res):
    """ Créer des murs en (posx, posy) selon sa hauteur. """

    FILL(couleur, (posx, posy, res, h_mur))
    if reflet:
        _reflets_murs(posx, posy + h_mur, h_mur, couleur, res)


# Dessine le sol et le plafond
# -----------------------------------------------------------------------------
def dessin_sol_plafond(posx, yplf, ysol, couleur_plaf, couleur_sol, res):
    """ Dessinne le sol et le plafond avec des lignes à partir de la position x
    d'un mur et yplf/ysol ordonnées haut/bas de ce mur (plafond/sol). """

    # Dessine le plafond + délimiteur bleu
    FILL(couleur_plaf, (posx, 0, res, yplf))
    FILL(1023, (posx, yplf - 1, res, 1))

    # Dessine le sol + délimiteur rouge
    FILL(couleur_sol, (posx, ysol, res, HAUTEUR))
    FILL(2146435072, (posx, ysol, res, 1))


# Dessine les textures des murs (experimentale optimisée)
# -----------------------------------------------------------------------------
def dessin_texture_murs(posx, posy, h_mur, h_img, mur, x_img, coef, ombre,
                        reflet, res):
    """ Procédure expérimentale permettant de dessiner les textures des murs.
    posx, posy = Colonne du pixel, ordonné du point de départ du mur.
    h_mur, x_img = Hauteur du mur, abcisse de la case touchée par le rayon.
    h_img, mur = Taille de l'image chargé, image du mur chargé.
    coef = [0:1] coefficient d'ombrage
    ombre, reflet = [0, 1] active/désactive les ombrages, reflets. """

    # Récupère l'abcisse de la colonne de pixel de l'image en prenant la valeur
    # tronqué de l'abcisse du mur (x_mur) et la multipliant par la largeur de
    # l'image (l_img). On rogne l'image pour récupérer la colonne de surface.
    # Redimensionnement de la hauteur de l'image rogné à la hauteur du mur

    surface = _SCALE(mur.subsurface((trunc(x_img), 0, 1, h_img)), (res, h_mur))
    BLIT(surface, (posx, posy))
    # Création des reflets des murs au sol
    if reflet:
        _reflets_murs_texture(surface, posx, posy + h_mur, h_mur, res)

    # Création des ombrage
    if ombre:
        surf_noir = creer_surface(res, h_mur * 2 if reflet else h_mur)
        # Rendus noir transparent pour l'ombrage
        surf_noir.fill((0, 0, 0, 255 - 255 * coef))
        BLIT(surf_noir, (posx, posy))


# Dessine les textures des murs (experimentale optimisée)
# -----------------------------------------------------------------------------
def dessin_sol(posx, posy, colp, ybas, l_img, h_img, mur, res, angle, x, y, d,
               angle_ray):
    """ Procédure expérimentale permettant de dessiner les textures des murs.
    posx, posy = Colonne du pixel, ordonné du point de départ du mur.
    h_mur, x_img = Hauteur du mur, abcisse de la case touchée par le rayon.
    h_img, mur = Taille de l'image chargé, image du mur chargé.
    coef = [0:1] coefficient d'ombrage
    ombre = [0, 1] active/désactive les ombrages
    reflet = [0, 1] active/désactive les reflets. """

    for i in range(HAUTEUR // 2, HAUTEUR, res):

        rx = trunc(posx + d * cos(angle_ray))
        ry = trunc(posy + d * sin(angle_ray))
        fx = rx % l_img
        fy = ry % h_img
        surface = _SCALE(mur.subsurface(fx, fy, l_img - fx, h_img - fy), (LARGEUR, res))
        BLIT(surface, (colp, ybas))


