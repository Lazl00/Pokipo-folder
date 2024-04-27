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
        self.vitesse = 1.5
        self.puissance_saut = 3
        self.gravite = 0.20
        self.vel_x = 0
        self.vel_y = 0
        self.marche = False
        self.direction=-1 # 0 gauche    1 droite
        
        # État du joueur
        self.grounded = True
        self.a_double_saut = True

    def update(self):
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
        
        
        # Gestion du saut et double saut
        if pyxel.btnp(pyxel.KEY_SPACE):
            if self.grounded:
                self.vel_y = -self.puissance_saut
                self.grounded = False
            elif self.a_double_saut:
                self.vel_y = -self.puissance_saut
                self.a_double_saut = False
        
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
            self.a_double_saut = True


    def draw(self):
        # Dessiner le joueur
        if self.marche == False:
                if pyxel.frame_count % 120 < 60:
                    pyxel.blt(self.x, self.y, 0, 0, 72, self.direction*self.largeur, self.hauteur, 2)
                else:
                    pyxel.blt(self.x, self.y, 0, 8, 72, self.direction*self.largeur, self.hauteur, 2)
        if self.marche == True:
            if pyxel.frame_count % 20 < 10:
                pyxel.blt(self.x, self.y, 0, 0, 64, self.direction*self.largeur, self.hauteur, 2)
            else:
                pyxel.blt(self.x, self.y, 0, 8, 64, self.direction*self.largeur, self.hauteur, 2)

        
class App:
    def __init__(self):
        pyxel.init(160, 120, fps=60)
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
