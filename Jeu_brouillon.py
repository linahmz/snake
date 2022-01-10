import pygame 
import sys 
import random 


class Jeu():
    # contenir toutes les variables ainsi que les fonctions utiles pour le bon deroulement du jeu

    def __init__(self):

        self.ecran = pygame.display.set_mode((800, 600))# definition de la resolution de la fenetre, tuple(largeur,longueur)

        pygame.display.set_caption('Jeu Snake')# attribue un titre a la fenetre

        self.jeu_encours = True

        self.serpent_position_x = 300
        self.serpent_position_y = 300
        self.serpent_direction_x = 0
        self.serpent_direction_y = 0
        self.serpent_dimension = 10

        self.pomme_x = random.randrange(0,600,10)# attention la pomme doit se trouver à un x ou y multiple de 10 sinon le serpent ne pourra pas se superposer exactement sur la pomme
        self.pomme_y = random.randrange(90,600,10)
        self.pomme = 10

        self.clock = pygame.time.Clock() # va permettre de gérer le nombre d'images qu'on a par seconde et donc la vitesse du jeu
        
        #création d'une liste qui recense toutes les positions du serpent
        self.positions_serpent = []

        #création de la taille du serpent (cad le nombre de petits carrés dont il est composé)
        self.taille = 1

        self.ecran_du_debut = True

        self.perdu = False

        self.image_accueil = pygame.image.load("Cr_er_le_jeu_Snake_sur_Scratch_snake-realite-augmentee-nokia-facebook.jpg")

        self.image_titre = pygame.transform.scale(self.image_accueil,(600,400)) #ajustement de la taille de l'image sur l'écran

        self.score = 0

        self.L = []

        self.dir = ""


    def fonction_principale(self):

        while self.ecran_du_debut:

            for evenement in pygame.event.get():

                if evenement.type == pygame.QUIT:

                    sys.exit()

                if evenement.type == pygame.KEYDOWN:

                    if evenement.key == pygame.K_RETURN:

                        self.ecran_du_debut = False

                self.ecran.fill((218,179,188))

                self.ecran.blit(self.image_titre,(100,50)) #affichage d'une surface sur l'écran

                self.afficher_message('petite',"Faites grandir le serpent le plus possible en lui faisant manger des pommes",(100,500,200,5),(0,0,0))

                self.afficher_message("moyenne", "Appuyez sur Return pour commencer",(180,520,200,5),(230,60,12))

                pygame.display.flip()

        
        while self.jeu_encours:
            
            for evenement in pygame.event.get(): # pygame.event. get donne une liste des évènements possibles dans pygame (ex: déplacement de la souris, pression sur une touche)
        
                if evenement.type == pygame.QUIT: # permet de sortir du jeu même s'il n'est pas terminé, on évite d'avoir un boucle qui tourne à l'infini
        
                    sys.exit()

                if evenement.type == pygame.KEYDOWN: #direction du serpent change en fonction de la touche sur laquelle on appuie
                    
                    if evenement.key == pygame.K_RIGHT:
                        self.serpent_direction_x = 10
                        self.serpent_direction_y = 0
                        self.dir = "D"
                        #print("D")

                    if evenement.key == pygame.K_LEFT:
                        self.serpent_direction_x = -10
                        self.serpent_direction_y = 0
                        self.dir = "G"
                        #print("G")

                    if evenement.key == pygame.K_DOWN:
                        self.serpent_direction_x = 0
                        self.serpent_direction_y = 10
                        self.dir = "B"
                        #print("B")

                    if evenement.key == pygame.K_UP:
                        self.serpent_direction_x = 0
                        self.serpent_direction_y = -10
                        self.dir = "H"
                        #print("H")
                
            self.L.append(self.dir)
            if len(self.L) > 2:
                del(self.L[0])

            if self.serpent_position_x < 0 or self.serpent_position_x > 800 or self.serpent_position_y < 80 or self.serpent_position_y > 590:
                self.perdu = True
                self.recommencement_du_jeu()

            self.serpent_bouge()
            
            self.le_serpent_mange()

            #crée une liste qui stocke la position de la tête du serpent
            tete_du_serpent = []
            tete_du_serpent.append(self.serpent_position_x)
            tete_du_serpent.append(self.serpent_position_y)

            
            #append dans la liste la liste des positions du serpent
            self.positions_serpent.append(tete_du_serpent)

            #cration de la condition de dessin de tous les blocs du serpent ou pas
            if len(self.positions_serpent) > self.taille:

                self.positions_serpent.pop(0) # quand le nombre d'éléments de la liste contenant les positions de toutes les parties du serpent
                #est plus grand que la taille du serpent, on supprime le 1er élément, qui correspond aux positions précédentes des parties du serpent)      
            
            self.afficher_pomme_et_serpent()

            #self.afficher_serpent()

            self.game_over(tete_du_serpent)

            self.afficher_message('moyenne', "Jeu Snake",(320,10,100,50),(0,0,150),)
            self.afficher_message('petite', "Score : {}".format(str(self.score)), (325,50,50,50), (0,0,150))

            self.cadre() # le cadre est dessiné à chaque passage dans la boucle
            
            self.recommencement_du_jeu()

            self.clock.tick(10) # permet d'avoir 20 images par secondes moins il ya d'images par seconde plus le déplacement du serpent est lent

            pygame.display.flip()# rafraîchir l'écran

        
        


    def cadre(self): #création des limites du jeu

        pygame.draw.rect(self.ecran,(255,255,255),(0,80,800,1),3)
        #pygame.draw.rect(self.ecran,(116,208,241),(0,0,800,80),1)
        

    def serpent_bouge(self): # les modifications des directions entraînent un déplacement du petit curseur
        self.serpent_position_x += self.serpent_direction_x
        self.serpent_position_y += self.serpent_direction_y
            #print(self.serpent_position_x,self.serpent_position_y)
    
    def afficher_pomme_et_serpent(self):
        
        self.ecran.fill((255,232,238))
   
        #afficher la pomme
        pygame.draw.circle(self.ecran,(255,0,0),(self.pomme_x + 5,self.pomme_y + 5),5)
        
        #afficher le serpent
        for partie_du_serpent in self.positions_serpent:
            pygame.draw.rect(self.ecran,(21,250,119),(partie_du_serpent[0],partie_du_serpent[1],self.serpent_dimension, self.serpent_dimension))
            
    def game_over(self,tete_du_serpent):
        # si le serpent se mord la queue
            if self.taille == 2:
                if (self.L[0],self.L[1]) == ("D","G") or (self.L[0],self.L[1]) == ("G","D") or (self.L[0],self.L[1]) == ("H","B") or (self.L[0],self.L[1]) == ("B","H") :
                    
                    self.jeu_encours = False
                    self.perdu = True


            for partie_du_serpent in self.positions_serpent[:-1] : # on prend toute la liste sauf le dernier élément car il correspond à la 
                #nouvelle position de la tête

                if tete_du_serpent == partie_du_serpent :

                    self.jeu_encours = False
                    self.perdu = True
    
    def le_serpent_mange(self):
        if self.pomme_x == self.serpent_position_x and self.pomme_y == self.serpent_position_y:
                
                print("ok")

                self.pomme_x = random.randrange(100,695,10)
                self.pomme_y = random.randrange(100,595,10)

                self.taille += 1

                self.score += 1

    def afficher_message(self, font, message, message_rectangle, couleur): #message_renctangle permet d'indiquer la position du rectangle dans le lequel on veut écrire puis sa longueur et sa largeur

        if font == 'petite':
            font = pygame.font.SysFont('timesnewroman',20,False)

        elif font == 'moyenne':
            font = pygame.font.SysFont('timesnewroman',30,False)
        
        elif font == 'grande':
                font = pygame.font.SysFont('timesnewroman',40,False)

        message = font.render(message,True,couleur)

        self.ecran.blit(message,message_rectangle)

        #pygame.draw.rect(self.ecran,(116,208,241),(0,0,800,80),40)
        
        
    def recommencement_du_jeu(self):

        while self.perdu == True :
            
            for evenement in pygame.event.get():
                
                if evenement.type == pygame.QUIT:

                    sys.exit()

                if evenement.type == pygame.KEYDOWN:

                    if evenement.key == pygame.K_RETURN:

                        self.perdu = False

                        Jeu().fonction_principale()

            self.ecran.fill((0,0,0))

            self.afficher_message('grande', "Vous avez perdu", (200,200,400,40), (255,255,255))

            self.afficher_message('grande', "Votre score est de {}".format(str(self.score)),(300,300,400,40), (255,255,255))

            self. afficher_message('moyenne', " Pour rejouer taper Return", (200,400,400,40), (150,80,0))

            pygame.display.flip()




if __name__ == '__main__':
    pygame.init()
    Jeu().fonction_principale()
    pygame.quit()

#instruction utilisée au début pour afficher un carré du serpent
#pygame.draw.rect(self.ecran,(27,79,8),(self.serpent_position_x, self.serpent_position_y,self.serpent_dimension,self.serpent_dimension))

#instruction pour tester la fonction afficher_message
# #self.afficher_message('petite','Snake',(0,0,0),(300,300,100,50))
