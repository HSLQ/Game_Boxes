# -*- coding: utf-8 -*
# Filename: button.py

__author__ = 'Piratf'

from settings import BUTTON
import pygame

class Button(object):
    """button class for click"""
    def __init__(self, rect):
        self.justClickedOrigin = BUTTON["BUTTON_JUST_CLICKED"]
        self.justClicked = self.justClickedOrigin
        self.rect = rect
        # super(Button, self).__init__()
    
    def click(self, foo, *args):
        if 0 == self.justClicked and pygame.mouse.get_pressed()[0]:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                print 111
                self.justClicked = self.justClickedOrigin
                ret = foo(*args)
                return ret
        return None

    def draw(self, screen):
        if 0 < self.justClicked and not pygame.mouse.get_pressed()[0]:
            self.justClicked -= 1
