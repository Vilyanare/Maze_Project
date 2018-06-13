from manager import Manager, SceneBase, Resources
import sdl2
from raycast import RayCast
from game_objects import GameMap, Camera
from constants import *
from colors import *

class TestScene(SceneBase):
    """A test scene."""

    def __init__(self, **kwargs):
        """Initialization."""
        # Nothing there for us but lets call super in case we implement
        # something later on, ok?
        super().__init__(**kwargs)

        # Load map data
        self.game_map = GameMap(MAP_PATH)

        # Create player
        self.player = Camera(self.game_map)
        self.map_size = self.game_map.map_size()

        # Set up raycasting engine with player and map data
        self.ray = RayCast(self.player, self.game_map)

        #Draw the grid and walls to the map
        if SCREEN_HEIGHT < SCREEN_WIDTH:
            sqr_size = SCREEN_HEIGHT // self.map_size[1]
            count = self.map_size[1]
        else:
            sqr_size = SCREEN_WIDTH // self.map_size[0]
            count = self.map_size[0]
        base_x = (SCREEN_WIDTH - (sqr_size * count)) // 2
        base_y = (SCREEN_HEIGHT - (sqr_size * count)) // 2
        self.x_offset = base_x
        self.y_offest = base_y
        self.sqr_width = (sqr_size * self.map_size[0])
        self.sqr_height = (sqr_size * self.map_size[1])
        self.grid = []
        self.walls = []
        for gy in range(self.map_size[1]):
            for gx in range(self.map_size[0]):
                rect = base_x + gx * sqr_size, base_y + gy * sqr_size, sqr_size, sqr_size
                if self.game_map.is_wall((gx, gy)):
                    self.walls.append(rect)
                else:
                    self.grid.append(rect)

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
            self.player.velocity("right")
        if sym == sdl2.SDLK_RIGHT:
            self.player.velocity("left")
        if sym == sdl2.SDLK_UP:
            self.player.velocity("forward")
        if sym == sdl2.SDLK_DOWN:
            self.player.velocity("backward")
        if sym == sdl2.SDLK_SPACE:
            self.on_off = not self.on_off

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
    def draw_player(self):
        '''
            function to draw the player
        '''
        player_x = int((self.player.x / (TILE_SIZE * self.map_size[0])) * self.sqr_width) + self.x_offset
        player_y = int((self.player.y / (TILE_SIZE * self.map_size[1])) * self.sqr_height) + self.y_offest
        self.renderer.fill((player_x, player_y, 5, 5), color=RED)

    def draw_lines(self):
        '''
            function to draw raycast lines
        '''
        rays = self.ray.cast()
        player_x = int((self.player.x / (TILE_SIZE * self.map_size[0])) * self.sqr_width) + self.x_offset
        player_y = int((self.player.y / (TILE_SIZE * self.map_size[1])) * self.sqr_height) + self.y_offest

        for x in rays:
            dest_x = int((x[2][0] / (TILE_SIZE * self.map_size[0])) * self.sqr_width) + self.x_offset
            dest_y = int((x[2][1] / (TILE_SIZE * self.map_size[1])) * self.sqr_height) + self.y_offest
            self.renderer.draw_line((player_x, player_y, dest_x, dest_y), color=RED)

    def on_update(self):
        """Graphical logic."""
        # render main window and clear it every frame
        self.player.move()
        self.renderer.clear(self.manager.window_color)
        self.renderer.draw_rect(self.grid, color=GREY)
        self.renderer.fill(self.walls, color=GREY)
        self.draw_player()
        self.draw_lines()
        #print("Player Direction: {} Orientation: {} Coords: ({})".format(self.player.angle, self.player.get_orientation(), self.game_map.grid_coords((self.player.x, self.player.y))))

if __name__ == '__main__':
    # create a game/Manager instance
    m = Manager(window_color=WHITE, border=False)

    m.set_scene(scene=TestScene)

    # make it fly!
    m.run()
