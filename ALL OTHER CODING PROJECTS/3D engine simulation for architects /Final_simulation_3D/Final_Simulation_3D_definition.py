# Travail de maturité genevoise - Collège Calvin 2024/2025 
# Travail: Coder une simulation tridimensionnelle d’une chambre, de la conception théorique à la programmation 
# Elève: Henry MC NEILL [groupe 407] - Maître accompagnant: Eric VON AARBURG 


### Fichier ayant toutes les définitions du programme ###

## Importer les librairies ##
import pygame
#librairie pour ouvrir une fenêtre et l'anime

from pygame.locals import (K_w, K_a, K_d, K_s, K_p, K_l, K_o, K_k, K_SPACE, K_ESCAPE, K_RETURN)
#librairie pour que le programme puisse répondre à l'utilisation des touches

import math
#librairie pour des opérations mathématiques (ex: sinus, cosinus, tangente, etc)

from PIL import Image, ImageFilter
#librairie pour modifier une image

import imageio.v3 as imageio
#librairie pour identifier le RGB d'un pixel 

## Listes des definitions ##
def blur_image(): # flouter l'image

    image = Image.open('Image11.png').convert('RGB') # importer l'image
    
    image = image.resize((1500, 1500)) # redimensionner image
    
    blurImage = image.filter(ImageFilter.BLUR) # flouter l'image
    
    blurImage = blurImage.resize((600, 600)) # redimensionner l'image
    
    blurImage.save('blurImage.png') # sauvegarder l'image
    

def scan_image(Nb_murs,longueur_murs): # scanner l'image et en définir le plan de la salle sous forme de liste
    ## SIGNIFICATION:
    ## 0 --> bloc de mur désactivé
    ## 1 --> bloc de mur activé
    
    
    bloc_liste= [] # liste pour définir le plan de la salle
    
    #boucle pour remplir la liste selon le nombre de murs:
    for i in range (Nb_murs*Nb_murs):
        bloc_liste.append(0) 
    
    blurImage = imageio.imread('blurImage.png') # importer l'image
    x= int(longueur_murs/2) # position horizontale du pixel que nous allons analyser
    y= int(longueur_murs/2) # position verticale du pixel que nous allons analyser
    
    #boucle pour scanner les pixels de chaque bloc de murs:
    for rangée in range (Nb_murs):
        # n-ième rangée
        for colonne in range (Nb_murs):
            # n-ième colonne
            
            if (int(blurImage[y,x,0])+int(blurImage[y,x,1])+int(blurImage[y,x,2])) <= 350:
                # il faut que le RGB du pixel soit plus petit que 96 pour considérer qu'il est noir
                
                bloc_liste [(rangée*Nb_murs) + colonne] =1
                # définir le bloc de mur comme actif
                
            x += int(longueur_murs) # décaler la position horizontale 
        x = int(longueur_murs/2) # redéfinir la position horizontale 
        y += int(longueur_murs) # décaler la position verticale
        
    return (bloc_liste) 
    

def creation_murs(Nb_murs,bloc_liste): # créer des listes différentes pour les murs horizontaux et verticaux
    ## REMARQUE: Pour garder la salle close/fermée, nous garderons les murs au bord de la salle activés
    
    ## la liste horizontale (liste_H) va se lire de haut en bas, colonne par colonne
    ## la liste verticale (liste_V) va se lire de gauche à droite, rangée par rangée
    
    ## SIGNIFICATION:
    ## 0 --> mur désactivé
    ## 1 --> mur activé
    
    
    liste_V = [1] # liste pour les murs verticaux 
    liste_H = [1] # liste pour les murs horizontaux 
    # nous débutons avec le premier mur déja activé, car il sera de tous les cas activé


    corriger_décalage = 0
    # corriger le décalage de la liste engendré par l'ajout du un mur au début de chaque rangée
    
    # définir la liste pour les murs verticaux:
    for n_ième_bloc in range (len(bloc_liste)):
        
        # Activer le mur du bloc d'avant, si le bloc actuel est activé
        if bloc_liste[n_ième_bloc]==1:
            liste_V[n_ième_bloc+corriger_décalage]= 1 
        
        # Si nous nous retrouvons au début d'une rangée, sans que nous sommes au début du programme
        if (n_ième_bloc)%(Nb_murs)== 0 and n_ième_bloc !=0 :
            liste_V[n_ième_bloc+corriger_décalage]= 1 # activer le mur de fin de rangée (celle précédente)
            liste_V.append(1) # ajouter un mur pour le début de la rangée
            corriger_décalage += 1
            # corriger le décalage de la liste engendré par l'ajout du mur au début de chaque rangée
            
        liste_V.append(bloc_liste[n_ième_bloc])
        # ajouter un mur activé/désactivé selon le bloc 
        
    liste_V [len(liste_V)-1] = 1 # activer le dernier mur de la liste, car il se trouve au bord
    
    
    
    ## REMARQUE: Comme les murs horizontaux vont se lire de haut en bas (colonne par colonne), nous devons définir la liste horizontale différemment que la liste verticale  
    
    corriger_décalage = 0
    # corriger le décalage de la liste engendré par l'ajout du un mur au début de chaque rangée
    
    # définir la liste pour les murs horizontaux:
    for n_ième_C in range (Nb_murs):
        for n_ième_R in range (Nb_murs):
            
            # Activer le mur du bloc d'avant, si le bloc actuel est activé
            if bloc_liste[(Nb_murs*n_ième_R)+ n_ième_C]==1:
                liste_H[n_ième_R+corriger_décalage+(n_ième_C*Nb_murs)]= 1
            
            # Si nous nous retrouvons au début d'une colonne, sans que nous sommes au début du programme   
            if (n_ième_R)%(Nb_murs)==0 and n_ième_C !=0:
                liste_H[n_ième_R+corriger_décalage+(n_ième_C*Nb_murs)]= 1 # activer le mur de fin de colonne (celle précédente)
                liste_H.append(1) # ajouter un mur pour le début de la colonne
                corriger_décalage+=1
                # corriger le décalage de la liste engendré par l'ajout du mur au début de chaque colonne
    
            liste_H.append(bloc_liste[n_ième_C+(Nb_murs*n_ième_R)])
            # ajouter un mur activé/désactivé selon le bloc
            
    liste_H [len(liste_H)-1]=1 # activer le dernier mur de la liste, car il se trouve au bord
    
    
    return (liste_H,liste_V) 
    

