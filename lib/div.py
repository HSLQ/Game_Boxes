# -*- coding: utf-8 -*
# Filename: div.py

__author__ = 'Piratf'

from background import Background
import pygame
from pygame.locals import *

class Div(object):
    """small panel in the frame"""
    def __init__(self, (width, height), (x, y)):
        # super(Div, self).__init__()
        self.width = width
        self.height = height
        self.x = x;
        self.y = y;
        self.rect = Rect((x, y), (width, height))
        self.initBackground()

    def initBackground(self):
        self.background = Background((self.width, self.height), (self.x, self.y))
        self.background.setColor((180, 180, 180))

    def draw(self, screen):
        self.background.draw(screen)
        
        # pygame.draw.rect(screen, (255, 255, 255), self.rect, 1)
