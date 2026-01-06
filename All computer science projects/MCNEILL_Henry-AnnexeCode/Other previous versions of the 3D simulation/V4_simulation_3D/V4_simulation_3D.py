#importer les librairies et l'autre partie du programme 
import pygame
import math 
from pygame.locals import (K_LEFT, K_RIGHT,
                           K_w, K_a, K_d, K_s, K_SPACE)

#import le programme avec les classes
from V4_Simulation_3D_definition import*

#position et vitesse du sprite
sprite_pos_x = 350
sprite_pos_y = 350
sprite_speed = 8

#varibales pour les rayons 
angle_rayon = 0
rayon = 900

#création de la scène et des murs#
scene= [0,0,0,0,
        0,0,0,1,
        0,1,0,0,
        0,0,0,1,]



serie=int(len(scene)**(1/2)) #nb de bloc (de la liste scene) par colonne/rangée
espace= 600/serie

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
    #verifier si l'utilisateur veut changer arrêter les modifications
    modif = inputs_modifications(modif)
    
    clock.tick(fps)
    
    #afficher les fonds d'écrans
    screen.fill("white")
    
    #Tracer les murs verticaux et horizontaux et les modifier
    liste_V,liste_H = murs_modificaion(serie,espace,liste_V,liste_H,screen)
    
    
    pygame.display.update()


pygame.display.set_caption('Jeu 2D')

run = True     
size=[1200,800]
screen = pygame.display.set_mode(size)

#début du jeu
while run==True:
    clock.tick(fps)
    
    #afficher les fonds d'écrans
    screen.fill("white")
    
    #inputs des déplacements et rayons du sprite
    sprite_pos_x,sprite_pos_y,angle_rayon= inputs_jeu(sprite_pos_x,sprite_pos_y,sprite_speed,angle_rayon)
    
    #Tracer les murs verticaux et horizontaux 
    rayons(serie,espace,liste_V,liste_H,screen)

    #collision entre les rayons et les murs
    collisions(angle_rayon,rayon,espace,liste_V,liste_H,sprite_pos_x,sprite_pos_y,screen)
            
        
    #pointreprésentant le sprite
    pygame.draw.circle(screen, "black",[sprite_pos_x, sprite_pos_y],5)
    
    
    pygame.display.update()
pygame.quit()
