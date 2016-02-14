# -*- coding: utf-8 -*
# Filename: menu.py

__author__ = 'Piratf'

from label import Label
from textButton import TextButton
from text import Text
from util import getFilePath 
from settings import STATE
from settings import RULES_CONTENT, RULES_CONTENT_FONTS, RULES_EXIT_FONTS
from background import Background
import pygame
from pygame.locals import *

class Rules(object):
    """menu of the game"""
    def __init__(self, width, height):
        self.initAttr(width, height);

    def loadResource(self):
        self.headMark = pygame.image.load(getFilePath("separators.png"))

    def initAttr(self, width, height):
        self.width, self.height = width, height
        self.loadResource()
        self.background = Background((width, height))
        # 规则文字开始的位置
        offLine = 100
        offSet = 50
        self.content = []
        for content in RULES_CONTENT[0 : -1]:
            offLine += offSet
            self.content.append(Label(RULES_CONTENT_FONTS, content, (50, offLine), headMark = self.headMark))
        self.returnButton = TextButton(RULES_EXIT_FONTS, RULES_CONTENT[-1], (offSet, self.height - offSet), (255, 255, 255))

    def draw(self, screen):
        self.background.draw(screen)
        [content.draw(screen) for content in self.content]
        self.returnButton.draw(screen)
        pygame.display.flip()

    def clickListener(self):
        if (pygame.mouse.get_pressed()[0]):
            mousePos = pygame.mouse.get_pos()
            if self.returnButton.rect.collidepoint(mousePos):
                return STATE.menu
        return STATE.rules
