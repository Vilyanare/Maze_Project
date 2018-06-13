#!/usr/bin/env python3
import sdl2
from manager import Manager, SceneBase, Resources
from raycast import RayCast
from game_objects import GameMap, Camera
from colors import *
from constants import (SCREEN_HEIGHT, SCREEN_WIDTH, TILE_SIZE, VIEW_PANE_DISTANCE,
                       FOV, DEBUG_MODE, MAP_PATH, RAY_ANGLE)


class Maze(SceneBase):
    """An aspiring Maze game's scene."""


    def __init__(self, **kwargs):
        """Initialization."""
        # Nothing there for us but lets call super in case we implement
        # something later on, ok?
        super().__init__(**kwargs)

        # toggle for the pause button
        self.on_off = True

        # Load map data
        self.game_map = GameMap(MAP_PATH)

        # Create player
        start = self.game_map
        self.player = Camera(start)

        # Set up raycasting engine with player and map data
        self.ray = RayCast(self.player, self.game_map)

        self.new_render = True
        self.debug_mode = DEBUG_MODE

    def draw_wall(self):
        '''
            draws a frame of walls and returns a list of sprites
            DEBUG_MODE draws red lines where the ray seperations are supposed to be.
        '''
        constant = TILE_SIZE * VIEW_PANE_DISTANCE
        wall_distances = self.ray.cast()
        x_vert = []
        y_vert = []
        debug_lines = []
        for idx, val in enumerate(wall_distances):
            orient = val[0]
            height = int(constant // val[1])
            debug_lines.append(self.game_map.find_seg_points(idx, height))
            if idx == 0:
                prev_distance = val[1]
                prev_height = height
                prev_orient = val[0]
                points = self.game_map.find_seg_points(idx, height)
                x_vert = x_vert + [points[0], points[2]]
                y_vert = y_vert + [points[1], points[3]]
            points = self.game_map.find_seg_points(idx, height)
            x_vert = x_vert + [points[0], points[2]]
            y_vert = y_vert + [points[3], points[1]]
            color = GREY if val[0] == "horizontal" else DARK_GREY
            if idx == FOV -1:
                x_vert[2] = SCREEN_WIDTH
                x_vert[3] = SCREEN_WIDTH
            if self.new_render:
                if abs(val[1] - prev_distance) >   RAY_ANGLE:
                    if prev_height - height < 0:
                        self.manager.polygonRGBA(x_vert, y_vert[:2] + y_vert[1::-1], 4, color)
                    else:
                        self.manager.polygonRGBA(x_vert, y_vert[:1:-1] + y_vert[2:], 4, color)
                else:
                    self.manager.polygonRGBA(x_vert, y_vert, 4, color)
            else:
                self.manager.polygonRGBA(x_vert, y_vert, 4, color)
            del x_vert[:2]
            y_vert[0] = y_vert[3]
            y_vert[1] = y_vert[2]
            del y_vert[2:]
            prev_orient = val[0]
            prev_height = height
            prev_distance = val[1]

        if self.debug_mode:
            for idx, val in enumerate(debug_lines):
                self.renderer.draw_line((val), color=RED)

    def on_key_press(self, event, sym, mod):
        """Called on keyboard input, when a key is **held down**.

        Args:
            event (sdl2.events.SDL_Event): The base event, as passed by SDL2.
                Unless specifically needed, sym and mod should be used
                instead.
            sym (int): Integer representing code of the key pressed. For
                printable keys ``chr(key)`` should return the corresponding
                character.
            mod (KeyboardStateController): the keyboard state for modifiers
                and locks. See :class:KeyboardStateController
        """
        if sym == sdl2.SDLK_LEFT:
            self.player.velocity("left")
        if sym == sdl2.SDLK_RIGHT:
            self.player.velocity("right")
        if sym == sdl2.SDLK_UP:
            self.player.velocity("forward")
        if sym == sdl2.SDLK_DOWN:
            self.player.velocity("backward")
        if sym == sdl2.SDLK_SPACE:
            self.on_off = not self.on_off
        if sym == sdl2.SDLK_p:
            self.debug_mode = not self.debug_mode
        if sym == sdl2.SDLK_o:
            self.new_render = not self.new_render

    def on_key_release(self, event, sym, mod):
        """Called on keyboard input, when a key is **released**.

        By default if the Escape key is pressed the manager quits.
        If that behaviour is desired you can call ``super().on_key_release(
        event, sym, mod)`` on a child class.

        Args:
            event (sdl2.events.SDL_Event): The base event, as passed by SDL2.
                The other arguments should be used for a higher level
                interaction, unless specifically needed.
            sym (int): Integer representing code of the key pressed. For
                printable keys ``chr(key)`` should return the corresponding
                character.
            mod (KeyboardStateController): the keyboard state for modifiers
                and locks. See :class:KeyboardStateController
        """
        if sym == sdl2.SDLK_UP or sym == sdl2.SDLK_DOWN:
            self.player.velocity("stop_move")
        if sym == sdl2.SDLK_LEFT or sym == sdl2.SDLK_RIGHT:
            self.player.velocity("stop_rot")
        if sym == sdl2.SDLK_ESCAPE:
            self.quit()

    def on_update(self):
        """Graphical logic."""
        # Pause button
        if self.on_off:
            # Blanks the screen
            self.renderer.clear(self.manager.window_color)

            # Update player poisition based on input keys
            self.player.move()

            # Draws the background colors
            self.renderer.fill((0, 0 // 2, SCREEN_WIDTH, SCREEN_HEIGHT // 2), color=BLUE)
            self.renderer.fill((0, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT // 2), color=GREEN)

            # Draws in the walls.
            self.draw_wall()


            #print("Player Direction: {} Orientation: {} Coords: ({})".format(self.player.angle, self.player.get_orientation(), self.game_map.grid_coords((self.player.x, self.player.y))))


if __name__ == '__main__':
    # create a game/Manager instance
    m = Manager(window_color=BLACK, border=False)
    m.set_scene(scene=Maze)

    m.run()
