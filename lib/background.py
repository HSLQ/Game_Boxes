# -*- coding: utf-8 -*
# Filename: backGround.py

__author__ = 'Piratf'

from div import Div
import pygame

class Background(Div, object):
    """draw background"""
    def __init__(self, (width, height), (x, y) = (0, 0)):
        # super(Background, self).__init__()
        Div.__init__(self, (width, height), (x, y))
        self.panel = pygame.Surface((self.width, self.height), depth=32)

    def setColor(self, color):
        if isinstance(color, pygame.Surface):
            self.panel = color
        else:
            self.panel.fill(color)

    def draw(self, screen):
        screen.blit(self.panel, (self.x, self.y))
