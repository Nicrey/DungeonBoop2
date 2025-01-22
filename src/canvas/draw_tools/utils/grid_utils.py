    


def get_grid_start(x,y, grid_starts, grid_size):
    """Takes a point x and returns the x,y coordinates of the grid start"""
    x_tile, y_tile = get_grid_tile(x,y, grid_size)
    return grid_starts[x_tile][y_tile]

def get_grid_tile(x,y, grid_size):
    x_tile = x // grid_size
    y_tile = y // grid_size
    return x_tile, y_tile

def grid_draw_useful(grid_tool, pos):
    x_tile, y_tile = get_grid_tile(pos.x(), pos.y(), grid_tool.grid_size)
    if x_tile == grid_tool.last_grid_x and y_tile == grid_tool.last_grid_y:
        return False
    return True