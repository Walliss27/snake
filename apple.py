"""Module gérant la logique de la pomme dans le jeu."""

import random

class Apple:
    """Représente la pomme sur la grille."""

    def __init__(self, x: int , y: int) -> None:
        """Initialise une nouvelle pomme

        Args:
            x(int): La coordonnée x sur la grille.
            y(int): La coordonnée y sur la grille.
        """
        self._x = x
        self._y = y

    @property
    def x(self) -> int:
        """Retourne la coordonnée x de la pomme."""
        return self._x
    
    @property
    def y(self) -> int:
        """Retourne la coordonnée y de la pomme."""
        return self._y

    def spawn(self, largeur: int, hauteur: int, taille_bloc: int,\
               snake_corps: list[tuple[int, int]]) -> None:
        """Gère l'apparition de la pomme à un nouvel endroit aléatoire.
        
        Args:
            largeur(int): La largeur de la fenêtre.
            hauteur(int): La hauteur de la fenêtre.
            taille_bloc(int): La taille d'un bloc de la grille en pixels.
            snake_corps(list[tuple[int, int]]: La liste des coordonnées du corps du serpent.
        """
        self._x, self._y = snake_corps[0]
        while (self._x, self._y) in snake_corps:
            self._x = round(random.randrange(0, largeur - taille_bloc) / 20.0) * 20.0
            self._y = round(random.randrange(0, hauteur - taille_bloc) / 20.0) * 20.0
    