# -*- coding: utf-8 -*
# Filename: div.py

__author__ = 'Piratf'

from pygame.locals import *
import pygame

class Div(object):
    """small panel in the frame"""
    def __init__(self, (width, height), (x, y) = (0, 0)):
        # super(Div, self).__init__()
        self.width = width
        self.height = height
        self.x = x;
        self.y = y;
        self.rect = Rect((x, y), (width, height))