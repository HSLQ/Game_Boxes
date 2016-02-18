# -*- coding: utf-8 -*
# Filename: board.py

__author__ = 'Piratf'

from settings import BOARD
from div import Div
from background import Background
import pygame
import math
import inspect

class Board(Div, object):
    """board for playing"""
    def __init__(self, (posX, posY)):
        # super(Board, self).__init__()
        Div.__init__(self, (BOARD["BOARD_WIDTH"], BOARD["BOARD_HEIGHT"]), (posX, posY))
        self.initAttr()
        self.initBoardArray()

    def initAttr(self):
        self.stickLength = int(BOARD["STICK_LENGTH"])
        self.separatorLength = int(BOARD["SEPARATOR_LENGTH"])
        self.separatorImage = BOARD["SEPARATOR_IMAGE"]
        self.normalLineImageV = BOARD["STICK_NOR_IMAGE"]
        self.normalLineImageH = pygame.transform.rotate(self.normalLineImageV, -90)
        self.doneLineImageV = BOARD["STICK_DONE_IMAGE"]
        self.doneLineImageH = pygame.transform.rotate(self.doneLineImageV, -90)

        self.greenplayerBase = BOARD["GREEN_SQUARE"]
        self.yellowplayerBase = BOARD["YELLOW_SQUARE"]
        self.marker = self.greenplayerBase
        self.othermarker = self.yellowplayerBase

        self.background = Background((self.width, self.height), (self.x, self.y))
        self.justPlaced = BOARD["JUST_PLACED"]
        self.setTurn(True)
        self.setLevel()

    def setLevel(self, level = 6):
        print "set level", level
        self.levelH = level
        self.levelV = level
        self.setTurn(True)
        self.getRealSize(level)
        self.width = self.levelH * self.squareSideLength + self.separatorLength
        self.height = self.levelV * self.squareSideLength + self.separatorLength
        return self.getRealSize(level)

    def setTurn(self, turn):
        self.turn = turn

    def initBoardArray(self):
        print "init board array"
        self.boardH = [[False for x in range(self.levelH)] for y in range(self.levelV + 1)]
        self.boardV = [[False for x in range(self.levelH + 1)] for y in range(self.levelV)]
        self.ownerBoard = [[0 for x in range(self.levelH)] for y in range(self.levelV)]

    def getRealSize(self, level):
        print "get real size"
        self.initBoardArray()
        self.stickLength = (int(math.ceil(((self.width - self.separatorLength) / level))) - self.separatorLength)
        self.normalLineImageH = pygame.transform.scale(self.normalLineImageH, (self.stickLength, self.separatorLength))
        self.normalLineImageV = pygame.transform.scale(self.normalLineImageV, ( self.separatorLength, self.stickLength))
        self.doneLineImageH = pygame.transform.scale(self.doneLineImageH, (self.stickLength, self.separatorLength))
        self.doneLineImageV = pygame.transform.scale(self.doneLineImageV, ( self.separatorLength, self.stickLength))

        self.greenplayer = pygame.transform.scale(self.greenplayerBase, (self.stickLength, self.stickLength))
        self.yellowplayer = pygame.transform.scale(self.yellowplayerBase, (self.stickLength, self.stickLength))

        self.marker = self.greenplayer
        self.othermarker = self.yellowplayer

        self.width = (self.stickLength + self.separatorLength) * self.levelH + self.separatorLength
        self.height = (self.stickLength + self.separatorLength) * self.levelV + self.separatorLength
        self.squareSideLength = self.stickLength + self.separatorLength
        self.background = Background((self.width, self.height), (self.x, self.y))
        return self.width, self.height

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

        self.drawOwnerMap(screen)

    def getOwnerPostion(self, h, v):
        return (self.x + h * self.squareSideLength + self.separatorLength, self.y + v * self.squareSideLength + self.separatorLength)

    # 绘制得分方块
    def drawOwnerMap(self, screen):
        for v in range(self.levelV):
            for h in range(self.levelH):
                if self.ownerBoard[v][h] != 0:
                    if self.ownerBoard[v][h] == "win":
                        screen.blit(self.marker, self.getOwnerPostion(h, v))
                    if self.ownerBoard[v][h] == "lose": 
                        screen.blit(self.othermarker, self.getOwnerPostion(h, v))

    # 返回得分座标 或 None
    def isGetPoint(self, hPos, vPos, is_horizontal):
        board = self.boardH if is_horizontal else self.boardV
        if (is_horizontal):
            if (vPos < self.levelV and self.boardH[vPos + 1][hPos] and self.boardV[vPos][hPos] and self.boardV[vPos][hPos + 1]):
                self.ownerBoard[vPos][hPos] = "win"
                return {"x":hPos, "y":vPos}
            if (vPos > 0 and self.boardH[vPos - 1][hPos] and self.boardV[vPos - 1][hPos] and  self.boardV[vPos - 1][hPos + 1]):
                self.ownerBoard[vPos - 1][hPos] = "win"
                return {"x":hPos, "y":vPos - 1}
        else:
            if (hPos > 0 and self.boardV[vPos][hPos - 1] and self.boardH[vPos][hPos - 1] and self.boardH[vPos + 1][hPos - 1]):
                self.ownerBoard[vPos][hPos - 1] = "win"
                return {"x":hPos - 1, "y":vPos}
            if (hPos < self.levelH and self.boardV[vPos][hPos + 1] and self.boardH[vPos][hPos] and self.boardH[vPos + 1][hPos]):
                self.ownerBoard[vPos][hPos] = "win"
                return {"x":hPos, "y":vPos}
        return None

    # 重新初始化棋盘，重新开始游戏
    def restart(self):
        self.initBoardArray()

    def mouseEvent(self, screen):
        # hover
        mousePos = list(pygame.mouse.get_pos())
        mousePos[0] -= self.x
        mousePos[1] -= self.y
        hPos = int(math.ceil( (mousePos[0] - (self.squareSideLength / 2.)) / float(self.squareSideLength)) )
        vPos = int(math.ceil( (mousePos[1] - (self.squareSideLength / 2.)) / float(self.squareSideLength)) )

        is_horizontal = abs(mousePos[1] - vPos * self.squareSideLength) < abs(mousePos[0] - hPos * self.squareSideLength)

        vPos = vPos - 1 if vPos > 0 and mousePos[1] - vPos * self.squareSideLength < 0 and not is_horizontal else vPos
        hPos = hPos - 1 if vPos > 0 and mousePos[0] - hPos * self.squareSideLength < 0 and is_horizontal else hPos

        if vPos < 0 or hPos < 0 or vPos > self.levelV or hPos > self.levelH:
            return

        board = self.boardH if is_horizontal else self.boardV
        isOutOfBounds = False
        try:
            if not board[vPos][hPos]: 
                screen.blit(self.doneLineImageH 
                    if is_horizontal 
                    else self.doneLineImageV, 
                    (self.x + 
                    (hPos * self.squareSideLength + self.separatorLength 
                        if is_horizontal 
                        else hPos * self.squareSideLength), 
                    self.y + 
                    (vPos * self.squareSideLength 
                        if is_horizontal 
                        else vPos * self.squareSideLength + self.separatorLength)))
        except:
            isOutOfBounds = True
            pass

        if not isOutOfBounds:
            alreadyPlaced = board[vPos][hPos]
        else:
            alreadyPlaced = False


        # 点击事件
        ret = None
        if (self.turn and pygame.mouse.get_pressed()[0] and not alreadyPlaced and not isOutOfBounds and self.turn == True and self.justPlaced <= 0):
            self.justPlaced = 10
            if (is_horizontal):
                self.boardH[vPos][hPos] = True
                ret = {"x":hPos, "y":vPos, "h": True}
            else:
                self.boardV[vPos][hPos] = True
                ret = {"x":hPos, "y":vPos, "h": False}
            ret["point"] = self.isGetPoint(hPos, vPos, is_horizontal)
        return ret

    def placeLine(self, x, y, h, point, win):
        board = self.boardH if h else self.boardV
        board[y][x] = True
        if point != None:
            if win:
                self.ownerBoard[point["y"]][point["x"]] = "win"
            else:
                self.ownerBoard[point["y"]][point["x"]] = "lose"

    def setHome(self):
        self.marker = self.greenplayer
        self.othermarker = self.yellowplayer

    def setAway(self):
        self.marker = self.yellowplayer
        self.othermarker = self.greenplayer

    def draw(self, screen):
        # screen.set_clip(self.x, self.y, self.width, self.height)
        if self.justPlaced > 0:
            self.justPlaced -= 1
        self.background.draw(screen)
        self.drawBoard(screen)
        return self.mouseEvent(screen)


