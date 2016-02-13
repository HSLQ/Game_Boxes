# -*- coding: utf-8 -*
# Filename: setLevel.py

__author__ = 'Piratf'

from util import getFilePath
from settings import SETLEVEL, STATE
from background import Background
from textButton import TextButton
from centeredText import CenteredText
from centeredImage import CenteredImage
import pygame

class SetLevel:
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

        self.background = Background(width, height)

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
        self.rArrow = CenteredImage(self.arrowImgRight, (coordX + 80, coordY - 10), (arrowSize, arrowSize))
        self.lArrow = CenteredImage(pygame.transform.flip(self.arrowImgRight, True, True), (coordX - 80, coordY - 10), (arrowSize, arrowSize))

    def setLevel(self, level = SETLEVEL["DEFAULT_LEVEL"]):
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
        if (self.justClicked > 0):
            self.justClicked -= 1
        self.background.draw(screen)
        self.titleText.draw(screen)

        self.drawLevelSet(screen)

        self.beginButton.draw(screen)
        self.returnButton.draw(screen)
        pygame.display.flip()

    def clickListener(self):
        if (pygame.mouse.get_pressed()[0]):
            mousePos = pygame.mouse.get_pos()
            if self.beginButton.rect.collidepoint(mousePos):
                return STATE.game
            elif self.returnButton.rect.collidepoint(mousePos):
                return STATE.menu
            else:
                if self.rArrow.rect.collidepoint(mousePos) and 0 == self.justClicked:
                    self.setLevel(self.level + 1)
                elif self.lArrow.rect.collidepoint(mousePos) and 0 == self.justClicked:
                    self.setLevel(self.level - 1)
                self.justClicked = SETLEVEL["JUST_CLICKED"]
                return self.level
            self.justClicked = SETLEVEL["JUST_CLICKED"]
        return STATE.setLevel

        
        