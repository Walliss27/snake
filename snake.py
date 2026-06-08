"""Module gérant la logique et l'état de l'entité principale du joueur."""

from direction import Direction

class Snake:
    """Représente le serpent contrôlé par le joueur
    
    Gère l'état interne du serpent, notamment sa taille actuelle,
    sa direction et les coordonnées de l'ensemble de son corps sur la grille.
    """

    def __init__(self, longueur : int = 1, direction : Direction = Direction.RIGHT) -> None:
        """Initialise un nouveau serpent au début de la partie
        
        Args:
            longueur(int, optional): La taille initiale du serpent. Par défaut à 1.
            direction(Direction, optional): La direction initiale du serpent. Par défaut à droite.
        """
        self._longueur = longueur
        self._corps: list[tuple[int, int]] = []
        self._direction = direction
