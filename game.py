import pygame
from pygame.locals import *
from constants import *
import labyrinth

my_maze = labyrinth.Maze()
my_elements = labyrinth.Elements(my_maze.structure)

pygame.init()
surface = pygame.display.set_mode((surface_width, surface_height))
icon = pygame.image.load(window_icon)
pygame.display.set_icon(icon)
pygame.display.set_caption(window_title)
sound_got = pygame.mixer.Sound(got_item_sound)
sound_won = pygame.mixer.Sound(win_sound)
sound_lost = pygame.mixer.Sound(lost_sound)
my_screen = labyrinth.Screen(surface, my_elements)
pygame.display.flip()


launched = True

while launched:
    pygame.time.Clock().tick(30)

    for event in pygame.event.get():
        direction = ""
        if event.type == pygame.QUIT:
            launched = False
        elif event.type == KEYDOWN:
            if event.key == K_RIGHT:
                direction = "right"
            elif event.key == K_LEFT:
                direction = "left"
            elif event.key == K_UP:
                direction = "up"
            elif event.key == K_DOWN:
                direction = "down"

        if direction != "":
            result = my_elements.macgyver_move(direction)

            if result != 0:
                my_screen.display_elements()
                pygame.display.flip()

            if result == 2:
                sound_got.play()

            if result == 3:
                sound_won.play()
                my_screen.you_won()
                pygame.time.delay(15000)
                pygame.quit()

            if result == 4:
                sound_lost.play()
                my_screen.you_lost()
                pygame.time.delay(5000)
                pygame.quit()
