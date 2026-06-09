"""Module gérant la logique et l'état de l'entité principale du joueur."""

from direction import Direction

class Snake:
    """Représente le serpent contrôlé par le joueur
    
    Gère l'état interne du serpent, notamment sa taille actuelle,
    sa direction et les coordonnées de l'ensemble de son corps sur la grille.
    """

    def __init__(self, x : int , y : int, longueur : int = 1,\
                  direction : Direction = Direction.RIGHT, taille_bloc : int = 20) -> None:
        """Initialise un nouveau serpent au début de la partie
        
        Args:
            x(int): La coordonnée x de départ (tête du serpent).
            y(int): La coordonnée y de départ (tête du serpent).
            longueur(int, optional): La taille initiale du serpent. Par défaut à 1.
            direction(Direction, optional): La direction initiale du serpent. Par défaut à droite.
            taille_bloc(int, optional): La taille des blocs, en nombre de pixels. Par défaut à 20.
        """
        self._longueur = longueur
        self._corps: list[tuple[int, int]] = [(x, y)]
        self._direction = direction
        self._taille_bloc = taille_bloc

    @property
    def corps(self) -> list[tuple[int, int]]:
        """Renvoie une copie des coordonnées du corps du serpent."""
        return self._corps[:]
    
    @property
    def direction(self) -> Direction:
        """Renvoie la direction actuelle de la tête du serpent."""
        return self._direction
    
    @direction.setter
    def direction(self, dir : Direction) -> None:
        """Modifie la direction actuelle de la tête du serpent."""
        mouvements_interdits = {
            Direction.UP: Direction.DOWN,
            Direction.DOWN: Direction.UP,
            Direction.LEFT: Direction.RIGHT,
            Direction.RIGHT: Direction.LEFT
        }
        if dir != mouvements_interdits[self._direction]:
            self._direction = dir

    def move(self) -> None:
        """Permet le mouvement du serpent."""
        x_head, y_head = self._corps[0]
        if self._direction == Direction.UP:
            self._corps.insert(0, (x_head, y_head - self._taille_bloc))
        elif self._direction == Direction.DOWN:
            self._corps.insert(0, (x_head, y_head + self._taille_bloc))
        elif self._direction == Direction.LEFT:
            self._corps.insert(0, (x_head - self._taille_bloc, y_head))
        elif self._direction == Direction.RIGHT:
            self._corps.insert(0, (x_head + self._taille_bloc, y_head))
        if len(self._corps) != self._longueur:
            self._corps.pop()