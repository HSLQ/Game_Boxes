# -*- coding: utf-8 -*
# Filename: centeredText.py

__author__ = 'Piratf'

import pygame
from util import getFilePath
from text import Text

# 以传入位置为中心位置 进行显示 的图片对象
# 内部包裹的是 pygame.image 对象
class CenteredImage():
    '''Centered Image Class'''
    # Constructror
    def __init__(self, imagePath, (x, y), (width, height)):
        # super(CenteredImage, self).__init__()

        if isinstance(imagePath, str):
            self.loadResouce(imagePath)
        elif isinstance(imagePath, pygame.Surface):
            self.imageObj = imagePath
        else:
            raise TypeError
        self.imageObj = pygame.transform.scale(self.imageObj, (width, height))
        self.rect = self.imageObj.get_rect()
        self.drawX = x - (width / 2.)
        self.drawY = y - (height / 2.)
        self.rect.x += self.drawX
        self.rect.y += self.drawY


    def loadResouce(self, imagePath):
        self.imageObj = pygame.image.load(getFilePath(imagePath))

    # Draw Method
    def draw(self, screen):
        # pygame.draw.rect(screen, (255, 255, 255), self.rect, 1)
        screen.blit(self.imageObj, (self.drawX, self.drawY))