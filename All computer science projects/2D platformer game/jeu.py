import pygame
import time

from classe_sprite import*

from pygame.locals import (K_LEFT, K_RIGHT,
                           K_w, K_a, K_d, K_SPACE)

#demarrage de pygame
pygame.init()

#titre de la fenetre de jeu
pygame.display.set_caption('2D Runner')

#creation de la fenetre
WINDOW_WIDTH = 1000 #1856
WINDOW_HEIGHT = 800 #960
WINDOW_DELTA_WIDTH = 1856 - WINDOW_WIDTH # différence de pixels pour atteindre le bord droit et gauche de l'écran

window = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))

#scrolling_screen
scrolling_screen_percent = 4/10 #il faut que le resultat final soit divisible par la vitesse (sinon le scrolling ne fonctionne pas)

#importation des images dans le programme
#le .convert_alpha() convertit l'image dans le meme format de pixel
#que la fenetre pygame
background_image = pygame.image.load("/home/henry.mcnll/USR/OC/S7_scrolling/images/background.png").convert_alpha()
platform_bloc = pygame.image.load("/home/henry.mcnll/USR/OC/S7_scrolling/images/plateforme_bloc.png").convert_alpha()
sprite_droite = [pygame.image.load("/home/henry.mcnll/USR/OC/S7_scrolling/images/sprite_droite_1.png").convert_alpha(),
                 pygame.image.load("/home/henry.mcnll/USR/OC/S7_scrolling/images/sprite_droite_2.png").convert_alpha(),
                 pygame.image.load("/home/henry.mcnll/USR/OC/S7_scrolling/images/sprite_droite_3.png").convert_alpha(),
                 pygame.image.load("/home/henry.mcnll/USR/OC/S7_scrolling/images/sprite_droite_4.png").convert_alpha()]
sprite_gauche = [pygame.image.load("/home/henry.mcnll/USR/OC/S7_scrolling/images/sprite_gauche_1.png").convert_alpha(),
                 pygame.image.load("/home/henry.mcnll/USR/OC/S7_scrolling/images/sprite_gauche_2.png").convert_alpha(),
                 pygame.image.load("/home/henry.mcnll/USR/OC/S7_scrolling/images/sprite_gauche_3.png").convert_alpha(),
                 pygame.image.load("/home/henry.mcnll/USR/OC/S7_scrolling/images/sprite_gauche_4.png").convert_alpha()]
game_over = pygame.image.load("/home/henry.mcnll/USR/OC/S7_scrolling/images/game_over.png").convert_alpha()
coeur= pygame.image.load("/home/henry.mcnll/USR/OC/S7_scrolling/images/coeur_4.png").convert_alpha()
music= pygame.mixer.Sound("/home/henry.mcnll/USR/OC/S7_scrolling/music_backgroung.mp3")
footsteps= pygame.mixer.Sound("/home/henry.mcnll/USR/OC/S7_scrolling/footsteps.mp3")
#déplacement de sprite
sprite_pos_x = 0
sprite_pos_y = -64*3 +WINDOW_HEIGHT
sprite_speed = 8

#animation de sprite
sprite_delay_max= 3 #On met 3 à la place de 4, car mon premier image n'a pas de poussiere derriere mon personnage, donc cela fait un effet bizarre. C'est pour cela qu'on va uniquement utiliser les 3 dernieres images de mon sprtie pour les déplacement
sprite_orientation= "droite"
sprite_v0= 40
sprite_a= -4

nb_vie=3

