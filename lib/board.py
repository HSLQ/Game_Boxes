# -*- coding: utf-8 -*
# Filename: board.py

__author__ = 'Piratf'

from settings import BOARD
from background import Background
import pygame

class Board:
    """board for playing"""
    def __init__(self, level):
        # super(Board, self).__init__()
        self.initAttr(level)

    def initAttr(self, level):
        self.level = level
        self.stickLength = BOARD["STICK_LENGTH"]
        self.separatorLength = BOARD["SEPARATOR_LENGTH"]
        self.separatorImage = BOARD["SEPARATOR_IMAGE"]
        self.normalLineImage = BOARD["STICK_NOR_IMAGE"]
        self.doneLineImage = BOARD["STICK_DONE_IMAGE"]
        self.squareSize = self.stickLength + self.separatorLength
        self.width = self.height = self.squareSize * self.level + self.separatorLength

        self.background = Background(self.width, self.height)

    def draw(screen):
        self.background.draw(screen)
