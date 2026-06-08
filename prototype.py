import pygame
import random
import sys

# 1. Initialisation
pygame.init()
LARGEUR, HAUTEUR = 600, 400
TAILLE_BLOC = 20
FPS = 15

# Couleurs (RGB)
NOIR = (0, 0, 0)
VERT = (0, 255, 0)
ROUGE = (255, 0, 0)

# Configuration de la fenêtre
ecran = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Snake Project - V1")
horloge = pygame.time.Clock()

def main():
    # État initial du serpent
    x, y = LARGEUR // 2, HAUTEUR // 2
    dx, dy = 0, 0
    serpent = [(x, y)]
    longueur = 1

    # État initial de la pomme (placée aléatoirement sur la grille)
    pomme_x = round(random.randrange(0, LARGEUR - TAILLE_BLOC) / 20.0) * 20.0
    pomme_y = round(random.randrange(0, HAUTEUR - TAILLE_BLOC) / 20.0) * 20.0

    en_cours = True

    # --- LA GAME LOOP ---
    while en_cours:
        
        # ÉTAPE A : Inputs (Événements)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and dx == 0:
                    dx = -TAILLE_BLOC; dy = 0
                elif event.key == pygame.K_RIGHT and dx == 0:
                    dx = TAILLE_BLOC; dy = 0
                elif event.key == pygame.K_UP and dy == 0:
                    dy = -TAILLE_BLOC; dx = 0
                elif event.key == pygame.K_DOWN and dy == 0:
                    dy = TAILLE_BLOC; dx = 0

        # ÉTAPE B : Logique (Mise à jour)
        x += dx
        y += dy
        serpent.append((x, y))

        # On supprime la queue si le serpent n'a pas mangé
        if len(serpent) > longueur:
            del serpent[0]

        # Conditions de défaite (Murs ou collision avec lui-même)
        if x < 0 or x >= LARGEUR or y < 0 or y >= HAUTEUR or (x, y) in serpent[:-1]:
            en_cours = False # Fin de la partie

        # Manger la pomme
        if x == pomme_x and y == pomme_y:
            longueur += 1
            pomme_x = round(random.randrange(0, LARGEUR - TAILLE_BLOC) / 20.0) * 20.0
            pomme_y = round(random.randrange(0, HAUTEUR - TAILLE_BLOC) / 20.0) * 20.0

        # ÉTAPE C : Rendu (Affichage)
        ecran.fill(NOIR)
        pygame.draw.rect(ecran, ROUGE, [pomme_x, pomme_y, TAILLE_BLOC, TAILLE_BLOC])
        for bloc in serpent:
            pygame.draw.rect(ecran, VERT, [bloc[0], bloc[1], TAILLE_BLOC, TAILLE_BLOC])

        pygame.display.update()
        horloge.tick(FPS) # Maintient le jeu à 15 images/seconde

if __name__ == "__main__":
    main()