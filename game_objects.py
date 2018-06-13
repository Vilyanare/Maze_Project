#!/usr/bin/env python3
'''
    contains objects used for game
'''
import json
from constants import (TILE_SIZE, MOVE_SPEED, ROTATION_SPEED, RAY_ANGLE,
                       CENTER_Y)


class GameMap():
    '''
        Class for taking in a file and turning it into a map

        Reads a JSON serialized dicitonary:
            game_map - list of lists with 0's being the empty space
                and 1's being walls.
            start - which grid coord the camera starts on
            direction - which direction the camera is facing in degrees
    '''
    def __init__(self, file_name):
        '''
            initializes class
        '''

        with open(file_name, encoding='utf-8') as a_file:
            self.data = json.load(a_file)

    def get_map(self):
        '''
            retrieves map from dictionary of data
        '''
        return self.data['game_map']

    def camera_pos(self):
        '''
            retrieves start position of camera
        '''
        return self.data['position']

    def camera_dir(self):
        '''
            retrieves start direction of camera
        '''
        return self.data['direction']

    def map_size(self):
        '''
            Size of the map
        '''
        return self.data['size']

    def is_wall(self, coords):
        '''
            checks to see if there is a wall at coords
            Arguments:
                coords - coordinates on grid to check
                (x, y)
            Return:
                True if wall False if not
        '''
        if coords[0] < 0:
            x = 0
        elif coords[0] >= self.map_size()[0]:
            x = self.map_size()[0] - 1
        else:
            x = coords[0]
        if coords[1] < 0:
            y = 0
        elif coords[1] >= self.map_size()[1]:
            y = self.map_size()[1] - 1
        else:
            y = coords[1]
        #print("is_wall real X: {} Y: {} grid X: {} Y: {}".format(coords[0], coords[1], x, y))
        if self.get_map()[y][x]:
            return True
        return False

    def grid_coords(self, coords):
        '''
            rounds coordinates to the size of each grid
            takes in a tuple of x y coordinates
            (x, y)
        '''
        grid_x = coords[0] // TILE_SIZE
        grid_y = coords[1] // TILE_SIZE
        return (int(grid_x), int(grid_y))

    def find_seg_points(self, ray_num, height):
        '''
            find x,y coords of top and bottom of a wall segment
            Arguments:
                ray_num - the ray we are working with
                height - height of wall segment
            Return:
                tuple with top coords and bot coords
        '''
        top_x = int(ray_num * RAY_ANGLE)
        top_y = CENTER_Y - (height // 2)
        bot_y = top_y + height
        return (top_x, top_y, top_x, bot_y)



class Camera():
    '''
        Class defining the camera

        Attributes:
            x - float x coordinate of camera
            y - float y coordinate of camera
            angle - direction camera is facing in degrees
    '''


    def __init__(self, map_data):
        '''
            initialize camera class
        '''
        self.map = map_data
        self.x = map_data.camera_pos()[0] * 64
        self.y = map_data.camera_pos()[1] * 64
        self.angle = map_data.camera_dir() # direction camera is facing
        self._velocity = 0 # how fast your are moving
        self.rot_velocity = 0 # how fast you are turning

    def move(self):
        '''
            moves object by velocity
        '''
        orient = self.get_orientation(self.angle)
        x_veloc = self._velocity * (1 - (self.angle / 90 % 1))
        y_veloc = self._velocity * (self.angle / 90 % 1)
        if (orient[1] == "down" and orient[0] == "right") or (orient[1] == "up" and orient[0] == "left"):
            y_veloc = self._velocity * (1 - (self.angle / 90 % 1))
            x_veloc = self._velocity * (self.angle / 90 % 1)
        if orient[1] == "up":
            y_veloc *= -1
        if orient[0] == "left":
            x_veloc *= -1
        new_coords = self.collision(self.x + x_veloc, self.y + y_veloc)
        self.x = new_coords[0]
        self.y = new_coords[1]
        self.angle = self.three_sixty(self.angle + self.rot_velocity)

    def collision(self, new_x, new_y):
        '''
            Collision detection system
        '''
        if self.map.is_wall(self.map.grid_coords((new_x, self.y))):
            x = self.x
        else:
            x = new_x
        if self.map.is_wall(self.map.grid_coords((self.x, new_y))):
            y = self.y
        else:
            y = new_y
        return (x, y)

    def velocity(self, direction):
        '''
            Controls the setting of velocity argument
        '''
        if direction == "forward":
            self._velocity = MOVE_SPEED
        if direction == "backward":
            self._velocity = -MOVE_SPEED
        if direction == "left":
            self.rot_velocity = -ROTATION_SPEED
        if direction == "right":
            self.rot_velocity = ROTATION_SPEED
        if direction == "stop_move":
            self._velocity = 0
        if direction == "stop_rot":
            self.rot_velocity = 0

    def get_orientation(self, ray_dir=None):
        '''
            set direction of ray
            default ray_dir finds direction of camera
        '''
        if not ray_dir:
            ray_dir = self.angle
        left_right = "right" if 91 <= ray_dir < 271 else "left"
        up_down = "down" if 1 <= ray_dir < 181 else "up"
        return (left_right, up_down)

    def three_sixty(self, num):
        '''
            Keeps number within 360 degree scope
        '''
        if num < 1:
            return num + 360
        elif num > 360:
            return num - 360
        else:
            return num
