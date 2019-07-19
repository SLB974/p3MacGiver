import pygame
import pygame.locals as cpy
import constants as ct
import labyrinth

my_maze = labyrinth.Maze()
my_elements = labyrinth.Elements(my_maze.structure)

pygame.init()
surface = pygame.display.set_mode((ct.surface_width, ct.surface_height))
icon = pygame.image.load(ct.window_icon)
pygame.display.set_icon(icon)
pygame.display.set_caption(ct.window_title)
sound_got = pygame.mixer.Sound(ct.got_item_sound)
sound_won = pygame.mixer.Sound(ct.win_sound)
sound_lost = pygame.mixer.Sound(ct.lost_sound)
my_screen = labyrinth.Screen(surface, my_elements)
pygame.display.flip()


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
                my_screen.display_elements()
                pygame.display.flip()

            if result == ct.FOUND_ITEM:
                sound_got.play()

            if result == ct.MOVE_WIN:
                sound_won.play()
                my_screen.you_won()
                pygame.time.delay(15000)
                launched = False

            if result == ct.MOVE_LOOSE:
                sound_lost.play()
                my_screen.you_lost()
                pygame.time.delay(5000)
                launched = False
