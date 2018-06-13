#!/usr/bin/env python3
'''
Defines constants for game
'''
import math
# the width of the screen in pixels.
SCREEN_WIDTH = 1024

# the height of the screen in pixels
SCREEN_HEIGHT = 768

# size of a (square) tile's side in arbitrary units.
TILE_SIZE = 64

# maximum frames per second that should be drawn
LIMIT_FPS = 30

# True for border False for no border
BORDER = True

# the window's background color (RGBA, from 0-255)
WINDOW_COLOR = (0, 0, 0, 255)

# title of the window
TITLE = "MazeRunner"

# path to map file
MAP_PATH = "map_file4.json"

# height of character
CHARACTER_HEIGHT = 32

# how wide player can see
FOV = 60

# y coord of center of the screen
CENTER_Y = SCREEN_HEIGHT // 2

# distance from player the view plane sits
VIEW_PANE_DISTANCE = SCREEN_WIDTH // 2 // math.tan((math.radians(FOV // 2)))

# how many units you want the player to move per second
MOVE_SPEED = 32
ROTATION_SPEED = 20

# degree of difference between rays
RAY_ANGLE = SCREEN_WIDTH / FOV

# if True activate debug functions
DEBUG_MODE = False
"""
.maze:
    draw_walls now draws red lines where ray segmentation should be
"""
