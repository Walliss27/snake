"""
Module serving as the entry point for AI training.

Initializes the Pygame environment and the Q-learning agent, manages 
the training loop over multiple episodes, and displays the final statistics.
"""

import sys
import pygame
from game import Game
from agent import Agent

def train():
    """
    Executes the training loop for the Q-learning agent.
    
    Initializes the game and the agent, then runs the game for a set 
    number of episodes. It forces the game to run at maximum speed 
    and occasionally renders the display to track visual progress.
    Saves the best score and keeps the window open upon completion.
    """
    agent = Agent()
    game = Game(600, 400)
    num_episodes = 10000
    game.fps = 10000

    for episode in range(num_episodes):
        game.reset()
        done = False
        show_display = (episode % 200 == 0)

        while not done:
            state = agent.get_state(game)
            action = agent.get_action(state)
            reward, done, score = game.play_step(action, render=show_display)
            next_state = agent.get_state(game)
            agent.update_q_table(state, action, reward, next_state, done)

        agent.epsilon = max(agent.epsilon_min, agent.epsilon * agent.epsilon_decay)
        print(f"Episode {episode + 1} - Score: {score} - Epsilon: {agent.epsilon:.2f}")

    print(f"High score : {game.high_score}")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        game.draw()

if __name__ == '__main__':
    train()