sprite= Sprite(sprite_gauche, sprite_droite, sprite_pos_x, sprite_speed, sprite_delay_max, sprite_orientation, sprite_pos_y, sprite_v0, sprite_a, nb_vie, WINDOW_WIDTH, WINDOW_DELTA_WIDTH, scrolling_screen_percent)
#plateforme
#pos_x, pos_y, taille, nb_bloc, image
plateformes=[Plateforme(0,-64*2+WINDOW_HEIGHT,64,4,platform_bloc),
             Plateforme(64*5,-64*3+WINDOW_HEIGHT,64,2,platform_bloc),
             Plateforme(64*5,-64*6+WINDOW_HEIGHT,64,4,platform_bloc),
             Plateforme(64*2,-64*4+WINDOW_HEIGHT,64,1,platform_bloc),
             Plateforme(64*8,-64*3+WINDOW_HEIGHT,64,3,platform_bloc),
             Plateforme(64*11,-64*4+WINDOW_HEIGHT,64,3,platform_bloc),
             Plateforme(64*11,-64*8+WINDOW_HEIGHT,64,4,platform_bloc),
             Plateforme(64*18,-64*5+WINDOW_HEIGHT,64,1,platform_bloc),
             Plateforme(64*16,-64*3+WINDOW_HEIGHT,64,1,platform_bloc),
             Plateforme(64*20,-64*7+WINDOW_HEIGHT,64,4,platform_bloc),
             Plateforme(64*25,-64*9+WINDOW_HEIGHT,64,4,platform_bloc)]

##################### JEU ##############################
#frames per second
fps = 30
clock = pygame.time.Clock()


pygame.mixer.Sound.play (music)
#début du jeu
while sprite.mort==False:
    
    clock.tick(fps)
    
    
    ####### APPUIS TOUCHES NON CONTINUS (click and release) #######
    #prend en compte les touches qui commencent a etre appuyees
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                sprite.activation_saut=True
                sprite.b = sprite.pos_y
    
    ############### APPUIS TOUCHES CONTINUS ####################
           
    #prend en compte toutes les touches actuellement appuyees
    keys = pygame.key.get_pressed()
    
    #Aller à droite
    if keys[K_d]==True:
        sprite.move_right(plateformes)
        
        
        
    #Aller à gauche 
    elif keys[K_a]==True:
        sprite.move_left(plateformes)
        
        
    #Si le joueur ne fait rien
    else:
        sprite.compteur_anim= -1 #On met -1 au conteur anim parce que plus tard, je rajoute 1 à mon résultat pour qu'il affiche l'image 0
     
    ####Saut####
    sprite.saut(plateformes) 
    
    ###mourir de chute
    if sprite.pos_y >1900:
        #annuler la run (Boucle)
        run = sprite.perdre_vie()
        
   
    #afficher les fonds d'écrans
    window.blit(background_image, (-(128+sprite.scroll/2) , 0)) #le /2 c'est pour qu ele deplacement du fond est lent et le 128 cêst pour que on decale le fond a droite (pour avoir les bouts plus estéthiques)

    
    for n in plateformes:
        for i in range (n.nb_blocs):
            window.blit(n.image,(n.pos_x + n.taille*i - sprite.scroll, n.pos_y))
            
   
    #appareance du sprite quand il saute
    if sprite.activation_saut==True:
        if sprite.orientation == "droite":
            window.blit(sprite.droite[1],(sprite.pos_x, sprite.pos_y))
        else:
            window.blit(sprite.gauche[1],(sprite.pos_x, sprite.pos_y))
    #appareance du sprite quand il court
    elif sprite.orientation == "droite":
        window.blit(sprite.droite[sprite.compteur_anim+1],(sprite.pos_x, sprite.pos_y)) #On rajoute +1 au conteur anim pour ne pas aficher la première image(car elle n'a pas de poussière)
        if (sprite.compteur_anim==1 or sprite.compteur_anim==3) and sprite.delay_anim==1:
            pygame.mixer.Sound.play (footsteps)
    elif sprite.orientation == "gauche":
        window.blit(sprite.gauche[sprite.compteur_anim+1],(sprite.pos_x, sprite.pos_y))
        if (sprite.compteur_anim==1 or sprite.compteur_anim==3) and sprite.delay_anim==1:
            pygame.mixer.Sound.play (footsteps)
        
    #Affichage des coeurs:
    for i in range (sprite.nb_vie):
         window.blit(coeur,(0+90*i,0))
    print(sprite.pos_x)
    
    pygame.display.update()
    
    
    
#death display

window.blit(game_over,(0, 0))
pygame.display.update()
time.sleep(2)

pygame.quit()