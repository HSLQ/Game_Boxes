# -*- coding: utf-8 -*
# Filename: button.py

__author__ = 'Piratf'

from settings import TEXTBUTTON
from util import getFilePath
from pygame.locals import *
import pygame

from centeredText import CenteredText

class TextButton(CenteredText):
    """Button with text, drawing with centered coordinate"""
    def __init__(self, font, content, (x, y), color = (255, 255, 255)):
        super(TextButton, self).__init__(font, content, (x, y), color)
        self.content = content
        self.initAttr()

    def initAttr(self):
        padding = TEXTBUTTON["BUTTON_TEXT_PADDING"]
        self.rect = Rect(self.drawX - padding, self.drawY - padding, self.size[0] + padding * 2, self.size[1] + padding * 2)
        self.justClickedOrigin = TEXTBUTTON["BUTTON_JUST_CLICKED"]
        self.justClicked = self.justClickedOrigin

    def setHeadFlag(self, imagePath):
        self.headFlag = pygame.image.load(getFilePath("separators.png"))

    def setTextColor(self, color):
        if not color:
            return
        self.color = color
        self.renderedText = self.font.render(self.content, True, color)

    def click(self, foo):
        if 0 == self.justClicked and pygame.mouse.get_pressed()[0]:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                self.justClicked = self.justClickedOrigin
                return foo()
        return None

    def draw(self, screen):
        if self.justClicked > 0 and not pygame.mouse.get_pressed()[0]:
            self.justClicked -= 1
        if (hasattr(self, "headFlag")):
            self.screen.blit(self.headFlag, [self.drawX - 10, self.drawY])

        super(TextButton, self).draw(screen)
        # 在按钮周围绘制边框
        # pygame.draw.rect(screen, (255, 255, 255), self.rect, 1)
