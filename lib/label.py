# -*- coding: utf-8 -*
# Filename: button.py

__author__ = 'Piratf'

from util import getFilePath
from pygame.locals import *
import pygame

from text import Text

class Label(Text):
    """Button with text, drawing with centered coordinate"""
    def __init__(self, font, text, (x, y), color = (255, 255, 255), headMark = None):
        self.setHeadFlag(headMark)
        super(Label, self).__init__(font, text, (x, y), color)
        self.content = text

    def setHeadFlag(self, headMark):
        self.headMark = headMark

    def draw(self, screen):
        if self.headMark:
            rect = self.renderedText.get_rect()
            screen.blit(self.headMark, [self.x - rect.height / 2, self.y + rect.height / 2])

        super(Label, self).draw(screen)
        # pygame.draw.rect(screen, (255, 255, 255), self.rect, 1)

    def setTextColor(self, color):
        if not color:
            return
        self.color = color
        self.renderedText = self.font.render(self.content, True, color)
