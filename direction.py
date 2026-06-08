"""Module gérant la direction du serpent."""

from enum import Enum

class Direction(Enum):
    """Représente la direction du serpent
    
    Gère les différentes directions possibles pour le serpent,
    à savoir UP, DOWN, LEFT et RIGHT.
    """
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4