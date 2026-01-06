# Travail de maturité genevoise - Collège Calvin 2024/2025
# Travail: Coder une simulation tridimensionnelle d’une chambre, de la conception théorique à la programmation
# Elève: Henry MC NEILL [groupe 407] - Maître accompagnant: Eric VON AARBURG


### Fichier ayant la strucuture du programme ###

## Importer les librairies et le fichier avec les définitions ##
import pygame
#librairie pour ouvrir une fenêtre et l'animer 

from Final_Simulation_3D_definition import*
#importer le fichier avec les définitions


## Variables de départ ##
Nb_murs= 50 # nombre de murs par côté
longueur_murs = 600/Nb_murs # calculer la longueur des murs 

angle_rayon = 0 # l'angle de notre rayon le plus à gauche de notre champ de vision

beta_fisheye = 80 # angle beta pour corriger l'effet fishbowl
omega = 12500/Nb_murs # omega --> distance du sprite à l'écran fictif * hauteur du mur
# Calcul pour proportionnellement modifier la "distance du sprite à l'écran fictif" et la "hauteur du mur" en fonction du nombre de murs

sprite_pos_x = 200 # position horizontale du sprite
sprite_pos_y = 200 # position verticale du sprite

sprite_speed = 32/Nb_murs
# Calcul pour proportionnellement  modifier la vitesse du sprite en fonction du nombre de murs


## Scan l'image pour le reproduire dans la simulation ##
blur_image() # def pour flouter l'image

bloc_liste = scan_image(Nb_murs,longueur_murs)
# def pour scan l'image et définir le plan de la salle sous forme de liste

liste_H,liste_V = creation_murs(Nb_murs,bloc_liste)
# def pour créer des listes pour les murs horizontaux et verticaux


## Variables pour lancer pygame ##
fps = 30 #frames per second
clock = pygame.time.Clock() # raccourci pour mettre en place les fps (temps)

size=[600,600] # dimensions de l'écran (en pixel)
screen = pygame.display.set_mode(size) # actualiser les dimensions de la fenêtre

pygame.display.set_caption('Ecran de modification') # titre de la fenetre pour l'interface de modification


## Lancement de l'interface de modificaton ##
run = True
while run==True:
    
    clock.tick(fps) # définir les fps
    
    screen.fill( (252, 252, 252)) # couleur du fond d'écran
    
    liste_H,liste_V,run = murs_modification(Nb_murs,longueur_murs,liste_H,liste_V,run,screen)
    # tracer les murs verticaux et horizontaux et les modifier
    
    pygame.display.update() # actualiser les éléments de la fenêtre


## Variables pour lancer pygame ##
size=[1200,600] # dimensions de l'écran (en pixel)
screen = pygame.display.set_mode(size) # actualiser les dimensions de la fenêtre

pygame.display.set_caption('Simulation tridimensionnelle')
# titre de la fenetre pour la simulation tridimensionnelle


## Lancement de la simulation tridimensionnelle ##
run = True  
while run==True:
    
    clock.tick(fps) # définir les fps
    
    background_3D(screen)
    # dessiner le sol et le plafond composants l'arrière plan
    
    sprite_pos_x,sprite_pos_y,sprite_speed,angle_rayon,omega,run= interactions_joueur(sprite_pos_x,sprite_pos_y,
                                                                                        sprite_speed,angle_rayon,omega,run,screen)
    # changement de la position, de l'angle de vue et d'autres paramètres 
    
    distance_sprite_mur = affichage_3D(angle_rayon,longueur_murs,liste_H,liste_V,sprite_pos_x,sprite_pos_y,
                                        Nb_murs,beta_fisheye,omega,screen)
    # collisions entre le champ de vision et les murs + affichage des murs 3D
    
    mini_map_murs_2D(Nb_murs,longueur_murs,liste_H,liste_V,screen)
    # tracer les murs 2D de la mini-map 
    
    pygame.draw.circle(screen, "black",[sprite_pos_x/3, sprite_pos_y/3],3)
    # dessiner le sprite sur la mini-map
    
    pygame.display.update() # actualiser les éléments de la fenêtre


## quitter pygame et python ##
pygame.quit()
quit()
