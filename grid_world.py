import pygame


white = (255, 255, 255)
black = (0, 0, 0)

display_width = 1000
display_height = 600


class Triangle:
    def __init__(self, coords, color, text=''):
        self.coords = coords
        self.color = color

    def draw(self, display):
        pygame.draw.polygon(display, self.color, self.coords)


class Tile:
    def __init__(self, coords, side_size, reward=0.0, border=2):
        self.position = list(coords)
        self.center = (coords[0]*side_size + side_size/2, coords[1]*side_size + side_size/2)
        self.side_size = side_size
        self.color = black

        self.reward = reward

        self.values = [0, 0, 0, 0]

        self.vertices_coords = ((self.center[0] - side_size/2, self.center[1] - side_size/2),
                                (self.center[0] - side_size/2, self.center[1] + side_size/2),
                                (self.center[0] + side_size/2, self.center[1] + side_size/2),
                                (self.center[0] + side_size/2, self.center[1] - side_size/2))

        self.text_points = ((self.center[0] - side_size/2.3, self.center[1]),
                            (self.center[0], self.center[1] + side_size/2.3),
                            (self.center[0] + side_size/2.3, self.center[1]),
                            (self.center[0], self.center[1] - side_size/2.3))

        self.triangles = [Triangle(((self.vertices_coords[0][0] + border, self.vertices_coords[0][1] + 2*border),
                                    (self.vertices_coords[1][0] + border, self.vertices_coords[1][1] - 2*border),
                                    (self.center[0] - border, self.center[1])), white),

                          Triangle(((self.vertices_coords[1][0] + 2*border, self.vertices_coords[1][1] - border),
                                    (self.vertices_coords[2][0] - 2*border, self.vertices_coords[2][1] - border),
                                    (self.center[0], self.center[1] + border)), white),

                          Triangle(((self.vertices_coords[2][0] - border, self.vertices_coords[2][1] - 2*border),
                                    (self.vertices_coords[3][0] - border, self.vertices_coords[3][1] + 2*border),
                                    (self.center[0] + border, self.center[1])), white),

                          Triangle(((self.vertices_coords[3][0] - 2*border, self.vertices_coords[3][1] + border),
                                    (self.vertices_coords[0][0] + 2*border, self.vertices_coords[0][1] + border),
                                    (self.center[0], self.center[1] - border)), white)]

    def draw(self, display, display_values):
        pygame.draw.polygon(display, self.color, self.vertices_coords)

        for triangle in self.triangles:
            triangle.draw(display)

        if display_values:
            font = pygame.font.SysFont("calibri", 32)

            text_surface = font.render("{:.2f}".format(self.values[0]), True, black)
            display.blit(text_surface, dest=(self.text_points[0][0], self.text_points[0][1] - text_surface.get_height()/2))

            text_surface = font.render("{:.2f}".format(self.values[1]), True, black)
            display.blit(text_surface, dest=(self.text_points[1][0] - text_surface.get_width()/2, self.text_points[1][1] - text_surface.get_height()))

            text_surface = font.render("{:.2f}".format(self.values[2]), True, black)
            display.blit(text_surface, dest=(self.text_points[2][0] - text_surface.get_width(), self.text_points[2][1] - text_surface.get_height()/2))

            text_surface = font.render("{:.2f}".format(self.values[3]), True, black)
            display.blit(text_surface, dest=(self.text_points[3][0] - text_surface.get_width()/2, self.text_points[3][1]))


class ExitTile:
    def __init__(self, coords, side_size, reward, border=2):
        self.position = list(coords)
        self.center = (coords[0]*side_size + side_size/2, coords[1]*side_size + side_size/2)
        self.side_size = side_size
        self.color = black
        self.inner_color = white

        self.values = [reward]

        self.reward = reward

        self.vertices_coords = ((self.center[0] - side_size/2, self.center[1] - side_size/2),
                                (self.center[0] - side_size/2, self.center[1] + side_size/2),
                                (self.center[0] + side_size/2, self.center[1] + side_size/2),
                                (self.center[0] + side_size/2, self.center[1] - side_size/2))

        self.inner_coords = ((self.center[0] - side_size/2 + border, self.center[1] - side_size/2 + border),
                             (self.center[0] - side_size/2 + border, self.center[1] + side_size/2 - border),
                             (self.center[0] + side_size/2 - border, self.center[1] + side_size/2 - border),
                             (self.center[0] + side_size/2 - border, self.center[1] - side_size/2 + border))

    def draw(self, display, display_values):
        pygame.draw.polygon(display, self.color, self.vertices_coords)
        pygame.draw.polygon(display, self.inner_color, self.inner_coords)

        if display_values:
            font = pygame.font.SysFont("calibri", 32)

            text_surface = font.render("{:.2f}".format(self.values[0]), True, black)
            display.blit(text_surface, dest=(self.center[0] - text_surface.get_width()/2, self.center[1] - text_surface.get_height()/2))


