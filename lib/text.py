# -*- coding: utf-8 -*
# Filename: text.py

__author__ = 'Piratf'

from util import getFilePath
import pygame

# 每次新建都加载 字体文件，计算等，减少 draw 消耗
class Text(object):
    """Text class for easy to drawing"""
    def __init__(self, font, text, (x, y), color = (255, 255, 255)):
        # super(Text, self).__init__()
        self.color = color

        pygame.font.init()
        self.font = font
        self.renderedText = self.font.render(text, True, color)
        self.x, self.y = x, y

    def draw(self, screen):
        screen.blit(self.renderedText, (self.x, self.y))