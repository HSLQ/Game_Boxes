# -*- coding: utf-8 -*
# Filename: hud.py

__author__ = 'Piratf'

from settings import HUD
from background import Background
import pygame

class Hud:
    """hud panel"""
    def __init__(self, width, offSetTop):
        # super(Hud, self).__init__()
        self.width = width
        self.height = HUD["HUD_HEIGHT"]
        backgroundImg = pygame.transform.scale(HUD["HUD_BACKGROUND_IMAGE"], (width, self.height))
        self.x, self.y = 0, offSetTop
        self.background = Background(self.width, self.height, self.x, self.y)
        self.background.setColor(backgroundImg)

    def draw(self, screen):
        screen.set_clip(self.x, self.y, self.width, self.height)
        self.background.draw(screen)

        