#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pyxel
TILEMAP=int(input("Choisissez une map (0,1) : "))
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
        self.direction=-1 # -1 gauche    1 droite
        self.court=False
        self.cd_course=0
        self.court_max=False

        # états de l'air dash
        self.airdash_dispo=True
        self.jauge_airdash=0
        self.est_en_airdash=False
        self.auto_airdash=False
        self.vel_airdash=0

        # états du dash
        self.dash_dispo=True
        self.jauge_dash=0
        self.cd_dash=0
        self.cd_dashmax=0
        self.est_en_dash=False
        self.auto_dash=False
        self.auto_dashmax=False
        self.vel_dash=0
        """"""""""""""""""""""""""""""
        """"""""""""""""""""""""""""""
        """"""""""""""""""""""""""""""

    def move(self):
        key_dir = 0
        if pyxel.btn(pyxel.KEY_Q):
            key_dir = -1
        elif pyxel.btn(pyxel.KEY_D):
            key_dir = 1

        if key_dir != 0:
            if not self.grounded:
                if self.direction != key_dir:
                           self.vel_x = key_dir * 0.3
                else:
                        self.vel_x = key_dir*self.vitesse
            else:
                self.direction = key_dir
                self.vel_x = self.direction*self.vitesse
                self.marche = True
        else:
                self.vel_x = 0
                self.marche = False

    def update(self):
        self.gravite=0.2
        self.vitesse=1
        self.court=False
        self.court_max=False
        
        if self.auto_airdash == True:
            self.gravite = 0
            self.vel_airdash = self.direction*4-self.vel_x
            self.jauge_airdash += 1
            if self.jauge_airdash >= 10:
                self.auto_airdash = False
                self.airdash_dispo = False
        
        if self.auto_dash == True:
            self.vel_dash = self.direction*3
            self.cd_dash+=1
            if self.cd_dash>=10:
                 self.dash_dispo=False
                 self.auto_dash=False


             

        # Gestion des déplacements horizontaux
        self.move()

        if not self.auto_airdash:
            if self.vel_airdash>=0:
                self.vel_airdash-=0.2
                if self.vel_airdash<=0:
                    self.vel_airdash=0
            else:
                self.vel_airdash+=0.2
                if self.vel_airdash>=0:
                    self.vel_airdash=0

        if not self.auto_dash:
            if self.vel_dash>=0:
                self.vel_dash-=0.2
                if self.vel_dash<=0:
                    self.vel_dash=0
            else:
                self.vel_dash+=0.2
                if self.vel_dash>=0:
                    self.vel_dash=0

         # Gestion du sprint
        if pyxel.btn(pyxel.KEY_CTRL):
            self.court = True
            self.move()
            if self.vel_x !=0:
                self.vel_x*=1.2
                self.cd_course += 1
        if self.cd_course>=50 and self.court:
            self.move()
            self.vel_x *= 2
            if self.vel_x !=0:
                self.court_max=True
        elif not self.court:
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
            self.auto_airdash=True

        # Gestion du dash
        if pyxel.btn( pyxel.MOUSE_BUTTON_RIGHT) and self.grounded and self.dash_dispo :
            self.auto_dash=True

        # Gestion du fast fall
        if pyxel.btn(pyxel.KEY_S) and not self.grounded:
            self.vel_y += 1.2 * self.gravite

        # Gravité
        self.vel_y += self.gravite

        # Mise à jour de la position
        self.x += self.vel_dash
        self.x += self.vel_airdash
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
            self.auto_airdash=False
            if not self.dash_dispo:
                self.jauge_dash=0
                self.cd_dash += 1
                if self.cd_dash >=60:
                    self.cd_dash=0
                    self.dash_dispo = True






    def draw(self):
        # Dessiner le joueur
        if self.court and self.grounded and not self.court_max and pyxel.btn( pyxel.KEY_D):#anim début de course (pré-glissade)
                if pyxel.frame_count % 8 < 4:
                    pyxel.blt(self.x, self.y, 0, 16, 64, self.direction*self.largeur, self.hauteur, 2)
                else:
                    pyxel.blt(self.x, self.y, 0, 24, 64, self.direction*self.largeur, self.hauteur, 2)
        if self.court and self.grounded and not self.court_max and pyxel.btn( pyxel.KEY_Q):#anim début de course (pré-glissade)
                if pyxel.frame_count % 8 < 4:
                    pyxel.blt(self.x, self.y, 0, 16, 64, self.direction*self.largeur, self.hauteur, 2)
                else:
                    pyxel.blt(self.x, self.y, 0, 24, 64, self.direction*self.largeur, self.hauteur, 2)

        if self.court_max and self.grounded:                                                          #anim course max (glissade)
                    pyxel.blt(self.x, self.y, 0, 16, 72, self.direction*self.largeur, self.hauteur, 2)

        if not self.grounded and not self.auto_airdash:                                               #anim vol
                if pyxel.frame_count % 8 < 4:
                    pyxel.blt(self.x, self.y, 0, 16, 16, self.direction*self.largeur, self.hauteur, 2)
                else:
                    pyxel.blt(self.x, self.y, 0, 24, 16, self.direction*self.largeur, self.hauteur, 2)

        if self.marche == False and self.grounded:                                                    #anim statique
                if pyxel.frame_count % 120 < 60:
                    pyxel.blt(self.x, self.y, 0, 0, 72, self.direction*self.largeur, self.hauteur, 2)
                else:
                    pyxel.blt(self.x, self.y, 0, 8, 72, self.direction*self.largeur, self.hauteur, 2)

        if self.marche == True and self.grounded and not self.court:                         #anim marche
            if pyxel.frame_count % 20 < 10:
                pyxel.blt(self.x, self.y, 0, 0, 64, self.direction*self.largeur, self.hauteur, 2)
            elif not self.auto_dash:
                pyxel.blt(self.x, self.y, 0, 8, 64, self.direction*self.largeur, self.hauteur, 2)

        if self.auto_dash:                                                               #anim dash
             pyxel.blt(self.x, self.y, 0, 0, 80, self.direction*self.largeur, self.hauteur, 2)
        if self.auto_airdash:                                                              #anim airdash
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
        pyxel.bltm(0, 0, TILEMAP, 0, 0, 10000, 10000, 0)
        # Dessiner le joueur
        self.joueur.draw()
        pos_x=self.joueur.x
        if self.joueur.x<80:
            pyxel.camera(0,0)
        else:
            pyxel.camera(pos_x-80,0)
        pyxel.text(10,10, "Ladies, with gentle hands", 3)
        
App()
