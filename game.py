# coding:utf-8
import pygame
import pygame.locals as cpy
import constants as ct
import labyrinth

""" Main script for game -Help MacGyver to Escape- """

# Manage pygame surface initialization
my_maze = labyrinth.Maze()
my_elements = labyrinth.Elements(my_maze.structure)
pygame.init()
surface = pygame.display.set_mode((ct.surface_width, ct.surface_height))
my_screen = labyrinth.Screen(surface, my_elements)

# Manage loop and pygame events until you win or loose
launched = True

while launched:
    pygame.time.Clock().tick(30)

    for event in pygame.event.get():
        direction = ""
        if event.type == pygame.QUIT:
            launched = False
        elif event.type == cpy.KEYDOWN:
            if event.key == cpy.K_RIGHT:
                direction = "right"
            elif event.key == cpy.K_LEFT:
                direction = "left"
            elif event.key == cpy.K_UP:
                direction = "up"
            elif event.key == cpy.K_DOWN:
                direction = "down"

        if direction != "":
            result = my_elements.macgyver_move(direction)

            if result != ct.CANT_MOVE:
                my_screen.display_elements(result)

            if result == ct.MOVE_WIN:
                pygame.time.delay(10000)
                launched = False

            if result == ct.MOVE_LOOSE:
                pygame.time.delay(5000)
                launched = False
