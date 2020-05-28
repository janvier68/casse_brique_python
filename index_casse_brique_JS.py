#####---------------------------------- CREDIE -------------------------------------------#####
#Matthieu S
#Jacques S
    #---somaire--#
#-importation
#-pygame initialisation
#-music
#-fonction d'indice
#-collision
#-ouvrir fichier
#-crée objet
#-class
#-fonction affichage
#-fonction jeux
#-fonction menu
    #---fin somaire--#

#####---------------------------------- IMPORTATION   -------------------------------------------#####

import pygame
from pygame.locals import *
import variable
from random import randint,choice
import tkinter as tk
from tkinter import filedialog

#####---------------------------------- FIN IMPORTATION -------------------------------------------#####


#####---------------------------------- PYGAME INITIALISATION  -------------------------------------------#####

#pour le song
pygame.mixer.pre_init(44100, -16, 2, 512)
#initialisation de pygame
pygame.init()
#on fix un chanel
pygame.mixer.set_num_channels(64)

# pour le text
font = pygame.font.SysFont("Comic Sans MS", 30)

#on définit une clock
clock = pygame.time.Clock()
#note de musicques
music_starteur=pygame.mixer.Sound('music/music.ogg')
#song interration
touche_brique=pygame.mixer.Sound('music/explosion.wav')
bouton_toucher=pygame.mixer.Sound('music/bouton_toucher.wav')
moin_une_vie=pygame.mixer.Sound('music/moin_une_vie.wav')
touche_joueur=pygame.mixer.Sound('music/touche_joueur.wav')
touche_mur=pygame.mixer.Sound('music/touche_mur.wav')

#Icone #a placer avant pour que le logo sans dans la bar des taches
icone = pygame.image.load(variable.image_icone)
pygame.display.set_icon(icone)

#Ouverture de la fenêtre Pygame (carré : largeur = hauteur)
screen = pygame.display.set_mode((variable.cote_fenetre_largeur, variable.cote_fenetre_longeur))

#Titre
pygame.display.set_caption(variable.titre_fenetre)

#image
BOUTON=pygame.image.load('img/bouton.png').convert()
BOUTON.set_colorkey((255,255,255))
TITRE=pygame.image.load('img/titre.png').convert()
BRIQUE=pygame.image.load('img/brique.png').convert()

#variable
nb_vie=3#jsp si obligatoi
#liste pour le multie joueur
liste_mur_pour_pvp=[[0,0,1,1],[0,0,0,1],[0,0,0,0]]
liste_mur_perd_vie_pour_pvp=[[1,1,0,0],[1,1,1,0],[1,1,1,1]]

COLOR=[(0, 153, 51),(255, 255, 0),(255, 0, 0),(255, 0, 255),(51, 153, 255),(0, 0, 255),(255, 255, 255),(0,0,0)]

#####---------------------------------- FIN PYGAME INITIALISATION  -------------------------------------------#####


#####---------------------------------- MUSIC  -------------------------------------------#####

def start_music():
    """ pour commener la music """
    pygame.mixer.init()
    pygame.mixer.music.load("music/bit-rush-arcade-2015-login-screen-league-of-legends.mp3")
    pygame.mixer.music.play(-1)

def stop_music():
    """ pour arrêter la music """
    pygame.mixer.music.stop()

def effect_song():
    """ en fonctio de la global is_song on coup ou alume le song """
    global is_song
    if is_song:
        is_song=0
        stop_music()
    else:
        is_song=1
        start_music()

#####---------------------------------- FIN MUSIC  -------------------------------------------#####


#####---------------------------------- FONCTION D'INDICE  -------------------------------------------#####

def couleur_fonction_nombre_vie(vie):
    """renvoie la couleur en fonction de vie"""
    if vie==3:
        return (51, 204, 51)#vert
    elif vie==2:
        return (255, 153, 0)#orange
    elif vie==1:
        return (255, 0, 0)#rouge
    else:
        return (0,255,0)#couleur de base

def convertire_index(i):
    """ renvoie nom joueur en fonction indice """
    if i==0:
        return 'joueur du bas'
    if i==1:
        return 'joueur du haut'
    if i==2:
        return 'joueur du gauche'
    if i==3:
        return 'joueur du droit'

#####---------------------------------- FIN FONCTION D'INDICE  -------------------------------------------#####

#####---------------------------------- COLLISION  -------------------------------------------#####

def collision_test(rect,tiles):
    """ on rentre un rect et un liste rect
    renvoie tout les rects toucher
    """
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list

