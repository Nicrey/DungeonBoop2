    


import math


def get_grid_start(x,y, grid_starts, grid_size, grid_angle):
    """Takes a point x and returns the x,y coordinates of the grid start"""
    x_tile, y_tile = get_grid_tile(x,y, grid_size, grid_angle)
    return grid_starts[(x_tile, y_tile)]

def get_grid_tile(x,y, grid_size, angle=0):
    x,y = rotate_point(x,y,angle)
    x_tile = x // grid_size
    y_tile = y // grid_size
    return x_tile, y_tile

def grid_draw_useful(grid_tool, pos):
    x_tile, y_tile = get_grid_tile(pos.x(), pos.y(), grid_tool.grid_size, grid_tool.grid_angle)
    if x_tile == grid_tool.last_grid_x and y_tile == grid_tool.last_grid_y:
        return False
    return True

def rotate_point(x,y, angle=-45):
    radians = math.radians(angle)
    cos_angle = math.cos(radians)
    sin_angle = math.sin(radians)
    x_rotated = x * cos_angle + y * sin_angle
    y_rotated = -x * sin_angle + y * cos_angle
    return (int(x_rotated), int(y_rotated))