def murs_modification(Nb_murs,longueur_murs,liste_H,liste_V,run,screen): # programme de la fenêtre d'accueil
    # tracer les murs horizontaux et verticaux, modifier leur texture et si l'utilisateur veut quitter la fenêtre d'accueil
    
    ## SIGNIFICATION:
    ## 0 --> mur désactivé
    ## 1 --> mur activé avec texture numéro 1 (de base)
    ## 2 --> mur activé avec texture numéro 2
    ## 3 --> mur activé avec texture numéro 3
    
    keys = pygame.key.get_pressed() # prend en compte toutes les touches appuyées
    
    x, y = -500, -500 # définir la position horizontale et verticale de la souris 
    for event in pygame.event.get():
        
        # Si la souris est clické, enregistrer sa position horizontale et verticale:
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
        
        # Si l'utilisateur veut quitter la fenêtre d'acceuil 
        if keys[K_SPACE]==True or keys[K_RETURN]==True or keys[K_ESCAPE]==True:
            run = False
    
    # Tracer les murs horizontaux et modifier leur texture:
    for n_ième_C in range (Nb_murs):
        for n_ième_R in range (Nb_murs+1):
            # Si le mur est activé avec texture numéro 1:
            if liste_H[((Nb_murs+1)*n_ième_C)+n_ième_R]==1:
                
                line = pygame.draw.line(screen,"black",[(longueur_murs)*n_ième_C,(longueur_murs)*n_ième_R],
                                        [(longueur_murs)+(longueur_murs)*n_ième_C,(longueur_murs)*n_ième_R],8)
                # affichage du mur en 2D
                
                # Si le lieu clické est un point de la droite tracée:
                if line.collidepoint(x, y):
                    liste_H[((Nb_murs+1)*n_ième_C)+n_ième_R]=2
                    # changer la texture du mur au numéro 2:
                    
            # Si le mur est activé avec texture numéro 2:
            elif liste_H[((Nb_murs+1)*n_ième_C)+n_ième_R]==2:
                
                line = pygame.draw.line(screen,"blue",[(longueur_murs)*n_ième_C,(longueur_murs)*n_ième_R],
                                        [(longueur_murs)+(longueur_murs)*n_ième_C,(longueur_murs)*n_ième_R],8)
                # affichage du mur en 2D
                
                # Si le lieu clické est un point de la droite tracée:
                if line.collidepoint(x, y):
                    
                    liste_H[((Nb_murs+1)*n_ième_C)+n_ième_R]=3
                    # changer la texture du mur au numéro 3:
                    
            # Si le mur est activé avec texture numéro 3:
            elif liste_H[((Nb_murs+1)*n_ième_C)+n_ième_R]==3:
                
                line = pygame.draw.line(screen,"purple",[(longueur_murs)*n_ième_C,(longueur_murs)*n_ième_R],
                                        [(longueur_murs)+(longueur_murs)*n_ième_C,(longueur_murs)*n_ième_R],8)
                # affichage du mur en 2D
                
                # Si le lieu clické est un point de la droite tracée:
                if line.collidepoint(x, y):
                    
                    liste_H[((Nb_murs+1)*n_ième_C)+n_ième_R]=0
                    # déactiver le mur:
                    
            # Si le mur est désactivé:
            else:
                
                line = pygame.draw.line(screen,"white",[(longueur_murs)*n_ième_C,(longueur_murs)*n_ième_R],
                                        [(longueur_murs)+(longueur_murs)*n_ième_C,(longueur_murs)*n_ième_R],8)
                # affichage du mur en 2D
                
                # Si le lieu clické est un point de la droite tracée:
                if line.collidepoint(x, y):
                    
                    liste_H[n_ième_R+((Nb_murs+1)*n_ième_C)]=1
                    # changer la texture du mur au numéro 1:
                    
            
    # Tracer les murs verticaux et modifier leur texture:
    for n_ième_R in range (Nb_murs): 
        for n_ième_C in range (Nb_murs+1):
            # Si le mur est activé avec texture numéro 1:
            if liste_V[((Nb_murs+1)*n_ième_R)+n_ième_C]==1:
                
                line = pygame.draw.line(screen,"black",[(longueur_murs)*n_ième_C, (longueur_murs)*n_ième_R],
                                        [(longueur_murs)*n_ième_C,(longueur_murs)+(longueur_murs)*n_ième_R],8)
                # affichage du mur en 2D
                
                # Si le lieu clické est un point de la droite tracée:
                if line.collidepoint(x, y):
                    
                    liste_V[((Nb_murs+1)*n_ième_R)+n_ième_C]=2
                    # changer la texture du mur au numéro 2:
                    
            # Si le mur est activé avec texture numéro 2:
            elif liste_V[((Nb_murs+1)*n_ième_R)+n_ième_C]==2:
                
                line = pygame.draw.line(screen,"blue",[(longueur_murs)*n_ième_C, (longueur_murs)*n_ième_R],
                                        [(longueur_murs)*n_ième_C,(longueur_murs)+(longueur_murs)*n_ième_R],8)
                # affichage du mur en 2D
                
                # Si le lieu clické est un point de la droite tracée:
                if line.collidepoint(x, y):
                    
                    liste_V[((Nb_murs+1)*n_ième_R)+n_ième_C]=3
                    # changer la texture du mur au numéro 3:
            
            # Si le mur est activé avec texture numéro 3:
            elif liste_V[((Nb_murs+1)*n_ième_R)+n_ième_C]==3:
                
                line = pygame.draw.line(screen,"purple",[(longueur_murs)*n_ième_C, (longueur_murs)*n_ième_R],
                                        [(longueur_murs)*n_ième_C,(longueur_murs)+(longueur_murs)*n_ième_R],8)
                # affichage du mur en 2D
                
                # Si le lieu clické est un point de la droite tracée:
                if line.collidepoint(x, y):
                    
                    liste_V[((Nb_murs+1)*n_ième_R)+n_ième_C]=0
                    # désactiver le mur:
            
            # Si le mur est désactivé:
            else:
                
                line = pygame.draw.line(screen,"white",[(longueur_murs)*n_ième_C, (longueur_murs)*n_ième_R],
                                        [(longueur_murs)*n_ième_C,(longueur_murs)+(longueur_murs)*n_ième_R],8)
                # affichage du mur en 2D
                
                # Si le lieu clické est un point de la droite tracée:
                if line.collidepoint(x, y):
                    
                    liste_V[((Nb_murs+1)*n_ième_R)+n_ième_C]=1
                    # changer la texture du mur au numéro 1:
    
    
    return (liste_H,liste_V,run)
    
