import pygame
import math
#Import required Image library
from PIL import Image, ImageFilter #pour importer et flouter l'image
import imageio.v3 as imageio #pour identifier le RGB d'un pixel de l'image
import numpy as np
from pygame.locals import (K_w, K_a, K_d, K_s, K_p,K_l,K_o,K_k, K_SPACE,K_ESCAPE)

def blur_image():
    #Open existing image
    image = Image.open('Image10.png').convert('RGB')
    #resize image
    image = image.resize((1500, 1500))
    blurImage = image.filter(ImageFilter.BLUR)
    blurImage = blurImage.resize((600, 600))
    blurImage.save('blurImage.png')
    

def scan_image(serie,espace):
    #création de la scène et des murs#
    
    scene= []
    for i in range (serie*serie):
        scene.append(0)
    
    blurImage = imageio.imread('blurImage.png')
    x= int(espace/2)
    y= int(espace/2)
    
    #listes des centres de tous les carrés
    for i in range (serie):
        for j in range (serie):
            #il faut que RGB soit plus petit que 96 pour que ca tende vers du noir
            if (int(blurImage[y,x,0])+int(blurImage[y,x,1])+int(blurImage[y,x,2])) <= 350:
                scene [(i*serie) + j] =1
            x+= int(espace) 
        x= int(espace/2)
        y+= int(espace)
    return (scene)
    

def creation_murs(scene,liste_V,liste_H,serie):
    
    aj=0 #pour pas que le range soit décalé lorsqu'on ajoute le 1
    #Verticale
    for i in range (len(scene)):
        if liste_V[i+aj] ==0 and scene[i]==1:
            liste_V[i+aj]= 1
            
        if (i)%(serie)==0 and i !=0:
            liste_V[i+aj]= 1
            liste_V.append(1)
            aj+=1 #pour pas que le range soit décalé lorsqu'on ajoute le 1
            
        liste_V.append(scene[i])
    liste_V [len(liste_V)-1]=1
    
    
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
    liste_H [len(liste_H)-1]=1
    
    # print(liste_H)#se lie verticalement
    # print(liste_V)#se lie horizontalement 
    
    
    
def interactions_utilisateur(modif):
    
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
            if liste_V[i+((serie+1)*j)]==1:
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
            if liste_H[i+((serie+1)*j)]==1:
                line = pygame.draw.line(screen,"black",[(espace)*j,(espace)*i],[(espace)+(espace)*j,(espace)*i],8)
                if line.collidepoint(x, y):
                    liste_H[i+((serie+1)*j)]=0

            else:
                line = pygame.draw.line(screen,"white",[(espace)*j,(espace)*i],[(espace)+(espace)*j,(espace)*i],8)
                if line.collidepoint(x, y):
                    liste_H[i+((serie+1)*j)]=1       
                    
    return (liste_V,liste_H)
  
    
def création_sprite_2D(sprite_pos_x,sprite_pos_y,sprite_speed,angle_rayon,distance_écran_et_hauteur_mur,screen):
    run= True
    
    #prend en compte toutes les touches actuellement appuyees
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if keys[K_ESCAPE]==True:
            run = False
            
    if keys[K_p]==True:
        sprite_speed = sprite_speed*1.2
    elif keys[K_l]==True:
        sprite_speed = sprite_speed/1.2
    
    if keys[K_o]==True:
        distance_écran_et_hauteur_mur = distance_écran_et_hauteur_mur*1.2
    elif keys[K_k]==True:
        distance_écran_et_hauteur_mur = distance_écran_et_hauteur_mur/1.2
    
    #Changer l'angle
    delta_x  = pygame.mouse.get_rel()
    
    pygame.mouse.set_pos([600, 300])
    pygame.mouse.set_visible(False)
    
    if delta_x[0]>0:
        angle_rayon += 2*delta_x[0]
    #Anti-horaire
    elif delta_x[0]<0:
        angle_rayon += 2*delta_x[0]
    
    if angle_rayon>=3600:
        angle_rayon-=3600
    elif angle_rayon<0:
        angle_rayon+=3600
        
    
    #recalculer l'angle reel de notre champs de vision, sinon le math.radians ne fonctionne pas avec des degrés trop haut
    angle_reel=(angle_rayon+600)/10
    if angle_reel>=360:
        angle_reel-=360
    elif angle_reel<0:
        angle_reel+=360
        
    #Aller en haut        
    if keys[K_w]==True:
        sprite_pos_x += sprite_speed* math.cos(math.radians(angle_reel))
        sprite_pos_y += sprite_speed* math.sin(math.radians(angle_reel))
    #Aller en bas
    elif keys[K_s]==True:
        sprite_pos_x -= sprite_speed* math.cos(math.radians(angle_reel))
        sprite_pos_y -= sprite_speed* math.sin(math.radians(angle_reel))
    #Aller à droite
    elif keys[K_d]==True:
        sprite_pos_x += sprite_speed* math.cos(math.radians(angle_reel+90))
        sprite_pos_y += sprite_speed* math.sin(math.radians(angle_reel+60))
    #Aller à gauche 
    elif keys[K_a]==True:
        sprite_pos_x += sprite_speed* math.cos(math.radians(angle_reel-90))
        sprite_pos_y += sprite_speed* math.sin(math.radians(angle_reel-90))
    

            
    return (sprite_pos_x,sprite_pos_y,angle_rayon, sprite_speed, distance_écran_et_hauteur_mur,run)

