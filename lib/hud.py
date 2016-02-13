# -*- coding: utf-8 -*
# Filename: hud.py

__author__ = 'Piratf'

from settings import HUD
from background import Background
import pygame

class Hud:
    """hud panel"""
    def __init__(self, width):
        # super(Hud, self).__init__()
        self.width = width
        self.height = HUD["HUD_HEIGHT"]
        self.background = pygame.transform.scale(HUD["HUD_BACKGROUND_IMAGE"], (width, self.height))

    def draw(self, screen, offSetTop):
        screen.blit(self.background, (0, offSetTop))

        