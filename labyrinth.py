import os
import pygame
from pygame.locals import *
from random import randint
from constants import *


class Maze:

    """
    Class to define labyrinth's struture
    """

    def __init__(self):

        directory = os.path.dirname(__file__)
        self.path_to_file = os.path.join(directory, structure_file)

        with open(self.path_to_file, "r") as f:

            structure = []

            for ligne in f:
                raw = []
                for column in ligne:
                    if column != "\n":
                        raw.append(column)
                structure.append(raw)
            self.structure = structure


class Elements:

    """
    Class to define Elements' position in the maze.
    MacGyver and Guardian's positions are written in structure
    Items' positions are randomly defined at start
    """

    def __init__(self, structure):

        self.structure = structure
        self.macGyver_YX = self.get_macgyver_position()
        self.guardian_YX = self.get_guardian_position()
        self.items = items_list
        self.counter = 0
        self.inventory = []
        self.define_items_position()

    def get_macgyver_position(self):

        for liste in self.structure:
            for column in liste:
                if column == "M":
                    y = self.structure.index(liste)
                    x = liste.index("M")
        return y, x

    def get_guardian_position(self):

        for liste in self.structure:
            for column in liste:
                if column == "G":
                    y = self.structure.index(liste)
                    x = liste.index("G")
        return y, x

    def define_items_position(self):

        """
        Define items' position randomly
        checking if position in structure is free
        """

        for item in self.items:

            y = randint(0, 14)
            free_position = False

            while not free_position:
                x = randint(0, 14)
                if self.structure[y][x] == "0":
                    if self.check_is_object_free(self.items.index(item), y, x):
                        self.items[self.items.index(item)][1] = y
                        self.items[self.items.index(item)][2] = x
                        free_position = True

    def check_is_object_free(self, index, y, x):

        """
        check if there is no other object at this position

        parameters :    index is item's index to check in items
                        y is item's y to check
                        x is item's x to check

        return :        True if position is free

        variables :      item_index is checked item's index
                        yy is checked item's y
                        xx is checked item's x
        """

        free_position = True

        for item in self.items:
            item_index = self.items.index(item)
            yy = self.items[item_index][1]
            xx = self.items[item_index][2]
            if not item_index == index:
                if y == yy and x == xx:
                    free_position = False
            return free_position

    def get_item(self, item_index):

        """
        Change item's coordinates to 0 when item is picked up by MacGyver
        """

        self.items[item_index][1] = 0
        self.items[item_index][2] = 0

    def is_free_to_go(self, y, x):

        """
        Check if there is no wall at the coordinates

        parameters : y and x
        return : True if position is free
        """
        if x < 0 or x > sprite_number - 1 or y < 0 or y > sprite_number - 1:
            return False
        elif self.structure[y][x] == "1":
            return False
        else:
            return True

    def macgyver_move(self, direction):

        y = self.macGyver_YX[0]
        x = self.macGyver_YX[1]

        reply = 0

        if direction == "right":
            yy = y
            xx = x + 1

        if direction == "left":
            yy = y
            xx = x - 1

        if direction == "up":
            yy = y - 1
            xx = x

        if direction == "down":
            yy = y + 1
            xx = x

        if self.is_free_to_go(yy, xx):
            reply = 1
            self.macGyver_YX = (yy, xx)
            if self.check_if_item(yy, xx):
                reply = 2
            if self.check_if_guardian(yy, xx) == 1:
                reply = 3
            elif self.check_if_guardian(yy, xx) == 2:
                reply = 4

        return reply

    def check_if_item(self, y, x):
        for item in self.items:
            item_index = self.items.index(item)
            if self.items[item_index][1] == y and self.items[item_index][2] == x:
                self.items[item_index][1] = 2
                self.items[item_index][2] = 16 + item_index
                self.counter += 1
                self.inventory.append(self.items[item_index][0])
                return True

    def check_if_guardian(self, y, x):
        if self.macGyver_YX == self.guardian_YX:
            if self.counter == len(self.items):
                return 1
            else:
                return 2
        else:
            return 0


class Screen:

    """
    Class to manage pygame's surface
    """

    def __init__(self, surface, my_elements):

        self.surface = surface
        self.my_elements = my_elements
        self.floor = pygame.image.load(floor_pic).convert()
        self.macgyver = pygame.image.load(macgyver_pic).convert_alpha(self.surface)
        self.guardian = pygame.image.load(guardian_pic).convert_alpha(self.surface)
        self.wall = pygame.image.load(wall_pic).convert_alpha(self.surface)
        self.panel = pygame.image.load(right_panel).convert()
        self.my_font = pygame.font.SysFont("tahoma", 20)
        self.my_font2 = pygame.font.SysFont("arial", 80)
        self.display_elements()

    def display_elements(self):

        self.counter = self.my_elements.counter
        self.label1 = "You got no item !"
        if self.counter != 0:
            self.label1 = "You got " + str(self.counter) + " item(s) !"
        self.label = self.my_font.render(self.label1, 1, (0, 0, 0))
        self.surface.blit(self.floor, (0, 0))
        self.surface.blit(self.panel, (surface_width - board_width, 0))

        raw_n = 0
        for raw in self.my_elements.structure:
            column_n = 0

            for column in raw:
                if column == "1":
                    self.surface.blit(
                        self.wall, (self.screen_pos(column_n), self.screen_pos(raw_n))
                    )
                column_n += 1
            raw_n += 1

        for item in self.my_elements.items:
            item_pic = item[3]
            item_pic = pygame.image.load(item_pic).convert_alpha(self.surface)
            self.surface.blit(
                item_pic, (self.screen_pos(item[2]), self.screen_pos(item[1]))
            )

        self.surface.blit(
            self.macgyver,
            (
                self.screen_pos(self.my_elements.macGyver_YX[1]),
                self.screen_pos(self.my_elements.macGyver_YX[0]),
            ),
        )

        self.surface.blit(
            self.guardian,
            (
                self.screen_pos(self.my_elements.guardian_YX[1]),
                self.screen_pos(self.my_elements.guardian_YX[0]),
            ),
        )

        self.surface.blit(self.label, (620, 20))

    def you_won(self):
        self.label2 = self.my_font2.render(text1, 1, (255, 0, 0))
        self.label3 = self.my_font2.render(text2, 1, (255, 0, 0))
        self.surface.blit(self.label2, (620, 350))
        self.surface.blit(self.label3, (620, 450))
        pygame.display.flip()

    def you_lost(self):
        self.label2 = self.my_font2.render(text1, 1, (255, 0, 0))
        self.label3 = self.my_font2.render(text3, 1, (255, 0, 0))
        self.surface.blit(self.label2, (620, 350))
        self.surface.blit(self.label3, (620, 450))
        pygame.display.flip()

    @staticmethod
    def screen_pos(coordinate):

        """
        Calculate position on pygame's surface
        """

        return coordinate * sprite_size
