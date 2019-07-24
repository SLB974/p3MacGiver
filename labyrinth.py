# coding:utf-8
import os
import pygame
from random import randint
import constants as ct


class Maze:

    """ Class to define labyrinth's struture """

    def __init__(self):

        """ At init, get the maze's structure in structure file """

        directory = os.path.dirname(__file__)
        self.path_to_file = os.path.join(directory, ct.structure_file)

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
    Class for managing elements in the maze : coordinates and MacGyver's moves
    """

    def __init__(self, structure):

        self.structure = structure
        self.macGyver_YX = self.get_macgyver_position()
        self.guardian_YX = self.get_guardian_position()
        self.items = ct.items_list
        self.counter = 0
        self.define_items_position()

    def get_macgyver_position(self):

        """ Get MacGyver position written in structure """

        for liste in self.structure:
            for column in liste:
                if column == "M":
                    y = self.structure.index(liste)
                    x = liste.index("M")
        return y, x

    def get_guardian_position(self):

        """ Get guardian position written in structure"""

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

            item_index = self.items.index(item)
            free_position = False

            while not free_position:
                y = randint(0, 14)
                x = randint(0, 14)
                if self.structure[y][x] == "0":
                    if self.check_is_object_free(item_index, y, x):
                        self.items[item_index][1] = y
                        self.items[item_index][2] = x
                        free_position = True

    def check_is_object_free(self, index, y, x):

        """
        check if there is no other object at this position

        parameters :    index is item's index to check in items
                        y is item's y to check
                        x is item's x to check

        return :        True if position is free

        variables :     item_index is checked item's index
                        yy is checked item's y
                        xx is checked item's x
        """

        for item in self.items:

            item_index = self.items.index(item)
            yy = self.items[item_index][1]
            xx = self.items[item_index][2]
            if not item_index == index:
                if y == yy and x == xx:
                    return False
        return True

    def is_free_to_go(self, y, x):

        """
        Check if there is no wall at the coordinates

        parameters : y and x
        return : True if position is free
        """

        if (
            x < 0
            or x > ct.sprite_number - 1
            or y < 0
            or y > ct.sprite_number - 1
        ):
            return False

        if self.structure[y][x] == "1":
            return False
        else:
            return True

    def macgyver_move(self, direction):

        """
        Manage MacGyver's moves :

        1/ define movement after parameter direction
        2/ check if new position is free with self.is_free_to_go()
        3/ check if item at new position with self.check_if_item()
        4/ check if guardian at new position with self.check_if_guardian()

        Parameter : direction

        Return : eiter CANT_MOVE, or self.check_if_guardian() constant
        """

        y = self.macGyver_YX[0]
        x = self.macGyver_YX[1]

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

            self.macGyver_YX = (yy, xx)
            if self.check_if_item(yy, xx):
                return ct.CAN_MOVE
            else:
                return self.check_if_guardian(yy, xx)

        return ct.CANT_MOVE

    def check_if_item(self, y, x):

        """
        check if MacGyver found item

        if so : increment self.counter
                define new position of item in right panel for inventory
                return true
        """

        sound_got = pygame.mixer.Sound(ct.got_item_sound)

        for item in self.items:
            item_index = self.items.index(item)
            if (
                self.items[item_index][1] == y
                and self.items[item_index][2] == x
            ):
                self.items[item_index][1] = 2
                self.items[item_index][2] = 16 + item_index
                self.counter += 1
                sound_got.play()
                return True

    def check_if_guardian(self, y, x):

        """
        Check if MacGyver found guardian
        returns move constants from ct (constants)
        """

        sound_won = pygame.mixer.Sound(ct.win_sound)
        sound_lost = pygame.mixer.Sound(ct.lost_sound)

        if self.macGyver_YX == self.guardian_YX:
            if self.counter == len(self.items):
                sound_won.play()
                return ct.MOVE_WIN
            else:
                sound_lost.play()
                return ct.MOVE_LOOSE
        else:
            return ct.CAN_MOVE


class Screen:

    """ Class to manage pygame's surface """

    def __init__(self, surface, my_elements):

        self.surface = surface
        icon = pygame.image.load(ct.window_icon)
        pygame.display.set_icon(icon)
        pygame.display.set_caption(ct.window_title)

        self.my_elements = my_elements
        self.floor = pygame.image.load(ct.floor_pic).convert()
        self.macgyver = pygame.image.load(ct.macgyver_pic).convert_alpha(
            self.surface
        )
        self.guardian = pygame.image.load(ct.guardian_pic).convert_alpha(
            self.surface
        )
        self.wall = pygame.image.load(ct.wall_pic).convert_alpha(self.surface)
        self.panel = pygame.image.load(ct.right_panel).convert()
        self.my_font = pygame.font.SysFont("tahoma", 20)
        self.my_font2 = pygame.font.SysFont("arial", 60)
        self.display_elements(ct.CAN_MOVE)

    def display_elements(self, situation):

        """
        Preparing elements' display and update screen

        parameter : situation after ct (constants)
        """

        # Message for picked up items
        self.counter = self.my_elements.counter
        self.label1 = "You got no item !"
        if self.counter == 1:
            self.label1 = "You got 1 item !"
        if self.counter > 1:
            self.label1 = "You got " + str(self.counter) + " items !"
        self.label = self.my_font.render(self.label1, 1, (0, 0, 0))

        # floor and panel location
        self.surface.blit(self.floor, (0, 0))
        self.surface.blit(self.panel, (ct.surface_width - ct.board_width, 0))

        # walls' location
        raw_n = 0
        for raw in self.my_elements.structure:
            column_n = 0

            for column in raw:
                if column == "1":
                    self.surface.blit(
                        self.wall,
                        (self.screen_pos(column_n), self.screen_pos(raw_n)),
                    )
                column_n += 1
            raw_n += 1

        # items' location
        for item in self.my_elements.items:
            item_pic = item[3]
            item_pic = pygame.image.load(item_pic).convert_alpha(self.surface)
            self.surface.blit(
                item_pic, (self.screen_pos(item[2]), self.screen_pos(item[1]))
            )

        # guardian's location
        self.surface.blit(
            self.guardian,
            (
                self.screen_pos(self.my_elements.guardian_YX[1]),
                self.screen_pos(self.my_elements.guardian_YX[0]),
            ),
        )

        # MacGyver's location
        self.surface.blit(
            self.macgyver,
            (
                self.screen_pos(self.my_elements.macGyver_YX[1]),
                self.screen_pos(self.my_elements.macGyver_YX[0]),
            ),
        )

        # informations' counter's label location
        self.surface.blit(self.label, (620, 20))

        # Informations' bottom panel's label

        if situation == ct.CAN_MOVE:
            self.you_play()

        if situation == ct.MOVE_WIN:
            self.you_won()

        if situation == ct.MOVE_LOOSE:
            self.you_lost()

        rect = pygame.Rect(600, 500, 200, 300)
        pygame.display.update(rect)
        pygame.display.flip()

    def you_play(self):

        """ informations' display if you're playing """

        self.my_font2 = pygame.font.SysFont("arial", 60)
        self.label2 = self.my_font2.render(ct.text0, 1, (0, 0, 0))
        self.surface.blit(self.label2, (620, 500))

    def you_won(self):

        """ informations' display if you won """

        self.my_font2 = pygame.font.SysFont("arial", 40)
        self.label2 = self.my_font2.render(ct.text1, 1, (255, 0, 0))
        self.surface.blit(self.label2, (620, 520))

    def you_lost(self):

        """ informations' display if you lost """

        self.my_font2 = pygame.font.SysFont("arial", 40)
        self.label2 = self.my_font2.render(ct.text2, 1, (255, 0, 0))
        self.surface.blit(self.label2, (620, 520))

    @staticmethod
    def screen_pos(coordinate):

        """ Calculate position on pygame's surface """

        return coordinate * ct.sprite_size