class Player:
    def __init__(self, grid, initial_pos=(0, 2), color=(0, 0, 180)):
        self.position = list(initial_pos)
        self.color = color

    def draw(self, grid, display):
        pos = tuple(self.position)
        self.vertices_coords = ((grid[pos].center[0] - 25, grid[pos].center[1]),
                       (grid[pos].center[0], grid[pos].center[1] + 25),
                       (grid[pos].center[0] + 25, grid[pos].center[1]),
                       (grid[pos].center[0], grid[pos].center[1] - 25))

        pygame.draw.polygon(display, self.color, self.vertices_coords)


class Game:
    def __init__(self, grid_shape, good_exit_tiles, bad_exit_tiles, tiles_to_pop, display_height, movement_reward=0.0):
        self.grid_shape = grid_shape
        self.grid = {}

        self.display_height = display_height
        self.display_width = int(display_height*(self.grid_shape[0]/self.grid_shape[1]))
        
        tile_width = display_height/grid_shape[1]
        for i in range(grid_shape[0]):
            for j in range(grid_shape[1]):
                self.grid[(i, j)] = Tile((i, j), tile_width, movement_reward)

        for tile_index in good_exit_tiles:
            self.grid[tile_index] = ExitTile(tile_index, tile_width, +1)

        for tile_index in bad_exit_tiles:
            self.grid[tile_index] = ExitTile(tile_index, tile_width, -1)

        for tile_index in tiles_to_pop:
            self.grid.pop(tile_index)

        self.player = Player(self.grid)

    def reset(self):
        self.player = Player(self.grid)

    def update(self, actions):
        self.update_grid_color()

        player_pos = list(self.player.position)

        for action in actions:
            if action == 'right':
                player_pos[0] += 1
            if action == 'left':
                player_pos[0] -= 1
            if action == 'up':
                player_pos[1] -= 1
            if action == 'down':
                player_pos[1] += 1

        if tuple(player_pos) in self.grid:
            self.player.position = player_pos

        reward = self.reward()

        return reward

    def reward(self):
        return self.grid[tuple(self.player.position)].reward

    def get_max_and_min_grid_values(self):
        grid_values = []
        for tile_index in self.grid:
            for value in self.grid[tile_index].values:
                grid_values.append(value)

        return max(grid_values), min(grid_values)

    def update_grid_color(self):
        max_grid_value, min_grid_value = self.get_max_and_min_grid_values()

        for tile_index in self.grid:
            if len(self.grid[tile_index].values) == 4:
                for value, triangle in zip(self.grid[tile_index].values, self.grid[tile_index].triangles):
                    if value > 0:
                        triangle.color = (255 - 255*value/max_grid_value, 255, 255 - 255*value/max_grid_value)
                    if value < 0:
                        triangle.color = (255, 255 - abs(255*value/min_grid_value), 255 - abs(255*value/min_grid_value))
                    if value == 0:
                        triangle.color = white
            else:
                for value in self.grid[tile_index].values:
                    if value > 0:
                        self.grid[tile_index].inner_color = (255 - 255*value/max_grid_value, 255, 255 - 255*value/max_grid_value)
                    if value < 0:
                        self.grid[tile_index].inner_color = (255, 255 - abs(255*value/min_grid_value), 255 - abs(255*value/min_grid_value))
                    if value == 0:
                        self.grid[tile_index].inner_color = white

    def draw(self, display, display_values=True):
        for tile in self.grid:
            self.grid[tile].draw(display, display_values)

        self.player.draw(self.grid, display)
