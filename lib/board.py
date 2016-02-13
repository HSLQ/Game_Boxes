# -*- coding: utf-8 -*
# Filename: board.py

__author__ = 'Piratf'

from settings import BOARD
from background import Background
import pygame
import math

class Board:
    """board for playing"""
    def __init__(self, level, (posX, posY)):
        # super(Board, self).__init__()
        self.initAttr(level, (posX, posY))
        self.initBoardArray()

    def initAttr(self, level, (posX, posY)):
        self.width, self.height = BOARD["BOARD_WIDTH"], BOARD["BOARD_HEIGHT"]
        self.levelH = level
        self.levelV = level
        self.stickLength = BOARD["STICK_LENGTH"]
        self.separatorLength = BOARD["SEPARATOR_LENGTH"]
        self.separatorImage = BOARD["SEPARATOR_IMAGE"]
        self.normalLineImageV = BOARD["STICK_NOR_IMAGE"]
        self.normalLineImageH = pygame.transform.rotate(self.normalLineImageV, -90)
        self.doneLineImageV = BOARD["STICK_DONE_IMAGE"]
        self.doneLineImageH = pygame.transform.rotate(self.doneLineImageV, -90)
        self.getRealSize(level)
        self.x, self.y = posX, posY

        self.background = Background(self.width, self.height, *(posX, posY))
        self.squareSideLength = self.stickLength + self.separatorLength

    def initBoardArray(self):
        self.boardH = [[False for x in range(self.levelH)] for y in range(self.levelV + 1)]
        self.boardV = [[False for x in range(self.levelH + 1)] for y in range(self.levelV)]

    def getRealSize(self, level):
        self.stickLength = (int(math.ceil(((self.width - self.separatorLength) / level))) - self.separatorLength)
        self.normalLineImageH = pygame.transform.scale(self.normalLineImageH, (self.stickLength, self.separatorLength))
        self.normalLineImageV = pygame.transform.scale(self.normalLineImageV, ( self.separatorLength, self.stickLength))
        self.doneLineImageH = pygame.transform.scale(self.doneLineImageH, (self.stickLength, self.separatorLength))
        self.doneLineImageV = pygame.transform.scale(self.doneLineImageV, ( self.separatorLength, self.stickLength))
        self.width = (self.stickLength + self.separatorLength) * self.levelH + self.separatorLength
        self.height = (self.stickLength + self.separatorLength) * self.levelV + self.separatorLength

    def getSquarePosH(self, h, v):
        return [self.x + h * self.squareSideLength + self.separatorLength, self.y + v * self.squareSideLength]

    def getSquarePosV(self, h, v):
        return [self.x +  h * self.squareSideLength, self.y + v * self.squareSideLength + self.separatorLength]

    def getSepPos(self, h, v):
        return [self.x + h * self.squareSideLength, self.y + v * self.squareSideLength]

    def drawBoard(self, screen):
        for v in range(self.levelV + 1):
            for h in range(self.levelH):
                if not self.boardH[v][h]:
                    screen.blit(self.normalLineImageH, self.getSquarePosH(h, v))
                else:
                    screen.blit(self.doneLineImageH, self.getSquarePosH(h, v))
        for v in range(self.levelV):
            for h in range(self.levelH + 1):
                if not self.boardV[v][h]:
                    screen.blit(self.normalLineImageV, self.getSquarePosV(h, v))
                else:
                    screen.blit(self.doneLineImageV, self.getSquarePosV(h, v))
        #draw separators
        for v in range(self.levelV + 1):
            for h in range(self.levelH + 1):
                screen.blit(self.separatorImage, self.getSepPos(h, v))

    def light(self, screen):
        pass

    def hover(self, screen):
        mousePos = list(pygame.mouse.get_pos())
        mousePos[0] -= self.x
        mousePos[1] -= self.y
        widthPos = int(math.ceil( (mousePos[0] - (self.squareSideLength / 2.)) / float(self.squareSideLength)) )
        heightPos = int(math.ceil( (mousePos[1] - (self.squareSideLength / 2.)) / float(self.squareSideLength)) )

        is_horizontal = abs(mousePos[1] - heightPos * self.squareSideLength) < abs(mousePos[0] - widthPos * self.squareSideLength)

        heightPos = heightPos - 1 if mousePos[1] - heightPos * self.squareSideLength < 0 and not is_horizontal else heightPos
        widthPos = widthPos - 1 if mousePos[0] - widthPos * self.squareSideLength < 0 and is_horizontal else widthPos


        board = self.boardH if is_horizontal else self.boardV
        isOutOfBounds = False
        try:
            if not board[heightPos][widthPos]: 
                screen.blit(self.doneLineImageH if is_horizontal else self.doneLineImageV, [self.x + (widthPos * self.squareSideLength + self.separatorLength if is_horizontal else widthPos * self.squareSideLength), self.y + (heightPos * self.squareSideLength if is_horizontal else heightPos * self.squareSideLength + self.separatorLength)])
        except:
            isOutOfBounds = True
            pass
        if not isOutOfBounds:
            alreadyPlaced = board[heightPos][widthPos]
        else:
            alreadyPlaced = False



    def draw(self, screen):
        # screen.set_clip(self.x, self.y, self.width, self.height)
        self.background.draw(screen)
        self.drawBoard(screen)
        self.hover(screen)