def background_3D(screen):
    # dessiner le sol et le plafond composants l'arrière plan
    
    # Version sans dégradé:
    screen.fill((210,210,190)) # couleur de l'arrière plan
    pygame.draw.rect(screen, (128,128,128), pygame.Rect(0, 0, 1200, 300),  width=0) # couleur du fond plafond
    
    #Version avec dégradé:
#     # dessiner le plafond, avec un dégradé de couleur:
#     for i in range (300):
#         pygame.draw.aaline(screen,(128+(i/5),128+(i/5),128+(i/5)),[0,i],[1200,i],1)
#     
#     # dessiner le plafond, avec un dégradé de couleur:
#     for i in range (300):
#         pygame.draw.aaline(screen,(210+(i/8),210+(i/8),190+(i/8)),[0,600-i],[1200,600-i],1)
    
    
def interactions_joueur(sprite_pos_x,sprite_pos_y,sprite_speed,angle_rayon,omega,run,screen):
    # changement de la position, de l'angle de vue et d'autres paramètres du joueur 
    
    keys = pygame.key.get_pressed() # prend en compte toutes les touches appuyées
    
    for event in pygame.event.get():
        # Si l'utilisateur veut quitter la fenêtre d'accueil 
        if keys[K_ESCAPE]==True: 
            run = False
    
    # augmenter ou réduire la vitesse du joueur:
    if keys[K_p]==True:
        sprite_speed = sprite_speed*1.2
    
    elif keys[K_l]==True:
        sprite_speed = sprite_speed/1.2
    
    
    # augmenter ou réduire la hauteur des murs
    if keys[K_o]==True:
        omega = omega*1.2
    
    elif keys[K_k]==True:
        omega = omega/1.2
    
    pygame.mouse.set_pos([600, 300]) # déplacer la souris au centre de l'écran
    pygame.mouse.set_visible(False) # rendre la souris invisible
    

    mouvements_souris  = pygame.mouse.get_rel() # définir les mouvements de la souris
    
    
    ## REMARQUE: la variable "angle_rayon" correspond à l'angle de notre rayon le plus à gauche de notre champ de vision
    
    # Changer l'angle du rayon de droite ou gauche selon le mouvement horizontal de la souris:
    if mouvements_souris[0]>0:
        angle_rayon += 2*mouvements_souris[0]
    
    elif mouvements_souris[0]<0:
        angle_rayon += 2*mouvements_souris[0]
    
    ##REMARQUE: le nombre maximum qui peut être atteint est reglé à 3600, car la variable va plus tard être divisé par 10    
    # modifier l'angle du rayon s'il est trop grand ou petit 
    if angle_rayon>=3600:
        angle_rayon-=3600
    
    elif angle_rayon<0:
        angle_rayon+=3600
        
    
    # Calculer le centre de notre champ de vision: 
    angle_centre=(angle_rayon+600)/10
    ## Pour trouver le centre de notre champ de vision, il faut l'additioner par la moitié de tous les rayons composants notre champ de vision --> 1200/2 = 600
    ## Nous divisons tout par 10, car notre variable est à la base 10 fois plus grande
    
    # modifier l'angle s'il est trop grand ou petit 
    if angle_centre>=360:
        angle_centre-=360
    
    elif angle_centre<0:
        angle_centre+=360
    
    # déplacement du joueur  
    # avancer        
    if keys[K_w]==True:
        sprite_pos_x += sprite_speed* math.cos(math.radians(angle_centre))
        sprite_pos_y += sprite_speed* math.sin(math.radians(angle_centre))
   
   # reculer
    elif keys[K_s]==True:
        sprite_pos_x -= sprite_speed* math.cos(math.radians(angle_centre))
        sprite_pos_y -= sprite_speed* math.sin(math.radians(angle_centre))
    
    # se déplacer à droite
    elif keys[K_d]==True:
        sprite_pos_x += sprite_speed* math.cos(math.radians(angle_centre+90))
        sprite_pos_y += sprite_speed* math.sin(math.radians(angle_centre+60))
    
    # se déplacer à gauche 
    elif keys[K_a]==True:
        sprite_pos_x += sprite_speed* math.cos(math.radians(angle_centre-90))
        sprite_pos_y += sprite_speed* math.sin(math.radians(angle_centre-90))
    

    return (sprite_pos_x,sprite_pos_y, sprite_speed, angle_rayon, omega,run) 

