# -*- coding: utf-8 -*
# Filename: menu.py

__author__ = 'Piratf'

from textButton import TextButton
from util import getFilePath 
from settings import MENU_TEXTS, MENU_FONTS, STATE
import pygame
from pygame.locals import *

class Menu(object):
    """menu of the game"""
    def __init__(self, width, height):
        self.initAttr(width, height);
        self.loadResource()

    def initAttr(self, width, height):
        self.width, self.height = width, height
        self.firstLinePos = 150
        self.buttons = []
        gap = 80
        for text in MENU_TEXTS:
            self.buttons.append(TextButton(MENU_FONTS, text, (self.width / 2, self.firstLinePos + gap), (255, 255, 255)))
            gap += 80

    def loadResource(self):
        # 纯色背景
        self.panel = pygame.Surface((self.width, self.height), depth=32)

    def draw(self, screen):
        # 背景图片
        screen.blit(self.panel, (0, 0))
        [button.draw(screen) for button in self.buttons]
        pygame.display.flip()

    def clickListener(self):
        if (pygame.mouse.get_pressed()[0]):
            mousePos = pygame.mouse.get_pos()
            for button in self.buttons:
                if button.rect.collidepoint(mousePos):
                    if MENU_TEXTS[0] == button.content:
                        print "start new game"
                        return STATE.setLevel
                    elif MENU_TEXTS[1] == button.content:
                        print "matching"
                        return STATE.matching
                    elif MENU_TEXTS[2] == button.content:
                        print "rules"
                        return STATE.rules
                    elif MENU_TEXTS[3] == button.content:
                        print "exit"
                        return STATE.exit
        return STATE.menu