#####---------------------------------- OUVRIR UN FICHIER  -------------------------------------------#####
def ouvrir_fichier():
    """
    Pour ouvrir l'explorateur pour selectionner le fichier image à ouvrir
    Entrée : None
    Sortie : Chemin absolu du fichier ouvert
    """
    popup=tk.Tk()
    i=1
    while i:
        chemin_fichier =  filedialog.askopenfilename(initialdir = "./",title = "Select file",filetypes = (("text","*.txt"),("all files","*.*")))
        if chemin_fichier!='':
            popup.destroy()
            i=0
    return chemin_fichier



#####---------------------------------- CREE OBJET  -------------------------------------------#####

def position_mur(x,y,hauteur,largeur,liste_mur):
    """ on donne la largeur/hauteur de la fenêtre puis en fonction de liste_mur
    1 ou 0 si on veut un mur
    [sud,nord,ouest,est]
    """
    a=[]
    if liste_mur[0]:#sud
        a.append(pygame.Rect(x,y+hauteur,largeur,0))
    if liste_mur[1]:#nord
        a.append(pygame.Rect(x,y,largeur,0))
    if liste_mur[2]:#ouest
        a.append(pygame.Rect(x,y,0,hauteur))
    if liste_mur[3]:#est
        a.append(pygame.Rect(x+largeur,y,0,hauteur))
    return a[:]

def cree_brique(x,y,color):
    """ crée des briques en liste avec stock de x,y,color,rect"""
    return [x,y,color,pygame.Rect(x,y,variable.brique_largeur,variable.brique_hauteur)]

def load_map(path):
    """ fonction qui transforme un ficher.txt en liste pour le terrin"""
    f = open(path,'r')
    data = f.read()
    f.close()
    data = data.split('\n')
    game_map = []
    for row in data:
        game_map.append(list(row))
    return game_map

def cree_map(terrin_liste):
    """ crée tout les brique en fonction du terrin"""
    global les_briques
    les_briques=[]
    y=0
    for ligne in terrin_liste:
        x=0
        for cologne in ligne:
            if int(cologne)==1:
                les_briques.append(cree_brique(x,y,variable.brique_couleur))
            x+=variable.brique_largeur
        y+=variable.brique_hauteur

#####---------------------------------- FIN CREE OBJET  -------------------------------------------#####


#####---------------------------------- CLASS  -------------------------------------------#####

class joueur():
    """ class qui contien la raquette"""

    def __init__(self,x,y):
        """ init avec co de la raquette"""

        self.player_location = [x,y]

        self.moving_right = False
        self.moving_left = False

        self.player_rect = pygame.Rect(self.player_location[0],self.player_location[1],70,10)

    def fait_move(self,indice):
        """ en fonction de l'indice donne la direction """
        if indice == 1:
            self.moving_right = True
        if indice == 2:
            self.moving_left = True
        if indice == 3:
            self.moving_right = False
        if indice == 4:
            self.moving_left = False

    def bouger(self,mur):
        """ en fonction de la fonction plus haut, affiche bouge actualisa sa position """
        touche=collision_test(self.player_rect,mur)

        pygame.draw.rect(screen,(0, 0, 0),self.player_rect)

        if touche:#si il touche se que on lui dit de toucher
            for tile in touche:
                if self.moving_right:
                    self.player_location[0]=10
                elif self.moving_left:
                    self.player_location[0]=915
        else:
            if self.moving_right == True:
                self.player_location[0] += 5
            if self.moving_left == True:
                self.player_location[0] -= 5


        self.player_rect.x = self.player_location[0] # update rect x
        #self.player_rect.y = self.player_location[1] # update rect y

        pygame.draw.rect(screen,(255, 0, 0),self.player_rect)

class joueur_vertical():
    """ pour le multie, la même que au dessus sauf que c en verticale"""
    def __init__(self,x,y):
        self.player_location = [x,y]
        self.moving_right = False
        self.moving_left = False
        self.player_rect = pygame.Rect(self.player_location[0],self.player_location[1],10,70)
    def fait_move(self,indice):
        if indice == 1:
            self.moving_right = True
        if indice == 2:
            self.moving_left = True
        if indice == 3:
            self.moving_right = False
        if indice == 4:
            self.moving_left = False
    def bouger(self,mur):
        touche=collision_test(self.player_rect,mur)
        pygame.draw.rect(screen,(0, 0, 0),self.player_rect)
        if touche:
            for tile in touche:
                if self.moving_right:
                    self.player_location[1]=10
                elif self.moving_left:
                    self.player_location[1]=720
        else:
            if self.moving_right == True:
                self.player_location[1] += 5
            if self.moving_left == True:
                self.player_location[1] -= 5
        #self.player_rect.x = self.player_location[0] # update rect x
        self.player_rect.y = self.player_location[1] # update rect y
        pygame.draw.rect(screen,(255, 0, 0),self.player_rect)