def mini_map_murs_2D (Nb_murs,longueur_murs,liste_H,liste_V,screen):
    # tracer les murs 2D de la mini-map 
    
    # tracer les murs horizontaux:
    for n_ième_C in range (Nb_murs):
        for n_ième_R in range (Nb_murs+1):
            
            # S'il y a bien un mur, le tracer:
            if liste_V[((Nb_murs+1)*n_ième_C)+n_ième_R]:
                pygame.draw.aaline(screen,"black",[((longueur_murs)*n_ième_R)/3, ((longueur_murs)*n_ième_C)/3],
                                   [((longueur_murs)*n_ième_R)/3,((longueur_murs)+(longueur_murs)*n_ième_C)/3],3)
                # nous divisons les coordonées par 3, pour que la mini-map réduise en taille et se situe en haut à droite
                
    # tracer les murs verticaux:
    for n_ième_R in range (Nb_murs):
        for n_ième_C in range (Nb_murs+1):
            
            # S'il y a bien un mur, le tracer:
            if liste_H[((Nb_murs+1)*n_ième_R)+n_ième_C]:
                pygame.draw.aaline(screen,"black",[((longueur_murs)*n_ième_R)/3,((longueur_murs)*n_ième_C)/3],
                                   [((longueur_murs)+(longueur_murs)*n_ième_R)/3,((longueur_murs)*n_ième_C)/3],3)
                # nous divisons les coordonées par 3, pour que la mini-map réduise en taille et se situe en haut à droite
                
 
