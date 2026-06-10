"""Module managing the snake's direction."""

from enum import Enum

class Direction(Enum):
    """Represents the direction of the snake.
    
    Manages the different possible directions for the snake,
    namely UP, DOWN, LEFT, and RIGHT.
    """
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4