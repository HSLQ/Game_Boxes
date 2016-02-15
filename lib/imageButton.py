# -*- coding: utf-8 -*
# Filename: button.py

__author__ = 'Piratf'

from button import Button
from centeredImage import CenteredImage
from pygame.locals import *
import pygame

class ImageButton(Button, CenteredImage):
    """Button with text, drawing with centered coordinate"""
    def __init__(self, image, (width, height), (x, y)):
        CenteredImage.__init__(self, image, (width, height), (x, y))
        Button.__init__(self, self.rect)
        self.x = x
        self.y = y
        self.bgImage = CenteredImage(image, (width, height), (x, y))

    def setImage(self, image, (width, height)):
        self.bgImage = CenteredImage(image, (width, height), (self.x, self.y))

    def draw(self, screen):
        Button.draw(self, screen);
        self.bgImage.draw(screen)
        # 在按钮周围绘制边框
        # pygame.draw.rect(screen, (255, 255, 255), self.rect, 1)
