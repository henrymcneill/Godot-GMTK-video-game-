import pygame
import math 
from pygame.locals import (K_LEFT, K_RIGHT,
                           K_w, K_a, K_d, K_s, K_SPACE)

#demarrage de pygame
pygame.init()

#titre de la fenetre de jeu
pygame.display.set_caption('2D')



#importation des images dans le programme
#le .convert_alpha() convertit l'image dans le meme format de pixel
#que la fenetre pygame

#déplacement de sprite
sprite_pos_x = 350
sprite_pos_y = 350
sprite_speed = 8

#créer un rayon
angle_rayon = -60
rayon = 900
##################### JEU ##############################
run=True
#frames per second
fps = 30
clock = pygame.time.Clock()

size=[1200,800]
screen = pygame.display.set_mode(size)

scene= []

for i in range(100):
    scene.append (1)

liste_V=[1] #Verticale
liste_H=[1] #mur du jeu horizontal
#On garde le 1 pour que la séquence d'après fonctionne


serie=int(len(scene)**(1/2)) #nb de bloc (de la liste scene) par coloone/rangée
espace= 600/serie

#Définir les mur!!!

aj=0 #pour pas que le range soit décalé lorsqu'on ajoute le 1
#Verticale
for i in range (len(scene)):
    if liste_V[i+aj] !=1 and scene[i]==1:
        liste_V[i+aj]= 1
        
    if (i)%(serie)==0 and i !=0:
        liste_V[i+aj]= 1
        liste_V.append(1)
        aj+=1 #pour pas que le range soit décalé lorsqu'on ajoute le 1
        
    liste_V.append(scene[i])
    
aj=0
#Horizontale
for j in range (serie):
    for i in range (serie):
        if liste_H[i+aj+(j*serie)] !=1 and scene[j+(serie*i)]==1:
            liste_H[i+aj+(j*serie)]= 1
            
        if (i)%(serie)==0 and j !=0:
            liste_H[i+aj+(j*serie)]= 1
            liste_H.append(1)
            aj+=1 #pour pas que le range soit décalé lorsqu'on ajoute le 1
        liste_H.append(scene[j+(serie*i)])
         

# print(liste_V)#se lie horizontalement 
# print(liste_H)#se lie verticalement 




#début du jeu
while run==True:
    clock.tick(fps)
    #quitter??:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
                
    ############### APPUIS TOUCHES CONTINUS ####################
            
    #prend en compte toutes les touches actuellement appuyees
    keys = pygame.key.get_pressed()
    
    
    
    
    if keys[K_w]==True:
        sprite_pos_y = sprite_pos_y - sprite_speed # Déplacement vers le haut de la fenêtre
    elif keys[K_s]==True:
        sprite_pos_y = sprite_pos_y + sprite_speed # Déplacement vers le bas de la fenêtre
    if keys[K_d]==True:
        sprite_pos_x = sprite_pos_x + sprite_speed # Déplacement vers la droite de la fenêtre
    elif keys[K_a]==True:
        sprite_pos_x = sprite_pos_x - sprite_speed # Déplacement vers la gauche de la fenêtre
    
    
    #afficher les fonds d'écrans
    screen.fill("white")
    #afficher les lignes
    #verticale
    for j in range (serie):
        for i in range (serie+1):
            if liste_V[i+((serie+1)*j)]:
                pygame.draw.aaline(screen,"black",[(espace)*i, (espace)*j],[(espace)*i,(espace)+(espace)*j],3)
    #verticale  
    for j in range (serie):
        for i in range (serie+1):
            if liste_H[i+((serie+1)*j)]:
                pygame.draw.aaline(screen,"black",[(espace)*j,(espace)*i],[(espace)+(espace)*j,(espace)*i],3)

#Rayons
#Changer l'angle
    #Aller à droite
    if keys[K_RIGHT]==True:
        angle_rayon += 2
        
    #Aller à gauche 
    elif keys[K_LEFT]==True:
        angle_rayon -= 2
    
# Créer les rayons et collisions avec le mur 
    for angle_mtn in range (angle_rayon, 61+angle_rayon, 4): #on rajoute un +1 pour qu'il y est jusqu'a l'angle 60
        pygame.draw.aaline(screen,"black",[sprite_pos_x, sprite_pos_y],[sprite_pos_x + rayon*math.cos(math.radians(angle_mtn)), sprite_pos_y + rayon*math.sin(math.radians(angle_mtn))],5)
        
        if angle_mtn>=360:
            angle_mtn-=360
        elif angle_mtn<0:
            angle_mtn+=360
        
        #detection des murs horizontaux
        if angle_mtn>180:
            dis_mur= sprite_pos_y%(espace)
            Nb_R=int(sprite_pos_y/(espace))
            Xm= -round(dis_mur/math.tan(math.radians(angle_mtn)),2) + sprite_pos_x
            Nb_C= int(Xm/(espace))
            Xa= round(espace/math.tan(math.radians(360-angle_mtn)),2)
                
            while Nb_R>=0:
                Nb_C= int((Xm)/(espace))
                            
                if Nb_C>=0 and Nb_C<4 and liste_H[Nb_C*5+Nb_R]==1:
                    pygame.draw.circle(screen, "black",[Xm, Nb_R*(espace)],5)
                    Nb_R=-1
                Nb_R-=1
                Xm+= Xa
            
        elif angle_mtn!=0:             
            dis_mur= (espace)-sprite_pos_y%(espace)
            Nb_R=int(sprite_pos_y/(espace))
            Xm= round(dis_mur/math.tan(math.radians(angle_mtn)),2) + sprite_pos_x
            Nb_C= int(Xm/(espace))
            Xa= round(espace/math.tan(math.radians(360-angle_mtn)),2)
            
            while Nb_R<=4:
                Nb_C= int((Xm)/(espace))
                            
                if Nb_C>=0 and Nb_C<4 and liste_H[Nb_C*5+Nb_R+1]==1:
                    pygame.draw.circle(screen, "black",[Xm, Nb_R*(espace)+(espace)],5)
                    Nb_R=5
                Nb_R+=1
                Xm-= Xa
                    
                    
        #detection des murs verticaux
        if angle_mtn < 90 or angle_mtn > 270:
            Bx= int(sprite_pos_x/espace)*espace + espace
            By=sprite_pos_y + (sprite_pos_x-Bx)* math.tan(math.radians(angle_mtn))
            Nb_R = int(By/espace)
            Nb_C= int(Bx/espace)
            Ya= espace*math.tan(math.radians(angle_mtn))
            
            
            
#             while Nb_R>=0:
#                 Nb_C= int((Xm)/(espace))
#                             
#                 if Nb_C>=0 and Nb_C<4 and liste_H[Nb_C*5+Nb_R]==1:
#                     pygame.draw.circle(screen, "black",[Xm, Nb_R*(espace)],5)
#                     Nb_R=-1
#                 Nb_R-=1
#                 Xm+= Xa
            
        

#le point
    pygame.draw.circle(screen, "black",[sprite_pos_x, sprite_pos_y],5)
    
    
    pygame.display.update()
pygame.quit()