def affichage_3D(angle_rayon,longueur_murs,liste_H,liste_V,sprite_pos_x,sprite_pos_y,Nb_murs,beta_fisheye,
                 omega,screen):
    # collisions entre le champ de vision et les murs + affichage des murs en 3D
    
    # pour chaque rayon formant le champ de vision  
    for angle_mtn in range (angle_rayon, angle_rayon +1200, 1):
        # nombre de rayons utilisé pour le champ de vision -->1200
        
        position_X_droite= angle_mtn - angle_rayon
        # le n-ième rayon correspond à la position horizontale de la droite que nous allons tracer
        
        ## REMARQUE: puisque "for i in range" n'arrive pas à traiter les nombres "float" (à virgule), nous ne pouvons pas obtenir 1200 rayons différents dans un secteur de 120 degrés (pour le champ de vision)
        ## donc nous divisons le résultat par 10 pour obtenir un angle à virgule
        angle_mtn= angle_mtn/10
        
        
        # modifier l'angle s'il est trop grand ou petit
        if angle_mtn>=360:
            angle_mtn-=360
        
        elif angle_mtn<0:
            angle_mtn+=360
        
        # variables pour déterminer la distance du sprite au mur horizontal ou vertical le plus proche 
        distance_sprite_murhorizontal= 100000
        distance_sprite_murvertical= 100000
        
        # variables pour détecter s'il y a bien eu une collision avec un mur horizontal ou vertical
        mur_vertical_collision=False
        mur_horizontal_collision=False
        
        ## REMARQUE: "n_ième_C" et "n_ième_R" sont utilisés pour identifier, dans la liste, le mur où il y a une collision
        
        ## Détecter les murs verticaux:
        
        Ya= longueur_murs*math.tan(math.radians(angle_mtn))
        # distance Y séparant chaque intersection
        
        # Si le rayon est orienté à droite (selon la mini-map) 
        if angle_mtn < 90 or angle_mtn > 270:
            
            Bx= int(sprite_pos_x/longueur_murs)*longueur_murs + longueur_murs
            # Coordonnée X de la première intersection
            
            By=sprite_pos_y + (sprite_pos_x-Bx)* math.tan(math.radians(-angle_mtn))
            # Coordonnée Y de la première intersection
            
            n_ième_C= int(Bx/longueur_murs) -1
            # calculer la première colonne à laquelle nous aurons notre première instersection
            
            # Boucle pour vérifie si le mur, à chaque intersection, est activé ou pas:
            while n_ième_C <= (Nb_murs-1):
                
                n_ième_R = int(By/longueur_murs)
                # calculer la rangée à laquelle nous aurons notre première instersection
                
                # Vérifier si le mur est activé:
                if 0<=n_ième_R<Nb_murs and liste_V[n_ième_R*(Nb_murs+1)+n_ième_C+1]!=0:
                    
                    distance_sprite_murvertical= (((sprite_pos_x-(n_ième_C*(longueur_murs)+ longueur_murs))**2)
                                                  +((sprite_pos_y- By)**2))**(1/2)
                    # calculer la distance du sprite au mur vertical trouvé
                    
                    # sauvergarder les résultats 
                    n_ième_C_sauvegarde = n_ième_C
                    n_ième_R_sauvegarde = n_ième_R
                    
                    mur_vertical_collision = True # pour informer s'il y a bien eu la collision
                    n_ième_C= Nb_murs+ 1 # pour sortir de la boucle "while"
                    
                    # Modifier l'alpha pour corriger l'effet fishbowl:
                    if angle_mtn > 270: # si le point de fuite se trouve à gauche
                        alpha_mur_vertical= beta_fisheye
                    else: # si le point de fuite se trouve à droite
                        alpha_mur_vertical= -beta_fisheye
                
                # Si le mur est désactivé, changer les variables pour définir la prochaine intersection 
                else:  
                    n_ième_C+=1
                    By += Ya
                
        # Si le rayon est orienté à gauche (selon la mini-map) 
        elif angle_mtn !=90 and 270:
            
            Bx= int(sprite_pos_x/longueur_murs)*longueur_murs
            # Coordonnée X de la première intersection
            
            By=sprite_pos_y + (sprite_pos_x-Bx)* math.tan(math.radians(-angle_mtn))
            # Coordonnée Y de la première intersection
            
            n_ième_C= int(Bx/longueur_murs) -1
            # calculer la première colonne à laquelle nous aurons notre première instersection
            
            # Boucle pour vérifie si le mur, à chaque intersection, est activé ou pas:
            while n_ième_C >= -1:
                
                n_ième_R = int(By/longueur_murs)
                # calculer la rangée à laquelle nous aurons notre première instersection
                
                # Vérifier si le mur est activé:
                if 0<=n_ième_R< Nb_murs and liste_V[n_ième_R*(Nb_murs+1)+n_ième_C+1]!=0:
                
                    distance_sprite_murvertical= (((sprite_pos_x-(n_ième_C*(longueur_murs)+ longueur_murs))**2)
                                                  +((sprite_pos_y- By)**2))**(1/2)
                    # calculer la distance du sprite au mur vertical trouvé
                    
                    # sauvergarder les résultats 
                    n_ième_C_sauvegarde = n_ième_C
                    n_ième_R_sauvegarde = n_ième_R
                    
                    mur_vertical_collision = True # pour informer s'il y a bien eu la collision
                    n_ième_C=-2 # pour sortir de la boucle "while"
                    
                    # Modifier l'alpha pour corriger l'effet fishbowl:
                    if angle_mtn < 180: # si le point de fuite se trouve à gauche
                        alpha_mur_vertical= beta_fisheye 
                    else: # si le point de fuite se trouve à droite
                        alpha_mur_vertical= -beta_fisheye
                
                # Si le mur est désactivé, changer les variables pour définir la prochaine intersection   
                else:   
                    n_ième_C-=1
                    By -= Ya 
        
        
        ## Détecter les murs horizontaux
                    
        n_ième_R=int(sprite_pos_y/(longueur_murs))
        # calculer la première rangée à laquelle nous aurons notre première instersection
        
        Xa= round(longueur_murs/math.tan(math.radians(360-angle_mtn)),2)
        # distance X séparant chaque intersection
        
        # Si le rayon est orienté en haut (selon la mini-map) 
        if angle_mtn>180:
            
            dis_mur= sprite_pos_y%(longueur_murs)
            Xm= -round(dis_mur/math.tan(math.radians(angle_mtn)),2) + sprite_pos_x
            # Coordonnée X de la première intersection 
            
            # Boucle pour vérifie si le mur, à chaque intersection, est activé ou pas
            while n_ième_R>=0:
                
                n_ième_C= int((Xm)/(longueur_murs))
                # calculer la colonne à laquelle nous aurons notre première instersection
                
                # Vérifier si le mur est activé:
                if 0<=n_ième_C<Nb_murs and liste_H[n_ième_C*(Nb_murs+1)+n_ième_R]!=0:
                    
                    distance_sprite_murhorizontal= (((sprite_pos_x-Xm)**2)+
                                                    ((sprite_pos_y- (n_ième_R*(longueur_murs)))**2))**(1/2)
                    # calculer la distance du sprite au mur horizontal trouvé
                    
                    # si la distance du sprite au mur horizontal est plus petite que celle verticale:
                    if distance_sprite_murhorizontal <= distance_sprite_murvertical:
                        
                        mur_horizontal_collision=True # pour informer s'il y a bien eu la collision
                        
                        # Modifier l'alpha pour corriger l'effet fishbowl:
                        if angle_mtn < 270: # si le point de fuite se trouve à gauche
                            alpha_mur_horizontal= beta_fisheye
                        
                        else: # si le point de fuite se trouve à droite
                            alpha_mur_horizontal= -beta_fisheye
                            
                        distance_correcte= (distance_sprite_murhorizontal)*math.cos(math.radians(alpha_mur_horizontal))
                        # corriger l'effet fishbowl
                        
                        # Pour ne pas faire une division par 0:
                        if distance_correcte==0:
                            distance_correcte=0.001
                        
                        hauteur_mur = (omega/distance_correcte)
                        # calculer la hauteur du mur que nous allons afficher
                        
                        pygame.draw.aaline(screen,"red",[sprite_pos_x/3, sprite_pos_y/3],
                                           [Xm/3, (n_ième_R*(longueur_murs))/3],3)
                        # tracer le rayon sur la mini-map
                        
                        mur_coord_X= Xm-(n_ième_C*longueur_murs)
                        # coordonnée horizontale de l'intersection par rapport au mur (pas de la mini-map!)
                        
                        ill = (distance_correcte/120)
                        # illusion de distance; éclaircir la couleur du mur
                        
                        textures(mur_coord_X,liste_H,n_ième_C,n_ième_R,position_X_droite,hauteur_mur,
                                 longueur_murs,Nb_murs,ill,screen)
                        # utiliser la def pour les textures textures
                        
                    n_ième_R=-1 # pour sortir de la boucle
                
                # Changer les variables pour définir la prochaine intersection:
                n_ième_R-=1
                Xm+= Xa
        
        # Si le rayon est orienté en bas (selon la mini-map) 
        elif angle_mtn!=0:             
            dis_mur= (longueur_murs)-sprite_pos_y%(longueur_murs)
            Xm= round(dis_mur/math.tan(math.radians(angle_mtn)),2) + sprite_pos_x
            # Coordonnée X de la première intersection
            
            # Boucle pour vérifie si le mur, à chaque intersection, est activé ou pas:
            while n_ième_R<= (Nb_murs-1):
                
                n_ième_C= int((Xm)/(longueur_murs))
                # calculer la colonne à laquelle nous aurons notre première instersection
                
                # Vérifier si le mur est activé:
                if 0<=n_ième_C<Nb_murs and liste_H[n_ième_C*(Nb_murs+1)+n_ième_R+1]!=0:
                    
                    distance_sprite_murhorizontal= (((sprite_pos_x-Xm)**2)+
                                                    ((sprite_pos_y- (n_ième_R*(longueur_murs)+longueur_murs))**2))**(1/2)
                    # calculer la distance du sprite au mur horizontal trouvé
                    
                    # si la distance du sprite au mur horizontal est plus petite que celle verticale:
                    if distance_sprite_murhorizontal <= distance_sprite_murvertical:
                        
                        mur_horizontal_collision=True # pour informer s'il y a bien eu la collision
                        
                        # Modifier l'alpha pour corriger l'effet fishbowl:
                        if angle_mtn < 90: # si le point de fuite se trouve à gauche
                            alpha_mur_horizontal= beta_fisheye
                        else: # si le point de fuite se trouve à droite
                            alpha_mur_horizontal= -beta_fisheye
                            
                        distance_correcte= (distance_sprite_murhorizontal)*math.cos(math.radians(alpha_mur_horizontal))
                        # corriger l'effet fishbowl
                        
                        # Pour ne pas faire une division par 0:
                        if distance_correcte==0:
                            distance_correcte=0.001
                            
                        hauteur_mur = (omega/distance_correcte)
                        # calculer la hauteur du mur que nous allons afficher
                        
                        pygame.draw.aaline(screen,"red",[sprite_pos_x/3, sprite_pos_y/3],
                                           [Xm/3, (n_ième_R*(longueur_murs)+longueur_murs)/3],3)
                        # tracer le rayon sur la mini-map
                        
                        mur_coord_X = Xm-(n_ième_C*longueur_murs)
                        # coordonnée horizontale de l'intersection par rapport au mur (pas de la mini-map!)
                        
                        ill = (distance_correcte/120)
                        # illusion de distance; éclaircir la couleur du mur
                        
                        textures(mur_coord_X,liste_H,n_ième_C,n_ième_R+1,position_X_droite,hauteur_mur,
                                 longueur_murs,Nb_murs,ill,screen)
                        # utiliser la def pour les textures textures
                        
                    n_ième_R=Nb_murs+ 1 # pour sortir de la boucle
                
                # Changer les variables pour définir la prochaine intersection:
                n_ième_R+=1
                Xm-= Xa       
        
        ## Si il n'y a pas eu de collisions au mur horizontal, afficher le mur vertical:  
        if mur_vertical_collision == True and mur_horizontal_collision==False:   #pour afficher le point si les deux options ne fonctionnent pas 
                        
            distance_correcte= (distance_sprite_murvertical)*math.cos(math.radians(alpha_mur_vertical))
            # corriger l'effet fishbowl
            
            # Pour ne pas faire une division par 0:
            if distance_correcte==0:
                distance_correcte=0.001
                
            hauteur_mur = (omega/distance_correcte)
            # calculer la hauteur du mur que nous allons afficher
            
            pygame.draw.aaline(screen,"red",[sprite_pos_x/3, sprite_pos_y/3],
                               [(n_ième_C_sauvegarde*(longueur_murs)+ longueur_murs)/3,By/3],3)
            # tracer le rayon sur la mini-map
            
            mur_coord_X= By-(n_ième_R_sauvegarde*longueur_murs)
            # coordonnée horizontale de l'intersection par rapport au mur (pas de la mini-map!)
            
            ill = (distance_correcte/120)
            # illusion de distance; éclaircir la couleur du mur
            
            textures(mur_coord_X,liste_V,n_ième_R_sauvegarde,n_ième_C_sauvegarde+1,position_X_droite,hauteur_mur,
                     longueur_murs,Nb_murs,ill,screen)
            # utiliser la def pour les textures textures
    
        
