# -*- coding: utf-8 -*
# Filename: backGround.py

__author__ = 'Piratf'

import pygame

# def backGroundDeco(aClass):
#     class Background:
#         """draw background"""
#         def __init__(self, width, height):
#             # super(Background, self).__init__()
#             self.initAttr(width, height)
#             self.wrapped = aClass(width, height)

#         def initAttr(self, width, height):
#             self.width, self.height = width, height
#             self.panel = pygame.Surface((self.width, self.height), depth=32)

#         def draw(self, screen):
#             screen.blit(self.panel, (0, 0))
#             self.wrapped.draw(screen)

#     return Background

class Background:
    """draw background"""
    def __init__(self, width, height):
        # super(Background, self).__init__()
        self.initAttr(width, height)

    def initAttr(self, width, height):
        self.width, self.height = width, height
        # 纯色背景
        self.panel = pygame.Surface((self.width, self.height), depth=32)

    def draw(self, screen, (x, y) = (0, 0)):
        screen.blit(self.panel, (x, y))
