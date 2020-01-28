import pygame
from game import Game

pygame.init()



#generer la fenetre du jeu
pygame.display.set_caption("monster Game")
screen = pygame.display.set_mode((1080, 720))

#importer de charger l'arriere plan de notre jeu
background = pygame.image.load('bg.jpg')

#charger notre jeu
game = Game()

running = True

#boucle s'execute tant que running est vrai
while running:

    #appliquer l'arriere plan du jeu
    screen.blit(background, (0, -200))
    #appliquer l'image de mon joueur
    screen.blit(game.player.image, game.player.rect)
    #print(game.pressed) pour tester les touches afficher dans dictionnaire
    #verifier si le joueur veut aller a gauche ou a droite
    #et ajouter condition pour ne pas traverser l'ecran (methode get_width = recupere la largeur de l'objet ici screen et du player) calculé en haut a gauche
    if game.pressed.get(pygame.K_RIGHT) and game.player.rect.x + game.player.rect.width < screen.get_width():
        game.player.move_right()
    elif game.pressed.get(pygame.K_LEFT) and game.player.rect.x > 0:
        game.player.move_left()
    #mettre a jour l'ecran (la fenetre)
    pygame.display.flip()
    #si le joueur ferme la fenetre
    for event in pygame.event.get():
        #verifier que l'evenement est la fermeture de fenetre
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            print("fermeture du jeu")
        # detecter si un joueur tape au clavier et savoir quel touche est activé ou non par le joueur
        elif event.type == pygame.KEYDOWN:
            game.pressed[event.key] = True
        elif event.type == pygame.KEYUP:
            game.pressed[event.key] = False


        
