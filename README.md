In this project, I designed a simple Snake game utilizing Q-learning, a popular
reinforce.The objective of this project is to design and implement a simple Snake game
using Q-learning, a widely applied reinforcement learning algorithm. The primary goal
is to allow the snake to continuously consume food while avoiding collisions with
walls, itself, and randomly generated obstacles. By utilizing a Q-learning agent, the
game enables the agent to learn optimal decision-making strategies based on rewards
and penalties, thereby enhancing the effectiveness of the gameplay strategy. 

The main objective of the game is for the snake to eat food, resulting in its growth.
The player controls the snake's movement and must navigate within a defined grid
space while avoiding collisions with walls, itself, or randomly generated obstacles. If
a collision occurs, the game ends. The rules of the game are straightforward and easy
to understand, allowing novice players to quickly get the hang of it. At the start of the
game, the snake's length is one segment, and with each food consumed, its length
increases, thereby raising the difficulty level.

Action Space
The possible actions the agent can take include moving up, down, left, or right. These
are represented as coordinate changes:
Up: (0, -GRID_SIZE)
Down: (0, GRID_SIZE)
Left: (-GRID_SIZE, 0)
Right: (GRID_SIZE, 0)

Reward Function
Designing a reasonable reward function is crucial for reinforcement learning. To
incentivize the agent to progress toward the objective, we designed the following
reward mechanism:
For desirable actions, positive rewards are given:
Eating food grants a reward of +10, encouraging the snake to consume as much food
as possible. Moving closer to food provides a reward of +1, motivating the agent to approach the
food. Exploring new areas yields a reward of +0.5, rewarding the agent for discovering
unknown regions. For undesirable actions, negative rewards are assigned:
Colliding with walls or obstacles results in -10, penalizing erroneous actions. Moving away from food incurs a -1 penalty, encouraging the agent to remain near the
food. This design ensures that the agent learns which behaviors are beneficial and which are
harmful, thereby enhancing its decision-making capabilities.

The user interface continuously displays the current state of the game, including:
The position and length of the snake. The position of the food. The locations of obstacles. The actions taken by the agent. The rewards and penalties received. This design allows players to stay informed about game progress, enhancing
interactivity. By displaying this information, players can better understand the agent's
decision-making process, thereby increasing the game's enjoyment and educational
value.
