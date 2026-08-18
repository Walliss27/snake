"""
Module defining the Q-learning AI agent.

This module contains the Agent class which implements the reinforcement 
learning logic, state evaluation, and Q-table updates using the Bellman equation.
"""

import random
from game import Game
from direction import Direction

class Agent:
    """
    Represents the reinforcement learning agent using Q-learning.

    The agent interacts with the game environment, stores knowledge in a Q-table, 
    and balances exploration (random moves) with exploitation (best known moves) 
    to maximize its score over time.
    """

    def __init__(self):
        """
        Initializes the Q-learning AI agent.
        
        Sets up the empty Q-table and defines the hyperparameters for learning 
        (alpha, gamma) and exploration (epsilon, epsilon_decay).
        """
        self._q_table = {}
        self._alpha = 0.15
        self._gamma = 0.99
        self._epsilon = 1
        self._epsilon_min = 0.01
        self._epsilon_decay = 0.9994

    @property
    def epsilon(self) -> float:
        """Gets the current exploration rate (epsilon)."""
        return self._epsilon

    @epsilon.setter
    def epsilon(self, value: float) -> None:
        """
        Sets the exploration rate (epsilon).

        Args:
            value (float): The new epsilon value, clamped between 0.0 and 1.0.
        """
        self._epsilon = max(0.0, min(1.0, value))

    @property
    def epsilon_min(self) -> float:
        """Gets the minimum exploration rate threshold."""
        return self._epsilon_min

    @property
    def epsilon_decay(self) -> float:
        """Gets the decay rate applied to epsilon after each episode."""
        return self._epsilon_decay

    def get_state(self, game) -> tuple:
        """
        Calculates the current state of the environment from the snake's perspective.

        The state acts as the "eyes" of the agent, returning an 11-value array 
        representing immediate dangers, current movement direction, and the 
        relative position of the apple.

        Args:
            game (Game): The current game instance to extract state variables from.

        Returns:
            tuple: An 11-element boolean tuple containing:
                - danger_straight (bool)
                - danger_left (bool)
                - danger_right (bool)
                - dir_l (bool): Moving left
                - dir_r (bool): Moving right
                - dir_u (bool): Moving up
                - dir_d (bool): Moving down
                - apple_left (bool)
                - apple_right (bool)
                - apple_up (bool)
                - apple_down (bool)
        """
        head_x, head_y = game.snake.body[0]
        apple_x = game.apple.x
        apple_y = game.apple.y
        dir_l = game.snake.direction == Direction.LEFT
        dir_r = game.snake.direction == Direction.RIGHT
        dir_u = game.snake.direction == Direction.UP
        dir_d = game.snake.direction == Direction.DOWN
        apple_left = apple_x < head_x
        apple_right = apple_x > head_x
        apple_up = apple_y < head_y
        apple_down = apple_y > head_y
        pt_left = (head_x - game.block_size, head_y)
        pt_right = (head_x + game.block_size, head_y)
        pt_up = (head_x, head_y - game.block_size)
        pt_down = (head_x, head_y + game.block_size)
        danger_straight = (dir_r and game.is_collision(pt_right)) or \
                        (dir_l and game.is_collision(pt_left)) or \
                        (dir_u and game.is_collision(pt_up)) or \
                        (dir_d and game.is_collision(pt_down))

        danger_left = (dir_u and game.is_collision(pt_left)) or \
                        (dir_d and game.is_collision(pt_right)) or \
                        (dir_l and game.is_collision(pt_down)) or \
                        (dir_r and game.is_collision(pt_up))

        danger_right = (dir_u and game.is_collision(pt_right)) or \
                        (dir_d and game.is_collision(pt_left)) or \
                        (dir_l and game.is_collision(pt_up)) or \
                        (dir_r and game.is_collision(pt_down))
        
        return (danger_straight, danger_left, danger_right,
            dir_l, dir_r, dir_u, dir_d,
            apple_left, apple_right, apple_up, apple_down)

    def get_action(self, state: tuple) -> int:
        """
        Determines the next action to take using an epsilon-greedy strategy.

        If the current state is not yet in the Q-table, it initializes it with zero values 
        for all possible actions. The agent either explores by picking a random action 
        (with probability epsilon) or exploits by choosing the action with the highest 
        Q-value for the current state.

        Args:
            state (tuple): The current 11-value state representation of the environment.

        Returns:
            int: The selected action (0: turn left, 1: go straight, 2: turn right).
        """
        if state not in self._q_table:
            self._q_table[state] = [0, 0, 0]
        rand_num = random.random()
        if rand_num < self._epsilon:
            return random.randint(0, 2)
        else:
            return self._q_table[state].index(max(self._q_table[state]))
          

    def update_q_table(self, state: tuple, action: int, reward: int, next_state: tuple, done: bool) -> None:
        """
        Updates the Q-table using the Bellman equation.

        Applies the Q-learning update rule to adjust the value of the taken action
        in the given state. If the game is over (done is True), the future expected 
        reward is ignored.
        
        The Bellman update formula used is:
        $Q(s, a) \leftarrow Q(s, a) + \alpha \cdot (R + \gamma \max Q(s', a') - Q(s, a))$

        Args:
            state (tuple): The state of the environment before taking the action.
            action (int): The action chosen and executed by the agent.
            reward (int): The reward received immediately after taking the action.
            next_state (tuple): The new state of the environment after the action.
            done (bool): True if the action resulted in a terminal state (game over), False otherwise.
        """
        if next_state not in self._q_table:
            self._q_table[next_state] = [0, 0, 0]
        if done:
            self._q_table[state][action] += self._alpha * (reward - self._q_table[state][action])
        else:
            self._q_table[state][action] += self._alpha * (reward + self._gamma * max(self._q_table[next_state]) - self._q_table[state][action])
