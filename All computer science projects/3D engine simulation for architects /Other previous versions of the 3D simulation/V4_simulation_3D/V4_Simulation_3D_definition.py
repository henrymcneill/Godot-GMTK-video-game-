import pygame
import math 
from pygame.locals import (K_LEFT, K_RIGHT,
                           K_w, K_a, K_d, K_s, K_SPACE)
    
def creation_murs(scene,liste_V,liste_H,serie):
    #Définir les mur!!!
        
    aj=0 #pour pas que le range soit décalé lorsqu'on ajoute le 1
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
        
    # print(liste_H)#se lie verticalement
    # print(liste_V)#se lie horizontalement 
    
    
    
def inputs_modifications(modif):
    
    keys = pygame.key.get_pressed()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            modif = False
        
    if keys[K_SPACE]==True:
        modif = False
    return modif

def murs_modificaion(serie,espace,liste_V,liste_H,screen):
    x, y = -500, -500
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos() 

    #Tracer les murs verticaux et horizontaux 
    for j in range (serie):
        for i in range (serie+1):
            if liste_V[i+((serie+1)*j)]:
                line = pygame.draw.line(screen,"black",[(espace)*i, (espace)*j],[(espace)*i,(espace)+(espace)*j],8)
                
                if line.collidepoint(x, y):
                    liste_V[i+((serie+1)*j)]=0
            else:
                line = pygame.draw.line(screen,"white",[(espace)*i, (espace)*j],[(espace)*i,(espace)+(espace)*j],8)
                if line.collidepoint(x, y):
                    liste_V[i+((serie+1)*j)]=1
            
    #verticale  
    for j in range (serie):
        for i in range (serie+1):
            if liste_H[i+((serie+1)*j)]:
                line = pygame.draw.line(screen,"black",[(espace)*j,(espace)*i],[(espace)+(espace)*j,(espace)*i],8)
                if line.collidepoint(x, y):
                    liste_H[i+((serie+1)*j)]=0
            else:
                line = pygame.draw.line(screen,"white",[(espace)*j,(espace)*i],[(espace)+(espace)*j,(espace)*i],8)

                if line.collidepoint(x, y):
                    liste_H[i+((serie+1)*j)]=1       
                    
    return (liste_V,liste_H)
  
    
def inputs_jeu(sprite_pos_x,sprite_pos_y,sprite_speed,angle_rayon):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            
    #prend en compte toutes les touches actuellement appuyees
    keys = pygame.key.get_pressed()
    
    #Aller à droite
    if keys[K_d]==True:
        sprite_pos_x = sprite_pos_x + sprite_speed
    #Aller à gauche 
    elif keys[K_a]==True:
        sprite_pos_x = sprite_pos_x - sprite_speed
    #Aller en haut
    if keys[K_w]==True:
        sprite_pos_y = sprite_pos_y - sprite_speed
    #Aller en bas
    elif keys[K_s]==True:
        sprite_pos_y = sprite_pos_y + sprite_speed
    
    #Changer l'angle
    #Horaire
    if keys[K_RIGHT]==True:
        angle_rayon += 2
    #Anti-horaire
    elif keys[K_LEFT]==True:
        angle_rayon -= 2
    
    if angle_rayon>=360:
        angle_rayon-=360
    elif angle_rayon<0:
        angle_rayon+=360
        
    return (sprite_pos_x,sprite_pos_y,angle_rayon)

def rayons(serie,espace,liste_V,liste_H,screen):
    #Tracer les murs verticaux et horizontaux 
    for j in range (serie):
        for i in range (serie+1):
            if liste_V[i+((serie+1)*j)]:
                pygame.draw.aaline(screen,"black",[(espace)*i, (espace)*j],[(espace)*i,(espace)+(espace)*j],3)
    #verticale  
    for j in range (serie):
        for i in range (serie+1):
            if liste_H[i+((serie+1)*j)]:
                pygame.draw.aaline(screen,"black",[(espace)*j,(espace)*i],[(espace)+(espace)*j,(espace)*i],3)
 