def textures(mur_coord_X,liste_VH,n_ième_1,n_ième_2,position_X_droite,hauteur_mur,longueur_murs,Nb_murs,ill,screen):
    # textures des murs
    
    # Equation pour changer le RGB selon la distance au mur (illusion de distance):
    # (255- RGB) * ill + RGB
    
    # texture munéro 1:
    if liste_VH[n_ième_1*(Nb_murs+1)+n_ième_2]==1:
          
        pygame.draw.aaline(screen,(90 * ill+ 165, 213 * ill+42, 213 * ill+42),[position_X_droite,300+hauteur_mur],
                               [position_X_droite,300-hauteur_mur],1)
        # tracer uniquement des traits bruns
        
        
    # texture munéro 2:
    elif liste_VH[n_ième_1*(Nb_murs+1)+n_ième_2]==2:
        
        
        pygame.draw.aaline(screen,(255,26 * ill+ 229, 51 * ill + 204),[position_X_droite,300+hauteur_mur],
                           [position_X_droite,300-hauteur_mur],1)
        # tracer l'arrière-plan 
        
        # tracer les traits horizontaux, situés en haut et en bas du mur:
        pygame.draw.aaline(screen,(255,55 * ill+ 200, 105 * ill + 150),[position_X_droite,300+hauteur_mur],
                           [position_X_droite,(300+hauteur_mur)-(hauteur_mur/15)],1)
        pygame.draw.aaline(screen,(255,55 * ill+ 200,105 * ill+ 150),[position_X_droite,300-hauteur_mur],
                           [position_X_droite,(300-hauteur_mur)+(hauteur_mur/15)],1)
        pygame.draw.aaline(screen,(255,77 * ill+ 178,153 * ill+ 102),[position_X_droite,300+hauteur_mur],
                           [position_X_droite,(300+hauteur_mur)-(hauteur_mur/25)],1)
        
        # tracer les fenêtres:
        if (longueur_murs/4)<mur_coord_X< (longueur_murs/2.3) or (longueur_murs-(longueur_murs/2.3))<mur_coord_X<(longueur_murs-(longueur_murs/4)):
            pygame.draw.aaline(screen,(102 * ill+ 153,255,255),
                               [position_X_droite,300+(hauteur_mur/2)],[position_X_droite,300-(hauteur_mur/2)],1)
            # tracer le ciel des fenêtre
            
            # fenetre_1 --> fenêtre à gauche de l'ecran
            # fenetre_2 --> fenêtre à droite de l'ecran
            centre_fenetre_1= ((longueur_murs/4)+(longueur_murs/2.3))/2
            centre_fenetre_2= ((longueur_murs-(longueur_murs/2.3))+(longueur_murs-(longueur_murs/4)))/2
            
            # l'epaisseur des cadres de la fenêtre:
            epaisseur_cadre_vertical = (longueur_murs/3.93)-(longueur_murs/4)
            epaisseur_cadre_horizontal=(hauteur_mur/2)-(hauteur_mur/2.1)
            
            # tracer les cadres verticaux:
            # 1. bord gauche de fenetre_1, 2.bord droite de fentre_1, 3. bord gauche de fenetre_2, 4.bord droite de fentre_2, 5. bord centre de fenetre_1, 6. bord centre de fenetre_2
            if mur_coord_X< (longueur_murs/3.93) or (longueur_murs/2.3)-epaisseur_cadre_vertical<mur_coord_X<(longueur_murs/2.3) or (longueur_murs-(longueur_murs/2.3))<mur_coord_X<(longueur_murs-(longueur_murs/2.3))+epaisseur_cadre_vertical or longueur_murs-(longueur_murs/3.93)<mur_coord_X or centre_fenetre_1 - (epaisseur_cadre_vertical/2) <mur_coord_X< centre_fenetre_1 + (epaisseur_cadre_vertical/2) or centre_fenetre_2 - (epaisseur_cadre_vertical/2) <mur_coord_X< centre_fenetre_2 + (epaisseur_cadre_vertical/2):
                pygame.draw.aaline(screen,(244 + ill, 224 + ill, 224 + ill),
                                   [position_X_droite,300+(hauteur_mur/2)],[position_X_droite,300-(hauteur_mur/2)],1)
            
            # tracer les cadres horizontaux:
            else:
                pygame.draw.aaline(screen,(224 + ill, 224 + ill,224 + ill),
                                   [position_X_droite,300+(hauteur_mur/2)],[position_X_droite,300+(hauteur_mur/2.4)],1)
                pygame.draw.aaline(screen,(224 + ill, 224 + ill,224 + ill),
                                   [position_X_droite,300-(hauteur_mur/2)],[position_X_droite,300-(hauteur_mur/2.1)],1)
                pygame.draw.aaline(screen,(224 + ill, 224 + ill,224 + ill),
                                   [position_X_droite,300-(epaisseur_cadre_horizontal/2)],[position_X_droite,300+(epaisseur_cadre_horizontal/2)],1)
            
            #bordure sombre se trouvant en bas de la fenetre   
            pygame.draw.aaline(screen,(40 * ill+ 215,40 * ill+ 215,40 * ill+ 215),
                               [position_X_droite,300+(hauteur_mur/2)],[position_X_droite,300+(hauteur_mur/2.1)],1)
              
            
    # texture munéro 3:
    else:
        
        pygame.draw.aaline(screen,(170 * ill + 85,179 * ill + 76,179 * ill + 76),
                           [position_X_droite,300+hauteur_mur],[position_X_droite,300-hauteur_mur],1)
        # tracer l'arrière-plan 
        
        # tracer les droites horizontaux, situées en bas
        pygame.draw.aaline(screen,(225 * ill + 30,225 * ill + 30,225 * ill + 30),
                           [position_X_droite,300+hauteur_mur-(hauteur_mur/18)],[position_X_droite,300+hauteur_mur-(hauteur_mur/19)],1)
        pygame.draw.aaline(screen,(225 * ill + 30,225 * ill + 30,225 * ill + 30),
                           [position_X_droite,300+hauteur_mur],[position_X_droite,300+hauteur_mur],1)
        
        # tracer les droites verticaux, situées en bas
        if round(mur_coord_X,1)%(longueur_murs/40)==0:
            pygame.draw.aaline(screen,(225 * ill + 30,225 * ill + 30,225 * ill + 30),
                               [position_X_droite,300+hauteur_mur],[position_X_droite,300+hauteur_mur-(hauteur_mur/19)],1)
        
        ## REMARQUE: il faut arrondir "mur_coord_X", sinon le modulo ne sera jamais égal à 0
        
        # tracer les droites verticales, situées en centre:
        if round(mur_coord_X,1)%(longueur_murs/12)==0:
            
            position_verticale= 300+hauteur_mur-(hauteur_mur/19)
            # pour déterminer la position verticale, d'où à où nous allons tracer la droite

            # tracer les droites verticales de chaque colonne de pixel, jusqu'à atteindre la hauteur max du mur 
            while position_verticale-(2*(hauteur_mur/19*4))>=300-hauteur_mur:
                pygame.draw.aaline(screen,(197 * ill + 58,202 * ill + 53,202 * ill + 53),
                                   [position_X_droite,position_verticale],[position_X_droite,position_verticale-(hauteur_mur/19*4)],1)
                position_verticale-= 2*(hauteur_mur/19*4)
        
        # même algorithme qu'au dessus, mais en décalé:
        elif round(mur_coord_X-(longueur_murs/12/2),1)%(longueur_murs/12)==0:
            
            position_verticale= 300+hauteur_mur-(hauteur_mur/19*5)
            # pour déterminer la position verticale, d'où à où nous allons tracer la droite
            
            # tracer les droites verticales de chaque colonne de pixel, jusqu'à atteindre la hauteur max du mur
            while position_verticale-(2*(hauteur_mur/19*4))>=300-hauteur_mur:
                pygame.draw.aaline(screen,(197 * ill + 58,202 * ill + 53,202 * ill + 53),
                                   [position_X_droite,position_verticale],[position_X_droite,position_verticale-(hauteur_mur/19*4)],1)
                position_verticale-= 2*(hauteur_mur/19*4)
        
        # tracer les droites horizontaux, situées en centre:
        
        position_verticale= 300+hauteur_mur-(hauteur_mur/19*5)
        # pour déterminer la position verticale, où nous allons tracer la droite
        
        # tracer les droites horizontaux de chaque rangée de pixel, jusqu'à atteindre la hauteur max du mur:
        while position_verticale-(2*(hauteur_mur/19*2))>=300-hauteur_mur:
            pygame.draw.aaline(screen,(197 * ill + 58,202 * ill + 53,202 * ill + 53),
                               [position_X_droite,position_verticale],[position_X_droite,position_verticale],1)
            position_verticale-= 2*(hauteur_mur/19*2)
        
        
        pygame.draw.aaline(screen,(225 * ill + 30,225 * ill + 30,225 * ill + 30),
                           [position_X_droite,position_verticale+2*(hauteur_mur/19*2)],[position_X_droite,position_verticale+2*(hauteur_mur/19*2)],1)
        # tracer les traits horizontaux, situées en haut
        
        # tracer les traits verticaux, situées en haut
        if round(mur_coord_X,1)%(longueur_murs/40)==0:
            pygame.draw.aaline(screen,(225 * ill + 30,225 * ill + 30,225 * ill + 30),
                               [position_X_droite,position_verticale+2*(hauteur_mur/19*2)],[position_X_droite,300-hauteur_mur],1)
        


