# Making a game with the SDL2 and PySDL2

## SUMMARY
The idea of this project was to create 2.5d game(a 2d game with the illusion of 3d using perspective) using SDL2.  I decided to make it in python so I ended up using a python wrapper called PySDL2 and c-type wrappers anywhere PySDL2 fell short.

## STACK
The tech I used for this project<br/>
python3<br/>
sdl2<br/>
sdl2-gfx<br/>
sdl2-ttf<br/>
pysdl2

---
Files | Description
---|---
constants.py | Settings file for the game that holds constants
manager.py | Contains all the code for the graphics display engine
maze.py | File to run to start the game
map_maker.py | Jsononify a matrix to be read by the game as the map
map files | Maps to be read by the map
raycast.py | Contains all the code for the raycasting engine
game_objects.py | Defines classes for different objects in the game
colors.py | Definitions for different colors
test.py | Test program to find bugs in my raycasting (minimap)
---

## INSTRUCTIONS
Assuming an environment with Python3 installed<br/>
Gitclone repository<br/>
Install PySDL2<br/>
Download SDL2 library<br/>
Run the program by typing "python3 maze.py"

## TO DO
Need to find a way to smooth the edge lines of the walls.  I used an old guide for something that wanted a 300x280 pixel screen so just need to think about it.<br/>
Make an all in one package so don't have to install SDL2 and PySDL2.<br/>
Add actual game elements such as player sprites.<br/>
Add textures to walls, ceiling and floor.

## RESOURCES USED
[Roguelike tutorial using PySDL2](http://www.roguebasin.com/index.php?title=Complete_Roguelike_Tutorial,_using_python3%2Bpysdl2,_part_1)<br/>
[PySDL2 tutorial](http://pysdl2.readthedocs.io/en/latest/tutorial/helloworld.html)<br/>
[Raycasting 1](https://permadi.com/1996/05/ray-casting-tutorial-1/)<br/>
[Raycasting 2](http://lodev.org/cgtutor/raycasting.html)<br/>
SDL2 github<br/>
SDL2gfx documentation<br/>
Stackoverflow<br/>
Google
