# -*- coding: utf-8 -*
# Filename: backGround.py

__author__ = 'Piratf'

import pygame

class Background(object):
    """draw background"""
    def __init__(self, (width, height), (x, y) = (0, 0)):
        # super(Background, self).__init__()
        self.initAttr((width, height), (x, y))

    def initAttr(self, (width, height), (x, y)):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.panel = pygame.Surface((self.width, self.height), depth=32)

    def setColor(self, color):
        if isinstance(color, pygame.Surface):
            self.panel = color
        else:
            self.panel.fill(color)


    def draw(self, screen):
        screen.blit(self.panel, (self.x, self.y))
