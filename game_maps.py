from grid_world import Game


display_height = 600

std_grid_world = Game(grid_shape=(4, 3),
						   good_exit_tiles=[(3, 0)],
						   bad_exit_tiles=[(3, 1)],
						   tiles_to_pop=[(1, 1)],
						   display_height=display_height)

std_grid_world_small_mov_penality = Game(grid_shape=(4, 3),
						   good_exit_tiles=[(3, 0)],
						   bad_exit_tiles=[(3, 1)],
						   tiles_to_pop=[(1, 1)],
						   display_height=display_height,
						   movement_reward=-0.2)

std_grid_world_high_mov_penality = Game(grid_shape=(4, 3),
						   good_exit_tiles=[(3, 0)],
						   bad_exit_tiles=[(3, 1)],
						   tiles_to_pop=[(1, 1)],
						   display_height=display_height,
						   movement_reward=-20)

the_box = Game(grid_shape=(10, 10),
			   good_exit_tiles=[(9, 9)],
			   bad_exit_tiles=[],
			   tiles_to_pop=[(0, 3), (1, 3), (2, 3), (3, 3), (4, 3), (4, 2), (4, 1),
			   				 (4, 4), (5, 4), (7, 4), (8, 4), (9, 4), (7, 5), (7, 6),
			   				 (6, 6), (5, 6), (4, 6), (3, 6), (2, 6), (2, 7), (6, 8),
			   				 (6, 9), (2, 8)],
			   display_height=display_height,
			   movement_reward=-0.2)