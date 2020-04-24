from grid_world import *
from game_maps import *

import numpy as np


class QLearningAgent:
    def __init__(self, q_table_shape, discount_factor, learning_rate, exploration_rate):
        self.DISCOUNT_FACTOR = discount_factor
        self.LEARNING_RATE = learning_rate
        self.EXPLORATION_RATE = exploration_rate

        self.q_table = np.zeros(q_table_shape)

    def update_q_table(self, transition):
        state, action, reward, new_state = transition

        max_future_q = np.max(self.q_table[tuple(new_state)])
        current_q = self.q_table[tuple(state) + (action,)]
        new_q = current_q + self.LEARNING_RATE * (reward + self.DISCOUNT_FACTOR * max_future_q - current_q)

        self.q_table[tuple(state) + (action,)] = new_q

    def take_action(self, state):
        if np.random.uniform() < (1 - self.EXPLORATION_RATE):
            action = np.argmax(self.q_table[tuple(state)])
        else:
            action = np.random.randint(0, self.q_table.shape[-1])
        return action


game = the_box

total_actions = ['left', 'down', 'right', 'up']
action_indices = {'left': 0, 'down': 1, 'right': 2, 'up': 3}
actions = [0, 1, 2, 3]

q_table_shape = list(game.grid_shape + (len(actions),))
agent = QLearningAgent(q_table_shape=q_table_shape, discount_factor=0.99, learning_rate=0.95, exploration_rate=0.65)


pygame.init()
game_display = pygame.display.set_mode((game.display_width, game.display_height))
clock = pygame.time.Clock()
tick = 20

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        if event.type == pygame.KEYDOWN:
            if event.key == 270: # key plus
                agent.EXPLORATION_RATE += 0.05
                agent.EXPLORATION_RATE = np.clip(agent.EXPLORATION_RATE, 0, 1)

                print('setting exploration rate to', "{:.2f}".format(agent.EXPLORATION_RATE))

            if event.key == 269: # key sub
                agent.EXPLORATION_RATE -= 0.05
                agent.EXPLORATION_RATE = np.clip(agent.EXPLORATION_RATE, 0, 1)

                print('setting exploration rate to', "{:.2f}".format(agent.EXPLORATION_RATE))

            if event.key == 273: # key up
                tick = 10000

            if event.key == 274: # key down
                tick = 20

    state = game.player.position

    actions = []
    actions.append(total_actions[agent.take_action(state)])
    action = action_indices[actions[0]]

    reward = game.update(actions)

    new_state = game.player.position

    transition = [state, action, reward, new_state]

    if type(game.grid[tuple(new_state)]) is Tile:
        agent.update_q_table(transition)
        game.grid[tuple(state)].values[action] = agent.q_table[tuple(state) + (action,)]
    else:
        agent.q_table[tuple(state) + (action,)] = game.grid[tuple(new_state)].reward
        game.grid[tuple(state)].values[action] = game.grid[tuple(new_state)].reward
        game.reset()

    game.update_grid_color()
    game_display.fill(white)
    game.draw(game_display, display_values=False)

    pygame.display.update()
    clock.tick(tick)
