# -*- coding: utf-8 -*
# Filename: button.py

__author__ = 'Piratf'

from util import getFilePath
from pygame.locals import *
import pygame

from centeredText import CenteredText

class TextButton(CenteredText):
    """Button with text, drawing with centered coordinate"""
    def __init__(self, font, text, (x, y), color = (255, 255, 255)):
        super(TextButton, self).__init__(font, text, (x, y), color)
        self.content = text
        padding = 5
        self.rect = Rect(self.drawX - padding, self.drawY - padding, self.size[0] + padding * 2, self.size[1] + padding * 2)

    def setHeadFlag(self, imagePath):
        self.headFlag = pygame.image.load(getFilePath("separators.png"))

    def setTextColor(self, color):
        if not color:
            return
        self.color = color
        self.renderedText = self.font.render(self.content, True, color)

    def click(self, foo):
        if pygame.mouse.get_pressed()[0]:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                return foo()

    def draw(self, screen):
        if (hasattr(self, "headFlag")):
            self.screen.blit(self.headFlag, [self.drawX - 10, self.drawY])

        super(TextButton, self).draw(screen)
        # 在按钮周围绘制边框
        # pygame.draw.rect(screen, (255, 255, 255), self.rect, 1)
