def collision(posx_1, posy_1, width_1, height_1, posx_2, posy_2, width_2, height_2):
    return posx_1+width_1 > posx_2 and posx_2+width_2 > posx_1 and posy_1+height_1 > posy_2 and posy_2+height_2>posy_1

class Sprite:
    def __init__(self, gauche, droite, pos_x, speed, delay_max, orientation, pos_y, sprite_v0, sprite_a, nb_vie, WINDOW_WIDTH, WINDOW_DELTA_WIDTH, scrolling_screen_percent):
        #Valeurs fixes quand le programme initialise
        self.compteur_anim= 0 # compteur pour savoir a quelle image on est dans la liste
        self.delay_anim= 0 # pour ne pas changer d'images à chaque fois
        self.activation_saut= False
        self.temps_saut= 1
        self.vt=0
        #dimensions des collisions
        self.width=64
        self.height=64
        #initialises avec les parametres du init
        
        #pour le déplacement en x
        self.gauche = gauche
        self.droite = droite
        self.pos_x = pos_x
        self.speed = speed
        self.delay_max= delay_max
        self.orientation = orientation
        #pour le déplacement en y (saut)
        self.pos_y = pos_y
        self.sprite_v0 = sprite_v0
        self.v0_stockage= sprite_v0
        self.sprite_a = sprite_a
        #respawn/vie
        self.mort = False
        self.nb_vie=nb_vie
        self.pos_x_stockage = pos_x
        self.pos_y_stockage = pos_y
        self.orientation_stockage = orientation
        #Window width:
        self.WINDOW_WIDTH= WINDOW_WIDTH
        self.WINDOW_DELTA_WIDTH = WINDOW_DELTA_WIDTH
        #scrolling
        self.scrolling_screen_percent = scrolling_screen_percent
        self.scroll=0
        
        self.debug= 1 
        
    def move_right(self, plateformes):
        self.orientation = "droite"
        coll = False
        
        if self.scrolling()==False:
            ####Determiner une collision
            for plateforme in plateformes:
                if collision(self.pos_x + self.speed, self.pos_y, self.width, self.height, plateforme.pos_x -self.scroll, plateforme.pos_y, plateforme.nb_blocs*plateforme.taille, plateforme.taille):
                    coll=True
                    break
            if coll == False:
                if (self.pos_x + self.speed) <= self.WINDOW_WIDTH-self.width: ###Pour pas qu'il tombe hors de l'écran
                    self.pos_x = self.pos_x + self.speed
        
     
                
        
        self.delay_anim=self.delay_anim+1
        #changement d'image pour sprite droite
        if self.delay_anim==self.delay_max:
            self.compteur_anim=(self.compteur_anim+1)%3 #On met 3 à la place de 4, car ma premiere image n'a pas de poussiere derriere mon personnage, donc cela fait un effet bizarre. C'est pour cela qu'on va uniquement utiliser les 3 dernieres images de mon sprtie pour les déplacement
            self.delay_anim= 0
        
    def move_left(self,plateformes):
        self.orientation = "gauche"
        coll = False
        
        if self.scrolling()==False:
            ####Determiner une collision
            for plateforme in plateformes:
                if collision(self.pos_x- self.speed, self.pos_y, self.width, self.height, plateforme.pos_x -self.scroll, plateforme.pos_y, plateforme.nb_blocs*plateforme.taille, plateforme.taille):
                    coll=True
                    break
            if coll == False:
                if (self.pos_x - self.speed) >=0: ###Pour pas qu'il tombe hors de l'écran
                    self.pos_x = self.pos_x - self.speed
                
     
            
        self.delay_anim=self.delay_anim+1
        #changement d'image pour sprite droite
        if self.delay_anim==self.delay_max:
            self.compteur_anim=(self.compteur_anim+1)%3 #On met 3 à la place de 4, car ma premiere image n'a pas de poussiere derriere mon personnage, donc cela fait un effet bizarre. C'est pour cela qu'on va uniquement utiliser les 3 dernieres images de mon sprtie pour les déplacement
            self.delay_anim= 0
    
    def saut(self, plateformes):                   
        if self.activation_saut==True:
            self.vt= self.sprite_v0 + self.sprite_a*self.temps_saut
            self.temps_saut = self.temps_saut +1
            coll=False
            for plateforme in plateformes:
                if collision(self.pos_x, self.pos_y-self.vt, self.width, self.height, plateforme.pos_x -self.scroll, plateforme.pos_y, plateforme.nb_blocs*plateforme.taille, plateforme.taille):
                    coll=True
                    #distinction entre le fait d'atterir ou se taper la tete
                    if self.vt >= 0:
                        self.pos_y= plateforme.pos_y +self.height
                        self.temps_saut=0
                        self.sprite_v0=0
                    else:
                        self.pos_y= plateforme.pos_y - self.height
                        self.activation_saut= False
                        #nous faisons ca au cas ou si le v0 a été changé à 0 (dans le if d'avant), pour qu ele saut soir normal pour les prochaines fois
                        self.sprite_v0= self.v0_stockage
                        
                        self.temps_saut=0
                    break
            if coll==False:
                self.pos_y = self.pos_y - self.vt
        #chute libre
        else:
            coll = False
            for plateforme in plateformes:
                if collision(self.pos_x, self.pos_y - self.sprite_a, self.width, self.height, plateforme.pos_x -self.scroll, plateforme.pos_y, plateforme.nb_blocs*plateforme.taille, plateforme.taille):
                    coll=True
                    break
            if coll==False:
                self.activation_saut=True
                self.sprite_v0=0
                #pour ne pas perdre un frame de deplacment
                self.temps_saut=1
                self.vt= self.sprite_v0 + self.sprite_a*self.temps_saut
                self.pos_y=self.pos_y - self.sprite_a
                
    def perdre_vie (self):
        self.nb_vie-=1
        if self.nb_vie == 0 :
            self.mort = True
        else:
            self.scroll = 0 
            self.pos_x= self.pos_x_stockage
            self.pos_y= self.pos_y_stockage
            self.orientation= self.orientation_stockage
            self.compteur_anim= 0
            
    def scrolling (self):
        
        if self.orientation=="gauche" and self.pos_x - self.speed < self.WINDOW_WIDTH* self.scrolling_screen_percent and self.scroll!= 0:
            if self.scroll -self.speed > 0:
                self.scroll = self.scroll - self.speed
                self.pos_x =  self.WINDOW_WIDTH* self.scrolling_screen_percent
                
           
            else:
                self.scroll= 0
            return(True)
        
        elif self.orientation=="droite" and self.pos_x + self.speed > self.WINDOW_WIDTH* (1- self.scrolling_screen_percent) and self.scroll!=self.WINDOW_DELTA_WIDTH:
            if self.scroll + self.speed < self.WINDOW_DELTA_WIDTH:
                self.scroll = self.scroll + self.speed
                self.pos_x= self.WINDOW_WIDTH* (1- self.scrolling_screen_percent)

            else:
                self.scroll= self.WINDOW_DELTA_WIDTH
            return(True)
        
        else:
            return(False)
                
class Plateforme: #collision
    def __init__(self, pos_x, pos_y, taille, nb_blocs, image):  
        self.pos_x= pos_x
        self.pos_y= pos_y
        self.taille= taille
        self.nb_blocs= nb_blocs
        self.image= image
        
