# -*- coding: utf-8 -*
# Filename: backGround.py

__author__ = 'Piratf'

import pygame

# def backGroundDeco(aClass):
#     class Background:
#         """draw background"""
#         def __init__(self, width, height):
#             # super(Background, self).__init__()
#             self.initAttr(width, height)
#             self.wrapped = aClass(width, height)

#         def initAttr(self, width, height):
#             self.width, self.height = width, height
#             self.panel = pygame.Surface((self.width, self.height), depth=32)

#         def draw(self, screen):
#             screen.blit(self.panel, (0, 0))
#             self.wrapped.draw(screen)

#     return Background

class Background:
    """draw background"""
    def __init__(self, width, height, *pos):
        # super(Background, self).__init__()
        if () == pos:
            pos = (0, 0)
        self.initAttr(width, height, pos)

    def initAttr(self, width, height, pos):
        self.width, self.height = width, height
        self.x, self.y = pos[0], pos[1]
        self.panel = pygame.Surface((self.width, self.height), depth=32)

    def setColor(self, color):
        if isinstance(color, pygame.Surface):
            self.panel = color
        else:
            self.panel.fill(color)


    def draw(self, screen):
        screen.blit(self.panel, (self.x, self.y))