def collisions(angle_rayon,rayon,espace,liste_V,liste_H,sprite_pos_x,sprite_pos_y,screen):
    
    # Créer les rayons et collisions avec le mur 
    for angle_mtn in range (angle_rayon, angle_rayon +120, 4): 
        pygame.draw.aaline(screen,"black",[sprite_pos_x, sprite_pos_y],
                           [sprite_pos_x + rayon*math.cos(math.radians(angle_mtn)),
                            sprite_pos_y + rayon*math.sin(math.radians(angle_mtn))],5)
        
        if angle_mtn>=360:
            angle_mtn-=360
        elif angle_mtn<0:
            angle_mtn+=360
                  

                
        distance_sprite_murhorizontal= 100000
        distance_sprite_murvertical= 100000
        mur_vertical_collision=False
        mur_horizontal_collision=False
        
        #detection des murs verticaux
        if angle_mtn < 90 or angle_mtn > 270:
            Bx= int(sprite_pos_x/espace)*espace + espace
            By=sprite_pos_y + (sprite_pos_x-Bx)* math.tan(math.radians(-angle_mtn))
            Nb_C= int(Bx/espace) -1
            Ya= espace*math.tan(math.radians(angle_mtn))
            while Nb_C <=3:
                Nb_R = int(By/espace)
                
                if Nb_R>=0 and Nb_R<4 and liste_V[Nb_R*5+Nb_C+1]==1:
                    distance_sprite_murvertical= (((sprite_pos_x-(Nb_C*(espace)+ espace))**2)+((sprite_pos_y- By)**2))**(1/2)
                    Nb_C_sauvegarde = Nb_C
                    By_sauvegarde= By
                    mur_vertical_collision = True
                    Nb_C=4
                    
                Nb_C+=1
                By += Ya
                
        elif angle_mtn !=90 and 270:
            Bx= int(sprite_pos_x/espace)*espace 
            By=sprite_pos_y + (sprite_pos_x-Bx)* math.tan(math.radians(-angle_mtn))
            Nb_C= int(Bx/espace) -1
            Ya= espace*math.tan(math.radians(angle_mtn))
            while Nb_C >= -1:
                Nb_R = int(By/espace)
                
                if Nb_R>=0 and Nb_R<4 and liste_V[Nb_R*5+Nb_C+1]==1:
                    distance_sprite_murvertical= (((sprite_pos_x-(Nb_C*(espace)+ espace))**2)+((sprite_pos_y- By)**2))**(1/2)
                    Nb_C_sauvegarde = Nb_C
                    By_sauvegarde= By
                    mur_vertical_collision = True
                    Nb_C=-1
                    
                Nb_C-=1
                By -= Ya
            
        
        #detection des murs horizontaux
        if angle_mtn>180:
            dis_mur= sprite_pos_y%(espace)
            Nb_R=int(sprite_pos_y/(espace))
            Xm= -round(dis_mur/math.tan(math.radians(angle_mtn)),2) + sprite_pos_x
            Xa= round(espace/math.tan(math.radians(360-angle_mtn)),2)
            
            while Nb_R>=0:
                Nb_C= int((Xm)/(espace))
                            
                if Nb_C>=0 and Nb_C<4 and liste_H[Nb_C*5+Nb_R]==1:
                    distance_sprite_murhorizontal= (((sprite_pos_x-Xm)**2)+((sprite_pos_y- (Nb_R*(espace)))**2))**(1/2)
                    mur_horizontal_collision=True
                    
                    if distance_sprite_murhorizontal <= distance_sprite_murvertical:
                        pygame.draw.circle(screen, "black",[Xm, Nb_R*(espace)],5)
                    elif mur_vertical_collision == True:
                        pygame.draw.circle(screen, "black",[Nb_C_sauvegarde*(espace)+ espace,By_sauvegarde],5)

                    Nb_R=-1
                Nb_R-=1
                Xm+= Xa
            
        elif angle_mtn!=0:             
            dis_mur= (espace)-sprite_pos_y%(espace)
            Nb_R=int(sprite_pos_y/(espace))
            Xm= round(dis_mur/math.tan(math.radians(angle_mtn)),2) + sprite_pos_x
            Xa= round(espace/math.tan(math.radians(360-angle_mtn)),2)
            
            while Nb_R<=3:
                Nb_C= int((Xm)/(espace))
                            
                if Nb_C>=0 and Nb_C<4 and liste_H[Nb_C*5+Nb_R+1]==1:
                    distance_sprite_murhorizontal= (((sprite_pos_x-Xm)**2)+((sprite_pos_y- (Nb_R*(espace)+espace))**2))**(1/2)
                    mur_horizontal_collision=True
                    
                    if distance_sprite_murhorizontal <= distance_sprite_murvertical:
                        pygame.draw.circle(screen, "black",[Xm, Nb_R*(espace)+espace],5)
                    elif mur_vertical_collision == True:
                        pygame.draw.circle(screen, "black",[Nb_C_sauvegarde*(espace)+ espace,By_sauvegarde],5)
                    
                    Nb_R=5
                Nb_R+=1
                Xm-= Xa       
        
        if mur_vertical_collision == True and mur_horizontal_collision==False:   #pour afficher le point si les deux options ne fonctionnent pas 
            pygame.draw.circle(screen, "black",[Nb_C_sauvegarde*(espace)+ espace,By_sauvegarde],5)
        

            
            


