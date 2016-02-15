# -*- coding: utf-8 -*
# Filename: setLevel.py

__author__ = 'Piratf'

from util import getFilePath
from settings import SETLEVEL, STATE
from background import Background
from textButton import TextButton
from centeredText import CenteredText
from centeredImage import CenteredImage
from imageButton import ImageButton
from game import Game
import pygame

class SetLevel(object):
    """set level frame"""
    def __init__(self, width, height):
        # super(SetLevel, self).__init__()
        self.initAttr(width, height)

    def initAttr(self, width, height):
        self.width, self.height = width, height
        self.justClicked = SETLEVEL["JUST_CLICKED"]
        # 默认 level
        self.loadResouce()
        self.setArrow()
        self.setLevel()

        self.background = Background((width, height))

        titleOffTop = 150

        self.titleText = CenteredText(SETLEVEL["TITLE_FONTS"], SETLEVEL["TITLE_CONTENT"], (self.width / 2, titleOffTop))

        offSet = 50
        self.beginButton = TextButton(SETLEVEL["BEGIN_FONTS"], SETLEVEL["BEGIN_CONTENT"], (self.width - offSet, self.height - offSet), (255, 255, 255))
        self.returnButton = TextButton(SETLEVEL["EXIT_FONTS"], SETLEVEL["EXIT_CONTENT"], (offSet, self.height - offSet), (255, 255, 255))

    def loadResouce(self):
        self.arrowImgRight = pygame.image.load(getFilePath("arrow.png"))

    def setArrow(self):
        arrowSize = SETLEVEL["ARROW_SIZE"]

        levelImageOffTop = 300
        coordX, coordY = self.width / 2, levelImageOffTop
        self.rArrow = ImageButton(self.arrowImgRight, (arrowSize, arrowSize), (coordX + 80, coordY - 10))
        self.lArrow = ImageButton(pygame.transform.flip(self.arrowImgRight, True, True), (arrowSize, arrowSize), (coordX - 80, coordY - 10))

    def setLevel(self, level = SETLEVEL["DEFAULT_LEVEL"]):
        if not isinstance(level, int):
            level = level[0]
        if (level > SETLEVEL["MAX_LEVEL"]):
            level = SETLEVEL["MAX_LEVEL"]
        if (level < SETLEVEL["MIN_LEVEL"]):
            level = SETLEVEL["MIN_LEVEL"]
        self.level = level
        levelTextOffTop = 300
        coordX, coordY = self.width / 2, levelTextOffTop
        self.levelText = CenteredText(SETLEVEL["LEVEL_FONTS"], str(self.level), (coordX, coordY))
        
    def drawLevelSet(self, screen):
        self.rArrow.draw(screen)
        self.levelText.draw(screen)
        self.lArrow.draw(screen)

    def draw(self, screen):
        self.background.draw(screen)
        self.titleText.draw(screen)
        self.drawLevelSet(screen)
        self.beginButton.draw(screen)
        self.returnButton.draw(screen)
        ret = self.beginButton.click(lambda *args : self.level)
        if ret != None:
            return ret
        ret = self.returnButton.click(lambda *args : STATE.menu)
        if ret != None:
            return ret
        self.rArrow.click(self.setLevel, self.level + 1)
        self.lArrow.click(self.setLevel, self.level - 1)
        return STATE.setLevel

        
        