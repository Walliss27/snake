"""
Module defining the movement directions for the game entities.

Provides an enumeration of all possible valid directions to standardize 
movement logic across the application.
"""

from enum import Enum

class Direction(Enum):
    """
    Enumeration representing the valid directions.

    Attributes:
        UP (int): Movement towards the top of the screen.
        DOWN (int): Movement towards the bottom of the screen.
        LEFT (int): Movement towards the left side of the screen.
        RIGHT (int): Movement towards the right side of the screen.
    """
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4