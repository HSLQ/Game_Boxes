# -*- coding: utf-8 -*
# Filename: finish.py

__author__ = 'Piratf'

from settings import FINISH, STATE
from background import Background
from textButton import TextButton
import pygame
from math import ceil

class Finish(object):
    """finish frame, win, lost or draw game"""
    def __init__(self, (width, height)):
        # super(Finish, self).__init__()
        self.width = width
        self.height = height
        self.loadResource()
        self.initElem()

    def initElem(self):
        self.background = Background((self.width, self.height))
        returnButtonCoord = (ceil(self.width / 2.), ceil(self.height / 2. + FINISH["RETURN_BUTTON_OFFSET_CENTER_HEIGHT"]))
        self.returnButton = TextButton(FINISH["RETURN_BUTTON_FONT"], FINISH["RETURN_BUTTON_CONTENT"], returnButtonCoord)

    def loadResource(self):
        self.winImg = pygame.transform.scale(FINISH["WIN_BACKGROUND_IMG"], (self.width, self.height))
        self.lostImg = pygame.transform.scale(FINISH["LOST_BACKGROUND_IMG"], (self.width, self.height))
        self.drawImg = pygame.transform.scale(FINISH["DRAW_BACKGROUND_IMG"], (self.width, self.height))

    def setWin(self, gameID):
        self.gameID = gameID
        self.background.setColor(self.winImg)

    def setLost(self, gameID):
        self.gameID = gameID
        self.background.setColor(self.lostImg)

    def setDraw(self, gameID):
        self.gameID = gameID
        self.background.setColor(self.drawImg)

    def leaveServer(self, *args):
        self.controller.leaveServer(self.gameID)

    def draw(self, screen):
        self.background.draw(screen)
        self.returnButton.draw(screen)

        var = self.returnButton.click(lambda *args : STATE.menu)
        if (var != None):
            return var
        return STATE.finish