class Ball():
    """ class qui fait la balle """

    def __init__(self, position_x,position_y,couleur,V_de_X=0,V_de_Y=0):
        """ beaucoup d'indice, les co*2, et les Vecteur*2 """
        self.player_coordonnee=[position_x,position_y]
        self.color=couleur

        self.player_mouvement=[0,0]
        if V_de_X:
            self.player_mouvement[0]=V_de_X
        else:
            self.player_mouvement[0]=randint(5,10)
        if V_de_Y:
            self.player_mouvement[1]=V_de_Y
        else:
            self.player_mouvement[1]=randint(5,10)

        #pour les collision, on crée les rectangle si dessous en en fonction on réagie
        self.player_rect={}
        #le rect de base
        self.player_rect["total"]=pygame.Rect(self.player_coordonnee[0],self.player_coordonnee[1],10,10)
        #lignes principale
        self.player_rect["n-s"]=pygame.Rect(self.player_coordonnee[0]+2,self.player_coordonnee[1],6,10)
        self.player_rect["o-e"]=pygame.Rect(self.player_coordonnee[0],self.player_coordonnee[1]+2,10,6)
        #diagonal
        self.player_rect["no"]=pygame.Rect(self.player_coordonnee[0],self.player_coordonnee[1],2,2)
        self.player_rect["ne"]=pygame.Rect(self.player_coordonnee[0]+8,self.player_coordonnee[1],2,2)
        self.player_rect["so"]=pygame.Rect(self.player_coordonnee[0],self.player_coordonnee[1]+8,2,2)
        self.player_rect["se"]=pygame.Rect(self.player_coordonnee[0]+8,self.player_coordonnee[1]+8,2,2)


    def afficher_cercle(self,color=(255,255,0)):
        """ affiche la balle et on peut modifier la couleur """
        pygame.draw.circle(screen, color, (self.player_rect['total'].x+self.player_rect['total'].height//2,self.player_rect['total'].y+self.player_rect['total'].height//2),self.player_rect['total'].height//2)

    def avancer_co_balle(self):
        """ fonction qui gère l'affichage de la balle+ avancement"""
        self.afficher_cercle((0,0,0))
        for key in self.player_rect.keys():
            self.player_rect[key].x += self.player_mouvement[0]
            self.player_rect[key].y += self.player_mouvement[1]
        self.afficher_cercle((255,255,0))

    def teste_collision(self,tiles):
        """ renvoie tout se que la balle touche + change les vecteurs """
        hit_list_total = collision_test(self.player_rect['total'],tiles)
        if hit_list_total:
            liste_toucher=[]
            for key in self.player_rect.keys():
                hit_list = collision_test(self.player_rect[key],tiles)
                if hit_list:
                    if key=="n-s":
                        self.player_mouvement[1]=-self.player_mouvement[1]
                        liste_toucher.append(hit_list)
                    if key=="o-e":
                        self.player_mouvement[0]=-self.player_mouvement[0]
                        liste_toucher.append(hit_list)
                    if key=="no" or key=="ne" or key=="so" or key=="se":
                        self.player_mouvement[0]=-self.player_mouvement[0]
                        self.player_mouvement[1]=-self.player_mouvement[1]
                        liste_toucher.append(hit_list)

            #on enlève les doublon
            liste_toucher=[elm for i in range(len(liste_toucher)) for elm in liste_toucher[0]]
            i=0
            while i!=len(liste_toucher):
                a=liste_toucher[i]
                j=i+1
                while j!= len(liste_toucher):
                    if liste_toucher[i]==liste_toucher[j]:
                        liste_toucher.pop(j)
                        j-=1
                    j+=1
                i+=1
            return liste_toucher
        else:
            return []

#####---------------------------------- FIN CLASS  -------------------------------------------#####


#####---------------------------------- FONCTION AFFICHAGE  -------------------------------------------#####

def draw_text(text, font, color, surface, x, y):
    """ fonction qui affiche le texte avec la police font de couleur color sur la surface au coo x y """
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def afficher_liste_rectangle(liste_rect,color,):
    """ donner liste de rectange et l'affiche avec la color"""
    for elm in liste_rect:
        pygame.draw.rect(screen,color,elm)

def disparaitre(recte,liste):
    """ surprime rect de liste et le fait disparaitre de l'écant"""
    pygame.draw.rect(screen,variable.BACKGROUND,recte[3])#recte[3] car c la ou est stoker le rect
    liste.remove(recte)

def afficher_bouton(x,y,text):
    """ affiche les bouton en x,y avec le text"""
    screen.blit(BOUTON,(x,y))
    draw_text(str(text), font, (255, 255, 255), screen, x+10, y+10)
    return  pygame.Rect(x, y, 182, 62)

def fonction_de_la_victoir_ou_deffete(v_d,nom_joueur=''):#1==>Victoir O==>Défaite
    """Affichage nom gagane + timeur retour menu"""
        #pour le nom
    #crée un carré noir qui vas ercouvir psd -1
    rect_filled = pygame.Surface((100,200))
    pygame.draw.rect(screen, (160,160,160), (0,300,1000,200))

    if v_d:#
        if nom_joueur=='':#si on pas de nom
            nom_joueur_affichage = font.render("tu a gagner", 50, variable.NOIR)
        else:
            nom_joueur_affichage = font.render("tu a gagner %s"%(nom_joueur), 50, variable.NOIR)
    else:#si on perd
        nom_joueur_affichage = font.render("tu a perdu", 50, variable.NOIR)

    screen.blit(nom_joueur_affichage, (300, 375))
    rect_filled = pygame.Surface((100,200))

    start_ticks=pygame.time.get_ticks()
    un_temps=1
    while un_temps:#boucle le temps de
        #on calcuce combien de seconde
        seconds=(pygame.time.get_ticks()-start_ticks)/1000
        #on affiche le temps restant
        temps_affichage = font.render("retour au menus dans %s seconde"%(round(5-seconds)), 50, variable.NOIR)
        #on mes dans pygame
        pygame.draw.rect(screen, (160,160,160), (400,420,500,50))
        screen.blit(temps_affichage, (400, 420))
        #actualiser
        pygame.display.flip()
        if seconds>5: # des qu'il en a plus que 5 on termine et on renvoie au menu
            un_temps=0

def afficher_brique(liste_rect):
    """ on envoie les rect et on affiche un image de brique"""
    for elm in liste_rect:
        screen.blit(BRIQUE,(elm.x,elm.y))

#####---------------------------------- FIN FONCTION AFFICHAGE  -------------------------------------------#####


#####---------------------------------- FONCTION JEUX  -------------------------------------------#####

def game(level=0):
    """ fonction qui fait jouer le joueur avec le terrin de son choie"""
    #on crée le nombre de vie
    nb_vie=3
    #on efface le terrin
    screen.fill((0,0,0))
    #on fix les mur sur les bor
    les_mur=position_mur(0,0,800,1000,[0,1,1,1])
    #les mur qui change quand la balle les touche pour la vie
    mur_perd_vie=position_mur(0,0,800,1000,[1,0,0,0])
    #on affiche les mur du terrin
    afficher_liste_rectangle(les_mur,(0,255,0))

    #on choisi le mode de choie du terrin
    if level==0:#utilisateur choisir l'emplacement du txt
        fichier=ouvrir_fichier()
        terrin=load_map(fichier)
        cree_map(terrin)
    else:#en charche le level en fonction de l'indice
        fichier="niveau/niveau_"+str(level)+".txt"
        terrin=load_map(fichier)
        cree_map(terrin)

    #on fait joueur les classe, on deffinit l'objet balle et joueur
    la_balle,Joueur=Ball(470,730,(255,255,255),-2,-2),joueur(450,750)

    # on commance la boucle infinit
    running=True
    while running:

        for event in pygame.event.get():#si il y a un évènement
            #pour quiter le jeu
            if event.type == QUIT:
                running = False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

            if event.type == KEYDOWN:#si le joueur bouge
                if event.key == K_RIGHT:
                        Joueur.fait_move(1)
                if event.key == K_LEFT:
                        Joueur.fait_move(2)
            if event.type == KEYUP:#des qu'il a terminer
                if event.key == K_RIGHT:
                    Joueur.fait_move(3)
                if event.key == K_LEFT:
                    Joueur.fait_move(4)

        if running: #si rening pas changer
            #on fait bouger le joueur qui et en colision avec les murs (qui le fait tp à l'autre bout du terrin)
            Joueur.bouger(les_mur)
            #on teste les collision de la balle
            if la_balle.teste_collision(les_mur):#avec les mur
                touche_mur.play()
            if la_balle.teste_collision([Joueur.player_rect]):#le joueur (il y à [] car normalement c fait pour des listes)
                touche_joueur.play()
            #on teste si la balle touche la zone qui fait perdre une vie
            if la_balle.teste_collision(mur_perd_vie):
                nb_vie-=1
                moin_une_vie.play()
                if nb_vie==0:#si il perd
                    fonction_de_la_victoir_ou_deffete(0)
                    running = False

            #on affiche toujours à nouveau les murs de tout sorte
            afficher_liste_rectangle(les_mur,(0,255,0))
            afficher_liste_rectangle(mur_perd_vie,couleur_fonction_nombre_vie(nb_vie))
            #on teste la collision de la balle avec les briques
            rect_brique_while=[les_briques[i][3] for i in range(len(les_briques))]
            afficher_brique(rect_brique_while)
            brique_toucher=la_balle.teste_collision(rect_brique_while)
            if brique_toucher:
                j=None#vas contenir l'indice de la brique touché
                for i in range(len(les_briques)):#on parcour tout les briques
                    if brique_toucher[0] == les_briques[i][3]:#si elle correspond à la brique toucher
                        j=i#on retien l'indice
                #on la supre
                disparaitre(les_briques[j],les_briques)
                #son destruction brique
                touche_brique.play()
                #si il n'y a plus de brique, ces donc la victoir
                if les_briques==[]:
                    fonction_de_la_victoir_ou_deffete(1)
                    running = False

            #on fait avancer la balle
            la_balle.avancer_co_balle()

            #on actualise
            pygame.display.update()
            #fps
            clock.tick(60)

def game_pvp(nb_joueur):
    """ fonction du jeux multie joueur, in faut indique le nombre de joueur, commence à 2
    un peut la même chose que game saut que c avec des listes"""

    #on définit le nombre de vie en fonction de nb_joueur
    nb_vie=[ 3 for i in range(nb_joueur)]

    #on crée les mur en fonction de nb_joueur
    les_mur=position_mur(0,0,800,1000,liste_mur_pour_pvp[nb_joueur-2])
    mur_perd_vie=position_mur(0,0,800,1000,liste_mur_perd_vie_pour_pvp[nb_joueur-2])

    #on crée l'objet balle
    la_balle=Ball(470,730,(255,255,255),2,-2)
    #on crée un liste d'objet joueur
    liste_joueur=[]
    if nb_joueur==2:
        liste_joueur.append(joueur(450,750))
        liste_joueur.append(joueur(450,50))
    elif nb_joueur==3:
        liste_joueur.append(joueur(450,750))
        liste_joueur.append(joueur(450,50))
        liste_joueur.append(joueur_vertical(50,350))
    elif nb_joueur==4:
        liste_joueur.append(joueur(450,750))
        liste_joueur.append(joueur(450,50))
        liste_joueur.append(joueur_vertical(50,350))
        liste_joueur.append(joueur_vertical(950,350))

    #on init variable qui reste dans la boucle
    running=True
    click=False#si on click
    largeur_carre,liste_carre=10,[]#on crée des blocques la taille, puis la liste de rect
    #on commence la boucle infini
    while running: # game loop
        #on inti l'écant
        screen.fill((0,0,0))
        #on récupaire le co de la souri
        mx, my = pygame.mouse.get_pos()

        #les évènements
        for event in pygame.event.get():#si il y a un évènement
            #évènement qui quite
            if event.type == QUIT:
                running = False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            #évenement pour crée des bloque
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:#poser blocques
                    click = True
                if event.button ==3:#rajouter de la taille
                    largeur_carre+=10
                    if largeur_carre>=100:
                        largeur_carre=10
                if event.button ==2:#pour suprimer
                    li=collision_test(pygame.Rect(mx-(largeur_carre//2),my-(largeur_carre//2),largeur_carre,largeur_carre),liste_carre)#tout les élement toucher pas la souri
                    for elm in li:#on parcour la liste
                        liste_carre.remove(elm)#on les suprime

            if event.type == MOUSEBUTTONUP:#des que l'on arrêtre de poser des blooques
                if event.button == 1:
                    click = False

            #si déplacement du joueur
            if event.type == KEYDOWN:
                #joueur 1
                if event.key == K_RIGHT and nb_vie[0]>0:
                        liste_joueur[0].fait_move(1)
                if event.key == K_LEFT and nb_vie[0]>0:
                        liste_joueur[0].fait_move(2)
                #joueur 2
                if event.key == K_SEMICOLON and nb_vie[1]>0:
                        liste_joueur[1].fait_move(1)
                if event.key == K_k and nb_vie[1]>0:
                        liste_joueur[1].fait_move(2)
                if nb_joueur>=3:
                    #joueur 3
                    if event.key == K_n and nb_vie[2]>0:
                            liste_joueur[2].fait_move(1)
                    if event.key == K_v and nb_vie[2]>0:
                            liste_joueur[2].fait_move(2)
                if nb_joueur>=4:
                    #joueur 4
                    if event.key == K_q and nb_vie[3]>0:
                            liste_joueur[3].fait_move(1)
                    if event.key == K_e and nb_vie[3]>0:
                            liste_joueur[3].fait_move(2)
            #si arrêt déplacement joueur
            if event.type == KEYUP:
                #joueur 1
                if event.key == K_RIGHT:
                    liste_joueur[0].fait_move(3)
                if event.key == K_LEFT:
                    liste_joueur[0].fait_move(4)
                #joueur 2
                if event.key == K_SEMICOLON:
                        liste_joueur[1].fait_move(3)
                if event.key == K_k:
                        liste_joueur[1].fait_move(4)
                if nb_joueur>=3:
                    #joueur 3
                    if event.key == K_n:
                        liste_joueur[2].fait_move(3)
                    if event.key >= K_v:
                            liste_joueur[2].fait_move(4)
                if nb_joueur==4:
                    #joueur 4
                    if event.key == K_q:
                            liste_joueur[3].fait_move(3)
                    if event.key == K_e:
                            liste_joueur[3].fait_move(4)

        #si il a cliquer
        if click:
            #on crée un rectangle
            rectangle=pygame.Rect(mx-(largeur_carre//2),my-(largeur_carre//2),largeur_carre,largeur_carre)
            if la_balle.teste_collision([rectangle]):#si rect sur la balle
                rectangle=0
            else:#sinon on l'aprend à la liste des rect
                liste_carre.append(rectangle)

        if running:
            #on geaire les joueur
            for i in range(len(liste_joueur)):#on parcour tout les joueurs
                if nb_vie[i]>0:#si il sont encor en vie
                    #on les fait bouger + teste si touche la balle
                    liste_joueur[i].bouger(les_mur+mur_perd_vie)
                    if la_balle.teste_collision([liste_joueur[i].player_rect]):
                        touche_joueur.play()
            #on si la balle touche les mur pas utile + les carre poser par l'utilisateur
            if la_balle.teste_collision(les_mur) or la_balle.teste_collision(liste_carre):
                touche_mur.play()


            #on parcour les mur qui font perdre des vie
            for i in range(len(mur_perd_vie)):
                #si il son encor en vie
                if nb_vie[i]!=0:
                    #on teste si la balle les touche
                    if la_balle.teste_collision([mur_perd_vie[i]]):
                        nb_vie[i]-=1
                        #song
                        moin_une_vie.play()
                        #si il a perdut
                        if nb_vie[i]==0:
                            les_mur.append(mur_perd_vie[i])
                            #on parcour le nombre de joueur restant
                            liste_survivant=[]
                            for j in range(len(nb_vie)):
                                if nb_vie[j]:
                                    liste_survivant.append(j)
                            #si il en reste que 1
                            if 1==len(liste_survivant):
                                fonction_de_la_victoir_ou_deffete(1,convertire_index(liste_survivant[0]))#affiche la victoir
                                running=0

            #on actualise tout les murs + les bloques poser par l'utilisateur
            for i in range(len(mur_perd_vie)):
                afficher_liste_rectangle([mur_perd_vie[i]],couleur_fonction_nombre_vie(nb_vie[i]))
            afficher_liste_rectangle(les_mur,(0,255,0))
            afficher_liste_rectangle(liste_carre,(0,255,0))

            #on fait avancer la balle
            la_balle.avancer_co_balle()

            #on actualise
            pygame.display.update()
            #fps
            clock.tick(60)

#####---------------------------------- FIN FONCTION JEUX  -------------------------------------------#####


#####---------------------------------- FONCTION MENU  -------------------------------------------#####

def menu_controle():
    """ menu d'affichage du paramètre des touches
    voir main_menu pour des préssisions sur le code"""
    continuer=1
    click = False
    screen.fill((0,0,0))
    image = pygame.image.load("img/controle.png")#crée image
    screen.blit(image, (0, 0))#on affiche l'image
    while continuer:
        mx, my = pygame.mouse.get_pos()
        if afficher_bouton(500,700,"retour").collidepoint((mx, my)):
            if click:
                bouton_toucher.play()
                continuer=0
                option()
        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                continuer=0
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                   continuer=0
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
            if event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    click = False
        if continuer:
            pygame.display.update()
            clock.tick(60)

def menu_credit():
    """ menu d'affichage des crédit
    voir main_menu pour des préssisions sur le code"""
    continuer=1
    click = False
    while continuer:
        screen.fill((0,0,0))
        screen.blit(TITRE,(0,0))
        draw_text(""" fait par Ma et Ja""", font, (255, 255, 255), screen, 400, 260)
        draw_text(""" Ma:code""", font, (255, 255, 255), screen, 400, 310)
        draw_text(""" Ja:code""", font, (255, 255, 255), screen, 400, 360)
        draw_text("""song: et """, font, (255, 255, 255), screen, 300, 600)
        mx, my = pygame.mouse.get_pos()
        if afficher_bouton(400,200,"retour").collidepoint((mx, my)):
            if click:
                bouton_toucher.play()
                continuer=0
        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                continuer=0
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                   continuer=0
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
            if event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    click = False
        if continuer:
            pygame.display.update()
            clock.tick(60)

def option():
    """ menu d'affichage des option
    voir main_menu pour des préssisions sur le code"""
    continuer=1
    click = False
    while continuer:
        screen.fill((0,0,0))
        screen.blit(TITRE,(0,0))
        mx, my = pygame.mouse.get_pos()
        bouton_menu=[[afficher_bouton(400,200,"crédit"),menu_credit],[afficher_bouton(400,300,"song"),effect_song],[afficher_bouton(400,400,"contrôle"),menu_controle],[afficher_bouton(400,500,"retour")]]
        for i in range(len(bouton_menu)):
            if bouton_menu[i][0].collidepoint((mx, my)):
                if click:
                    bouton_toucher.play()
                    if i==3:
                        continuer=0
                    else:
                        bouton_menu[i][1]()
        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                continuer=0
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                   continuer=0
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
            if event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    click = False
        if continuer:
            pygame.display.update()
            clock.tick(60)

#---------Joueur solo menu
#on crée des fonction spécifique pour se menu
niveaux_de_solo_1=lambda : game(1)
niveaux_de_solo_2=lambda : game(2)
niveaux_de_solo_3=lambda : game(3)
niveaux_de_solo_4=lambda : game(4)
def Joueur_solo_menu():
    """ menu d'affichage pour choisir son niveau dans le solo
    voir main_menu pour des préssisions sur le code"""
    continuer=1
    click = False
    while continuer:
        screen.fill((0,0,0))
        screen.blit(TITRE,(0,0))
        mx, my = pygame.mouse.get_pos()
        bouton_menu=[[afficher_bouton(400,200,"Level 1"),niveaux_de_solo_1],[afficher_bouton(400,300,"Level 2"),niveaux_de_solo_2],[afficher_bouton(400,400,"Level 3"),niveaux_de_solo_3],[afficher_bouton(400,500,"Level 4"),niveaux_de_solo_4],[afficher_bouton(400,600,"Level ?"),game],[afficher_bouton(400,700,"retour")]]
        for i in range(len(bouton_menu)):
            if bouton_menu[i][0].collidepoint((mx, my)):
                if click:
                    bouton_toucher.play()
                    if i==5:#si il clic sur retour
                        continuer=0#on termine la boucle
                    else:
                        bouton_menu[i][1]()
        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                continuer=0
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    continuer=0
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
            if event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    click = False
        if continuer:
            pygame.display.update()
            clock.tick(60)

# ------ joueur multi menu
#on crée des fonction spécifique pour se menu
niveaux_perso_2=lambda : game_pvp(2)
niveaux_perso_3=lambda : game_pvp(3)
niveaux_perso_4=lambda : game_pvp(4)
def Joueur_muti_menu():
    """ menu d'affichage pour choisir le nombre de joueur
    voir main_menu pour des préssisions sur le code"""
    continuer=1
    click = False
    while continuer:
        screen.fill((0,0,0))
        screen.blit(TITRE,(0,0))
        mx, my = pygame.mouse.get_pos()
        bouton_menu=[[afficher_bouton(400,200,"2 joueur"),niveaux_perso_2],[afficher_bouton(400,300,"3 joueur"),niveaux_perso_3],[afficher_bouton(400,400,"4 joueur"),niveaux_perso_4],[afficher_bouton(400,500,"retour")]]
        for i in range(len(bouton_menu)):
            if bouton_menu[i][0].collidepoint((mx, my)):
                if click:
                    bouton_toucher.play()#song
                    if i==3:#si il clic sur retour
                        continuer=0#on termine la boucle
                    else:
                        bouton_menu[i][1]()
        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                continuer=0
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    continuer=0
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
            if event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    click = False
        if continuer:
            pygame.display.update()
            clock.tick(60)

def main_menu():
    """ menu d'affichage pour choisir le mode de jeux les optio et quitter
    voir main_menu pour des préssisions sur le code"""
    #on mais en global si il y a du son our pas
    global is_song
    #on dit que non
    is_song=0
    #on allument le song
    effect_song()

    #on init variablre pour la boucle infini
    continuer=1
    #pour les particule
    TILE_SIZE = 20
    particles = []
    tile_map = {}
    #si on clik on remait à 0
    click = False
    #si on veut quitter l'aplication
    meurt=0
    #on commence la boucle inifi
    while continuer:
        #on mais un écrant noir
        screen.fill((0,0,0))
        #on affiche le titre
        screen.blit(TITRE,(0,0))
        #on prend la posiont de la souri
        mx, my = pygame.mouse.get_pos()
        #on init un list qui continer [rect du bouton, la fonction qui init quand le bouton toucher]
        bouton_menu=[[afficher_bouton(400,200,"Jouer Solo"),Joueur_solo_menu],[afficher_bouton(400,300,"Multie"),Joueur_muti_menu],[afficher_bouton(400,400,"Option"),option],[afficher_bouton(400,500,"Quitter")]]

        #on parcour les bouton
        for i in range(len(bouton_menu)):
            #si la souri touche
            if bouton_menu[i][0].collidepoint((mx, my)):
                if click:#si click
                    bouton_toucher.play()#song
                    if i==3:#si c quiter
                        meurt=1#on dit que l'on veut quiter
                    else:#sinon
                        bouton_menu[i][1]()#on active la fontion


        #les mille est un confitie
         #on dit ici on l'on veut mêtre des confiti
        particles.append([[randint(0,1000), randint(0,800)], [randint(0, 42) / 6 - 3.5, randint(0, 42) / 6 - 3.5],randint(4, 6)])
        particles.append([[631, 25], [randint(0, 42) / 6 - 3.5, randint(0, 42) / 6 - 3.5],randint(4, 6)])
        particles.append([[242, 129], [randint(0, 42) / 6 - 3.5, randint(0, 42) / 6 - 3.5],randint(4, 6)])
        particles.append([[822, 36], [randint(0, 42) / 6 - 3.5, randint(0, 42) / 6 - 3.5],randint(4, 6)])
        #on parcour les particle et on détécte si il touche un chose (je n'est pas mie d'objets avec des collisions) + momentum qui baisse
        for particle in particles:
            particle[0][0] += particle[1][0]
            loc_str = str(int(particle[0][0] / TILE_SIZE)) + ';' + str(int(particle[0][1] / TILE_SIZE))
            if loc_str in tile_map:
                particle[1][0] = -0.7 * particle[1][0]
                particle[1][1] *= 0.95
                particle[0][0] += particle[1][0] * 2
            particle[0][1] += particle[1][1]
            loc_str = str(int(particle[0][0] / TILE_SIZE)) + ';' + str(int(particle[0][1] / TILE_SIZE))
            if loc_str in tile_map:
                particle[1][1] = -0.7 * particle[1][1]
                particle[1][0] *= 0.95
                particle[0][1] += particle[1][1] * 2
            particle[2] -= 0.035
            particle[1][1] += 0.15
            pygame.draw.circle(screen, COLOR[randint(0,7)], [int(particle[0][0]), int(particle[0][1])], int(particle[2]))
            if particle[2] <= 0:
                particles.remove(particle)

        click = False

        #si l'utilisateur quite ou click
        for event in pygame.event.get():
            if event.type == QUIT:
                meurt=1
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
            if event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    click = False
        #on actualise
        pygame.display.update()
        clock.tick(60)
        #si on veut quitter
        if meurt:
            continuer=0
            pygame.quit()

def pres_menu():
    """ affiche logo + music avant de redirectionet au menu"""
    #on lance la music
    music_starteur.play()
    #variablre pour la boucle infinit
    continuer=1
    i,switch=0,1#varriable i=oppaciter,switch pour savoir si on + ou -
    while continuer:
        #on recouvre de noir
        screen.fill((0,0,0))
        #on l'utilisateur quite
        for event in pygame.event.get():
            if event.type == QUIT:
                continuer=0
                pygame.quit()

        if continuer:
            #si on +
            if switch:
                i+=7
            else: #si on -
                i-=7
            #on switch des le max
            if i>=255:
                switch=0
                i=255#pour ne pas que sa dépace
            elif i<=0:
                i=0#5#pour ne pas que sa dépace
                continuer=0#on termie la boucle

            #on crée un image avec un opaciter différance à chaque foir
            image = pygame.image.load("img/logo.png")
            image.fill((255, 255, 255, i), special_flags=BLEND_RGBA_MULT)
            screen.blit(image, (0, 0))
            #on  actualise
            pygame.display.update()
            clock.tick(60)
    #à la fin de la boucle on redirectionnne au menu
    main_menu()

#####---------------------------------- FIN FONCTION MENU  -------------------------------------------#####


if __name__ == "__main__":#si on l'éxécute ici
    pres_menu()
