#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pyxel

class Joueur:
    def __init__(self, x, y):
        # Position et dimensions du joueur
        self.x = x
        self.y = y
        self.largeur = 8
        self.hauteur = 8
        
        # Paramètres de mouvement
        self.vitesse = 1
        self.puissance_saut = 3
        self.gravite = 0.20
        self.vel_x = 0
        self.vel_y = 0
        """"""""""""""""""""""""""""""
        """ État du joueur """""""""""
        """"""""""""""""""""""""""""""
        self.grounded = True
        self.double_saut_dispo = True
        self.marche = False
        self.direction=-1 # 0 gauche    1 droite
        self.court=False
        self.cd_course=0
        self.court_max=False

        # états de l'air dash
        self.airdash_dispo=True
        self.jauge_airdash=0
        self.est_en_airdash=False

        # états du dash
        self.dash_dispo=True
        self.jauge_dash=0
        self.cd_dash=0
        self.est_en_dash=False
        """"""""""""""""""""""""""""""
        """"""""""""""""""""""""""""""
        """"""""""""""""""""""""""""""
    def update(self):
        self.gravite=0.2
        self.vitesse=1
        self.court=False
        self.court_max=False
        

        
        # Gestion des déplacements horizontaux
        if pyxel.btn(pyxel.KEY_Q):
            self.vel_x = -self.vitesse
            self.marche = True
            self.direction = -1
        elif pyxel.btn(pyxel.KEY_D):
            self.vel_x = self.vitesse
            self.marche = True
            self.direction = 1
        else:
            self.vel_x = 0
            self.marche = False
        
         # Gestion du sprint
        if pyxel.btn(pyxel.KEY_CTRL) and pyxel.btn(pyxel.KEY_Q):
            self.vel_x = 1.5 * self.direction * self.vitesse
            self.court=True
            self.cd_course+=1
        if pyxel.btn(pyxel.KEY_CTRL) and pyxel.btn(pyxel.KEY_D):
            self.vel_x = 1.2 * self.direction * self.vitesse              #oui je sais, rip. c'est overcompliqué pour rien mais c'était plus simple a coder (modifie stv)
            self.court=True
            self.cd_course+=1
        if self.cd_course>=50 and self.court:
            self.vel_x = 2 * self.direction * self.vitesse
            self.court_max=True
        if not self.court:
            self.cd_course=0
            self.court_max=False


        # Gestion du saut et double saut
        if pyxel.btnp(pyxel.KEY_SPACE):
            if self.grounded:
                self.vel_y = -self.puissance_saut
                self.grounded = False
            elif self.double_saut_dispo:
                self.vel_y = -self.puissance_saut
                self.double_saut_dispo = False
                
        # Gestion du air dash
        if pyxel.btn( pyxel.MOUSE_BUTTON_RIGHT) and not self.grounded and self.airdash_dispo :
            self.gravite=0
            self.vel_x = self.direction*5
            self.jauge_airdash += 1
            if self.jauge_airdash>=10:
                self.airdash_dispo = False

        
        # Gestion du dash
        if pyxel.btn( pyxel.MOUSE_BUTTON_RIGHT) and self.grounded and self.dash_dispo :
            if not self.court_max:
                 self.vel_x = self.direction*5
            if self.court_max:
                 self.vel_x = self.direction*6
            self.jauge_dash += 1
            if self.jauge_dash >= 8:
                self.dash_dispo = False
        
        if pyxel.btn( pyxel.MOUSE_BUTTON_RIGHT) and self.grounded and self.dash_dispo:
             self.est_en_dash=True
        else:
             self.est_en_dash=False

        if pyxel.btn( pyxel.MOUSE_BUTTON_RIGHT) and not self.grounded and self.airdash_dispo:
             self.est_en_airdash=True
        else:
             self.est_en_airdash=False

        # Gestion du fast fall
        if pyxel.btn(pyxel.KEY_S) and not self.grounded:
            self.vel_y += 1.2 * self.gravite

        # Gravité
        self.vel_y += self.gravite

        # Mise à jour de la position
        self.x += self.vel_x
        self.y += self.vel_y

        # Détection de la fin du saut
        if self.y + self.hauteur >= pyxel.height:
            self.y = pyxel.height - self.hauteur
            self.vel_y = 0
            self.grounded = True
            self.double_saut_dispo = True
            self.airdash_dispo = True
            self.jauge_airdash=0
            if not self.dash_dispo:
                self.jauge_dash=0
                self.cd_dash += 1
                if self.cd_dash >=60:
                    self.cd_dash=0
                    self.dash_dispo = True






    def draw(self):
        # Dessiner le joueur
        if self.court and self.grounded and not self.court_max:               #anim début de course (pré-glissade)
                if pyxel.frame_count % 8 < 4:
                    pyxel.blt(self.x, self.y, 0, 16, 64, self.direction*self.largeur, self.hauteur, 2)
                else:
                    pyxel.blt(self.x, self.y, 0, 24, 64, self.direction*self.largeur, self.hauteur, 2)

        if self.court_max and self.grounded:           #anim course max (glissade)
                    pyxel.blt(self.x, self.y, 0, 16, 72, self.direction*self.largeur, self.hauteur, 2)

        if not self.grounded and not self.est_en_airdash:                                                  #anim vol
                if pyxel.frame_count % 8 < 4:
                    pyxel.blt(self.x, self.y, 0, 16, 16, self.direction*self.largeur, self.hauteur, 2)
                else:
                    pyxel.blt(self.x, self.y, 0, 24, 16, self.direction*self.largeur, self.hauteur, 2)

        if self.marche == False and self.grounded:     #anim statique
                if pyxel.frame_count % 120 < 60:
                    pyxel.blt(self.x, self.y, 0, 0, 72, self.direction*self.largeur, self.hauteur, 2)
                else:
                    pyxel.blt(self.x, self.y, 0, 8, 72, self.direction*self.largeur, self.hauteur, 2)

        if self.marche == True and self.grounded and not self.court:            #anim marche
            if pyxel.frame_count % 20 < 10:
                pyxel.blt(self.x, self.y, 0, 0, 64, self.direction*self.largeur, self.hauteur, 2)
            elif not self.est_en_dash:
                pyxel.blt(self.x, self.y, 0, 8, 64, self.direction*self.largeur, self.hauteur, 2)

        if self.court_max and self.est_en_dash:               #anim dash
             pyxel.blt(self.x, self.y, 0, 0, 80, self.direction*self.largeur, self.hauteur, 2)
        if self.court_max and self.est_en_airdash:               #anim airdash
             pyxel.blt(self.x, self.y, 0, 0, 80, self.direction*self.largeur, self.hauteur, 2)
        

        
class App:
    def __init__(self):
        pyxel.init(160, 120, title="Pokipo", fps=60, quit_key=pyxel.KEY_ESCAPE)
        pyxel.load("pokipo.pyxres")
        self.joueur = Joueur(80, 60)
        pyxel.run(self.update, self.draw)

    def update(self):
        self.joueur.update()

    def draw(self):
        # Remplir l'écran avec une couleur de fond grise
        pyxel.cls(12)
        # Dessiner le joueur
        self.joueur.draw()

App()
