#!/usr/bin/env python3
# -*- coding: utf-8 -*

# __________________________WOLFENSTEIN 3D - MAIN______________________________
# =============================================================================
# main.py
# Version 0.7 (21 Février 2019)
# PAJANY Allan
# 3ème Annee - License Informatique - UTLN
# =============================================================================

""" Module principale du lancement du jeu. """

from datetime import datetime
from pygame import mixer, event, key, time
from annimation import *


# Mise à jour champ vision et résolution
# -----------------------------------------------------------------------------
def mise_a_jour(chvision, res, modif=0):
    """ Met à jour champ vision et résolution lors des modifications. """

    if modif:
        return chvision / RAD / LARGEUR * res, chvision / RAD / MINIMAP_L * res

    return (chvision / RAD / LARGEUR * res, chvision / RAD / MINIMAP_L * res,
            chvision / RAD)


# =========================================================================== #
# ==================|       FONCTION PRINCIPALE        |===================== #
# =========================================================================== #
def jeu(densite, ch_vision, mode, affiche_infos, affiche_carte, varie, ombre,
        reflet, texture, mvmt, res, plein_ecr):
    """ Fonction finale parmettant le lancement du jeu.
    ch_vision [1:180] : Entier représentant la valeur du champ de vision
    mode [0, 1] : Basculement mode carte/terrain de jeu
    affiche_infos/carte [0, 1] : Affiche/cache les informations du jeu/minimap
    ombre, reflet, texture, mvmt [0, 1] : Active/desactive les effets d'ombre,
    reflets, textures et mouvements lors du déplacement. """

    global FENETRE

    # Liste des noms des textures à charger
    liste_img = tuple([f"./Images/m{i}.png" for i in range(1, NB_COUL + 1)])
    coulrayons = generer_couleur()              # Couleurs aléatoire des rayons
    # Dictionnaire/liste de couleurs/textures pour les murs. Variation de 9
    texture_mur, coulmur = generer_couleurs_textures(liste_img)

    # Couleur/texture du mur par défaut
    mur, murc = texture_mur[randint(0, NB_COUL - 1)], coulmur[1]
    limg, himg = mur.get_width(), mur.get_height()
    dict_rgb = {"r": 0, "g": 1, "b": 2}

    # Chargement de l'image d'une arme, d'un coup de feu et redimenssionnement
    arme = image.load("./Images/Arme.png")
    feu = transform.scale(image.load("./Images/Feu.png"), (60, 60))
    h_arme, x_arme = HAUTEUR - 320, CENTRE_L - 100

    # Initialisation de la musique et du son du coup de feu
    mixer.init()
    son = mixer.Sound("./Musiques/son_arme.wav")
    mixer.music.load("./Musiques/chanson1.ogg")
    mixer.music.set_volume(0.01)
    # mixer.music.play(-1)                                 # Répetition infinie
    musique, piste = 1, 1            # [0, 1] Pause/lecture, numero de la piste

    # Initialisation de la variable qui récupèrera le nombre de fps
    ips = time.Clock()
    fps = ips.tick

    # Initialisation de la matrice et de la minimap
    # -------------------------------------------------------------------------
    mini_map = creer_surface(MINIMAP_L, MINIMAP_H)   # Création surface minimap
    mini_map.fill((255, 255, 255, 140))
    carte = creer_matrice_carte(densite)        # Création matrice carte

    # Initialisation des paramètres de lancé de rayon
    # -------------------------------------------------------------------------
    # Colonne de pixel du terrain de jeu et de la minimap
    colpix_t, colpix_c, ch_vision_r = mise_a_jour(ch_vision, res)
    tan_ch_vision = tan(ch_vision_r / 2)
    # Centre, distance max pour les effets d'ombre. /nbr augmente son intensité
    centre, dist_max = HAUTEUR // 2, hypot(LARGEUR - 0, HAUTEUR - 0) / 3

    # Informations joueur
    # -------------------------------------------------------------------------
    jox, joy, angle = init_joueur(carte)
    v_depl, v_rot = 5, 5

    # Gestion des mouvements lorsque l'on se déplace
    # -------------------------------------------------------------------------
    mouv, taille = 0, 22        # mouv pacours le tableau de mouvements suivant
    # Tableau de variation des mouvements parcourus lors du déplacement
    l_mouvement = tuple([centre + i for i in range(0, taille, 2)] +
                        [centre + taille - i for i in range(0, taille, 2)])

    # Tableau gérant les touches clavier hors de la boucle d'évènement. Fluide.
    touche = 324 * [0]
    # Durée du délais avant appuie et de l'intervalle de répétition
    key.set_repeat(200, 10)
    # Appelé lorsqu'une touche sera préssée pour récupérer la touche
    kpresse = key.get_pressed()
    # ======================================================================= #
    # ================|          BOUCLE PRINCIPALE        |================== #
    # ======================================================================= #
    while 1:
        angle_r = angle / RAD
        # Mode carte normale
        # ---------------------------------------------------------------------
        if mode:
            FILL(-1)
            # Création carte normale
            creer_map(jox, joy, angle_r, ch_vision_r, colpix_t, carte, U_CARTE,
                      LARGEUR, HAUTEUR, 3, coulrayons, res)

        # Mode terrain de jeu
        # ---------------------------------------------------------------------
        else:
            FILL(-1)
            # Création de la liste des intersections
            liste_inter = lancer_rayon(jox, joy, angle_r, ch_vision_r,
                                       colpix_t, UNITE, LARGEUR, carte, res)
            col = 0  # Numero de la colonne de pixel
            for ray in liste_inter:
                # Correction du "fish eyes"²
                distance_mur = ray[2] * cos(angle_r - ray[3])
                # Calcul de la hauteur du mur et condition de dépassement
                hmur = trunc(hauteur_mur(distance_mur, tan_ch_vision))
                yinf = centre + hmur * 0.5
                ysup = yinf - 2 * hmur * 0.5
                # hmur = hmur + (yinf - (ysup + hmur))
                # Coefficient d'ombre, float [0:1] selon la distance maximale
                # et la distance du rayon actuelle ray[2]
                coef = (1 - ray[2] / dist_max if ray[2] < dist_max else 0) if\
                    ombre else 1
                # Création du sol, plafond
                dessin_sol_plafond(col, ysup, yinf, (100 * coef, 100 * coef,
                                                     100 * coef), 0, res)
                # dessin_sol(jox, joy, col, yinf, limg,
                # himg, mur, res, angle_r, ray[0], ray[1],ray[2], ray[3])
                # Dessin des textures des murs
                # -------------------------------------------------------------
                if texture:
                    if varie:
                        # Récupération de la valeur de la case (indy, indx)
                        indx, indy = indice_case(ray[0], ray[1], UNITE)
                        # Choix de l'image correspondant (aléatoirement)
                        mur = texture_mur[carte[indy][indx]]
                        limg, himg = mur.get_width(), mur.get_height()
                        dessin_texture_murs(col, ysup, hmur, himg, mur,
                                            ray[4] * limg, coef, ombre,
                                            reflet, res)

                    else:
                        dessin_texture_murs(col, ysup, hmur, himg, mur,
                                            ray[4] * limg, coef, ombre,
                                            reflet, res)

                # Dessin des murs sans textures
                # -------------------------------------------------------------
                else:
                    # Couleurs variés
                    if varie:
                        # Récupération de l'indice du murs dans le tableau
                        indx, indy = indice_case(ray[0], ray[1], UNITE)
                        # Récupération de la couleur dans le dictionnaire
                        coul = coulmur[carte[indy][indx]]
                        dessin_murs(col, ysup, hmur, (coul[0] * coef,
                                                      coul[1] * coef,
                                                      coul[2] * coef), reflet,
                                    res)

                    # Couleurs unique, première couleur du dictonnaire
                    else:
                        dessin_murs(col, ysup, hmur, (murc[0] * coef,
                                                      murc[1] * coef,
                                                      murc[2] * coef), reflet,
                                    res)

                    # Colore les bordures en noir avec épaisseur = 2. 0 = haut
                    # de l'écran pour l'ombre et hauteur du mur sans ombre.
                    if ray[5]:
                        FILL(0, (col, 0 if ombre else ysup, 2,
                                 ysup if ombre else hmur))

                col += res

            # Affichage de la minimap
            # -----------------------------------------------------------------
            if affiche_carte:
                # Initialisation de la surface de la minimap
                BLIT(mini_map, (0, 0))
                creer_map(jox, joy, angle_r, ch_vision_r, colpix_c, carte,
                          UNITE_C, MINIMAP_L, MINIMAP_H, 1, coulrayons, res)

            # Affichae d'une arme (-mouv pour le mouvement de l'arme)
            BLIT(arme, (x_arme, h_arme - mouv))

        # ------------------------------------------------------------------- #
        # --------------------|       MOUVEMENTS      |---------------------- #
        # ------------------------------------------------------------------- #
        # Avancer/reculer
        # ---------------------------------------------------------------------
        if touche[K_UP]:
            jox, joy = deplacement(jox, joy, angle, v_depl, carte, 1)
            # Mouvements du joeur
            if mvmt:
                centre = l_mouvement[mouv]
                mouv = (mouv + 1) % taille

        if touche[K_DOWN]:
            jox, joy = deplacement(jox, joy, angle, v_depl, carte, -1)
            if mvmt:
                centre = l_mouvement[mouv]
                mouv = (mouv + 1) % taille

        # Rotation droite/gauche
        # ---------------------------------------------------------------------
        if touche[K_LEFT]:
            angle = rotation(angle, v_rot)

        if touche[K_RIGHT]:
            angle = rotation(angle, -v_rot)

        fps(0)                      # Mise à jour de l'horloge comptant les fps
        # Affichage de toutes les informations après mise à jour
        if affiche_infos:
            afficher_informations(jox, joy, angle, ch_vision, v_rot, v_depl,
                                  ips.get_fps(), time.get_ticks() // 1000,
                                  mode, affiche_carte, varie, ombre, reflet,
                                  texture,  mvmt, musique, murc, res)

        # ------------------------------------------------------------------- #
        # --------------|       GESTION DES EVENEMENTS      |---------------- #
        # ------------------------------------------------------------------- #
        for evt in event.get():
            if evt.type is QUIT:
                quit()

            elif evt.type is KEYDOWN:
                # ----------------------------------------------------------- #
                # ---------------|       MODIFICATIONS      |---------------- #
                # ----------------------------------------------------------- #
                touche[evt.key] = 1                # Active la touche si appuie
                # Modification de la vitesse de déplacement
                # -------------------------------------------------------------
                if kpresse[K_KP_PLUS] or evt.key == K_KP_PLUS:
                    v_depl += 1

                elif kpresse[K_KP_MINUS] or evt.key == K_KP_MINUS:
                    if v_depl > 0:
                        v_depl -= 1

                # Modification de la valeur du champ de vision
                # -------------------------------------------------------------
                elif kpresse[K_KP2] or evt.key == K_KP2:
                    ch_vision = ch_vision - 1 if ch_vision > 1 else 1
                    colpix_t, colpix_c, ch_vision_r = mise_a_jour(ch_vision,
                                                                  res)
                    tan_ch_vision = tan(ch_vision_r / 2)

                elif kpresse[K_KP8] or evt.key == K_KP8:
                    ch_vision = ch_vision + 1 if ch_vision < 180 else 180
                    colpix_t, colpix_c, ch_vision_r = mise_a_jour(ch_vision,
                                                                  res)
                    tan_ch_vision = tan(ch_vision_r / 2)

                # Modification de la résolution
                # -------------------------------------------------------------
                elif kpresse[K_KP3] or evt.key == K_KP3:
                    res = res - 1 if res > 1 else 1
                    colpix_t, colpix_c = mise_a_jour(ch_vision, res, 1)

                elif kpresse[K_KP9] or evt.key == K_KP9:
                    res = res + 1 if res < LARGEUR else LARGEUR
                    colpix_t, colpix_c = mise_a_jour(ch_vision, res, 1)

                # Modification de la vitesse de rotation
                # -------------------------------------------------------------
                elif kpresse[K_KP4] or evt.key == K_KP4:
                    v_rot -= 1 if v_rot > 0 else v_rot

                elif kpresse[K_KP6] or evt.key == K_KP6:
                    v_rot += 1

                # Coup de feu
                elif evt.key == K_KP5:
                    BLIT(feu, (CENTRE_L - 10, HAUTEUR - 160))
                    son.play()

                # Plein écran
                elif evt.key == K_f:
                    plein_ecr = not plein_ecr
                    if plein_ecr:
                        FENETRE = SET_MODE((LARGEUR, HAUTEUR), FULLSCREEN |
                                           HWSURFACE | DOUBLEBUF)
                    else:
                        FENETRE = SET_MODE((LARGEUR, HAUTEUR),
                                           HWSURFACE | DOUBLEBUF)

                # Captures d'écran
                elif evt.key == K_s:
                    date = f"{datetime.now()}".replace(':', '.')
                    image.save(FENETRE, f"./Captures/{date}.bmp")

                # Modifiaction couleurs murs
                elif chr(evt.key) in dict_rgb:
                    murc_tmp = list(murc)
                    murc_tmp[dict_rgb[chr(evt.key)]] =\
                        (murc_tmp[dict_rgb[chr(evt.key)]] + 1) % 255
                    murc = tuple(murc_tmp)

                # ----------------------------------------------------------- #
                # ---------------|        AFFICHAGE        |----------------- #
                # ----------------------------------------------------------- #
                # Passer de la minimap au terrain et inversement
                elif evt.key == K_F1:
                    mode = not mode

                # Affichage ou non des informations
                elif evt.key == K_F2:
                    affiche_infos = not affiche_infos

                # Affichage ou non de la minimap
                elif evt.key == K_F3:
                    affiche_carte = not affiche_carte

                # Activation ou non des variations de couleurs
                elif evt.key == K_F4:
                    varie = not varie
                    # Création d'une nouvelle map selon la variation
                    carte = varation(carte)

                # Activation ou non de l'ombre
                elif evt.key == K_F5:
                    ombre = not ombre

                # Activation ou non des reflets
                elif evt.key == K_F6:
                    reflet = not reflet

                # Activation ou non des textures
                elif evt.key == K_F7:
                    texture = not texture
                    mur = choice(texture_mur)
                    limg, himg = mur.get_width(), mur.get_height()
                    coulrayons, murc = generer_couleur(), generer_couleur()

                # Activation ou non des mouvemets
                elif evt.key == K_F8:
                    mvmt = not mvmt

                # Pause/lecture musique
                elif evt.key == K_SPACE:
                    musique = not musique
                    # Reprise lecture
                    if musique:
                        mixer.music.unpause()

                    else:
                        mixer.music.pause()

                # Musique suivante
                elif evt.key == K_n:
                    # Arrêt de la musique actuelle
                    if musique:
                        mixer.music.stop()
                        piste = (piste + 1) % 3
                        # Chargement de la prochaine musique et leccture
                        mixer.music.load(f"./Musiques/chanson{piste}.ogg")
                        mixer.music.play(-1)

                elif evt.key == K_ESCAPE:
                    quit()

            elif evt.type is KEYUP:
                touche[evt.key] = 0        # Désactive la touche au relachement

        display.flip()                             # Mise à jour de l'affichage


# =========================================================================== #
# ====================|          TEST UNITAIRE        |====================== #
# =========================================================================== #
if __name__ == '__main__':

    jeu(0.20, 70, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0)