def affichage_murs_2D (serie,espace,liste_V,liste_H,screen):
    #Tracer les murs verticaux et horizontaux 
    for j in range (serie):
        for i in range (serie+1):
            if liste_V[i+((serie+1)*j)]:
                pygame.draw.aaline(screen,"black",[((espace)*i)/3, ((espace)*j)/3],[((espace)*i)/3,((espace)+(espace)*j)/3],3)
    #verticale  
    for j in range (serie):
        for i in range (serie+1):
            if liste_H[i+((serie+1)*j)]:
                pygame.draw.aaline(screen,"black",[((espace)*j)/3,((espace)*i)/3],[((espace)+(espace)*j)/3,((espace)*i)/3],3)
 
def collisions_affichage_3D(angle_rayon,rayon,espace,liste_V,liste_H,sprite_pos_x,sprite_pos_y,serie,beta_fisheye,distance_écran_et_hauteur_mur,screen):
      
    # Créer les rayons et collisions avec le mur   
    for angle_mtn in range (angle_rayon, angle_rayon +1200, 1):
        
        angle_mtn_sauvegarde= angle_mtn -angle_rayon
        angle_mtn= angle_mtn/10
        
        if angle_mtn>=360:
            angle_mtn-=360
        elif angle_mtn<0:
            angle_mtn+=360
        
        distance_sprite_murhorizontal= 100000
        distance_sprite_murvertical= 100000
        mur_vertical_collision=False
        mur_horizontal_collision=False
        
        #detection des murs verticaux
        Ya= espace*math.tan(math.radians(angle_mtn))
        if angle_mtn < 90 or angle_mtn > 270:
            Bx= int(sprite_pos_x/espace)*espace + espace
            By=sprite_pos_y + (sprite_pos_x-Bx)* math.tan(math.radians(-angle_mtn))
            Nb_C= int(Bx/espace) -1
            
            while Nb_C <= (serie-1):
                Nb_R = int(By/espace)
                
                if 0<=Nb_R<serie and liste_V[Nb_R*(serie+1)+Nb_C+1]!=0:
                    distance_sprite_murvertical= (((sprite_pos_x-(Nb_C*(espace)+ espace))**2)+((sprite_pos_y- By)**2))**(1/2)
                    Nb_C_sauvegarde = Nb_C
                    By_sauvegarde= By
                    #Trouver alpha pour le "fishbowl effect"
                    if angle_mtn > 270:
                        alpha_mur_vertical= beta_fisheye
                    else:
                        alpha_mur_vertical= -beta_fisheye
                        
                    mur_vertical_collision = True
                    Nb_C= serie + 1
                    
                Nb_C+=1
                By += Ya     
        elif angle_mtn !=90 and 270:
            Bx= int(sprite_pos_x/espace)*espace 
            By=sprite_pos_y + (sprite_pos_x-Bx)* math.tan(math.radians(-angle_mtn))
            Nb_C= int(Bx/espace) -1
            
            while Nb_C >= -1:
                Nb_R = int(By/espace)
                
                if 0<=Nb_R<serie and liste_V[Nb_R*(serie+1)+Nb_C+1]!=0:
                    distance_sprite_murvertical= (((sprite_pos_x-(Nb_C*(espace)+ espace))**2)+((sprite_pos_y- By)**2))**(1/2)
                    Nb_C_sauvegarde = Nb_C
                    By_sauvegarde= By
                    #Trouver alpha pour le "fishbowl effect"
                    if angle_mtn < 180:
                        alpha_mur_vertical= beta_fisheye
                    else:
                        alpha_mur_vertical= -beta_fisheye
                    mur_vertical_collision = True
                    Nb_C=-1
                    
                Nb_C-=1
                By -= Ya 
        
        #detection des murs horizontaux
        Nb_R=int(sprite_pos_y/(espace))
        Xa= round(espace/math.tan(math.radians(360-angle_mtn)),2)
        
        if angle_mtn>180:
            dis_mur= sprite_pos_y%(espace)
            Xm= -round(dis_mur/math.tan(math.radians(angle_mtn)),2) + sprite_pos_x
            
            while Nb_R>=0:
                Nb_C= int((Xm)/(espace))
                            
                if 0<=Nb_C<serie and liste_H[Nb_C*(serie+1)+Nb_R]!=0:
                    distance_sprite_murhorizontal= (((sprite_pos_x-Xm)**2)+((sprite_pos_y- (Nb_R*(espace)))**2))**(1/2)
                    
                    
                    if distance_sprite_murhorizontal <= distance_sprite_murvertical:
                        mur_horizontal_collision=True
                        
                        #Trouver alpha pour le "fishbowl effect"
                        if angle_mtn < 270:
                            alpha_mur_horizontal= beta_fisheye
                        else:
                            alpha_mur_horizontal= -beta_fisheye
                            
                        distance_correcte= (distance_sprite_murhorizontal)*math.cos(math.radians(alpha_mur_horizontal))
                        if distance_correcte==0:
                            distance_correcte=0.001
                            
                        hauteur_mur = (distance_écran_et_hauteur_mur/distance_correcte)/2
                        pygame.draw.aaline(screen,"brown",[angle_mtn_sauvegarde,300+hauteur_mur],[angle_mtn_sauvegarde,300-hauteur_mur],1)
                        
                        pygame.draw.aaline(screen,"red",[sprite_pos_x/3, sprite_pos_y/3],[Xm/3, (Nb_R*(espace))/3],3)
                        pygame.draw.circle(screen, "black",[Xm/3, (Nb_R*(espace))/3],3)

                    Nb_R=-1
                Nb_R-=1
                Xm+= Xa
            
        elif angle_mtn!=0:             
            dis_mur= (espace)-sprite_pos_y%(espace)
            Xm= round(dis_mur/math.tan(math.radians(angle_mtn)),2) + sprite_pos_x
            
            while Nb_R<= (serie-1):
                Nb_C= int((Xm)/(espace))
                            
                if 0<=Nb_C<serie and liste_H[Nb_C*(serie+1)+Nb_R+1]!=0:
                    distance_sprite_murhorizontal= (((sprite_pos_x-Xm)**2)+((sprite_pos_y- (Nb_R*(espace)+espace))**2))**(1/2)
                    
                    
                    if distance_sprite_murhorizontal <= distance_sprite_murvertical:
                        mur_horizontal_collision=True
                        #Trouver alpha pour le "fishbowl effect"
                        if angle_mtn < 90:
                            alpha_mur_horizontal= beta_fisheye
                        else:
                            alpha_mur_horizontal= -beta_fisheye
                        distance_correcte= (distance_sprite_murhorizontal)*math.cos(math.radians(alpha_mur_horizontal))
                        if distance_correcte==0:
                            distance_correcte=0.001
                        hauteur_mur = (distance_écran_et_hauteur_mur/distance_correcte)/2
                        pygame.draw.aaline(screen,"brown",[angle_mtn_sauvegarde,300+hauteur_mur],[angle_mtn_sauvegarde,300-hauteur_mur],1)
                        pygame.draw.aaline(screen,"red",[sprite_pos_x/3, sprite_pos_y/3],[Xm/3, (Nb_R*(espace)+espace)/3],3)
                        pygame.draw.circle(screen, "black",[Xm/3, (Nb_R*(espace)+espace)/3],3)
                    Nb_R=serie + 1
                Nb_R+=1
                Xm-= Xa       
        
        if mur_vertical_collision == True and mur_horizontal_collision==False:   #pour afficher le point si les deux options ne fonctionnent pas 
                        
            distance_correcte= (distance_sprite_murvertical)*math.cos(math.radians(alpha_mur_vertical))
            if distance_correcte==0:
                distance_correcte=0.001
            hauteur_mur = (distance_écran_et_hauteur_mur/distance_correcte/2)
            pygame.draw.aaline(screen,"brown",[angle_mtn_sauvegarde,300+hauteur_mur],[angle_mtn_sauvegarde,300-hauteur_mur],1)
            pygame.draw.aaline(screen,"red",[sprite_pos_x/3, sprite_pos_y/3],[(Nb_C_sauvegarde*(espace)+ espace)/3,By_sauvegarde/3],3)
            pygame.draw.circle(screen, "black",[(Nb_C_sauvegarde*(espace)+ espace)/3,By_sauvegarde/3],3)
            
        pygame.draw.circle(screen, "black",[sprite_pos_x/3, sprite_pos_y/3],3)
