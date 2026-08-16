"""Module gérant la logique et l'état de l'entité principale du joueur."""

from direction import Direction
from collections import deque

class Snake:
    """Represents the snake controlled by the player.
    
    Manages the internal state of the snake, notably its current length,
    its direction, and the coordinates of its entire body on the grid.
    """

    def __init__(self, x : int , y : int, length : int = 1,\
                  direction : Direction = Direction.RIGHT, block_size : int = 20) -> None:
        """Initializes a new snake at the start of the game.
        
        Args:
            x (int): The starting x coordinate (head of the snake).
            y (int): The starting y coordinate (head of the snake).
            length (int, optional): The initial length of the snake. Defaults to 1.
            direction (Direction, optional): The initial direction of the snake. Defaults to RIGHT.
            block_size (int, optional): The size of the blocks, in pixels. Defaults to 20.
        """
        self._length = length
        self._body: list[tuple[int, int]] = [(x, y)]
        self._direction = direction
        self._block_size = block_size

    @property
    def body(self) -> list[tuple[int, int]]:
        """Returns a copy of the snake's body coordinates."""
        return self._body[:]
    
    @property
    def direction(self) -> Direction:
        """Returns the current direction of the snake's head."""
        return self._direction
    
    @direction.setter
    def direction(self, dir : Direction) -> None:
        """Modifies the current direction of the snake's head."""
        forbidden_moves = {
            Direction.UP: Direction.DOWN,
            Direction.DOWN: Direction.UP,
            Direction.LEFT: Direction.RIGHT,
            Direction.RIGHT: Direction.LEFT
        }
        if dir != forbidden_moves[self._direction]:
            self._direction = dir

    def move(self) -> None:
        """Handles the movement of the snake."""
        x_head, y_head = self._body[0]
        if self._direction == Direction.UP:
            self._body.insert(0, (x_head, y_head - self._block_size))
        elif self._direction == Direction.DOWN:
            self._body.insert(0, (x_head, y_head + self._block_size))
        elif self._direction == Direction.LEFT:
            self._body.insert(0, (x_head - self._block_size, y_head))
        elif self._direction == Direction.RIGHT:
            self._body.insert(0, (x_head + self._block_size, y_head))

        if len(self._body) != self._length:
            self._body.pop()

    def grow(self) -> None:
        """Increases the snake's length by 1."""
        self._length += 1

    def check_self_collision(self) -> bool:
        """Checks if the snake's head collides with its own body."""
        head = self._body[0]
        return head in self._body[1:]
    
    @property
    def score(self) -> int:
        """Returns the current score."""
        return self._length - 1

    def _bfs(self, start: tuple[int, int], target: tuple[int, int], width: int, height: int)\
          -> dict[tuple[int, int], tuple[int, int]]:
        """
        Performs a breadth-first search to find the shortest path to the target.

        Args:
            start: The (x, y) coordinates of the starting node (snake's head).
            target: The (x, y) coordinates of the target node (apple).
            width: The total width of the game grid.
            height: The total height of the game grid.

        Returns:
            A dictionary mapping each visited node to the node it came from.
        """
        queue = deque([start])
        visited = set([start])
        came_from = {}
        directions = [(0, -self._block_size), (0, self._block_size), (-self._block_size, 0),\
                       (self._block_size,0)]
        while queue:
            current_node = queue.popleft()
            if current_node == target:
                break
            for d in directions:
                neighbor = current_node[0] + d[0], current_node[1] + d[1]
                if neighbor not in self._body and neighbor not in visited and neighbor[0] >= 0\
                      and neighbor[0] < width and neighbor[1] >= 0 and neighbor[1] < height:
                    visited.add(neighbor)
                    queue.append(neighbor)
                    came_from[neighbor] = current_node
        return came_from
        
    def _get_path(self, came_from: dict, start: tuple, target: tuple) -> list:
        """
        Reconstructs the shortest path from start to target using the came_from dictionary.

        Args:
            came_from: Dictionary tracking the path history (node: parent).
            start: The (x, y) coordinates of the starting node (snake's head).
            target: The (x, y) coordinates of the target node (apple).

        Returns:
            A list of (x, y) coordinates representing the path from start to target.
            Returns an empty list if the target is unreachable.
        """
        if target not in came_from:
            return list()
        path = list()
        current = target
        while current != start:
            path.append(current)
            current = came_from[current]
        return path[::-1]