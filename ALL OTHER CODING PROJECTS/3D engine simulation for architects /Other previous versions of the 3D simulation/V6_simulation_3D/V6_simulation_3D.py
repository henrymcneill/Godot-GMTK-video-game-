#importer les librairies et l'autre partie du programme 
import pygame
import math 
from pygame.locals import (K_LEFT, K_RIGHT,
                           K_w, K_a, K_d, K_s, K_SPACE)

#import le programme avec les classes
from V6_Simulation_3D_definition import*

#varibales pour les rayons 
angle_rayon = 0
rayon = 900

serie= 20
espace= 600/serie

beta_fisheye= 80
distance_écran_et_hauteur_mur= 25000/serie

#position et vitesse du sprite
sprite_pos_x = 150
sprite_pos_y = 300
sprite_speed = 32/serie

#def pour flouter l'image
blur_image()
#def pour scan l'image
scene= scan_image(serie,espace)

liste_V=[1] #Verticale
liste_H=[1] #mur du jeu horizontal
#On garde le 1 pour que la séquence d'après fonctionne

#Définir les mur!!!
creation_murs(scene,liste_V,liste_H,serie)

##################### JEU ##############################
#demarrage de pygame
pygame.init()

#frames per second
fps = 30
clock = pygame.time.Clock()

#titre de la fenetre de jeu
pygame.display.set_caption('Ecran de modification')

modif=True
size=[600,600]
screen = pygame.display.set_mode(size)

#écran de modificaton
while modif==True:
    clock.tick(fps)
    #afficher le fond d'écrans
    screen.fill( (252, 252, 252))
    
    #Tracer les murs verticaux et horizontaux et les modifier
    liste_V,liste_H = murs_modificaion(serie,espace,liste_V,liste_H,screen)
    
    #verifier si l'utilisateur veut changer arrêter les modifications
    modif = interactions_utilisateur(modif)
    
    #On le met deux fois pour que les modifications soient bien prisent en comptent
    liste_V,liste_H = murs_modificaion(serie,espace,liste_V,liste_H,screen)
    pygame.display.update()


pygame.display.set_caption('Jeu 3D')

run = True     
size=[1200,600]
screen = pygame.display.set_mode(size)

#début du jeu
while run==True:
    clock.tick(fps)
    
    #afficher les fonds d'écrans
    screen.fill("beige")
    #afficher le plafond 
    pygame.draw.rect(screen, "gray", pygame.Rect(0, 0, 1200, 300),  width=0)
    
    # changement de la position, l'angle de vue et autres paramètres
    sprite_pos_x,sprite_pos_y,angle_rayon, sprite_speed, distance_écran_et_hauteur_mur,run= création_sprite_2D(sprite_pos_x,sprite_pos_y,sprite_speed,angle_rayon,distance_écran_et_hauteur_mur,screen)
    affichage_murs_2D(serie,espace,liste_V,liste_H,screen)
    #collision entre les rayons et les murs
    distance_sprite_mur = collisions_affichage_3D(angle_rayon,rayon,espace,liste_V,liste_H,sprite_pos_x,sprite_pos_y,serie,beta_fisheye,distance_écran_et_hauteur_mur,screen)
    
    #Tracer les murs verticaux et horizontaux 
    affichage_murs_2D(serie,espace,liste_V,liste_H,screen)
    
    pygame.display.update()
pygame.quit()
quit()
