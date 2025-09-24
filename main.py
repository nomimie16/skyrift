import pygame
from win32api import GetSystemMetrics # pour récuperer la taille de l'écran

# Initialiser Pygame
pygame.init()
 
# Créer la fenêtre
taille_ecran = GetSystemMetrics(1)
screen = pygame.display.set_mode((taille_ecran, taille_ecran))
 
# Définir les couleurs
WHITE = (255, 255, 255)
 
# Bouton quitter le jeu
quit_img = pygame.image.load("assets/img/quit.png").convert_alpha()
quit_img = pygame.transform.scale(quit_img, (55, 55))
quit_rect = quit_img.get_rect()
quit_rect.topleft = (taille_ecran - 50, 0)

# Police pour le texte
# font = pygame.font.Font(None, 36)
 
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
 
        if event.type == pygame.MOUSEBUTTONDOWN:
            if quit_rect.collidepoint(event.pos):
                running = False
                print("##################\nJeu SkyRift Fermé.\n##################")
                
 
    # Remplir l'écran avec du blanc
    screen.fill(WHITE)
    
    # Dessiner le bouton quitter
    screen.blit(quit_img, quit_rect)
  
    # Mettre à jour l'affichage
    pygame.display.flip()

pygame.quit()