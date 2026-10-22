# Snake AI — Pathfinding vs Reinforcement learning

A classic Snake game built with `pygame`, extended with two different AI approaches to control the snake : a deterministic **BFS pathfinding agent** and a self-taught **Q-learning agent** trained from scratch using the Bellman equation.

This project was my introduction to reinforcement learning, going from "make the snake move" to "make the snake learn to survive" one step at a time.

## Features

- Playable classic Snake (arrow-key controls)
- **BFS agent**: computes the shortest path to the apple in real time, with fallback strategies when no safe path exists
- **Q-Learning agent**: learns a policy purely from trial and error over thousands of episodes, no hardcoded pathfinding
- Score and high-score tracking

## Project Structure

```
├── game.py        # Main game loop, rendering, environment logic
├── snake.py       # Snake entity: movement, growth, BFS pathfinding
├── apple.py       # Apple spawning logic
├── direction.py   # Direction enum
├── agent.py       # Q-learning agent: state extraction, action selection, Bellman update
└── train.py       # Training entry point
```

## How it works

### 1. The game engine

The game runs on a grid (default 600×400, 20px blocks, can be changed in `game.py`). It supports two entry points:

- `game.py` — interactive mode: choose **1** for a human player, **2** for the BFS AI
- `train.py` — trains the Q-learning agent over a large number of episodes (default 10,000, can be changed) at higher speed

### 2. Approach #1 - BFS pathfinding

At every step, the snake runs a breadth-first search from its head to the apple, avoiding its own body, and takes the first step of the shortest path found.

If no path to the apple exists (the snake would trap itself), it falls back to chasing its own tail — buying time and reducing the risk of an immediate dead end. If even that fails, it falls back to a survival heuristic. Among the immediately safe moves, it picks the one that maximizes the reachable space, via flood-fill. This favors staying in open areas instead of just diving into the end. The snake evaluates all three levels (apple, then tail and finally survival) every single step, so when the apple is reachable again, the snake goes back to the fastest way into it.

This approach is **deterministic**: no training, no learning, just a shortest-path strategy re-computed every frame.

### 3. Approach #2 - Q-learning

The Q-Learning agent has no notion of pathfinding. It only knows:

**State (11 booleans):**
- Danger straight ahead / to the left / to the right (relative to current heading)
- Current direction (up / down / left / right)
- Apple position relative to the head (left / right / up / down)

**Actions (3, relative to heading):** turn left, go straight, turn right — this avoids representing the 4 absolute directions, which would allow an illegal instant U-turn.

**Reward:** `+10` for eating an apple, `-100` on death, `0` otherwise.

**Update rule (Bellman equation):**

```
Q(s, a) ← Q(s, a) + α · [ R + γ · max(Q(s', a')) − Q(s, a) ]
```

**Hyperparameters:**

| Parameter | Default value | Role |
|---|---|---|
| α (learning rate) | 0.15 | How much new information overrides old estimates |
| γ (discount factor) | 0.99 | How much future rewards matter vs immediate ones |
| ε (exploration rate) | 1.0 → 0.01 | Probability of taking a random action |
| ε decay | 0.9994 / episode | Gradual shift from exploration to exploitation |
| Episodes | 10,000 | Training length |

The agent starts with a completely empty Q-table and pure random exploration (ε = 1), and progressively shifts toward exploiting what it has learned as ε decays.

## Results & Analysis

| | BFS | Q-Learning |
|---|---|---|
| Typical high score | 50 – 110 | 60 – 70 |
| Consistency | Irregular | Regular |
| Peak potential | Higher ceiling | Lower ceiling |
| Needs training? | No | Yes |

**Interpretation:**

- **BFS is a greedy, single-objective planner.** It optimizes purely for "shortest path to the apple right now," with no awareness of the long-term consequences of the shape it forces its own body into. This produces high variance: when the board layout stays favorable, BFS plays near-optimally and pushes very high scores. When the snake's growing body starts boxing in future paths, runs end early. It never reasons about avoiding that risk, it only reacts to it once already trapped, via the tail-chasing fallback.

- **Q-Learning trades ceiling for consistency.** Because its state is limited to immediate danger detection, it never plans more than one step ahead and has no explicit notion of "shortest path." What it learns instead is closer to a cautious, generalizable survival policy : avoid immediate danger, drift toward the apple. That's enough to reliably reach the 60–70 range, but the same lack of lookahead caps how high it can climb — it can't foresee that a locally safe move might box it in a few steps later. Furthermore, using more than 10,000 episodes seems useless. I tried to go further with a 100,000 episodes training, but the results were not better, despite the process being longer. This can be explained by the fact that I only tried with the default grid, more episodes would be useful for a bigger one.

In short: BFS optimizes locally-perfect decisions with no risk-awareness, while Q-Learning optimizes risk-awareness with no explicit planning. The two failure modes are almost complementary, which points to the improvements below.

## Getting Started

### Prerequisites

- pygame

```bash
pip install pygame
```

### Run

```bash
# Play or watch the BFS AI
python game.py

# Train the Q-learning agent from scratch
python train.py
```

## Key Takeaways

- Implementing BFS for real-time pathfinding under moving constraints
- Framing a game as a Markov decision process (states, actions, rewards)
- Understanding and coding the Bellman equation for Q-learning
- Balancing exploration vs exploitation
- Designing a compact, generalizable state representation

## Possible Improvements

- Richer state for the Q-learning agent (for instance distance to walls/body in each direction, or apple distance rather than just direction)
- Persist and reload the trained Q-table instead of retraining from scratch each run
- Try a Deep Q-network (DQN) to scale beyond a discrete state space
- Systematic hyperparameter comparison (α, γ, decay schedule)
- A hybrid agent : use BFS for planning when a safe path exists, fall back to the learned policy otherwise
- For the BFS strategy, implementing the Hamiltonian cycle would make the results better.
