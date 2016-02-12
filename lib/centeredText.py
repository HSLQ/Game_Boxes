# -*- coding: utf-8 -*
# Filename: centeredText.py

__author__ = 'Piratf'

import pygame
from util import getFilePath
from text import Text

class CenteredText(Text):
    '''Centered Text Class'''
    # Constructror
    def __init__(self, font, text, (x, y), color = (255, 255, 255)):
        super(CenteredText, self).__init__(font, text, (x, y), color)
        # Start PyGame Font
        # font = pygame.font.SysFont("Yahei Consolas Hybrid", 20)
        self.size = self.font.size(text)
        self.drawX = self.x - (self.size[0] / 2.)
        self.drawY = self.y - (self.size[1] / 2.)

    # Draw Method
    def draw(self, screen):
        coords = (self.drawX, self.drawY)
        screen.blit(self.renderedText, coords)