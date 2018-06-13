#!/usr/bin/env python3
'''
Module containing all classes needed for raycasting

classes:
    MapGenerator - pulls in data from json file
'''
import math
from constants import (TILE_SIZE, FOV)


class RayCast():
    '''
        Class that does all the math to cast a ray
    '''

    def __init__(self, camera, game_map):
        '''
            initializing method
            Attributes:
                camera - camera object
        '''
        self.camera = camera
        self.orientation = None
        self.game_map = game_map
        self.map_size = self.game_map.map_size()
        self.grid_coords = game_map.grid_coords

    def cast(self):
        '''
            cast all rays in field of view
            Returns:
                List tuples with orientation and distance of walls
                    Len based on FOV
                    ("vertical", distance)
        '''
        ray_dir = self.camera.three_sixty(self.camera.angle - (FOV // 2))
        dist_list = []
        for x in range(FOV):
            self.orientation = self.camera.get_orientation(ray_dir)
            dist_list.append(self.find_wall(ray_dir))
            ray_dir = self.camera.three_sixty(ray_dir + 1)
            #print("Ray", x, dist_list[x], ray_dir)
        return dist_list

    def find_wall(self, ray_dir):
        '''
            finds first vertical and horizontal wall and returns closest one
            Arguments:
                ray_dir - degree of direction the ray is traveling
            Return:
                tuple containing distance and orientation of the closest wall
                    the ray collides with. ("vertical", distance)
        '''
        h_d = "horizontal"
        horiz_node = self.first_node(h_d, ray_dir)
        #print("First horizontal node: ", horiz_node)
        horiz_dist = self.node_distance(horiz_node, h_d, ray_dir)
        while (self.game_map.is_wall(self.grid_coords(horiz_node)) == False):
            horiz_node = (
                horiz_node[0] + horiz_dist[0], horiz_node[1] + horiz_dist[1])
        horiz_len = self.ray_len(horiz_node, ray_dir)
        v_d = "vertical"
        vert_node = self.first_node(v_d, ray_dir)
        #print("First vertical node: ", vert_node)
        vert_dist = self.node_distance(vert_node, v_d, ray_dir)
        while (self.game_map.is_wall(self.grid_coords(vert_node)) == False):
            vert_node = (
                vert_node[0] + vert_dist[0], vert_node[1] + vert_dist[1])
        vert_len = self.ray_len(vert_node, ray_dir)
        #print("Final nodes  Vert: {} Horizontal {}".format(vert_node, horiz_node))
        #print("Distances Vert: {} Horiz: {}".format(vert_len, horiz_len))
        #print("Node spacing Vert: {} Horiz {}".format(vert_dist, horiz_dist))
        if vert_len < horiz_len:
            return (v_d, vert_len, vert_node)
        else:
            return (h_d, horiz_len, horiz_node)

    def first_node(self, line_dir, ray_dir):
        '''
            finds first line that ray hits on the grid
            arguments:
                line_dir - horizontal or vertical which direction on the grid
                    you want to check for
                ray_dir - direction that the ray is traveling in
            Return:
                tuple with (x, y) coordinates
        '''
        if line_dir == "horizontal":
            if self.orientation[1] == "down":
                A_y = (self.camera.y // TILE_SIZE) * (TILE_SIZE) + TILE_SIZE
            else:
                A_y = (self.camera.y // TILE_SIZE) * (TILE_SIZE) - 1

            A_x = self.camera.x + (self.camera.y - A_y) / math.tan(math.radians(ray_dir))
            return (A_x, A_y)

        else:
            if self.orientation[0] == "left":
                B_x = (self.camera.x // TILE_SIZE) * (TILE_SIZE) - 1
            else:
                B_x = (self.camera.x // TILE_SIZE) * (TILE_SIZE) + TILE_SIZE

            B_y = self.camera.y + (self.camera.x - B_x) * math.tan(math.radians(ray_dir))

            return (B_x, B_y)


    def node_distance(self, coords, line_dir, ray_dir):
        '''
            distance between nodes after you found the first plot
            Arguments:
                line_dir - vertical or horizontal
                ray_dir - which direction the ray is traveling
            Returns:
                tuple with (xdist, ydist)
        '''
        map_units_x = TILE_SIZE * (self.map_size[0] - 1)
        map_units_y = TILE_SIZE * (self.map_size[1] - 1)
        if line_dir == "horizontal":
            xdist = TILE_SIZE / abs(math.tan(math.radians(ray_dir)))
            ydist = TILE_SIZE
            #print("xdist: ", xdist)
        else:
            xdist = TILE_SIZE
            ydist = TILE_SIZE * abs(math.tan(math.radians(ray_dir)))
            #print("ydist: ", ydist)
        if (-map_units_x > int(xdist)) or (int(xdist) > map_units_x) or (int(xdist) == 0):
            xdist = 0
        if (-map_units_y > int(ydist)) or (int(ydist) > map_units_y) or (int(ydist) == 0):
            ydist = 0
        if self.orientation[1] == "up":
            ydist *= -1
        if self.orientation[0] == "left":
            xdist *= -1
        return (int(xdist), int(ydist))

    def ray_len(self, end_node, ray_dir):
        '''
            return length of ray from the camera to the wall
            Arguments:
                end_node - last node of the line
                ray_dir - direction the ray is traveling
            Return:
                length of the ray
        '''
        anti_fish = math.cos(math.radians(ray_dir - self.camera.angle))
        # print("Anti_fish", anti_fish)
        first = abs((self.camera.y - end_node[1]) / math.sin(math.radians(ray_dir))) * anti_fish
        second = abs((self.camera.x - end_node[0]) / math.cos(math.radians(ray_dir))) * anti_fish
        # print("Ray lengths  First: {}  Second: {}".format(first, second))
        # print("Nodes real: ({}, {}) grid: {}".format(end_node[0], end_node[1], self.grid_coords(end_node)))
        return first if first > second else second
